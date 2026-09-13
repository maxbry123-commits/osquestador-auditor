# SW-N06 — RUNTIME_AND_AGENT_MAINTENANCE_RISK_AUDIT

- schema: `sharck-input.multisol-dag.v1`
- agent_name: `SOL-6-GPT`
- chat_id: `chat-sol6-20260912T2310-0500`
- node_id: `SW-N06`
- parent_node: `M47_8SOL_SWARM_CONTROL_PLANE`
- claim_commit: `7c3d296b014abf89e35ada4671c3992bf4dcc7fc`
- claim_base_sha: `985f6312cfe850a27c26a87b54373fe456d5eba2`
- pre_report_fresh_main_sha: `c6927518f8de2d9795754ea2b7862502443b2947`
- mode: `READ_ONLY_RESEARCH`
- failure_class: `RESEARCH_GAP + CONTROL_PLANE_DRIFT`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- acquisition_performed: `NO`
- product/runtime wiring performed: `NO`

## Assertion under test
Agent/runtime candidates can be ranked by current official upstream, maintenance, license, immutable ref and overlap before any acquisition.

## STEP 1 — SYNC / VERIFY / CLAIM

Fresh M47 control plane and claim were read back before execution. `SW-N06` was `READY_TO_CLAIM`, then atomically claimed by `SOL-6-GPT`. `SW-N05` became occupied during preflight and was explicitly skipped.

M40 I08/I10 was re-read as research only, not authorization. Physical B03 runtime inventory currently contains at least:

- `continue`
- `kythe`
- `open-codebase-index`
- `smolagents`
- `sourcebot`
- `sqry`

This creates a real overlap gate for additional general-purpose/coding-agent runtimes.

A current physical manifest exists for `continue` and reports `extraction_verified=true`, `reconstruction_verified=true`, `no_lfs=true`, `source_repo=https://github.com/continuedev/continue`, and `source_commit=5522c6f44ca0ac3528b37244818fbfa39b5af470`.

## STEP 2 — EXECUTE / VERIFY

### Decision semantics
- `KEEP`: keep on the candidate/preflight track; this is NOT download approval.
- `REFERENCE`: use API/spec/pattern/pointer; do not vendor as a runtime under this node.
- `DEFER`: potentially useful but overlap/scope/size/ref risk prevents promotion now.
- `REJECT`: do not acquire under current evidence.

### 11 useful findings / risk matrix

