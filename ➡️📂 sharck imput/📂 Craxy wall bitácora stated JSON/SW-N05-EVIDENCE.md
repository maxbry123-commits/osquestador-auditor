# SW-N05 EVIDENCE — HF BRIDGE PORT / ADAPTER / FAILURE CONTRACT AUDIT

- schema: `sharck-input.swarm-node-evidence.v1`
- agent_name: `SOL-1-GPT`
- chat_id: `chat-sol1-20260912T2305-0500`
- node_id: `SW-N05`
- task: `HF_BRIDGE_PORT_CONTRACT_AUDIT`
- mode: `READ_ONLY_RESEARCH`
- claim_commit: `23ea92715b05cffe23038e9e1378e6b4fdbaf835`
- claim_blob: `ebf7c8a2e08baaf38f59fb4d15434614a9c3fc35`
- base_sha: `dc809f15a32c3943de0e1a5cc338990a25a90bc3`
- fresh_head_before_evidence_write: `8fa359c9684e01dd37134e66d1379df66265ed14`
- stale-head revalidation: `PASS`; intervening writes are independent worker claims/evidence/logs.
- physical_mutation: `false`
- acquisition: `false`

## STEP 1 — SYNC / VERIFY / CLAIM

Atomic N05 claim was created first and read back successfully. A later SOL-5 write records a claim blocker, confirming anti-collision behavior rather than shared ownership.

Authoritative evidence read:
- `HF-BRIDGE-DESIGN.md` blob `7f0dd8a6da2cc70e4f302cef965f045d0d22d0f4`.
- canonical component index: #40 HF Skills, #108 `huggingface_hub`, #109 `datasets`, #110 `hf-mcp-server`.
- physical B04 directory: `datasets/` and `hf-mcp-server/` present.
- `B04-XRAY-2026-09-11.md`: #108 `huggingface_hub` remains FAILED by confirmed source symlink; #109/#110 belong to the B04 VERIFIED_CLOSED set.
- M40 I06: Dataset Viewer API, Spaces agents interface, Agent Traces and Inference Endpoints MCP are reference-only ports/integrations; TEI is a new candidate, not a prerequisite for this base bridge.

Physical gates remain closed; this node only specifies contracts.

### GOALS12_INPUT
- G01 literal bridge scope preserved: PASS.
- G02 fresh HEAD/readback: PASS.
- G03 design/index/B04/M40 evidence read: PASS.
- G04 N05 owner claim: PASS.
- G05 gates valid for read-only design audit: PASS.
- G06 write scope isolated: PASS.
- G07 existing #40/#108-#110 reused before proposing anything new: PASS.
- G08 minimal delta: evidence/log only.
- G09 port/failure/test matrix defined below.
- G10 three simulations + three refutations required.
- G11 evidence/log readback required.
- G12 SOL-0 fan-in required.

## STEP 2 — EXECUTE / VERIFY

### A. Minimal bridge decision

The core HF bridge requires **zero new component acquisition** to specify its ports:

1. `HFHubPort` → canonical #108 identity/API surface.
2. `HFDatasetPort` → canonical #109 `datasets` plus official Dataset Viewer REST as reference-only metadata/sample lane.
3. `HFMCPPort` → canonical #110 `hf-mcp-server` when MCP is available.
4. `HFSkillPointerPort` → canonical #40 `huggingface/skills`, pointer-first and relevance-loaded.

Reference-only official surfaces may extend input retrieval without vendoring a component:
- `HFSpacePointerPort` → Spaces agent schema/call/poll/upload metadata only when relevant.
- `HFTracePointerPort` → Agent Traces/Session Traces JSONL as provenance-bearing context source.
- `HFEndpointMetadataPort` → Inference Endpoints MCP/status/log/metrics pointers only; endpoint creation/scaling is outside Sharck Input PRE-LLM scope.

`TEI` stays `NEW_CANDIDATE / NOT_REQUIRED_FOR_BASE_BRIDGE`; it must not be downloaded merely because an embeddings/rerank lane could use it later.

### B. Physical-state-aware port matrix

