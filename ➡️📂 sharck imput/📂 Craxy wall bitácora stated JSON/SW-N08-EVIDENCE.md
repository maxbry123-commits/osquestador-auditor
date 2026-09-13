# SW-N08 EVIDENCE — CONTROL PLANE CONTRADICTION / DRIFT WATCH

- schema: `sharck-input.swarm-node-evidence.v1`
- agent_name: `SOL-1-GPT`
- chat_id: `chat-sol1-20260912T2305-0500`
- node_id: `SW-N08`
- task: `CONTROL_PLANE_CONTRADICTION_WATCH`
- mode: `READ_ONLY_CONTROL`
- claim_commit: `7ec9bec5c4839f3c57d219514048668f7cfc8608`
- claim_blob: `776f2056da705b3ad90af6906c0153d07922996e`
- base_sha: `063e054c51e5214b28608ca0719969f0b827575e`
- fresh_head_before_evidence_write: `526857e6965715613c3766ecb11ed7514d202e7c`
- stale-head revalidation: `PASS`; intervening commits are worker-local evidence/log/release operations with no N08 write-scope collision.
- primary_classification: `CONTROL_PLANE_DRIFT`
- shared_control_write: `false`
- physical_mutation: `false`

## STEP 1 — SYNC / VERIFY / CLAIM

Atomic N08 claim was created and read back before material work.

Control surfaces compared:
- `STATE-DELTA-036-M47-8SOL-SWARM-CONTROL.json` blob `6504d56a2ea2d71e38e0896e8f828ecee74c7cac`.
- `CHECKPOINT-DELTA-034-M47-8SOL-SWARM-CONTROL.json` blob `816a6f7abe15c302e782816a4371475065f03e0f`.
- `PLAN-DELTA-018-M47-8SOL-SWARM-CONTROL.json` blob `59328018fcbec1999e07c345eab515b4228ff4fd`.
- `HANDOFF-MULTIENV-3STEP-20X-2026-09-11.md` blob `8327f27672ea54b2cb04a61737a0277025dc7ba7`.
- `RECOVERY-MULTI-ENV-SHARCK-INPUT.md` blob `d31e65c8eac9e592528479d3f7617d21c8accedc` plus root recovery previously read in this worker boot.
- `SWARM-DAG-8SOL-M47-v1.json` blob `eee95bc7e3e46c17725b33fd0b9224ed3dcde243`.
- current queue and `swarm-claims/` physical tree.
- worker logs/evidence required to distinguish lock-presence from current worker activity.

### GOALS12_INPUT
- G01 literal requirement preserved: PASS.
- G02 fresh HEAD read: PASS.
- G03 STATE/CHECKPOINT/PLAN/Handoff/Recovery/DAG + claims/logs read: PASS.
- G04 N08 atomic owner lock: PASS.
- G05 read-only gate valid: PASS.
- G06 write scope isolated: PASS.
- G07 current worker evidence used before declaring drift: PASS.
- G08 minimum permitted delta: evidence/log only.
- G09 contradiction matrix defined: PASS.
- G10 three simulations + three refutations required: PASS.
- G11 SHA/readback required: claim PASS; evidence/log readback follows.
- G12 supervisor reconciliation required: PASS.

## STEP 2 — EXECUTE / VERIFY

### A. Stable facts — NO contradiction

The following remain mutually consistent across current M47 control surfaces and fresh physical evidence:

- canonical catalog = `117`.
- B01-B04 = `17 VERIFIED_CLOSED / 23 FAILED`.
- failed split = `12 partial + 11 source-special/symlink`.
- partial universe = `12 components / 139 exact anomalies`.
- B05/B06 = `20 researched / 0 downloaded`.
- M06/M07/M08 remain reserved to `ASTRA / CLAUDE / GROK`.
- `physical_repair_allowed=false`.
- `b05_b06_download_allowed=false`.
- `step3_allowed=false`.
- canonical motors remain immutable.
- N04 did NOT physically expand M25 sandbox coverage: its evidence explicitly leaves achieved physical coverage at `3/12 touched / 4/139 anomalies`; proposed batches are design-only. Therefore the M47 coverage snapshot is still physically valid.

### B. Fresh live worker/claim snapshot

The physical claim namespace now contains **all eight** locks `CLAIM-SW-N01.json` through `CLAIM-SW-N08.json`.

Fresh worker/evidence status visible before this evidence write:
- `SW-N01`: SOL-1 evidence complete, worker scope released to supervisor fan-in.
- `SW-N02`: SOL-2 evidence complete, released.
- `SW-N03`: SOL-1 evidence complete, worker scope released.
- `SW-N04`: SOL-4 evidence complete, released/rescanned.
- `SW-N05`: SOL-1 evidence complete, worker scope released.
- `SW-N06`: SOL-6 currently `ACTIVE_CLAIMED` in own log.
- `SW-N07`: evidence/readback PASS, `CLAIMED_RELEASE_PENDING` in SOL-2 log at fresh read.
- `SW-N08`: active under SOL-1 until this report/readback/release.

