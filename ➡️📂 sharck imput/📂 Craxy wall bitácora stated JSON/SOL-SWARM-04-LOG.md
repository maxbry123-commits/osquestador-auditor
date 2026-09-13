# SOL-SWARM-04 LOG — SHARCK INPUT

- agent_name: `SOL-4-GPT`
- chat_id: `chat-sol4-20260912T2308-0500`
- state: `REPORT_READY_RELEASE_PENDING`
- active_node: `SW-N04`
- rule: claim only one `READY_TO_CLAIM` node from `SWARM-DAG-8SOL-M47-v1.json` after fresh read; write only this log + node-unique evidence + own claim; never write shared STATE/PLAN/CHECKPOINT/Handoff/Watchdog/DAG/queue.
- reserved nodes forbidden: `M06_ASTRA`, `M07_CLAUDE`, `M08_GROK`.
- physical mutation: `false`.

## 2026-09-12T23:12-05:00 — STEP 1 SYNC / VERIFY / CLAIM

- First safe candidate `SW-N03` collided during atomic create; exact read-back proved SOL-1 materialized `CLAIM-SW-N03.json` first.
- Response: `CLAIM_COLLISION → NO_OVERWRITE → READ_FRESH → NEXT_SAFE_FREE`.
- Fresh HEAD for next claim: `8be890dce641d42d4b1fb447f838b4e143b86667`.
- `SW-N04` exact claim path was absent before create.
- claim path: `swarm-claims/CLAIM-SW-N04.json`.
- claim commit: `de5f22df1e3c34fc33ebd3d2560f9dfd489890b2`.
- claim blob/readback: `dbb5d84021417c635595c12f6e8632eb75d8cbb6`.
- owner/readback: `SOL-4-GPT / SW-N04 / CLAIMED`.
- gate snapshot: physical repair=`false`; B05/B06 download=`false`; Step3=`false`; canonical motors=`IMMUTABLE`; shared control writes=`SOL-0_ONLY`.

## STEP 2 EXECUTE / VERIFY

- node: `SW-N04 — STRATEGYDELTA_SANDBOX_COVERAGE_EXPANSION_DESIGN`.
- causal class: `EVIDENCE_FAILURE` (coverage insufficiency), not proven product failure.
- evidence reused/deduplicated: M22 partial diff, M25 staging sandbox, M28 ignore/attributes causality, M35 coverage audit, B04 spaCy X-Ray.
- historical physical sandbox run read back: run `34568249222`, job `103164691377`, conclusion=`success`, head=`2499be177fd359825051a9dba4bc09c5cfad7b02`.
- exact historical workflow readback blob: `ca9b3f0c0cc2663ba85efcd28a649ce75634bdd6`.
- workflow gates Motor 3 exact blob `3689924361ce4a1a9fde4ae2b6f6009c37a6042d` before sandbox copy.
- exact coverage accounting: `12 components / 139 anomalies = 4 M25 sampled + 135 uncovered`.
- semantic correction: M25/M35 `3/12 components` = touched components; only spaCy is anomaly-complete. sqry and OpenSearch remain partially sampled.
- expansion design partitions uncovered set into `87 + 39 + 9 = 135` new anomaly checks, reaching design target `139/139` only if future sandbox execution passes.
- required future acceptance upgraded from anomaly replay to full invariant: `source_tracked_set == sandbox_staged_set == sandbox_committed_set`, bytes exact, exact Git mode equality, zero missing/extra/changed, Motor 3 pre/post hash unchanged.
- source-special/symlink lane explicitly excluded.

## STEP 3 TEST / REFUTE / REPORT

- T1 exact component arithmetic: PASS (`139`).
- T2 sampled/uncovered arithmetic: PASS (`4 + 135 = 139`).
- T3 batch partition: PASS (`87 + 39 + 9 = 135`).
- T4 12-component uniqueness/accounting: PASS.
- T5 partial-vs-special causal separation: PASS.
- T6 historical Actions run readback: PASS as M25 historical evidence only.
- T7 historical workflow/Motor 3 hash gate readback: PASS.
- T8 worker write-scope discipline: PASS; no product/component/motor/shared-control write.

