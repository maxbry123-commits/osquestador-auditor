# -*- coding: utf-8 -*-
"""Descubrimiento de plugins + AgentManager con fallback_chain.
El kernel NUNCA importa plugins por nombre: importlib sobre carpetas."""
import os, importlib.util
from ..base.resilience import read_json, jlog, CircuitBreaker

def _load(dirpath, clsbase, pkg_base):
    m = read_json(os.path.join(dirpath, "manifest.json"), None)
    if not m or m.get("status", "active") != "active": return None, None
    ap = os.path.join(dirpath, "adapter.py")
    if not os.path.exists(ap): return m, None
    import sys
    parent = os.path.dirname(pkg_base)
    if parent not in sys.path: sys.path.insert(0, parent)
    rel = os.path.relpath(ap, parent).replace(os.sep, ".")[:-3]
    spec = importlib.util.spec_from_file_location(rel, ap)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[rel] = mod
    spec.loader.exec_module(mod)
    for v in vars(mod).values():
        if isinstance(v, type) and issubclass(v, clsbase) and v is not clsbase:
            return m, v
    return m, None

class Registry:
    """Escanea inputs/ outputs/ agents/. Hot-reload por mtime."""
    def __init__(self, base, contracts, config, kv):
        self.base, self.ct, self.config, self.kv = base, contracts, config, kv
        self.inputs, self.outputs, self.agents = {}, {}, {}
        self._mtimes = {}
    def _dirty(self, root):
        t = 0
        if not os.path.isdir(root): return False
        for d in os.listdir(root):
            p = os.path.join(root, d, "manifest.json")
            if os.path.exists(p): t = max(t, os.path.getmtime(p))
        if self._mtimes.get(root) != t:
            self._mtimes[root] = t; return True
        return False
    def scan(self, force=False):
        for root, store, base_cls, mk in [
            (os.path.join(self.base, "inputs"), self.inputs, self.ct.InputAdapter, lambda c: c(self.config, self.kv)),
            (os.path.join(self.base, "outputs"), self.outputs, self.ct.OutputConnector, lambda c: c(self.config)),
            (os.path.join(self.base, "agents"), self.agents, self.ct.AgentAdapter, lambda c: c(self.config))]:
            if not (force or self._dirty(root)): continue
            store.clear()
            for d in sorted(os.listdir(root)):
                if d.startswith("_") or not os.path.isdir(os.path.join(root, d)): continue
                m, cls = _load(os.path.join(root, d), base_cls, self.base)
                if m and cls:
                    try:
                        store[m["name"]] = {"manifest": m, "obj": mk(cls)}
                        jlog(level="info", ev="plugin_load", name=m["name"])
                    except Exception as e:
                        jlog(level="error", ev="plugin_fail", name=m.get("name"), err=str(e))

class AgentManager:
    def __init__(self, registry, mode="prod"):
        self.r = registry
        self.breakers = {}
        self.enabled = mode != "dev"
    def _chain(self, cap):
        c = []
        for name, e in self.r.agents.items():
            caps = e["manifest"].get("capabilities", [])
            if cap in caps:
                c.append((e["manifest"].get("priority", 9), name, e["obj"]))
        return [x[1:] for x in sorted(c)]
    def execute(self, cap, payload, ctx):
        br = self.breakers.setdefault(cap, CircuitBreaker(cap, 5, 300, self.enabled))
        last = None
        for name, obj in self._chain(cap):
            if not br.allow(): break
            try:
                r = obj.execute(cap, payload, ctx); br.ok()
                return {"ok": True, "agent": name, "result": r}
            except Exception as e:
                last = e; br.fail()
                jlog(level="warn", ev="agent_fail", agent=name, cap=cap, err=str(e))
        return {"ok": False, "error": str(last) if last else f"sin agente para {cap}"}

class OutputManager:
    def __init__(self, registry): self.r = registry
    def call(self, capability, accion, payload):
        for e in self.r.outputs.values():
            if e["manifest"].get("capability") == capability:
                return e["obj"].call(accion, payload)
        return {"ok": False, "error": f"sin conector {capability}"}
