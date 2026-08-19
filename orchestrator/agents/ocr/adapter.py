import os
from ...base.contracts import AgentAdapter
TEXT_EXT = {"md","txt","py","json","html","csv","yaml","yml"}

class OCRAgent(AgentAdapter):
    name = "ocr"
    def capabilities(self): return ["ocr"]
    def execute(self, cap, p, ctx):
        ruta, tipo = ctx.get("ruta", ""), ctx.get("tipo", "")
        if tipo in TEXT_EXT and os.path.exists(ruta):
            return {"texto": open(ruta, encoding="utf-8", errors="replace").read(), "requiere_ocr": False}
        return {"texto": "", "requiere_ocr": True}
