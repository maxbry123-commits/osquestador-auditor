# SW-N27 — SWARM LIVE STATE RECONCILER SANDBOX

- schema: `sharck-input.multisol-dag.v1`
- node_id: `SW-N27`
- parent_node: `M51_ADD_CONCURRENCY_AND_REPLAY_SAFE_NODES`
- agent_name: `SOL-6-GPT`
- chat_id: `chat-sol6-20260912T2329-0500`
- mode: `READ_ONLY_PLUS_SANDBOX`
- claim_commit: `a72b82afd2f5a49d52c7f17101fb143a13a0dd1f`
- claim_blob: `edf151915b37a69532cfebb0cb45e67f5952ad3c`
- evidence_prewrite_head: `a156ff8d561585328f74258537e56103c4041cc5`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- canonical_mutation: `NO`
- shared_control_write: `NO`

## Assertion under test

A deterministic reconciler can derive safe live swarm state from queue metadata + durable claim files + worker logs + HEAD chronology without treating static READY labels, registration, or retained lock files as sufficient proof of ACTIVE/FREE state.

## STEP 1 — DEFINE INPUTS / REPRODUCE REAL DRIFT

### Required inputs

1. `queue_event`: latest supervisor dispatch metadata for node, including generation, state, explicit reopen flag when applicable, and commit chronology.
2. `claim_event`: durable `CLAIM-<NODE>.json` state, owner/chat, paths/write_scope, generation, claimed/released timestamps, blob SHA and commit chronology.
3. `worker_event`: worker-own log state and `active_node`, with blob/commit chronology.
4. `head_event`: ordered repository commit history used to determine which observation is fresher.
5. `registration_event`: identity registration only; never ownership by itself.

### Real drift reproduced

- `CRAZY-WALL-SWARM-QUEUE-M47.json` still labels SW-N01..SW-N08 `READY_TO_CLAIM`; therefore static queue state cannot establish current FREE state.
- `CRAZY-WALL-SWARM-QUEUE-M50.json` explicitly states its own truth rule: claim file + worker log/evidence are authoritative for live execution and queue metadata must not override fresher claim state.
- M50 snapshot lists SW-N16 as claimed, while fresh `CLAIM-SW-N16.json` now says `BLOCKED_RELEASED` and the worker log says `active_node: null`; therefore queue snapshot alone can create a false ACTIVE.
- `CLAIM-SW-N17.json` remains physically present but says `RELEASED`; therefore physical lock-file existence alone cannot mean ACTIVE.
- SOL-1 worker log captured after N16 release says `active_node: null`, while a later `CLAIM-SW-N25.json` exists in state `CLAIMED`; chronology is therefore required so an older idle log cannot override a newer durable claim.

Causal class: `CONTROL_PLANE_DRIFT + EVIDENCE_ORDERING_GAP`.

## Deterministic reconciliation contract

### Per-node state

Use these normalized outputs:

- `FREE`: supervisor queue says READY and there is no durable claim for this dispatch generation.
- `ACTIVE`: durable claim is in an active state and no global invariant conflict exists.
- `TERMINAL_NO_RECLAIM`: claim is RELEASED/BLOCKED_RELEASED or equivalent terminal state; retained lock is historical evidence, not a fresh free lock.
- `FREE_REQUEUED`: only an explicit newer supervisor requeue generation, chronologically after terminal claim, may make a terminal node claimable again.
- `BLOCKED`: latest supervisor dispatch says blocked/reserved and there is no contradictory newer authorized state.
- `CONFLICT_STALE_ACTIVE_LOCK`: durable claim still ACTIVE but a newer worker event says terminal/released; fail closed, not free.
- `CONFLICT_ACTIVE_WITHOUT_CLAIM`: worker says active but no durable atomic claim exists; fail closed.
- `CONFLICT_DOUBLE_ACTIVE_CHAT`: one chat has >1 reconciled active claims.
- `CONFLICT_PATH_OVERLAP`: >1 active claims overlap any normalized write path.
- `CONFLICT_UNKNOWN_CLAIM_STATE`: unrecognized durable claim state.

### Precedence / chronology

