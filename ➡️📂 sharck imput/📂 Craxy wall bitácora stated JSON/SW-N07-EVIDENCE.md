# SW-N07 EVIDENCE — COMPONENT → PORT → ADAPTER → FAILURE → TEST MATRIX

- schema: `sharck-input.swarm-node-evidence.v1`
- agent_name: `SOL-2-GPT`
- chat_id: `chat-sol2-20260912T2306-0500`
- node_id: `SW-N07`
- parent_node: `M47_8SOL_SWARM_CONTROL_PLANE`
- mode: `READ_ONLY_ARCHITECTURE`
- claim_commit: `002cfa814ce23bb14777615673b30664ae9c3638`
- claim_blob: `e3b10fac1bdcb0728a0b2f4fe66aefd202b8947d`
- base_sha: `8fa359c9684e01dd37134e66d1379df66265ed14`
- fresh_head_before_evidence_write: `7ec9bec5c4839f3c57d219514048668f7cfc8608`
- stale-head revalidation: `PASS`; intervening `SW-N08` claim is a disjoint SOL-1 path.
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- production_wiring_performed: `false`

## Assertion under test

> Current verified components and approved candidates can be mapped to V2.1 microkernel ports without wiring production.

### Fail-closed correction to the assertion

The mapping is possible, but the phrase **approved candidates** cannot be promoted beyond current physical authority:

- the 17 successful B01-B04 acquisitions are `VERIFIED_CLOSED` for acquisition/read-back, **not** `APPROVED_FOR_WIRE`;
- the 20X set is `RESEARCHED_CANDIDATE_NO_DOWNLOAD / REVIEW_GATE_REQUIRED`, not physically acquired or review-approved.

Therefore this node produces **architecture contracts only**. It does not wire, acquire, activate, or promote any component.

## STEP 1 — SYNC / VERIFY / CLAIM

Atomic claim was created and read back at:

`➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/swarm-claims/CLAIM-SW-N07.json`

Sources read fresh:

- V2.1 architecture and pipeline.
- code-root README and integration-state semantics.
- canonical 117-component index.
- B01-B04 acquisition state.
- 20X candidate plan.
- M47 DAG/queue/gates.

V2.1 base microkernels preserved:

`input_lock`, `focus`, `questions`, `role_router`, `geo_language`, `query_lattice`, `community`, `github`, `huggingface`, `labs`, `youtube`, `capture`, `extract`, `index`, `dedup`, `code_pointer`, `skill_pointer`, `tool_finder`, `evidence`, `gap_loop`, `context_compiler`, `checkpoint`, `verdict`.

V2.1 candidate ports preserved:

`capture.warc`, `provenance.lineage`, `observability.otel`, `policy.engine`, `supply_chain.sbom`, `supply_chain.vuln`, `supply_chain.secrets`, `structured_output`, `evidence.compute`, `evidence.rules`, `llm_policy_eval`.

### GOALS12_INPUT

| Goal | Verdict |
|---|---|
| G01 literal requirement preserved | PASS |
| G02 fresh HEAD read | PASS |
| G03 Handoff/STATE/CHECKPOINT/PLAN/Watchdog/DAG read | PASS |
| G04 owner free / claim valid | PASS |
| G05 gates permit read-only architecture only | PASS |
| G06 write scope isolated | PASS |
| G07 physical components/candidates deduplicated | PASS |
| G08 delta is evidence-only | PASS |
| G09 adapter-specific test contracts required | PASS |
| G10 3 simulations + 3 refutations required | PASS |
| G11 SHA/readback | POST_WRITE |
| G12 release/fan-in | POST_WRITE |

## STEP 2 — EXECUTE / VERIFY

## A. Physical acquisition-verified set — 17 components

Physical B01-B04 accounting is `17 VERIFIED_CLOSED / 23 FAILED`. The 17 acquisition-verified components are mapped below. `VERIFIED_CLOSED` here means upstream acquisition/extraction/read-back closed; it does **not** mean wired or runtime-active.

