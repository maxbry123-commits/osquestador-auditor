"""
agentmemory — Hybrid retrieval engine.

Implements RetrievalEngine: a six-signal hybrid scorer combining semantic
cosine similarity, BM25 lexical search, node activation, graph spreading
activation, importance×confidence, and temporal Gaussian proximity. Also
provides QueryCache (LRU), RetrieverWeightAdapter (adaptive EMA weight
learning), and RetrievalQuery (query parameter dataclass).
"""

from __future__ import annotations

import json
import math
import os
import re
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Callable, Optional

from .ann_index import HNSWIndex
from .embeddings import Embedder, cosine_similarity
from .graph import MemoryGraph
from .importance import ImportanceEvolver
from .models import (FilterExpr, MemoryKind, MemoryNode, MemoryTier,
                     Namespace, RetrievalResult)


@dataclass
class RetrievalQuery:
    text: str = ""
    embedding: Optional[list[float]] = None
    tiers: Optional[set[MemoryTier]] = None
    kinds: Optional[set[MemoryKind]] = None
    tags: Optional[set[str]] = None
    sources: Optional[set[str]] = None
    session_id: Optional[str] = None
    namespace: Optional[Namespace] = None
    min_importance: float = 0.0
    min_confidence: float = 0.0
    exclude_superseded: bool = True
    include_expired: bool = False  # Upgrade 5
    time_start: Optional[float] = None
    time_end: Optional[float] = None
    event_time_start: Optional[float] = None
    event_time_end: Optional[float] = None
    temporal_center: Optional[float] = None
    temporal_width_hours: float = 168.0
    use_event_time: bool = False
    w_semantic: float = 0.30
    w_lexical: float = 0.12
    w_activation: float = 0.18
    w_graph: float = 0.18
    w_importance: float = 0.10
    w_temporal: float = 0.12
    context_ids: list[str] = field(default_factory=list)
    limit: int = 10
    graph_depth: int = 2
    ann_candidates: int = 200
    filter_expr: Optional[FilterExpr] = None
    kind_boost: Optional[dict] = None  # {MemoryKind: float multiplier}


class QueryCache:
    def __init__(self, max_size: int = 128):
        self._cache: OrderedDict[str, list[RetrievalResult]] = OrderedDict()
        self._max_size = max_size

    def get(self, key: str) -> Optional[list[RetrievalResult]]:
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(self, key: str, results: list[RetrievalResult]):
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)
        self._cache[key] = results

    def invalidate(self):
        self._cache.clear()


# ---- Upgrade 2: Adaptive Retrieval Weight Learning ----

class RetrieverWeightAdapter:
    """
    Learns optimal retrieval signal weights from quality feedback.
    Maintains EMA of per-signal correlation with quality scores.
    """

    SIGNALS = ("semantic", "lexical", "activation", "graph", "importance", "temporal")

    def __init__(self, alpha: float = 0.05, checkpoint_path: Optional[str] = None):
        self._alpha = alpha
        self._checkpoint_path = checkpoint_path
        self._signal_ema: dict[str, float] = {s: 0.5 for s in self.SIGNALS}
        self._query_count = 0
        if checkpoint_path and os.path.exists(checkpoint_path):
            self._load_checkpoint()

    def record_quality(self, score_components: dict[str, float], quality: float):
        """Record quality feedback for a retrieval result."""
        self._query_count += 1
        for signal in self.SIGNALS:
            val = score_components.get(signal, 0.0)
            correlation = val * quality
            self._signal_ema[signal] = (
                (1 - self._alpha) * self._signal_ema[signal] +
                self._alpha * correlation
            )
        if self._checkpoint_path and self._query_count % 50 == 0:
            self._save_checkpoint()

    def get_adapted_weights(self) -> dict[str, float]:
        """Return adapted weights normalized to sum to 1."""
        if self._query_count < 10:
            return {}  # Not enough data, use defaults
        total = sum(max(0.01, v) for v in self._signal_ema.values())
        if total == 0:
            return {}
        return {s: round(max(0.01, v) / total, 4)
                for s, v in self._signal_ema.items()}

    def _save_checkpoint(self):
        try:
            with open(self._checkpoint_path, "w") as f:
                json.dump({"ema": self._signal_ema, "count": self._query_count}, f)
        except Exception:
            pass

    def _load_checkpoint(self):
        try:
            with open(self._checkpoint_path) as f:
                data = json.load(f)
                self._signal_ema = data.get("ema", self._signal_ema)
                self._query_count = data.get("count", 0)
        except Exception:
            pass


_PREF_QUERY_WORDS = frozenset(
    "prefer like love hate favorite always never tend usually dislike enjoy avoid".split())

# Proper-noun pattern for entity-centric retrieval
_PROPER_NOUN_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b")


