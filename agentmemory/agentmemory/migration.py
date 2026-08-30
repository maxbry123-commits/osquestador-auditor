"""
agentmemory V3 — Migration and import tools.

Import from Mem0, Zep, LangMem, and generic JSON formats.
Export in portable format.
"""

from __future__ import annotations

import json
import time
from typing import Any, Optional

from .models import MemoryKind, MemoryNode, Namespace, Provenance


class MigrationImporter:
    """Import memory stores from competing formats."""

    def __init__(self, store):
        self._store = store

    async def from_mem0(self, data: list[dict]) -> int:
        """
        Import from Mem0 export format.
        Mem0 memories: [{"id": ..., "memory": ..., "metadata": {...}, "created_at": ...}]
        """
        count = 0
        for item in data:
            content = item.get("memory", item.get("text", ""))
            if not content:
                continue
            meta = item.get("metadata", {})
            kind = self._infer_kind_from_meta(meta)
            await self._store.async_add(
                content=content,
                kind=kind,
                metadata=meta,
                source="mem0_import",
                tags=set(meta.get("tags", [])),
                event_time=item.get("created_at"),
            )
            count += 1
        return count

    async def from_zep(self, data: dict) -> int:
        """
        Import from Zep export format.
        Zep: {"facts": [...], "episodes": [...], "entities": [...]}
        """
        count = 0
        for fact in data.get("facts", []):
            content = fact.get("fact", fact.get("content", ""))
            if not content:
                continue
            await self._store.async_add(
                content=content,
                kind="fact",
                confidence=fact.get("confidence", 0.8),
                source="zep_import",
                event_time=fact.get("valid_at"),
                metadata={"zep_id": fact.get("uuid", ""),
                          "expired_at": fact.get("expired_at")},
            )
            count += 1

        for ep in data.get("episodes", []):
            content = ep.get("content", ep.get("body", ""))
            if not content:
                continue
            await self._store.async_add(
                content=content,
                kind="event",
                source="zep_import",
                event_time=ep.get("created_at"),
            )
            count += 1

        for ent in data.get("entities", []):
            name = ent.get("name", "")
            desc = ent.get("description", ent.get("summary", ""))
            if name:
                content = f"{name}: {desc}" if desc else name
                await self._store.async_add(
                    content=content,
                    kind="entity",
                    source="zep_import",
                    metadata={"entity_type": ent.get("type", "")},
                )
                count += 1
        return count

    async def from_langmem(self, data: list[dict]) -> int:
        """Import from LangMem/LangGraph memory format."""
        count = 0
        for item in data:
            content = item.get("content", item.get("value", ""))
            if not content:
                continue
            kind = item.get("type", "fact")
            if kind not in [k.value for k in MemoryKind]:
                kind = "fact"
            await self._store.async_add(
                content=content,
                kind=kind,
                source="langmem_import",
                metadata=item.get("metadata", {}),
            )
            count += 1
        return count

    async def from_json(self, data: dict) -> int:
        """
        Import from agentmemory export format (any version).
        """
        nodes = data.get("nodes", [])
        count = 0
        for nd in nodes:
            kind = nd.get("kind", "fact")
            if kind not in [k.value for k in MemoryKind]:
                kind = "observation"
            prov = Provenance.from_dict(nd.get("provenance", {}))
            if not prov.source and "source" in nd:
                prov.source = nd["source"]
            await self._store.async_add(
                content=nd["content"],
                kind=kind,
                importance=nd.get("importance", 0.5),
                confidence=nd.get("confidence", 1.0),
                tags=set(nd.get("tags", [])),
                metadata=nd.get("metadata", {}),
                provenance=prov,
                event_time=nd.get("event_time"),
            )
            count += 1
        return count

    async def from_file(self, path: str, format: str = "auto") -> int:
        """Import from a file. Auto-detects format."""
        with open(path, "r") as f:
            data = json.load(f)

        if format == "auto":
            format = self._detect_format(data)

        if format == "mem0":
            return await self.from_mem0(data if isinstance(data, list) else data.get("memories", []))
        elif format == "zep":
            return await self.from_zep(data)
        elif format == "langmem":
            return await self.from_langmem(data if isinstance(data, list) else data.get("memories", []))
        elif format == "agentmemory":
            return await self.from_json(data)
        else:
            raise ValueError(f"Unknown format: {format}")

    @staticmethod
    def _detect_format(data: Any) -> str:
        if isinstance(data, list):
            if data and "memory" in data[0]:
                return "mem0"
            return "langmem"
        if isinstance(data, dict):
            if "version" in data and "nodes" in data:
                return "agentmemory"
            if "facts" in data or "episodes" in data:
                return "zep"
            if "memories" in data:
                sample = data["memories"]
                if sample and "memory" in sample[0]:
                    return "mem0"
                return "langmem"
        return "agentmemory"

    @staticmethod
    def _infer_kind_from_meta(meta: dict) -> str:
        category = meta.get("category", "").lower()
        if category in ("entity", "person", "organization"):
            return "entity"
        if category in ("preference", "like", "dislike"):
            return "preference"
        if category in ("fact", "knowledge"):
            return "fact"
        if category in ("event", "action"):
            return "event"
        return "fact"


class MigrationExporter:
    """Export to portable formats."""

    def __init__(self, store):
        self._store = store

    async def to_mem0_format(self) -> list[dict]:
        """Export in Mem0-compatible format."""
        data = await self._store.async_export()
        return [
            {
                "id": n["id"],
                "memory": n["content"],
                "metadata": {
                    "kind": n["kind"],
                    "importance": n.get("importance", 0.5),
                    "tags": n.get("tags", []),
                    **n.get("metadata", {}),
                },
                "created_at": n.get("created_at"),
            }
            for n in data.get("nodes", [])
        ]

    async def to_file(self, path: str, format: str = "agentmemory"):
        """Export to file."""
        if format == "agentmemory":
            data = await self._store.async_export()
        elif format == "mem0":
            data = await self.to_mem0_format()
        else:
            data = await self._store.async_export()
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
