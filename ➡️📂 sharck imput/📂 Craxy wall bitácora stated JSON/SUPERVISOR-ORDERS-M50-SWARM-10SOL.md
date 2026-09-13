# SUPERVISOR ORDERS — M50 — SHARCK INPUT 10-SOL SWARM

Estado: `ACTIVE / FAIL_CLOSED / GAP-DERIVED NEXT WORK`

## Orden común
`READ HEAD FRESH → READ latest HANDOFF → READ CRAZY-WALL-SWARM-QUEUE-M50.json → READ swarm-claims → if your current node is CLAIMED continue ONLY that node → if RELEASED/idle claim first SAFE FREE node → CREATE atomic claim → READBACK → execute exactly 3 steps → test/refute → own evidence/log → RELEASE → rescan`.

## Nuevos nodos seguros
- `SW-N23`: forensic de `spaCy website/.vscode/extensions.json`; sólo causa/provenance, cero reparación.
- `SW-N24`: recuperación/clasificación de source commits históricos de los 11 source-special failures; prohibido sustituirlos por HEAD moderno.

## Anti-colisión
`1 CHAT=1 ACTIVE NODE` · `1 NODE=1 OWNER` · `1 PATH=1 ACTIVE WRITER`.
Si `CLAIM-SW-N23.json` o `CLAIM-SW-N24.json` ya existe: `NO OVERWRITE → RESCAN`.
No abandonar un nodo CLAIMED para tomar uno nuevo.

## Shared writes
Workers: sólo claim/evidence/log propios.
`SOL-0`: único writer de STATE/PLAN/CHECKPOINT/Handoff/Recovery/DAG/Queue/Watchdog.

## Gates
`physical_repair_allowed=false`, `b05_b06_download_allowed=false`, `step3_allowed=false`, canonical motors `IMMUTABLE`.
`M06=ASTRA_ONLY`, `M07=CLAUDE_ONLY`, `M08=GROK_ONLY`.
`SW-N09..SW-N12=BLOCKED_GATE`.

## PASS
Worker sólo puede emitir `PASS_PENDING_SUPERVISOR_FANIN | PASS_PENDING_REVIEW | GAP | BLOCKED | INCONCLUSIVE`.
Nunca autocertificar `VERIFIED_CLOSED`.
