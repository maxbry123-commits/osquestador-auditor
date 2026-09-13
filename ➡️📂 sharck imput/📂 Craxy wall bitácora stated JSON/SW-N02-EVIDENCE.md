# SW-N02 EVIDENCE — 11 SOURCE-SPECIAL / SYMLINK PROVENANCE FAILURES

- schema: `sharck-input.swarm-node-evidence.v1`
- agent_name: `SOL-2-GPT`
- chat_id: `chat-sol2-20260912T2306-0500`
- node_id: `SW-N02`
- parent_node: `M47_8SOL_SWARM_CONTROL_PLANE`
- mode: `READ_ONLY_FORENSIC`
- claim_commit: `00ef425add4d258e65b1b3a932b235720bb298b0`
- claim_blob: `513c8cf4cb48ebf734a7dab06d2c0d3fb0ef5d0d`
- base_sha: `77e544c2d29bbb47b38573ce3fd7811d14cd63a2`
- fresh_head_before_evidence_write: `0611bef7e98eaae263730aa68bc0a5f8fcb903c4`
- stale-head revalidation: `PASS`; intervening writes are other swarm-node paths outside SW-N02 write scope.
- primary_classification: `SOURCE_PROVENANCE_FAILURE`
- secondary_classification: `EVIDENCE_FAILURE`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`

## Assertion under test

> The 11 source-special/symlink failures can be separated into recoverable/currently reproducible source topology versus irrecoverable historical-ref gaps without fabricating source commits.

## STEP 1 — SYNC / VERIFY / CLAIM

Atomic claim was created and read back at:

`➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/swarm-claims/CLAIM-SW-N02.json`

The claim remains owned by `SOL-2-GPT`; no shared control-plane file is in this node's write scope.

Fresh control-plane reads confirmed:

- M47 8-SOL control active.
- `SW-N02` was safe/free when claimed after `SW-N01` was observed occupied by SOL-1.
- M06/M07/M08 remain reserved to ASTRA/CLAUDE/GROK.
- physical repair, B05/B06 download, and Step3 production gates remain closed.
- this node is evidence-only; no canonical component, acquisition motor, queue, adapter, STATE, PLAN, CHECKPOINT, HANDOFF, or DAG mutation is authorized.

### GOALS12_INPUT

| goal | verdict | evidence |
|---|---|---|
| G01 literal requirement preserved | PASS | SW-N02 assertion and 11-component universe preserved |
| G02 fresh HEAD read | PASS | HEAD re-read before claim and before evidence write |
| G03 Handoff/STATE/CHECKPOINT/PLAN/Watchdog/DAG read | PASS | M47 control-plane set + current architecture/method read |
| G04 owner free | PASS | atomic claim + readback; N01 collision caused rescan before N02 claim |
| G05 dependency/gate valid | PASS | evidence-only node permitted while physical gates false |
| G06 write_scope non-colliding | PASS | evidence + own log + own claim only |
| G07 existing evidence/code deduplicated | PASS | M23/M30/M32/M33/B04/state/queue evidence reused |
| G08 delta minimal and allowed | PASS | report-only delta |
| G09 specific causal test defined | PASS | queue ref + failed-state persistence + current upstream special-file cross-check |
| G10 3 simulations + 3 refutations | PASS | specified below |
| G11 evidence + SHA + readback | PENDING_POST_WRITE | evidence commit/blob and readback must be recorded in SOL-02 log/claim |
| G12 state/next-node reconciliation | PENDING_POST_WRITE | supervisor fan-in + release required |

## STEP 2 — EXECUTE / VERIFY

### A. Exact 11-component universe

The source-special/symlink failure universe is exactly:

1. `stormcrawler`
2. `tika`
3. `docling`
4. `vespa`
5. `networkx`
6. `cocoindex`
7. `pydantic-ai`
8. `litellm`
9. `fastmcp`
10. `huggingface_hub`
11. `unstructured`

The first nine are the B01-B03 source-special group. The final two are B04 source-special failures.

### B. Provenance persistence failure

The acquisition sequence resolves a source and a `commit`, then scans the tree. The special-file guard can throw during tree scanning before the normal success result is persisted. Failed state records retain source repository/status/traceback but do not retain the acquired dependency `source_commit` for these early failures.

All 11 queue entries used the mutable ref `HEAD` rather than a pinned immutable source commit:

- B01: `stormcrawler`, `tika`, `docling` -> `source_ref: HEAD`.
- B02: `vespa`, `networkx` -> `source_ref: HEAD`.
- B03: `cocoindex`, `pydantic-ai`, `litellm`, `fastmcp` -> `source_ref: HEAD`.
- B04: `huggingface_hub`, `unstructured` -> `source_ref: HEAD`.

Therefore the exact historical dependency commit used by each failed acquisition attempt is **not recoverable from the canonical persisted queue/state evidence alone**. The GitHub Actions workflow `head_sha` identifies the orchestration repository revision, not the dependency's acquired source commit.

### C. Special-path evidence already present

The prior forensics preserve a real special-path surface; this audit does not erase it:

- `stormcrawler`: 2 special paths observed.
- `tika`: at least 30 special paths observed.
- `docling`: 6 special paths observed.
- `vespa`: 3 special paths observed.
- `networkx`: 1 special path observed.
- `cocoindex`: 7 special paths observed.
- `pydantic-ai`: 15 special paths observed.
- `litellm`: 1 special path observed.
- `fastmcp`: 2 special paths observed.
- `huggingface_hub`: `CLAUDE.md` was independently observed as Git mode `120000` in an official current-source tree.
- `unstructured`: the B04 X-Ray identifies 20 special paths under `scripts/performance/docs/`; inspected current-source fixtures are Git mode `120000`.

For B01-B03, the canonical special-file ledger correctly treats `special` as **non-regular** and does not silently upgrade every entry to `symlink` without exact mode evidence.

### D. Current upstream corroboration is not historical reconstruction

Two B04 repositories were independently re-checked against their current official `main` branches during SW-N02:

- `huggingface/huggingface_hub`: current `main` resolved to `e8df036ec87e4c2b165cd8d66f66ad357fdcd77c`; `CLAUDE.md` is represented in the current Git tree with mode `120000` and blob `47dc3e3d863cfb5727b87d785d09abf9743c0a72`.
- `Unstructured-IO/unstructured`: current `main` resolved to `68d1e5bec313380c6013f4ac5b06cc16417a9654`; the current `scripts/performance/docs/DA-1p.pdf` resolves as a link target into the test fixture tree, corroborating the current special/symlink topology documented by the B04 X-Ray.

These current commits were discovered **after** the historical failed acquisitions. They are evidence of current upstream topology only. They MUST NOT be substituted for the unknown historical source commits of the failed attempts.

### E. Per-component verdict — 11/11

| component | batch | persisted ref | historical source_commit recoverable from canonical failed state? | special topology evidence | SW-N02 verdict | prerequisite for any future repair/replay |
|---|---|---|---|---|---|---|
| stormcrawler | B01 | `HEAD` | NO | 2 non-regular paths observed | `HISTORICAL_REF_NONRECOVERABLE` | pin immutable official commit before scan; persist provenance pre-scan; exact modes/targets + full-tree readback |
| tika | B01 | `HEAD` | NO | >=30 non-regular paths observed | `HISTORICAL_REF_NONRECOVERABLE` | same; do not infer all special entries are symlinks |
| docling | B01 | `HEAD` | NO | 6 non-regular paths observed | `HISTORICAL_REF_NONRECOVERABLE` | same; preserve all six exact paths and modes from pinned source |
| vespa | B02 | `HEAD` | NO | 3 non-regular paths observed | `HISTORICAL_REF_NONRECOVERABLE` | immutable source commit + pre-scan provenance + exact path metadata |
| networkx | B02 | `HEAD` | NO | 1 non-regular path observed | `HISTORICAL_REF_NONRECOVERABLE` | immutable source commit + exact special-file proof before any gated strategy |
| cocoindex | B03 | `HEAD` | NO | 7 non-regular paths observed | `HISTORICAL_REF_NONRECOVERABLE` | immutable source commit + exact mode/target ledger |
| pydantic-ai | B03 | `HEAD` | NO | 15 non-regular paths observed | `HISTORICAL_REF_NONRECOVERABLE` | immutable source commit + exact mode/target ledger |
| litellm | B03 | `HEAD` | NO | 1 non-regular path observed | `HISTORICAL_REF_NONRECOVERABLE` | immutable source commit + exact mode/target ledger |
| fastmcp | B03 | `HEAD` | NO | 2 non-regular paths observed | `HISTORICAL_REF_NONRECOVERABLE` | immutable source commit + exact mode/target ledger |
| huggingface_hub | B04 | `HEAD` | NO | current official tree independently corroborates `CLAUDE.md` mode `120000` | `CURRENT_SOURCE_SYMLINK_CORROBORATED__HISTORICAL_REF_NONRECOVERABLE` | never backfill historical commit with modern HEAD; future replay pins immutable commit and persists source_commit before scan |
| unstructured | B04 | `HEAD` | NO | B04/current official tree corroborates symlink fixture topology | `CURRENT_SOURCE_SYMLINK_CORROBORATED__HISTORICAL_REF_NONRECOVERABLE` | same; exact 20-path mode/target ledger must be tied to pinned commit |

Classification result: **11/11 classified; 0 fabricated source commits.**

### F. Causal classification

Primary: `SOURCE_PROVENANCE_FAILURE`.

Secondary: `EVIDENCE_FAILURE`.

This is not a `PRODUCT_FAILURE`: the acquisition intentionally fails closed on non-regular/special source topology. The forensic deficiency is that mutable `HEAD` plus an early exception leaves the exact acquired dependency commit absent from durable failed-state evidence.

### G. Minimal future StrategyDelta — prerequisite only, NOT authorized execution

When and only when an explicit future gate permits acquisition repair/replay, the minimum safe direction is:

1. Resolve official ref -> immutable dependency commit before any special-file scan.
2. Persist `{source_repo, requested_ref, resolved_commit}` durably before the scan can abort.
3. Scan and persist exact Git object mode/path/target metadata for special entries, then keep the existing fail-closed policy unless a reviewed component-specific strategy explicitly permits a safe representation.

This audit does **not** authorize changing the canonical acquisition engine now. It does not authorize bypassing special-file rejection, downloading B05/B06, or repairing the 11 failed components.

## STEP 3 — TEST / REFUTE / REPORT

### Specific tests executed

1. `QUEUE_REF_TEST`: B01/B02/B03/B04 acquisition queues inspected for the 11 components -> all use `source_ref: HEAD`.
2. `FAILED_STATE_PERSISTENCE_TEST`: B01/B02/B03/B04 failed states inspected -> early source-special failures do not provide a durable acquired `source_commit` equivalent to successful state entries.
3. `UPSTREAM_CURRENT_TOPOLOGY_TEST`: current official trees for `huggingface_hub` and `unstructured` checked -> current special/symlink topology corroborated, while historical attempt identity remains unresolved.
4. `ORCHESTRATOR_SHA_REFUTATION_TEST`: workflow/repository head SHA rejected as dependency source provenance.

### 3 simulations

**SIM-1 — replay mutable HEAD today**

Input: replay the same queue entry using `source_ref: HEAD` today.
Expected: the acquisition resolves today's upstream commit, not necessarily the historical commit used by the failed run.
Verdict: `ABSTAIN_HISTORICAL_IDENTITY`; replay cannot reconstruct old provenance.

**SIM-2 — observe mode 120000 in current official tree**

Input: current upstream shows a special path as mode `120000`.
Expected: classify as `CURRENT_SOURCE_SYMLINK_CORROBORATED` only.
Verdict: cannot promote to historical source-commit proof.

**SIM-3 — hypothetical pinned/pre-persisted acquisition**

Input: future authorized acquisition resolves and durably records immutable dependency commit before scanning.
Expected: if scan fails on a special entry, provenance remains replayable without weakening fail-closed special-file protection.
Verdict: prerequisite design would close the evidence gap for future runs; no production mutation performed here.

### 3 refutations

**REF-1 — “Actions run head SHA is the dependency source commit.”**

REFUTED. The run/head SHA belongs to `maxbry123-commits/osquestador-auditor`; it is not proof of the acquired third-party repository commit.

**REF-2 — “The B01-B03 special-path list proves every path is a symlink.”**

REFUTED. The ledger proves non-regular/special entries; exact Git mode must be proven per path/commit before naming all of them symlinks.

**REF-3 — “A modern B04 `main` symlink recovers the historical source snapshot.”**

REFUTED. Current topology corroborates the condition, but mutable `HEAD` plus missing pre-scan persisted commit means the historical attempt commit remains unknown.

### GOALS12_OUTPUT

| goal | verdict |
|---|---|
| G01 literal requirement preserved | PASS |
| G02 fresh HEAD read | PASS |
| G03 Handoff/STATE/CHECKPOINT/PLAN/Watchdog/DAG read | PASS |
| G04 owner/claim valid | PASS |
| G05 dependency/gate valid | PASS |
| G06 write_scope isolated | PASS |
| G07 evidence/code deduplicated | PASS |
| G08 minimal permitted delta | PASS |
| G09 specific causal tests executed | PASS |
| G10 three simulations + three refutations | PASS |
| G11 evidence + SHA + readback persisted | `POST_WRITE_READBACK_REQUIRED`; exact evidence commit/blob recorded in SOL-02 log and released claim |
| G12 node reconciliation | `SUPERVISOR_FANIN_REQUIRED`; worker cannot self-certify VERIFIED_CLOSED |

## COUNCIL12 — analytical review

1. **Objective:** classify the 11 source-special failures without manufacturing provenance.
2. **Requirement:** distinguish recoverable/current observations from historical source identity.
3. **Authority:** fresh physical tree/state/queues and official upstream evidence outrank old prose/chat.
4. **Physical state:** 11 failures remain failed; no repair is authorized.
5. **Owner:** SOL-2 owns only SW-N02 evidence/log/claim scope.
6. **Gates:** physical repair=false; B05/B06 download=false; Step3=false; canonical motors immutable.
7. **Collision risk:** controlled by atomic N02 claim; intervening node writes are disjoint.
8. **Causal GAP:** failed early scan + mutable HEAD + no durable pre-scan source_commit.
9. **Alternatives:** guessing from current HEAD, workflow SHA, timestamps, or LLM inference rejected.
10. **StrategyDelta:** future pre-scan immutable-commit persistence + exact special metadata; prerequisite only.
11. **Tests/refutations:** 4 causal checks, 3 simulations, 3 explicit refutations.
12. **Verdict:** `PASS_PENDING_SUPERVISOR_FANIN`; never `VERIFIED_CLOSED` by this producer.

## Report contract

- node_id: `SW-N02`
- chat_id: `chat-sol2-20260912T2306-0500`
- agent_name: `SOL-2-GPT`
- state: `PASS_PENDING_SUPERVISOR_FANIN`
- base_sha: `77e544c2d29bbb47b38573ce3fd7811d14cd63a2`
- final_sha: `POST_WRITE_READBACK_IN_SOL_02_LOG`
- write_scope: `SW-N02-EVIDENCE.md`, `SOL-SWARM-02-LOG.md`, `swarm-claims/CLAIM-SW-N02.json`
- paths_changed_this_step: `SW-N02-EVIDENCE.md`
- commit_sha: `POST_WRITE_READBACK_IN_SOL_02_LOG`
- blob_sha: `POST_WRITE_READBACK_IN_SOL_02_LOG`
- tests: `QUEUE_REF_TEST`, `FAILED_STATE_PERSISTENCE_TEST`, `UPSTREAM_CURRENT_TOPOLOGY_TEST`, `ORCHESTRATOR_SHA_REFUTATION_TEST`
- run_id: `N/A_READ_ONLY_CONNECTOR_AUDIT`
- job_id: `N/A_READ_ONLY_CONNECTOR_AUDIT`
- logs: `SOL-SWARM-02-LOG.md` after readback
- evidence: this file + cited canonical M23/M30/M32/M33/B04/queue/state artifacts
- simulations: `3/3`
- refutations: `3/3`
- remaining_gaps: historical dependency source commits for all 11 are not durably recoverable from current canonical failed-state evidence; production strategy remains gate-blocked
- gate_snapshot: unchanged / all three physical gates false
- review_required: `true`
- next_free_node: `RESCAN_AFTER_RELEASE`

## Final worker verdict

`PASS_PENDING_SUPERVISOR_FANIN`

SW-N02 establishes a fail-closed distinction: the special-file condition is real and partly/currently reproducible, but the exact historical dependency commit for all 11 failed attempts is not certified by the durable canonical evidence. No source commit was fabricated, no modern HEAD was substituted for history, and no production repair/download/wiring was performed.
