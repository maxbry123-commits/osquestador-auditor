# SW-N04 EVIDENCE — STRATEGYDELTA SANDBOX COVERAGE EXPANSION DESIGN

- schema: `sharck-input.swarm-evidence.v1`
- node_id: `SW-N04`
- parent_node: `M47_8SOL_SWARM_CONTROL_PLANE`
- agent_name: `SOL-4-GPT`
- chat_id: `chat-sol4-20260912T2308-0500`
- mode: `SANDBOX_ONLY`
- base_sha_at_claim: `8be890dce641d42d4b1fb447f838b4e143b86667`
- claim_commit: `de5f22df1e3c34fc33ebd3d2560f9dfd489890b2`
- claim_blob: `dbb5d84021417c635595c12f6e8632eb75d8cbb6`
- causal_class: `EVIDENCE_FAILURE`
- product_failure: `NOT_PROVEN`
- physical_mutation: `false`
- canonical_destinations_touched: `false`
- canonical_motors_modified: `false`
- B05_B06_downloads: `0`
- shared_control_writes: `0`

## Assertion under test

M25 proved a viable staging StrategyDelta on a representative sandbox sample, but the evidence coverage is too small for production. This node tests whether the uncovered partial universe can be partitioned into a complete, fail-closed sandbox validation matrix without mutating canonical destinations or motors.

## Authority / fresh evidence used

1. `STAGING-STRATEGYDELTA-SANDBOX-2026-09-11.md`
   - workflow `.github/workflows/sharck-input-staging-strategydelta-lite.yml`
   - commit `2499be177fd359825051a9dba4bc09c5cfad7b02`
   - run `34568249222`, job `103164691377`, conclusion `success`
   - Motor 3 expected canonical blob `3689924361ce4a1a9fde4ae2b6f6009c37a6042d`
   - pinned sources: spaCy `26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`, OpenSearch `0249cde03ef66b56ac61e8929c3ba7e10b062523`, sqry `631710ce145b6ef6adb527dda13ac60e20be16cf`
2. `STRATEGYDELTA-COVERAGE-AUDIT-2026-09-11.md`
   - partial universe `12 components / 139 exact anomalies`
   - M25 direct sample `3/12 components touched / 4/139 anomalies`
3. `PARTIALS-XRAY-11-2026-09-11.md`
   - run `34567075204`
   - `130 missing + 7 changed + 0 extra`
   - exact source commits per 11 B01–B03 partials
4. `B04-XRAY-2026-09-11.md`
   - spaCy adds exactly two missing paths at source commit `26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`
5. `NESTED-IGNORE-BLAST-RADIUS-2026-09-11.md`
   - `130/130` missing explained by ignore rules
   - `7/7` changed explained separately by attributes / CRLF→LF
6. Fresh GitHub Actions read-back of run `34568249222` confirms completed/success at head `2499be177fd359825051a9dba4bc09c5cfad7b02`.
7. Exact historical workflow read-back at that commit has blob `ca9b3f0c0cc2663ba85efcd28a649ce75634bdd6` and explicitly gates Motor 3 hash to `3689924361ce4a1a9fde4ae2b6f6009c37a6042d` before sandbox copy.

## STEP 1 — SYNC / VERIFY / CLAIM

Claim collision handling was exercised in reality:
- `SW-N03` appeared free during preflight but SOL-1 materialized its claim first.
- SOL-4 did not overwrite it, reread fresh main, moved to `SW-N04`, created the unique lock and performed read-back.
- `SW-N04` claim is therefore an atomic non-overlapping owner lock.

Gate snapshot remains:
- `physical_repair_allowed=false`
- `b05_b06_download_allowed=false`
- `step3_allowed=false`
- `canonical_motors=IMMUTABLE`
- shared control plane writes=`SOL-0_ONLY`

## STEP 2 — EXECUTE / VERIFY

### A. Exact coverage accounting

| Component | Exact anomalies | M25 directly sampled | Uncovered after M25 | Causal surface |
|---|---:|---:|---:|---|
| spaCy | 2 | 2 | 0 | ignore/staging |
| sqry | 21 | 1 | 20 | root `build/` ignore |
| OpenSearch | 11 | 1 | 10 | 4 `.idea` missing + 7 attributes-changed |
| heritrix3 | 57 | 0 | 57 | root `dist/` ignore |
| yacy_search_server | 5 | 0 | 5 | root/nested ignore |
| nutch | 3 | 0 | 3 | nested config/ivy ignore |
| kythe | 14 | 0 | 14 | build/class/vscode/vendor ignores |
| scira | 12 | 0 | 12 | `*.sql` ignore |
| continue | 5 | 0 | 5 | `*.iml` + nested webview ignore |
| datasketch | 5 | 0 | 5 | benchmark PNG ignore |
| smolagents | 1 | 0 | 1 | test-data ignore |
| pyserini | 3 | 0 | 3 | sentinel paths ignored |
| **TOTAL** | **139** | **4** | **135** | — |

