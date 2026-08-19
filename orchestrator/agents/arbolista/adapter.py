"""Extrae piezas del doc: objetivos, decisiones, repos, urls, archivos código."""
import re
from ...base.contracts import AgentAdapter

PAT = [("objetivo", r"^(objetivo|meta|goal)\b[:\-]"),
       ("decision", r"^(decisi[oó]n|decision)\b[:\-]"),
       ("tarea", r"^(tarea|task)\b[:\-]")]

class ArbolistaAgent(AgentAdapter):
    name = "arbolista"
    def capabilities(self): return ["arbol"]
    def execute(self, cap, p, ctx):
        texto, nombre = ctx.get("texto", ""), ctx["nombre"]
        edges, piezas = [], []
        proyecto = ctx["proyecto"]
        edges.append({"proyecto": proyecto, "de": nombre, "a": "RAIZ", "tipo": "pertenece_a"})
        for linea in texto.splitlines():
            l = linea.strip()
            for tipo, pat in PAT:
                if re.match(pat, l, re.I):
                    piezas.append({"tipo": tipo, "texto": l})
                    edges.append({"proyecto": proyecto, "de": nombre,
                                  "a": l[:60], "tipo": f"define_{tipo}"})
        for url in re.findall(r"https?://\S+", texto)[:50]:
            t = "repo" if "github.com" in url else "url"
            edges.append({"proyecto": proyecto, "de": nombre, "a": url[:120], "tipo": t})
        for f in re.findall(r"\b[\w\-/]+\.(?:py|md|json|yaml|js|html)\b", texto)[:50]:
            edges.append({"proyecto": proyecto, "de": nombre, "a": f, "tipo": "menciona_archivo"})
        return {"edges": edges, "piezas": piezas}
