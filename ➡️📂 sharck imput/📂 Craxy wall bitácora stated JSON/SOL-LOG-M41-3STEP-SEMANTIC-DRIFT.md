# SOL — M41 / 3-STEP SEMANTIC DRIFT AUDIT

claim_id: `SOL-M41-20260911-2043-COT`
owner: `SOL`
status: `VERIFIED_READ_ONLY_CONTROL_GAP`
base_state_delta: `STATE-DELTA-029-M40-RESEARCH-REVIEW.json`
base_state_blob_sha: `31c167fdfff104168374971ec201dc5cab66f808`
base_checkpoint: `CP-V2-M40-RESEARCH-REVIEW-027`
base_checkpoint_blob_sha: `04ec9c2954b4ffd703306e91af3b1c1752d7e301`
physical_mutation: false

## Node contract — max 3 steps
1. `SYNC+CLAIM`: re-read M40 Handoff/state/checkpoint plus ASTRA/CLAUDE/GROK logs; M06/M07/M08 remain unclaimed.
2. `EXECUTE+VERIFY`: cross-check global 3-step semantics between Architecture V2.1, MULTIENV DAG/X-Ray and M40 Handoff.
3. `REPORT+FAN-IN`: record control-plane contradiction fail-closed; do not alter physical acquisition, Step3, owner nodes, or B05/B06.

## New evidence
Canonical Architecture V2.1 section 8 defines:
- Step1 = INVENTARIO/X-RAY/ARQUITECTURA.
- Step2 = ADQUISICIÓN/StrategyDelta (`research → gate → motores canónicos → read-back/hash/state/index`).
- Step3 = WIRE/PRUNE/MIN-CODE/TEST only after M06+M07+M08 + director decision.

Current M40 Handoff instead labels:
- Step2 = INVESTIGACIÓN + SHORTLIST.
- Step3 = ARQUITECTURA + ADQUISICIÓN + READBACK + DSL/DAG.

This is a semantic phase drift. It does not prove any physical error, but if consumed literally it can move acquisition into Step3 and conflate architecture/acquisition with integration. Under FAIL_CLOSED, the Architecture V2.1 3-step contract remains authoritative and M40 Handoff must be interpreted/corrected so that research/shortlist is a preflight inside Step2, not a redefinition of the global phases.

## Verdict
`G-V2-3STEP-SEMANTIC-DRIFT-M40 = CONFIRMED_CONTROL_GAP`

Locks preserved:
- `physical_repair_allowed=false`
- `b05_b06_download_allowed=false`
- `step3_allowed=false`
- `M06/M07/M08` ownership untouched
- 117 canonical components unchanged
- B01-B04 unchanged at 17 VERIFIED_CLOSED / 23 FAILED / 0 pending
- 12 partial components / 139 exact anomalies unchanged

Recommended fail-closed interpretation until corrected handoff/readback:
`STEP1 INVENTORY/XRAY/ARCHITECTURE → STEP2 RESEARCH/PREFLIGHT + ACQUISITION/STRATEGYDELTA + READBACK → FAN-IN M06+M07+M08 + DIRECTOR GATE → STEP3 WIRE/PRUNE/MIN-CODE/TEST`.
