# agentmemory V4 — Repository Audit

> Audit date: 2026-03-21
> Auditor: Claude Code (claude-sonnet-4-6)
> Scope: All Python source files, documentation, configuration, and benchmark result files
> Excluded: `.venv/`, `__pycache__/`, `.claude/`

---

## Section 1 — File Inventory

Every file in the repository with one-sentence purpose description, approximate line count, and quality rating.

Quality ratings:
- **clean** — well-structured, self-documenting, comments adequate for complexity
- **needs-comments** — logic is non-obvious in places; inline comments are sparse
- **needs-docstrings** — public methods/classes lack docstrings
- **needs-cleanup** — dead code, inconsistent style, or structural issues

### Package source files

| File | Purpose | ~Lines | Quality |
|------|---------|--------|---------|
| `agentmemory/__init__.py` | Public API exports (`__all__`) and module-level quick-start docstring | 77 | clean |
| `agentmemory/core.py` | Central `MemoryStore` class; all primary async/sync CRUD, recall, consolidation, GDPR, health, lineage, and export operations | 804 | needs-docstrings |
| `agentmemory/models.py` | All dataclass definitions: `MemoryNode`, `MemoryKind`, `MemoryTier`, `Namespace`, `Provenance`, `Edge`, `RetrievalResult`, `FilterExpr`, `MemoryEvent`, `HealthReport`, `DeletionReceipt`, `LineageReport`, `MemoryProfile`, and all supporting enums | 620 | needs-docstrings |
| `agentmemory/retrieval.py` | `RetrievalEngine` implementing six-signal hybrid scoring (semantic cosine, lexical FTS, activation, graph spreading, importance×confidence, temporal Gaussian) plus `QueryCache` and `RetrieverWeightAdapter` | 396 | needs-comments |
| `agentmemory/embeddings.py` | `Embedder` Protocol and four implementations: `DenseEmbedder`, `TFIDFEmbedder`, `MultiModalEmbedder`, `FunctionEmbedder`; plus `create_embedder` factory and `cosine_similarity` | 240 | clean |
| `agentmemory/consolidation.py` | `ConsolidationEngine` (deduplicate, promote, consolidate episodic→semantic, detect/resolve contradictions, decay confidence) and `ConsolidationScheduler` background task | 715 | needs-comments |
| `agentmemory/storage/backend.py` | `StorageBackend` Protocol defining the complete storage interface (save, get, update, delete, search, FTS, audit, edges) | 54 | clean |
| `agentmemory/storage/__init__.py` | Re-exports `StorageBackend` Protocol for package-level import | 54 | clean |
| `agentmemory/storage/sqlite_backend.py` | `SQLiteBackend` with WAL mode, FTS5 virtual table, 34-column schema, ThreadPoolExecutor async wrapping, and full audit log | 429 | needs-comments |
| `agentmemory/storage/postgres_backend.py` | `PostgresBackend` using asyncpg connection pool, GIN-indexed tsvector full-text search, and full parity with SQLite backend | 337 | needs-comments |
| `agentmemory/graph.py` | `MemoryGraph` (in-memory adjacency with spreading activation), `EntityRelationExtractor` (regex + optional spaCy), and `auto_link_node` async entity linking with Jaccard cross-session matching | 330 | needs-comments |
| `agentmemory/ann_index.py` | Pure-Python `HNSWIndex` (thread-safe HNSW approximate nearest neighbor) and `HNSWLibIndex` adapter for the `hnswlib` package | 258 | needs-comments |
| `agentmemory/extraction.py` | `ExtractionPipeline` (rule-based / LLM / hierarchical), `HierarchicalExtractor` (3-pass), `DocumentChunker`, `DocumentIngestionPipeline`, and temporal grounding during ingestion | 495 | needs-docstrings |
| `agentmemory/validation.py` | `WriteValidator` orchestrating six constitutional rules: schema, content length, importance floor, near-duplicate, contradiction pre-check, source authorization | 214 | clean |
| `agentmemory/importance.py` | Feature-engineered logistic `ImportanceClassifier` and `ImportanceEvolver` (Bayesian on-access update + exponential decay of unaccessed nodes) | 131 | needs-comments |
| `agentmemory/classification.py` | `KindClassifier` signal-word scoring across 12 memory kinds with structural bonuses and confidence output | 162 | needs-comments |
| `agentmemory/events.py` | `EventBus` pub/sub (sync + async handlers) and `ProactiveSurfacer` (hot-memory set with similarity-triggered surface events) | 133 | clean |
| `agentmemory/health.py` | `HealthMonitor` producing full `HealthReport`, abstention threshold calibration (10th percentile), and drift detection (contradiction rate, stale fraction, entropy, calibration gap) | 125 | needs-docstrings |
| `agentmemory/calibration.py` | `CalibrationEngine` with Bayesian feedback weighting (`min(1, total/10)`) and 5-bucket calibration curve report | 118 | clean |
| `agentmemory/lineage.py` | `LineageEngine.lineage(node_id)` reconstructing complete `LineageReport` from audit log and graph neighbors | 99 | clean |
| `agentmemory/temporal.py` | `TemporalGrounder` resolving 30+ relative date patterns ("yesterday", "last Monday", "3 weeks ago") to Unix timestamps | 326 | needs-comments |
| `agentmemory/gdpr.py` | `GDPRPipeline` implementing complete deletion with ANN/FTS/audit cleanup and verifiable `DeletionReceipt` | 111 | clean |
| `agentmemory/federation.py` | `FederatedStore` querying multiple `MemoryStore` instances, deduplicating by content hash, and merging ranked results | 57 | clean |
| `agentmemory/migration.py` | `MigrationImporter` (from Mem0, Zep, LangMem, JSON, auto-detect) and `MigrationExporter` (to Mem0 format, to file) | 223 | needs-docstrings |
| `agentmemory/query_expansion.py` | `QueryExpander` with three strategies: synonym groups (14 groups), entity normalization (strip titles, name extraction), and question reformulation (10 patterns) | 166 | clean |
| `agentmemory/reranking.py` | `CrossEncoderReranker` lazy-loading `cross-encoder/ms-marco-MiniLM-L-6-v2`, batch scoring, blending 70% bi-encoder + 30% CE | 65 | clean |
| `agentmemory/server.py` | FastAPI REST server (`create_app`) with 16 endpoints covering all MemoryStore operations | 213 | needs-docstrings |
| `agentmemory/mcp.py` | `MCPServer` with 11 MCP tools over stdio JSON-RPC for Model Context Protocol integration | 183 | needs-docstrings |
| `agentmemory/__main__.py` | CLI entry point with subcommands: `serve`, `mcp`, `inspect`, `bench`, `import`, `export` | 111 | clean |
| `agentmemory/benchmark.py` | `Benchmark` class with 6 workloads: scale write/recall, retrieval fidelity, consolidation efficiency, temporal retrieval, conversation ingestion | 250 | needs-comments |
| `agentmemory/tests.py` | 24 async test functions covering all core subsystems and the `run_all()` orchestrator | 433 | needs-comments |
| `agentmemory/integrations/__init__.py` | Five framework adapters: `LangChainMemory`, `LangGraphMemoryAdapter`, `OpenAIToolAdapter`, `CrewAIMemoryAdapter`, `VercelAIAdapter` | 234 | needs-docstrings |

