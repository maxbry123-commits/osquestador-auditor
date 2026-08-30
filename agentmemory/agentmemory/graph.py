"""
agentmemory V4 — Relationship graph with auto-construction.

V4 Fix 1: auto_link_node is async, creates real entity nodes,
persists all edges to storage.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Optional

from .models import Edge, MemoryNode


class MemoryGraph:

    def __init__(self):
        self._edges: dict[str, Edge] = {}
        self._outgoing: dict[str, set[str]] = defaultdict(set)
        self._incoming: dict[str, set[str]] = defaultdict(set)
        self._by_relation: dict[str, set[str]] = defaultdict(set)

    @property
    def edge_count(self) -> int:
        return len(self._edges)

    def add_edge(self, edge: Edge):
        self._edges[edge.id] = edge
        self._outgoing[edge.source_id].add(edge.id)
        self._incoming[edge.target_id].add(edge.id)
        self._by_relation[edge.relation].add(edge.id)

    def remove_edge(self, edge_id: str):
        e = self._edges.pop(edge_id, None)
        if e:
            self._outgoing[e.source_id].discard(edge_id)
            self._incoming[e.target_id].discard(edge_id)
            self._by_relation[e.relation].discard(edge_id)

    def remove_node(self, node_id: str):
        for eid in list(self._outgoing.get(node_id, [])):
            self.remove_edge(eid)
        for eid in list(self._incoming.get(node_id, [])):
            self.remove_edge(eid)

    def neighbors(self, node_id: str, relation: Optional[str] = None,
                  direction: str = "out") -> list[tuple[str, Edge]]:
        out = []
        if direction in ("out", "both"):
            for eid in self._outgoing.get(node_id, []):
                e = self._edges[eid]
                if relation is None or e.relation == relation:
                    out.append((e.target_id, e))
        if direction in ("in", "both"):
            for eid in self._incoming.get(node_id, []):
                e = self._edges[eid]
                if relation is None or e.relation == relation:
                    out.append((e.source_id, e))
        return out

    def spreading_activation(self, seed_ids: list[str], max_depth: int = 3,
                             decay: float = 0.5,
                             min_activation: float = 0.05) -> dict[str, float]:
        activation: dict[str, float] = {}
        frontier = [(nid, 1.0) for nid in seed_ids]
        visited_depth: dict[str, int] = {}
        for depth in range(max_depth + 1):
            nxt = []
            for nid, act in frontier:
                if act < min_activation:
                    continue
                activation[nid] = max(activation.get(nid, 0.0), act)
                if depth < max_depth:
                    for nb_id, edge in self.neighbors(nid, direction="both"):
                        if edge.relation == "contradicts":
                            continue
                        prop = act * decay * edge.weight
                        if prop >= min_activation:
                            prev = visited_depth.get(nb_id, max_depth + 1)
                            if depth + 1 < prev:
                                visited_depth[nb_id] = depth + 1
                                nxt.append((nb_id, prop))
            frontier = nxt
        return activation

    def find_by_relation(self, relation: str) -> list[Edge]:
        return [self._edges[eid]
                for eid in self._by_relation.get(relation, [])]

    def get_subgraph(self, node_ids: set[str]) -> list[Edge]:
        out = []
        for nid in node_ids:
            for eid in self._outgoing.get(nid, []):
                e = self._edges[eid]
                if e.target_id in node_ids:
                    out.append(e)
        return out

    def to_list(self) -> list[dict]:
        return [{"source_id": e.source_id, "target_id": e.target_id,
                 "relation": e.relation, "weight": e.weight,
                 "metadata": e.metadata, "created_at": e.created_at}
                for e in self._edges.values()]


# ---- Regex-based entity/relation extraction ----

_PROPER_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b")
_IS_RE = re.compile(
    r"^(.+?)\s+(?:is|are|was|were)\s+(?:a|an|the)?\s*(.+?)\.?$", re.I)
_HAS_RE = re.compile(r"^(.+?)\s+(?:has|have|had)\s+(.+?)\.?$", re.I)
_WORKS_RE = re.compile(
    r"^(.+?)\s+(?:works?\s+(?:at|for)|is\s+(?:at|with))\s+(.+?)\.?$", re.I)
_ROLE_RE = re.compile(
    r"^(.+?)\s+is\s+(?:the\s+)?(\w+(?:\s+\w+)?)\s+(?:of|for|at)\s+(.+?)\.?$", re.I)
_MANAGES_RE = re.compile(
    r"^(.+?)\s+(?:manages?|leads?|reports?\s+to|oversees?)\s+(.+?)\.?$", re.I)
_USES_RE = re.compile(
    r"^(.+?)\s+(?:uses?|runs?\s+on|built\s+with|powered\s+by)\s+(.+?)\.?$", re.I)
_LOCATED_RE = re.compile(
    r"^(.+?)\s+is\s+(?:located\s+)?(?:in|at)\s+(.+?)\.?$", re.I)


class EntityRelationExtractor:
    """Zero-dependency entity/relation extractor using regex patterns."""

    def __init__(self):
        self._spacy_nlp = None

    def use_spacy(self, nlp=None):
        if nlp is not None:
            self._spacy_nlp = nlp
            return
        try:
            import spacy
            self._spacy_nlp = spacy.load("en_core_web_sm")
        except (ImportError, OSError):
            pass

    def extract(self, content: str) -> list[tuple[str, str, str]]:
        if self._spacy_nlp:
            return self._extract_spacy(content)
        return self._extract_regex(content)

    def extract_entities(self, content: str) -> list[str]:
        if self._spacy_nlp:
            doc = self._spacy_nlp(content)
            return list({ent.text for ent in doc.ents})
        return _PROPER_RE.findall(content)

    def _extract_regex(self, content: str) -> list[tuple[str, str, str]]:
        triples = []
        sentences = re.split(r'[.!?]+', content)
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            m = _ROLE_RE.match(sent)
            if m:
                triples.append((m.group(1).strip(),
                                f"is_{m.group(2).strip().replace(' ', '_')}",
                                m.group(3).strip()))
                continue
            m = _WORKS_RE.match(sent)
            if m:
                triples.append((m.group(1).strip(), "works_at", m.group(2).strip()))
                continue
            m = _MANAGES_RE.match(sent)
            if m:
                triples.append((m.group(1).strip(), "manages", m.group(2).strip()))
                continue
            m = _USES_RE.match(sent)
            if m:
                triples.append((m.group(1).strip(), "uses", m.group(2).strip()))
                continue
            m = _LOCATED_RE.match(sent)
            if m:
                subj, obj = m.group(1).strip(), m.group(2).strip()
                if len(subj) > 2 and len(obj) > 2:
                    triples.append((subj, "located_in", obj))
                continue
            m = _IS_RE.match(sent)
            if m:
                subj, obj = m.group(1).strip(), m.group(2).strip()
                if len(subj) > 2 and len(obj) > 2:
                    triples.append((subj, "is", obj))
                continue
            m = _HAS_RE.match(sent)
            if m:
                subj, obj = m.group(1).strip(), m.group(2).strip()
                if len(subj) > 2 and len(obj) > 2:
                    triples.append((subj, "has", obj))
        return triples

    def _extract_spacy(self, content: str) -> list[tuple[str, str, str]]:
        doc = self._spacy_nlp(content)
        triples = []
        entities = {ent.text: ent.label_ for ent in doc.ents}
        for sent in doc.sents:
            subjects, objects, root_verb = [], [], None
            for token in sent:
                if token.dep_ in ("nsubj", "nsubjpass") and token.head.pos_ == "VERB":
                    subjects.append(token.text if token.text in entities
                                    else " ".join(t.text for t in token.subtree))
                    root_verb = token.head
                if token.dep_ in ("dobj", "attr", "pobj") and root_verb:
                    objects.append(token.text if token.text in entities
                                   else " ".join(t.text for t in token.subtree))
            if subjects and objects and root_verb:
                for s in subjects:
                    for o in objects:
                        triples.append((s.strip(), root_verb.lemma_, o.strip()))
        triples.extend(self._extract_regex(content))
        seen = set()
        unique = []
        for t in triples:
            key = (t[0].lower(), t[1].lower(), t[2].lower())
            if key not in seen:
                seen.add(key)
                unique.append(t)
        return unique


# ---- Fix 1: async auto_link_node with real entity nodes ----

async def auto_link_node(node: MemoryNode, graph: MemoryGraph,
                         storage, extractor: EntityRelationExtractor,
                         entity_index: dict[str, str] | None = None) -> list[Edge]:
    """
    Extract entities/relations from node content and persist graph edges.
    Creates real MemoryNode records for entities that do not yet exist.
    Uses in-memory entity_index for O(1) lookups instead of querying storage.
    """
    from .models import MemoryKind, Provenance

    if entity_index is None:
        entity_index = {}

    triples = extractor.extract(node.content)
    entities = extractor.extract_entities(node.content)
    edges_created = []

    entity_node_ids: dict[str, str] = {}

    for entity in entities:
        entity_key = entity.lower().strip()

        if entity_key in entity_index:
            entity_node_ids[entity_key] = entity_index[entity_key]
        else:
            # Cross-session entity matching via token Jaccard similarity
            matched_existing = None
            entity_tokens = set(entity_key.split())
            for existing_key, existing_id in entity_index.items():
                existing_tokens = set(existing_key.split())
                intersection = entity_tokens & existing_tokens
                union = entity_tokens | existing_tokens
                if union:
                    jaccard = len(intersection) / len(union)
                    if jaccard >= 0.6:
                        matched_existing = (existing_key, existing_id, jaccard)
                        break

            if matched_existing:
                existing_key, existing_id, jaccard_score = matched_existing
                entity_node_ids[entity_key] = existing_id
                entity_index[entity_key] = existing_id  # alias

                # Check if cross-session — create same_entity edge
                existing_node = await storage.load_node(existing_id)
                if (existing_node and
                    existing_node.provenance.session_id != node.provenance.session_id):
                    se = Edge(
                        source_id=existing_id,
                        target_id=existing_id,  # self-link for activation propagation
                        relation="same_entity",
                        weight=jaccard_score,
                        metadata={"matched_keys": [entity_key, existing_key],
                                  "auto_extracted": True},
                    )
                    # Only add the edge if it doesn't already exist
                    edge_id = se.id
                    if edge_id not in {e.id for e in graph.find_by_relation("same_entity")}:
                        graph.add_edge(se)
                        await storage.save_edge(se)
                        edges_created.append(se)
            else:
                entity_node = MemoryNode(
                    content=entity,
                    kind=MemoryKind.ENTITY,
                    importance=0.6,
                    provenance=Provenance(source="auto_graph",
                                          extraction_method="auto_graph",
                                          session_id=node.provenance.session_id),
                    namespace=node.namespace,
                )
                await storage.save_node(entity_node)
                entity_node_ids[entity_key] = entity_node.id
                entity_index[entity_key] = entity_node.id  # update shared index

        e = Edge(
            source_id=node.id,
            target_id=entity_node_ids[entity_key],
            relation="mentions",
            weight=0.8,
            metadata={"entity": entity, "auto_extracted": True},
        )
        graph.add_edge(e)
        await storage.save_edge(e)
        edges_created.append(e)

    for subj, rel, obj in triples:
        subj_key = subj.lower().strip()
        obj_key = obj.lower().strip()
        if subj_key in entity_node_ids and obj_key in entity_node_ids:
            e = Edge(
                source_id=entity_node_ids[subj_key],
                target_id=entity_node_ids[obj_key],
                relation=rel.replace(" ", "_"),
                weight=0.9,
                metadata={"auto_extracted": True, "source_node": node.id},
            )
            graph.add_edge(e)
            await storage.save_edge(e)
            edges_created.append(e)

    return edges_created