| Candidate | Decision | Official upstream / maintenance | License | Default ref + immutable commit observed | Size KiB | Overlap / exact reason |
|---|---|---|---|---|---:|---|
| Hermes Agent | `DEFER` | `NousResearch/hermes-agent`; active, not archived; pushed 2026-09-13 | MIT | `main` → `f79cb77224525a884c3c21cd4aa2474da2ec4a0f` | 946916 | Very broad agent/skills/memory/MCP/runtime surface; strong overlap with existing B03 agent/runtime lane. Too large to promote without a proven pre-LLM capability gap. |
| OpenClaw | `REFERENCE` | `openclaw/openclaw`; active, not archived; pushed 2026-09-13 | MIT by authoritative `LICENSE`; GitHub metadata detector says `NOASSERTION` | `main` → `f369c90e95afb636531157e6fc4e8faa1bdff726` | 4588596 | Useful bridge/control-plane patterns, but full runtime is extremely large and risks expanding Sharck Input into the full workflow. Keep pointer/reference only. |
| Agent Skills open standard | `REFERENCE` | `agentskills/agentskills`; active; specification/documentation repo | Apache-2.0 | `main` → `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | 782 | It is a contract/spec, not a runtime. Strong fit as common skill format; no runtime acquisition required. |
| OpenHands Software Agent SDK | `KEEP` | `OpenHands/software-agent-sdk`; active, not archived; pushed 2026-09-13 | MIT | `main` → `c37007429be8b4465a83487dc1fd0914df0ea734` | 37220 | Modular SDK is materially narrower than a full IDE agent and may provide a clean future adapter/harness boundary. Keep for later acquisition preflight only. |
| Cline | `DEFER` | `cline/cline`; active, not archived; pushed 2026-09-12 | Apache-2.0 | `main` → `cfe9cadab99617d5013bf89f07b079d105057791` | 579713 | Autonomous coding SDK/IDE/CLI overlaps heavily with physical Continue and the existing B03 runtime lane; no net-new Sharck pre-LLM gap proven. |
| goose | `DEFER` | Historical `block/goose` redirects; current canonical upstream is `aaif-goose/goose`; active under AAIF/Linux Foundation | Apache-2.0 | `main` → `50666ae0b9a51e260b52b7efbab2e4e020346e94` | 973620 | M40 source pointer is stale. Full multi-model/MCP agent overlaps broad runtime lane and is large. Correct upstream first; defer acquisition. |
| OpenCode | `DEFER` | Historical `sst/opencode` redirects; current canonical upstream is `anomalyco/opencode`; active | MIT | default `dev` → `95daf90670b7c039c436c85537da5fbfe2205b41` | 511921 | Source transfer + moving `dev` default branch is a pin/stability risk; strong overlap with Continue/coding-agent runtime. Require stable ref policy before any queue. |
| mini-SWE-agent | `KEEP` | `SWE-agent/mini-swe-agent`; active, not archived; pushed 2026-09-07 | MIT | `main` → `04d809ceab9df28f9adaed044884180159172930` | 20171 | Small, intentionally minimal issue-solving harness gives a distinct baseline/eval role with much lower footprint than full IDE runtimes. Keep for later preflight. |
| Continue | `KEEP` (`EXISTING_117`, no new acquisition) | `continuedev/continue`; currently active and NOT archived; pushed 2026-09-13 | Apache-2.0 | `main` → `5522c6f44ca0ac3528b37244818fbfa39b5af470` | 872434 | M40 maintenance-risk statement is stale/refuted. Physical canonical manifest already points to exactly the current upstream HEAD commit and is extraction/reconstruction verified. Do not duplicate. |
| Roo Code | `REJECT` | `RooCodeInc/Roo-Code`; `archived=true`; last push 2026-05-15 | Apache-2.0 | `main` → `b867ec9145750d0ae1ff7f02d35406e9bf2a0b16` | 368021 | Archived/sunset repository; M40 rejection remains supported. |
| OpenAI Agents SDK | `REFERENCE` | `openai/openai-agents-python`; active, not archived; pushed 2026-09-12 | MIT | `main` → `fbd2dbcaaf74a2c447c6d3fa9d5645d83fd7e292` | 47037 | Useful agent/handoff/guardrail/tracing architecture, but Sharck Input is PRE-LLM and must not become the complete agent workflow. Use as adapter/harness reference, not core runtime. |

### Source corrections / control drift
1. M40 `goose` pointer `block/goose` is stale; GitHub returns a permanent move and current repo identity is `aaif-goose/goose` (same repository id `846698999`).
2. M40 `OpenCode` pointer `sst/opencode` is stale; GitHub returns a permanent move and current repo identity is `anomalyco/opencode` (repository id `975734319`).
3. M40 says Continue is read-only/no longer maintained. Fresh GitHub metadata says `archived=false` with recent push, and the physical canonical `continue` manifest is pinned to the same current official HEAD `5522c6f44ca0ac3528b37244818fbfa39b5af470`. Historical maintenance-risk classification must not be inherited.
4. OpenClaw repository metadata license classifier returns `NOASSERTION`, but direct readback of canonical `LICENSE` identifies MIT License. Treat direct license-file evidence as stronger than metadata classifier.

### Candidate preflight fields not promoted by this node
For every NEW candidate above:
- `SPECIAL FILE SURFACE`: `UNPROVEN_IN_SW-N06`; recursive symlink/submodule/LFS/special-file scan belongs to a later acquisition preflight. This uncertainty forbids acquisition approval here.
- `DESTINATION`: no canonical write authorized. If a later director gate approves a runtime, the only proposed lane is `B03-code-runtime/<slug>` after dedup; reference-only candidates receive no vendored destination.
- `PROPOSED ADAPTER`: pointer/port first; do not patch canonical motors. OpenHands → future `agent.harness.openhands`; mini-SWE → future `agent.eval.miniswe`; reference candidates → documentation/port pointers only.
- `TEST PLAN`: immutable pin → special-file scan → license/readme readback → isolated sandbox import/CLI smoke → no-network deterministic microtest → overlap check → only then director review.

## STEP 3 — TEST / REFUTE / REPORT

### Specific tests
1. `OFFICIAL_UPSTREAM_RESOLUTION`: PASS with two required corrections (`block/goose`→`aaif-goose/goose`; `sst/opencode`→`anomalyco/opencode`).
2. `LICENSE_EVIDENCE`: PASS for ranking; OpenClaw required direct LICENSE readback to resolve metadata `NOASSERTION`.
3. `IMMUTABLE_PIN_CAPTURE`: PASS; every matrix row has an observed immutable commit SHA.
4. `CANONICAL_OVERLAP_CHECK`: PASS; physical B03 inventory was read and Continue canonical manifest read back.
5. `NO_PHYSICAL_MUTATION`: PASS; no component download, extraction, wiring, product repair, canonical motor mutation, LFS, force push, or shared control-plane write was performed.

### 3 simulations
- `SIM-1_ACTIVE_SMALL_NET_NEW`: active + permissive + relatively small + distinct baseline role ⇒ mini-SWE-agent remains `KEEP`, never auto-download.
- `SIM-2_TRANSFERRED_UPSTREAM`: old official URL redirects to same repository identity ⇒ repair source pointer first, capture new canonical owner/ref, then re-rank; goose/OpenCode correctly become `DEFER` rather than silently queueing stale URLs.
- `SIM-3_EXISTING_CANONICAL_MATCHES_FRESH_HEAD`: existing component + verified physical manifest + source commit equals fresh upstream HEAD ⇒ `KEEP_EXISTING`, no duplicate acquisition; Continue satisfies this case.

### 3 refutations
- `REFUTE-1`: hypothesis “Continue is read-only/unmaintained” is REFUTED by fresh `archived=false`, recent push, current official HEAD and exact physical manifest source-commit match.
- `REFUTE-2`: hypothesis “block/goose is still the canonical upstream” is REFUTED by GitHub permanent redirect and current `aaif-goose/goose` repository identity.
- `REFUTE-3`: hypothesis “sst/opencode is still the canonical upstream” is REFUTED by GitHub permanent redirect and current `anomalyco/opencode` repository identity.

Additional adversarial check: hypothesis “OpenClaw license is unknown because metadata says NOASSERTION” is REFUTED by direct canonical LICENSE readback showing MIT.

## COUNCIL12 — analytical review
1. **Objective:** rank runtime/agent candidates before acquisition.
2. **Requirement:** read-only research only; exactly 3 steps; no reserved-owner work.
3. **Authority:** fresh physical B03 + physical Continue manifest + current official GitHub upstream > historical M40 labels.
4. **Physical state:** existing B03 runtime lane confirmed; Continue physically present with verified manifest.
5. **Owner:** SW-N06 atomically owned by SOL-6-GPT; no scope collision observed after claim.
6. **Gates:** all physical/acquisition/step3 gates remain false; canonical motors immutable.
7. **Collision risk:** evidence/log paths are node/agent unique; shared control files untouched.
8. **Causal GAP:** stale upstream pointers and stale maintenance labels can cause wrong acquisition/ranking; broad runtime candidates also overlap existing B03.
9. **Alternatives:** use pointers/specs/reference patterns when capability can be obtained without vendoring; prefer minimal harness over full runtime when evaluating behavior.
10. **StrategyDelta:** correct source identities, preserve Continue, keep OpenHands + mini-SWE for later preflight, reference Agent Skills/OpenClaw/OpenAI SDK, defer overlapping heavy runtimes, reject Roo.
11. **Tests/refutations:** 5 specific checks + 3 simulations + 3 required refutations completed; additional license refutation completed.
12. **Verdict:** `PASS_PENDING_REVIEW`; ranking evidence is sufficient for supervisor fan-in, but it does NOT authorize acquisition or production integration.

## GOALS12_OUTPUT
- G01 literal requirement preserved: `PASS`
- G02 fresh HEAD read: `PASS`
- G03 Handoff/STATE/CHECKPOINT/PLAN/Watchdog/DAG read: `PASS`
- G04 owner free / atomic claim verified: `PASS`
- G05 dependencies/gates valid: `PASS`
- G06 write_scope non-overlapping: `PASS`
- G07 existing code/components deduplicated: `PASS`
- G08 minimal permitted delta only: `PASS`
- G09 node-specific verification executed: `PASS`
- G10 three simulations + three refutations: `PASS`
- G11 evidence + SHA + readback persisted: `PENDING_READBACK_AT_WRITE_TIME`
- G12 final state / next free node reconciled: `PENDING_RELEASE_AT_WRITE_TIME`

## Remaining gaps
- Special-file/symlink/submodule/LFS surface has NOT been proven for NEW candidates; later acquisition preflight required.
- No runtime integration/sandbox execution was authorized or performed.
- `KEEP` here means shortlist retention only; director/acquisition gate remains mandatory.
- Supervisor must fan-in source-pointer corrections and Continue maintenance-drift correction into shared control surfaces if accepted.

## Producer verdict
`PASS_PENDING_REVIEW`

The producer does not self-certify `VERIFIED_CLOSED`.
