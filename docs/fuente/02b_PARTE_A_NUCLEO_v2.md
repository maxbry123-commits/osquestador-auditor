# SALIDA 2 v2.0 — PARTE A: NÚCLEO
## Paquete `orchestrator/` — kernel + contratos + store

Despliegue: `pip install requests pyyaml` → copiar paquete → `python3 -m orchestrator`.
Kernel agnóstico: jamás nombra plugins; todo se descubre por carpeta+manifest.

---

## `orchestrator/base/contracts.py`

```python
# -*- coding: utf-8 -*-
"""Contratos universales. El kernel SOLO conoce estas interfaces."""
from dataclasses import dataclass, field

IFACE_INPUT = "input.v1"; IFACE_OUTPUT = "output.v1"; IFACE_AGENT = "agent.v1"

@dataclass
class Document:
    doc_id: str = ""          # sha256 al materializar
    origen: str = ""          # nombre del input plugin
    proyecto: str = "general"
    nombre: str = ""
    tipo: str = ""            # md|txt|pdf|img|comando|...
    ruta: str = ""            # path local materializado
    texto: str = ""
    meta: dict = field(default_factory=dict)

@dataclass
class Health:
    status: str = "ok"        # ok|degraded|down
    latency_ms: int = 0
    detail: str = ""

class InputAdapter:
    name = "base"; iface = IFACE_INPUT
    def __init__(self, config, kv): self.config, self.kv = config, kv
    def discover(self) -> list: raise NotImplementedError   # -> [Document]
    def ack(self, doc: Document): pass
    def health(self) -> Health: return Health()

class OutputConnector:
    name = "base"; iface = IFACE_OUTPUT; capability = ""
    def __init__(self, config): self.config = config
    def call(self, accion: str, payload: dict) -> dict: raise NotImplementedError
    def health(self) -> Health: return Health()

class AgentAdapter:
    name = "base"; iface = IFACE_AGENT
    def __init__(self, config): self.config = config
    def capabilities(self) -> list: return []
    def execute(self, capability: str, payload: dict, ctx: dict) -> dict:
        raise NotImplementedError
    def health(self) -> Health: return Health()
```

---

## `orchestrator/base/resilience.py`

```python
# -*- coding: utf-8 -*-
import os, json, time, uuid, signal, random, hashlib, threading
from datetime import datetime, timezone

def now(): return datetime.now(timezone.utc).isoformat()
def new_id(): return uuid.uuid4().hex[:12]

def atomic_write_json(path, data):
    tmp = f"{path}.{uuid.uuid4().hex}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)

def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except Exception: return default

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""): h.update(c)
    return h.hexdigest()

_LOG_PATH = None
def init_log(path): 
    global _LOG_PATH; _LOG_PATH = path
def jlog(**kw):
    kw.setdefault("ts", now())
    line = json.dumps(kw, ensure_ascii=False)
    print(line, flush=True)
    if _LOG_PATH:
        with open(_LOG_PATH, "a", encoding="utf-8") as f: f.write(line + "\n")

_shutdown = threading.Event()
def _sig(*_): _shutdown.set()
def install_signals():
    signal.signal(signal.SIGTERM, _sig); signal.signal(signal.SIGINT, _sig)
def shutting_down(): return _shutdown.is_set()
def wait(sec): _shutdown.wait(sec)

class CircuitBreaker:
    def __init__(self, name, threshold=5, cooldown=60, enabled=True):
        self.name, self.t, self.cd, self.enabled = name, threshold, cooldown, enabled
        self.fails, self.opened = 0, None
    def allow(self):
        if not self.enabled: return True
        if self.opened and time.time() - self.opened > self.cd:
            self.opened, self.fails = None, 0
        return self.opened is None
    def ok(self): self.fails = 0
    def fail(self):
        self.fails += 1
        if self.fails >= self.t: self.opened = time.time()

def backoff(i, base=0.5, cap=10.0):
    d = min(cap, base * 2 ** i); return d + d * 0.1 * random.random()
```