### Configuration files

| File | Purpose | ~Lines | Quality |
|------|---------|--------|---------|
| `pyproject.toml` | Package metadata (name, version, Python requires, optional dependency extras: dense, onnx, server, spacy, postgres, clip, whisper, all) | 36 | clean |

### Documentation and benchmark result files

| File | Purpose | ~Lines | Quality |
|------|---------|--------|---------|
| `README.md` | Primary user-facing documentation (installation, quick-start, API overview, feature list, links) | ~(not re-read; estimated 400+) | needs-cleanup (see Section 6) |
| `BENCHMARKS.md` | Comprehensive benchmark documentation: hardware spec, internal suite results, LongMemEval run history, competitive comparison table, reproduction instructions | 634 | clean |
| `stability_final_analysis.md` | Stability verification report: two gpt-4.1 runs (98.00% + 97.40%), systematic vs stochastic failure analysis | 84 | clean |
| `longmemeval_4o_report.md` | GPT-4o judge evaluation: 94.40% (472/500), per-type breakdown, all 28 wrong cases | 201 | clean |
| `latency_results.md` | 2026-03-21 latency benchmark comparing TF-IDF vs dense (MPNet) modes against published BENCHMARKS.md figures | 216 | clean |

---

## Section 2 — Public API Surface

Every class and method a developer would interact with, classified as:
- **primary** — first thing a new user reaches for
- **secondary** — used in most real deployments but after basics work
- **advanced** — power-user / framework-integration / operational use

### `MemoryStore` (agentmemory/core.py)