| port | backing source | current state | minimal adapter behavior | fail-closed rule | test contract |
|---|---|---|---|---|---|
| `HFHubPort` | #108 `huggingface_hub` / official HF HTTP metadata | canonical item FAILED due source symlink; do not relabel | metadata/pointer adapter: repo/model/dataset id, revision, URL, card/license metadata; `trust_remote_code=false` | if local component unavailable, record `HF_COMPONENT_UNAVAILABLE` and use only authorized official HTTP metadata fallback; no fake VERIFIED_CLOSED | known model/dataset lookup returns id+revision+URL+license/provenance; failed local component state remains unchanged |
| `HFDatasetPort` | #109 `datasets` + Dataset Viewer REST | #109 VERIFIED_CLOSED; Dataset Viewer is reference-only | metadata first; `/is-valid`, `/splits`, `/rows`, `/search`, `/filter`, `/parquet`, `/size`, `/statistics`; load/stream only under bounded request | no whole-dataset context ingestion; connector unavailable → `HF_CONNECTOR_GAP`; remote code remains off | metadata-only query; bounded sample query; deny/stop unbounded full ingestion request |
| `HFMCPPort` | #110 `hf-mcp-server` | VERIFIED_CLOSED physical B04 component | expose official MCP tools through allowlisted read/search operations; return provenance | MCP unavailable/tool missing → `HF_MCP_GAP`; never convert tool discovery into authorization | tool discovery + one read-only call + provenance; simulate unavailable server and assert no PASS |
| `HFSkillPointerPort` | #40 `huggingface/skills` | already canonical; no duplicate acquisition | store pointer/skill metadata; load specific `SKILL.md` only on relevance | no bulk prompt injection of all skills; absent skill → `HF_SKILL_POINTER_GAP` | pointer resolution then selective skill read; unrelated skill remains unloaded |
| `HFSpacePointerPort` | official Spaces agents interface | `REFERENCE_ONLY_PORT` | L0 metadata/schema, then optional authorized call/poll/upload pointer | untrusted Space code is not executed locally; unsupported Space → explicit gap | schema discovery without local execution; bounded authorized call path only |
| `HFTracePointerPort` | official Agent Traces format | `REFERENCE_ONLY_PORT` | ingest redacted JSONL trace pointer/metadata as evidence source | secrets/tokens must be redacted; malformed trace → `HF_TRACE_SCHEMA_GAP` | reject trace containing secret-like fields until redacted; preserve source revision |
| `HFEndpointMetadataPort` | official Inference Endpoints MCP docs/tooling | `REFERENCE_ONLY_INTEGRATION` | read status/log/metrics/pointer metadata only for context | CREATE/PAUSE/SCALE is `HF_SCOPE_VIOLATION` in Sharck Input unless a separate runtime owner authorizes it | read-only status succeeds; mutation command is rejected by input-layer policy |

### C. Common adapter output contract

Every HF port should normalize to a pointer/evidence envelope, not raw unbounded content:

`{source_type, hf_id, revision, url, license, card_or_schema_ref, retrieved_at, content_level, provenance, fact_class, hash_or_etag, warnings}`

Required `content_level`:
- `L0`: id/type/description/tags/license/revision/URL.
- `L1`: relevant card/README excerpt.
- `L2`: selected files/schema/features/sample rows.
- `L3`: heavy retrieval/inference only via isolated authorized adapter; not default Sharck Input behavior.

Required `fact_class`: `FACT | INFERENCE | UNKNOWN`.

### D. Failure contracts

1. `HF_COMPONENT_UNAVAILABLE` — canonical backing component is FAILED/not operational; state is preserved.
2. `HF_CONNECTOR_GAP` — connector disabled/unavailable; fallback only to authorized official metadata path.
3. `HF_MCP_GAP` — MCP server/tool unavailable or incompatible.
4. `HF_LICENSE_UNKNOWN` — license/card missing; do not promote source for unrestricted use.
5. `HF_REVISION_UNPINNED` — mutable pointer lacks revision/commit; evidence cannot be immutable.
6. `HF_REMOTE_CODE_REQUIRED` — requested source requires remote code; reject/defer by default (`trust_remote_code=false`).
7. `HF_DATASET_BOUNDS_GAP` — request lacks bounded subset/split/sample policy or exceeds context budget.
8. `HF_PROVENANCE_GAP` — no source URL/revision/hash/etag; do not emit authoritative FACT.
9. `HF_SECRET_EXPOSURE` — token/credential detected in payload/log/context; hard fail and redact.
10. `HF_SCOPE_VIOLATION` — request attempts model execution, endpoint lifecycle mutation or workflow orchestration outside PRE-LLM input scope.