---

## `orchestrator/store/db.py`

```python
# -*- coding: utf-8 -*-
"""SQLite: única fuente de estado estructurado (WAL). Journal = replay."""
import sqlite3, json
from ..base.resilience import now, new_id

SCHEMA = """
CREATE TABLE IF NOT EXISTS inventory(
  hash TEXT PRIMARY KEY, proyecto TEXT, nombre TEXT, vault TEXT,
  estado TEXT, parents TEXT DEFAULT '', ts TEXT);
CREATE INDEX IF NOT EXISTS ix_inv ON inventory(proyecto, estado);
CREATE TABLE IF NOT EXISTS conflictos(
  id TEXT PRIMARY KEY, proyecto TEXT, doc_a TEXT, doc_b TEXT,
  similitud REAL, estado TEXT, ts TEXT);
CREATE INDEX IF NOT EXISTS ix_conf ON conflictos(proyecto, estado);
CREATE TABLE IF NOT EXISTS tareas(
  id TEXT PRIMARY KEY, proyecto TEXT, titulo TEXT, etiqueta TEXT,
  estado TEXT, remoto_id TEXT, ts TEXT, UNIQUE(proyecto, titulo));
CREATE TABLE IF NOT EXISTS journal(
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, wf TEXT, step TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT);
"""

class DB:
    def __init__(self, path):
        self.c = sqlite3.connect(path, check_same_thread=False)
        self.c.execute("PRAGMA journal_mode=WAL")
        self.c.executescript(SCHEMA); self.c.commit()
    def _x(self, q, a=()):
        cur = self.c.execute(q, a); self.c.commit(); return cur
    # inventario (estados: ingresado→auditado|conflicto|duplicado→en_arbol)
    def inv_add(self, h, proyecto, nombre, vault):
        self._x("INSERT OR IGNORE INTO inventory VALUES(?,?,?,?,?,?,?)",
                (h, proyecto, nombre, vault, "ingresado", "", now()))
    def inv_get(self, h):
        r = self._x("SELECT * FROM inventory WHERE hash=?", (h,)).fetchone()
        return r and dict(zip(["hash","proyecto","nombre","vault","estado",
                               "parents","ts"], r))
    def inv_estado(self, h, estado, parents=None):
        if parents is not None:
            self._x("UPDATE inventory SET estado=?, parents=? WHERE hash=?",
                    (estado, parents, h))
        else:
            self._x("UPDATE inventory SET estado=? WHERE hash=?", (estado, h))
    def inv_por(self, proyecto=None, estado=None):
        q, a = "SELECT * FROM inventory WHERE 1=1", []
        if proyecto: q += " AND proyecto=?"; a.append(proyecto)
        if estado: q += " AND estado=?"; a.append(estado)
        return [dict(zip(["hash","proyecto","nombre","vault","estado",
                          "parents","ts"], r)) for r in self._x(q, a)]
    # conflictos
    def conf_add(self, proyecto, a, b, sim):
        cid = new_id()
        self._x("INSERT INTO conflictos VALUES(?,?,?,?,?,?,?)",
                (cid, proyecto, a, b, sim, "abierto", now()))
        return cid
    def conf_abiertos(self, proyecto=None):
        q, a = "SELECT * FROM conflictos WHERE estado='abierto'", []
        if proyecto: q += " AND proyecto=?"; a.append(proyecto)
        return [dict(zip(["id","proyecto","doc_a","doc_b","similitud",
                          "estado","ts"], r)) for r in self._x(q, a)]
    def conf_resolver(self, cid, estado):
        self._x("UPDATE conflictos SET estado=? WHERE id=?", (estado, cid))
        r = self._x("SELECT * FROM conflictos WHERE id=?", (cid,)).fetchone()
        return r and dict(zip(["id","proyecto","doc_a","doc_b","similitud",
                               "estado","ts"], r))
    # tareas (UNIQUE evita duplicar DEFINIR)
    def tarea_add(self, proyecto, titulo, etiqueta, remoto_id=""):
        self._x("INSERT OR IGNORE INTO tareas VALUES(?,?,?,?,?,?,?)",
                (new_id(), proyecto, titulo, etiqueta, "pendiente",
                 remoto_id, now()))
    def tareas(self, proyecto):
        return [dict(zip(["id","proyecto","titulo","etiqueta","estado",
                          "remoto_id","ts"], r)) for r in
                self._x("SELECT * FROM tareas WHERE proyecto=?", (proyecto,))]
    # journal + kv
    def j(self, wf, step, payload):
        self._x("INSERT INTO journal(ts,wf,step,payload) VALUES(?,?,?,?)",
                (now(), wf, step, json.dumps(payload, ensure_ascii=False)))
    def kv_get(self, k, d=""):
        r = self._x("SELECT v FROM kv WHERE k=?", (k,)).fetchone()
        return r[0] if r else d
    def kv_set(self, k, v):
        self._x("INSERT INTO kv VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=?",
                (k, str(v), str(v)))
```