class RetrievalEngine:

    def __init__(self, storage, graph: MemoryGraph,
                 embedder: Embedder,
                 ann_index: Optional[HNSWIndex] = None,
                 importance_evolver: Optional[ImportanceEvolver] = None,
                 cache_size: int = 128,
                 weight_adapter: Optional[RetrieverWeightAdapter] = None,
                 quality_evaluator_fn: Optional[Callable] = None,
                 entity_index: Optional[dict] = None,
                 query_expander=None,
                 reranker=None):
        self._storage = storage
        self._graph = graph
        self._embedder = embedder
        self._ann = ann_index
        self._evolver = importance_evolver
        self._cache = QueryCache(max_size=cache_size) if cache_size > 0 else None
        self._weight_adapter = weight_adapter
        self._quality_fn = quality_evaluator_fn
        self._entity_index = entity_index or {}
        self._query_expander = query_expander
        self._reranker = reranker

    def _cache_key(self, q: RetrievalQuery) -> str:
        parts = [q.text, str(q.limit), str(q.min_importance),
                 str(q.tiers), str(q.kinds), str(q.tags),
                 str(q.w_semantic), str(q.w_temporal), str(q.include_expired)]
        return "|".join(parts)

    async def retrieve(self, q: RetrievalQuery) -> list[RetrievalResult]:
        # Apply adaptive weights if available
        if self._weight_adapter:
            adapted = self._weight_adapter.get_adapted_weights()
            if adapted:
                for s in RetrieverWeightAdapter.SIGNALS:
                    if s in adapted and getattr(q, f"w_{s}") == getattr(RetrievalQuery(), f"w_{s}"):
                        setattr(q, f"w_{s}", adapted[s])

        if self._cache:
            key = self._cache_key(q)
            cached = self._cache.get(key)
            if cached is not None:
                return cached

        qe = q.embedding
        if qe is None and q.text:
            qe = self._embedder.embed(q.text)

        candidates = await self._candidates(q, qe)
        if not candidates:
            return []

        graph_act: dict[str, float] = {}
        if q.context_ids:
            graph_act = self._graph.spreading_activation(
                q.context_ids, max_depth=q.graph_depth)

        lex: dict[str, float] = {}
        if q.text and q.w_lexical > 0:
            fts = await self._storage.fulltext_search(q.text, limit=200)
            if fts:
                mx = max(s for _, s in fts) or 1.0
                lex = {nid: s / mx for nid, s in fts}

        now = time.time()
        # --- Six-signal hybrid scoring ---
        # Each signal is normalized to [0, 1] before weighting.
        # Default weights: semantic=0.30, lexical=0.12, activation=0.18,
        #   graph=0.18, importance=0.10, temporal=0.12
        # Weights sum to 1.0 and can be overridden per-query or learned
        # adaptively via RetrieverWeightAdapter.
        # The temporal signal uses a Gaussian centered on `temporal_center`
        # (default: now) with half-width `temporal_width_hours` (default: 168h).
        # A node created exactly at temporal_center scores 1.0; nodes further
        # away decay smoothly — sigma = temporal_width_hours * 3600 seconds.
        results: list[RetrievalResult] = []
        for node in candidates:
            c: dict[str, float] = {}
            c["semantic"] = (max(0.0, cosine_similarity(qe, node.embedding))
                             if qe and node.embedding else 0.0)
            c["lexical"] = lex.get(node.id, 0.0)
            c["activation"] = min(1.0, node.activation)
            c["graph"] = graph_act.get(node.id, 0.0)
            c["importance"] = node.importance * node.calibrated_confidence
            c["temporal"] = self._temporal(node, q, now)

            score = (q.w_semantic * c["semantic"] + q.w_lexical * c["lexical"]
                     + q.w_activation * c["activation"] + q.w_graph * c["graph"]
                     + q.w_importance * c["importance"] + q.w_temporal * c["temporal"])

            # Apply kind_boost multiplier
            if q.kind_boost:
                score *= q.kind_boost.get(node.kind, 1.0)

            results.append(RetrievalResult(
                node=node, score=score, score_components=c,
                explanation=self._explain(c, q)))

        results.sort(key=lambda r: r.score, reverse=True)

        # Cross-encoder reranking (Upgrade 5, Prompt 2)
        if self._reranker and q.text:
            rerank_pool = results[:q.limit * 4]
            rerank_pool = self._reranker.rerank(q.text, rerank_pool)
            top = rerank_pool[:q.limit]
        else:
            top = results[:q.limit]

        for r in top:
            r.node.touch()
            if self._evolver:
                self._evolver.on_access(r.node)
            await self._storage.save_node(r.node)

        # Adaptive weight learning: evaluate quality and record
        if self._quality_fn and self._weight_adapter and top:
            try:
                quality = self._quality_fn(q.text, top[0].node.content)
                self._weight_adapter.record_quality(top[0].score_components, quality)
            except Exception:
                pass

        if self._cache:
            self._cache.put(self._cache_key(q), top)
        return top

    async def _candidates(self, q: RetrievalQuery,
                          qe: Optional[list[float]]) -> list[MemoryNode]:
        cand_ids: Optional[set[str]] = None
        if self._ann and qe and self._ann.size > 0:
            cand_ids = {k for k, _ in self._ann.query(qe, k=q.ann_candidates)}
            if q.text:
                fts = await self._storage.fulltext_search(q.text, 50)
                if fts:
                    cand_ids.update(nid for nid, _ in fts)
            if q.context_ids:
                cand_ids.update(
                    self._graph.spreading_activation(
                        q.context_ids, max_depth=q.graph_depth).keys())
        if cand_ids is None and q.text:
            fts = await self._storage.fulltext_search(q.text, q.ann_candidates)
            if fts:
                cand_ids = {nid for nid, _ in fts}
                if q.context_ids:
                    cand_ids.update(
                        self._graph.spreading_activation(
                            q.context_ids, max_depth=q.graph_depth).keys())
        # Upgrade 1: Query expansion — lexical-only FTS for each expanded term
        if q.text and self._query_expander:
            expanded_terms = self._query_expander.expand(q.text)
            for term in expanded_terms:
                if term != q.text:
                    efts = await self._storage.fulltext_search(term, 30)
                    if efts:
                        if cand_ids is not None:
                            cand_ids.update(nid for nid, _ in efts)
                        else:
                            cand_ids = {nid for nid, _ in efts}
        # Entity-centric retrieval: expand candidates via entity graph
        if q.text and self._entity_index:
            proper_nouns = _PROPER_NOUN_RE.findall(q.text)
            entity_additions: set[str] = set()
            for noun in proper_nouns:
                entity_key = noun.lower().strip()
                entity_node_id = self._entity_index.get(entity_key)
                if entity_node_id:
                    activated = self._graph.spreading_activation(
                        [entity_node_id], max_depth=2)
                    entity_additions.update(activated.keys())
            if entity_additions:
                # Cap at 50 to prevent runaway expansion
                entity_additions = set(list(entity_additions)[:50])
                if cand_ids is not None:
                    cand_ids.update(entity_additions)
                else:
                    cand_ids = entity_additions

        if cand_ids is not None:
            nodes = []
            for nid in cand_ids:
                n = await self._storage.load_node(nid)
                if n:
                    nodes.append(n)
        else:
            nodes = await self._storage.get_active_nodes(q.min_importance)
        return self._filter(nodes, q)

    def _filter(self, nodes: list[MemoryNode], q: RetrievalQuery) -> list[MemoryNode]:
        now = time.time()
        out = []
        for n in nodes:
            if q.exclude_superseded and n.superseded_by:
                continue
            # Upgrade 5: Filter expired facts by default
            if not q.include_expired:
                if n.valid_until is not None and now > n.valid_until:
                    continue
            if q.tiers and n.tier not in q.tiers:
                continue
            if q.kinds and n.kind not in q.kinds:
                continue
            if q.tags and not (n.tags & q.tags):
                continue
            if q.sources and n.provenance.source not in q.sources:
                continue
            if q.session_id and n.provenance.session_id != q.session_id:
                continue
            if n.confidence < q.min_confidence:
                continue
            if n.importance < q.min_importance:
                continue
            if q.namespace and not q.namespace.contains(n.namespace):
                continue
            if q.time_start and n.created_at < q.time_start:
                continue
            if q.time_end and n.created_at > q.time_end:
                continue
            if q.event_time_start and n.effective_time < q.event_time_start:
                continue
            if q.event_time_end and n.effective_time > q.event_time_end:
                continue
            if q.filter_expr and not q.filter_expr.evaluate(n):
                continue
            out.append(n)
        return out

    @staticmethod
    def _temporal(node: MemoryNode, q: RetrievalQuery, now: float) -> float:
        center = q.temporal_center or now
        w = (q.temporal_width_hours or 168.0) * 3600  # guard against None
        if w <= 0:
            return 1.0
        t = node.effective_time if q.use_event_time else node.created_at
        return math.exp(-0.5 * ((t - center) / w) ** 2)

    @staticmethod
    def _explain(c: dict[str, float], q: RetrievalQuery) -> str:
        parts = []
        if c.get("semantic", 0) >= 0.15 and q.w_semantic > 0:
            parts.append(f"semantically similar ({int(c['semantic']*100)}%)")
        if c.get("lexical", 0) >= 0.15 and q.w_lexical > 0:
            parts.append("matching keywords")
        if c.get("activation", 0) >= 0.5 and q.w_activation > 0:
            parts.append("recently/frequently accessed")
        if c.get("graph", 0) >= 0.15 and q.w_graph > 0:
            parts.append(f"graph-linked ({int(c['graph']*100)}%)")
        if c.get("importance", 0) >= 0.7 and q.w_importance > 0:
            parts.append("high importance")
        if c.get("temporal", 0) >= 0.8 and q.w_temporal > 0:
            parts.append("within time window")
        return ("Retrieved because: " + "; ".join(parts) + ".") if parts else "General match across signals."

    def invalidate_cache(self):
        if self._cache:
            self._cache.invalidate()
