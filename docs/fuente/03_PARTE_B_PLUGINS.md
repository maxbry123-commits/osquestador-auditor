# SALIDA 2 v2.0 — PARTE B: PLUGINS
## inputs/ outputs/ agents/ workflows/ — cada uno carpeta + manifest + adapter

---

## `orchestrator/inputs/inbox/manifest.json`
```json
{"type":"input","name":"inbox","version":"2.0","iface":"input.v1","status":"active"}
```

## `orchestrator/inputs/inbox/adapter.py`
```python
import os, shutil
from ...base.contracts import InputAdapter, Document

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class InboxInput(InputAdapter):
    name = "inbox"
    def discover(self):
        docs, root = [], os.path.join(BASE, "inbox")
        for proyecto in os.listdir(root):
            pd = os.path.join(root, proyecto)
            if not os.path.isdir(pd): continue
            for fn in os.listdir(pd):
                fp = os.path.join(pd, fn)
                if os.path.isfile(fp):
                    ext = os.path.splitext(fn)[1].lower().strip(".")
                    docs.append(Document(origen="inbox", proyecto=proyecto,
                                         nombre=fn, tipo=ext, ruta=fp))
        return docs
    def ack(self, doc):
        d = os.path.join(BASE, "archive", doc.proyecto)
        os.makedirs(d, exist_ok=True)
        dest = os.path.join(d, doc.nombre)
        if os.path.exists(dest):                       # colisión: sufijo
            base, ext = os.path.splitext(doc.nombre)
            dest = os.path.join(d, f"{base}_{abs(hash(doc.ruta))%10**8}{ext}")
        shutil.move(doc.ruta, dest)
```

---

## `orchestrator/inputs/telegram/manifest.json`
```json
{"type":"input","name":"telegram","version":"2.0","iface":"input.v1","status":"active"}
```

## `orchestrator/inputs/telegram/adapter.py`
```python
import os, time
from ...base.contracts import InputAdapter, Document
from ...base.resilience import CircuitBreaker
try:
    import requests
except ImportError:
    requests = None

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TelegramInput(InputAdapter):
    name = "telegram"
    def __init__(self, config, kv):
        super().__init__(config, kv)
        self.token = config.get("telegram", {}).get("token", "")
        self.br = CircuitBreaker("tg-in")
    def discover(self):
        if not (self.token and requests and self.br.allow()): return []
        # offset inicial -1: solo el último update; backlog histórico se
        # descarta a propósito (evita clasificar backlog como general)
        off = int(self.kv.kv_get("tg_offset", "-1"))
        try:
            r = requests.get(
                f"https://api.telegram.org/bot{self.token}/getUpdates",
                params={"offset": off + 1 if off >= 0 else -1, "timeout": 0},
                timeout=15).json()
            self.br.ok()
        except Exception:
            self.br.fail(); return []
        docs = []
        import re
        for u in r.get("result", []):
            off = max(off, u["update_id"])
            msg = u.get("message") or {}
            texto = msg.get("caption") or msg.get("text") or ""
            if texto.startswith("/"):
                docs.append(Document(origen="telegram", tipo="comando",
                                     texto=texto)); continue
            proyecto = "telegram_general"
            m = re.search(r"#(\w+)", texto)
            if m: proyecto = m.group(1)
            if "document" in msg:
                fid = msg["document"]["file_id"]
                fname = msg["document"].get("file_name", fid)
                try:
                    fp = requests.get(
                        f"https://api.telegram.org/bot{self.token}/getFile",
                        params={"file_id": fid}, timeout=15
                    ).json()["result"]["file_path"]
                    data = requests.get(
                        f"https://api.telegram.org/file/bot{self.token}/{fp}",
                        timeout=60).content
                    d = os.path.join(BASE, "inbox", proyecto)
                    os.makedirs(d, exist_ok=True)
                    local = os.path.join(d, fname)
                    open(local, "wb").write(data)
                    # lo materializa en inbox: el input inbox lo levanta
                except Exception: pass
            elif texto.strip():
                d = os.path.join(BASE, "inbox", proyecto)
                os.makedirs(d, exist_ok=True)
                open(os.path.join(d, f"nota_{int(time.time())}.md"),
                     "w", encoding="utf-8").write(texto)
        self.kv.kv_set("tg_offset", off)
        return docs   # solo comandos; archivos van vía inbox
```