---

## `orchestrator/kernel/managers.py`

```python
# -*- coding: utf-8 -*-
"""Descubrimiento de plugins + AgentManager con fallback_chain.
El kernel NUNCA importa plugins por nombre: importlib sobre carpetas."""
import os, importlib.util
from ..base.resilience import read_json, jlog, CircuitBreaker

def _load(dirpath, clsbase, pkg_base):
    m = read_json(os.path.join(dirpath, "manifest.json"), None)
    if not m or m.get("status", "active") != "active": return None, None
    ap = os.path.join(dirpath, "adapter.py")
    if not os.path.exists(ap): return m, None
    # FIX v2.1: nombre paquetizado -> imports relativos (...) funcionan
    import sys
    parent = os.path.dirname(pkg_base)
    if parent not in sys.path: sys.path.insert(0, parent)
    rel = os.path.relpath(ap, parent).replace(os.sep, ".")[:-3]
    spec = importlib.util.spec_from_file_location(rel, ap)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[rel] = mod
    spec.loader.exec_module(mod)
    for v in vars(mod).values():
        if isinstance(v, type) and issubclass(v, clsbase) and v is not clsbase:
            return m, v
    return m, None

class Registry:
    """Escanea inputs/ outputs/ agents/. Hot-reload por mtime."""
    def __init__(self, base, contracts, config, kv):
        self.base, self.ct, self.config, self.kv = base, contracts, config, kv
        self.inputs, self.outputs, self.agents = {}, {}, {}
        self._mtimes = {}
    def _dirty(self, root):
        t = 0
        for d in os.listdir(root):
            p = os.path.join(root, d, "manifest.json")
            if os.path.exists(p): t = max(t, os.path.getmtime(p))
        if self._mtimes.get(root) != t:
            self._mtimes[root] = t; return True
        return False
    def scan(self, force=False):
        for root, store, base_cls, mk in [
            (os.path.join(self.base, "inputs"), self.inputs,
             self.ct.InputAdapter, lambda c: c(self.config, self.kv)),
            (os.path.join(self.base, "outputs"), self.outputs,
             self.ct.OutputConnector, lambda c: c(self.config)),
            (os.path.join(self.base, "agents"), self.agents,
             self.ct.AgentAdapter, lambda c: c(self.config))]:
            if not (force or self._dirty(root)): continue
            store.clear()
            for d in sorted(os.listdir(root)):
                if d.startswith("_"): continue
                m, cls = _load(os.path.join(root, d), base_cls, self.base)
                if m and cls:
                    try:
                        store[m["name"]] = {"manifest": m, "obj": mk(cls)}
                        jlog(level="info", ev="plugin_load", name=m["name"])
                    except Exception as e:
                        jlog(level="error", ev="plugin_fail",
                             name=m.get("name"), err=str(e))

class AgentManager:
    """capability → cadena de agentes por prioridad; breaker por capacidad."""
    def __init__(self, registry, mode="prod"):
        self.r = registry
        self.breakers = {}
        self.enabled = mode != "dev"
    def _chain(self, cap):
        c = []
        for name, e in self.r.agents.items():
            caps = e["manifest"].get("capabilities", [])
            if cap in caps:
                c.append((e["manifest"].get("priority", 9), name, e["obj"]))
        return [x[1:] for x in sorted(c)]
    def execute(self, cap, payload, ctx):
        br = self.breakers.setdefault(cap,
             CircuitBreaker(cap, 5, 300, self.enabled))
        last = None
        for name, obj in self._chain(cap):
            if not br.allow(): break
            try:
                r = obj.execute(cap, payload, ctx); br.ok()
                return {"ok": True, "agent": name, "result": r}
            except Exception as e:
                last = e; br.fail()
                jlog(level="warn", ev="agent_fail", agent=name,
                     cap=cap, err=str(e))
        return {"ok": False, "error": str(last) if last
                else f"sin agente para {cap}"}

class OutputManager:
    """capability de salida → conector. Kernel jamás dice 'telegram'."""
    def __init__(self, registry): self.r = registry
    def call(self, capability, accion, payload):
        for e in self.r.outputs.values():
            if e["manifest"].get("capability") == capability:
                return e["obj"].call(accion, payload)
        return {"ok": False, "error": f"sin conector {capability}"}
```

