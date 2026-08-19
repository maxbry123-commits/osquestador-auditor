# SALIDA 2 v2.0 — PARTE C: MCP + TOOLS + DESPLIEGUE

---

## `orchestrator/mcp/server.py` — el orquestador COMO servidor MCP
Expone 4 tools por HTTP JSON-RPC. Tu futura interface (o Claude/Cursor) consume esto directo: control del sistema sin abrir Kanboard/Obsidian.

```python
# -*- coding: utf-8 -*-
import json, threading, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_DB = None

TOOLS = {
  "search_project": {"desc": "Docs y estado de un proyecto",
                     "params": ["proyecto"]},
  "get_doc":        {"desc": "Contenido íntegro por hash",
                     "params": ["hash"]},
  "list_conflicts": {"desc": "Conflictos abiertos",
                     "params": ["proyecto?"]},
  "queue_doc":      {"desc": "Encolar doc a inbox",
                     "params": ["proyecto", "nombre", "contenido"]},
}

def _dispatch(method, params):
    if method == "tools/list":
        return {"tools": [{"name": k, **v} for k, v in TOOLS.items()]}
    if method == "tools/call":
        name, a = params.get("name"), params.get("arguments", {})
        if name == "search_project":
            return {"docs": _DB.inv_por(a["proyecto"]),
                    "tareas": _DB.tareas(a["proyecto"]),
                    "conflictos": _DB.conf_abiertos(a["proyecto"])}
        if name == "get_doc":
            row = _DB.inv_get(a["hash"])
            if not row: return {"error": "no existe"}
            return {"meta": row, "contenido":
                    open(row["vault"], encoding="utf-8",
                         errors="replace").read()}
        if name == "list_conflicts":
            return {"conflictos": _DB.conf_abiertos(a.get("proyecto"))}
        if name == "queue_doc":
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            d = os.path.join(base, "inbox", a["proyecto"])
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, a["nombre"]), "w",
                 encoding="utf-8").write(a["contenido"])
            return {"ok": True}
    return {"error": f"metodo {method}"}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(n))
            res = {"jsonrpc": "2.0", "id": req.get("id"),
                   "result": _dispatch(req.get("method"),
                                       req.get("params", {}))}
        except Exception as e:
            res = {"jsonrpc": "2.0", "id": None,
                   "error": {"code": -32000, "message": str(e)}}
        body = json.dumps(res, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)

def start_bg(db, port=8765):
    global _DB; _DB = db
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv
```

## `orchestrator/mcp/client.py` — el orquestador COMO cliente MCP
Puente genérico stdio + HTTP: conecta a CUALQUIER servidor MCP (Notion, Slack, GitHub…) sin conocer al proveedor.

```python
# -*- coding: utf-8 -*-
import json, subprocess, uuid
try:
    import requests
except ImportError:
    requests = None

class HTTPBridge:
    def __init__(self, url): self.url = url
    def call(self, method, params=None):
        r = requests.post(self.url, timeout=30, json={
            "jsonrpc": "2.0", "id": uuid.uuid4().hex,
            "method": method, "params": params or {}})
        r.raise_for_status(); return r.json().get("result")
    def tools(self): return self.call("tools/list")
    def tool(self, name, args):
        return self.call("tools/call", {"name": name, "arguments": args})

class StdioBridge:
    def __init__(self, cmd):
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True)
    def call(self, method, params=None):
        req = {"jsonrpc": "2.0", "id": uuid.uuid4().hex,
               "method": method, "params": params or {}}
        self.p.stdin.write(json.dumps(req) + "\n"); self.p.stdin.flush()
        return json.loads(self.p.stdout.readline()).get("result")
```

---

## `orchestrator/tools/check_kernel_isolation.py` — linter del kernel
```python
#!/usr/bin/env python3
"""Falla si kernel/ conoce nombres de plugins o proveedores."""
import os, re, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROHIBIDO = re.compile(
    r"(telegram|kanboard|obsidian|graphiti|haystack|plandex|hermes|notion|"
    r"slack|cerebras|groq|swe\b|repomix)", re.I)
errores = []
for fn in os.listdir(os.path.join(BASE, "kernel")):
    if not fn.endswith(".py"): continue
    for i, linea in enumerate(open(os.path.join(BASE, "kernel", fn),
                                   encoding="utf-8"), 1):
        if PROHIBIDO.search(linea):
            errores.append(f"kernel/{fn}:{i}: {linea.strip()}")
if errores:
    print("VIOLACIONES DE AISLAMIENTO:"); print("\n".join(errores))
    sys.exit(1)
print("kernel limpio ✓")
```

