# SUPERVISOR ORDERS — M52 — 10 SOL GPT

Estado: `ACTIVE / FAIL_CLOSED / CLAIMS-ARE-LIVE-TRUTH`

## Orden transversal
`READ HEAD FRESH → READ latest Handoff → READ CRAZY-WALL-SWARM-QUEUE-M52 → READ your current claim + all candidate claims → if current node active CONTINUE IT ONLY → if terminal/idle CLAIM FIRST SAFE FREE → READBACK CLAIM → execute exactly 3 steps → test + 3 refutations → persist own evidence/log → readback → RELEASE/BLOCK → rescan`.

## Nodos adicionales M50–M52
- `SW-N23`: spaCy `website/.vscode/extensions.json` forensic.
- `SW-N24`: historical source-commit recovery feasibility.
- `SW-N25`: stale-head/concurrent-write protocol sandbox.
- `SW-N26`: fresh pinned tracked-tree replay sandbox.
- `SW-N27`: claims/logs/live-state reconciler sandbox.
- `SW-N28`: evidence persistence write-path diagnostic from N16 BLOCKED.

El número SOL NO fija nodo.

## Invariantes
`1 CHAT=1 ACTIVE NODE`
`1 NODE=1 OWNER`
`1 PATH=1 ACTIVE WRITER`
`EXACTLY 3 STEPS PER NODE`

Atomic claim:
`READ FRESH → confirm SAFE/FREE → CREATE CLAIM → READBACK`.
Si existe claim: `NO OVERWRITE → RESCAN`.
Si HEAD cambió: `STALE_HEAD → ABORT/REVALIDATE`, nunca force.

## Shared control
Workers sólo claim/evidence/log propios.
`SOL-0` único writer de queue/DAG/STATE/PLAN/CHECKPOINT/Handoff/Recovery/Watchdog.

## Gates
`M06 ASTRA_ONLY`, `M07 CLAUDE_ONLY`, `M08 GROK_ONLY`.
`SW-N09..SW-N12 BLOCKED_GATE`.
`physical_repair_allowed=false`.
`b05_b06_download_allowed=false`.
`step3_allowed=false`.
Canonical motors `IMMUTABLE`.

## Veredicto worker
Sólo: `PASS_PENDING_SUPERVISOR_FANIN | PASS_PENDING_REVIEW | GAP | BLOCKED | INCONCLUSIVE`.
No autocertificar `VERIFIED_CLOSED`.

## Si no hay nodo libre
No inventar trabajo. Buscar GAP real desde evidencia terminal → dedup → non-overlap → supervisor materializa nodo nuevo.