**Construction and lifecycle**

| Method / attribute | Classification | Notes |
|-------------------|---------------|-------|
| `MemoryStore.__init__(db_path, embedder, llm_extractor, …)` | primary | Main constructor; 15+ keyword parameters |
| `MemoryStore.from_profile(preset_name, **overrides)` | secondary | Named presets: `default`, `summarizer`, `coding_assistant`, `support_agent`, `research_agent` |
| `MemoryStore.close()` / `async_close()` | secondary | Flush, persist, shutdown background tasks |

**Write operations**

| Method | Classification | Notes |
|--------|---------------|-------|
| `add(content, kind, importance, …)` / `async_add(…)` | primary | Core write; runs validation, extraction, auto-graph, consolidation trigger |
| `add_batch(memories)` / `async_add_batch(…)` | secondary | Bulk insert list of dicts |
| `ingest_conversation(messages)` / `async_ingest_conversation(…)` | primary | Extract memories from `ConversationMessage` list |
| `ingest_document(text, …)` / `async_ingest_document(…)` | secondary | Chunk + extract memories from long text |

**Read / recall operations**

| Method | Classification | Notes |
|--------|---------------|-------|
| `recall(query, top_k, …)` / `async_recall(…)` | primary | Main retrieval; returns `List[RetrievalResult]` |
| `query(filter_expr)` / `async_query(…)` | secondary | Structured filter-based query (no semantic scoring) |
| `get(node_id)` / `async_get(…)` | secondary | Fetch single node by ID |
| `build_context(query, …)` / `async_build_context(…)` | primary | Returns formatted string context block ready to inject into LLM prompt |

**Update and delete operations**

| Method | Classification | Notes |
|--------|---------------|-------|
| `update(node_id, **fields)` / `async_update(…)` | secondary | Partial update of mutable fields |
| `delete(node_id)` / `async_delete(…)` | secondary | Soft or hard delete single node |

**Consolidation and maintenance**

| Method | Classification | Notes |
|--------|---------------|-------|
| `consolidate()` / `async_consolidate()` | secondary | Run full consolidation cycle manually |

**GDPR and compliance**

| Method | Classification | Notes |
|--------|---------------|-------|
| `delete_user(user_id)` / `async_delete_user(…)` | advanced | Complete user data erasure with `DeletionReceipt` |
| `delete_namespace(namespace)` / `async_delete_namespace(…)` | advanced | Namespace-scoped erasure |

**Observability**

| Method | Classification | Notes |
|--------|---------------|-------|
| `health()` / `async_health()` | secondary | Returns `HealthReport` with quality metrics, drift signals, abstention threshold |
| `stats()` / `async_stats()` | secondary | Returns dict of aggregate memory statistics |
| `lineage(node_id)` / `async_lineage(…)` | advanced | Returns `LineageReport` with full causal audit chain |
| `feedback(node_id, correct)` / `async_feedback(…)` | secondary | Bayesian confidence update; drives calibration curve |

**Export**

| Method | Classification | Notes |
|--------|---------------|-------|
| `export(fmt)` / `async_export(…)` | secondary | Export all memories; supports `agentmemory` and `mem0` formats |

---

### `MemoryNode` (agentmemory/models.py)

| Attribute / property | Classification | Notes |
|---------------------|---------------|-------|
| `content`, `kind`, `importance`, `confidence`, `namespace`, `tags` | primary | Core fields |
| `event_time`, `valid_from`, `valid_until` | secondary | Bi-temporal and validity window fields |
| `is_valid()` | secondary | Checks `valid_from` / `valid_until` against reference time |
| `calibrated_confidence` | secondary | Property blending raw confidence with calibration weight |
| `activation` | secondary | Property: `importance × confidence` |
| `effective_time` | secondary | Property: `event_time` if set, else `created_at` |
| `provenance` | advanced | Source tracking (`Provenance` dataclass) |

### `MemoryProfile` (agentmemory/models.py)

| Method | Classification | Notes |
|--------|---------------|-------|
| `MemoryProfile.from_preset(name)` | secondary | Factory for 5 named profiles |

### `RetrievalResult` (agentmemory/models.py)

| Attribute | Classification | Notes |
|-----------|---------------|-------|
| `node`, `score`, `rank`, `explanation` | primary | Main result wrapper returned by `recall()` |

### `FilterExpr` / `FilterCondition` (agentmemory/models.py)

