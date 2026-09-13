# SOL-SWARM-04 LOG — SHARCK INPUT

- agent_name: `SOL-4-GPT`
- chat_id: `chat-sol4-20260912T2308-0500`
- state: `RELEASED_RESCAN_PENDING`
- active_node: `null`
- rule: claim only one current Crazy Wall `READY_TO_CLAIM` node after fresh read; write only this log + node-unique evidence + own claim; never write shared STATE/PLAN/CHECKPOINT/Handoff/Watchdog/DAG/queue.
- reserved nodes forbidden: `M06_ASTRA`, `M07_CLAUDE`, `M08_GROK`.
- physical mutation: `false`.

## 2026-09-12T23:12-05:00 — STEP 1 SYNC / VERIFY / CLAIM — SW-N04

- First safe candidate `SW-N03` collided during atomic create; exact read-back proved SOL-1 materialized `CLAIM-SW-N03.json` first.
- Response: `CLAIM_COLLISION → NO_OVERWRITE → READ_FRESH → NEXT_SAFE_FREE`.
- Fresh HEAD for next claim: `8be890dce641d42d4b1fb447f838b4e143b86667`.
- `SW-N04` exact claim path was absent before create.
- claim path: `swarm-claims/CLAIM-SW-N04.json`.
- claim commit: `de5f22df1e3c34fc33ebd3d2560f9dfd489890b2`.
- claim blob/readback: `dbb5d84021417c635595c12f6e8632eb75d8cbb6`.
- owner/readback: `SOL-4-GPT / SW-N04 / CLAIMED`.
- gate snapshot: physical repair=`false`; B05/B06 download=`false`; Step3=`false`; canonical motors=`IMMUTABLE`; shared control writes=`SOL-0_ONLY`.

## SW-N04 STEP 2 EXECUTE / VERIFY

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

## SW-N04 STEP 3 TEST / REFUTE / REPORT

- T1 exact component arithmetic: PASS (`139`).
- T2 sampled/uncovered arithmetic: PASS (`4 + 135 = 139`).
- T3 batch partition: PASS (`87 + 39 + 9 = 135`).
- T4 12-component uniqueness/accounting: PASS.
- T5 partial-vs-special causal separation: PASS.
- T6 historical Actions run readback: PASS as M25 historical evidence only.
- T7 historical workflow/Motor 3 hash gate readback: PASS.
- T8 worker write-scope discipline: PASS; no product/component/motor/shared-control write.

### SW-N04 simulations
1. `SIM-1` ignore-heavy: heritrix3(57)+sqry(21), fail on any missing/extra/byte/mode mismatch.
2. `SIM-2` mixed attributes/ignore: OpenSearch(4 missing+7 changed), require all 11 exact plus restored `.gitattributes` parity.
3. `SIM-3` heterogeneous remainder: yacy+nutch+kythe+scira+continue+datasketch+smolagents+pyserini with full tracked-set equality per component.

### SW-N04 refutations
1. `REFUTE-1`: 139/139 known-anomaly replay can still miss newly damaged good paths → require full tracked-set equality.
2. `REFUTE-2`: unconstrained `git add -f` can overstage → require exact upstream tracked allowlist + zero extras; compare no-filter plumbing in sandbox.
3. `REFUTE-3`: byte equality can hide executable-mode loss → require exact source/staged/committed Git mode equality including `100755`.

## SW-N04 evidence publication / readback

- evidence path: `SW-N04-EVIDENCE.md`.
- evidence commit: `954507ee91eb6dfa143b7d3d6434caa62521fb69`.
- evidence blob/readback: `2d8131a67a32396e1a7441db2fde330e5bf62492`.
- evidence worker verdict: `PASS_PENDING_SUPERVISOR_FANIN` for design/evidence reconciliation only.
- new expanded sandbox batches were **not** claimed as executed.
- achieved physical sandbox coverage remains historical M25: `3/12 touched`, `4/139`, only spaCy anomaly-complete.

## SW-N04 concurrent HEAD advance reconciliation

- pre-evidence-write HEAD read: `985f6312cfe850a27c26a87b54373fe456d5eba2`.
- actual evidence commit parent: `b16022c24188298890afd45340f79875f8bedce4`.
- comparison `985f631... → b16022c...`: 4 intervening commits.
- intervening changed paths: `SOL-SWARM-02-LOG.md`, `SOL-SWARM-05-LOG.md`, `CLAIM-SW-N02.json`, `CLAIM-SW-N06.json` only.
- overlap with SW-N04/SOL-4 scope: `0`.
- result: `HEAD_ADVANCE_NON_OVERLAPPING_REVALIDATED`.

## SW-N04 GOALS12_OUTPUT

