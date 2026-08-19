"""Objetivos sin tarea → DEFINIR. Dedup real vía UNIQUE en SQLite."""
import os
from ...base.contracts import AgentAdapter
from ...store.db import DB
from ...base.resilience import read_json
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class PlandexAgent(AgentAdapter):
    name = "plandex"
    def capabilities(self): return ["planificar"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        proyecto = ctx["proyecto"]
        g = read_json(os.path.join(BASE, "state", "graph.json"), {"edges": []})
        objetivos = {e["a"] for e in g["edges"]
                     if e.get("proyecto") == proyecto and e.get("tipo") == "define_objetivo"}
        nuevas = []
        for o in objetivos:
            titulo = f"[{proyecto}] {o[:80]}"
            antes = len(db.tareas(proyecto))
            db.tarea_add(proyecto, titulo, "DEFINIR")
            if len(db.tareas(proyecto)) > antes:
                nuevas.append(titulo)
        return {"tareas_nuevas": nuevas}