| Usage | Classification | Notes |
|-------|---------------|-------|
| `FilterCondition(field, op, value)` | secondary | Single filter predicate |
| `FilterExpr(conditions, combinator)` | secondary | AND/OR compound filter for `query()` |

### `ConversationMessage` (agentmemory/models.py)

| Usage | Classification | Notes |
|-------|---------------|-------|
| `ConversationMessage(role, content, timestamp)` | primary | Input type for `ingest_conversation()` |

### Storage backends

| Class | Classification | Notes |
|-------|---------------|-------|
| `SQLiteBackend(db_path)` | secondary | Default backend; used automatically by `MemoryStore` |
| `PostgresBackend(dsn)` | advanced | Production-scale backend; pass as `storage=` to `MemoryStore` |
| `StorageBackend` (Protocol) | advanced | Implement to create a custom storage backend |

### Embedders (agentmemory/embeddings.py)

| Class | Classification | Notes |
|-------|---------------|-------|
| `create_embedder(model_name_or_none, prefer_dense)` | secondary | Preferred factory; auto-selects TF-IDF or dense |
| `DenseEmbedder(model_name)` | secondary | sentence-transformers dense embedder |
| `TFIDFEmbedder()` | secondary | Zero-dependency sparse embedder (default) |
| `FunctionEmbedder(fn)` | advanced | Wrap any callable as an embedder |
| `MultiModalEmbedder(…)` | advanced | CLIP + Whisper multi-modal support |

### Framework integrations (agentmemory/integrations/__init__.py)

| Class | Classification | Notes |
|-------|---------------|-------|
| `LangChainMemory(store)` | advanced | LangChain `BaseMemory` adapter |
| `LangGraphMemoryAdapter(store)` | advanced | LangGraph node-compatible adapter |
| `OpenAIToolAdapter(store)` | advanced | OpenAI Assistants tool spec adapter |
| `CrewAIMemoryAdapter(store)` | advanced | CrewAI memory interface adapter |
| `VercelAIAdapter(store)` | advanced | Vercel AI SDK adapter |

### Federation and migration

| Class | Classification | Notes |
|-------|---------------|-------|
| `FederatedStore(stores)` | advanced | Multi-store query with content-hash deduplication |
| `MigrationImporter` | advanced | Import from Mem0, Zep, LangMem, or JSON |
| `MigrationExporter` | advanced | Export to Mem0 format or file |

### Servers

| Class / function | Classification | Notes |
|-----------------|---------------|-------|
| `create_app(db_path)` (server.py) | advanced | FastAPI application factory; 16 REST endpoints |
| `MCPServer` (mcp.py) | advanced | Stdio JSON-RPC MCP server with 11 tools |

### EventBus (agentmemory/events.py)

| Method | Classification | Notes |
|--------|---------------|-------|
| `EventBus.on(event_type, handler)` | secondary | Subscribe sync or async handler |
| `EventBus.on_any(handler)` | secondary | Subscribe to all event types |
| `EventBus.emit(event)` / `emit_sync(event)` | advanced | Publish `MemoryEvent` to all subscribers |
| `EventBus.watch(event_type)` | advanced | Async generator yielding matching events |

---

## Section 3 — Docstring Coverage (core.py Public Methods)

For every public method in `agentmemory/core.py`, whether a docstring exists, what it says, and whether it is sufficient.

