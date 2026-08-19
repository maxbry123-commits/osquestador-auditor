import os, json, shutil
from ...base.contracts import OutputConnector
from ...base.resilience import atomic_write_json, now
from ...store.db import DB
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class HandoffOut(OutputConnector):
    name = "handoff"; capability = "handoff"
    def call(self, accion, p):
        if accion != "export": return {"ok": False}
        proyecto = p["proyecto"]
        db = DB(os.path.join(BASE, "state", "state.db"))
        d = os.path.join(BASE, "handoff", proyecto); os.makedirs(d, exist_ok=True)
        docs = db.inv_por(proyecto); conf = db.conf_abiertos(proyecto)
        pkg = {"proyecto": proyecto, "ts": now(),
               "frontera_ok": len(conf) == 0 and len(docs) > 0,
               "docs": docs, "tareas": db.tareas(proyecto),
               "conflictos_abiertos": conf}
        atomic_write_json(os.path.join(d, "handoff.json"), pkg)
        raiz = os.path.join(BASE, "vault", proyecto, "README_RAIZ.md")
        if os.path.exists(raiz):
            shutil.copy(raiz, os.path.join(d, "README_RAIZ.md"))
        return {"ok": True, "path": d, "frontera_ok": pkg["frontera_ok"]}