Therefore there is currently **no legally free N01-N08 node** despite static/shared surfaces still describing the original eight-node READY set.

### C. Drift / contradiction matrix

| ID | severity | surface | finding | safety effect | reconciliation proposal for SOL-0 |
|---|---|---|---|---|---|
| `DRIFT-01` | HIGH operational | queue + PLAN/Handoff/DAG summary vs claim tree | shared/static surfaces still present N01-N08 as READY while eight physical claim locks now exist | a worker relying only on READY text could attempt collision; atomic lock readback currently prevents overwrite | next supervisor delta/queue reconciliation must distinguish `READY_FREE`, `LOCK_PRESENT_ACTIVE`, `WORKER_PASS_PENDING_FANIN`, `RELEASED_LOCK_RETAINED` |
| `DRIFT-02` | HIGH operational | `PLAN-DELTA-018` | `next_action` still instructs SOL-1..8 to claim distinct N01..N08 | instruction is temporally stale after claims | next versioned PLAN delta should replace initial-dispatch instruction with fan-in/current-worker-status instruction |
| `DRIFT-03` | MEDIUM | Handoff | verdict still says `8_SAFE_READY_NODES` although all eight locks exist | snapshot wording is stale, but Handoff also mandates reading claims/logs, which preserves safety | update Handoff only by SOL-0 after worker fan-in; retain physical gates unchanged |
| `DRIFT-04` | MEDIUM | Recovery Multi-Env | explicit source pointers/frontier still cite M42/M43 deltas/checkpoint while current control node is M47 | recovery agent could begin from stale pointers unless it obeys higher-authority latest Handoff/delta rule | publish versioned recovery reconciliation pointing to latest M47-or-later STATE/CHECKPOINT/PLAN and atomic-claim semantics |
| `DRIFT-05` | LOW / historical snapshot | STATE/CHECKPOINT | `active_claims_at_creation=0` / `active_claims_at_checkpoint=0` no longer describes live claim count | not a false historical record; dangerous only if misread as current telemetry | preserve old delta/checkpoint; add newer versioned delta/checkpoint rather than rewriting history |
| `DRIFT-06` | LOW / schema semantics | SWARM-DAG | node definitions retain `READY_TO_CLAIM`; DAG `current_verdict` says 8 ready | DAG is primarily static orchestration definition, but embedded live-sounding verdict is stale | next DAG delta should separate immutable node eligibility from live queue state, or defer live state exclusively to queue/state |
| `DRIFT-07` | MEDIUM | claim files vs worker logs | some retained claim files still contain original `state=CLAIMED` while worker logs report released/pass-pending-fanin | physical lock existence correctly prevents duplicate ownership, but `CLAIMED` cannot be treated as live execution telemetry indefinitely | supervisor should model `lock_state` separately from `worker_state`; never delete evidence solely to make telemetry cleaner |
| `DRIFT-08` | MEDIUM semantic | Recovery ownership/claim wording | Recovery says broad SOL state/control role and claim in own log; M47 supersedes this with SOL-0-only shared writes + atomic claim files | older semantics could authorize an unsafe shared write if read alone | recovery reconciliation must explicitly adopt M47 shared-writer and atomic-claim rules |
| `DRIFT-09` | NONE | physical counts/gates | all current numerical state and closed gates remain coherent | no gate change justified | carry counts/gates forward unchanged unless newer physical evidence proves otherwise |
| `DRIFT-10` | NONE | reserved owners | M06/M07/M08 remain ASTRA/CLAUDE/GROK-only | no owner conflict | preserve reservation; worker evidence is advisory only |

### D. Authority resolution

No detected drift justifies a physical mutation or gate opening.

Where apparent contradictions exist, authority resolves them safely:

`physical claim tree + worker evidence/readback > STATE delta > CHECKPOINT delta > PLAN delta > Handoff > Recovery > logs/chat`.

Thus:
- the physical claim namespace proves N01-N08 are not free;
- worker logs/evidence provide activity/release semantics;
- shared M47 snapshots remain historically valid at creation but require supervisor fan-in for current telemetry;
- stale Recovery pointers cannot override later M47 Handoff/deltas.

### E. Supervisor-ready reconciliation proposal — NOT APPLIED

SOL-0 should, only after reading every latest worker evidence/log and fresh HEAD, fan-in sequentially with fresh SHA:

1. **STATE delta (next revision, number determined fresh)**
   - preserve physical counts and all three false gates;
   - record all eight lock files as materialized;
   - split lock status from worker status;
   - record PASS workers only as `PASS_PENDING_SUPERVISOR_FANIN`, never `VERIFIED_CLOSED` by inheritance.

2. **CHECKPOINT delta**
   - resume from actual worker/fan-in state rather than original `8 ready / 0 claims` snapshot;
   - keep N09-N12 blocked unless explicit independent gates change.