| Component | Capability | V2.1 port/microkernel | Minimal adapter contract | Failure contract | Test contract | Wiring decision now |
|---|---|---|---|---|---|---|
| Scrapy | programmable crawl/capture | `capture` | `capture(request)->CapturedSource` | timeout/robots/parser/network => explicit capture GAP | `T-CAP-01` fixed local HTTP fixture, content+metadata hash | `CONTRACT_READY / NO_WIRE` |
| Trafilatura | HTML main-text/metadata extraction | `extract` | `extract(CapturedSource)->NormalizedDocument` | empty/low-confidence extraction => no silent success | `T-EXT-01` fixed HTML fixtures + expected text/metadata hashes | `CONTRACT_READY / NO_WIRE` |
| MinerU | complex document/OCR extraction | `extract` | MIME-routed document extractor | unsupported/corrupt/OCR uncertainty => typed failure | `T-EXT-02` pinned PDF fixture, structure/page-count/text assertions | `CONTRACT_READY / NO_WIRE` |
| Lucene | sparse/BM25 index | `index` | `build/query(IndexDocument|Query)->RankedHits` | index corruption/version/query failure => GAP | `T-IDX-01` fixed corpus + deterministic top-k/score-order assertions | `ALT_ENGINE / NO_WIRE` |
| PyTerrier | IR pipeline/evaluation | `index` + `evidence` | evaluation adapter over immutable query/run sets | run/corpus mismatch => evaluation invalid | `T-IR-01` fixed qrels + ranking metrics | `EVAL_ADAPTER / NO_WIRE` |
| Tantivy | sparse full-text index | `index` | same sparse-index port as Lucene | schema/index mismatch => GAP | `T-IDX-02` same fixture corpus used against Lucene contract | `ALT_ENGINE / NO_WIRE` |
| RDFLib | RDF/provenance graph | `evidence` | `evidence_graph.add/query/serialize` | malformed graph/provenance loss => reject | `T-EVG-01` round-trip triples + source pointers + canonical serialization | `CONTRACT_READY / NO_WIRE` |
| RapidFuzz | deterministic fuzzy/entity matching | `dedup` / entity-resolution stage | `match(candidates)->scored_matches` | threshold ambiguity => unresolved entity, never forced match | `T-DEDUP-01` fixed aliases, thresholds, tie/negative cases | `CONTRACT_READY / NO_WIRE` |
| open-codebase-index | code search/call-graph/MCP | `code_pointer` + `index` | `locate_code(query)->CodePointers` | stale/incomplete index => pointer GAP | `T-CODE-01` fixture repo symbols/calls/path+commit assertions | `COMPARE_WITH_SOURCEBOT / NO_WIRE` |
| Sourcebot | multi-repo code search | `code_pointer` + `github` | provider behind same `CodePointerPort` | repo unavailable/stale revision => explicit source GAP | `T-CODE-02` same fixture repos + exact path/ref readback | `COMPARE_WITH_OPEN_CODEBASE_INDEX / NO_WIRE` |
| Hugging Face Datasets | dataset discovery/load/stream | `huggingface` | `dataset_pointer/load_stream` with immutable repo/revision pointer | missing revision/schema/network => no context promotion | `T-HF-01` pinned tiny dataset revision + row/schema/hash checks | `CONTRACT_READY / NO_WIRE` |
| HF MCP Server | HF tool/resource exposure | `huggingface` + `tool_finder` | MCP adapter returns pointers/capabilities, not hidden authority | tool discovered but unavailable => `TOOL_NOT_OPERATIONAL` | `T-HF-02` list→invoke read-only fixture + capability/readback | `CONTRACT_READY / NO_WIRE` |
| LLMLingua | context compression | `context_compiler` | `compress(ContextPackage)->ContextPatch` preserving source pointers | evidence/pointer loss or budget violation => reject compressed result | `T-CTX-01` invariant pointers + required facts retained + size budget | `OPTIONAL / NO_WIRE` |
| MarkItDown | document→Markdown normalization | `extract` | MIME-routed normalization adapter | unsupported/lossy parse => explicit fallback | `T-EXT-03` Office/PDF fixture → normalized Markdown assertions | `ROUTED_ALTERNATIVE / NO_WIRE` |
| Chonkie | semantic/light chunking | `extract`→`index` boundary | `chunk(NormalizedDocument)->Chunks` with source spans | orphan/overlap/source-span loss => reject | `T-CHUNK-01` full coverage/no orphan + stable source spans | `CONTRACT_READY / NO_WIRE` |
| Ragas | retrieval/context evaluation | `evidence` | advisory evaluator emits metrics/evidence only | evaluator error => no PASS mutation | `T-EVAL-01` known good/bad retrieval fixture + metric direction checks | `ADVISORY_ONLY / NO_WIRE` |
| DeepEval | evaluation framework | `evidence` | advisory test/eval adapter | evaluator result cannot set `verdict` directly | `T-EVAL-02` deterministic mocked cases + authority-boundary assertion | `ADVISORY_ONLY / NO_WIRE` |