Arithmetic invariant: `139 = 4 already sampled + 135 uncovered`.

Important semantic correction: M35's `3/12 components` means **touched components**, not three fully covered component trees. Only spaCy is anomaly-complete under M25; sqry and OpenSearch remain partial. Production review must not reinterpret `3/12 touched` as `3/12 fully closed`.

### B. Sandbox expansion batches

The expansion is intentionally staged by risk/criticality. This node designs the executable sandbox contract; it does **not** claim these unexecuted batches passed.

#### Batch A — critical acquisition/staging classes
- sqry remaining `20`
- OpenSearch remaining `10`
- heritrix3 `57`
- new anomalies exercised if executed: `87`
- cumulative anomaly target including M25: `91/139`
- fully anomaly-covered component target: `4/12` = spaCy + sqry + OpenSearch + heritrix3

#### Batch B — build/runtime/schema classes
- yacy_search_server `5`
- nutch `3`
- kythe `14`
- scira `12`
- continue `5`
- new anomalies exercised if executed: `39`
- cumulative anomaly target: `130/139`
- fully anomaly-covered component target: `9/12`

#### Batch C — benchmark/test/sentinel parity
- datasketch `5`
- smolagents `1`
- pyserini `3`
- new anomalies exercised if executed: `9`
- cumulative anomaly target: `139/139`
- fully anomaly-covered component target: `12/12`

### C. Required per-component sandbox test contract

For each of the 12 partial components:

1. **PIN / ENUMERATE**
   - use the already persisted exact `source_commit`;
   - enumerate upstream tracked paths, Git mode and blob identity from that commit;
   - fail closed if a special-file mode is encountered in this partial lane; special/symlink classes remain routed to their separate provenance/StrategyDelta lane.
2. **COPY WITH IMMUTABLE MOTOR**
   - verify Motor 3 blob exactly `3689924361ce4a1a9fde4ae2b6f6009c37a6042d` immediately before sandbox copy;
   - copy only into an isolated ephemeral sandbox, never a canonical destination.
3. **STAGE EXACT TRACKED SET**
   - Candidate A: reproduce M25 but constrain forced staging to the exact upstream tracked allowlist and neutralize attributes only within the ephemeral staging operation;
   - Candidate B for comparative sandbox evaluation: Git plumbing (`hash-object --no-filters` + explicit index/tree construction) so ignore/attributes cannot silently transform source bytes;
   - neither candidate is authorized for production by this document.
4. **FULL READBACK**
   - require `source_tracked_set == sandbox_staged_set == sandbox_committed_set`;
   - missing=`0`, extra=`0`, changed bytes=`0`;
   - require per-path byte/blob equality;
   - require exact source Git mode equality (`100644`/`100755` where applicable), not merely membership in an allowed mode set;
   - require component-level file count/tree digest consistency.
5. **SAFETY READBACK**
   - re-hash Motor 3 after sandbox operation and require unchanged blob;
   - no LFS, no force, no source-ref change, no canonical destination write, no shared control-plane write.

### D. Why anomaly-only checking is insufficient

A future `139/139` anomaly replay is necessary but not sufficient. Production-quality evidence must also compare the **entire upstream tracked set** for every component because a candidate staging wrapper could accidentally introduce a new omission or extra path outside the known 139 anomaly set.

## STEP 3 — TEST / REFUTE / REPORT

### Static / evidence tests executed by this node

- **T1 Coverage arithmetic:** per-component totals sum to `139`; M25 samples sum to `4`; uncovered sum is `135` — PASS.
- **T2 Partition arithmetic:** proposed new batches `87 + 39 + 9 = 135`; adding M25's `4` yields `139` — PASS.
- **T3 Component accounting:** exactly 12 partial components are represented once in the matrix — PASS.
- **T4 Causal separation:** partial lane contains ignore/attributes/spaCy partials only; source-special/symlink failures are not merged — PASS.
- **T5 Historical run verification:** GitHub Actions run `34568249222` is physically read back as `completed/success` on exact historical head `2499be177...` — PASS as historical M25 evidence only.
- **T6 Historical workflow/motor gate verification:** exact workflow read-back contains a pre-copy `git hash-object` equality check against Motor 3 blob `368992...` — PASS.
- **T7 Canonical mutation test:** this worker changed no component destination, motor, source ref, B05/B06 acquisition, STATE/PLAN/CHECKPOINT/Handoff/Watchdog/DAG/queue — PASS by write-scope discipline.

### Three simulations