---

## `orchestrator/outputs/obsidian/manifest.json`
```json
{"type":"output","name":"obsidian","version":"2.0","iface":"output.v1","capability":"vault","status":"active"}
```

## `orchestrator/outputs/obsidian/adapter.py`
```python
import os
from ...base.contracts import OutputConnector
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ObsidianOut(OutputConnector):
    name = "obsidian"; capability = "vault"
    def call(self, accion, p):
        root = self.config.get("obsidian", {}).get("vault_path") or \
               os.path.join(BASE, "vault")
        if accion == "save":
            d = os.path.join(root, p["proyecto"]); os.makedirs(d, exist_ok=True)
            nombre = p["nombre"]
            path = os.path.join(d, nombre)
            if os.path.exists(path) and p.get("hash"):     # colisión
                b, e = os.path.splitext(nombre)
                path = os.path.join(d, f"{b}_{p['hash'][:8]}{e}")
            open(path, "w", encoding="utf-8").write(p["contenido"])
            return {"ok": True, "path": path}
        return {"ok": False, "error": f"accion {accion}"}
```

---

## `orchestrator/outputs/kanboard/manifest.json`
```json
{"type":"output","name":"kanboard","version":"2.0","iface":"output.v1","capability":"taskboard","status":"active"}
```

## `orchestrator/outputs/kanboard/adapter.py`
```python
import uuid
from ...base.contracts import OutputConnector
from ...base.resilience import CircuitBreaker, jlog
try:
    import requests
except ImportError:
    requests = None

class KanboardOut(OutputConnector):
    name = "kanboard"; capability = "taskboard"
    def __init__(self, config):
        super().__init__(config)
        k = config.get("kanboard", {})
        self.url, self.user = k.get("url", ""), k.get("user", "jsonrpc")
        self.token, self.pid = k.get("token", ""), k.get("project_id", 1)
        self.br = CircuitBreaker("kanboard")
    def _rpc(self, method, params):
        r = requests.post(self.url, auth=(self.user, self.token), timeout=15,
            json={"jsonrpc": "2.0", "method": method,
                  "id": uuid.uuid4().hex, "params": params})
        r.raise_for_status(); return r.json().get("result")
    def call(self, accion, p):
        if accion == "crear_tarea":
            remoto = ""
            if self.url and requests and self.br.allow():
                try:
                    remoto = str(self._rpc("createTask",
                        {"title": p["titulo"], "project_id": self.pid,
                         "description": p.get("descripcion", "")}))
                    self.br.ok()
                except Exception as e:
                    self.br.fail()
                    jlog(level="warn", ev="kanboard_local", err=str(e))
            # única fuente de verdad = SQLite; remoto_id solo si hubo éxito
            return {"ok": True, "remoto_id": remoto}
        return {"ok": False, "error": f"accion {accion}"}
```

---

## `orchestrator/outputs/graphiti/manifest.json`
```json
{"type":"output","name":"graphiti","version":"2.0","iface":"output.v1","capability":"graph","status":"active"}
```

## `orchestrator/outputs/graphiti/adapter.py`
```python
import os
from ...base.contracts import OutputConnector
from ...base.resilience import read_json, atomic_write_json, now, CircuitBreaker
try:
    import requests
except ImportError:
    requests = None

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GraphitiOut(OutputConnector):
    name = "graphiti"; capability = "graph"
    def __init__(self, config):
        super().__init__(config)
        self.url = config.get("graphiti", {}).get("mcp_url", "")
        self.local = os.path.join(BASE, "state", "graph.json")
        self.br = CircuitBreaker("graphiti")
    def call(self, accion, p):
        if accion == "bulk_edges":
            edges = p["edges"]
            for e in edges: e["ts"] = now()
            if self.url and requests and self.br.allow():
                try:
                    requests.post(self.url.rstrip("/") + "/edges/bulk",
                                  json={"edges": edges}, timeout=20)
                    self.br.ok(); return {"ok": True, "remote": True}
                except Exception: self.br.fail()
            g = read_json(self.local, {"edges": []})
            g["edges"].extend(edges); atomic_write_json(self.local, g)
            return {"ok": True, "remote": False}
        if accion == "edges":
            g = read_json(self.local, {"edges": []})
            return {"ok": True, "edges": [e for e in g["edges"]
                    if e.get("proyecto") == p.get("proyecto")]}
        return {"ok": False, "error": f"accion {accion}"}
```