### Physical alternatives / routing rules

1. `Lucene` and `Tantivy` implement the same sparse-index capability. Do not activate both by default. Run one shared benchmark contract and select/profile explicitly.
2. `open-codebase-index` and `Sourcebot` overlap at `code_pointer`. Do not fan-out both by default; select primary/fallback after correctness/freshness/cost test.
3. `Trafilatura`, `MinerU`, and `MarkItDown` are MIME/domain-routed extractors, not a mandatory three-stage chain.
4. `Ragas` and `DeepEval` are advisory. Neither can write deterministic `verdict=PASS`.
5. `LLMLingua` acts only on derived working context. It must never mutate `INPUT_RAW`/`INPUT_LOCK` or erase evidence pointers.
6. `hf-mcp-server` exposes tools/pointers; it does not replace `datasets`, and it does not make failed `huggingface_hub` acquisition magically verified.

## B. 20X candidate contract matrix — 20/20, NO DOWNLOAD

All entries below remain `RESEARCHED_CANDIDATE_NO_DOWNLOAD`. A port mapping is a design hypothesis, not an acquisition approval.

| Candidate | Proposed V2.1 port | Adapter/failure contract | Test contract | Overlap/pruning verdict now |
|---|---|---|---|---|
| Browsertrix Crawler | `capture.warc` | browser crawl → WARC pointer; incomplete/timeout capture => GAP | `T-WARC-01` fixed local dynamic site, WARC record count/hash/replay | `KEEP_CONTRACT`; overlaps Firecrawl/Crawl4AI/browser tooling but adds reproducible WARC |
| warcio | `capture.warc` | WARC read/write/inspect; malformed record/hash mismatch => reject | `T-WARC-02` write→read round-trip with fixed payload/hash | `KEEP_CONTRACT`, complementary to Browsertrix |
| ArchiveBox | `capture`/snapshot | snapshot pointer set; nondeterministic/missing artifacts => GAP | `T-SNAP-01` fixed local site snapshot manifest/readback | `DEFER`; overlaps existing capture stack + Browsertrix/warcio |
| OpenLineage | `provenance.lineage` | emit source→retrieval→claim→package lineage; missing parent/ref => reject event | `T-LIN-01` deterministic DAG lineage round-trip | `KEEP_CONTRACT` |
| Marquez | `provenance.lineage` backend | optional lineage query store; backend outage must not fabricate lineage | `T-LIN-02` ingest/query OpenLineage fixture | `DEFER`; local ledger/OpenLineage may be sufficient |
| OpenTelemetry Collector | `observability.otel` | traces/metrics/logs only; exporter failure cannot alter evidence verdict | `T-OTEL-01` node trace contains IDs/latency/errors and no secrets | `KEEP_CONTRACT` |
| OPA | `policy.engine` | deterministic allow/deny; engine unavailable => default deny for gated action | `T-POL-01` allow/deny/unknown fixtures | `SELECT_ONE_REQUIRED` vs Cedar |
| Cedar | `policy.engine` | typed authorization; parse/unavailable => default deny | `T-POL-02` same policy corpus mapped to Cedar semantics | `SELECT_ONE_REQUIRED` vs OPA |
| Syft | `supply_chain.sbom` | acquired tree→SBOM pointer/hash; generation gap blocks promotion requiring SBOM | `T-SBOM-01` known fixture dependency inventory | `KEEP_CONTRACT` |
| Grype | `supply_chain.vuln` | SBOM/filesystem→findings; DB unavailable/stale => scanner GAP | `T-VULN-01` seeded known-vulnerable fixture | `PRUNE_REQUIRED` with Trivy/OSV |
| Trivy | `supply_chain.vuln` | vuln/misconfig/SBOM scan; unavailable DB/module => explicit GAP | `T-VULN-02` same seeded fixture + mode-specific output | `PRUNE_REQUIRED`; overlaps Syft/Grype/secrets/licensing |
| OSV-Scanner | `supply_chain.vuln` | lockfile/dependency→OSV findings; unsupported ecosystem => typed GAP | `T-VULN-03` pinned lockfile with known OSV case | `KEEP_OR_COMPLEMENT_AFTER_M08`; dependency-focused |
| Gitleaks | `supply_chain.secrets` | source tree→secret findings; any raw secret must be redacted from evidence/logs | `T-SEC-01` synthetic fake-secret fixture + redaction assertion | `KEEP_CONTRACT` |
| Instructor | `structured_output` | model output→typed object through existing schema authority | `T-STRUCT-01` valid/invalid/nested schema cases against Pydantic baseline | `DEFER_SELECT`; overlaps Pydantic/JSON Schema/Guardrails/LMQL |
| DSPy | `llm_policy_eval` | optimization/eval result is advisory only | `T-DSPY-01` optimized score cannot mutate deterministic verdict | `DEFER_ADVISORY`; overlaps eval layer partially |
| LMQL | `structured_output` | constrained generation; constraint failure => reject result | `T-STRUCT-02` fixed constraint corpus vs baseline | `DEFER_SELECT`; overlap gate |
| Guardrails | `structured_output` | validation/reask layer; failure must remain schema failure | `T-STRUCT-03` same invalid payload corpus vs Pydantic/Instructor | `DEFER_SELECT`; overlap gate |
| DuckDB | `evidence.compute` | immutable snapshot/Parquet→query result + query provenance | `T-COMP-01` fixed Parquet aggregate/join expected result/hash | `KEEP_POC`; compare/complement Polars |
| Polars | `evidence.compute` | columnar normalize/dedup/stats; schema/type mismatch => explicit failure | `T-COMP-02` fixed frame normalize/dedup/stat result | `KEEP_POC`; compare/complement DuckDB |
| Soufflé | `evidence.rules` | evidence facts→deterministic derived contradiction/dependency facts | `T-RULE-01` fixture contradiction/coverage rules + negative cases | `KEEP_CONTRACT` |

