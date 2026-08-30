"""
agentmemory V3 — Cross-store federation.
"""

from __future__ import annotations

from typing import Optional

from .models import Namespace, RetrievalResult


class FederatedStore:
    """Query across multiple MemoryStore instances, merge results."""

    def __init__(self, stores: list):
        self._stores = stores

    async def async_recall(self, query: str, limit: int = 10, **kwargs
                           ) -> list[RetrievalResult]:
        all_results: list[RetrievalResult] = []
        seen: set[str] = set()
        for store in self._stores:
            try:
                results = await store.async_recall(
                    query=query, limit=limit * 2, **kwargs)
                for r in results:
                    h = r.node.content_hash()
                    if h not in seen:
                        seen.add(h)
                        all_results.append(r)
            except Exception:
                continue
        all_results.sort(key=lambda r: r.score, reverse=True)
        return all_results[:limit]

    def recall(self, query: str, limit: int = 10, **kwargs
               ) -> list[RetrievalResult]:
        import asyncio
        return asyncio.run(self.async_recall(query, limit, **kwargs))

    async def async_stats(self) -> dict:
        t = {"stores": len(self._stores),
             "total_memories": 0, "active_memories": 0, "edges": 0}
        for s in self._stores:
            try:
                st = await s.async_stats()
                t["total_memories"] += st.get("total_memories", 0)
                t["active_memories"] += st.get("active_memories", 0)
                t["edges"] += st.get("edges", 0)
            except Exception:
                pass
        return t

    @property
    def stores(self) -> list:
        return self._stores