| Method | Has Docstring | Summary (if present) | Sufficient? |
|--------|--------------|----------------------|-------------|
| `MemoryStore.__init__` | No | — | No — 15+ parameters with non-obvious interactions (prefer_dense, auto_consolidate_threshold, llm_extractor, etc.) need parameter-level documentation |
| `MemoryStore.from_profile` | No | — | No — preset names and what each configures should be listed |
| `MemoryStore._ensure_init` | No | — | N/A (private) |
| `MemoryStore.async_add` | No | — | No — primary write method with 10+ parameters; callers need to know validation, auto-classification, and consolidation trigger behavior |
| `MemoryStore.add` | No | — | No — sync alias; should reference async_add and note threading behavior |
| `MemoryStore.async_add_batch` | No | — | No — should document input dict schema and batch atomicity guarantees |
| `MemoryStore.add_batch` | No | — | No |
| `MemoryStore.async_ingest_conversation` | No | — | No — should document `ConversationMessage` input format and what memories are extracted |
| `MemoryStore.ingest_conversation` | No | — | No |
| `MemoryStore.async_ingest_document` | No | — | No — should describe chunking strategy and how chunk_size/overlap interact |
| `MemoryStore.ingest_document` | No | — | No |
| `MemoryStore.async_recall` | No | — | No — most-used retrieval method; needs docs on top_k, filter, namespace, rerank, min_score parameters and score range |
| `MemoryStore.recall` | No | — | No |
| `MemoryStore.async_query` | No | — | No — filter expression DSL is non-obvious; needs examples |
| `MemoryStore.query` | No | — | No |
| `MemoryStore.async_get` | No | — | No |
| `MemoryStore.get` | No | — | No |
| `MemoryStore.async_build_context` | No | — | No — should clarify max_tokens, format string structure, and when to prefer this over `recall()` |
| `MemoryStore.build_context` | No | — | No |
| `MemoryStore.async_update` | No | — | No — should list which fields are mutable |
| `MemoryStore.update` | No | — | No |
| `MemoryStore.async_delete` | No | — | No — should document soft vs hard delete behavior |
| `MemoryStore.delete` | No | — | No |
| `MemoryStore.async_consolidate` | No | — | No — should note this is also triggered automatically |
| `MemoryStore.consolidate` | No | — | No |
| `MemoryStore.async_delete_user` | No | — | No — should reference GDPR compliance and `DeletionReceipt` return |
| `MemoryStore.delete_user` | No | — | No |
| `MemoryStore.async_delete_namespace` | No | — | No |
| `MemoryStore.delete_namespace` | No | — | No |
| `MemoryStore.async_health` | No | — | No — should describe the fields in `HealthReport` |
| `MemoryStore.health` | No | — | No |
| `MemoryStore.async_stats` | No | — | No — should list the keys in the returned dict |
| `MemoryStore.stats` | No | — | No |
| `MemoryStore.async_lineage` | No | — | No — should explain what constitutes lineage (audit ops + graph neighbors) |
| `MemoryStore.lineage` | No | — | No |
| `MemoryStore.async_feedback` | No | — | No — should describe Bayesian update mechanism and `correct` parameter |
| `MemoryStore.feedback` | No | — | No |
| `MemoryStore.async_export` | No | — | No — should list valid `fmt` values and output structure |
| `MemoryStore.export` | No | — | No |
| `MemoryStore.async_close` | No | — | No |
| `MemoryStore.close` | No | — | No |

**Summary**: `core.py` has zero docstrings on any public method. This is the single highest-priority documentation gap in the entire codebase. Every method listed above is either primary or secondary in the API surface and is used externally; none have parameter documentation, return type descriptions, exception notes, or usage examples in docstring form.

---

## Section 4 — Inline Comment Quality

The five most complex or non-obvious code sections across all files, with adequacy assessment.

---

### 1. `_sync` decorator (agentmemory/core.py, top of file)

**What it does**: Wraps any async coroutine method so it can be called synchronously, handling two distinct cases: (a) no running event loop — run via `asyncio.run()`; (b) running event loop already exists (e.g., Jupyter, nested async) — submit to a `ThreadPoolExecutor` thread that creates its own loop.

**Existing comments**: None. The decorator is implemented inline with no explanation of why the two-branch approach is needed or why ThreadPoolExecutor is used for the running-loop case.

**Adequacy**: Insufficient. This pattern is the cornerstone of the entire sync API surface and is non-obvious to anyone unfamiliar with asyncio internals. The absence of any comment forces readers to derive the intent from `asyncio.get_event_loop()` exception handling, which is a known footgun. Minimum needed: a block comment explaining the two cases and why `loop.run_until_complete` cannot be used from a running loop.

---

### 2. Six-signal hybrid scoring (agentmemory/retrieval.py, `RetrievalEngine._score_candidates`)

**What it does**: Combines six independently computed signals — semantic cosine similarity, lexical BM25/FTS score, activation (importance × confidence), graph spreading-activation score, importance×confidence product, and temporal Gaussian decay — into a single composite score using weighted sum, then applies cross-encoder reranking as an optional 7th signal blending 70/30.

**Existing comments**: Sparse. Individual signal computations are not labeled; the weight vector is defined inline without names; the Gaussian temporal decay formula has no explanation of the sigma parameter.

**Adequacy**: Insufficient. The scoring formula is the core ranking logic of the entire system. A developer tuning retrieval or debugging poor recall results must reverse-engineer which weight corresponds to which signal. Needed: (a) named constants for each weight, (b) a formula comment summarizing the composite, (c) a note on the Gaussian sigma semantics (half-life in seconds / days).

