# -*- coding: utf-8 -*-
"""Contratos universales. El kernel SOLO conoce estas interfaces."""
from dataclasses import dataclass, field

IFACE_INPUT = "input.v1"; IFACE_OUTPUT = "output.v1"; IFACE_AGENT = "agent.v1"

@dataclass
class Document:
    doc_id: str = ""
    origen: str = ""
    proyecto: str = "general"
    nombre: str = ""
    tipo: str = ""
    ruta: str = ""
    texto: str = ""
    meta: dict = field(default_factory=dict)

@dataclass
class Health:
    status: str = "ok"
    latency_ms: int = 0
    detail: str = ""

class InputAdapter:
    name = "base"; iface = IFACE_INPUT
    def __init__(self, config, kv): self.config, self.kv = config, kv
    def discover(self) -> list: raise NotImplementedError
    def ack(self, doc: Document): pass
    def health(self) -> Health: return Health()

class OutputConnector:
    name = "base"; iface = IFACE_OUTPUT; capability = ""
    def __init__(self, config): self.config = config
    def call(self, accion: str, payload: dict) -> dict: raise NotImplementedError
    def health(self) -> Health: return Health()

class AgentAdapter:
    name = "base"; iface = IFACE_AGENT
    def __init__(self, config): self.config = config
    def capabilities(self) -> list: return []
    def execute(self, capability: str, payload: dict, ctx: dict) -> dict:
        raise NotImplementedError
    def health(self) -> Health: return Health()