---

## `orchestrator/outputs/telegram_notify/manifest.json`
```json
{"type":"output","name":"telegram_notify","version":"2.0","iface":"output.v1","capability":"notify","status":"active"}
```

## `orchestrator/outputs/telegram_notify/adapter.py`
```python
from ...base.contracts import OutputConnector
from ...base.resilience import CircuitBreaker
try:
    import requests
except ImportError:
    requests = None

class TgNotify(OutputConnector):
    name = "telegram_notify"; capability = "notify"
    def __init__(self, config):
        super().__init__(config)
        t = config.get("telegram", {})
        self.token, self.chat = t.get("token", ""), t.get("chat_id", "")
        self.br = CircuitBreaker("tg-out")
    def call(self, accion, p):
        if not (self.token and self.chat and requests and self.br.allow()):
            return {"ok": False, "error": "sin config"}
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": self.chat, "text": p["text"][:4000]},
                timeout=10)
            self.br.ok(); return {"ok": True}
        except Exception as e:
            self.br.fail(); return {"ok": False, "error": str(e)}
```

---

## `orchestrator/outputs/handoff/manifest.json`
```json
{"type":"output","name":"handoff","version":"2.0","iface":"output.v1","capability":"handoff","status":"active"}
```

## `orchestrator/outputs/handoff/adapter.py`
```python
import os, json, shutil
from ...base.contracts import OutputConnector
from ...base.resilience import atomic_write_json, now
from ...store.db import DB

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class HandoffOut(OutputConnector):
    """Paquete de entrega a Fase 1: árbol + tareas + docs índice."""
    name = "handoff"; capability = "handoff"
    def call(self, accion, p):
        if accion != "export": return {"ok": False}
        proyecto = p["proyecto"]
        db = DB(os.path.join(BASE, "state", "state.db"))
        d = os.path.join(BASE, "handoff", proyecto); os.makedirs(d, exist_ok=True)
        docs = db.inv_por(proyecto)
        conf = db.conf_abiertos(proyecto)
        pkg = {"proyecto": proyecto, "ts": now(),
               "frontera_ok": len(conf) == 0 and len(docs) > 0,
               "docs": docs, "tareas": db.tareas(proyecto),
               "conflictos_abiertos": conf}
        atomic_write_json(os.path.join(d, "handoff.json"), pkg)
        raiz = os.path.join(BASE, "vault", proyecto, "README_RAIZ.md")
        if os.path.exists(raiz):
            shutil.copy(raiz, os.path.join(d, "README_RAIZ.md"))
        return {"ok": True, "path": d, "frontera_ok": pkg["frontera_ok"]}
```

---

## `orchestrator/agents/ocr/manifest.json`
```json
{"type":"agent","name":"ocr","version":"2.0","iface":"agent.v1","capabilities":["ocr"],"priority":1,"status":"active"}
```

## `orchestrator/agents/ocr/adapter.py`
```python
import os
from ...base.contracts import AgentAdapter
TEXT_EXT = {"md","txt","py","json","html","csv","yaml","yml"}

class OCRAgent(AgentAdapter):
    name = "ocr"
    def capabilities(self): return ["ocr"]
    def execute(self, cap, p, ctx):
        ruta, tipo = ctx.get("ruta", ""), ctx.get("tipo", "")
        if tipo in TEXT_EXT and os.path.exists(ruta):
            return {"texto": open(ruta, encoding="utf-8",
                                  errors="replace").read(),
                    "requiere_ocr": False}
        # binario: NO texto placeholder — se marca y NO entra a auditoría
        return {"texto": "", "requiere_ocr": True}
```

---

## `orchestrator/agents/haystack/manifest.json`
```json
{"type":"agent","name":"haystack","version":"2.0","iface":"agent.v1","capabilities":["similitud"],"priority":1,"status":"active"}
```