### Simulations
1. `SIM-1` ignore-heavy: heritrix3(57)+sqry(21), fail on any missing/extra/byte/mode mismatch.
2. `SIM-2` mixed attributes/ignore: OpenSearch(4 missing+7 changed), require all 11 exact plus restored `.gitattributes` parity.
3. `SIM-3` heterogeneous remainder: yacy+nutch+kythe+scira+continue+datasketch+smolagents+pyserini with full tracked-set equality per component.

### Refutations
1. `REFUTE-1`: 139/139 known-anomaly replay can still miss newly damaged good paths → require full tracked-set equality.
2. `REFUTE-2`: unconstrained `git add -f` can overstage → require exact upstream tracked allowlist + zero extras; compare no-filter plumbing in sandbox.
3. `REFUTE-3`: byte equality can hide executable-mode loss → require exact source/staged/committed Git mode equality including `100755`.

## Evidence publication / readback

- evidence path: `SW-N04-EVIDENCE.md`.
- evidence commit: `954507ee91eb6dfa143b7d3d6434caa62521fb69`.
- evidence blob/readback: `2d8131a67a32396e1a7441db2fde330e5bf62492`.
- evidence worker verdict: `PASS_PENDING_SUPERVISOR_FANIN` for design/evidence reconciliation only.
- new expanded sandbox batches were **not** claimed as executed.
- achieved physical sandbox coverage remains historical M25: `3/12 touched`, `4/139`, only spaCy anomaly-complete.

## Concurrent HEAD advance reconciliation

- pre-evidence-write HEAD read: `985f6312cfe850a27c26a87b54373fe456d5eba2`.
- actual evidence commit parent: `b16022c24188298890afd45340f79875f8bedce4`.
- comparison `985f631... → b16022c...`: 4 intervening commits.
- intervening changed paths: `SOL-SWARM-02-LOG.md`, `SOL-SWARM-05-LOG.md`, `CLAIM-SW-N02.json`, `CLAIM-SW-N06.json` only.
- overlap with SW-N04/SOL-4 scope: `0`.
- result: `HEAD_ADVANCE_NON_OVERLAPPING_REVALIDATED`; evidence create landed on the newer parent and did not overwrite another writer.

## GOALS12_OUTPUT

- G01 literal requirement preserved: `PASS`
- G02 fresh HEAD/claim reads: `PASS`
- G03 mandatory control surfaces read: `PASS`
- G04 owner lock: `PASS`
- G05 gate/dependency valid: `PASS`
- G06 write scope non-overlap: `PASS`
- G07 dedup/reuse existing evidence: `PASS`
- G08 minimal allowed delta: `PASS`
- G09 specific evidence/coverage tests: `PASS`
- G10 3 simulations + 3 refutations: `PASS`
- G11 evidence SHA + readback persisted: `PASS`
- G12 release/next-node reconciliation: `PENDING_CLAIM_RELEASE`

## COUNCIL12 verdict

1. objective: expand safe coverage evidence — PASS design.
2. literal scope: sandbox-only — preserved.
3. authority: physical run/workflow/readbacks used.
4. state: 12/139 universe, 4 sampled.
5. owner: SOL-4 valid claim.
6. gates: remain false.
7. collision: N03 avoided; N04 unique.
8. causal GAP: evidence coverage insufficiency.
9. alternatives: constrained M25 staging vs no-filter plumbing comparison.
10. StrategyDelta: whole tracked-set parity, bytes+modes.
11. proof pressure: 8 checks + 3 simulations + 3 refutations.
12. verdict: `PASS_PENDING_SUPERVISOR_FANIN`; `KEEP_PHYSICAL_GATES_CLOSED`.

## Remaining gaps

- `G-SW-N04-EXECUTION`: expansion batches A/B/C not executed.
- `G-SW-N04-FULLSET`: whole tracked-set equality not demonstrated for all 12.
- `G-SW-N04-MODES`: `100755` preservation still needs execution coverage.
- `G-SW-N04-PLUMBING-COMPARE`: no-filter plumbing alternative is design-only.
- `G-SW-N04-REVIEWS`: M06 ASTRA + M07 CLAUDE + M08 GROK + director gate still required.

release_action: update own claim to `RELEASED` after fresh claim SHA read and readback; then rescan next FREE node without claiming overlapping work.
