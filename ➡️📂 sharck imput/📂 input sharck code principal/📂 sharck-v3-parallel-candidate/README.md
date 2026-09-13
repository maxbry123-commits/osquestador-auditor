# SHARCK INPUT V3 — Parallel 11-Lane Candidate

**Status:** `SANDBOX_CANDIDATE / NOT_PRODUCTION_WIRED`  
**Purpose:** upgrade SHARCK INPUT V2.1 into a continuous, evidence-first PRE-LLM context harness without replacing the immutable canonical acquisition motors or opening production gates.

## Bootstrap then parallel

Only two deterministic operations precede fan-out: `INPUT_RAW → INPUT_LOCK → literal decomposition`. Immediately after, all 11 LaneKernels start with `asyncio.create_task()` against the same immutable `InputSpec`:

1. research — advanced official/community research
2. skills — >=3 libraries, >=20 metadata reads, max 3 full activations
3. datasets — >=3 active, 5 standby
4. adapters — >=3 active, 5 standby
5. tools_plugins — capability/transport/auth/schema usage plan
6. persistence_loop — 12 input/output goals, 12 council checks, 3 refutations, 4 simulations
7. evidence_validator — official + forum + community + blog + YouTube/social evidence; 10 alternatives ranked by friction/time/overengineering/evidence
8. error_lens — negative reports, regressions, pitfalls, breaking changes
9. solution_guides — manuals, install guides, runbooks, troubleshooting
10. multi_shark — counter-routes, newer/older versions, simpler alternatives, refutation
11. anti_hallucination — literal INPUT checklist + final deterministic alignment gate

A 12th supporting task `continuous_research` runs concurrently and emits context deltas.

## Universal harness

The runtime uses protocols instead of 11 unrelated mini operating systems: `SearchProvider`, `CatalogProvider`, `DownloadEngine`, `LaneKernel`, `RunLedger`, `LiteralAlignmentJudge`. Each lane is an independent kernel/task with its own result, candidates, gaps and evidence, but shares a bounded router, dedup and append-only ledger.

## Parallel search router

`ParallelRouter` supports 10..100 search jobs per research round with:
- bounded concurrency
- timeout
- in-flight deduplication
- fan-out/fan-in
- provider errors returned as data (fail closed)

`provider_adapters.py` adds a local router and a web API router. The web router reads up to 100 API keys from `SHARCK_WEB_API_KEY_01..100`; secrets are never written to memory/profile/handoff.

## Acquisition / extraction bridge

No new unsafe downloader is introduced. `QueueDownloadEngine` writes traceable per-lane acquisition requests under `RUN/artifacts/acquisition-requests/`. Requests require source pin, license and readback. `publish=false` in the candidate. The existing immutable canonical Motor 2 remains the physical acquisition authority.

## Per-job persistence

Every run creates:
- `INPUT_RAW.txt` + SHA256 lock
- `input_spec.json`
- `evidence-ledger.jsonl`
- `profile.json`
- `memory.md`
- `HANDOFF.md`
- `handoff-index.json`
- `CONTEXT_PACKAGE.json`
- `lane-results.json`
- optional `artifacts/acquisition-requests/*.json`

`handoff_index.py` is an executable lookup tool over prior pointers so a resumed job can reuse already-fetched evidence instead of starting the search from zero.

## Fail-closed final gate

`CONTEXT_READY` requires all 11 mandatory lanes PASS, non-empty evidence, and final literal goal→evidence alignment PASS. Otherwise verdict is `CONTEXT_GAP_LOOP`. Structural lane completion alone cannot release context.

## Tests

Local deterministic tests currently prove:
- 11-lane contract and required run artifacts
- concurrent start (not serial)
- skill gate: <3 libraries fails
- acquisition bridge: pinned+licensed is request-ready; missing pin/license stays blocked
- anti-hallucination gate rejects unrelated context
- HF skills, Zenodo, Data.gov and MCP registry parsers with fixtures
- API-key pool only reads configured environment variables

Live public-provider smoke from the local sandbox is **not PASS** because that sandbox cannot resolve external hosts (`URLError`). This is preserved as an infrastructure GAP, not hidden.