## `orchestrator/agents/haystack/adapter.py`
```python
import difflib
from ...base.contracts import AgentAdapter

class HaystackAgent(AgentAdapter):
    name = "haystack"
    def capabilities(self): return ["similitud"]
    def execute(self, cap, p, ctx):
        a, b = p.get("a", ctx.get("texto", "")), p.get("b", "")
        return {"similitud": difflib.SequenceMatcher(
            None, a[:20000], b[:20000]).ratio()}
```

---

## `orchestrator/agents/auditor/manifest.json`
```json
{"type":"agent","name":"auditor","version":"2.0","iface":"agent.v1","capabilities":["auditoria"],"priority":1,"status":"active"}
```

## `orchestrator/agents/auditor/adapter.py`
```python
"""Auditoría de corpus: duplicado / versión(conflicto) / único + lineage."""
import os
from ...base.contracts import AgentAdapter
from ...store.db import DB
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AuditorAgent(AgentAdapter):
    name = "auditor"
    def capabilities(self): return ["auditoria"]
    def execute(self, cap, p, ctx):
        import difflib
        db = DB(os.path.join(BASE, "state", "state.db"))
        h, proyecto = ctx["hash"], ctx["proyecto"]
        texto = ctx.get("texto", "")
        dup = float(p.get("similitud_duplicado", 0.98))
        ver = float(p.get("similitud_version", 0.70))
        for row in db.inv_por(proyecto):
            if row["hash"] == h or row["estado"] in ("archivado",): continue
            try:
                otro = open(row["vault"], encoding="utf-8",
                            errors="replace").read()
            except Exception: continue
            sim = difflib.SequenceMatcher(None, texto[:20000],
                                          otro[:20000]).ratio()
            if sim >= dup:
                db.inv_estado(h, "duplicado", parents=row["hash"])
                return {"resultado_auditoria": "duplicado"}
            if sim >= ver:
                cid = db.conf_add(proyecto, h, row["hash"], round(sim, 2))
                db.inv_estado(h, "conflicto", parents=row["hash"])
                return {"resultado_auditoria": "conflicto",
                        "conflicto_id": cid, "sim": round(sim, 2),
                        "contra": row["nombre"]}
        db.inv_estado(h, "auditado")
        return {"resultado_auditoria": "unico"}
```

---

## `orchestrator/agents/arbolista/manifest.json`
```json
{"type":"agent","name":"arbolista","version":"2.0","iface":"agent.v1","capabilities":["arbol"],"priority":1,"status":"active"}
```

## `orchestrator/agents/arbolista/adapter.py`
```python
"""Extrae piezas del doc: objetivos, decisiones, repos, urls, archivos código."""
import re
from ...base.contracts import AgentAdapter

PAT = [("objetivo",  r"^(objetivo|meta|goal)\b[:\-]"),
       ("decision",  r"^(decisi[oó]n|decision)\b[:\-]"),
       ("tarea",     r"^(tarea|task)\b[:\-]")]

class ArbolistaAgent(AgentAdapter):
    name = "arbolista"
    def capabilities(self): return ["arbol"]
    def execute(self, cap, p, ctx):
        texto, nombre = ctx.get("texto", ""), ctx["nombre"]
        edges, piezas = [], []
        proyecto = ctx["proyecto"]
        edges.append({"proyecto": proyecto, "de": nombre,
                      "a": "RAIZ", "tipo": "pertenece_a"})
        for linea in texto.splitlines():
            l = linea.strip()
            for tipo, pat in PAT:
                if re.match(pat, l, re.I):
                    piezas.append({"tipo": tipo, "texto": l})
                    edges.append({"proyecto": proyecto, "de": nombre,
                                  "a": l[:60], "tipo": f"define_{tipo}"})
        for url in re.findall(r"https?://\S+", texto)[:50]:
            t = "repo" if "github.com" in url else "url"
            edges.append({"proyecto": proyecto, "de": nombre,
                          "a": url[:120], "tipo": t})
        for f in re.findall(r"\b[\w\-/]+\.(?:py|md|json|yaml|js|html)\b",
                            texto)[:50]:
            edges.append({"proyecto": proyecto, "de": nombre,
                          "a": f, "tipo": "menciona_archivo"})
        return {"edges": edges, "piezas": piezas}
```

---

