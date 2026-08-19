# -*- coding: utf-8 -*-
"""Intérprete declarativo de workflows (YAML o JSON). Sin lógica de negocio."""
import os, json
from ..base.resilience import jlog
try:
    import yaml
except ImportError:
    yaml = None

def load_workflows(path):
    wfs = {}
    if not os.path.isdir(path): return wfs
    for fn in os.listdir(path):
        p = os.path.join(path, fn)
        try:
            if fn.endswith((".yaml", ".yml")) and yaml:
                w = yaml.safe_load(open(p, encoding="utf-8"))
            elif fn.endswith(".json"):
                w = json.load(open(p, encoding="utf-8"))
            else: continue
            wfs[w["trigger"]] = w
        except Exception as e:
            jlog(level="error", ev="wf_load", file=fn, err=str(e))
    return wfs

def _when(cond, ctx):
    if not cond: return True
    v = ctx.get(cond.get("campo"))
    if "in" in cond: return v in cond["in"]
    if "eq" in cond: return v == cond["eq"]
    if "truthy" in cond: return bool(v) == cond["truthy"]
    return True

def run(wf, ctx, agents, outputs, db):
    for step in wf["steps"]:
        if not _when(step.get("when"), ctx): continue
        sid = step["id"]
        try:
            if "capability" in step:
                r = agents.execute(step["capability"], step.get("params", {}), ctx)
            elif "connector" in step:
                # Pasar resultados previos relevantes
                extra = {k: ctx[k] for k in ("edges", "nombre", "contenido", "proyecto",
                       "hash", "titulo", "descripcion", "readme", "tareas_nuevas")
                       if k in ctx}
                r = outputs.call(step["connector"], step.get("accion", "call"),
                                 {**step.get("params", {}), **extra,
                                  "ctx_doc": {k: ctx.get(k) for k in
                                              ("hash","proyecto","nombre","texto")}})
            else:
                r = {"ok": True}
            ctx[f"step.{sid}"] = r
            db.j(wf.get("id","wf"), sid, {"ok": r.get("ok"), "agent": r.get("agent","")})
            if not r.get("ok") and step.get("on_error") == "stop":
                return ctx
            res = r.get("result")
            if isinstance(res, dict): ctx.update(res)
        except Exception as e:
            jlog(level="error", ev="step_fail", wf=wf.get("id"), step=sid, err=str(e))
            if step.get("on_error") == "stop": return ctx
    return ctx
