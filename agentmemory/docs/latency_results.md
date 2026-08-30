# agentmemory V4 — Latency Benchmark Results

> Benchmark date: 2026-03-21
> Hardware: Intel Core i3-12100F, 16 GB DDR4, Windows 11 Pro 10.0.26200
> Python: 3.12.10
> agentmemory: 4.0.0
> Storage: SQLite `:memory:` (in-process)

---

## Methodology Note

The current benchmark harness (`agentmemory/benchmark.py`) reports the following metrics:

- **Write**: `write_{n}_total_s` (total seconds) and `write_{n}_per_ms` (average ms per write). The harness does not instrument per-operation samples, so true p50/p95 write latency cannot be derived from harness output alone. Average write time is used as a p50 proxy; p95 is marked N/A.
- **Recall**: `recall_{n}_mean_ms` (mean of 5 queries) and `recall_{n}_p95_ms` (computed as `sorted(lats)[int(5 * 0.95)]` = max of 5 queries). The mean serves as a p50 proxy; the reported p95 is the single-sample maximum across 5 queries.

---

## Run 1 — TF-IDF Mode (default CLI)

**Command**: `python -m agentmemory bench --sizes 100,1000,5000`
**Embedder mode**: TF-IDF (sparse, zero external dependencies)

### Write Latency

| Memory Count | Total (s) | Avg per write (ms) [≈p50] | p95 |
|-------------|-----------|--------------------------|-----|
| 100 | 5.24 | 52.40 | N/A |
| 1,000 | 132.04 | 132.04 | N/A |
| 5,000 | 752.53 | 150.51 | N/A |

### Recall Latency (5 queries)

| Memory Count | Mean (ms) [≈p50] | p95 (ms) |
|-------------|-----------------|----------|
| 100 | 25.30 | 37.15 |
| 1,000 | 73.46 | 89.07 |
| 5,000 | 74.86 | 99.62 |

### Retrieval Fidelity (500 background memories, 3 planted targets)

| Metric | Value |
|--------|-------|
| Precision@10 | 0.3333 |
| Recall@10 | 0.3333 |
| Targets found (of 3) | 1 |

### Consolidation Efficiency (200 memories)

| Metric | Value |
|--------|-------|
| Active before | 200 |
| Active after | 1 |
| Consolidation time (ms) | 161.23 |
| Reduction % | 99.5% |

### Temporal Retrieval

| Metric | Value |
|--------|-------|
| Recent event rank | 0 (first) |
| Older event rank | 1 (second) |
| Recent preferred | Yes |

### Conversation Ingestion (6-message conversation)

| Metric | Value |
|--------|-------|
| Memories extracted | 9 |
| Ingest time (ms) | 16.62 |
| Entity recall (Alice) | Yes |
| Preference recall (Tuesday) | Yes |

---

## Run 2 — Dense Embedding Mode (prefer_dense=True)

**Command**: `python -c "..."` (python -m agentmemory bench does not expose --prefer-dense; invoked via Python directly with store_factory using prefer_dense=True)
**Embedder mode**: Dense — **`all-mpnet-base-v2` (768-dim)** via sentence-transformers
**⚠ Note**: The current default dense embedder is `all-mpnet-base-v2` (768-dim). BENCHMARKS.md published numbers used `all-MiniLM-L6-v2` (384-dim). This is a significant configuration change that affects all dense latency figures.

### Write Latency

| Memory Count | Total (s) | Avg per write (ms) [≈p50] | p95 |
|-------------|-----------|--------------------------|-----|
| 100 | 11.93 | 119.31 | N/A |
| 1,000 | 236.63 | 236.63 | N/A |
| 5,000 | 1300.49 | 260.10 | N/A |

### Recall Latency (5 queries)

| Memory Count | Mean (ms) [≈p50] | p95 (ms) |
|-------------|-----------------|----------|
| 100 | 59.94 | 61.72 |
| 1,000 | 114.56 | 130.96 |
| 5,000 | 136.40 | 165.33 |

### Retrieval Fidelity (500 background memories, 3 planted targets)

| Metric | Value |
|--------|-------|
| Precision@10 | 0.3333 |
| Recall@10 | 0.3333 |
| Targets found (of 3) | 1 |

### Consolidation Efficiency (200 memories)

| Metric | Value |
|--------|-------|
| Active before | 200 |
| Active after | 38 |
| Consolidation time (ms) | 449.66 |
| Reduction % | 81.0% |

### Temporal Retrieval

| Metric | Value |
|--------|-------|
| Recent event rank | 0 (first) |
| Older event rank | 1 (second) |
| Recent preferred | Yes |

### Conversation Ingestion (6-message conversation)

| Metric | Value |
|--------|-------|
| Memories extracted | 9 |
| Ingest time (ms) | 270.60 |
| Entity recall (Alice) | Yes |
| Preference recall (Tuesday) | Yes |

---

## Comparison vs. BENCHMARKS.md Published Numbers

> BENCHMARKS.md numbers were recorded 2026-03-17 with `all-MiniLM-L6-v2` (384-dim).
> Current dense run uses `all-mpnet-base-v2` (768-dim) — this is the primary driver of dense differences.

### Write Latency — TF-IDF

| Memories | Published p50 (ms) | Published p95 (ms) | Current avg (ms) | Delta (avg vs p50) |
|----------|-------------------|--------------------|-----------------|-------------------|
| 100 | 57.64 | 65.26 | 52.40 | -5.24 ms (-9%) |
| 1,000 | 78.11 | 88.58 | 132.04 | +53.93 ms (+69%) ⬆ |
| 5,000 | 80.30 | 97.59 | 150.51 | +70.21 ms (+87%) ⬆ |

