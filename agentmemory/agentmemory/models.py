"""
agentmemory — Core data models.

Defines all dataclasses and enums used throughout the system:
  - MemoryNode: the fundamental unit of storage
  - MemoryKind / MemoryTier: classification taxonomy
  - Namespace / Provenance: scoping and source tracking
  - RetrievalResult: recall output wrapper
  - FilterExpr / FilterCondition: structured query predicates
  - MemoryEvent / EventType: event bus payloads
  - HealthReport / DeletionReceipt / LineageReport: output types
  - ConversationMessage: input type for ingest_conversation()
  - MemoryProfile: named configuration presets
"""

from __future__ import annotations

import hashlib
import math
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union


class MemoryTier(Enum):
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class MemoryKind(Enum):
    INSTRUCTION = "instruction"
    OBSERVATION = "observation"
    SCRATCH = "scratch"
    EVENT = "event"
    DIALOGUE = "dialogue"
    ACTION = "action"
    OUTCOME = "outcome"
    FACT = "fact"
    ENTITY = "entity"
    PREFERENCE = "preference"
    PROCEDURE = "procedure"
    BELIEF = "belief"

    @property
    def tier(self) -> MemoryTier:
        return _KIND_TIER_MAP[self.value]


_KIND_TIER_MAP = {
    "instruction": MemoryTier.WORKING,
    "observation": MemoryTier.WORKING,
    "scratch": MemoryTier.WORKING,
    "event": MemoryTier.EPISODIC,
    "dialogue": MemoryTier.EPISODIC,
    "action": MemoryTier.EPISODIC,
    "outcome": MemoryTier.EPISODIC,
    "fact": MemoryTier.SEMANTIC,
    "entity": MemoryTier.SEMANTIC,
    "preference": MemoryTier.SEMANTIC,
    "procedure": MemoryTier.SEMANTIC,
    "belief": MemoryTier.SEMANTIC,
}


@dataclass
class Namespace:
    """Hierarchical memory scope: org / team / agent / session."""
    org: str = ""
    team: str = ""
    agent: str = ""
    session: str = ""

    @property
    def path(self) -> str:
        parts = [p for p in [self.org, self.team, self.agent, self.session] if p]
        return "/".join(parts) if parts else ""

    def contains(self, other: Namespace) -> bool:
        if self.org and self.org != other.org:
            return False
        if self.team and self.team != other.team:
            return False
        if self.agent and self.agent != other.agent:
            return False
        if self.session and self.session != other.session:
            return False
        return True

    def to_dict(self) -> dict:
        return {"org": self.org, "team": self.team,
                "agent": self.agent, "session": self.session}

    @classmethod
    def from_dict(cls, d: dict) -> Namespace:
        return cls(org=d.get("org", ""), team=d.get("team", ""),
                   agent=d.get("agent", ""), session=d.get("session", ""))


@dataclass
class Provenance:
    """Rich provenance tracking for auditability."""
    source: str = ""
    session_id: str = ""
    conversation_turn: Optional[int] = None
    agent_id: str = ""
    tool_call_id: str = ""
    document_id: str = ""
    parent_message_role: str = ""
    extraction_method: str = ""

    def to_dict(self) -> dict:
        return {k: v for k, v in {
            "source": self.source, "session_id": self.session_id,
            "conversation_turn": self.conversation_turn,
            "agent_id": self.agent_id, "tool_call_id": self.tool_call_id,
            "document_id": self.document_id,
            "parent_message_role": self.parent_message_role,
            "extraction_method": self.extraction_method,
        }.items() if v}

    @classmethod
    def from_dict(cls, d: dict) -> Provenance:
        return cls(**{k: d[k] for k in cls.__dataclass_fields__ if k in d})


