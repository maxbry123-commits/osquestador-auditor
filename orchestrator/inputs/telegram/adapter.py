import os, time
from ...base.contracts import InputAdapter, Document
from ...base.resilience import CircuitBreaker
try:
    import requests
except ImportError:
    requests = None
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TelegramInput(InputAdapter):
    name = "telegram"
    def __init__(self, config, kv):
        super().__init__(config, kv)
        self.token = config.get("telegram", {}).get("token", "")
        self.br = CircuitBreaker("tg-in")
    def discover(self):
        if not (self.token and requests and self.br.allow()): return []
        off = int(self.kv.kv_get("tg_offset", "-1"))
        try:
            r = requests.get(f"https://api.telegram.org/bot{self.token}/getUpdates",
                params={"offset": off + 1 if off >= 0 else -1, "timeout": 0}, timeout=15).json()
            self.br.ok()
        except Exception:
            self.br.fail(); return []
        docs = []
        import re
        for u in r.get("result", []):
            off = max(off, u["update_id"])
            msg = u.get("message") or {}
            texto = msg.get("caption") or msg.get("text") or ""
            if texto.startswith("/"):
                docs.append(Document(origen="telegram", tipo="comando", texto=texto)); continue
            proyecto = "telegram_general"
            m = re.search(r"#(\w+)", texto)
            if m: proyecto = m.group(1)
            if "document" in msg:
                fid = msg["document"]["file_id"]; fname = msg["document"].get("file_name", fid)
                try:
                    fp = requests.get(f"https://api.telegram.org/bot{self.token}/getFile",
                        params={"file_id": fid}, timeout=15).json()["result"]["file_path"]
                    data = requests.get(f"https://api.telegram.org/file/bot{self.token}/{fp}", timeout=60).content
                    d = os.path.join(BASE, "inbox", proyecto); os.makedirs(d, exist_ok=True)
                    open(os.path.join(d, fname), "wb").write(data)
                except Exception: pass
            elif texto.strip():
                d = os.path.join(BASE, "inbox", proyecto); os.makedirs(d, exist_ok=True)
                open(os.path.join(d, f"nota_{int(time.time())}.md"), "w", encoding="utf-8").write(texto)
        self.kv.kv_set("tg_offset", off)
        return docs