- G01 literal requirement preserved: `PASS`
- G02 fresh HEAD/claim reads: `PASS`
- G03 mandatory control surfaces read: `PASS`
- G04 owner lock: `PASS`
- G05 gate/dependency valid: `PASS`
- G06 write scope non-overlap: `PASS`
- G07 dedup/reuse existing evidence: `PASS`
- G08 minimal allowed delta: `PASS`
- G09 specific evidence/coverage tests: `PASS_DESIGN_EVIDENCE_ONLY`
- G10 3 simulations + 3 refutations: `PASS`
- G11 evidence SHA + readback persisted: `PASS`
- G12 release/next-node reconciliation: `PASS_NO_SAFE_FREE_NODE_AT_RESCAN`

## SW-N04 COUNCIL12 verdict

1. objective: expand safe coverage evidence — PASS design.
2. literal scope: sandbox-only — preserved.
3. authority: physical run/workflow/readbacks used.
4. state: 12/139 universe, 4 sampled.
5. owner: SOL-4 valid claim, now released.
6. gates: remain false.
7. collision: N03 avoided; N04 unique.
8. causal GAP: evidence coverage insufficiency.
9. alternatives: constrained M25 staging vs no-filter plumbing comparison.
10. StrategyDelta: whole tracked-set parity, bytes+modes.
11. proof pressure: 8 checks + 3 simulations + 3 refutations.
12. verdict: `PASS_PENDING_SUPERVISOR_FANIN`; `KEEP_PHYSICAL_GATES_CLOSED`.

## SW-N04 remaining gaps

- `G-SW-N04-EXECUTION`: expansion batches A/B/C not executed.
- `G-SW-N04-FULLSET`: whole tracked-set equality not demonstrated for all 12.
- `G-SW-N04-MODES`: `100755` preservation still needs execution coverage.
- `G-SW-N04-PLUMBING-COMPARE`: no-filter plumbing alternative is design-only.
- `G-SW-N04-REVIEWS`: M06 ASTRA + M07 CLAUDE + M08 GROK + director gate still required.

## SW-N04 Release / next-free rescan — 2026-09-12T23:16-05:00

- claim release commit: `8b4e8397e7e6277e77d2d08718a5f813cec8e51e`.
- released claim blob/readback: `6769564e35157d6ce5ed17bca5c143b30a289c37`.
- claim state readback: `RELEASED`.
- fresh main after release/rescan: `24e4cdea4b2a001fd60e41f3117dc1bd5f9b1bc0`.
- claim directory then materialized `SW-N01` through `SW-N08`.
- `next_free_node`: `NONE_SAFE_FREE_AT_RESCAN` at that historical point.

## SW-N04 Crazy Wall report fields

- node_id: `SW-N04`
- chat_id: `chat-sol4-20260912T2308-0500`
- agent_name: `SOL-4-GPT`
- state: `RELEASED` with result `PASS_PENDING_SUPERVISOR_FANIN`
- base_sha: `8be890dce641d42d4b1fb447f838b4e143b86667`
- claim_commit: `de5f22df1e3c34fc33ebd3d2560f9dfd489890b2`
- evidence_commit: `954507ee91eb6dfa143b7d3d6434caa62521fb69`
- report_commit: `f6faea6e4d2e602795b96d60669748796ca8aa0b`
- release_commit: `8b4e8397e7e6277e77d2d08718a5f813cec8e51e`
- evidence_blob: `2d8131a67a32396e1a7441db2fde330e5bf62492`
- released_claim_blob: `6769564e35157d6ce5ed17bca5c143b30a289c37`
- tests: `8 PASS` within design/evidence scope
- run_id/job_id: historical M25 supporting evidence only (`34568249222` / `103164691377`)
- simulations: `3`
- refutations: `3`
- gate_snapshot: physical repair=false; B05/B06=false; Step3=false; canonical motors immutable
- review_required: `SOL-0 supervisor fan-in`.

---

## 2026-09-12T23:30:20-05:00 — SW-N19 CLAIM / M48→M50 REVALIDATION

- M48 queue scan: N14/N15/N16/N17/N18 were already physically claimed by other workers after collision-safe fresh reads.
- `SW-N19` was the first safe FREE node at the successful claim point.
- claim base SHA: `ac038d8c4d9763ac579c6ba6a9c9001f9169e955`.
- atomic claim commit: `ffdfe3ef233aaa137327485aa98500511cdf3a8c`.
- claim readback owner: `SOL-4-GPT`.
- node mode: `READ_ONLY_RESEARCH`.
- task: `RUNTIME_CANDIDATE_SPECIAL_SURFACE_SCAN`.
- During execution control plane advanced to M50. Fresh `CRAZY-WALL-SWARM-QUEUE-M50.json` explicitly retained `SW-N19 / SOL-4-GPT` and declared live claim files authoritative. Node remained valid.
- claim-base→pre-report comparison contained 23 concurrent commits but zero other-writer overlap with `SW-N19-EVIDENCE.md` or this SOL-4 log.

## SW-N19 STEP 1 — N06 KEEP/REFERENCE SET

- OpenHands Software Agent SDK — KEEP.
- mini-SWE-agent — KEEP.
- Continue — KEEP_EXISTING_117 / no duplicate.
- OpenClaw — REFERENCE.
- Agent Skills — REFERENCE.
- OpenAI Agents SDK — REFERENCE.
- DEFER/REJECT candidates were not silently promoted into this node.

