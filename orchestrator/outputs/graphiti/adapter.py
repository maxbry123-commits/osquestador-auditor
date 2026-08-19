import os
from ...base.contracts import OutputConnector
from ...base.resilience import read_json, atomic_write_json, now, CircuitBreaker
try:
    import requests
except ImportError:
    requests = None
BASE = os.environ.get("NCT_BASE", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class GraphitiOut(OutputConnector):
    name = "graphiti"; capability = "graph"
    def __init__(self, config):
        super().__init__(config)
        self.url = config.get("graphiti", {}).get("mcp_url", "")
        self.local = os.path.join(BASE, "state", "graph.json")
        self.br = CircuitBreaker("graphiti")
    def call(self, accion, p):
        if accion == "bulk_edges":
            edges = p["edges"]
            for e in edges: e["ts"] = now()
            if self.url and requests and self.br.allow():
                try:
                    requests.post(self.url.rstrip("/") + "/edges/bulk", json={"edges": edges}, timeout=20)
                    self.br.ok(); return {"ok": True, "remote": True}
                except Exception: self.br.fail()
            g = read_json(self.local, {"edges": []})
            g["edges"].extend(edges); atomic_write_json(self.local, g)
            return {"ok": True, "remote": False}
        if accion == "edges":
            g = read_json(self.local, {"edges": []})
            return {"ok": True, "edges": [e for e in g["edges"] if e.get("proyecto") == p.get("proyecto")]}
        return {"ok": False, "error": f"accion {accion}"}