## C. Port-level minimum contract

Every adapter, existing or candidate, must obey the same boundary:

`INPUT(pointer + immutable metadata) → ADAPTER → TYPED RESULT OR TYPED FAILURE → EVIDENCE POINTER → NO DIRECT VERDICT AUTHORITY`

Required adapter envelope:

- `adapter_id`
- `capability`
- `port`
- `input_pointer`
- `source_ref/source_commit` when external source is used
- `result_pointer`
- `evidence_hash`
- `failure_code`
- `latency/attempt metadata`
- `no_secret_value`

A provider may propose evidence; only deterministic runtime/gates can authorize promotion.

## D. Minimal wiring candidate matrix after future gates

This is sequencing guidance only, not authorization.

1. **Capture lane**: `capture` primary existing adapter + optional `capture.warc` Browsertrix→warcio pair after gate; ArchiveBox remains defer unless a snapshot capability gap survives comparison.
2. **Extract lane**: router by MIME/content → Trafilatura / MarkItDown / MinerU; Chonkie only after normalized document with source spans.
3. **Sparse index lane**: one selected `SparseIndexPort` implementation (`Lucene` or `Tantivy`) + PyTerrier evaluation adapter; no duplicate default indexing.
4. **Code pointer lane**: select `open-codebase-index` or `Sourcebot` primary; second may be fallback only with explicit freshness/cost policy.
5. **HF lane**: datasets pointer/stream + hf-mcp tool exposure; failed huggingface_hub remains fail-closed until its independent acquisition gap is reviewed.
6. **Evidence lane**: RDFLib graph; Ragas/DeepEval advisory; future DuckDB/Polars compute and Soufflé rules only after candidate gates.
7. **Context lane**: LLMLingua optional derived-context compressor, preserving source/evidence pointers.
8. **Control/supply-chain lane**: future OPA-or-Cedar, OTel, Syft, Gitleaks, selected vuln scanners; no candidate gets direct PASS authority.