---

## `orchestrator/kernel/motor.py`

```python
# -*- coding: utf-8 -*-
"""Intérprete declarativo de workflows (YAML o JSON). Sin lógica de negocio."""
import os, json
from ..base.resilience import jlog
try:
    import yaml
except ImportError:
    yaml = None

def load_workflows(path):
    wfs = {}
    for fn in os.listdir(path):
        p = os.path.join(path, fn)
        try:
            if fn.endswith((".yaml", ".yml")) and yaml:
                w = yaml.safe_load(open(p, encoding="utf-8"))
            elif fn.endswith(".json"):
                w = json.load(open(p, encoding="utf-8"))
            else: continue
            wfs[w["trigger"]] = w
        except Exception as e:
            jlog(level="error", ev="wf_load", file=fn, err=str(e))
    return wfs

def _when(cond, ctx):
    if not cond: return True
    v = ctx.get(cond.get("campo"))
    if "in" in cond: return v in cond["in"]
    if "eq" in cond: return v == cond["eq"]
    if "truthy" in cond: return bool(v) == cond["truthy"]
    return True

def run(wf, ctx, agents, outputs, db):
    for step in wf["steps"]:
        if not _when(step.get("when"), ctx): continue
        sid = step["id"]
        try:
            if "capability" in step:
                r = agents.execute(step["capability"],
                                   step.get("params", {}), ctx)
            elif "connector" in step:
                r = outputs.call(step["connector"], step.get("accion", "call"),
                                 {**step.get("params", {}), "ctx_doc":
                                  {k: ctx.get(k) for k in
                                   ("hash","proyecto","nombre","texto")}})
            else:
                r = {"ok": True}
            ctx[f"step.{sid}"] = r
            db.j(wf.get("id","wf"), sid,
                 {"ok": r.get("ok"), "agent": r.get("agent","")})
            if not r.get("ok") and step.get("on_error") == "stop":
                return ctx
            # branch: resultado puede fijar campos de ctx
            res = r.get("result")
            if isinstance(res, dict): ctx.update(res)
        except Exception as e:
            jlog(level="error", ev="step_fail", wf=wf.get("id"),
                 step=sid, err=str(e))
            if step.get("on_error") == "stop": return ctx
    return ctx
```

---

## `orchestrator/kernel/commands.py`

