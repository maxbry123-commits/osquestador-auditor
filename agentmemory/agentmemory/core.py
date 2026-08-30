"""
agentmemory V4 — MemoryStore.

All V3 fixes applied:
  Fix 1: async auto_link_node with edge persistence
  Fix 2: _ensure_init race condition via asyncio.Lock
  Fix 3: Validation uses pre-loaded nearby_nodes
  Fix 4: Importance evolver passed to consolidation engine
  Fix 5: Contradiction edges conditional (in consolidation.py)

V4 upgrades integrated:
  Upgrade 2: Adaptive retrieval weight learning
  Upgrade 3: Document ingestion via ingest_document()
  Upgrade 4: Confidence calibration via feedback()
  Upgrade 5: Temporal validity windows (valid_from/valid_until)
  Upgrade 6: Multi-modal memory support
  Upgrade 7: Memory profiles via from_profile()
  Upgrade 11: Memory lineage via lineage()
"""

from __future__ import annotations

import asyncio
import functools
from typing import Any, Callable, Optional, Union

from .ann_index import ExactKNNIndex, HNSWIndex
from .calibration import CalibrationEngine
from .classification import KindClassifier
from .consolidation import ConsolidationEngine, ConsolidationScheduler
from .embeddings import (Embedder, cosine_similarity, create_embedder)
from .events import EventBus, ProactiveSurfacer
from .extraction import DocumentIngestionPipeline, ExtractionPipeline
from .gdpr import GDPRPipeline
from .graph import EntityRelationExtractor, MemoryGraph, auto_link_node
from .health import HealthMonitor
from .importance import ImportanceClassifier, ImportanceEvolver
from .lineage import LineageEngine
from .models import (AuditEvent, AuditOp, ConversationMessage,
                     DeletionReceipt, Edge, EventType, FilterExpr,
                     HealthReport, LineageReport, MemoryEvent, MemoryKind,
                     MemoryNode, MemoryProfile, MemoryTier, Namespace,
                     Provenance, RetrievalResult)
from .retrieval import RetrievalEngine, RetrievalQuery, RetrieverWeightAdapter
from .storage.sqlite_backend import SQLiteBackend
from .validation import WriteValidator


def _sync(coro_fn):
    # Wraps an async coroutine method to be callable synchronously.
    # Two cases must be handled:
    #   (a) No running event loop (typical script/CLI context): use asyncio.run().
    #   (b) Running event loop exists (Jupyter, nested async, frameworks like FastAPI
    #       calling sync methods from async context): asyncio.run() raises RuntimeError
    #       because it cannot create a new loop inside an existing one. Solution:
    #       submit the coroutine to a ThreadPoolExecutor thread that creates its
    #       own fresh event loop via asyncio.run(). This avoids loop-nesting while
    #       still blocking the caller until the result is ready.
    @functools.wraps(coro_fn)
    def wrapper(self, *args, **kwargs):
        coro = coro_fn(self, *args, **kwargs)
        try:
            loop = asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, coro).result()
        except RuntimeError:
            return asyncio.run(coro)
    wrapper._is_sync_wrapper = True
    return wrapper


