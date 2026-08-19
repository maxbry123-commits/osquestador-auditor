"""Consolida README_RAIZ: identidad del proyecto (docs + tabla tareas)."""
import os
from ...base.contracts import AgentAdapter
from ...base.resilience import now
from ...store.db import DB
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class HermesAgent(AgentAdapter):
    name = "hermes"
    def capabilities(self): return ["documentar"]
    def execute(self, cap, p, ctx):
        db = DB(os.path.join(BASE, "state", "state.db"))
        proyecto = ctx["proyecto"]
        docs = [d["nombre"] for d in db.inv_por(proyecto) if d["estado"] in ("auditado", "en_arbol")]
        tareas = db.tareas(proyecto)
        filas = "\n".join(f"| {t['titulo']} | {t['etiqueta']} | {t['estado']} |"
                          for t in tareas) or "| — | | |"
        listado = "\n".join(f"- {d}" for d in docs) or "- (vacío)"
        contenido = (f"# {proyecto} — RAÍZ DEL PROYECTO\n\n"
                     f"Actualizado: {now()}\n\n## Documentos\n{listado}\n\n"
                     f"## Tabla de tareas\n| Tarea | Etiqueta | Estado |\n|---|---|---|\n{filas}\n")
        return {"readme": contenido, "nombre": "README_RAIZ.md", "contenido": contenido}