## E. Explicit NO-OP / DEFER / REJECT cases

- `NO-OP`: do not create a second acquisition engine, second source-of-truth, or provider-specific logic inside Core.
- `NO-OP`: do not wire a component merely because its acquisition is `VERIFIED_CLOSED`.
- `NO-OP`: do not download any of 20X while `b05_b06_download_allowed=false`.
- `NO-OP`: do not use `huggingface_hub` or `unstructured` as wired providers while their acquisition state is failed.
- `DEFER`: ArchiveBox until Browsertrix/warcio + existing capture stack leave a demonstrated snapshot gap.
- `DEFER`: Marquez unless local ledger/OpenLineage queryability proves insufficient.
- `DEFER/SELECT_ONE`: OPA vs Cedar.
- `DEFER/PRUNE`: Grype vs Trivy vs OSV composition; avoid three scanners for the same contract without incremental evidence.
- `DEFER/SELECT`: Instructor vs Guardrails vs LMQL against existing Pydantic/JSON Schema/Outlines/Guidance baseline.
- `DEFER/COMPARE`: Lucene vs Tantivy and open-codebase-index vs Sourcebot before runtime activation.
- `REJECT`: any adapter design that bypasses evidence ledger, erases source commit/pointer, logs secret values, or writes `verdict=PASS` from an LLM/evaluator.

## STEP 3 — TEST / REFUTE / REPORT

### Static architecture checks

1. `PORT_COVERAGE_CHECK`: all 17 acquisition-verified components have capability→port→adapter→failure→test mapping.
2. `CANDIDATE_CONTRACT_CHECK`: all 20 20X candidates have a port, failure behavior, test ID, and overlap/pruning disposition.
3. `AUTHORITY_BOUNDARY_CHECK`: no adapter or evaluator has direct deterministic PASS authority.
4. `GATE_CHECK`: no production wiring/download/repair requested while physical gates remain false.
5. `OVERLAP_CHECK`: mutually overlapping engines are marked route/select/prune/defer rather than simultaneously activated.

### 3 simulations

**SIM-1 — web research path**

Hypothesis only: local fixture → Scrapy `capture` → Trafilatura `extract` → Chonkie chunking → selected Lucene-or-Tantivy `index` → RDFLib evidence pointer → context package.

Expected: each transition keeps source pointer/hash; any adapter failure returns typed GAP; no provider controls verdict.

Result: architecture contract coherent; production execution not performed.

**SIM-2 — document path**

Hypothesis only: pinned PDF pointer → MIME router → MarkItDown or MinerU (selected, not chained blindly) → Chonkie source-span chunks → sparse index → Ragas/DeepEval advisory evaluation.

Expected: parser failure does not become empty-success; evaluator cannot promote PASS.

Result: architecture contract coherent; production execution not performed.

**SIM-3 — future candidate security/control path**

Hypothesis only after gate: acquired component tree → Syft SBOM → selected vuln scanner set + Gitleaks → OPA-or-Cedar policy decision → OTel observability record.

Expected: scanner/policy unavailability yields explicit GAP/default-deny where required; telemetry outage cannot falsify security PASS.

Result: contract defines fail-closed boundaries without authorizing acquisition.

### 3 refutations

**REF-1 — “VERIFIED_CLOSED acquisition means ready to wire.”**

REFUTED. Code-root state model explicitly separates acquisition/read-back from `APPROVED_FOR_WIRE`, `WIRED`, `TESTED`, and `PROMOTED`.

**REF-2 — “20X researched candidates are already approved/downloadable.”**