## `orchestrator/tools/scaffold.py` — generador de plugins en 5 minutos
```python
#!/usr/bin/env python3
"""python3 tools/scaffold.py input notion → inputs/notion/ listo."""
import os, sys, json
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIPOS = {"input": ("inputs", "InputAdapter", "input.v1"),
         "output": ("outputs", "OutputConnector", "output.v1"),
         "agent": ("agents", "AgentAdapter", "agent.v1")}

def main():
    tipo, nombre = sys.argv[1], sys.argv[2]
    carpeta, clase, iface = TIPOS[tipo]
    d = os.path.join(BASE, carpeta, nombre); os.makedirs(d, exist_ok=True)
    m = {"type": tipo, "name": nombre, "version": "0.1",
         "iface": iface, "status": "active"}
    if tipo == "agent": m["capabilities"] = ["TODO"]
    if tipo == "output": m["capability"] = "TODO"
    json.dump(m, open(os.path.join(d, "manifest.json"), "w"), indent=2)
    open(os.path.join(d, "adapter.py"), "w").write(
f'''from ...base.contracts import {clase}

class {nombre.capitalize()}Plugin({clase}):
    name = "{nombre}"
    # TODO: implementar contrato {iface}
''')
    open(os.path.join(d, "README.md"), "w").write(
        f"# {nombre}\n\nTODO: propósito, config, ejemplos.\n")
    print(f"{carpeta}/{nombre}/ creado — implementa adapter.py, "
          f"secrets a config.json; hot-reload lo detecta solo.")

if __name__ == "__main__": main()
```

---

## NOTA DE INTEGRACIÓN (motor ↔ conectores)
El motor copia el `result` de cada paso al `ctx`. Para que los conectores
reciban resultados previos (ej. `grafo` necesita `edges` de `extraer`;
`guardar_raiz` necesita `nombre`/`contenido` de `documentar`), en
`kernel/motor.py` la llamada a conectores debe enviar:
`{**step.get("params", {}), **{k: ctx[k] for k in ("edges", "nombre",
"contenido", "proyecto", "hash", "titulo", "descripcion") if k in ctx}}`
— reemplaza la línea de `ctx_doc`. Un solo cambio, declarado aquí para
que Claude Code lo aplique al ensamblar el paquete.

## MODOS (config "mode")
- `dev`: breakers desactivados, fallos ruidosos.
- `staging`: todo activo, notificaciones digest.
- `prod`: breakers agresivos, reintentos completos.

## ÁRBOL FINAL DEL PAQUETE
```
orchestrator/
├── __main__.py
├── config.json                (autogenerado al primer arranque)
├── base/      contracts.py resilience.py
├── store/     db.py           (SQLite WAL + journal replay)
├── kernel/    core.py motor.py managers.py commands.py
├── inputs/    inbox/ telegram/ _template/
├── outputs/   obsidian/ kanboard/ graphiti/ telegram_notify/ handoff/ _template/
├── agents/    ocr/ persistir/ auditor/ arbolista/ plandex/ hermes/ swe/ _template/
├── workflows/ 01..04 .json    (declarativos, editables sin Python)
├── mcp/       server.py client.py
├── tools/     scaffold.py check_kernel_isolation.py
└── inbox/ vault/ handoff/ archive/ state/
```

## DESPLIEGUE (3 comandos)
```bash
pip install requests pyyaml
python3 orchestrator/tools/check_kernel_isolation.py   # linter
python3 -m orchestrator                                 # auto-run
```
Sin credenciales: modo local completo (inbox + vault + grafo/kanban locales).
Con config.json lleno (Salida 3): Telegram + Kanboard + Graphiti reales se
activan solos, sin tocar código.

## VERIFICACIÓN DE TU REQUISITO CLAVE
- Tu interface propia → habla con `mcp/server.py` (4 tools) y controla todo.
- Interfaces de otros sistemas → siguen usables (Kanboard UI, Obsidian app).
- Control remoto sin abrir sus UIs → conectores `outputs/` vía API.
- Fuente/salida nueva mañana → `scaffold` + carpeta + manifest. Kernel intacto.

## FIXES APLICADOS EN v2.0 (trazabilidad)
1-13 de tu lista: AgentManager+fallback (managers.py), OCR devuelve
`requiere_ocr` sin placeholder, dedup DEFINIR por UNIQUE en SQLite,
tg_offset=-1 descarta backlog, estados transaccionales en inventory
(recover al arrancar), Kanboard remoto_id solo si éxito (SQLite única
verdad), colisión vault con sufijo hash, fallback_chain, handoff/,
detectores ampliados (urls/repos/archivos), offset persistente en DB,
uuid en RPC, poll configurable. 14-19 míos: /resolver reencola al árbol,
comandos Telegram completos, PLANTILLA.md, re-proceso post-conflicto,
export handoff, lineage parents en inventory+grafo.
