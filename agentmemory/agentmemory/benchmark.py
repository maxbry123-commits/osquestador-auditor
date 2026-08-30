"""
agentmemory V3 — Benchmark harness.

Standardized workloads covering all V3 features:
scale_write, scale_recall, retrieval_fidelity,
consolidation_efficiency, temporal_retrieval,
conversation_ingestion, health_check_perf.
"""

from __future__ import annotations

import asyncio
import random
import statistics
import time
from dataclasses import dataclass, field


@dataclass
class BenchmarkResult:
    name: str
    metrics: dict[str, float]
    params: dict = field(default_factory=dict)
    duration_seconds: float = 0.0

    def summary(self) -> str:
        lines = [f"Benchmark: {self.name}",
                 f"Duration: {self.duration_seconds:.2f}s"]
        if self.params:
            lines.append(f"Params: {self.params}")
        for k, v in self.metrics.items():
            lines.append(f"  {k}: {v:.4f}" if isinstance(v, float)
                         else f"  {k}: {v}")
        return "\n".join(lines)


_TOPICS = [
    "deployment", "customer", "pricing", "bug", "feature request",
    "API", "database", "authentication", "performance", "security",
    "infrastructure", "monitoring", "testing", "release", "rollback",
    "user feedback", "support ticket", "integration", "migration",
    "documentation", "onboarding", "billing", "compliance", "analytics"]

_TEMPLATES = {
    "fact": ["The {t} system uses {d} for {p}",
             "{e} is responsible for the {t} component",
             "Current {t} metrics show {v}% {dir}"],
    "event": ["Observed {sev} {t} issue at {time}",
              "Completed {t} {act} successfully"],
    "preference": ["User prefers {app} for {t} workflows",
                   "Avoid {anti} in {t} implementations"],
    "entity": ["{e} is the {role} for the {t} team",
               "The {t} service runs on {infra}"]}
_DETAILS = ["microservices", "REST API", "GraphQL", "Redis", "PostgreSQL"]
_ENTITIES = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank"]
_SEV = ["critical", "major", "minor", "low"]


def generate_workload(n: int, seed: int = 42) -> list[tuple[str, str]]:
    rng = random.Random(seed)
    kinds = list(_TEMPLATES.keys())
    out = []
    for _ in range(n):
        k = rng.choice(kinds)
        tmpl = rng.choice(_TEMPLATES[k])
        c = tmpl.format(
            t=rng.choice(_TOPICS), d=rng.choice(_DETAILS),
            p=rng.choice(["prod", "staging", "dev", "test"]),
            e=rng.choice(_ENTITIES), v=rng.randint(5, 95),
            dir=rng.choice(["up", "down", "stable"]),
            sev=rng.choice(_SEV),
            time=rng.choice(["today", "yesterday", "last week"]),
            act=rng.choice(["deploy", "migrate", "update"]),
            app=rng.choice(["automated", "manual", "hybrid"]),
            anti=rng.choice(["direct DB access", "hardcoded values"]),
            role=rng.choice(["lead", "owner", "reviewer"]),
            infra=rng.choice(["AWS", "GCP", "Azure"]))
        out.append((c, k))
    return out


# Import here to avoid circular at module level
def _make_store():
    from .core import MemoryStore
    return MemoryStore(prefer_dense=False, write_validation=False,
                       auto_graph=False, proactive_surfacing=False)

MemoryStore = None  # Lazy import


