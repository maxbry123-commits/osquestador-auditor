# SW-N01 EVIDENCE — M40 + 20X + CANONICAL-117 DEDUP / DECISION MATRIX

- schema: `sharck-input.swarm-node-evidence.v1`
- agent_name: `SOL-1-GPT`
- chat_id: `chat-sol1-20260912T2305-0500`
- node_id: `SW-N01`
- parent_node: `M47_8SOL_SWARM_CONTROL_PLANE`
- mode: `READ_ONLY_RESEARCH`
- claim_commit: `77e544c2d29bbb47b38573ce3fd7811d14cd63a2`
- claim_blob: `130aa41e6168602107f9d95cfaa95ee9af00f019`
- original_base_sha: `6e1925155c9942855dba0bd29e9a27a9d73998f5`
- fresh_head_before_evidence_write: `00ef425add4d258e65b1b3a932b235720bb298b0`
- stale-head revalidation: `PASS`; intervening commit is independent `SW-N02` atomic claim, no overlap with N01 paths.
- primary_classification: `RESEARCH_GAP`
- physical_mutation: `false`
- acquisition: `false`
- shared_control_write: `false`

## STEP 1 — SYNC / VERIFY / CLAIM

Claim was atomically created and read back at:
`swarm-claims/CLAIM-SW-N01.json`.

Authoritative inputs read fresh:
- `SWARM-DAG-8SOL-M47-v1.json` blob `eee95bc7e3e46c17725b33fd0b9224ed3dcde243`.
- canonical component index `➡️📂 readme indice de componentes sharck imput.md` blob `8cb11ccceeb5759ce9802140091340f26b0387ed`.
- `RESEARCH-SHORTLIST-M40-6TRACK-2026-09-11.md` blob `405667869e7c2d473494c00c483a11659a345c01`.
- `20X-OSS-MEJORAS-2026-09-11.md` blob `c4a18bd24059293060ff1f64ce84de46f39d06b0`.
- latest M47 STATE/CHECKPOINT/PLAN/Handoff/Watchdog read; gates remain false for physical repair, B05/B06 acquisition and Step3.

Write scope remains unique to this node: this evidence + `SOL-SWARM-01-LOG.md`; shared control files are SOL-0-only.

### GOALS12_INPUT

- G01 literal requirement preserved: PASS.
- G02 fresh HEAD read: PASS.
- G03 Handoff/STATE/CHECKPOINT/PLAN/Watchdog/DAG read: PASS.
- G04 owner free before claim: PASS; atomic claim read-back verified.
- G05 dependency/gate valid: PASS; read-only node is legal under closed physical gates.
- G06 write_scope non-overlapping: PASS.
- G07 existing catalogs/components deduplicated first: PASS.
- G08 minimum permitted delta selected: PASS; evidence/log only.
- G09 specific deterministic matrix tests planned: PASS.
- G10 3 simulations + 3 refutations required: registered below.
- G11 SHA/readback required: claim done; evidence/log readback pending STEP 3.
- G12 reconciliation delegated to SOL-0 fan-in after report: PASS by contract.

## STEP 2 — EXECUTE / VERIFY

### A. Canonical authority

