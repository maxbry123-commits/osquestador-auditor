# RECOVERY M53 — SHARCK INPUT V2.1 — 10 SOL SWARM

Estado: `ACTIVE / FAIL_CLOSED / M53_ADD_GAP_DERIVED_PREINTEGRATION_NODES`

## Reanudación obligatoria
1. Leer HEAD fresco.
2. Leer `STATE-DELTA-040-M53-PREINTEGRATION-WAVE.json`.
3. Leer `PLAN-DELTA-022-M53-PREINTEGRATION-WAVE.json`.
4. Leer `CHECKPOINT-DELTA-038-M53-PREINTEGRATION-WAVE.json`.
5. Leer `CRAZY-WALL-SWARM-QUEUE-M53.json`.
6. Leer DAG base M48 + deltas M50/M51/M52/M53.
7. Leer `WATCHDOG-SWARM-10SOL-M53-2026-09-12.json`.
8. Leer `SUPERVISOR-ORDERS-M53-SWARM-10SOL.md`.
9. Leer `swarm-claims/`, logs SOL-SWARM-01..10 y evidence del nodo relevante.
10. Resolver live state por claim+log/evidence+HEAD chronology. No usar snapshot viejo como telemetría viva.

## Estado físico preservado
- catálogo: `117`.
- B01–B04: `17 VERIFIED_CLOSED / 23 FAILED / 0 pending`.
- partial universe: `12 components / 139 anomalies`.
- B05/B06: `20 researched / 0 downloaded`.
- gates: `physical_repair_allowed=false`, `b05_b06_download_allowed=false`, `step3_allowed=false`.
- canonical motors: `IMMUTABLE`.

## GAPs/terminales que no deben maquillarse
- `SW-N16 = BLOCKED_RELEASED`: evidence file persistence failed.
- `SW-N24 = RELEASED / PASS_PENDING_SUPERVISOR_FANIN`: 11/11 historical source commits NONRECOVERABLE from persisted evidence; modern HEAD cannot replace history.
- `SW-N26 = RELEASED / GAP / INFRA_FAILURE`: source pinned, but full tracked-tree byte replay was NOT_EXECUTED because sandbox GitHub network access was unavailable.
- `SW-N27 = RELEASED / PASS_PENDING_REVIEW`: live-state reconciler tests passed; supervisor implementation/fan-in remains.
- `SW-N28 = RELEASED / PASS_PENDING_SUPERVISOR_FANIN`: root cause bounded to evidence-create capability block; N16 remains blocked.

## M53 dispatch
`SW-N29..SW-N34` are gap-derived read-only/sandbox nodes. Their real state must be re-read from claim files before any assignment.

## Anti-colisión
`1 CHAT=1 ACTIVE NODE` · `1 NODE=1 OWNER` · `1 PATH=1 ACTIVE WRITER`.
Atomic claim: `READ FRESH → verify SAFE/FREE → CREATE CLAIM → READBACK`.
409/stale: `ABORT → READ FRESH → REVALIDATE → RETRY`; never force or overwrite.

## Reserved / blocked
`M06 ASTRA`, `M07 CLAUDE`, `M08 GROK` reserved.
`SW-N09..SW-N12` blocked by physical gates.

## Supervisor
`SOL-0` is the only writer of shared control. Workers write only own claim/evidence/log. External automation `Sharck Swarm Supervisor` runs hourly and must use the newest frontier.
