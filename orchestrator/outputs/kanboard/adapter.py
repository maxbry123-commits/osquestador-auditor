import uuid
from ...base.contracts import OutputConnector
from ...base.resilience import CircuitBreaker, jlog
try:
    import requests
except ImportError:
    requests = None

class KanboardOut(OutputConnector):
    name = "kanboard"; capability = "taskboard"
    def __init__(self, config):
        super().__init__(config)
        k = config.get("kanboard", {})
        self.url, self.user = k.get("url", ""), k.get("user", "jsonrpc")
        self.token, self.pid = k.get("token", ""), k.get("project_id", 1)
        self.br = CircuitBreaker("kanboard")
    def _rpc(self, method, params):
        r = requests.post(self.url, auth=(self.user, self.token), timeout=15,
            json={"jsonrpc": "2.0", "method": method, "id": uuid.uuid4().hex, "params": params})
        r.raise_for_status(); return r.json().get("result")
    def call(self, accion, p):
        if accion == "crear_tarea":
            remoto = ""
            if self.url and requests and self.br.allow():
                try:
                    remoto = str(self._rpc("createTask", {"title": p["titulo"],
                        "project_id": self.pid, "description": p.get("descripcion", "")}))
                    self.br.ok()
                except Exception as e:
                    self.br.fail()
                    jlog(level="warn", ev="kanboard_local", err=str(e))
            return {"ok": True, "remoto_id": remoto}
        return {"ok": False, "error": f"accion {accion}"}
