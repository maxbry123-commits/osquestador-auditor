import os
from ...base.contracts import AgentAdapter
from ...base.resilience import sha256_file, now
from ...store.db import DB
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class PersistirAgent(AgentAdapter):
    name = "persistir"
    def capabilities(self): return ["persistir"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        h = sha256_file(ctx["ruta"])
        if db.inv_get(h):
            return {"resultado_auditoria": "duplicado", "hash": h, "ya_existia": True}
        root = os.path.join(BASE, "vault", ctx["proyecto"])
        os.makedirs(root, exist_ok=True)
        nombre = ctx["nombre"] + ".md"
        path = os.path.join(root, nombre)
        if os.path.exists(path):
            b, e = os.path.splitext(nombre)
            path = os.path.join(root, f"{b}_{h[:8]}{e}")
        cuerpo = f"---\norigen: {ctx['origen']}\nhash: {h}\nfecha: {now()}\n---\n\n{ctx['texto']}"
        open(path, "w", encoding="utf-8").write(cuerpo)
        db.inv_add(h, ctx["proyecto"], ctx["nombre"], path)
        return {"hash": h, "vault": path}
