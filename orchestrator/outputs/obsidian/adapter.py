import os
from ...base.contracts import OutputConnector
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class ObsidianOut(OutputConnector):
    name = "obsidian"; capability = "vault"
    def call(self, accion, p):
        root = self.config.get("obsidian", {}).get("vault_path") or os.path.join(BASE, "vault")
        if accion == "save":
            d = os.path.join(root, p["proyecto"]); os.makedirs(d, exist_ok=True)
            nombre = p["nombre"]
            path = os.path.join(d, nombre)
            if os.path.exists(path) and p.get("hash"):
                b, e = os.path.splitext(nombre)
                path = os.path.join(d, f"{b}_{p['hash'][:8]}{e}")
            open(path, "w", encoding="utf-8").write(p["contenido"])
            return {"ok": True, "path": path}
        return {"ok": False, "error": f"accion {accion}"}
