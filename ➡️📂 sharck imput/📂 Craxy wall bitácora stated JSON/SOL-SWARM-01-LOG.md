# SOL-SWARM-01 LOG — SHARCK INPUT

- agent_name: `SOL-1-GPT`
- chat_id: `chat-sol1-20260912T2305-0500`
- state: `GAP_ACTIVE_EVIDENCE_WRITE_BLOCKED`
- active_node: `SW-N16`
- physical_mutation: `false`
- canonical_motors_mutated: `false`
- shared_control_files_written: `0`
- reserved nodes forbidden: `M06_ASTRA`, `M07_CLAUDE`, `M08_GROK`

## SW-N01 — RELEASED TO SUPERVISOR FAN-IN
- task: `M40_20X_DEDUP_AND_DECISION_MATRIX`
- claim_commit: `77e544c2d29bbb47b38573ce3fd7811d14cd63a2`
- evidence_commit: `16c3f273d2cf5cad1ff431fd92e44ad80b31bf63`
- result: `65/65 M40 rows + 20/20 20X classified; no acquisition authorized`
- simulations/refutations: `3/3 + 3/3`
- verdict: `PASS_PENDING_SUPERVISOR_FANIN`

## SW-N03 — RELEASED TO SUPERVISOR FAN-IN
- task: `PARTIAL_139_ANOMALY_CLASSIFICATION`
- claim_commit: `8be890dce641d42d4b1fb447f838b4e143b86667`
- evidence_commit: `0611bef7e98eaae263730aa68bc0a5f8fcb903c4`
- result: `12/12 partial components; 139/139 anomalies accounted; 137/139 causally explained; 2/139 spaCy CAUSE_UNPROVEN`
- simulations/refutations: `3/3 + 3/3`
- verdict: `PASS_PENDING_SUPERVISOR_FANIN`

## SW-N05 — RELEASED TO SUPERVISOR FAN-IN
- task: `HF_BRIDGE_PORT_CONTRACT_AUDIT`
- claim_commit: `23ea92715b05cffe23038e9e1378e6b4fdbaf835`
- evidence_commit: `909f9f931538a7f1de31a500c2a9973ee5941086`
- result: `4/4 base HF ports + 3 reference-only ports + 10 failure contracts; zero duplicate acquisition; #108 stays FAILED`
- simulations/refutations: `3/3 + 3/3`
- verdict: `PASS_PENDING_SUPERVISOR_FANIN`

## SW-N08 — RELEASED TO SUPERVISOR FAN-IN
- task: `CONTROL_PLANE_CONTRADICTION_WATCH`
- claim_commit: `7ec9bec5c4839f3c57d219514048668f7cfc8608`
- evidence_commit: `83342a9b7a2d25c379705a7afb74414b6d951ab4`
- result: `control-plane drift identified; counts/owners/gates coherent`
- simulations/refutations: `3/3 + 3/3`
- verdict: `PASS_PENDING_SUPERVISOR_FANIN`

## SW-N16 — ACTIVE GAP, OWNERSHIP RETAINED
- task: `MODE_AND_EOL_PRESERVATION_SANDBOX`
- mode: `SANDBOX_ONLY`
- claim_commit: `b71f263fe24b3aeb7c53b436c974e4c04702a763`
- claim_blob_current: `ec75eb681f0970be4e03bd5201fcb59dfdacd85e`
- claim_state: `GAP_ACTIVE_EVIDENCE_WRITE_BLOCKED`
- execution: `COMPLETE_FOR_SANDBOX_TESTS`
- ordinary_git_staging: `EOL_MUTATION_REPRODUCED`
- regular_blob_exact_staging: `PASS byte+SHA+CRLF+mode for 100644/100755`
- deliberate_mode_loss: `DETECTED 100755!=100644`
- special_mode_120000: `FAIL_CLOSED as required`
- simulations/refutations: `3/3 + 3/3`
- canonical_mutation: `0`
- downloads: `0`
- evidence_path: `SW-N16-EVIDENCE.md`
- evidence_readback: `404 NOT_FOUND`
- evidence_write_attempts: `3 normal create_file attempts blocked by tool safety controls`
- current_gap: `EVIDENCE_FAILURE / tooling persistence only; sandbox behavior itself tested`
- release: `NOT_ALLOWED until evidence file exists and readback passes`
- next_action: `retain SW-N16 ownership; do not claim N17+; retry only via normal authorized evidence write path when available`
- node_pass: `80% because persistence/readback/fan-in incomplete`

## Worker control
- M49 current queue keeps N14-N22 as next-wave work, but SOL-1 owns N16 until explicit release.
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- shared_control_writer: `SOL-0_ONLY`
- rule: `FAIL -> repeat same node; do not skip while active claim exists`.
- worker_verdict: `GAP_ACTIVE_EVIDENCE_WRITE_BLOCKED`.