@dataclass
class MemoryNode:
    """Single unit of memory with bi-temporal modeling and validity windows."""
    content: str
    kind: MemoryKind
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    # Bi-temporal: ingestion time vs event time
    created_at: float = field(default_factory=time.time)
    event_time: Optional[float] = None
    accessed_at: float = field(default_factory=time.time)
    access_count: int = 0
    importance: float = 0.5
    confidence: float = 1.0
    decay_rate: float = 0.0
    embedding: Optional[list[float]] = field(default=None, repr=False)
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: Provenance = field(default_factory=Provenance)
    namespace: Namespace = field(default_factory=Namespace)
    parent_id: Optional[str] = None
    superseded_by: Optional[str] = None
    tags: set[str] = field(default_factory=set)
    version: int = 1
    # V4: Temporal validity windows (Upgrade 5)
    valid_from: Optional[float] = None
    valid_until: Optional[float] = None
    # V4: Multi-modal (Upgrade 6)
    media_type: str = "text"  # text, image, audio
    raw_data_ref: str = ""    # path or URL to raw media
    # V4: Calibration feedback counters (Upgrade 4)
    feedback_correct: int = 0
    feedback_incorrect: int = 0

    # Compat properties for provenance fields
    @property
    def source(self) -> str:
        return self.provenance.source

    @source.setter
    def source(self, val: str):
        self.provenance.source = val

    @property
    def session_id(self) -> str:
        return self.provenance.session_id

    @session_id.setter
    def session_id(self, val: str):
        self.provenance.session_id = val

    @property
    def tier(self) -> MemoryTier:
        return self.kind.tier

    @property
    def effective_time(self) -> float:
        return self.event_time if self.event_time is not None else self.created_at

    @property
    def is_valid(self) -> bool:
        """Check if memory is within its validity window."""
        now = time.time()
        if self.valid_until is not None and now > self.valid_until:
            return False
        if self.valid_from is not None and now < self.valid_from:
            return False
        return True

    @property
    def calibrated_confidence(self) -> float:
        """Bayesian-calibrated confidence from feedback."""
        total = self.feedback_correct + self.feedback_incorrect
        if total == 0:
            return self.confidence
        observed = self.feedback_correct / total
        # Weighted blend: prior confidence + observed accuracy
        weight = min(1.0, total / 10.0)
        return self.confidence * (1 - weight) + observed * weight

    @property
    def age_hours(self) -> float:
        return (time.time() - self.created_at) / 3600

    @property
    def recency_hours(self) -> float:
        return (time.time() - self.accessed_at) / 3600

    @property
    def activation(self) -> float:
        base = self.importance
        recency = 1.0 / (1.0 + self.recency_hours)
        frequency = math.log1p(self.access_count) * 0.1
        decay_penalty = self.decay_rate * self.age_hours
        return max(0.0, base + recency * 0.3 + frequency - decay_penalty)

    def touch(self):
        self.accessed_at = time.time()
        self.access_count += 1

    def content_hash(self) -> str:
        return hashlib.sha256(self.content.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "id": self.id, "content": self.content,
            "kind": self.kind.value, "tier": self.tier.value,
            "created_at": self.created_at, "event_time": self.event_time,
            "accessed_at": self.accessed_at,
            "access_count": self.access_count, "importance": self.importance,
            "confidence": self.confidence, "decay_rate": self.decay_rate,
            "metadata": self.metadata,
            "provenance": self.provenance.to_dict(),
            "namespace": self.namespace.to_dict(),
            "parent_id": self.parent_id, "superseded_by": self.superseded_by,
            "tags": list(self.tags), "version": self.version,
            "valid_from": self.valid_from, "valid_until": self.valid_until,
            "media_type": self.media_type, "raw_data_ref": self.raw_data_ref,
            "feedback_correct": self.feedback_correct,
            "feedback_incorrect": self.feedback_incorrect,
        }

    @classmethod
    def from_dict(cls, d: dict) -> MemoryNode:
        prov = Provenance.from_dict(d.get("provenance", {}))
        if not prov.source and "source" in d:
            prov.source = d["source"]
        if not prov.session_id and "session_id" in d:
            prov.session_id = d["session_id"]
        ns = Namespace.from_dict(d.get("namespace", {}))
        return cls(
            id=d["id"], content=d["content"],
            kind=MemoryKind(d["kind"]),
            created_at=d.get("created_at", time.time()),
            event_time=d.get("event_time"),
            accessed_at=d.get("accessed_at", time.time()),
            access_count=d.get("access_count", 0),
            importance=d.get("importance", 0.5),
            confidence=d.get("confidence", 1.0),
            decay_rate=d.get("decay_rate", 0.0),
            metadata=d.get("metadata", {}),
            provenance=prov, namespace=ns,
            parent_id=d.get("parent_id"),
            superseded_by=d.get("superseded_by"),
            tags=set(d.get("tags", [])),
            version=d.get("version", 1),
            valid_from=d.get("valid_from"),
            valid_until=d.get("valid_until"),
            media_type=d.get("media_type", "text"),
            raw_data_ref=d.get("raw_data_ref", ""),
            feedback_correct=d.get("feedback_correct", 0),
            feedback_incorrect=d.get("feedback_incorrect", 0),
        )


@dataclass
class Edge:
    """Directed relationship between memory nodes."""
    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    @property
    def id(self) -> str:
        return f"{self.source_id}-{self.relation}-{self.target_id}"


class AuditOp(Enum):
    CREATE = "create"
    UPDATE = "update"
    SUPERSEDE = "supersede"
    DELETE = "delete"
    CONSOLIDATE = "consolidate"
    CONFIDENCE_DECAY = "confidence_decay"
    PROMOTE = "promote"
    ROLLBACK = "rollback"
    GDPR_DELETE = "gdpr_delete"
    CONTRADICTION_RESOLVED = "contradiction_resolved"
    VALIDATION_REJECT = "validation_reject"
    LOW_QUALITY_CONSOLIDATION = "low_quality_consolidation"
    FEEDBACK = "feedback"
    FACT_INVALIDATED = "fact_invalidated"


