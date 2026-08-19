from ...base.contracts import OutputConnector
from ...base.resilience import CircuitBreaker
try:
    import requests
except ImportError:
    requests = None

class TgNotify(OutputConnector):
    name = "telegram_notify"; capability = "notify"
    def __init__(self, config):
        super().__init__(config)
        t = config.get("telegram", {})
        self.token, self.chat = t.get("token", ""), t.get("chat_id", "")
        self.br = CircuitBreaker("tg-out")
    def call(self, accion, p):
        if not (self.token and self.chat and requests and self.br.allow()):
            return {"ok": False, "error": "sin config"}
        try:
            requests.post(f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": self.chat, "text": p["text"][:4000]}, timeout=10)
            self.br.ok(); return {"ok": True}
        except Exception as e:
            self.br.fail(); return {"ok": False, "error": str(e)}
