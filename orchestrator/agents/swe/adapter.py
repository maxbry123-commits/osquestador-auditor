"""Audita frontera Fase 0."""
import os
from ...base.contracts import AgentAdapter
from ...store.db import DB
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class SWEAgent(AgentAdapter):
    name = "swe"
    def capabilities(self): return ["frontera"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        proyecto = ctx["proyecto"]
        conf = len(db.conf_abiertos(proyecto))
        pend = len(db.inv_por(proyecto, "ingresado")) + len(db.inv_por(proyecto, "conflicto"))
        docs = len(db.inv_por(proyecto))
        ok = conf == 0 and pend == 0 and docs > 0
        return {"frontera_ok": ok, "docs": docs, "conflictos": conf, "pendientes": pend}