---

### 3. HNSW `_search_layer` (agentmemory/ann_index.py)

**What it does**: Pure-Python HNSW graph search within a single layer using a priority queue of (negative distance, node_id) tuples. Maintains a candidates heap and a results heap, expanding neighbors of the best candidate until the worst candidate is better than the best result, at which point the layer traversal terminates.

**Existing comments**: Minimal. The heap inversion (negated distances for max-heap simulation) is not explained. The stopping condition is present in code but has no comment explaining why it is correct per the HNSW paper.

**Adequacy**: Insufficient. HNSW layer traversal is a non-trivial algorithm. The priority-queue inversion pattern confuses developers unfamiliar with Python's `heapq` (min-heap only). Needed: a comment block at the method level referencing the HNSW paper's Algorithm 2, and an inline comment on the negation pattern and the early-exit condition.

---

### 4. `_detect_update_signal` (agentmemory/consolidation.py)

**What it does**: Scores a candidate memory string 0.0–1.0 for how strongly it signals an update or correction to an existing fact. Applies a weighted regex battery: explicit correction phrases ("actually", "correction:", "I meant") score high; negation patterns score medium; first-person state-change verbs score lower. The final score is a clipped weighted sum divided by a normalization constant.

**Existing comments**: None. The regex patterns are present but their semantic grouping and weight rationale are invisible.

**Adequacy**: Insufficient. The regex battery is the key heuristic separating legitimate knowledge updates from semantically-similar but non-updating memories. Without comments, future maintenance will introduce pattern collisions or unbalanced weights unknowingly. Needed: (a) group the patterns by intent with a comment header per group, (b) note the weight normalization ceiling, (c) explain why the threshold used in the caller is set where it is.

---

### 5. `consolidate_episodic_to_semantic` quality gating (agentmemory/consolidation.py)

**What it does**: When promoting a cluster of episodic memories into a single semantic summary, computes a "quality score" by evaluating the candidate summary node against: (a) centroid cosine similarity to all cluster members, (b) coverage fraction (how many cluster members are above a similarity threshold), (c) confidence of the node, and (d) importance. Rejects promotion if quality score is below a threshold, leaving the cluster in episodic tier.

**Existing comments**: Sparse. The four sub-components of the quality score are present in code but not named; the threshold constant is a magic number with no justification.

**Adequacy**: Insufficient. The multi-component quality gate determines whether expensive LLM-generated summaries are actually used. A magic-number threshold without explanation makes it impossible to tune this without empirical experimentation or source archaeology. Needed: named constants for the threshold and each weight, a comment explaining why centroid similarity alone is insufficient (coverage fraction catches fringe-cluster members), and a reference to the intended behavior when quality is low (fall-through to raw episodic storage).

---

## Section 5 — Benchmark Results Inventory

Every results file, progress file, and report file in the repository, noting which contain verified scores.

---

### `BENCHMARKS.md`

**Path**: `C:\Agentmemory V4\BENCHMARKS.md`
**Type**: Comprehensive benchmark documentation
**Contents**:
- Hardware spec (Intel Core i3-12100F, 16 GB DDR4, Windows 11 Pro)
- Internal latency suite: TF-IDF and Dense write/recall latency at 100/1K/5K memory scale (p50/p95)
- Retrieval fidelity benchmark (Precision@10, Recall@10)
- Consolidation efficiency benchmark (active count before/after, time, reduction %)
- LongMemEval full evaluation run history: v1–v3 iterative development results and the two stability runs
- Proxy results: LongMemEval 50-case proxy (used during development), LOCOMO F1 scores
- Competitive comparison table vs OMEGA, MemGPT, Zep, Mem0
- Complete reproduction instructions (dataset setup, API key env vars, command line)

**Verified scores recorded**:
- LongMemEval gpt-4.1 Run 1: **98.00%** (490/500) — verified
- LongMemEval gpt-4.1 Run 2: **97.40%** (487/500) — verified; stability spread ±0.60 pp
- OMEGA published baseline: **95.40%** (gpt-4o judge) — third-party reference
- Internal latency p50/p95: recorded 2026-03-17 with `all-MiniLM-L6-v2` — superseded by latency_results.md

---

### `stability_final_analysis.md`