class Benchmark:

    def __init__(self, store_factory=None, seed: int = 42):
        self._f = store_factory or _make_store
        self._seed = seed

    def run_all(self, sizes: list[int] | None = None) -> list[BenchmarkResult]:
        sizes = sizes or [100, 1000, 5000]
        return asyncio.run(self._run_all_async(sizes))

    async def _run_all_async(self, sizes):
        return [
            await self._scale_write(sizes),
            await self._scale_recall(sizes),
            await self._retrieval_fidelity(),
            await self._consolidation_efficiency(),
            await self._temporal_retrieval(),
            await self._conversation_ingestion(),
        ]

    async def _scale_write(self, sizes: list[int]) -> BenchmarkResult:
        m: dict[str, float] = {}
        t0 = time.time()
        for n in sizes:
            s = self._f()
            wl = generate_workload(n, self._seed)
            st = time.time()
            for c, k in wl:
                await s.async_add(c, kind=k)
            el = time.time() - st
            m[f"write_{n}_total_s"] = round(el, 4)
            m[f"write_{n}_per_ms"] = round(el / n * 1000, 4)
            await s.async_close()
        return BenchmarkResult("scale_write", m, {"sizes": sizes},
                               time.time() - t0)

    async def _scale_recall(self, sizes: list[int]) -> BenchmarkResult:
        m: dict[str, float] = {}
        t0 = time.time()
        qs = ["deployment issues", "customer feedback",
              "security concerns", "performance metrics",
              "team responsibilities"]
        for n in sizes:
            s = self._f()
            for c, k in generate_workload(n, self._seed):
                await s.async_add(c, kind=k)
            lats = []
            for q in qs:
                st = time.time()
                await s.async_recall(q, limit=10)
                lats.append(time.time() - st)
            m[f"recall_{n}_mean_ms"] = round(statistics.mean(lats) * 1000, 4)
            m[f"recall_{n}_p95_ms"] = round(
                sorted(lats)[int(len(lats) * 0.95)] * 1000, 4)
            await s.async_close()
        return BenchmarkResult("scale_recall", m, {"sizes": sizes},
                               time.time() - t0)

    async def _retrieval_fidelity(self, n: int = 500) -> BenchmarkResult:
        t0 = time.time()
        s = self._f()
        for c, k in generate_workload(n, self._seed):
            await s.async_add(c, kind=k)
        targets = [
            ("The CEO's name is Alice Johnson who founded the company in 2019", "entity"),
            ("Alice prefers weekly standups over daily ones", "preference"),
            ("Alice's direct report Bob handles backend engineering", "entity")]
        tids = []
        for c, k in targets:
            node = await s.async_add(c, kind=k, importance=0.8)
            tids.append(node.id)
        results = await s.async_recall("Who is Alice and what does she prefer?", limit=10)
        rids = {r.node.id for r in results}
        hits = sum(1 for t in tids if t in rids)
        await s.async_close()
        return BenchmarkResult("retrieval_fidelity", {
            "precision_at_10": round(hits / min(len(results), len(tids)), 4)
                               if results else 0,
            "recall_at_10": round(hits / len(tids), 4),
            "targets_found": hits, "background": n},
            duration_seconds=time.time() - t0)

    async def _consolidation_efficiency(self, n: int = 200) -> BenchmarkResult:
        t0 = time.time()
        s = self._f()
        for i in range(n):
            await s.async_add(f"Docker pipeline variant {i % 10}", kind="fact")
        before = await s.async_len()
        st = time.time()
        await s.async_consolidate()
        ct = time.time() - st
        stats = await s.async_stats()
        await s.async_close()
        return BenchmarkResult("consolidation_efficiency", {
            "before": before, "active_after": stats["active_memories"],
            "time_ms": round(ct * 1000, 4),
            "reduction_pct": round(
                (1 - stats["active_memories"] / before) * 100, 2)
                             if before else 0},
            duration_seconds=time.time() - t0)

    async def _temporal_retrieval(self) -> BenchmarkResult:
        t0 = time.time()
        s = self._f()
        now = time.time()
        old = await s.async_add("Deployed v1.0 to production", kind="event")
        old_node = await s.async_get(old.id)
        old_node.created_at = now - 86400 * 30
        await s._storage.save_node(old_node)
        recent = await s.async_add("Deployed v2.0 to production", kind="event")
        recent_node = await s.async_get(recent.id)
        recent_node.created_at = now - 3600
        await s._storage.save_node(recent_node)
        results = await s.async_recall("deployment to production", limit=5,
                                        weights={"temporal": 0.4, "semantic": 0.3,
                                                 "lexical": 0.1, "activation": 0.1,
                                                 "graph": 0.0, "importance": 0.1})
        rr = or_ = None
        for i, r in enumerate(results):
            if r.node.id == recent.id:
                rr = i
            if r.node.id == old.id:
                or_ = i
        await s.async_close()
        return BenchmarkResult("temporal_retrieval", {
            "recent_rank": rr if rr is not None else -1,
            "old_rank": or_ if or_ is not None else -1,
            "recent_preferred": 1 if rr is not None and (
                or_ is None or rr < or_) else 0},
            duration_seconds=time.time() - t0)

    async def _conversation_ingestion(self) -> BenchmarkResult:
        t0 = time.time()
        s = self._f()
        messages = [
            {"role": "user", "content": "Hi, my name is Alice Johnson and I'm the CEO of TechCorp."},
            {"role": "assistant", "content": "Nice to meet you, Alice! How can I help you today?"},
            {"role": "user", "content": "I prefer to have our meetings on Tuesdays at 2pm. We use Slack for team communication."},
            {"role": "assistant", "content": "Got it. Tuesday 2pm meetings and Slack for communication."},
            {"role": "user", "content": "Our main product is a B2B SaaS platform. Revenue last quarter was $2.5M."},
            {"role": "assistant", "content": "Understood. B2B SaaS with $2.5M quarterly revenue."},
        ]
        st = time.time()
        nodes = await s.async_ingest_conversation(messages, session_id="bench")
        ingest_time = time.time() - st

        results = await s.async_recall("Who is Alice and what company?", limit=5)
        alice_found = any("alice" in r.node.content.lower() for r in results)

        results2 = await s.async_recall("meeting schedule preferences", limit=5)
        pref_found = any("tuesday" in r.node.content.lower() for r in results2)

        await s.async_close()
        return BenchmarkResult("conversation_ingestion", {
            "memories_extracted": len(nodes),
            "ingest_time_ms": round(ingest_time * 1000, 4),
            "alice_found": 1 if alice_found else 0,
            "preference_found": 1 if pref_found else 0,
        }, duration_seconds=time.time() - t0)
