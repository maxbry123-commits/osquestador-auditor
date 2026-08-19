"""Auditoría de corpus: duplicado / versión(conflicto) / único + lineage."""
import os, difflib
from ...base.contracts import AgentAdapter
from ...store.db import DB
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class AuditorAgent(AgentAdapter):
    name = "auditor"
    def capabilities(self): return ["auditoria"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        h, proyecto = ctx["hash"], ctx["proyecto"]
        texto = ctx.get("texto", "")
        dup = float(p.get("similitud_duplicado", 0.98))
        ver = float(p.get("similitud_version", 0.70))
        for row in db.inv_por(proyecto):
            if row["hash"] == h or row["estado"] in ("archivado",): continue
            try: otro = open(row["vault"], encoding="utf-8", errors="replace").read()
            except Exception: continue
            sim = difflib.SequenceMatcher(None, texto[:20000], otro[:20000]).ratio()
            if sim >= dup:
                db.inv_estado(h, "duplicado", parents=row["hash"])
                return {"resultado_auditoria": "duplicado"}
            if sim >= ver:
                cid = db.conf_add(proyecto, h, row["hash"], round(sim, 2))
                db.inv_estado(h, "conflicto", parents=row["hash"])
                return {"resultado_auditoria": "conflicto", "conflicto_id": cid,
                        "sim": round(sim, 2), "contra": row["nombre"]}
        db.inv_estado(h, "auditado")
        return {"resultado_auditoria": "unico"}