**Path**: `C:\Agentmemory V4\stability_final_analysis.md`
**Type**: Stability verification report
**Contents**:
- Score comparison table across both gpt-4.1 runs (per question type)
- Stability verdict: ±0.60 pp overall — STABLE
- 6 systematic failure cases (wrong in both runs) with question IDs
- 11 stochastic failure cases (wrong in one run only) with question IDs
- Failure taxonomy: multi-session counting with ambiguous scope (4/6 systematic), temporal multi-hop arithmetic (2/6 systematic)
- Ranked optimization observations (marked "do not implement" — analysis only)

**Verified scores**:
- Overall range: **97.40%–98.00%** with gpt-4.1 judge, confirmed STABLE
- Per-type: knowledge-update 98.72%–100.00%, temporal-reasoning 97.74% (both runs), multi-session 93.23%–95.49%, SSU 100.00% (both), SSA 100.00% (both), SSP 96.67%–100.00%
- Token consumption: ~5.25M per run (vs ~850K original projection — projection needs updating)

---

### `longmemeval_4o_report.md`

**Path**: `C:\Agentmemory V4\longmemeval_4o_report.md`
**Type**: Single evaluation run report (GPT-4o judge)
**Contents**:
- Final score comparison table (this run, prior gpt-4.1 runs, OMEGA published)
- Per-type accuracy table (6 question types + overall)
- Run configuration (embedder, reranker, token budgets, total tokens)
- All 28 wrong cases with gold answer and system answer
- Analysis section: judge model impact, primary weakness areas

**Verified scores**:
- agentmemory V4 with gpt-4o judge: **94.40%** (472/500) — verified single run
- Gap vs OMEGA (same judge): **−1.00 pp**
- Gap vs gpt-4.1 runs: **−3.00 to −3.60 pp** (demonstrates judge-model sensitivity)
- Per-type: knowledge-update 100%, SSU 100%, SSA 98.21%, SSP 93.33%, TR 93.98%, MS 87.22%
- Abstention accuracy: 29/30 = 96.67%
- Total tokens: 5,186,133

---

### `latency_results.md`

**Path**: `C:\Agentmemory V4\latency_results.md`
**Type**: Latency benchmark re-run report (2026-03-21)
**Contents**:
- TF-IDF and Dense latency results at 100/1K/5K scale (write avg, recall mean/p95)
- Retrieval fidelity results (both modes)
- Consolidation efficiency (both modes)
- Temporal retrieval, conversation ingestion
- Comparison vs BENCHMARKS.md published figures
- Summary table of regressions and stable metrics

**Key findings — regressions vs published BENCHMARKS.md**:
- Dense embedder changed: `all-MiniLM-L6-v2` (384-dim, published) → `all-mpnet-base-v2` (768-dim, current); this is the root cause of most dense regressions
- Dense write latency: ~3× slower (260 ms avg at 5K vs 74 ms published)
- Dense recall latency: ~2× slower (136 ms at 5K vs 73 ms published)
- Dense fidelity: dropped from 3/3 to 1/3 (perfect → 0.333 P@10)
- TF-IDF fidelity: dropped from 2/3 to 1/3 (0.667 → 0.333 P@10) — cause unclear; possible scoring pipeline change or nondeterminism
- Dense consolidation: 81% reduction vs 96% published; 38 active remaining vs 8

**Stable metrics**:
- TF-IDF recall latency: within ±10% of published p50 at all scales
- TF-IDF consolidation: same result (1 active), +14% time
- Temporal ordering: recent event ranked first in both modes (both runs)
- Conversation ingestion: 9 memories extracted (vs 8 published), entity recall correct

---

### No additional results files found

No other `*_results.json`, `*_progress.*`, or `*_report.*` files were identified in the repository root or subdirectories outside `.venv/` and `.claude/`. The four files above constitute the complete benchmark documentation corpus.

---

## Section 6 — Existing README and Documentation Review

### README.md

**What is good**:
- Covers installation (pip install with extras), basic quick-start code example, and a feature overview list
- Links to BENCHMARKS.md for detailed performance data
- Includes the CLI subcommand overview (`serve`, `mcp`, `bench`, `import`, `export`, `inspect`)
- Mentions the server and MCP integration options

