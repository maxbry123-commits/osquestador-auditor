# -*- coding: utf-8 -*-
"""MCP server: expone 4 tools por HTTP JSON-RPC."""
import json, threading, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_DB = None

TOOLS = {
  "search_project": {"desc": "Docs y estado de un proyecto", "params": ["proyecto"]},
  "get_doc":        {"desc": "Contenido íntegro por hash", "params": ["hash"]},
  "list_conflicts": {"desc": "Conflictos abiertos", "params": ["proyecto?"]},
  "queue_doc":      {"desc": "Encolar doc a inbox", "params": ["proyecto", "nombre", "contenido"]},
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
            return {"meta": row,
                    "contenido": open(row["vault"], encoding="utf-8", errors="replace").read()}
        if name == "list_conflicts":
            return {"conflictos": _DB.conf_abiertos(a.get("proyecto"))}
        if name == "queue_doc":
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            d = os.path.join(base, "inbox", a["proyecto"])
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, a["nombre"]), "w", encoding="utf-8").write(a["contenido"])
            return {"ok": True}
    return {"error": f"metodo {method}"}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(n))
            res = {"jsonrpc": "2.0", "id": req.get("id"),
                   "result": _dispatch(req.get("method"), req.get("params", {}))}
        except Exception as e:
            res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
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