1. **SIM-1 — ignore-heavy critical trees:** heritrix3(57) + sqry(21). Expected candidate acceptance requires every upstream tracked path staged with byte+mode parity and zero extras. A single missing path fails the component.
2. **SIM-2 — attributes + ignore mixed tree:** OpenSearch(4 missing + 7 changed). Expected candidate acceptance requires all 11 known anomalies resolved simultaneously and all seven changed files byte-identical to source; temporary attribute handling must leave the restored `.gitattributes` itself exact.
3. **SIM-3 — heterogeneous remaining classes:** yacy+nutch+kythe+scira+continue+datasketch+smolagents+pyserini, with existing spaCy evidence retained. Expected acceptance requires per-component full tracked-set equality; low functional criticality does not permit dropping tracked benchmark/test/sentinel files from evidence parity.

These are **design simulations**, not claims of newly executed sandbox runs.

### Three refutations

1. **REFUTE-1 — `139/139` anomaly replay could still be a false PASS.** A staging change may damage a previously-good tracked path. Countermeasure: compare the entire tracked upstream set, not only the known anomaly list.
2. **REFUTE-2 — `git add -f` could overstage unintended files.** A green byte check on selected paths does not prove absence of extras. Countermeasure: constrain staging to the exact upstream tracked allowlist and require staged-set equality; compare a plumbing-based no-filter strategy in sandbox.
3. **REFUTE-3 — byte equality can hide executable-mode loss.** Countermeasure: require exact source-vs-staged-vs-committed Git mode per path, including `100755`, plus byte/blob equality.

Additional boundary: no result from this partial-lane strategy may be extrapolated to source-special/symlink failures.

## GOALS12_OUTPUT

- G01 literal requirement preserved: `PASS`
- G02 fresh HEAD read before claim/write: `PASS`
- G03 Handoff/STATE/CHECKPOINT/PLAN/Watchdog/DAG read: `PASS`
- G04 owner lock: `PASS` (`SW-N04`, SOL-4 only)
- G05 dependency/gate validity: `PASS` (`SANDBOX_ONLY`; all physical gates remain false)
- G06 write scope non-colliding: `PASS`
- G07 existing evidence reused/deduplicated: `PASS`
- G08 delta minimal/permitted: `PASS` (evidence + own log/claim only)
- G09 specific tests: `PASS` for design/evidence tests; expansion execution remains future sandbox work
- G10 3 simulations + 3 refutations: `PASS`
- G11 evidence + SHA + readback: `PENDING_WRITE_READBACK` at document construction, to be filled by physical read-back metadata in owner log/claim completion
- G12 state/next node reconciliation: `PENDING_RELEASE` at document construction

## COUNCIL12

1. **Objective:** expand M25 coverage evidence safely before any production repair.
2. **Requirement:** no canonical mutation; exact 3-step worker contract.
3. **Authority:** physical run/workflow/readbacks + M22/M25/M28/M35 evidence outrank chat inference.
4. **Physical state:** 12 partial components / 139 anomalies; 4 anomalies directly sampled by M25.
5. **Owner:** SOL-4 owns only SW-N04 after atomic claim readback.
6. **Gates:** physical repair, B05/B06 download and Step3 remain false.
7. **Collision risk:** controlled by unique evidence/log/claim paths; N03 collision was correctly aborted.
8. **Causal GAP:** `EVIDENCE_FAILURE` — representative staging viability exists, coverage is insufficient.
9. **Alternatives:** constrained M25 forced staging vs no-filter Git plumbing; both sandbox-only until independent review.
10. **StrategyDelta:** validate full tracked sets component-by-component, bytes and exact modes, with special files excluded.
11. **Tests/refutations:** seven evidence/static checks + three simulations + three explicit refutations.
12. **Verdict:** `PASS_PENDING_SUPERVISOR_FANIN` for the **coverage-expansion design and evidence reconciliation only**; production and unexecuted expanded sandbox batches remain open.

## Remaining gaps / gate recommendation

- `G-SW-N04-EXECUTION`: Batches A/B/C have not been executed by this worker; achieved physical coverage remains M25's `3/12 touched` and `4/139`, with only spaCy anomaly-complete.
- `G-SW-N04-FULLSET`: full tracked-set equality has not yet been demonstrated for all 12 components.
- `G-SW-N04-MODES`: exact executable `100755` preservation remains to be exercised where present.
- `G-SW-N04-PLUMBING-COMPARE`: no-filter plumbing alternative is design-only and must be independently sandbox-tested.
- `G-SW-N04-REVIEWS`: M06 ASTRA + M07 CLAUDE + M08 GROK + director gate remain required.

Recommendation: `KEEP_PHYSICAL_GATES_CLOSED`. Even a future `12/12 + 139/139` sandbox PASS would be review evidence, not production authorization; any eventual physical repair still requires explicit gate opening and canonical full read-back.

## Worker verdict

`PASS_PENDING_SUPERVISOR_FANIN`

No `VERIFIED_CLOSED` is asserted by SOL-4.