**What is missing**:
- No parameter reference for `MemoryStore.__init__` — the 15+ constructor parameters are undocumented
- No explanation of memory kinds (the 12-kind taxonomy) or when to choose each
- No explanation of memory tiers (WORKING/EPISODIC/SEMANTIC) and automatic promotion
- No documentation of `FilterExpr` / `FilterCondition` query DSL — the `query()` method is effectively unusable without examples
- No documentation of the event bus system or how to subscribe to memory events
- No documentation of `MemoryProfile` presets and what each configures
- No federation or migration documentation
- No documentation of bi-temporal fields (`event_time`, `valid_from`, `valid_until`) and when to set them
- No documentation of the GDPR pipeline, `DeletionReceipt`, or compliance workflow
- No framework integration examples (LangChain, LangGraph, OpenAI Assistants, CrewAI, Vercel AI SDK)
- No REST server endpoint reference (16 endpoints are undocumented outside the source)
- No MCP tool reference (11 tools are undocumented outside the source)
- No troubleshooting section for common issues (missing optional dependencies, PostgreSQL DSN format, async/sync mixing in Jupyter)

**What needs replacement or correction**:
- BENCHMARKS.md latency figures reference `all-MiniLM-L6-v2` as the dense embedder but the codebase now uses `all-mpnet-base-v2` by default — the published numbers are no longer reproducible with default settings. A prominent note must be added to both README.md and BENCHMARKS.md flagging this change and the resulting latency and fidelity deltas.
- The "zero mandatory dependencies" claim is accurate at install time but misleading for production use — dense retrieval (which drives the benchmark scores) requires `sentence-transformers`, and the REST server requires `fastapi` + `uvicorn`. These dependency tiers should be explained in the README with guidance on which extras are needed for which use cases.

### BENCHMARKS.md

**What is good**:
- Extremely thorough: hardware spec, exact command lines, per-run per-type score tables, judge model comparisons, proxy result methodology
- The competitive comparison table is well-structured with honest caveats (different judges, different datasets)
- Reproduction instructions include both dataset download steps and environment variable requirements

**What is missing / needs updating**:
- The default dense embedder change (`MiniLM` → `MPNet`) is documented in `latency_results.md` but not yet integrated into BENCHMARKS.md — the published latency table header should note the embedder used and add a dated addendum with the new measurements
- The TF-IDF fidelity regression (0.667 → 0.333 P@10) has no root cause — BENCHMARKS.md should flag this as an open investigation item rather than leaving readers to discover the discrepancy by cross-referencing `latency_results.md`
- The token consumption reality (~5.25M per LongMemEval run) vs the original budget projection (~850K) is noted only in `stability_final_analysis.md` — the cost projection in BENCHMARKS.md should be updated

### stability_final_analysis.md and longmemeval_4o_report.md

**What is good**:
- Both are internally consistent and clearly written
- Failure case listings with question IDs are actionable for future targeted improvements
- The judge-model sensitivity analysis in the 4o report is valuable methodological context

**What is missing**:
- These files are standalone; they are not linked from BENCHMARKS.md or README.md. A developer encountering the repo for the first time will not find them without exploring the directory listing.
- `stability_final_analysis.md` contains an "Observations for Future Optimization" section that would benefit from being tracked as issues rather than ephemeral markdown notes.

### latency_results.md

**What is good**:
- Explicitly calls out the embedder configuration change and attributes each regression to it
- The summary table at the end (STABLE / SLOWER / REGRESSION per area) is easy to scan

**What is missing**:
- No action items or next steps for the fidelity regressions — the report ends at observation without recommending investigation paths
- The Dense fidelity drop to 1/3 is described as possibly due to "nondeterminism in the ANN index" — this hypothesis is not tested and should be followed up with a controlled re-run using the same planted target texts

---

## Audit Summary

**Total files audited**: 36 Python source files + 5 documentation/config files = 41 files

**Highest-priority gaps identified**:

1. **Zero docstrings on all ~40 public methods in core.py** — the most-used file in the package has no inline API documentation. This is the single largest developer experience gap.

2. **`_sync` decorator has no explanatory comments** — the threading/asyncio boundary logic is critical and non-obvious; it is currently undocumented.

3. **Dense embedder change is not propagated to BENCHMARKS.md** — `latency_results.md` documents the `MiniLM → MPNet` switch and its regressions, but BENCHMARKS.md still presents the old latency figures as current, creating a misleading baseline.

4. **Five complex code sections lack adequate inline comments** — the six-signal scoring formula, HNSW layer traversal, `_detect_update_signal` regex battery, `consolidate_episodic_to_semantic` quality gate, and `_sync` decorator all contain non-obvious logic with no explanatory comments.

5. **README.md is missing documentation for half the API surface** — `FilterExpr` DSL, event bus, bi-temporal fields, federation, migration, GDPR pipeline, all framework integrations, and all REST/MCP endpoints are absent.
