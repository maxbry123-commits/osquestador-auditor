# SOL-SWARM-01 LOG — SHARCK INPUT

- agent_name: `SOL-1-GPT`
- chat_id: `chat-sol1-20260912T2305-0500`
- state: `IDLE_READ_FRESH_REQUIRED`
- active_node: `null`
- physical_mutation: `false`
- canonical_motors_mutated: `false`
- shared_control_files_written: `0`
- reserved nodes forbidden: `M06_ASTRA`, `M07_CLAUDE`, `M08_GROK`

## Released history
- SW-N01: `PASS_PENDING_SUPERVISOR_FANIN`, evidence commit `16c3f273d2cf5cad1ff431fd92e44ad80b31bf63`.
- SW-N03: `PASS_PENDING_SUPERVISOR_FANIN`, evidence commit `0611bef7e98eaae263730aa68bc0a5f8fcb903c4`.
- SW-N05: `PASS_PENDING_SUPERVISOR_FANIN`, evidence commit `909f9f931538a7f1de31a500c2a9973ee5941086`.
- SW-N08: `PASS_PENDING_SUPERVISOR_FANIN`, evidence commit `83342a9b7a2d25c379705a7afb74414b6d951ab4`.

## SW-N16 — BLOCKED_RELEASED, NOT PASS
- task: `MODE_AND_EOL_PRESERVATION_SANDBOX`
- claim_commit: `b71f263fe24b3aeb7c53b436c974e4c04702a763`
- release_commit: `c8dab4acc0ead9da9cdb6640f8377193f2e7646b`
- sandbox tests: `3/3 simulations + 3/3 refutations`
- evidence file: `MISSING`
- verdict: `BLOCKED`
- verified_closed: `false`
- blocker: `evidence create path was blocked; M52 preserves this as real evidence-persistence gap`

## SW-N25 — RELEASED TO SUPERVISOR FAN-IN
- task: `STALE_HEAD_CONCURRENCY_PROTOCOL_SANDBOX`
- claim_commit: `fd11e38afc8c32a5c521b8ec8e2e5a98b84c0c96`
- evidence_commit: `8267ab3831c26c9cd0c63bc65159797aac6439e3`
- evidence_blob: `0f2ccbb45b1476d36092a95c4ca1c66dfd463303`
- release_commit: `a156ff8d561585328f74258537e56103c4041cc5`
- tests: `6/6`
- simulations/refutations: `3/3 + 3/3`
- result: `stale overlap aborts deterministically; unrelated changes proceed only after fresh revalidation; claim collisions and stale optimistic updates reject; no silent overwrite`
- real_repo_race: `release first returned 409 during concurrent M52/N28 commits; no overwrite was attempted; claim was refetched, scope revalidated as non-overlap, release reconstructed and succeeded`
- verdict: `PASS_PENDING_SUPERVISOR_FANIN`
- verified_closed: `false`

## Current control
- latest control plane observed: `M52_EVIDENCE_PERSISTENCE_AND_CONCURRENCY_WAVE`.
- gates: `physical_repair_allowed=false / b05_b06_download_allowed=false / step3_allowed=false / canonical_motors=IMMUTABLE`.
- shared_control_writer: `SOL-0_ONLY`.
- next_action: `READ FRESH latest queue + physical claims; claim only first SAFE/FREE node`.
