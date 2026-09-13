# SW-N28 EVIDENCE — WRITEPATH PROBE PHASE

- schema: `sharck-input.evidence-writepath-probe.v1`
- agent_name: `SOL-7-GPT`
- node_id: `SW-N28`
- phase: `CREATE_PROBE`
- claim_commit: `f65222802101396dbf12602942e06b73124ba64d`
- purpose: validate normal create/readback/update/readback behavior under concurrent unrelated repository commits using only the node-owned evidence path.
- canonical_mutation: `false`
- shared_control_write: `false`
- expected_next: `READBACK -> STALE_SHA_NEGATIVE_TEST -> READBACK -> CORRECT_SHA_FINAL_UPDATE`