## `orchestrator/agents/plandex/manifest.json`
```json
{"type":"agent","name":"plandex","version":"2.0","iface":"agent.v1","capabilities":["planificar"],"priority":1,"status":"active"}
```

## `orchestrator/agents/plandex/adapter.py`
```python
"""Objetivos sin tarea → DEFINIR. Dedup real vía UNIQUE en SQLite."""
import os
from ...base.contracts import AgentAdapter
from ...store.db import DB
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class PlandexAgent(AgentAdapter):
    name = "plandex"
    def capabilities(self): return ["planificar"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        proyecto = ctx["proyecto"]
        # piezas 'objetivo' del grafo local
        from ...base.resilience import read_json
        g = read_json(os.path.join(BASE, "state", "graph.json"),
                      {"edges": []})
        objetivos = {e["a"] for e in g["edges"]
                     if e.get("proyecto") == proyecto
                     and e.get("tipo") == "define_objetivo"}
        nuevas = []
        for o in objetivos:
            titulo = f"[{proyecto}] {o[:80]}"
            antes = len(db.tareas(proyecto))
            db.tarea_add(proyecto, titulo, "DEFINIR")
            if len(db.tareas(proyecto)) > antes:
                nuevas.append(titulo)
        return {"tareas_nuevas": nuevas}
```

---

## `orchestrator/agents/hermes/manifest.json`
```json
{"type":"agent","name":"hermes","version":"2.0","iface":"agent.v1","capabilities":["documentar"],"priority":1,"status":"active"}
```

## `orchestrator/agents/hermes/adapter.py`
```python
"""Consolida README_RAIZ: identidad del proyecto (docs + tabla tareas)."""
import os
from ...base.contracts import AgentAdapter
from ...base.resilience import now
from ...store.db import DB
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class HermesAgent(AgentAdapter):
    name = "hermes"
    def capabilities(self): return ["documentar"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        proyecto = ctx["proyecto"]
        docs = [d["nombre"] for d in db.inv_por(proyecto)
                if d["estado"] in ("auditado", "en_arbol")]
        tareas = db.tareas(proyecto)
        filas = "\n".join(f"| {t['titulo']} | {t['etiqueta']} | "
                          f"{t['estado']} |" for t in tareas) or "| — | | |"
        listado = "\n".join(f"- {d}" for d in docs) or "- (vacío)"
        contenido = (f"# {proyecto} — RAÍZ DEL PROYECTO\n\n"
                     f"Actualizado: {now()}\n\n## Documentos\n{listado}\n\n"
                     f"## Tabla de tareas\n| Tarea | Etiqueta | Estado |\n"
                     f"|---|---|---|\n{filas}\n")
        return {"readme": contenido, "nombre": "README_RAIZ.md",
                "contenido": contenido}
```

---

## `orchestrator/agents/swe/manifest.json`
```json
{"type":"agent","name":"swe","version":"2.0","iface":"agent.v1","capabilities":["frontera"],"priority":1,"status":"active"}
```

## `orchestrator/agents/swe/adapter.py`
```python
"""Audita frontera Fase 0."""
import os
from ...base.contracts import AgentAdapter
from ...store.db import DB
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SWEAgent(AgentAdapter):
    name = "swe"
    def capabilities(self): return ["frontera"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        proyecto = ctx["proyecto"]
        conf = len(db.conf_abiertos(proyecto))
        pend = len(db.inv_por(proyecto, "ingresado")) + \
               len(db.inv_por(proyecto, "conflicto"))
        docs = len(db.inv_por(proyecto))
        ok = conf == 0 and pend == 0 and docs > 0
        return {"frontera_ok": ok, "docs": docs,
                "conflictos": conf, "pendientes": pend}
```

---

