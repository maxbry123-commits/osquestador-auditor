# SUPERVISOR ORDERS — M48 — 10 SOL GPT

Estado: `ACTIVE / FAIL_CLOSED / NEXT_WAVE_READY`

## Orden única para SOL 1–10
`READ FRESH → READ CRAZY-WALL-SWARM-QUEUE-M48 → READ swarm-claims → CLAIM FIRST SAFE READY SW-N13..SW-N22 → READBACK CLAIM → EXECUTE EXACTLY 3 STEPS → TEST + 3 REFUTATIONS → WRITE OWN EVIDENCE + OWN LOG → RELEASE → READ FRESH → NEXT SAFE FREE`.

## No pisarse
- 1 chat = 1 nodo activo.
- 1 node_id = 1 owner.
- 1 evidence path = 1 writer.
- Workers NO escriben STATE/PLAN/CHECKPOINT/Handoff/Watchdog/DAG/Queue.
- Claim válido sólo tras crear `swarm-claims/CLAIM-<NODE>.json` y leerlo de vuelta.
- Si el claim file ya existe: `COLLISION → NO OVERWRITE → RESCAN`.
- Si HEAD cambió y toca tu scope: `STALE_HEAD → REVALIDATE`.

## Cola dinámica actual
`SW-N13` spaCy 2 anomalies forensic.
`SW-N14` special-file/provenance contract.
`SW-N15` StrategyDelta sandbox full-set batch A.
`SW-N16` mode/EOL preservation sandbox.
`SW-N17` full-tree/plumbing compare validator.
`SW-N18` HF #108 failure preflight.
`SW-N19` runtime candidate special-surface scan.
`SW-N20` M40 priority license/ref/pin/size preflight.
`SW-N21` I09 web capture/extraction preflight.
`SW-N22` I04/I10 eval harness preflight.

El número de SOL NO asigna nodo fijo. Cada chat toma el primer nodo libre seguro sobre HEAD fresco.

## Gates
`M06=ASTRA_ONLY`, `M07=CLAUDE_ONLY`, `M08=GROK_ONLY`.
`SW-N09..SW-N12=BLOCKED_GATE`.
Mientras `physical_repair_allowed=false`, `b05_b06_download_allowed=false`, `step3_allowed=false`: cero reparación canónica, cero descarga B05/B06/M40, cero wiring de producción.

## Worker PASS
`PASS_PENDING_SUPERVISOR_FANIN` solamente. `VERIFIED_CLOSED` requiere gate/reviewer según contrato.

## Supervisor SOL-0
Cada ciclo: `READ HEAD → reconcile claims/worker_state → detectar colisiones/stale locks → verificar evidencia → fan-in shared deltas secuencial → readback → publicar órdenes siguientes`.
