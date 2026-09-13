# SW-N28 EVIDENCE — EVIDENCE PERSISTENCE DIAGNOSTIC

- agent: `SOL-7-GPT`
- node: `SW-N28`
- claim_commit: `f65222802101396dbf12602942e06b73124ba64d`
- probe_create_commit: `c52d80291ba30d4a82d338354fe4c84d069b40b5`
- probe_blob: `5f2ffe3f612e2c57c13070d11b3edb0cbd276bf3`
- mode: `READ_ONLY_PLUS_SANDBOX`
- gates: `physical_repair_allowed=false; b05_b06_download_allowed=false; step3_allowed=false; canonical_motors=IMMUTABLE`

## STEP 1 — N16 chronology

`SW-N16` completed `3/3` simulations and `3/3` refutations but its required evidence file was never persisted. Its claim/log record an evidence-create capability block after repeated normal attempts, and `SW-N16-EVIDENCE.md` still returns 404. N16 correctly released `BLOCKED_RELEASED`, not PASS.

Bounded root cause: `EVIDENCE_CREATE_CAPABILITY_BLOCK`. No evidence proves an invalid path, stale target SHA, path collision, or failed N16 sandbox logic. N16 remains blocked and is not retroactively promoted by N28.

## STEP 2 — real write-path fixtures

1. `CREATE_PROBE`: created this N28-owned evidence path normally -> PASS, commit `c52d80291ba30d4a82d338354fe4c84d069b40b5`.
2. `CREATE_READBACK`: read back blob `5f2ffe3f612e2c57c13070d11b3edb0cbd276bf3` -> PASS.
3. `WRONG_SHA_UPDATE`: deliberately supplied a different blob SHA to this same owned path -> GitHub rejected with 409 -> PASS.
4. `NO_SILENT_MUTATION`: read-back after 409 showed original probe unchanged -> PASS.
5. `CREATE_COLLISION`: before N28, N27 was read absent, but another worker created its claim before our create; our create was rejected and read-back showed SOL-6 ownership -> PASS fail-closed behavior.
6. `CORRECT_SHA_UPDATE`: this final document updates the probe using its freshly read blob SHA -> must be followed by final read-back.

## Deterministic persistence contract

### Create
- read queue/DAG/claim fresh;
- verify target belongs to worker scope;
- fetch target path;
- if absent, create once;
- successful create requires immediate read-back and blob capture;
- path-exists/409/422 requires re-fetch, ownership check and abort/rescan on collision;
- never convert a failed create into blind overwrite.

### Update
- fetch target immediately before update;
- verify node/owner content and current blob SHA;
- update only with that SHA;
- on 409, re-fetch and retry only if the same worker still owns the path and expected content is intact;
- unrelated HEAD movement alone does not authorize overwrite or imply failure;
- final read-back is mandatory.

### Capability block
- preserve execution facts in worker-owned claim/log where possible;
- mark evidence persistence blocked;
- do not mark PASS/VERIFIED_CLOSED without required evidence;
- do not modify another worker's path;
- supervisor may create a separate diagnostic/recovery node.

## Supervisor acceptance

Fan-in requires: matching claim owner/node/scope, evidence file exists, final read-back succeeded, evidence blob/commit recorded, terminal worker state, no path-owner collision, no stale-SHA overwrite, and unchanged gates.

## Tests
- `T01 N16 evidence absent`: PASS.
- `T02 N16 claim/log chronology`: PASS.
- `T03 N28 create`: PASS.
- `T04 N28 create read-back`: PASS.
- `T05 stale/wrong SHA rejected`: PASS.
- `T06 failed update leaves file unchanged`: PASS.
- `T07 N27 create collision abort`: PASS.
- `T08 correct-SHA final update`: EXECUTED; final read-back required.
- `T09 N16 untouched`: PASS.

## Simulations
- unrelated HEAD advances + target unchanged -> revalidate target and use exact blob: PASS.
- path appears after absence read -> create collision, abort/rescan: PASS; physically observed on N27.
- stale target SHA -> reject/re-fetch: PASS; physically observed on N28.
- evidence capability block -> BLOCKED, no false PASS: PASS; matches N16.

## Refutations
1. `latest HEAD alone is sufficient concurrency control` -> REFUTED; target blob CAS + read-back are required.
2. `409/422 should be solved by overwriting` -> REFUTED; collision/stale state must be reconciled first.
3. `N28 write success makes N16 a PASS` -> REFUTED; N16 lacks its required persisted evidence.

Worker verdict before final read-back: `PASS_PENDING_FINAL_READBACK_THEN_SUPERVISOR_FANIN`.

Coverage: steps `3/3`; tests `9/9` with T08 awaiting read-back confirmation; simulations `4/4`; refutations `3/3`; N16 mutations `0`; shared writes `0`; canonical mutations `0`; downloads/LFS `0`.