## SW-N19 STEP 2 — SPECIAL SURFACE / LICENSE / REF

- OpenHands: commit `c37007429be8b4465a83487dc1fd0914df0ea734`; MIT; no symlink/submodule observed in current recursive scan; no `.gitattributes` observed.
- mini-SWE-agent: commit `04d809ceab9df28f9adaed044884180159172930`; MIT from `LICENSE.md`; no symlink/submodule observed; no `.gitattributes` observed.
- Continue: commit `5522c6f44ca0ac3528b37244818fbfa39b5af470`; Apache-2.0; no symlink/submodule observed; existing canonical component only, no duplicate acquisition.
- OpenClaw: current commit `9ef7fb4ccc8f9f09dd2bd6c5331b7c0918e48da9`; MIT; current tree contains mode `120000` symlink surface; root `.gitmodules` absent; root `.gitattributes` has no LFS filter. N06 pin `f369c90e...` remains a valid historical commit but current `main` is 5 commits ahead.
- Agent Skills: commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379`; Apache-2.0; `CLAUDE.md` mode `120000` observed; `.gitmodules`/root `.gitattributes` absent.
- OpenAI Agents SDK: commit `fbd2dbcaaf74a2c447c6d3fa9d5645d83fd7e292`; MIT; no symlink/submodule observed; `.gitattributes`=`* text=auto eol=lf`, therefore future vendoring would require byte-safe readback.
- Cross-repo `filter=lfs` search returned one OpenClaw test-fixture mock occurrence, not an actual repository LFS policy.

## SW-N19 STEP 3 — TEST / REFUTE / REPORT

Specific tests: `11/11 PASS` inside read-only preflight scope.

### Simulations
1. KEEP candidate future sandbox must repin + rescan special modes before any gate.
2. Blind full-repo vendoring of current OpenClaw/Agent Skills is expected to fail the canonical special-file gate; therefore preserve REFERENCE-only.
3. OpenAI Agents SDK ordinary Git staging can normalize line endings; any future promotion must compare source/staged/published bytes+modes.

### Refutations
1. Hypothesis `N06 immutable pins are tree SHAs` → **REFUTED**; N06 rows inspected use commit SHAs, distinct from tree SHAs.
2. Hypothesis `REFERENCE_ONLY makes special-file scan unnecessary` → **REFUTED** by current OpenClaw/Agent Skills symlinks.
3. Hypothesis `filter=lfs search hit proves OpenClaw uses LFS` → **REFUTED**; hit belongs to a test fixture and inspected root attributes contain no LFS filter.

## SW-N19 evidence / release

- evidence path: `SW-N19-EVIDENCE.md`.
- evidence commit: `5622020669cc3221abc50024816266e8186cf111`.
- evidence blob/readback: `67b20280b0acfccb6c4b7a10927f60532c11b7cd`.
- worker verdict: `PASS_PENDING_SUPERVISOR_FANIN`.
- physical/acquisition mutation: `false`.
- release commit: `7ac2876c8e20034f813dd493e43d1d763bd7e870`.
- released claim blob: `65a022e57a16adaa3326f3f912fe2fcd23f00700`.
- released_at: `2026-09-12T23:35:51-05:00`.
- review_required: `SOL-0 supervisor fan-in`.
- gates recommendation: `KEEP_PHYSICAL_GATES_CLOSED`.

## SW-N19 GOALS12_OUTPUT

- G01 requirement preserved: `PASS`
- G02 fresh HEAD reads: `PASS`
- G03 current M48/M50 control surfaces + N06 evidence read: `PASS`
- G04 atomic owner claim/readback: `PASS`
- G05 dependency/gates valid: `PASS`
- G06 write scope non-overlap: `PASS`
- G07 candidate set deduplicated: `PASS`
- G08 minimal read-only delta: `PASS`
- G09 specific topology/license/ref tests: `PASS`
- G10 3 simulations + 3 refutations: `PASS`
- G11 evidence SHA/readback persisted: `PASS`
- G12 claim released: `PASS`; next-node rescan pending immediately after this log write.

## SW-N19 COUNCIL12

1. objective: current special-surface preflight — PASS.
2. literal scope: six N06 KEEP/REFERENCE candidates only — PASS.
3. authority: official immutable GitHub refs/tree/license + Crazy Wall — PASS.
4. physical state: no download/wire/repair — PASS.
5. owner: valid SOL-4 claim, now released.
6. gates: false/immutable preserved.
7. collision: concurrent work non-overlapping.
8. causal gap: N06 special/LFS surface uncertainty — resolved for current snapshot with explicit residual future-drift limit.
9. alternatives: reference/pointer, or later gated subtree/package/sandbox rather than blind vendoring.
10. StrategyDelta: repin and rescan immediately before any future approval.
11. proof pressure: 11 tests + 3 simulations + 3 refutations.
12. verdict: `PASS_PENDING_SUPERVISOR_FANIN`; never `VERIFIED_CLOSED` by producer.
