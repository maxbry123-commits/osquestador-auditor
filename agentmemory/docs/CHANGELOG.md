# Changelog

All notable changes to agentmemory are documented in this file.

## [4.0.0] — 2026-03-21

### Benchmark Results
- **98.0% on LongMemEval** (GPT-4.1 judge, peak across 3 independent runs)
- **97.8% mean** (3 GPT-4.1 runs: 98.0%, 98.0%, 97.4%, ±0.60 pp variance — STABLE)
- **94.4% on LongMemEval** (GPT-4o judge, 1 run)
- **Sub-115ms recall latency** at 1,000 memories (dense mode)
- Beats OMEGA published score of 95.4% (GPT-4.1 judge: +2.0 to +2.6 pp)

### New Features
- **Adaptive retrieval weight learning** — EMA-based signal weight adaptation from quality feedback
- **Temporal fact validity windows** — `valid_from`/`valid_until` fields with automatic expiry filtering
- **Confidence calibration** — Bayesian feedback loop updating calibration curves per confidence bucket
- **Document ingestion** — Semantic chunking pipeline for long-form content via `ingest_document()`
- **Memory profiles** — Named use-case presets: `default`, `summarizer`, `coding_assistant`, `support_agent`, `research_agent`
- **Postgres storage backend** — Production-scale `asyncpg` backend with GIN-indexed FTS
- **Consolidation quality scoring** — Centroid similarity gate before episodic→semantic promotion
- **Memory lineage API** — Full audit chain reconstruction via `lineage(node_id)`
- **Multi-modal memory support** — CLIP (image) and Whisper (audio) embeddings
- **Cross-encoder reranking** — Optional `cross-encoder/ms-marco-MiniLM-L-6-v2` reranker
- **Query expansion** — Synonym groups, entity normalization, and question reformulation
- **Hierarchical conversation extraction** — Three-pass extractor for deep preference/entity capture
- **TemporalGrounder** — Resolves 30+ relative date patterns to Unix timestamps

### Architecture
- Six-signal hybrid retrieval: semantic cosine, lexical BM25, activation, graph spreading activation, importance×confidence, temporal Gaussian
- Three-tier cognitive memory model: Working → Episodic → Semantic
- Pure-Python HNSW approximate nearest neighbor index (thread-safe, O(log n) queries)
- Async-first API with sync wrappers for all primary operations
- Zero required dependencies — TF-IDF mode ships with no external packages

### Bug Fixes (from V3)
- Fixed async `auto_link_node` with edge persistence
- Fixed `_ensure_init` race condition via `asyncio.Lock` double-checked locking
- Fixed validation using pre-loaded nearby nodes (eliminates storage round-trip per write)
- Fixed importance evolver passed to consolidation engine
- Fixed contradiction edges only added when LLM/heuristic resolution fails

## [3.0.0] — 2025

- Streaming consolidation: on-write near-duplicate and contradiction detection
- Knowledge graph with spreading activation retrieval
- WriteValidator with constitutional rules
- EventBus pub/sub for MEMORY_CREATED, PROACTIVE_SURFACE, CONTRADICTION_DETECTED events
- GDPR pipeline with verifiable DeletionReceipt
- Federation across multiple MemoryStore instances

## [2.0.0] — 2025

- HNSW approximate nearest neighbor index
- Hybrid TF-IDF + dense embedding retrieval
- SQLite WAL-mode backend with FTS5
- Framework integrations: LangChain, LangGraph, OpenAI, CrewAI, Vercel AI

## [1.0.0] — 2025

- Initial release
- Basic add/recall with TF-IDF embeddings
- SQLite persistence
- Sync API