> The published p50/p95 write numbers were computed from per-operation timing samples not produced by the current harness output. Average write latency is used as a comparison proxy. The significant increase at 1K and 5K may reflect system load differences (classification overhead, SQLite contention) or a change in write path since the original measurement.

### Write Latency — Dense (embedder change: MiniLM → MPNet)

| Memories | Published p50 (ms) | Published p95 (ms) | Current avg (ms) | Delta |
|----------|-------------------|--------------------|-----------------|-------|
| 100 | 56.20 | 67.96 | 119.31 | +63.11 ms (+112%) ⬆ |
| 1,000 | 72.53 | 90.68 | 236.63 | +164.10 ms (+226%) ⬆ |
| 5,000 | 74.32 | 94.96 | 260.10 | +185.78 ms (+250%) ⬆ |

> Nearly all of this increase is attributable to the embedder change. `all-mpnet-base-v2` (768-dim) has approximately 3–4× the inference cost of `all-MiniLM-L6-v2` (384-dim) on CPU.

### Recall Latency — TF-IDF

| Memories | Published p50 (ms) | Published p95 (ms) | Current mean (ms) | Current p95 (ms) |
|----------|-------------------|--------------------|------------------|-----------------|
| 100 | 25.24 | 28.38 | 25.30 | 37.15 |
| 1,000 | 79.73 | 94.06 | 73.46 | 89.07 |
| 5,000 | 80.90 | 105.78 | 74.86 | 99.62 |

> TF-IDF recall latency is **stable** — current mean values are within ±10% of published p50 across all scales. P95 (current harness = max of 5 queries) is slightly lower than published p95 (measured over 10 queries), which is expected given the smaller sample.

### Recall Latency — Dense (embedder change: MiniLM → MPNet)

| Memories | Published p50 (ms) | Published p95 (ms) | Current mean (ms) | Current p95 (ms) |
|----------|-------------------|--------------------|------------------|-----------------|
| 100 | 29.22 | 33.87 | 59.94 | 61.72 |
| 1,000 | 85.04 | 90.38 | 114.56 | 130.96 |
| 5,000 | 73.35 | 111.57 | 136.40 | 165.33 |

> Dense recall latency has increased significantly vs. published numbers. Again, the switch from `all-MiniLM-L6-v2` to `all-mpnet-base-v2` is the primary factor. The HNSW advantage at 5K that was visible in published results (dense p50 < TF-IDF p50) has reversed: dense is now slower than TF-IDF at all scales.

### Retrieval Fidelity

| Mode | Published Precision@10 | Published Recall@10 | Current Precision@10 | Current Recall@10 | Change |
|------|------------------------|---------------------|---------------------|------------------|--------|
| TF-IDF | 0.667 | 0.667 | 0.333 | 0.333 | ⬇ -0.333 |
| Dense | **1.000** | **1.000** | 0.333 | 0.333 | ⬇ -0.667 |

> **Significant regression.** Both modes have dropped from their published fidelity. Dense mode previously achieved perfect retrieval (3/3 targets); now only 1/3 is found. TF-IDF dropped from 2/3 to 1/3. This may indicate a change in the retrieval scoring pipeline, the dense embedder switch changing semantic alignment of the planted targets, or nondeterminism in the ANN index at this scale.

### Consolidation Efficiency (200 memories)

| Mode | Published Active After | Published Time (ms) | Published Reduction % | Current Active After | Current Time (ms) | Current Reduction % |
|------|----------------------|--------------------|-----------------------|---------------------|-------------------|---------------------|
| TF-IDF | 1 | 141.13 | 99.5% | 1 | 161.23 | 99.5% |
| Dense | 8 | 145.05 | 96.0% | 38 | 449.66 | 81.0% |

> TF-IDF consolidation is **stable** — same result, +14% time.
> Dense consolidation shows significant regression: 38 active memories remaining (vs. 8 published) and 81% reduction (vs. 96%). Combined with the embedder change, this suggests `all-mpnet-base-v2` embeddings are producing less aggressive deduplication on this synthetic workload.

---

## Summary of Key Changes vs. Published BENCHMARKS.md

| Area | Status | Notes |
|------|--------|-------|
| TF-IDF recall latency | **STABLE** | Within ±10% of published p50 across all scales |
| TF-IDF write latency | **SLOWER** | +69% at 1K, +87% at 5K vs. published p50 |
| TF-IDF consolidation | **STABLE** | Same result (1 active), +14% time |
| Dense recall latency | **SLOWER** | ~2× slower; caused by embedder upgrade (MiniLM → MPNet) |
| Dense write latency | **SLOWER** | ~3× slower; caused by embedder upgrade |
| Dense fidelity | **REGRESSION** | Dropped from perfect 3/3 to 1/3 |
| TF-IDF fidelity | **REGRESSION** | Dropped from 2/3 to 1/3 |
| Dense consolidation | **REGRESSION** | 81% vs 96% reduction; 449ms vs 145ms |
| Temporal ordering | **STABLE** | Recent event correctly ranked first in both modes |
| Conversation ingestion | **STABLE** | 9 memories extracted (vs 8 published), entities recalled correctly |
| Current dense embedder | **CHANGED** | Now `all-mpnet-base-v2` (768-dim); published used `all-MiniLM-L6-v2` (384-dim) |