## `orchestrator/workflows/01_document_new.json`
```json
{
  "id": "ingesta_auditoria", "version": "2.0", "trigger": "document.new",
  "steps": [
    {"id": "ocr", "capability": "ocr", "on_error": "stop"},
    {"id": "skip_binario", "when": {"campo": "requiere_ocr", "truthy": true},
     "connector": "notify", "accion": "send",
     "params": {"text": "📄 Binario recibido: pendiente de OCR externo"},
     "on_error": "continue"},
    {"id": "persistir", "when": {"campo": "requiere_ocr", "truthy": false},
     "capability": "persistir", "on_error": "stop"},
    {"id": "auditar", "when": {"campo": "requiere_ocr", "truthy": false},
     "capability": "auditoria",
     "params": {"similitud_duplicado": 0.98, "similitud_version": 0.70}},
    {"id": "avisar_conflicto",
     "when": {"campo": "resultado_auditoria", "eq": "conflicto"},
     "connector": "notify", "accion": "send",
     "params": {"text": "⚠️ CONFLICTO detectado — usa /conflictos y /resolver"}},
    {"id": "tarjeta_conflicto",
     "when": {"campo": "resultado_auditoria", "eq": "conflicto"},
     "connector": "taskboard", "accion": "crear_tarea",
     "params": {"titulo": "CONFLICTO: revisar versiones",
                "descripcion": "Resolver con /resolver <id> A|B|FUSION"}}
  ]
}
```

## `orchestrator/workflows/02_document_audit.json`
```json
{"id": "re_auditoria", "version": "2.0", "trigger": "document.audit",
 "steps": [{"id": "auditar", "capability": "auditoria"}]}
```

## `orchestrator/workflows/03_document_tree.json`
```json
{
  "id": "arbol", "version": "2.0", "trigger": "document.tree",
  "steps": [
    {"id": "extraer", "capability": "arbol", "on_error": "stop"},
    {"id": "grafo", "connector": "graph", "accion": "bulk_edges",
     "params": {}}
  ]
}
```
Nota motor: el paso `grafo` recibe `edges` desde ctx (el motor copia el
resultado del paso previo al ctx; el conector lee `p["ctx_doc"]` + `edges`
inyectados — ver nota de integración en Parte C).

## `orchestrator/workflows/04_project_taskindex.json`
```json
{
  "id": "taskindex", "version": "2.0", "trigger": "project.taskindex",
  "steps": [
    {"id": "planificar", "capability": "planificar"},
    {"id": "documentar", "capability": "documentar"},
    {"id": "guardar_raiz", "connector": "vault", "accion": "save",
     "params": {}},
    {"id": "frontera", "capability": "frontera"},
    {"id": "handoff", "when": {"campo": "frontera_ok", "truthy": true},
     "connector": "handoff", "accion": "export", "params": {}},
    {"id": "avisar", "when": {"campo": "frontera_ok", "truthy": true},
     "connector": "notify", "accion": "send",
     "params": {"text": "✅ FASE 0 lista — contenedor exportado en handoff/"}}
  ]
}
```

---

## Agente interno `persistir` — `orchestrator/agents/persistir/`

manifest.json:
```json
{"type":"agent","name":"persistir","version":"2.0","iface":"agent.v1","capabilities":["persistir"],"priority":1,"status":"active"}
```
adapter.py:
```python
"""Hash + guardar íntegro en vault + registrar inventario (transacción)."""
import os
from ...base.contracts import AgentAdapter
from ...base.resilience import sha256_file, now
from ...store.db import DB
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class PersistirAgent(AgentAdapter):
    name = "persistir"
    def capabilities(self): return ["persistir"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        h = sha256_file(ctx["ruta"])
        if db.inv_get(h):
            return {"resultado_auditoria": "duplicado", "hash": h,
                    "ya_existia": True}
        root = os.path.join(BASE, "vault", ctx["proyecto"])
        os.makedirs(root, exist_ok=True)
        nombre = ctx["nombre"] + ".md"
        path = os.path.join(root, nombre)
        if os.path.exists(path):
            b, e = os.path.splitext(nombre)
            path = os.path.join(root, f"{b}_{h[:8]}{e}")
        cuerpo = (f"---\norigen: {ctx['origen']}\nhash: {h}\n"
                  f"fecha: {now()}\n---\n\n{ctx['texto']}")
        open(path, "w", encoding="utf-8").write(cuerpo)
        db.inv_add(h, ctx["proyecto"], ctx["nombre"], path)
        return {"hash": h, "vault": path}
```

**PLANTILLA.md estándar** (lo que tú subes; `arbolista` la parsea línea a línea):
```
proyecto: nombre_del_proyecto
objetivo: construir X
objetivo: lograr Y
decision: usar SQLite
tarea: definir esquema de datos
https://github.com/usuario/repo-relacionado
```
