"""
agentmemory V4 — Complete memory operating system for AI agents.

V4: Adaptive retrieval weights, temporal fact validity, multi-modal memory,
confidence calibration, document ingestion, memory profiles, Postgres backend,
memory lineage, consolidation quality scoring.

Quick start:
    from agentmemory import MemoryStore
    mem = MemoryStore()
    mem.add("Alice is the CEO of Acme Corp")
    results = mem.recall("who runs Acme?")

Profiles:
    mem = MemoryStore.from_profile("support_agent", path="agent.db")

Document ingestion:
    mem.ingest_document(long_text, title="Q3 Report")

Confidence calibration:
    mem.feedback(node_id, correct=True)
    report = mem.calibration_report()

Lineage:
    report = mem.lineage(node_id)

REST server:  python -m agentmemory serve --port 8000
MCP server:   python -m agentmemory mcp --db agent.db
"""

from .core import MemoryStore
from .embeddings import (DenseEmbedder, FunctionEmbedder, MultiModalEmbedder,
                         TFIDFEmbedder, cosine_similarity, create_embedder)
from .models import (AuditEvent, AuditOp, ConversationMessage,
                     DeletionReceipt, Edge, EventType, FilterCondition,
                     FilterExpr, FilterOp, HealthReport, LineageReport,
                     MemoryEvent, MemoryKind, MemoryNode, MemoryProfile,
                     MemoryTier, Namespace, Provenance, RetrievalResult)
from .retrieval import RetrievalQuery, RetrieverWeightAdapter
from .query_expansion import QueryExpander
from .reranking import CrossEncoderReranker
from .importance import ImportanceClassifier, ImportanceEvolver
from .classification import KindClassifier
from .federation import FederatedStore
from .validation import WriteValidator, ValidationRule
from .events import EventBus
from .extraction import (ExtractionPipeline, DocumentIngestionPipeline,
                         DocumentChunker, HierarchicalExtractor,
                         create_default_llm_extractor)
from .health import HealthMonitor
from .migration import MigrationImporter, MigrationExporter
from .calibration import CalibrationEngine
from .lineage import LineageEngine
from .temporal import TemporalGrounder

__version__ = "4.0.0"
__all__ = [
    "MemoryStore",
    "MemoryNode", "MemoryKind", "MemoryTier", "Namespace", "Provenance",
    "Edge", "RetrievalResult", "RetrievalQuery", "AuditEvent", "AuditOp",
    "ConversationMessage", "DeletionReceipt", "HealthReport", "MemoryEvent",
    "MemoryProfile", "LineageReport",
    "FilterExpr", "FilterCondition", "FilterOp",
    "EventType", "EventBus",
    "DenseEmbedder", "TFIDFEmbedder", "FunctionEmbedder", "MultiModalEmbedder",
    "cosine_similarity", "create_embedder",
    "ImportanceClassifier", "ImportanceEvolver", "KindClassifier",
    "WriteValidator", "ValidationRule",
    "ExtractionPipeline", "DocumentIngestionPipeline", "DocumentChunker",
    "create_default_llm_extractor",
    "RetrieverWeightAdapter",
    "QueryExpander", "CrossEncoderReranker", "HierarchicalExtractor",
    "FederatedStore", "HealthMonitor",
    "MigrationImporter", "MigrationExporter",
    "CalibrationEngine", "LineageEngine", "TemporalGrounder",
]
