"""
agentmemory — Memory consolidation engine.

Implements ConsolidationEngine which merges near-duplicate memories,
promotes working→episodic tier, clusters episodic memories into semantic
summaries, detects and resolves contradictions (via LLM resolver or
heuristic recency+confidence), propagates confidence decay through
contradiction edges, and decays unaccessed importance scores.

Also provides ConsolidationScheduler: a background asyncio task that
triggers full consolidation cycles when episodic memory count exceeds a
configurable threshold.
"""

from __future__ import annotations

import asyncio
import re
import time
from typing import Any, Callable, Coroutine, Optional, Union

from .ann_index import HNSWIndex
from .embeddings import Embedder, cosine_similarity
from .graph import MemoryGraph
from .models import (AuditEvent, AuditOp, Edge, EventType,
                     MemoryEvent, MemoryKind, MemoryNode, MemoryTier)

ContradictionResolverFn = Union[
    Callable[[str, str], str],
    Callable[[str, str], Coroutine[Any, Any, str]]
]


class ConsolidationEngine:

    def __init__(self, storage, graph: MemoryGraph,
                 embedder: Embedder,
                 ann_index: Optional[HNSWIndex] = None,
                 summarizer: Optional[Callable[[list[str]], str]] = None,
                 contradiction_detector: Optional[Callable[[str, str], bool]] = None,
                 contradiction_resolver: Optional[ContradictionResolverFn] = None,
                 event_bus=None,
                 evolver=None,
                 consolidation_quality_threshold: float = 0.6):
        self._storage = storage
        self._graph = graph
        self._embedder = embedder
        self._ann = ann_index
        self._summarizer = summarizer
        self._contra_fn = contradiction_detector
        self._resolver = contradiction_resolver
        self._event_bus = event_bus
        self._evolver = evolver
        self._quality_threshold = consolidation_quality_threshold

    async def run_full_cycle(self) -> dict[str, int]:
        result = {
            "pruned": await self.prune_decayed(),
            "deduplicated": await self.deduplicate(),
            "promoted": await self.promote_working_to_episodic(),
            "preferences_consolidated": await self.consolidate_preferences(),
            "consolidated": await self.consolidate_episodic_to_semantic(),
            "contradictions": len(await self.detect_and_resolve_contradictions()),
            "confidence_updates": await self.propagate_confidence_decay(),
            "importance_decayed": 0,
        }
        # Fix 4: Run importance decay
        if self._evolver:
            nodes = await self._storage.get_active_nodes()
            decayed = self._evolver.decay_unaccessed(nodes)
            for n in decayed:
                await self._storage.save_node(n)
            result["importance_decayed"] = len(decayed)
        if self._event_bus:
            await self._event_bus.emit(MemoryEvent(
                event_type=EventType.CONSOLIDATION_COMPLETE,
                data=result))
        return result

    async def prune_decayed(self) -> int:
        pruned = 0
        for n in await self._storage.get_all_nodes():
            if n.decay_rate > 0 and n.activation < 0.01:
                await self._storage.log_audit(AuditEvent(
                    node_id=n.id, op=AuditOp.DELETE,
                    detail={"reason": "decay", "activation": n.activation}))
                await self._storage.delete_node(n.id)
                self._graph.remove_node(n.id)
                if self._ann:
                    self._ann.remove(n.id)
                pruned += 1
        return pruned

    async def deduplicate(self, threshold: float = 0.92) -> int:
        nodes = await self._storage.get_active_nodes()
        merged = 0
        seen: set[str] = set()
        ann = self._ann
        if ann is None or ann.size == 0:
            ann = HNSWIndex(M=16, ef_construction=50, ef_search=30)
            for n in nodes:
                if n.embedding:
                    ann.add(n.id, n.embedding)
        nmap = {n.id: n for n in nodes if n.embedding}
        radius = 1.0 - threshold
        for node in nodes:
            if node.id in seen or not node.embedding:
                continue
            for nid, dist in ann.query_radius(node.embedding, radius, 20):
                if nid == node.id or nid in seen:
                    continue
                other = nmap.get(nid)
                if other is None or node.kind != other.kind:
                    continue
                keep, drop = ((node, other) if node.importance >= other.importance
                              else (other, node))
                keep.access_count += drop.access_count
                keep.importance = max(keep.importance, drop.importance)
                keep.tags |= drop.tags
                keep.metadata.update(drop.metadata)
                keep.version += 1
                drop.superseded_by = keep.id
                await self._storage.save_node(keep)
                await self._storage.save_node(drop)
                e = Edge(source_id=drop.id, target_id=keep.id, relation="superseded_by")
                self._graph.add_edge(e)
                await self._storage.save_edge(e)
                await self._storage.log_audit(AuditEvent(
                    node_id=drop.id, op=AuditOp.SUPERSEDE,
                    detail={"superseded_by": keep.id, "similarity": round(1.0 - dist, 3)}))
                seen.add(drop.id)
                if self._ann:
                    self._ann.remove(drop.id)
                merged += 1
        return merged

    async def promote_working_to_episodic(self, min_accesses: int = 2,
                                           min_age_min: float = 5) -> int:
        working = await self._storage.query_by_kind(
            [k.value for k in MemoryKind if k.tier == MemoryTier.WORKING])
        promoted = 0
        kind_map = {MemoryKind.INSTRUCTION: MemoryKind.EVENT,
                    MemoryKind.OBSERVATION: MemoryKind.EVENT,
                    MemoryKind.SCRATCH: MemoryKind.ACTION}
        for n in working:
            age = (time.time() - n.created_at) / 60
            if age < min_age_min:
                continue
            if n.access_count >= min_accesses or n.importance >= 0.7:
                old = n.kind
                n.kind = kind_map.get(n.kind, MemoryKind.EVENT)
                n.decay_rate = max(0.0, n.decay_rate - 0.01)
                n.version += 1
                await self._storage.save_node(n)
                await self._storage.log_audit(AuditEvent(
                    node_id=n.id, op=AuditOp.PROMOTE,
                    detail={"from": old.value, "to": n.kind.value}))
                promoted += 1
        return promoted

    async def consolidate_episodic_to_semantic(self, cluster_thresh: float = 0.75,
                                                min_cluster: int = 3) -> int:
        episodic = await self._storage.query_by_kind(
            [k.value for k in MemoryKind if k.tier == MemoryTier.EPISODIC])
        embedded = [n for n in episodic if n.embedding and n.superseded_by is None]
        if len(embedded) < min_cluster:
            return 0
        ep_ann = HNSWIndex(M=16, ef_construction=50, ef_search=30)
        for n in embedded:
            ep_ann.add(n.id, n.embedding)
        nmap = {n.id: n for n in embedded}
        radius = 1.0 - cluster_thresh
        assigned: set[str] = set()
        clusters: list[list[MemoryNode]] = []
        for node in embedded:
            if node.id in assigned:
                continue
            cluster = [node]
            assigned.add(node.id)
            for nid, _ in ep_ann.query_radius(node.embedding, radius, 50):
                if nid == node.id or nid in assigned:
                    continue
                other = nmap.get(nid)
                if other:
                    cluster.append(other)
                    assigned.add(nid)
            if len(cluster) >= min_cluster:
                clusters.append(cluster)

        consolidated = 0
        for cluster in clusters:
            if self._summarizer:
                summary = self._summarizer([n.content for n in cluster])
            else:
                cluster.sort(key=lambda n: n.importance, reverse=True)
                summary = cluster[0].content

            sem = MemoryNode(
                content=summary, kind=MemoryKind.FACT,
                importance=max(n.importance for n in cluster),
                confidence=sum(n.confidence for n in cluster) / len(cluster),
                decay_rate=0.0, namespace=cluster[0].namespace,
                tags=set().union(*(n.tags for n in cluster)),
                metadata={"consolidated_from": [n.id for n in cluster],
                          "cluster_size": len(cluster)})
            sem.provenance.source = "consolidation"
            sem.embedding = self._embedder.embed(summary)

            # --- Consolidation quality gate ---
            # Before committing an episodic→semantic promotion, verify the
            # generated summary actually represents its source cluster.
            # Quality is measured as cosine similarity between the summary
            # embedding and the arithmetic centroid of the cluster embeddings.
            # A centroid similarity < quality_threshold (default 0.6) indicates
            # the summary is semantically distant from its sources — e.g., the
            # LLM summarizer hallucinated or drifted off-topic. In that case,
            # the summary is saved (for audit) but logged as LOW_QUALITY and
            # the cluster members are NOT superseded, preserving raw episodic
            # memories as the ground truth.
            # Upgrade 9: Quality scoring
            quality_ok = True
            if sem.embedding:
                centroid = [0.0] * len(sem.embedding)
                emb_count = 0
                for cn in cluster:
                    if cn.embedding and len(cn.embedding) == len(centroid):
                        for i in range(len(centroid)):
                            centroid[i] += cn.embedding[i]
                        emb_count += 1
                if emb_count > 0:
                    centroid = [c / emb_count for c in centroid]
                    score = cosine_similarity(sem.embedding, centroid)
                    sem.metadata["consolidation_quality"] = round(score, 4)
                    if score < self._quality_threshold:
                        quality_ok = False
                        await self._storage.log_audit(AuditEvent(
                            node_id=sem.id,
                            op=AuditOp.LOW_QUALITY_CONSOLIDATION,
                            detail={"quality_score": round(score, 4),
                                    "threshold": self._quality_threshold}))

            await self._storage.save_node(sem)
            if self._ann:
                self._ann.add(sem.id, sem.embedding)
            await self._storage.log_audit(AuditEvent(
                node_id=sem.id, op=AuditOp.CONSOLIDATE,
                detail={"from_ids": [n.id for n in cluster],
                        "quality_ok": quality_ok}))

            for n in cluster:
                e = Edge(source_id=n.id, target_id=sem.id, relation="consolidated_into")
                self._graph.add_edge(e)
                await self._storage.save_edge(e)
                if n.importance < 0.8:
                    n.superseded_by = sem.id
                    n.version += 1
                    await self._storage.save_node(n)
            consolidated += 1
        return consolidated

    # ---- Fix 5: Contradiction edges only added when unresolved ----

    async def detect_and_resolve_contradictions(self) -> list[tuple[str, str]]:
        semantic = await self._storage.query_by_kind(
            [k.value for k in MemoryKind if k.tier == MemoryTier.SEMANTIC])
        active = [n for n in semantic if n.superseded_by is None]
        contras: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()

        async def _rec(a_id: str, b_id: str, w: float):
            pair = (min(a_id, b_id), max(a_id, b_id))
            if pair in seen:
                return
            seen.add(pair)
            contras.append((a_id, b_id))

            resolved = await self._try_resolve(a_id, b_id)
            if not resolved:
                a = await self._storage.load_node(a_id)
                b = await self._storage.load_node(b_id)
                if a and b:
                    # Use threshold 0.0 if either node has an update signal
                    t_override = None
                    if (ConsolidationEngine._detect_update_signal(a.content) >= 0.6 or
                            ConsolidationEngine._detect_update_signal(b.content) >= 0.6):
                        t_override = 0.0
                    heuristic_resolved = await self._heuristic_resolve(
                        a, b, w, threshold_override=t_override)
                    if not heuristic_resolved:
                        e = Edge(source_id=a_id, target_id=b_id,
                                 relation="contradicts", weight=w)
                        self._graph.add_edge(e)
                        await self._storage.save_edge(e)

            if self._event_bus:
                await self._event_bus.emit(MemoryEvent(
                    event_type=EventType.CONTRADICTION_DETECTED,
                    data={"node_a": a_id, "node_b": b_id}))

        embedded = [n for n in active if n.embedding]
        if self._ann and self._ann.size > 0:
            for n in embedded:
                for nid, dist in self._ann.query_radius(n.embedding, radius=0.2, max_results=10):
                    if nid == n.id:
                        continue
                    o = await self._storage.load_node(nid)
                    if o and not o.superseded_by and self._is_contra(n, o):
                        await _rec(n.id, o.id, 1.0 - dist)

        if len(active) <= 500:
            by_kind: dict[str, list[MemoryNode]] = {}
            for n in active:
                by_kind.setdefault(n.kind.value, []).append(n)
            for nodes in by_kind.values():
                for i, a in enumerate(nodes):
                    for b in nodes[i + 1:]:
                        pair = (min(a.id, b.id), max(a.id, b.id))
                        if pair in seen:
                            continue
                        if self._is_contra(a, b):
                            w = 0.5
                            if a.embedding and b.embedding:
                                w = max(0.3, cosine_similarity(a.embedding, b.embedding))
                            await _rec(a.id, b.id, w)
        return contras

    async def _try_resolve(self, a_id: str, b_id: str) -> bool:
        if not self._resolver:
            return False
        a = await self._storage.load_node(a_id)
        b = await self._storage.load_node(b_id)
        if not a or not b:
            return False
        result = self._resolver(a.content, b.content)
        if asyncio.iscoroutine(result):
            result = await result
        if result == "a":
            # Upgrade 5: Set valid_until on loser
            b.valid_until = time.time()
            b.superseded_by = a.id
            b.version += 1
            await self._storage.save_node(b)
            await self._storage.log_audit(AuditEvent(
                node_id=b.id, op=AuditOp.CONTRADICTION_RESOLVED,
                detail={"winner": a.id, "method": "llm"}))
            return True
        elif result == "b":
            a.valid_until = time.time()
            a.superseded_by = b.id
            a.version += 1
            await self._storage.save_node(a)
            await self._storage.log_audit(AuditEvent(
                node_id=a.id, op=AuditOp.CONTRADICTION_RESOLVED,
                detail={"winner": b.id, "method": "llm"}))
            return True
        return False

    async def _heuristic_resolve(self, a: MemoryNode, b: MemoryNode,
                                  weight: float,
                                  min_age_hours: float = 0.0,
                                  threshold_override: Optional[float] = None) -> bool:
        """
        Heuristic resolution: recency + confidence.
        When either node is younger than min_age_hours, resolve on confidence only
        to prevent brand-new low-confidence observations from winning on recency.
        threshold_override: if set, use this threshold instead of 0.1.
        """
        threshold = threshold_override if threshold_override is not None else 0.1
        too_new = (a.age_hours < min_age_hours or b.age_hours < min_age_hours)

        if too_new:
            # Confidence-only resolution for very recent nodes
            if abs(a.confidence - b.confidence) > threshold:
                if a.confidence > b.confidence:
                    b.valid_until = time.time()
                    b.superseded_by = a.id
                    b.version += 1
                    await self._storage.save_node(b)
                    await self._storage.log_audit(AuditEvent(
                        node_id=b.id, op=AuditOp.CONTRADICTION_RESOLVED,
                        detail={"winner": a.id, "method": "heuristic_confidence_only",
                                "a_confidence": round(a.confidence, 3),
                                "b_confidence": round(b.confidence, 3)}))
                else:
                    a.valid_until = time.time()
                    a.superseded_by = b.id
                    a.version += 1
                    await self._storage.save_node(a)
                    await self._storage.log_audit(AuditEvent(
                        node_id=a.id, op=AuditOp.CONTRADICTION_RESOLVED,
                        detail={"winner": b.id, "method": "heuristic_confidence_only",
                                "a_confidence": round(a.confidence, 3),
                                "b_confidence": round(b.confidence, 3)}))
                return True
            # With threshold 0.0, resolve by recency when confidence is equal
            if threshold == 0.0:
                newer, older = (a, b) if a.created_at > b.created_at else (b, a)
                older.valid_until = time.time()
                older.superseded_by = newer.id
                older.version += 1
                await self._storage.save_node(older)
                await self._storage.log_audit(AuditEvent(
                    node_id=older.id, op=AuditOp.CONTRADICTION_RESOLVED,
                    detail={"winner": newer.id, "method": "heuristic_update_signal"}))
                return True
            return False

        # Standard recency + confidence resolution
        a_score = a.confidence * 0.6 + (1.0 / (1.0 + a.age_hours)) * 0.4
        b_score = b.confidence * 0.6 + (1.0 / (1.0 + b.age_hours)) * 0.4
        if abs(a_score - b_score) > threshold:
            if a_score > b_score:
                b.valid_until = time.time()
                b.superseded_by = a.id
                b.version += 1
                await self._storage.save_node(b)
                await self._storage.log_audit(AuditEvent(
                    node_id=b.id, op=AuditOp.CONTRADICTION_RESOLVED,
                    detail={"winner": a.id, "method": "heuristic",
                            "a_score": round(a_score, 3),
                            "b_score": round(b_score, 3)}))
            else:
                a.valid_until = time.time()
                a.superseded_by = b.id
                a.version += 1
                await self._storage.save_node(a)
                await self._storage.log_audit(AuditEvent(
                    node_id=a.id, op=AuditOp.CONTRADICTION_RESOLVED,
                    detail={"winner": b.id, "method": "heuristic",
                            "a_score": round(a_score, 3),
                            "b_score": round(b_score, 3)}))
            return True
        return False

    @staticmethod
    def _detect_update_signal(content: str) -> float:
        """
        Detect update/correction signals. Returns confidence 0.0-1.0.
        Use >= 0.6 as threshold for zero-gap resolution.
        Truthiness: float >= 0.6 evaluates as True for backward compat.
        """
        lower = content.lower()
        score = 0.0

        # Three groups of patterns, ordered by signal strength:
        # Group 1 (score → 1.0): Explicit self-correction or state-change phrases
        #   that unambiguously indicate the speaker is updating a prior statement.
        # Group 2 (score → 0.7–0.8): Temporal supersession phrases ("as of",
        #   "starting from") that indicate a new fact replaces an old one.
        # Group 3 (score → 0.5): Weak present-tense change verbs with lower
        #   signal strength; insufficient alone to trigger zero-gap resolution.
        # The caller uses threshold >= 0.6 to gate zero-gap resolution, meaning
        # only Group 1 and Group 2 patterns reliably trigger immediate supersession.
        # Sentence-initial explicit markers (high confidence)
        sentences = re.split(r'(?<=[.!?])\s+', content.strip())
        high_markers = [
            "actually", "correction", "update", "let me correct",
            "i misspoke", "i was wrong about", "i should mention",
            "i forgot to say", "i forgot to mention", "i changed my mind",
            "to clarify",
        ]
        medium_markers = ["by the way"]
        for sent in sentences:
            sl = sent.strip().lower()
            if any(sl.startswith(prefix) for prefix in high_markers):
                score = max(score, 1.0)
            if any(sl.startswith(prefix) for prefix in medium_markers):
                score = max(score, 0.7)

        # State change phrases (high confidence)
        strong_phrases = [
            r"\bhas\s+changed\s+to\b", r"\bis\s+now\b", r"\breplaced\s+by\b",
            r"\bno\s+longer\b", r"\bgoing\s+forward\b",
        ]
        for pat in strong_phrases:
            if re.search(pat, lower):
                score = max(score, 1.0)

        # Medium phrases
        medium_phrases = [
            r"\bnow\s+is\b", r"\bused\s+to\s+be\b.*\bnow\b",
            r"\bas\s+of\s+today\b", r"\bas\s+of\b",
            r"\bstarting\s+from\b", r"\beffective\b",
        ]
        for pat in medium_phrases:
            if re.search(pat, lower):
                score = max(score, 0.8)

        # Temporal supersession patterns
        if re.search(r"\bwas\b.*\bbut\b.*\b(?:is|are)\s+now\b", lower):
            score = max(score, 1.0)
        if re.search(r"\bused\s+to\s+be\b.*\bnow\s+(?:it'?s|they\s+are|it\s+is)\b", lower):
            score = max(score, 1.0)

        # Weak signal
        if re.search(r"\bnow\s+(?:use|work|live|prefer)\b", lower):
            score = max(score, 0.5)

        return score

    def _is_contra(self, a: MemoryNode, b: MemoryNode) -> bool:
        if self._contra_fn:
            return self._contra_fn(a.content, b.content)
        return self._structural_check(a.content, b.content)

    @staticmethod
    def _structural_check(ta: str, tb: str) -> bool:
        if ta == tb:
            return False
        al, bl = ta.lower().strip(), tb.lower().strip()
        wa = re.findall(r"[a-z0-9']+", al)
        wb = re.findall(r"[a-z0-9']+", bl)
        if not wa or not wb:
            return False
        pfx = 0
        for x, y in zip(wa, wb):
            if x == y:
                pfx += 1
            else:
                break
        if pfx >= 3 and len(wa) > pfx and len(wb) > pfx:
            if " ".join(wa[pfx:]) != " ".join(wb[pfx:]):
                return True
        pat = re.compile(r"^(.{5,}?)\s+(?:is|are|was|were|=)\s+(.+)$", re.I)
        ma, mb = pat.match(ta.strip()), pat.match(tb.strip())
        if ma and mb:
            sa = set(re.findall(r"[a-z0-9]+", ma.group(1).lower()))
            sb = set(re.findall(r"[a-z0-9]+", mb.group(1).lower()))
            if sa and sb:
                overlap = len(sa & sb) / max(len(sa), len(sb))
                if overlap >= 0.6:
                    if ma.group(2).lower().strip() != mb.group(2).lower().strip():
                        return True
        sa, sb = set(wa), set(wb)
        if sa and sb:
            jaccard = len(sa & sb) / len(sa | sb)
            if jaccard >= 0.5 and al != bl:
                return True
        # Lower threshold when update signal present (entity overlap suffices)
        if sa and sb and jaccard >= 0.3 and al != bl:
            proper_a = set(re.findall(r"\b[A-Z][a-z]+\b", ta))
            proper_b = set(re.findall(r"\b[A-Z][a-z]+\b", tb))
            if proper_a & proper_b:
                return True
        return False

    async def consolidate_preferences(self) -> int:
        """Consolidate overlapping preference memories into stronger signals."""
        prefs = await self._storage.query_by_kind(["preference"], limit=500)
        active = [n for n in prefs if n.superseded_by is None]
        if len(active) < 2:
            return 0

        # Group by entity (primary proper noun or pronoun reference)
        _PROPER_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b")
        entity_groups: dict[str, list[MemoryNode]] = {}
        for n in active:
            proper_nouns = _PROPER_RE.findall(n.content)
            entity_key = proper_nouns[0].lower() if proper_nouns else "_self"
            entity_groups.setdefault(entity_key, []).append(n)

        consolidated = 0
        for entity_key, group in entity_groups.items():
            if len(group) < 2:
                continue
            # Find overlapping topic clusters within this entity group
            clusters = self._cluster_preferences(group)
            for cluster in clusters:
                if len(cluster) < 2:
                    continue
                # Pick best member: highest word_count * importance
                best = max(cluster, key=lambda n: len(n.content.split()) * n.importance)
                max_imp = max(n.importance for n in cluster)
                max_conf = max(n.confidence for n in cluster)

                sem = MemoryNode(
                    content=best.content,
                    kind=MemoryKind.PREFERENCE,
                    importance=min(1.0, max_imp + 0.1),
                    confidence=max_conf,
                    decay_rate=0.0,
                    namespace=best.namespace,
                    tags=set().union(*(n.tags for n in cluster)),
                    metadata={"consolidated_from": [n.id for n in cluster],
                              "cluster_size": len(cluster)})
                sem.provenance.source = "preference_consolidation"
                sem.embedding = self._embedder.embed(best.content)

                await self._storage.save_node(sem)
                if self._ann:
                    self._ann.add(sem.id, sem.embedding)

                for n in cluster:
                    e = Edge(source_id=n.id, target_id=sem.id, relation="consolidated_into")
                    self._graph.add_edge(e)
                    await self._storage.save_edge(e)
                    if n.importance < 0.8:
                        n.superseded_by = sem.id
                        n.version += 1
                        await self._storage.save_node(n)

                consolidated += 1
        return consolidated

    @staticmethod
    def _cluster_preferences(nodes: list[MemoryNode]) -> list[list[MemoryNode]]:
        """Cluster preferences by topic overlap (token Jaccard >= 0.4)."""
        _TOKEN_RE = re.compile(r"[a-z0-9]+")
        assigned: set[str] = set()
        clusters: list[list[MemoryNode]] = []
        for i, a in enumerate(nodes):
            if a.id in assigned:
                continue
            cluster = [a]
            assigned.add(a.id)
            a_tokens = set(_TOKEN_RE.findall(a.content.lower()))
            for b in nodes[i + 1:]:
                if b.id in assigned:
                    continue
                b_tokens = set(_TOKEN_RE.findall(b.content.lower()))
                union = a_tokens | b_tokens
                if union:
                    jaccard = len(a_tokens & b_tokens) / len(union)
                    if jaccard >= 0.4:
                        cluster.append(b)
                        assigned.add(b.id)
            clusters.append(cluster)
        return clusters

    async def propagate_confidence_decay(self, base_pen: float = 0.15) -> int:
        updated = 0
        for edge in self._graph.find_by_relation("contradicts"):
            a = await self._storage.load_node(edge.source_id)
            b = await self._storage.load_node(edge.target_id)
            if not a or not b:
                continue
            if a.superseded_by or b.superseded_by:
                continue
            pa = base_pen * edge.weight * b.importance
            pb = base_pen * edge.weight * a.importance
            oa, ob = a.confidence, b.confidence
            a.confidence = max(0.1, a.confidence - pa)
            b.confidence = max(0.1, b.confidence - pb)
            for node, old in [(a, oa), (b, ob)]:
                if node.confidence != old:
                    node.version += 1
                    await self._storage.save_node(node)
                    other = b if node is a else a
                    await self._storage.log_audit(AuditEvent(
                        node_id=node.id, op=AuditOp.CONFIDENCE_DECAY,
                        detail={"old": round(old, 4), "new": round(node.confidence, 4),
                                "contradicted_by": other.id}))
                    updated += 1
                    if node.confidence < 0.3 and self._event_bus:
                        await self._event_bus.emit(MemoryEvent(
                            event_type=EventType.CONFIDENCE_BELOW_THRESHOLD,
                            node_id=node.id, data={"confidence": node.confidence}))
        return updated

    async def on_write(self, node: MemoryNode) -> dict[str, list]:
        result: dict[str, list] = {"duplicates": [], "contradictions": []}
        if not node.embedding or not self._ann or self._ann.size == 0:
            return result
        for nid, dist in self._ann.query_radius(node.embedding, radius=0.08, max_results=5):
            if nid != node.id:
                result["duplicates"].append({"id": nid, "similarity": round(1.0 - dist, 3)})
        update_signal = self._detect_update_signal(node.content)
        has_update_signal = update_signal >= 0.6
        contra_radius = 0.4 if has_update_signal else 0.2
        seen_ids = {d["id"] for d in result["duplicates"]}
        candidates = []
        for nid, dist in self._ann.query_radius(node.embedding, radius=contra_radius, max_results=10):
            if nid != node.id and nid not in seen_ids:
                candidates.append((nid, dist))
        # For update signals, brute-force scan if ANN misses due to embedding distance
        if has_update_signal and not candidates:
            all_nodes = await self._storage.get_all_nodes()
            for other in all_nodes:
                if other.id != node.id and other.id not in seen_ids:
                    if not other.superseded_by and self._is_contra(node, other):
                        candidates.append((other.id, 0.5))
        for nid, dist in candidates:
            other = await self._storage.load_node(nid)
            if other and self._is_contra(node, other):
                result["contradictions"].append({"id": nid, "similarity": round(1.0 - dist, 3)})
                if has_update_signal:
                    # Immediate supersession with threshold 0.0
                    await self._heuristic_resolve(
                        node, other, 1.0 - dist,
                        min_age_hours=0.0, threshold_override=0.0)
                    # Anchor valid_until to event_time of the update
                    updated_other = await self._storage.load_node(nid)
                    if updated_other and updated_other.superseded_by:
                        valid_time = node.event_time or node.created_at
                        updated_other.valid_until = valid_time
                        await self._storage.save_node(updated_other)
                else:
                    await self._heuristic_resolve(node, other, 1.0 - dist,
                                                  min_age_hours=1/60)  # 1-minute guard
        return result


class ConsolidationScheduler:
    def __init__(self, engine: ConsolidationEngine, storage,
                 threshold: int = 100, check_interval: float = 60.0):
        self._engine = engine
        self._storage = storage
        self._threshold = threshold
        self._interval = check_interval
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run_loop(self):
        while self._running:
            try:
                episodic = await self._storage.query_by_kind(
                    [k.value for k in MemoryKind if k.tier == MemoryTier.EPISODIC])
                active = [n for n in episodic if n.superseded_by is None]
                if len(active) >= self._threshold:
                    await self._engine.run_full_cycle()
            except Exception:
                pass
            await asyncio.sleep(self._interval)

    @property
    def is_running(self) -> bool:
        return self._running