class MemoryStore:
    """
    V4 Memory Store — complete memory operating system.

    Async-first with sync wrappers. Ingests raw conversation and documents,
    builds knowledge graphs, validates writes, resolves contradictions with
    temporal invalidation, monitors health, calibrates confidence from feedback,
    learns optimal retrieval weights, supports multi-modal memory, and provides
    full memory lineage for audit.
    """

    def __init__(
        self,
        path: str = ":memory:",
        *,
        storage_backend=None,
        embedder: Optional[Embedder] = None,
        prefer_dense: bool = True,
        multimodal: bool = False,
        summarizer: Optional[Callable[[list[str]], str]] = None,
        contradiction_detector: Optional[Callable[[str, str], bool]] = None,
        contradiction_resolver=None,
        extractor_fn=None,
        quality_evaluator_fn: Optional[Callable] = None,
        auto_importance: bool = True,
        auto_classify: bool = True,
        auto_graph: bool = True,
        streaming_consolidation: bool = True,
        write_validation: bool = True,
        importance_evolution: bool = True,
        proactive_surfacing: bool = True,
        ann_M: int = 16,
        ann_ef_construction: int = 200,
        ann_ef_search: int = 100,
        consolidation_threshold: int = 100,
        auto_consolidate: bool = False,
        query_cache_size: int = 128,
        weight_checkpoint_path: Optional[str] = None,
        profile: Optional[MemoryProfile] = None,
        query_expansion: bool = True,
        reranker: bool = False,
        auto_calibrate_abstention: bool = False,
        use_exact_knn: bool = False,
    ):
        """
        Create a new MemoryStore.

        All parameters are keyword-only (except path). The store is lazily
        initialized on first use — the first async_add/recall/etc. call triggers
        _ensure_init() which loads the ANN index and graph from storage.

        Args:
            path: SQLite database path. Use ":memory:" for an ephemeral in-process
                store (default). Pass a file path for persistence across restarts.
            storage_backend: Custom StorageBackend implementation. If provided,
                ``path`` is ignored. Use this to plug in PostgresBackend or a
                custom implementation.
            embedder: Custom Embedder instance. If None, auto-selected based on
                ``prefer_dense`` and ``multimodal`` flags.
            prefer_dense: If True (default), use sentence-transformers dense
                embeddings when the package is installed. Falls back to TF-IDF
                automatically if sentence-transformers is not available.
            multimodal: If True, use MultiModalEmbedder supporting image (CLIP)
                and audio (Whisper) in addition to text. Requires optional deps.
            summarizer: Callable[[list[str]], str] invoked during episodic→semantic
                consolidation to produce semantic summaries. If None, uses the
                highest-importance memory as the summary.
            contradiction_detector: Callable[[str, str], bool] returning True if
                two content strings contradict each other. If None, uses a built-in
                structural heuristic.
            contradiction_resolver: Callable[[str, str], str] returning "a", "b",
                or "neither" to resolve a contradiction. Accepts both sync and
                async callables. If None, uses heuristic recency+confidence.
            extractor_fn: Custom extraction function for conversation ingestion.
                If None, uses the built-in rule-based/hierarchical extractor.
            quality_evaluator_fn: Callable[[str, str], float] scoring retrieval
                quality (0.0–1.0) for adaptive weight learning. Used with
                ``weight_checkpoint_path``.
            auto_importance: If True (default), automatically score importance
                using ImportanceClassifier's feature-engineered logistic model.
            auto_classify: If True (default), automatically classify memory kind
                using KindClassifier's signal-word scoring.
            auto_graph: If True (default), automatically extract entities and
                build the knowledge graph on each write.
            streaming_consolidation: If True (default), run on_write consolidation
                checks (near-duplicate detection, contradiction detection) after
                each write. Disable for bulk imports.
            write_validation: If True (default), run WriteValidator checks before
                each write (schema, duplicate, source authorization).
            importance_evolution: If True (default), update importance on access
                (Bayesian) and decay unaccessed nodes during consolidation.
            proactive_surfacing: If True (default), emit PROACTIVE_SURFACE events
                when new writes are related to hot (frequently accessed) memories.
            ann_M: HNSW graph connectivity parameter. Higher = better recall at
                higher memory cost. Default 16.
            ann_ef_construction: HNSW construction search width. Higher = better
                index quality at higher build cost. Default 200.
            ann_ef_search: HNSW search width. Higher = better recall at higher
                query cost. Default 100.
            consolidation_threshold: Number of active episodic memories that
                triggers automatic consolidation when ``auto_consolidate=True``.
                Default 100.
            auto_consolidate: If True, run a background ConsolidationScheduler
                that consolidates automatically when the threshold is reached.
                Default False (manual consolidation via async_consolidate()).
            query_cache_size: LRU cache size for retrieval results. Set to 0 to
                disable caching. Default 128.
            weight_checkpoint_path: File path for persisting adaptive retrieval
                weights learned by RetrieverWeightAdapter. If None, adaptive
                weight learning is disabled.
            profile: MemoryProfile preset. If provided, overrides prefer_dense,
                auto_graph, auto_classify, streaming_consolidation,
                proactive_surfacing, and consolidation_threshold with
                preset-specific values.
            query_expansion: If True and prefer_dense is True, use QueryExpander
                to generate synonym/reformulation variants of recall queries for
                improved lexical coverage. Default True.
            reranker: If True, load CrossEncoderReranker (cross-encoder/ms-marco-
                MiniLM-L-6-v2) and apply it to the top candidates after initial
                retrieval. Improves ranking quality at the cost of latency.
                Default False.
            auto_calibrate_abstention: If True, compute an abstention threshold
                at initialization time (10th percentile of existing memory scores)
                and use it to filter low-confidence build_context results.
                Default False.
        """
        # Apply profile overrides
        if profile:
            prefer_dense = profile.prefer_dense
            auto_graph = profile.auto_graph
            auto_classify = profile.auto_classify
            streaming_consolidation = profile.streaming_consolidation
            proactive_surfacing = profile.proactive_surfacing
            consolidation_threshold = profile.consolidation_threshold

        self._storage = storage_backend or SQLiteBackend(path)
        self._graph = MemoryGraph()
        self._embedder = embedder or create_embedder(
            prefer_dense=prefer_dense, multimodal=multimodal)
        if use_exact_knn:
            self._ann = ExactKNNIndex()
        else:
            self._ann = HNSWIndex(M=ann_M, ef_construction=ann_ef_construction,
                                  ef_search=ann_ef_search)
        self._entity_index: dict[str, str] = {}  # entity_key → node_id
        self._imp_clf = ImportanceClassifier() if auto_importance else None
        self._evolver = ImportanceEvolver() if importance_evolution else None
        self._classifier = KindClassifier() if auto_classify else None
        self._extractor = EntityRelationExtractor() if auto_graph else None
        self._event_bus = EventBus()
        self._surfacer = ProactiveSurfacer() if proactive_surfacing else None
        self._streaming = streaming_consolidation

        # Fix 4: Pass evolver to consolidation engine
        self._consolidation = ConsolidationEngine(
            self._storage, self._graph, self._embedder, self._ann,
            summarizer, contradiction_detector, contradiction_resolver,
            self._event_bus, self._evolver)

        # Upgrade 2: Adaptive weight learning
        self._weight_adapter = (RetrieverWeightAdapter(checkpoint_path=weight_checkpoint_path)
                                if weight_checkpoint_path else None)

        # Query expansion (Upgrade 1, Prompt 2)
        self._query_expander = None
        if query_expansion and prefer_dense:
            from .query_expansion import QueryExpander
            self._query_expander = QueryExpander()

        # Cross-encoder reranker (Upgrade 5, Prompt 2)
        self._reranker_instance = None
        if reranker:
            from .reranking import CrossEncoderReranker
            self._reranker_instance = CrossEncoderReranker()

        self._retrieval = RetrievalEngine(
            self._storage, self._graph, self._embedder, self._ann,
            self._evolver, cache_size=query_cache_size,
            weight_adapter=self._weight_adapter,
            quality_evaluator_fn=quality_evaluator_fn,
            entity_index=self._entity_index,
            query_expander=self._query_expander,
            reranker=self._reranker_instance)

        # Apply profile retrieval weights
        self._profile = profile
        self._profile_weights = profile.retrieval_weights if profile else None

        self._validator = WriteValidator() if write_validation else None
        self._extraction = ExtractionPipeline(extractor_fn=extractor_fn,
                                               auto_classify=auto_classify,
                                               hierarchical_extraction=True)
        self._doc_pipeline = DocumentIngestionPipeline(classifier=self._classifier)
        self._health = HealthMonitor(self._storage, self._graph, self._ann)
        self._gdpr = GDPRPipeline(self._storage, self._graph, self._ann)
        self._calibration = CalibrationEngine(self._storage, self._event_bus)
        self._lineage = LineageEngine(self._storage, self._graph)

        self._scheduler: Optional[ConsolidationScheduler] = None
        self._auto_consolidate = auto_consolidate
        self._consolidation_threshold = consolidation_threshold
        self._auto_calibrate_abstention = auto_calibrate_abstention
        self._abstention_threshold: float = 0.0
        self._namespace = Namespace()
        self._source = ""
        self._init_done = False
        # Fix 2: asyncio.Lock for init
        self._init_lock = asyncio.Lock()

    @classmethod
    def from_profile(cls, profile_name: str, path: str = ":memory:", **kwargs) -> MemoryStore:
        """Create a MemoryStore from a named profile preset."""
        profile = MemoryProfile.from_preset(profile_name)
        return cls(path, profile=profile, **kwargs)

    # Fix 2: Double-checked locking
    async def _ensure_init(self):
        if self._init_done:
            return
        async with self._init_lock:
            if self._init_done:
                return
            await self._reload()
            self._init_done = True
            if self._auto_calibrate_abstention:
                self._abstention_threshold = await self._health.calibrate_abstention_threshold()
            if self._auto_consolidate:
                self._scheduler = ConsolidationScheduler(
                    self._consolidation, self._storage, self._consolidation_threshold)
                await self._scheduler.start()

    async def _reload(self):
        for e in await self._storage.load_edges():
            self._graph.add_edge(e)
        for n in await self._storage.get_active_nodes():
            if n.embedding:
                self._ann.add(n.id, n.embedding)
            if n.kind.value == "entity":
                self._entity_index[n.content.lower().strip()] = n.id
        if self._surfacer:
            nodes = await self._storage.get_active_nodes()
            self._surfacer.update_hot_set(nodes)

    def set_namespace(self, org="", team="", agent="", session=""):
        self._namespace = Namespace(org=org, team=team, agent=agent, session=session)
        return self

    def set_session(self, session_id: str):
        self._namespace.session = session_id
        return self

    def set_source(self, source: str):
        self._source = source
        return self

    def on(self, event_type, handler):
        return self._event_bus.on(event_type, handler)

    def watch(self, event_types, handler):
        return self._event_bus.watch(event_types, handler)

    # ---- Core add (Fixes 1,3 applied) ----

    async def async_add(
        self, content: str, kind: Optional[str] = None,
        importance: Optional[float] = None, confidence: float = 1.0,
        decay_rate: float = 0.0, tags: Optional[set[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        parent_id: Optional[str] = None, embed: bool = True,
        source: Optional[str] = None, namespace: Optional[Namespace] = None,
        event_time: Optional[float] = None, provenance: Optional[Provenance] = None,
        valid_from: Optional[float] = None, valid_until: Optional[float] = None,
        media_type: str = "text", raw_data_ref: str = "",
    ) -> MemoryNode:
        """
        Store a new memory in the system.

        Automatically classifies the memory kind if not specified, scores importance
        from content signals, embeds the content, validates the write against
        constitutional rules (near-duplicate, schema, source authorization), persists
        to storage, updates the ANN index and knowledge graph, triggers streaming
        consolidation checks, and emits MEMORY_CREATED and optionally
        HIGH_IMPORTANCE_WRITE events.

        Args:
            content: The memory content to store. Should be a clear, standalone
                statement. Minimum 3 characters.
            kind: Memory kind string. One of: fact, entity, preference, procedure,
                event, dialogue, action, outcome, belief, instruction, observation,
                scratch. Auto-classified from content signals if None.
            importance: Importance score 0.0–1.0. Auto-scored by ImportanceClassifier
                from content signals if None.
            confidence: Initial confidence score 0.0–1.0. Default 1.0.
            decay_rate: Rate at which this memory loses activation over time.
                0.0 means no decay. Default 0.0.
            tags: Optional set of string tags for filtering.
            metadata: Optional dict of arbitrary metadata attached to the node.
            parent_id: ID of a parent MemoryNode to establish a parent-child edge.
            embed: If False, skip embedding computation. The node will not appear
                in ANN-based recall. Default True.
            source: Source identifier string for provenance tracking.
            namespace: Optional Namespace for hierarchical scoping (org/team/agent/session).
            event_time: Unix timestamp of when the described event occurred in the
                real world, distinct from ingestion time (created_at).
            provenance: Full Provenance object. Overrides source/session if provided.
            valid_from: Unix timestamp from which this memory is valid.
            valid_until: Unix timestamp after which this memory is treated as expired
                and excluded from recall (unless include_expired=True).
            media_type: One of 'text', 'image', 'audio'. Default 'text'.
            raw_data_ref: Reference to raw media data for non-text memories.

        Returns:
            MemoryNode: The created memory node with assigned ID, computed importance
                score, embedding, and provenance.

        Raises:
            ValueError: If write validation fails. Reasons include: near-duplicate
                detected (cosine similarity > 0.92 with existing node of same kind),
                content too short, importance below floor, or source not authorized.

        Example:
            node = await mem.async_add(
                "Alice is the CEO of TechCorp",
                kind="entity",
                importance=0.9,
                tags={"people", "leadership"}
            )
        """
        await self._ensure_init()

        if kind is None and self._classifier:
            mk = self._classifier.classify(content)
        elif kind is None:
            mk = MemoryKind.OBSERVATION
        else:
            mk = MemoryKind(kind)

        if importance is None:
            importance = self._imp_clf.predict(content, mk) if self._imp_clf else 0.5

        prov = provenance or Provenance()
        if source is not None:
            prov.source = source
        elif not prov.source:
            prov.source = self._source
        if not prov.session_id:
            prov.session_id = self._namespace.session

        ns = namespace or Namespace(
            org=self._namespace.org, team=self._namespace.team,
            agent=self._namespace.agent, session=self._namespace.session)

        node = MemoryNode(
            content=content, kind=mk, importance=importance,
            confidence=confidence, decay_rate=decay_rate,
            tags=tags or set(), metadata=metadata or {},
            provenance=prov, namespace=ns, parent_id=parent_id,
            event_time=event_time, valid_from=valid_from, valid_until=valid_until,
            media_type=media_type, raw_data_ref=raw_data_ref)

        if embed:
            node.embedding = self._embedder.embed(content)

        # Fix 3: Pre-load nearby nodes for validation
        if self._validator:
            nearby_nodes = {}
            if node.embedding and self._ann.size > 0:
                hits = self._ann.query_radius(node.embedding, radius=0.25, max_results=10)
                for nid, _ in hits:
                    if nid != node.id:
                        n = await self._storage.load_node(nid)
                        if n:
                            nearby_nodes[nid] = n
            ctx = {"ann": self._ann, "storage": self._storage,
                   "nearby_nodes": nearby_nodes,
                   "contradiction_detector": self._consolidation._is_contra}
            result = self._validator.validate(node, ctx)
            if not result.valid:
                await self._storage.log_audit(AuditEvent(
                    node_id=node.id, op=AuditOp.VALIDATION_REJECT,
                    detail={"reasons": result.reasons}))
                raise ValueError(f"Write validation failed: {'; '.join(result.reasons)}")

        await self._storage.save_node(node)
        await self._storage.log_audit(AuditEvent(
            node_id=node.id, op=AuditOp.CREATE,
            detail={"kind": mk.value, "importance": importance}))

        if node.embedding:
            self._ann.add(node.id, node.embedding)

        # Fix 1: async auto_link_node
        if self._extractor and node.embedding:
            await auto_link_node(node, self._graph, self._storage,
                                 self._extractor, self._entity_index)

        if self._streaming and node.embedding:
            await self._consolidation.on_write(node)

        if self._surfacer and node.embedding:
            self._surfacer.add_to_hot_set(node)
            relevant = self._surfacer.check_relevance(node, cosine_similarity)
            for hot_node in relevant:
                await self._event_bus.emit(MemoryEvent(
                    event_type=EventType.PROACTIVE_SURFACE, node_id=node.id,
                    data={"related_to": hot_node.id, "related_content": hot_node.content[:200]}))

        await self._event_bus.emit(MemoryEvent(event_type=EventType.MEMORY_CREATED, node_id=node.id))
        if importance >= 0.8:
            await self._event_bus.emit(MemoryEvent(
                event_type=EventType.HIGH_IMPORTANCE_WRITE, node_id=node.id,
                data={"importance": importance}))
        self._retrieval.invalidate_cache()
        return node

    add = _sync(async_add)
    # Synchronous wrapper. For full documentation see async_add().

    async def async_add_batch(self, items: list[dict]) -> list[MemoryNode]:
        """
        Store multiple memories in a single batch operation.

        More efficient than calling async_add() in a loop because writes are
        batched to storage. Validation and streaming consolidation are skipped
        per-item; run async_consolidate() after a batch import to deduplicate.

        Args:
            items: List of dicts, each containing:
                - content (str, required): The memory content.
                - kind (str, optional): Memory kind string.
                - importance (float, optional): Importance score 0.0–1.0.
                - confidence (float, optional): Confidence score. Default 1.0.
                - decay_rate (float, optional): Decay rate. Default 0.0.
                - tags (list[str], optional): Tags for filtering.
                - metadata (dict, optional): Arbitrary metadata.
                - provenance (dict or Provenance, optional): Source/session info.
                - parent_id (str, optional): Parent node ID.
                - event_time (float, optional): Event Unix timestamp.

        Returns:
            list[MemoryNode]: Created nodes in the same order as ``items``.
        """
        await self._ensure_init()
        nodes = []
        for it in items:
            c = it["content"]
            kind_str = it.get("kind")
            mk = (self._classifier.classify(c) if kind_str is None and self._classifier
                  else MemoryKind(kind_str) if kind_str else MemoryKind.OBSERVATION)
            imp = it.get("importance")
            if imp is None:
                imp = self._imp_clf.predict(c, mk) if self._imp_clf else 0.5
            prov = it.get("provenance", Provenance())
            if isinstance(prov, dict):
                prov = Provenance.from_dict(prov)
            if not prov.source:
                prov.source = self._source
            ns = Namespace(org=self._namespace.org, team=self._namespace.team,
                           agent=self._namespace.agent, session=self._namespace.session)
            n = MemoryNode(content=c, kind=mk, importance=imp,
                           confidence=it.get("confidence", 1.0),
                           decay_rate=it.get("decay_rate", 0.0),
                           tags=set(it.get("tags", [])), metadata=it.get("metadata", {}),
                           provenance=prov, namespace=ns, parent_id=it.get("parent_id"),
                           event_time=it.get("event_time"))
            n.embedding = self._embedder.embed(c)
            nodes.append(n)
        await self._storage.save_nodes_batch(nodes)
        for n in nodes:
            if n.embedding:
                self._ann.add(n.id, n.embedding)
            await self._storage.log_audit(AuditEvent(
                node_id=n.id, op=AuditOp.CREATE,
                detail={"kind": n.kind.value, "importance": n.importance}))
            if self._extractor:
                await auto_link_node(n, self._graph, self._storage,
                                     self._extractor, self._entity_index)
        self._retrieval.invalidate_cache()
        return nodes

    add_batch = _sync(async_add_batch)

    # ---- Conversation + Document Ingestion ----

    async def async_ingest_conversation(self, messages, session_id="",
                                         source="conversation", agent_id="",
                                         reference_date=None):
        """
        Extract and store memories from a conversation.

        Runs the ExtractionPipeline's hierarchical extractor over the message
        list to produce structured memory items (facts, preferences, entities,
        events, etc.), then stores each as a MemoryNode via async_add().

        Args:
            messages: List of ConversationMessage objects or dicts with keys
                'role' (str), 'content' (str), and optionally 'timestamp' (float)
                and 'metadata' (dict).
            session_id: Optional session identifier for namespace scoping and
                per-session retrieval filtering.
            source: Provenance source string. Default "conversation".
            agent_id: Agent identifier for multi-agent deployments.
            reference_date: Unix timestamp used as "now" for relative date
                resolution (e.g., "yesterday" → specific date). If None,
                uses the current system time.

        Returns:
            list[MemoryNode]: All memory nodes created from the conversation.
        """
        await self._ensure_init()
        msgs = []
        for m in messages:
            if isinstance(m, dict):
                msgs.append(ConversationMessage(
                    role=m.get("role", "user"), content=m.get("content", ""),
                    timestamp=m.get("timestamp"), metadata=m.get("metadata", {})))
            else:
                msgs.append(m)
        items = await self._extraction.ingest_conversation(
            msgs, session_id=session_id, source=source, agent_id=agent_id,
            reference_date=reference_date)
        nodes = []
        for item in items:
            prov = item.get("provenance", Provenance())
            if isinstance(prov, dict):
                prov = Provenance.from_dict(prov)
            node = await self.async_add(
                content=item["content"], kind=item.get("kind"),
                importance=item.get("importance"), confidence=item.get("confidence", 0.8),
                tags=item.get("tags", set()), metadata=item.get("metadata", {}),
                provenance=prov, event_time=item.get("event_time"))
            nodes.append(node)
        return nodes

    ingest_conversation = _sync(async_ingest_conversation)

    async def async_ingest_document(self, content: str, title: str = "",
                                     source: str = "document", document_id: str = ""):
        """
        Ingest a long document with semantic chunking.

        Splits the document into semantically coherent chunks using DocumentChunker,
        then extracts memory items from each chunk and stores them via async_add().
        Useful for indexing reference documents, knowledge bases, or long-form content.

        Args:
            content: Full document text to ingest.
            title: Optional document title, prepended to chunks for context.
            source: Provenance source string. Default "document".
            document_id: Optional identifier for the source document, stored in
                metadata for retrieval and lineage tracking.

        Returns:
            list[MemoryNode]: Memory nodes extracted and stored from the document.
        """
        await self._ensure_init()
        items = self._doc_pipeline.process_document(
            content, title=title, source=source, document_id=document_id)
        nodes = []
        for item in items:
            prov = item.get("provenance", Provenance())
            if isinstance(prov, dict):
                prov = Provenance.from_dict(prov)
            node = await self.async_add(
                content=item["content"], kind=item.get("kind"),
                importance=item.get("importance"), confidence=item.get("confidence", 0.8),
                tags=item.get("tags", set()), metadata=item.get("metadata", {}),
                provenance=prov)
            nodes.append(node)
        return nodes

    ingest_document = _sync(async_ingest_document)

    # ---- CRUD ----

    async def async_get(self, node_id):
        """
        Fetch a single memory node by its ID.

        Args:
            node_id: The UUID string identifier of the memory node.

        Returns:
            MemoryNode if found, None if the node does not exist.
        """
        await self._ensure_init()
        return await self._storage.load_node(node_id)
    get = _sync(async_get)

    async def async_update(self, node_id, **kwargs):
        """
        Partially update mutable fields of an existing memory node.

        Mutable fields include: content, importance, confidence, decay_rate,
        tags, metadata, valid_from, valid_until, kind. Each update increments
        the node's version counter. If content is updated, the embedding is
        recomputed and the ANN index is refreshed.

        Args:
            node_id: The UUID string identifier of the node to update.
            **kwargs: Field name → new value pairs. Only fields present in
                MemoryNode are accepted; unknown fields are ignored.

        Returns:
            MemoryNode: The updated node, or None if node_id was not found.
        """
        await self._ensure_init()
        n = await self._storage.load_node(node_id)
        if not n:
            return None
        changes = {}
        for k, v in kwargs.items():
            if hasattr(n, k):
                changes[k] = {"old": str(getattr(n, k))[:100], "new": str(v)[:100]}
                setattr(n, k, v)
        if changes:
            n.version += 1
            if "content" in kwargs:
                n.embedding = self._embedder.embed(n.content)
                self._ann.add(n.id, n.embedding)
            await self._storage.save_node(n)
            await self._storage.log_audit(AuditEvent(
                node_id=n.id, op=AuditOp.UPDATE,
                detail={"changes": changes, "version": n.version}))
            self._retrieval.invalidate_cache()
        return n
    update = _sync(async_update)

    async def async_delete(self, node_id):
        """
        Permanently delete a memory node.

        Removes the node from storage, the knowledge graph, and the ANN index.
        Logs a DELETE audit event before removal. This is a hard delete —
        for GDPR-compliant user erasure use async_delete_user() instead.

        Args:
            node_id: The UUID string identifier of the node to delete.
        """
        await self._ensure_init()
        await self._storage.log_audit(AuditEvent(
            node_id=node_id, op=AuditOp.DELETE, detail={"reason": "manual"}))
        await self._storage.delete_node(node_id)
        self._graph.remove_node(node_id)
        self._ann.remove(node_id)
        self._retrieval.invalidate_cache()
    delete = _sync(async_delete)

    async def async_link(self, source_id, target_id, relation, weight=1.0, metadata=None):
        e = Edge(source_id=source_id, target_id=target_id, relation=relation,
                 weight=weight, metadata=metadata or {})
        self._graph.add_edge(e)
        await self._storage.save_edge(e)
        return e
    link = _sync(async_link)

    async def async_rollback(self, node_id, to_version):
        n = await self._storage.load_node(node_id)
        if not n or to_version >= n.version:
            return n
        cur = n.version
        n.version = to_version
        await self._storage.save_node(n)
        await self._storage.log_audit(AuditEvent(
            node_id=node_id, op=AuditOp.ROLLBACK, detail={"from": cur, "to": to_version}))
        return n
    rollback = _sync(async_rollback)

    # ---- Upgrade 4: Confidence calibration feedback ----

    async def async_feedback(self, node_id: str, correct: bool):
        """
        Record whether a memory retrieval result was correct.

        Drives the Bayesian confidence calibration engine. Each feedback call
        updates the calibration weight for the node's confidence bucket. After
        sufficient feedback (≥10 calls), calibrated_confidence diverges from
        raw confidence for over- and under-confident nodes.

        Args:
            node_id: The UUID string identifier of the memory that was used.
            correct: True if the retrieved memory led to a correct answer,
                False if it led to an incorrect or irrelevant answer.

        Returns:
            Updated calibration state dict from CalibrationEngine.
        """
        await self._ensure_init()
        return await self._calibration.record_feedback(node_id, correct)

    feedback = _sync(async_feedback)

    async def async_calibration_report(self):
        await self._ensure_init()
        return await self._calibration.calibration_report()
    calibration_report = _sync(async_calibration_report)

    # ---- Upgrade 11: Lineage ----

    async def async_lineage(self, node_id: str) -> LineageReport:
        """
        Retrieve the complete lineage history of a memory node.

        Constructs a LineageReport by tracing the audit log for all operations
        on the node (CREATE, UPDATE, SUPERSEDE, CONSOLIDATE, DELETE) and
        collecting its immediate graph neighbors (parent, children, edges).

        Args:
            node_id: The UUID string identifier of the node.

        Returns:
            LineageReport dataclass containing:
                - node_id: The queried node ID.
                - operations: List of AuditEvent records in chronological order.
                - graph_neighbors: List of (relation, neighbor_node_id) tuples.
        """
        await self._ensure_init()
        return await self._lineage.lineage(node_id)
    lineage = _sync(async_lineage)

    # ---- Retrieval ----

    async def async_recall(self, query: str, limit=10, tiers=None, kinds=None,
                            tags=None, sources=None, context_ids=None,
                            min_importance=0.0, weights=None, namespace=None,
                            time_start=None, time_end=None,
                            event_time_start=None, event_time_end=None,
                            temporal_center=None, temporal_width_hours=168.0,
                            use_event_time=False, filter_expr=None,
                            include_expired=False, kind_boost=None):
        """
        Retrieve memories semantically relevant to a query.

        Combines six signals into a composite ranking score:
          1. Semantic cosine similarity (dense or TF-IDF embedding match)
          2. Lexical BM25/FTS keyword match
          3. Activation (importance × confidence of the node)
          4. Graph spreading activation (proximity via knowledge graph edges)
          5. Importance × calibrated confidence product
          6. Temporal Gaussian proximity to a reference time window

        Optionally applies cross-encoder reranking when ``reranker=True`` was
        passed to MemoryStore.__init__. Expired memories (valid_until < now)
        are excluded by default.

        Args:
            query: Natural language query string.
            limit: Maximum number of results to return. Default 10.
            tiers: Optional set of MemoryTier values to restrict results to
                ('working', 'episodic', 'semantic').
            kinds: Optional set of memory kind strings to restrict results.
            tags: Optional set of tag strings; only memories with at least one
                matching tag are returned.
            sources: Optional set of source strings to filter by provenance.
            context_ids: List of MemoryNode IDs to use as graph spreading
                activation seeds (for follow-on contextual retrieval).
            min_importance: Minimum importance score filter. Default 0.0.
            weights: Dict of signal name → weight overrides. Keys: 'semantic',
                'lexical', 'activation', 'graph', 'importance', 'temporal'.
            namespace: Namespace for hierarchical scope filtering.
            time_start: Filter to memories created after this Unix timestamp.
            time_end: Filter to memories created before this Unix timestamp.
            event_time_start: Filter by event_time (real-world event time) after
                this Unix timestamp.
            event_time_end: Filter by event_time before this Unix timestamp.
            temporal_center: Unix timestamp for Gaussian temporal scoring center.
                Defaults to now.
            temporal_width_hours: Half-width of the temporal Gaussian window in
                hours. Default 168 (one week). Wider = more memories are
                temporally relevant.
            use_event_time: If True, use event_time for temporal scoring instead
                of created_at. Default False.
            filter_expr: Optional FilterExpr for structured predicate filtering.
            include_expired: If True, include memories where valid_until < now.
                Default False.
            kind_boost: Dict of MemoryKind → float score multiplier applied to
                results of that kind. Example: {MemoryKind.PREFERENCE: 1.5}.

        Returns:
            list[RetrievalResult]: Ranked results, each containing:
                - node: The MemoryNode
                - score: Composite score (unbounded, higher is better)
                - score_components: Dict of per-signal scores
                - explanation: Human-readable explanation of why retrieved
        """
        await self._ensure_init()
        rq = RetrievalQuery(
            text=query, limit=limit,
            tiers={MemoryTier(t) for t in tiers} if tiers else None,
            kinds={MemoryKind(k) for k in kinds} if kinds else None,
            tags=tags, sources=sources, context_ids=context_ids or [],
            min_importance=min_importance, namespace=namespace,
            time_start=time_start, time_end=time_end,
            event_time_start=event_time_start, event_time_end=event_time_end,
            temporal_center=temporal_center, temporal_width_hours=temporal_width_hours,
            use_event_time=use_event_time, filter_expr=filter_expr,
            include_expired=include_expired)
        effective_weights = weights or self._profile_weights or {}
        for k in ("semantic", "lexical", "activation", "graph", "importance", "temporal"):
            if k in effective_weights:
                setattr(rq, f"w_{k}", effective_weights[k])
        # Auto-detect preference query and set kind_boost
        if kind_boost is not None:
            rq.kind_boost = kind_boost
        elif query:
            _pref_words = {"prefer", "like", "love", "hate", "favorite",
                           "always", "never", "tend to", "usually"}
            q_lower = query.lower()
            if any(w in q_lower for w in _pref_words):
                rq.kind_boost = {MemoryKind.PREFERENCE: 1.5}
        return await self._retrieval.retrieve(rq)
    recall = _sync(async_recall)

    async def async_query(self, kinds=None, tags=None, session_id=None,
                          source=None, namespace=None, time_start=None,
                          time_end=None, limit=50):
        """
        Structured filter-based query without semantic scoring.

        Returns memories matching a single filter criterion without computing
        similarity scores. Faster than async_recall() for exact-match lookups.
        Only one filter parameter is active per call (priority: kinds > tags >
        session_id > source > namespace > time range > none).

        Args:
            kinds: List of kind strings to match (e.g., ['fact', 'entity']).
            tags: Set of tag strings; returns memories with any matching tag.
            session_id: Return all memories from a specific session.
            source: Return all memories from a specific provenance source.
            namespace: Return all memories within a namespace scope.
            time_start: Return memories created after this Unix timestamp.
            time_end: Return memories created before this Unix timestamp.
            limit: Maximum results. Default 50.

        Returns:
            list[MemoryNode]: Unscored memory nodes matching the filter.
        """
        await self._ensure_init()
        if kinds: return await self._storage.query_by_kind(list(kinds), limit)
        if tags: return await self._storage.query_by_tags(tags, limit)
        if session_id: return await self._storage.query_by_session(session_id)
        if source: return await self._storage.query_by_source(source, limit)
        if namespace: return await self._storage.query_by_namespace(namespace, limit)
        if time_start is not None or time_end is not None:
            return await self._storage.query_by_time_range(time_start, time_end, limit)
        return await self._storage.get_active_nodes()
    query = _sync(async_query)

    async def async_build_context(self, query, token_budget=4000, chars_per_token=4.0,
                                   context_ids=None, include_metadata=False,
                                   include_explanations=False, include_confidence=False,
                                   min_relevance_score=0.0, context_as_of=None,
                                   session_balanced=False, recall_limit=30,
                                   candidate_ids=None):
        """
        Build a formatted context string ready to inject into an LLM prompt.

        Retrieves relevant memories via async_recall(), respects a token budget,
        groups results by memory tier (Semantic / Episodic / Working), and
        returns a structured text block. Optionally abstracts over retrieval
        via candidate_ids to preselect specific nodes.

        Prefer this method over async_recall() when constructing LLM prompts,
        as it handles budget truncation, tier grouping, session balancing, and
        abstention automatically.

        Args:
            query: Query string for memory retrieval.
            token_budget: Approximate maximum output tokens. Converted to
                characters using chars_per_token. Default 4000.
            chars_per_token: Characters per token estimate. Default 4.0.
            context_ids: Seed node IDs for graph spreading activation.
            include_metadata: If True, append tag list to each memory line.
            include_explanations: If True, append retrieval explanation to
                each memory line.
            include_confidence: If True, append confidence percentage to
                each memory line.
            min_relevance_score: Minimum composite score threshold for inclusion.
                If max_score < this threshold, returns abstention message.
                Uses auto-calibrated threshold if 0.0 and auto_calibrate_abstention
                was set at init time.
            context_as_of: Unix timestamp; exclude memories with valid_until
                before this time (historical context reconstruction).
            session_balanced: If True, allocate context budget across sessions
                proportionally before filling by score. Useful for multi-session
                question answering.
            recall_limit: Number of candidates to retrieve before applying
                budget truncation. Default 30.
            candidate_ids: If provided, load these specific node IDs directly
                instead of running async_recall(). Bypasses semantic retrieval.

        Returns:
            tuple[str, dict]: (context_string, metadata) where metadata contains:
                - abstained (bool): True if no memories met the relevance threshold
                - max_relevance_score (float): Highest score in the result set
                - memories_retrieved (int): Number of memories retrieved
        """
        budget = int(token_budget * chars_per_token)
        # Use auto-calibrated threshold if none explicitly provided
        if min_relevance_score == 0.0 and self._abstention_threshold > 0:
            min_relevance_score = self._abstention_threshold

        if candidate_ids is not None:
            # Load specific nodes directly (bypasses internal recall).
            # Sort by activation score as proxy for retrieval relevance.
            results = []
            for nid in candidate_ids:
                n = await self._storage.load_node(nid)
                if n and not n.superseded_by:
                    results.append(RetrievalResult(
                        node=n,
                        score=n.activation,
                        score_components={"activation": n.activation},
                        explanation="Externally provided candidate node."))
            results.sort(key=lambda r: r.score, reverse=True)
            results = results[:recall_limit]
        else:
            results = await self.async_recall(query, limit=recall_limit, context_ids=context_ids)

        # Filter by context_as_of: exclude memories with valid_until before that time
        if context_as_of is not None:
            results = [r for r in results
                       if r.node.valid_until is None or r.node.valid_until >= context_as_of]

        # Compute abstention metadata
        max_score = max((r.score for r in results), default=0.0)
        memories_retrieved = len(results)
        abstained = (min_relevance_score > 0 and max_score < min_relevance_score)

        meta = {
            "abstained": abstained,
            "max_relevance_score": max_score,
            "memories_retrieved": memories_retrieved,
        }

        if abstained:
            return ("No relevant memories found for this query.", meta)

        lines, used = [], 0
        def _add(s):
            nonlocal used
            if used + len(s) > budget: return False
            lines.append(s); used += len(s); return True
        _add("=== Agent Memory Context ===\n")

        if session_balanced and results:
            # Session-balanced context assembly (Upgrade 6)
            ordered = self._session_balanced_order(results, budget)
            for r in ordered:
                e = f"- {r.node.content}"
                if include_confidence: e += f" (conf: {r.node.confidence:.0%})"
                if include_metadata and r.node.tags: e += f" [{', '.join(r.node.tags)}]"
                if include_explanations and r.explanation: e += f"\n  ^ {r.explanation}"
                if not _add(e + "\n"): break
        else:
            groups = {t: [] for t in MemoryTier}
            for r in results:
                groups[r.node.tier].append(r)
            labels = {MemoryTier.SEMANTIC: "Known Facts", MemoryTier.EPISODIC: "Recent Events",
                      MemoryTier.WORKING: "Active Context"}
            for tier in (MemoryTier.SEMANTIC, MemoryTier.EPISODIC, MemoryTier.WORKING):
                if not groups[tier]: continue
                if not _add(f"\n[{labels[tier]}]\n"): break
                for r in groups[tier]:
                    e = f"- {r.node.content}"
                    if include_confidence: e += f" (conf: {r.node.confidence:.0%})"
                    if include_metadata and r.node.tags: e += f" [{', '.join(r.node.tags)}]"
                    if include_explanations and r.explanation: e += f"\n  ^ {r.explanation}"
                    if not _add(e + "\n"): break
        return ("".join(lines), meta)
    build_context = _sync(async_build_context)

    # ---- Consolidation ----
    async def async_consolidate(self):
        """
        Run the full consolidation cycle manually.

        Executes in order: prune decayed memories, deduplicate near-identical
        nodes, promote working→episodic, consolidate preferences, consolidate
        episodic→semantic clusters, detect and resolve contradictions, propagate
        confidence decay through contradiction edges, and decay unaccessed
        importance scores.

        Consolidation runs automatically on each write (streaming mode) when
        streaming_consolidation=True. Call this manually after bulk imports or
        to force a full cycle.

        Returns:
            dict with keys: pruned, deduplicated, promoted, preferences_consolidated,
                consolidated, contradictions, confidence_updates, importance_decayed.
                Each value is a count of affected nodes.
        """
        await self._ensure_init()
        result = await self._consolidation.run_full_cycle()
        self._retrieval.invalidate_cache()
        return result
    consolidate = _sync(async_consolidate)

    async def async_prune(self):
        return await self._consolidation.prune_decayed()
    prune = _sync(async_prune)

    # ---- GDPR ----
    async def async_delete_user(self, user_id):
        """
        GDPR-compliant erasure of all memories associated with a user.

        Deletes all MemoryNodes whose provenance.session_id or provenance.source
        matches user_id, removes their embeddings from the ANN index, their
        entries from FTS, their edges from the graph, and their audit log entries.
        Returns a verifiable DeletionReceipt.

        Args:
            user_id: User identifier string. Matched against provenance.session_id
                and provenance.source fields.

        Returns:
            DeletionReceipt dataclass containing: user_id, deleted_node_count,
                deleted_edge_count, receipt_id (UUID), timestamp, and a
                verification_hash for compliance audit trails.
        """
        await self._ensure_init()
        r = await self._gdpr.delete_user(user_id)
        self._retrieval.invalidate_cache()
        return r
    delete_user = _sync(async_delete_user)

    async def async_delete_namespace(self, ns):
        """
        Delete all memories within a namespace scope.

        Args:
            ns: Namespace object or string identifying the scope to erase.

        Returns:
            DeletionReceipt with deletion counts and verification hash.
        """
        await self._ensure_init()
        r = await self._gdpr.delete_namespace(ns)
        self._retrieval.invalidate_cache()
        return r
    delete_namespace = _sync(async_delete_namespace)

    # ---- Health ----
    async def async_health_check(self):
        """
        Return a health report for the memory store.

        Computes aggregate quality metrics: total/active/superseded/expired
        node counts, contradiction rate, stale fraction, confidence entropy,
        calibration gap, and an overall health score. Also calibrates the
        abstention threshold as the 10th percentile of active memory scores.

        Returns:
            HealthReport dataclass with fields: total_nodes, active_nodes,
                superseded_nodes, expired_nodes, contradiction_rate, stale_fraction,
                confidence_entropy, calibration_gap, health_score, abstention_threshold,
                and drift_signals dict.
        """
        await self._ensure_init()
        return await self._health.health_check()
    health_check = _sync(async_health_check)

    async def async_detect_drift(self):
        await self._ensure_init()
        return await self._health.detect_drift()
    detect_drift = _sync(async_detect_drift)

    # ---- Audit / Introspection ----
    async def async_history(self, node_id=None, limit=100):
        return await self._storage.get_audit_log(node_id, limit)
    history = _sync(async_history)

    async def async_stats(self):
        """
        Return aggregate statistics about the memory store.

        Returns:
            dict with keys:
                - total_memories (int): All nodes including superseded.
                - active_memories (int): Non-superseded nodes.
                - superseded (int): Superseded node count.
                - expired (int): Active nodes past their valid_until timestamp.
                - edges (int): Total graph edges.
                - ann_index_size (int): Nodes in the ANN index.
                - embedder_mode (str): 'dense', 'tfidf', or 'custom'.
                - profile (str): Active MemoryProfile name, or 'none'.
                - by_tier (dict): Node counts per tier (working/episodic/semantic).
                - by_kind (dict): Node counts per kind (fact/entity/etc.).
        """
        await self._ensure_init()
        nodes = await self._storage.get_all_nodes()
        tc = {t.value: 0 for t in MemoryTier}
        kc: dict[str, int] = {}
        for n in nodes:
            tc[n.tier.value] += 1
            kc[n.kind.value] = kc.get(n.kind.value, 0) + 1
        active = [n for n in nodes if n.superseded_by is None]
        import time as _t
        expired = sum(1 for n in active if n.valid_until and _t.time() > n.valid_until)
        return {
            "total_memories": len(nodes), "active_memories": len(active),
            "superseded": len(nodes) - len(active), "expired": expired,
            "edges": self._graph.edge_count, "ann_index_size": self._ann.size,
            "embedder_mode": getattr(self._embedder, 'mode', 'custom'),
            "profile": self._profile.name if self._profile else "none",
            "by_tier": tc, "by_kind": {k: v for k, v in kc.items() if v > 0}}
    stats = _sync(async_stats)

    def explain(self, result: RetrievalResult) -> str:
        n = result.node
        return "\n".join([
            f"Memory: {n.content[:100]}...",
            f"Kind: {n.kind.value} | Tier: {n.tier.value}",
            f"Score: {result.score:.4f}",
            f"Components: {', '.join(f'{k}={v:.3f}' for k, v in result.score_components.items())}",
            f"Confidence: {n.confidence:.2f} | Importance: {n.importance:.2f}",
            f"Valid: {n.is_valid} | Media: {n.media_type}",
            f"Explanation: {result.explanation}"])

    @staticmethod
    def _session_balanced_order(results: list[RetrievalResult],
                                budget: int) -> list[RetrievalResult]:
        """Order results with session-balanced allocation."""
        from collections import defaultdict
        sessions: dict[str, list[RetrievalResult]] = defaultdict(list)
        for r in results:
            sid = r.node.provenance.session_id or "_default"
            sessions[sid].append(r)
        for sid in sessions:
            sessions[sid].sort(key=lambda r: r.score, reverse=True)

        num_sessions = max(len(sessions), 1)
        floor_chars = min(600, budget // num_sessions)

        # Phase 1: fill floor allocation per session
        ordered: list[RetrievalResult] = []
        remaining: list[RetrievalResult] = []
        for sid, group in sessions.items():
            chars_used = 0
            for r in group:
                entry_len = len(r.node.content) + 4  # "- " + "\n"
                if chars_used + entry_len <= floor_chars:
                    ordered.append(r)
                    chars_used += entry_len
                else:
                    remaining.append(r)

        # Phase 2: fill rest by score descending
        remaining.sort(key=lambda r: r.score, reverse=True)
        ordered.extend(remaining)
        return ordered

    def neighbors(self, node_id, relation=None):
        return self._graph.neighbors(node_id, relation=relation, direction="both")

    async def async_export(self):
        """
        Export all memories, edges, audit log, and stats to a dict.

        Returns:
            dict with keys:
                - version (str): "4.0.0"
                - nodes (list[dict]): All MemoryNode records as dicts.
                - edges (list[dict]): All graph edges as dicts.
                - audit_log (list[dict]): Up to 10,000 most recent audit events.
                - stats (dict): Output of async_stats().

            Pass to MigrationExporter to convert to Mem0 format or write to file.
        """
        await self._ensure_init()
        nodes = await self._storage.get_all_nodes()
        return {
            "version": "4.0.0",
            "nodes": [n.to_dict() for n in nodes],
            "edges": self._graph.to_list(),
            "audit_log": [e.to_dict() for e in await self._storage.get_audit_log(limit=10000)],
            "stats": await self.async_stats()}
    export = _sync(async_export)

    async def async_close(self):
        """
        Flush pending operations and shut down the memory store.

        Stops the ConsolidationScheduler background task if running, then
        closes the storage backend (flushes WAL, closes connections).
        Call this when the store is no longer needed, or use the async
        context manager (async with MemoryStore() as mem:) for automatic cleanup.
        """
        if self._scheduler:
            await self._scheduler.stop()
        await self._storage.close()
    close = _sync(async_close)

    async def async_len(self):
        return await self._storage.count()

    def __len__(self):
        try:
            asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, self.async_len()).result()
        except RuntimeError:
            return asyncio.run(self.async_len())

    def __repr__(self):
        p = self._profile.name if self._profile else "default"
        return f"MemoryStore(v4, profile={p}, embedder={getattr(self._embedder, 'mode', 'custom')})"

    async def __aenter__(self):
        await self._ensure_init()
        return self

    async def __aexit__(self, *a):
        await self.async_close()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()