### E. Duplication/overlap verdict

- No new acquisition is needed for the four base ports: reuse #40/#108/#109/#110.
- `huggingface_hub` must **not** be reacquired under another name to evade its symlink gate.
- Dataset Viewer, Spaces interface, Agent Traces, and Endpoint MCP are `REFERENCE_ONLY` surfaces, not vendored duplicates.
- TEI remains optional candidate and requires a separate capability gap + dedup + M08/director gate before any acquisition.

## STEP 3 — TEST / REFUTE / REPORT

### Three simulations
1. #108 unavailable locally because source symlink gate remains FAILED: `HFHubPort` returns authorized official metadata pointer with `HF_COMPONENT_UNAVAILABLE` warning; canonical #108 remains FAILED.
2. Dataset connector disabled by server configuration: `HFDatasetPort` records `HF_CONNECTOR_GAP`, may use official Dataset Viewer HTTP metadata if authorized, and does not claim a dataset installation.
3. Request asks Inference Endpoint port to SCALE an endpoint: adapter rejects with `HF_SCOPE_VIOLATION`; input layer may only return read-only status/log/metrics pointers.

### Three refutations
1. Refute `#108 FAILED means the whole HF bridge is blocked`: FALSE for metadata/pointer design; official HTTP metadata fallback exists, but #108 remains FAILED and no local-code PASS is claimed.
2. Refute `#109 VERIFIED_CLOSED means full datasets can be injected into context`: FALSE; progressive disclosure and bounded streaming/sample rules remain mandatory.
3. Refute `MCP tool discovered = action authorized`: FALSE; discovery/availability is separate from policy authorization and Sharck Input scope.

### Test results
- four base ports mapped: `4/4` PASS.
- reference-only extension ports mapped: `3/3` PASS.
- failure contracts defined: `10`.
- duplicate acquisitions proposed: `0` PASS.
- failed B04 item promoted: `0` PASS.
- physical writes/wiring: `0` PASS.
- secret values persisted: `0` PASS.

### COUNCIL12
1. Objective: minimum HF context bridge, not general HF runtime.
2. Requirement: reuse canonical components and pointer APIs without duplicate acquisition.
3. Authority: physical B04 + HF bridge design + canonical index + M40 I06.
4. Physical state: #109/#110 present/verified; #108 remains fail-closed; #40 already canonical.
5. Owner: SOL-1-GPT owns only SW-N05.
6. Gates: wiring/acquisition/Step3 false.
7. Collision: SOL-5 encountered blocker after N05 claim; no shared ownership created.
8. Causal GAP: bridge contract exists; runtime wiring is gated, and #108 local acquisition remains failed.
9. Alternatives rejected: duplicate `huggingface_hub`; bulk dataset ingestion; execute remote code; endpoint lifecycle mutation inside input layer.
10. StrategyDelta: pointer-first normalized envelope + explicit failure contracts.
11. Tests/refutations: 3 simulations + 3 refutations + no-duplicate/no-mutation invariants.
12. Verdict: `PASS_PENDING_SUPERVISOR_FANIN`; physical integration remains blocked.

### GOALS12_OUTPUT
- G01 scope preserved: PASS.
- G02 fresh HEAD: PASS.
- G03 required evidence: PASS.
- G04 ownership: PASS.
- G05 gates: PASS.
- G06 isolation: PASS.
- G07 dedup/reuse: PASS.
- G08 minimal delta: PASS.
- G09 port/test/failure matrix: PASS.
- G10 simulations/refutations: PASS.
- G11 evidence/log readback: pending immediate readback.
- G12 supervisor reconciliation: required.

## WORKER VERDICT
`PASS_PENDING_SUPERVISOR_FANIN`

Remaining gaps:
- #108 `huggingface_hub` physical acquisition remains FAILED until reserved review/gate chooses a lawful StrategyDelta;
- no production wiring has been authorized;
- TEI and any new HF component remain candidate-only;
- live connector/API availability must be tested at runtime and may yield `HF_CONNECTOR_GAP` without changing project PASS state.
