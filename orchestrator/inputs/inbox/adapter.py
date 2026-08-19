import os, shutil
from ...base.contracts import InputAdapter, Document
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class InboxInput(InputAdapter):
    name = "inbox"
    def discover(self):
        docs, root = [], os.path.join(BASE, "inbox")
        if not os.path.isdir(root): return []
        for proyecto in os.listdir(root):
            pd = os.path.join(root, proyecto)
            if not os.path.isdir(pd): continue
            for fn in os.listdir(pd):
                fp = os.path.join(pd, fn)
                if os.path.isfile(fp):
                    ext = os.path.splitext(fn)[1].lower().strip(".")
                    docs.append(Document(origen="inbox", proyecto=proyecto, nombre=fn, tipo=ext, ruta=fp))
        return docs
    def ack(self, doc):
        d = os.path.join(BASE, "archive", doc.proyecto)
        os.makedirs(d, exist_ok=True)
        dest = os.path.join(d, doc.nombre)
        if os.path.exists(dest):
            base, ext = os.path.splitext(doc.nombre)
            dest = os.path.join(d, f"{base}_{abs(hash(doc.ruta))%10**8}{ext}")
        shutil.move(doc.ruta, dest)