Canonical index contains `117` components. M40 has `65` research rows across I04/I06/I07/I08/I09/I10. 20X has `20` non-canonical research candidates (#118-#137) and explicitly records `0 downloaded / 0 wired / 0 tested`.

The matrix below is advisory research evidence only. `KEEP_PENDING_PREFLIGHT` does NOT mean APPROVED, QUEUED, DOWNLOADED, VERIFIED_CLOSED or WIRED.

### B. M40 — exhaustive row classification (65/65)

#### `KEEP_PENDING_PREFLIGHT` — 31 rows
Official/project source reference is present, but immutable commit/ref + complete license/maintenance/special-file/size/destination evidence is not uniformly closed in the current M40 artifact. Therefore these remain research candidates only:

`Inspect AI`; `Promptfoo`; `BrowserGym`; `AgentLab`; `SWE-bench`; `MCPMark`; `tau2/tau3-bench`; `AgentBench`; `Text Embeddings Inference (TEI)`; `LibCST`; `Comby`; `Difftastic`; `tree-sitter-graph`; `jscodeshift`; `Joern`; `CodeQL queries/libraries`; `ts-morph`; `Hermes Agent`; `OpenClaw`; `Agent Skills open standard`; `OpenHands Software Agent SDK`; `Cline`; `goose`; `OpenCode`; `mini-SWE-agent`; `Newspaper4k`; `Goose3`; `selectolax`; `curl_cffi`; `Browserless`; `OpenAI Agents SDK`.

Special preflight gates already known from M40 are preserved, including CodeQL/license review, curl_cffi/policy gate and Browserless/license gate.

#### `REFERENCE_ONLY` — 14 rows
No vendoring/acquisition justified by this node:

`BFCL V4`; `Dataset Viewer REST API`; `Spaces agents.md`; `Agent Traces / Session Traces Format`; `Inference Endpoints MCP Server`; `OpenAI Responses API tool model`; `OpenAI sandbox/harness separation`; `OpenAI manager vs handoffs`; `Anthropic effective context engineering`; `Anthropic multi-agent research`; `Anthropic advanced tool use`; `Anthropic Managed Agents`; `Anthropic tool/eval guidance`; `Anthropic simple/composable agents`.

#### `DEFER` — 4 rows
`srcML` (license compatibility gate); `Camoufox` (experimental/operational-policy risk); `camofox-browser` (experimental wrapper, only if standard browser lane fails); `Patchright` (policy/security gate).

#### `REJECT` — 5 rows
`Text Generation Inference (TGI)` (maintenance/archive signal in M40); `GitHub stack-graphs` (archived/unmaintained); `Roo Code` (sunset/archive); `Whoogle` (development ended/no useful results); classic `searx` (stale duplicate; canonical #1 is SearXNG).

#### `EXISTING_117` — 7 M40 rows
`Ragas + DeepEval` (#116/#117; composite row); `huggingface_hub` (#108); `Hugging Face Datasets` (#109); `HF MCP Server` (#110); `HF Skills` (#40); `MCP Registry` (#46); `Continue` (#103, maintenance risk).

These must NOT create duplicate acquisition jobs. Existing FAILED canonical items remain FAILED; dedup is not repair authorization.

#### `EXISTING_20X` — 3 rows
`Browsertrix Crawler` (#118); `warcio` (#119); `ArchiveBox` (#120).

#### `DUPLICATE_M40` — 1 row
`Promptfoo` in I10 duplicates the same candidate already listed in I04. It is one candidate with two research-track rationales, not two acquisition units.

### C. M40 deterministic coverage check

`31 KEEP_PENDING_PREFLIGHT + 14 REFERENCE_ONLY + 4 DEFER + 5 REJECT + 7 EXISTING_117 + 3 EXISTING_20X + 1 DUPLICATE_M40 = 65/65 rows`.

Important normalization: row count is not unique-component count because `Ragas + DeepEval` is one row containing two canonical components and `Promptfoo` appears in two tracks.

### D. 20X — exact canonical dedup + advisory decision matrix (20/20)

The 20X source artifact records that all 20 were checked against the canonical 117 and none is an exact canonical entry. That exact-dedup result is consistent with the current canonical index names/repos. This does NOT eliminate functional overlap.

#### `KEEP_PENDING_M08_PREFLIGHT` — 12
`Browsertrix Crawler`; `warcio`; `ArchiveBox`; `OpenLineage`; `OpenTelemetry Collector`; `OPA`; `Syft`; `Trivy`; `OSV-Scanner`; `Gitleaks`; `DuckDB`; `Soufflé`.

Rationale: distinct net capability is plausible, but every KEEP remains blocked from acquisition until exact license/ref/immutable commit/special-file scan/size/destination/overlap evidence and required reviewer/director gates exist.

#### `DEFER_OVERLAP` — 8
`Marquez` (optional backend behind OpenLineage); `Cedar` (alternative to OPA); `Grype` (scanner overlap with Syft+Trivy lane); `Instructor`; `DSPy`; `LMQL`; `Guardrails` (structured-output/eval overlap with canonical Pydantic/JSON Schema/Outlines/Guidance and each other); `Polars` (evidence-compute overlap with DuckDB for current scope).

This is an advisory dedup/pruning recommendation for supervisor/M08 review, not the reserved M08 official verdict.

#### `REJECT` — 0
No 20X candidate is rejected solely from the current 20X artifact: it records all 20 as public/not archived at its 2026-09-11 verification. Functional overlap is handled as DEFER, not fabricated rejection.

### E. 20X deterministic coverage check
`12 KEEP_PENDING_M08_PREFLIGHT + 8 DEFER_OVERLAP = 20/20`.

### F. Acquisition-readiness verdict

`0/20` 20X candidates are acquisition-ready from this worker evidence because the control plane gate is false and the 20X artifact itself requires immutable pin/license/ref/special-scan/size/destination/overlap closure before queueing.

For the 31 M40 new-candidate rows, current project evidence is also insufficient to promote any to APPROVED/QUEUED as a class. Exact immutable pins are not uniformly persisted in M40. Fail-closed action is `KEEP_PENDING_PREFLIGHT`, not acquisition.

No download, canonical destination write, motor mutation, wiring or Step3 action occurred.

## STEP 3 — TEST / REFUTE / REPORT

### Three simulations

1. `huggingface_hub`: M40 label resolves to canonical #108 → `EXISTING_117`; expected action = no duplicate acquisition, preserve current FAILED state/gate.
2. `Browsertrix Crawler`: M40 I09 resolves to 20X #118 → `EXISTING_20X`; expected action = one candidate record, no duplicate queue.
3. `OpenAI Agents SDK`: not an exact canonical/20X entry; semantic overlap with existing agent frameworks does not prove duplication → retain `KEEP_PENDING_PREFLIGHT` until capability/overlap/pin review.

### Three refutations

1. Refute `65 M40 rows = 65 unique components`: FALSE. Promptfoo is cross-track duplicated and `Ragas + DeepEval` is a composite row.
2. Refute `NEW_CANDIDATE = acquisition-ready`: FALSE. Required immutable pin/license/ref/special-scan evidence is not uniformly closed and physical acquisition gate is false.
3. Refute `20X has no exact canonical duplicate = no overlap`: FALSE. The 20X plan itself identifies functional conflicts such as OPA↔Cedar, Syft/Grype↔Trivy, Instructor/Guardrails/LMQL, DuckDB↔Polars, OpenLineage↔Marquez.

### Test results

- M40 row-accounting invariant: `65/65` classified — PASS.
- 20X accounting invariant: `20/20` classified — PASS.
- Exact duplicate suppression: canonical and 20X duplicates identified without download — PASS for documented exact matches.
- Physical mutation invariant: `0` canonical product writes — PASS.
- Reserved-owner invariant: no M06/M07/M08 official review emitted — PASS.
- Acquisition gate invariant: no candidate promoted to QUEUED/DOWNLOADED — PASS.

### COUNCIL12

1. Objective: dedup M40 + 20X against canonical 117 and produce a decision matrix.
2. Literal requirement: research-only, no acquisition or canonical mutation.
3. Authority: physical/index + current M47 deltas > research docs > worker inference.
4. Physical state: canonical 117; B01-B04 17 verified/23 failed; B05/B06 20 researched/0 downloaded.
5. Owner: SOL-1-GPT owns only SW-N01 after atomic read-back.
6. Gates: physical_repair=false; b05_b06_download=false; step3=false.
7. Collision risk: evidence/log paths unique; intervening SW-N02 claim is non-overlapping.
8. Causal GAP: `RESEARCH_GAP` — candidate dedup/preflight data is not equivalent to immutable acquisition evidence.
9. Alternatives rejected: bulk-download all candidates; duplicate existing components; promote based on research label alone.
10. StrategyDelta: normalize M40/20X into exact existing/reference/defer/reject/keep-pending classes while preserving missing-pin blockers.
11. Tests/refutations: 65/65 + 20/20 accounting; 3 simulations; 3 refutations; no physical writes.
12. Verdict: `PASS_PENDING_SUPERVISOR_FANIN`; no self-certification of VERIFIED_CLOSED.

### GOALS12_OUTPUT

- G01 literal preserved: PASS.
- G02 fresh HEAD re-read before material evidence write: PASS.
- G03 mandatory control sources read: PASS.
- G04 owner/claim: PASS.
- G05 gates/dependencies: PASS.
- G06 scope isolation: PASS.
- G07 dedup against 117 + 20X + M40: PASS.
- G08 delta minimum/read-only: PASS.
- G09 specific tests: PASS.
- G10 3 simulations + 3 refutations: PASS.
- G11 evidence SHA/readback: PENDING immediate post-write readback; log SHA/readback follows.
- G12 next-node reconciliation: SOL-0 supervisor fan-in required; next free node must be selected only after fresh queue/claims read.

## WORKER VERDICT

`PASS_PENDING_SUPERVISOR_FANIN`

Remaining gaps:
- reserved M08 must issue its own official OSS/license/maintenance/overlap verdict;
- immutable commit/ref/license/special-file/size/destination evidence is not complete for all KEEP candidates;
- director/acquisition gates remain closed;
- this evidence does not authorize B05/B06 or M40 downloads.

Release intent: after evidence + own-log readback, `SOL-1-GPT` has no further write authority on SW-N01 except corrections requested by supervisor. Shared queue/state reconciliation belongs to SOL-0.
