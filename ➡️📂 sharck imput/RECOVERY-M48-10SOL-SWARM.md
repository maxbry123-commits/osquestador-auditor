# RECOVERY M48 — SHARCK INPUT V2.1 — 10 SOL SWARM

Estado: `ACTIVE / FAIL_CLOSED / M48_10SOL_SWARM_FANIN_AND_NEXT_WAVE`

## Fuente de verdad
`GitHub physical tree + manifests/hashes/runs/readback > STATE/deltas > CHECKPOINT/deltas > PLAN/deltas > Handoff > Recovery > owner/worker logs > chat`.

## Reanudación obligatoria
1. Leer HEAD fresco de `main`.
2. Leer `STATE-DELTA-037-M48-10SOL-SWARM-FANIN.json`.
3. Leer `CHECKPOINT-DELTA-035-M48-10SOL-SWARM-FANIN.json`.
4. Leer `PLAN-DELTA-019-M48-10SOL-SWARM-FANIN.json`.
5. Leer `SWARM-DAG-10SOL-M48-v1.json`.
6. Leer `CRAZY-WALL-SWARM-QUEUE-M48.json`.
7. Leer `WATCHDOG-SWARM-10SOL-M48-2026-09-12.json`.
8. Leer `SUPERVISOR-ORDERS-M48-SWARM-10SOL.md`.
9. Leer físicamente `swarm-claims/` y `SOL-SWARM-01-LOG.md` ... `SOL-SWARM-10-LOG.md`.
10. Separar siempre `lock_state` de `worker_state`: un claim retenido puede ser evidencia histórica aunque el worker ya esté RELEASED.

## Estado recuperable
- M47 `SW-N01..SW-N08`: worker scopes liberados; resultados `PASS_PENDING_SUPERVISOR_FANIN`; cero promoción automática a `VERIFIED_CLOSED`.
- M48 `SW-N13..SW-N22`: cola segura para hasta 10 workers dinámicos; actividad real sólo existe con claim atómico/readback.
- `SW-N09..SW-N12`: BLOCKED_GATE.
- `M06 ASTRA`, `M07 CLAUDE`, `M08 GROK`: owners reservados.

## Estado físico preservado
- catálogo: `117`.
- B01–B04: `17 VERIFIED_CLOSED / 23 FAILED / 0 pending`.
- partials: `12 components / 139 anomalies`.
- B05/B06: `20 researched / 0 downloaded`.

## Gates
`physical_repair_allowed=false`
`b05_b06_download_allowed=false`
`step3_allowed=false`
`canonical_motors=IMMUTABLE`

Mientras sigan falsos: sólo `READ_ONLY / RESEARCH / PREFLIGHT / SANDBOX_ISOLATED / EVIDENCE / CONTROL_DRIFT`.

## Anti-colisión
`1 CHAT = 1 ACTIVE NODE`
`1 NODE = 1 OWNER`
`1 PATH = 1 ACTIVE WRITER`

Claim válido:
`READ FRESH → verify READY and free → create swarm-claims/CLAIM-<NODE>.json → READBACK`.
Si ya existe: `COLLISION → NO OVERWRITE → RESCAN`.

Workers sólo escriben claim/evidence/log propios. `STATE/PLAN/CHECKPOINT/Handoff/Recovery/DAG/Queue/Watchdog` son shared writes de `SOL-0` supervisor, secuenciales con SHA fresco y readback.

## Regla de cierre
No inferir agentes activos por capacidad registrada. No heredar PASS. No force/LFS/silent overwrite. No auto-certificar `VERIFIED_CLOSED`.