1. Registration never creates ownership.
2. Static queue READY is dispatch permission only; it does not override a claim file.
3. A durable active claim establishes candidate ACTIVE state.
4. A durable terminal claim establishes `TERMINAL_NO_RECLAIM`; never infer FREE merely because an old queue still says READY.
5. Worker logs corroborate claims but must be ordered by commit chronology; older logs cannot override newer claims.
6. If a newer worker event says terminal while durable claim remains active, classify stale-lock conflict and fail closed until reconciled.
7. Reuse after terminal state requires a **newer explicit supervisor requeue generation**; silent lock reuse is forbidden.
8. After per-node classification, run global one-chat and path-overlap checks. Any conflict quarantines affected active nodes from write execution.

### Path normalization before overlap test

- resolve repository-relative canonical path form;
- reject `..` traversal and ambiguous aliases;
- normalize Unicode/path separators consistently for comparison;
- compare exact files and parent/child directory containment, not only string equality;
- shared control paths are never worker-writable regardless of non-overlap.

## STEP 2 — EXECUTE SYNTHETIC STATE MATRIX

The reconciler logic was exercised in an isolated in-memory fixture; no repository product/control state was mutated.

### Base classification matrix — 10/10 PASS

| Test | Inputs | Expected/Observed |
|---|---|---|
| T1 | queue READY, no claim | `FREE` PASS |
| T2 | queue READY + claim CLAIMED | `ACTIVE` PASS |
| T3 | queue READY + claim RELEASED | `TERMINAL_NO_RECLAIM` PASS |
| T4 | claim CLAIMED + newer worker RELEASED | `CONFLICT_STALE_ACTIVE_LOCK` PASS |
| T5 | registration only | `IDLE_REGISTERED` PASS |
| T6 | worker ACTIVE, no claim | `CONFLICT_ACTIVE_WITHOUT_CLAIM` PASS |
| T7 | stale queue READY + claim BLOCKED_RELEASED | `TERMINAL_NO_RECLAIM` PASS |
| T8 | terminal claim gen1 + newer explicit supervisor requeue gen2 | `FREE_REQUEUED` PASS |
| T9 | terminal claim + older/non-newer requeue metadata | `TERMINAL_NO_RECLAIM` PASS |
| T10 | queue BLOCKED_GATE, no claim | `BLOCKED` PASS |

### Global invariant matrix — 3/3 PASS

| Test | Inputs | Expected/Observed |
|---|---|---|
| G1 | 2 active claims, different chats, disjoint paths | no global conflict PASS |
| G2 | 2 active claims, same chat, disjoint paths | both `CONFLICT_DOUBLE_ACTIVE_CHAT` PASS |
| G3 | 2 active claims, different chats, shared path | both `CONFLICT_PATH_OVERLAP` PASS |

### Fail-closed dispatch algorithm

```text
READ latest supervisor queue/deltas
READ claim files
READ worker logs
READ HEAD chronology
NORMALIZE each node
ORDER conflicting observations by chronology
CLASSIFY node state
CHECK one-chat-one-active
CHECK one-path-one-writer including parent/child overlap
IF any conflict -> QUARANTINE affected node(s), NO WRITE
ELSE first supervisor-authorized FREE node may be atomically claimed
CREATE claim (never update an existing path)
READBACK exact owner/chat/node/base/write_scope
ONLY THEN execute node
```

## STEP 3 — TEST / REFUTE / REPORT

### 3 simulations

1. `SIM-STATIC-READY-RELEASED-LOCK`: old queue says READY, claim says RELEASED. Result `TERMINAL_NO_RECLAIM`; no duplicate claim.
2. `SIM-STALE-QUEUE-BLOCKED-RELEASE`: queue snapshot says claimed, newer claim/log says BLOCKED_RELEASED. Result terminal/blocked history, not ACTIVE and not automatically FREE.
3. `SIM-NEW-ACTIVE-AFTER-OLD-IDLE-LOG`: older worker log says idle, newer atomic claim says CLAIMED. Chronology selects candidate ACTIVE; global invariant checks still run before writes.

### 3 refutations