@dataclass
class AuditEvent:
    """Immutable record of a memory mutation."""
    node_id: str
    op: AuditOp
    timestamp: float = field(default_factory=time.time)
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"node_id": self.node_id, "op": self.op.value,
                "timestamp": self.timestamp, "detail": self.detail}


@dataclass
class RetrievalResult:
    """A scored memory node returned from a query."""
    node: MemoryNode
    score: float
    score_components: dict[str, float] = field(default_factory=dict)
    explanation: str = ""

    def __repr__(self):
        return (f"RetrievalResult(id={self.node.id}, "
                f"score={self.score:.3f}, kind={self.node.kind.value})")


# ---- Compound Filter Expressions ----

class FilterOp(Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GE = "ge"
    LT = "lt"
    LE = "le"
    IN = "in"
    CONTAINS = "contains"
    STARTSWITH = "startswith"


@dataclass
class FilterCondition:
    """Single filter condition on a node field."""
    field: str
    op: FilterOp
    value: Any

    def evaluate(self, node: MemoryNode) -> bool:
        val = self._get_field(node)
        if val is None:
            return False
        if self.op == FilterOp.EQ:
            return val == self.value
        elif self.op == FilterOp.NE:
            return val != self.value
        elif self.op == FilterOp.GT:
            return val > self.value
        elif self.op == FilterOp.GE:
            return val >= self.value
        elif self.op == FilterOp.LT:
            return val < self.value
        elif self.op == FilterOp.LE:
            return val <= self.value
        elif self.op == FilterOp.IN:
            return val in self.value
        elif self.op == FilterOp.CONTAINS:
            if isinstance(val, set):
                return self.value in val
            return self.value in str(val)
        elif self.op == FilterOp.STARTSWITH:
            return str(val).startswith(str(self.value))
        return False

    def _get_field(self, node: MemoryNode) -> Any:
        if self.field == "kind":
            return node.kind.value
        elif self.field == "tier":
            return node.tier.value
        elif self.field == "source":
            return node.provenance.source
        elif self.field == "session_id":
            return node.provenance.session_id
        elif self.field == "agent_id":
            return node.provenance.agent_id
        elif self.field.startswith("namespace."):
            return getattr(node.namespace, self.field.split(".", 1)[1], None)
        elif self.field.startswith("metadata."):
            return node.metadata.get(self.field.split(".", 1)[1])
        elif hasattr(node, self.field):
            return getattr(node, self.field)
        return None


@dataclass
class FilterExpr:
    """Compound boolean filter expression supporting AND/OR/NOT."""
    op: str  # "and", "or", "not"
    children: list[Union[FilterExpr, FilterCondition]] = field(default_factory=list)

    def evaluate(self, node: MemoryNode) -> bool:
        if self.op == "and":
            return all(c.evaluate(node) for c in self.children)
        elif self.op == "or":
            return any(c.evaluate(node) for c in self.children)
        elif self.op == "not":
            return not self.children[0].evaluate(node) if self.children else True
        return True

    @classmethod
    def AND(cls, *conditions) -> FilterExpr:
        return cls(op="and", children=list(conditions))

    @classmethod
    def OR(cls, *conditions) -> FilterExpr:
        return cls(op="or", children=list(conditions))

    @classmethod
    def NOT(cls, condition) -> FilterExpr:
        return cls(op="not", children=[condition])


# ---- Event types ----

class EventType(Enum):
    MEMORY_CREATED = "memory_created"
    MEMORY_UPDATED = "memory_updated"
    MEMORY_DELETED = "memory_deleted"
    CONTRADICTION_DETECTED = "contradiction_detected"
    CONTRADICTION_RESOLVED = "contradiction_resolved"
    HIGH_IMPORTANCE_WRITE = "high_importance_write"
    CONSOLIDATION_COMPLETE = "consolidation_complete"
    CONFIDENCE_BELOW_THRESHOLD = "confidence_below_threshold"
    PROACTIVE_SURFACE = "proactive_surface"
    VALIDATION_REJECTED = "validation_rejected"
    FACT_INVALIDATED = "fact_invalidated"
    FEEDBACK_RECEIVED = "feedback_received"


@dataclass
class MemoryEvent:
    """Event emitted by the memory system."""
    event_type: EventType
    node_id: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class ConversationMessage:
    """Single message in a conversation for ingestion."""
    role: str
    content: str
    timestamp: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthReport:
    """Memory store health assessment."""
    total_memories: int = 0
    active_memories: int = 0
    contradiction_rate: float = 0.0
    confidence_distribution: dict[str, int] = field(default_factory=dict)
    importance_distribution: dict[str, int] = field(default_factory=dict)
    stale_memory_fraction: float = 0.0
    retrieval_quality_trend: list[float] = field(default_factory=list)
    importance_entropy: float = 0.0
    namespace_count: int = 0
    by_tier: dict[str, int] = field(default_factory=dict)
    by_kind: dict[str, int] = field(default_factory=dict)
    edges: int = 0
    ann_index_size: int = 0
    low_quality_consolidations: int = 0
    expired_memories: int = 0
    calibration_gap: float = 0.0

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class DeletionReceipt:
    """GDPR-compliant deletion receipt."""
    target_type: str
    target_id: str
    memories_deleted: int = 0
    edges_deleted: int = 0
    audit_entries_redacted: int = 0
    ann_entries_removed: int = 0
    fts_entries_removed: int = 0
    timestamp: float = field(default_factory=time.time)
    verified: bool = False

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class LineageEntry:
    """Single step in a memory's lineage chain."""
    event: AuditEvent
    related_node_id: str = ""
    description: str = ""


@dataclass
class LineageReport:
    """Complete causal chain for a memory (Upgrade 11)."""
    node_id: str
    current_content: str = ""
    current_kind: str = ""
    current_confidence: float = 0.0
    current_importance: float = 0.0
    created_from: str = ""
    creation_method: str = ""
    history: list[LineageEntry] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    consolidated_from: list[str] = field(default_factory=list)
    referenced_by: list[str] = field(default_factory=list)
    superseded_by: str = ""
    feedback_summary: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "current_content": self.current_content,
            "current_kind": self.current_kind,
            "current_confidence": self.current_confidence,
            "current_importance": self.current_importance,
            "created_from": self.created_from,
            "creation_method": self.creation_method,
            "history": [{"op": e.event.op.value, "timestamp": e.event.timestamp,
                         "detail": e.event.detail, "related": e.related_node_id,
                         "description": e.description} for e in self.history],
            "contradictions": self.contradictions,
            "consolidated_from": self.consolidated_from,
            "referenced_by": self.referenced_by,
            "superseded_by": self.superseded_by,
            "feedback_summary": self.feedback_summary,
        }