```python
# -*- coding: utf-8 -*-
"""Comandos del usuario (/estado /conflictos /resolver /frontera /handoff).
Opera SOLO sobre DB + OutputManager por capacidad."""

def handle(texto, db, outputs):
    p = texto.strip().split()
    cmd = p[0].lower() if p else ""
    if cmd == "/estado":
        docs = len(db.inv_por()); conf = len(db.conf_abiertos())
        return f"📊 Docs: {docs} | Conflictos abiertos: {conf}"
    if cmd == "/conflictos":
        cs = db.conf_abiertos()
        if not cs: return "✅ Sin conflictos abiertos."
        return "\n".join(f"{c['id']}: [{c['proyecto']}] "
                         f"{c['doc_a'][:8]} vs {c['doc_b'][:8]} "
                         f"(sim {c['similitud']})" for c in cs[:20])
    if cmd == "/resolver" and len(p) >= 3:
        cid, dec = p[1], p[2].upper()
        c = db.conf_resolver(cid, f"resuelto_{dec}")
        if not c: return "❌ Conflicto no encontrado."
        gana = c["doc_a"] if dec == "A" else c["doc_b"]
        pierde = c["doc_b"] if dec == "A" else c["doc_a"]
        if dec in ("A", "B"):
            db.inv_estado(gana, "auditado")           # re-entra al árbol
            db.inv_estado(pierde, "archivado", parents=gana)  # lineage
            return f"✅ {cid}: gana {gana[:8]}, {pierde[:8]} archivado."
        if dec == "FUSION":
            db.tarea_add(c["proyecto"],
                         f"FUSIONAR {c['doc_a'][:8]}+{c['doc_b'][:8]}",
                         "FUSION")
            return f"🔀 {cid}: fusión solicitada. Sube el doc fusionado."
        return "Uso: /resolver <id> A|B|FUSION"
    if cmd == "/frontera" and len(p) >= 2:
        pr = p[1]
        conf = len(db.conf_abiertos(pr))
        pend = len(db.inv_por(pr, "ingresado"))
        ok = conf == 0 and pend == 0 and len(db.inv_por(pr)) > 0
        return (f"{'✅ FRONTERA OK' if ok else '⏳ Pendiente'} — "
                f"{pr}: {conf} conflictos, {pend} sin auditar")
    if cmd == "/handoff" and len(p) >= 2:
        r = outputs.call("handoff", "export", {"proyecto": p[1]})
        return f"📦 Handoff: {r.get('path', r.get('error'))}"
    return ("Comandos: /estado /conflictos /resolver <id> A|B|FUSION "
            "/frontera <proyecto> /handoff <proyecto>")
```

---

## `orchestrator/kernel/core.py`