1. `REFUTE-REGISTRATION-EQUALS-ACTIVE`: REFUTED — registration-only fixture normalizes to `IDLE_REGISTERED`.
2. `REFUTE-LOCK-FILE-EXISTS-EQUALS-ACTIVE`: REFUTED — RELEASED/BLOCKED_RELEASED retained claims normalize to terminal history.
3. `REFUTE-QUEUE-READY-EQUALS-FREE`: REFUTED — any durable active/terminal claim prevents naive FREE; only no-claim or explicit newer requeue generation can authorize claimability.

### Additional adversarial results

- same chat with two active claims is detected even if write paths are disjoint;
- two chats with overlapping write scopes are detected even if both claims are otherwise valid;
- newer worker-release with stale active claim never becomes silently FREE;
- active worker log without atomic claim never becomes valid ACTIVE;
- unrelated non-overlapping active claims remain parallel-safe.

## Supervisor acceptance schema

Recommended read-only reconciler output per node:

```json
{
  "node_id":"...",
  "queue_generation":0,
  "queue_state":"...",
  "claim_state":"...|null",
  "claim_owner":"...|null",
  "chat_id":"...|null",
  "worker_state":"...|null",
  "effective_state":"FREE|ACTIVE|TERMINAL_NO_RECLAIM|BLOCKED|CONFLICT_*",
  "write_scope":[],
  "evidence_order":["commit/blob refs"],
  "conflicts":[],
  "claimable":false,
  "reason":"deterministic rule id"
}
```

Global output must also contain:

```json
{
  "active_by_chat":{},
  "active_path_owners":{},
  "double_active_chats":[],
  "path_collisions":[],
  "stale_locks":[],
  "active_without_claim":[],
  "first_safe_free_node":null
}
```

The reconciler is advisory/read-only for workers. Only SOL-0 may fan results into shared queue/state/control files.

## GOALS12_OUTPUT

- G01 literal M51/N27 requirement preserved: `PASS`
- G02 fresh HEAD read: `PASS`
- G03 M47/M50/M51 metadata + claims/logs read: `PASS`
- G04 owner free / claim readback: `PASS`
- G05 dependency/gates valid: `PASS`
- G06 write_scope non-overlap: `PASS`
- G07 existing control evidence reused: `PASS`
- G08 minimal permitted delta: `PASS`
- G09 node-specific tests: `PASS 10/10 base + 3/3 global`
- G10 three simulations + three refutations: `PASS`
- G11 evidence SHA/readback: `PENDING_WRITE_READBACK`
- G12 release/rescan: `PENDING_RELEASE`

## COUNCIL12

1. Objective: derive live swarm state deterministically.
2. Requirement: read-only plus synthetic sandbox; no shared mutation.
3. Authority: fresh claim/log/HEAD chronology outranks static dispatch snapshots.
4. Physical state: claims persist as evidence after release; this is expected and must be interpreted by state, not existence.
5. Owner: SOL-6 owns only SW-N27.
6. Gates: physical/download/step3 remain false; motors immutable.
7. Collision risk: one-chat and write-path collisions are explicit global checks.
8. Causal GAP: state drift arises when queue/registration/retained lock are treated as sufficient live-state authority.
9. Alternatives: deletion of released locks rejected because it destroys evidence; queue-only and worker-log-only reconciliation rejected as stale-prone.
10. StrategyDelta: event chronology + durable claim semantics + explicit requeue generations + global collision checks.
11. Tests: 10 base + 3 global + 3 simulations + 3 refutations.
12. Verdict: `PASS_PENDING_REVIEW`; contract is tested in sandbox, not wired into supervisor control plane by this worker.

## Remaining gaps

- No supervisor/shared queue implementation was modified; SOL-0 fan-in required.
- Parent/child path-overlap normalization contract is specified but production repository-wide path index was not materialized by N27.
- A real concurrent race can still occur between reconciler read and atomic claim; atomic create + readback remains mandatory.
- Terminal-node requeue requires an explicit supervisor generation field/policy; existing historical queue schemas do not consistently expose generations.

## Producer verdict

`PASS_PENDING_REVIEW`