@dataclass
class MemoryProfile:
    """Named configuration for agent memory behavior (Upgrade 7)."""
    name: str
    description: str = ""
    retrieval_weights: dict[str, float] = field(default_factory=dict)
    context_token_budget: int = 4000
    consolidation_threshold: int = 100
    importance_floor: float = 0.1
    auto_graph: bool = True
    auto_classify: bool = True
    streaming_consolidation: bool = True
    proactive_surfacing: bool = True
    prefer_dense: bool = True

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, d: dict) -> MemoryProfile:
        return cls(**{k: d[k] for k in cls.__dataclass_fields__ if k in d})

    @classmethod
    def from_preset(cls, name: str) -> MemoryProfile:
        presets = {
            "summarizer": cls(
                name="summarizer",
                description="Optimized for summarization agents with high context budgets",
                retrieval_weights={"semantic": 0.35, "lexical": 0.10, "activation": 0.15,
                                   "graph": 0.10, "importance": 0.20, "temporal": 0.10},
                context_token_budget=8000,
                consolidation_threshold=50,
                proactive_surfacing=False,
            ),
            "coding_assistant": cls(
                name="coding_assistant",
                description="Optimized for code-aware agents with procedural memory emphasis",
                retrieval_weights={"semantic": 0.25, "lexical": 0.20, "activation": 0.15,
                                   "graph": 0.15, "importance": 0.15, "temporal": 0.10},
                context_token_budget=6000,
                consolidation_threshold=200,
                auto_graph=True,
            ),
            "support_agent": cls(
                name="support_agent",
                description="Optimized for customer support with entity/preference focus",
                retrieval_weights={"semantic": 0.30, "lexical": 0.15, "activation": 0.20,
                                   "graph": 0.20, "importance": 0.10, "temporal": 0.05},
                context_token_budget=3000,
                consolidation_threshold=75,
                proactive_surfacing=True,
            ),
            "research_agent": cls(
                name="research_agent",
                description="Optimized for research with broad recall and high fidelity",
                retrieval_weights={"semantic": 0.35, "lexical": 0.15, "activation": 0.10,
                                   "graph": 0.20, "importance": 0.10, "temporal": 0.10},
                context_token_budget=12000,
                consolidation_threshold=150,
                auto_graph=True,
            ),
            "default": cls(
                name="default",
                description="Balanced defaults",
                retrieval_weights={"semantic": 0.30, "lexical": 0.12, "activation": 0.18,
                                   "graph": 0.18, "importance": 0.10, "temporal": 0.12},
            ),
        }
        if name not in presets:
            raise ValueError(f"Unknown preset: {name}. Available: {list(presets.keys())}")
        return presets[name]
