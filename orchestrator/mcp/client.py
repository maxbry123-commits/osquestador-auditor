# -*- coding: utf-8 -*-
"""MCP client: puente genérico stdio + HTTP."""
import json, subprocess, uuid
try:
    import requests
except ImportError:
    requests = None

class HTTPBridge:
    def __init__(self, url): self.url = url
    def call(self, method, params=None):
        r = requests.post(self.url, timeout=30, json={
            "jsonrpc": "2.0", "id": uuid.uuid4().hex,
            "method": method, "params": params or {}})
        r.raise_for_status(); return r.json().get("result")
    def tools(self): return self.call("tools/list")
    def tool(self, name, args):
        return self.call("tools/call", {"name": name, "arguments": args})

class StdioBridge:
    def __init__(self, cmd):
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True)
    def call(self, method, params=None):
        req = {"jsonrpc": "2.0", "id": uuid.uuid4().hex,
               "method": method, "params": params or {}}
        self.p.stdin.write(json.dumps(req) + "\n"); self.p.stdin.flush()
        return json.loads(self.p.stdout.readline()).get("result")