REFUTED. Their authoritative status is `RESEARCHED_CANDIDATE_NO_DOWNLOAD / REVIEW_GATE_REQUIRED`; current download gate is false.

**REF-3 — “Multiple providers on the same port can all be activated because redundancy is always safer.”**

REFUTED. Lucene/Tantivy, Sourcebot/open-codebase-index, OPA/Cedar, scanner sets, and structured-output stacks require routing/pruning/comparative tests. Blind multi-wiring increases contradiction, cost, drift, and duplicated authority.

### GOALS12_OUTPUT

| Goal | Verdict |
|---|---|
| G01 literal requirement preserved | PASS |
| G02 fresh HEAD read | PASS |
| G03 control surfaces read | PASS |
| G04 owner/claim valid | PASS |
| G05 dependency/gate valid | PASS |
| G06 write scope isolated | PASS |
| G07 17 physical + 20 candidate set deduplicated | PASS |
| G08 minimal evidence-only delta | PASS |
| G09 test contract for every mapped adapter | PASS |
| G10 3 simulations + 3 refutations | PASS |
| G11 evidence SHA/readback | POST_WRITE_READBACK_REQUIRED |
| G12 release/supervisor fan-in | POST_WRITE_REQUIRED |

## COUNCIL12

1. **Objective:** produce a wiring-ready design map without wiring.
2. **Requirement:** component→capability→port→adapter→failure→test, overlaps included.
3. **Authority:** physical state/index + V2.1 architecture + gates outrank candidate prose.
4. **Physical state:** 17 acquisition-verified; 23 failed; 20X all research-only.
5. **Owner:** SOL-2 owns SW-N07 evidence/log/claim only.
6. **Gates:** physical repair/download/Step3 all false.
7. **Collision:** N08 concurrent claim is disjoint; no path overlap.
8. **GAP:** wiring contracts were not consolidated into one explicit provider-neutral matrix.
9. **Alternatives:** monolithic/provider-coupled wiring and blind multi-provider activation rejected.
10. **StrategyDelta:** provider-neutral ports + explicit routing/pruning + typed failure + test IDs.
11. **Tests/refutations:** 5 static architecture checks + 3 simulations + 3 refutations.
12. **Verdict:** `PASS_PENDING_SUPERVISOR_FANIN`; production wiring remains blocked.

## Report contract

- node_id: `SW-N07`
- chat_id: `chat-sol2-20260912T2306-0500`
- agent_name: `SOL-2-GPT`
- state: `PASS_PENDING_SUPERVISOR_FANIN`
- base_sha: `8fa359c9684e01dd37134e66d1379df66265ed14`
- final_sha: `POST_WRITE_READBACK_IN_SOL_02_LOG`
- write_scope: `SW-N07-EVIDENCE.md`, `SOL-SWARM-02-LOG.md`, `swarm-claims/CLAIM-SW-N07.json`
- paths_changed_this_step: `SW-N07-EVIDENCE.md`
- commit_sha: `POST_WRITE_READBACK_IN_SOL_02_LOG`
- blob_sha: `POST_WRITE_READBACK_IN_SOL_02_LOG`
- tests: `PORT_COVERAGE_CHECK`, `CANDIDATE_CONTRACT_CHECK`, `AUTHORITY_BOUNDARY_CHECK`, `GATE_CHECK`, `OVERLAP_CHECK`
- run_id: `N/A_READ_ONLY_ARCHITECTURE`
- job_id: `N/A_READ_ONLY_ARCHITECTURE`
- simulations: `3/3`
- refutations: `3/3`
- remaining_gaps: independent review + candidate M06/M07/M08/director gates + acquisition approval + Step3 authorization
- gate_snapshot: unchanged / physical gates false
- review_required: `true`
- next_free_node: `RESCAN_AFTER_RELEASE`

## Final worker verdict

`PASS_PENDING_SUPERVISOR_FANIN`

The V2.1 architecture can expose current physical components and future candidates through provider-neutral ports with explicit failure/test contracts, but this design does **not** authorize wiring. Physical acquisition status, review approval, wiring, runtime activation, testing, and system verification remain separate states.