```python
# -*- coding: utf-8 -*-
"""Kernel. boot→pump→shutdown. Agnóstico: cero nombres de plugins."""
import os
from ..base import contracts as ct
from ..base.resilience import (atomic_write_json, read_json, init_log, jlog,
                               install_signals, shutting_down, wait, now)
from ..store.db import DB
from . import motor, commands
from .managers import Registry, AgentManager, OutputManager

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(BASE, *a)

DEFAULT_CONFIG = {
    "mode": "prod", "poll_seconds": 10,
    "telegram": {"token": "", "chat_id": ""},
    "kanboard": {"url": "", "user": "jsonrpc", "token": "", "project_id": 1},
    "graphiti": {"mcp_url": ""}, "obsidian": {"vault_path": ""},
    "mcp_server": {"enabled": True, "port": 8765},
    "similitud_duplicado": 0.98, "similitud_version": 0.70
}
DIRS = ["inputs/_template", "outputs/_template", "agents/_template",
        "skills", "workflows", "state", "inbox", "archive", "vault",
        "handoff", "mcp", "tools"]

def boot():
    for d in DIRS: os.makedirs(P(d), exist_ok=True)
    if not os.path.exists(P("config.json")):
        atomic_write_json(P("config.json"), DEFAULT_CONFIG)
    init_log(P("state", "log.jsonl"))
    cfg = read_json(P("config.json"), DEFAULT_CONFIG)
    db = DB(P("state", "state.db"))
    reg = Registry(BASE, ct, cfg, db)
    reg.scan(force=True)
    agents = AgentManager(reg, cfg.get("mode", "prod"))
    outputs = OutputManager(reg)
    wfs = motor.load_workflows(P("workflows"))
    return cfg, db, reg, agents, outputs, wfs

def _health(db, status, step=""):
    atomic_write_json(P("state", "health.json"),
                      {"ts": now(), "status": status, "step": step})

def _recover(db, wfs, agents, outputs):
    """Docs atascados en 'ingresado' (kill -9 previo) → re-auditar."""
    for row in db.inv_por(estado="ingresado"):
        ctx = {"hash": row["hash"], "proyecto": row["proyecto"],
               "nombre": row["nombre"], "vault": row["vault"],
               "texto": open(row["vault"], encoding="utf-8",
                             errors="replace").read(), "tipo": "recuperado"}
        wf = wfs.get("document.audit")
        if wf: motor.run(wf, ctx, agents, outputs, db)

def pump():
    install_signals()
    cfg, db, reg, agents, outputs, wfs = boot()
    if cfg.get("mcp_server", {}).get("enabled"):
        try:
            from ..mcp.server import start_bg
            start_bg(db, cfg["mcp_server"].get("port", 8765))
        except Exception as e:
            jlog(level="warn", ev="mcp_off", err=str(e))
    jlog(level="info", ev="boot", mode=cfg.get("mode"))
    _recover(db, wfs, agents, outputs)
    while not shutting_down():
        reg.scan()                                   # hot-reload
        tocados = set()
        for e in list(reg.inputs.values()):
            try: docs = e["obj"].discover()
            except Exception as ex:
                jlog(level="warn", ev="input_fail",
                     name=e["manifest"]["name"], err=str(ex)); continue
            for doc in docs:
                if shutting_down(): break
                _health(db, "alive", doc.nombre)
                if doc.tipo == "comando":
                    resp = commands.handle(doc.texto, db, outputs)
                    outputs.call("notify", "send", {"text": resp}); continue
                ctx = {"proyecto": doc.proyecto, "nombre": doc.nombre,
                       "ruta": doc.ruta, "tipo": doc.tipo,
                       "origen": doc.origen, "texto": doc.texto}
                wf = wfs.get("document.new")
                if wf:
                    ctx = motor.run(wf, ctx, agents, outputs, db)
                    if ctx.get("resultado_auditoria") == "unico":
                        tocados.add(ctx["proyecto"])
                try: e["obj"].ack(doc)
                except Exception: pass
        # re-entrada de docs auditados (post-/resolver) al árbol
        for row in db.inv_por(estado="auditado"):
            ctx = {"hash": row["hash"], "proyecto": row["proyecto"],
                   "nombre": row["nombre"], "vault": row["vault"],
                   "texto": open(row["vault"], encoding="utf-8",
                                 errors="replace").read()}
            wf = wfs.get("document.tree")
            if wf:
                motor.run(wf, ctx, agents, outputs, db)
                db.inv_estado(row["hash"], "en_arbol")
                tocados.add(row["proyecto"])
        for proyecto in tocados:
            wf = wfs.get("project.taskindex")
            if wf: motor.run(wf, {"proyecto": proyecto},
                             agents, outputs, db)
        _health(db, "alive", "idle")
        wait(cfg.get("poll_seconds", 10))
    _health(db, "shutdown"); jlog(level="info", ev="shutdown")
```

---

## `orchestrator/__main__.py`

```python
from .kernel.core import pump
if __name__ == "__main__":
    pump()
```

Parte B: plugins (inputs, outputs, agentes, workflows). Parte C: MCP + tools + despliegue.
