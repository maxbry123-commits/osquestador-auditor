# -*- coding: utf-8 -*-
"""Kernel. boot→pump→shutdown. Agnóstico: cero nombres de plugins."""
import os
from ..base import contracts as ct
from ..base.resilience import (atomic_write_json, read_json, init_log, jlog,
                               install_signals, shutting_down, wait, now)
from ..store.db import DB
from . import motor, commands
from .managers import Registry, AgentManager, OutputManager

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(BASE, *a)

DEFAULT_CONFIG = {
    "mode": "prod",
    "poll_seconds": 10,
    "mcp_server": {"enabled": True, "port": 8765},
    "similitud_duplicado": 0.98,
    "similitud_version": 0.70,
    "inputs": {},
    "outputs": {},
    "agents": {},
}
DIRS = ["inputs", "outputs", "agents", "workflows",
        "inbox", "archive", "vault", "handoff", "state"]

def boot():
    for d in DIRS: os.makedirs(P(d), exist_ok=True)
    if not os.path.exists(P("config.json")):
        atomic_write_json(P("config.json"), DEFAULT_CONFIG)
    init_log(P("state", "log.jsonl"))
    cfg = read_json(P("config.json"), DEFAULT_CONFIG)
    db = DB(P("state", "state.db"))
    reg = Registry(BASE, ct, cfg, db)
    reg.scan(force=True)
    agents = AgentManager(reg, cfg.get("mode", "prod"))
    outputs = OutputManager(reg)
    wfs = motor.load_workflows(P("workflows"))
    return cfg, db, reg, agents, outputs, wfs

def _health(db, status, step=""):
    atomic_write_json(P("state", "health.json"), {"ts": now(), "status": status, "step": step})

def _recover(db, wfs, agents, outputs):
    for row in db.inv_por(estado="ingresado"):
        try:
            ctx = {"hash": row["hash"], "proyecto": row["proyecto"],
                   "nombre": row["nombre"], "vault": row["vault"],
                   "texto": open(row["vault"], encoding="utf-8", errors="replace").read(),
                   "tipo": "recuperado"}
            wf = wfs.get("document.audit")
            if wf: motor.run(wf, ctx, agents, outputs, db)
        except Exception as e:
            jlog(level="warn", ev="recover_fail", err=str(e))

def pump():
    install_signals()
    cfg, db, reg, agents, outputs, wfs = boot()
    if cfg.get("mcp_server", {}).get("enabled"):
        try:
            from ..mcp.server import start_bg
            start_bg(db, cfg["mcp_server"].get("port", 8765))
        except Exception as e:
            jlog(level="warn", ev="mcp_off", err=str(e))
    jlog(level="info", ev="boot", mode=cfg.get("mode"))
    _recover(db, wfs, agents, outputs)
    while not shutting_down():
        reg.scan()
        tocados = set()
        for e in list(reg.inputs.values()):
            try: docs = e["obj"].discover()
            except Exception as ex:
                jlog(level="warn", ev="input_fail", name=e["manifest"]["name"], err=str(ex)); continue
            for doc in docs:
                if shutting_down(): break
                _health(db, "alive", doc.nombre)
                if doc.tipo == "comando":
                    resp = commands.handle(doc.texto, db, outputs)
                    outputs.call("notify", "send", {"text": resp}); continue
                ctx = {"proyecto": doc.proyecto, "nombre": doc.nombre,
                       "ruta": doc.ruta, "tipo": doc.tipo,
                       "origen": doc.origen, "texto": doc.texto}
                wf = wfs.get("document.new")
                if wf:
                    ctx = motor.run(wf, ctx, agents, outputs, db)
                    if ctx.get("resultado_auditoria") == "unico":
                        tocados.add(ctx["proyecto"])
                try: e["obj"].ack(doc)
                except Exception: pass
        for row in db.inv_por(estado="auditado"):
            try:
                ctx = {"hash": row["hash"], "proyecto": row["proyecto"],
                       "nombre": row["nombre"], "vault": row["vault"],
                       "texto": open(row["vault"], encoding="utf-8", errors="replace").read()}
                wf = wfs.get("document.tree")
                if wf:
                    motor.run(wf, ctx, agents, outputs, db)
                    db.inv_estado(row["hash"], "en_arbol")
                    tocados.add(row["proyecto"])
            except Exception as e:
                jlog(level="warn", ev="tree_fail", err=str(e))
        for proyecto in tocados:
            wf = wfs.get("project.taskindex")
            if wf: motor.run(wf, {"proyecto": proyecto}, agents, outputs, db)
        _health(db, "alive", "idle")
        wait(cfg.get("poll_seconds", 10))
    _health(db, "shutdown"); jlog(level="info", ev="shutdown")