3. **PLAN delta**
   - retire the stale initial-dispatch next_action;
   - remove already locked/completed N01-N08 from `READY_FREE` semantics;
   - next work should be supervisor verification + reserved-review/director dependencies, not invented N13 work.

4. **Queue/Handoff**
   - queue states should reflect live worker outcomes after verification;
   - Handoff should replace `8_SAFE_READY_NODES` snapshot with current fan-in status;
   - retain SOL-0-only shared-write rule and atomic-lock protocol.

5. **Recovery reconciliation**
   - point recovery to latest M47-or-later deltas/checkpoint;
   - explicitly state M47 atomic lock namespace and supervisor-only shared writes;
   - preserve old recovery document/history or use versioned delta; no destructive evidence rewrite.

6. **DAG semantics**
   - keep node definitions as static eligibility if desired, but do not use embedded READY labels as live ownership state;
   - live state should come from queue/state + physical claims + worker evidence.

## STEP 3 — TEST / REFUTE / REPORT

### Three simulations

1. **SIM-1 — stale READY selector:** a new worker reads PLAN/queue and chooses SW-N06 because it says READY. It then reads `CLAIM-SW-N06.json`; collision protocol must block the write. Expected result: `CLAIM_COLLISION → NO WRITE → RESCAN`. Safety mechanism PASS.
2. **SIM-2 — stale Recovery boot:** an agent starts from Recovery M43 pointers. Authority/order requires reading latest Handoff/deltas and physical claims, which moves it to M47 and blocks duplicate claims/shared writes. Safety is recoverable, but Recovery pointer drift remains a real reconciliation GAP.
3. **SIM-3 — worker PASS arrives:** N01/N02/N03/N04/N05/N07 worker evidence reports PASS_PENDING_FANIN. The three physical gates remain false because worker PASS is not director/reviewer authorization. Expected result: no N09/N10/N11 execution.

### Three refutations

1. Refute `PLAN says 8 READY, therefore eight nodes are free now`: FALSE. All eight physical claim files exist; physical lock authority wins.
2. Refute `a retained claim file with state CLAIMED proves the worker is still executing`: FALSE. Worker log/evidence may show released/pass-pending-fanin; lock ownership and execution state are different dimensions.
3. Refute `successful worker evidence permits opening physical/download/Step3 gates`: FALSE. M06/M07/M08 reserved reviews + director gate remain required and no later authoritative gate-opening evidence was found.

### Test results
- mandatory control surfaces compared: PASS.
- physical claim namespace N01-N08 present: PASS.
- stable physical counts cross-check: PASS.
- closed-gate cross-check: PASS.
- owner-reservation cross-check: PASS.
- shared files written by SW-N08: `0` PASS.
- simulations: `3/3`.
- refutations: `3/3`.

### COUNCIL12
1. Objective: detect control-plane contradictions without rewriting shared state.
2. Requirement: latest physical claims/evidence outrank stale snapshots.
3. Authority: physical tree/readback > shared deltas > plan/handoff/recovery.
4. State: M47 active; all eight node locks materialized; fan-in not globally reconciled.
5. Owner: SOL-1 owns only SW-N08 in this step; SOL-0 owns shared fan-in.
6. Gates: all physical/acquisition/Step3 gates remain false.
7. Collision risk: high if READY text is read without lock tree; atomic locks currently contain the risk.
8. Causal GAP: shared control telemetry has not yet caught up with asynchronous worker claims/results; Recovery also retains older M43 pointers.
9. Alternatives rejected: worker rewrites shared files; delete claim history; infer gate opening from PASS; invent new safe work after all N01-N08 locks exist.
10. StrategyDelta: versioned SOL-0 fan-in with lock_state vs worker_state separation and Recovery pointer reconciliation.
11. Tests/refutations: cross-surface checks + 3 simulations + 3 refutations.
12. Verdict: `PASS_PENDING_SUPERVISOR_FANIN`; drift identified with no safety gate bypass.

### GOALS12_OUTPUT
- G01 literal preserved: PASS.
- G02 fresh HEAD before evidence write: PASS.
- G03 all required control surfaces compared: PASS.
- G04 owner/claim: PASS.
- G05 gates/dependencies: PASS.
- G06 write-scope isolation: PASS.
- G07 current physical claims/logs used: PASS.
- G08 minimum permitted delta: PASS.
- G09 contradiction/drift matrix: PASS.
- G10 simulations/refutations: PASS.
- G11 evidence/log SHA/readback: evidence pending immediate post-write readback; log follows.
- G12 reconciliation: proposal prepared; application correctly delegated to SOL-0.

## WORKER VERDICT

`PASS_PENDING_SUPERVISOR_FANIN`

No shared STATE/PLAN/CHECKPOINT/Handoff/Recovery/DAG/queue file was modified by this worker.
No gate was opened.
No `VERIFIED_CLOSED` was self-certified.
