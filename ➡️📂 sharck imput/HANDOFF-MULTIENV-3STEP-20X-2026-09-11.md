# 🦈 HANDOFF MULTI-ENTORNO — SHARCK INPUT V2.1

Estado: `ACTIVE / FAIL_CLOSED / STEP2 / M52_10SOL_SWARM_ACTIVE / PHYSICAL_GATES_CLOSED`
Repo: `maxbry123-commits/osquestador-auditor` · branch `main` · raíz operativa `➡️📂 sharck imput/`.

## Orden obligatorio de lectura
1. `README-METODO-TRABAJO-MULTIAGENTE.md`
2. `📁 readme arquitectura sharck imput V2.1.md`
3. `📂 Craxy wall bitácora stated JSON/XRAY-ADN-CROSSCHECK-2026-09-11.md`
4. `📂 Craxy wall bitácora stated JSON/STATE.json` + `STATE-DELTA-039-M52-SWARM-EXPANSION.json` o posterior.
5. `📂 Craxy wall bitácora stated JSON/CHECKPOINT.json` + `CHECKPOINT-DELTA-037-M52-SWARM-EXPANSION.json` o posterior.
6. `📂 Craxy wall bitácora stated JSON/PLAN.json` + `PLAN-DELTA-021-M52-SWARM-EXPANSION.json` o posterior.
7. `RECOVERY-M52-10SOL-SWARM.md`.
8. DAG: `SWARM-DAG-10SOL-M48-v1.json` + `SWARM-DAG-10SOL-M50-DELTA.json` + `SWARM-DAG-10SOL-M51-DELTA.json` + `SWARM-DAG-10SOL-M52-DELTA.json`.
9. Queue viva: `CRAZY-WALL-SWARM-QUEUE-M52.json`.
10. Watchdog: `WATCHDOG-SWARM-10SOL-M52-2026-09-12.json`.
11. Orders: `SUPERVISOR-ORDERS-M52-SWARM-10SOL.md`.
12. `📂 Craxy wall bitácora stated JSON/swarm-claims/`.
13. `SOL-0-SUPERVISOR-LOG.md` + `SOL-SWARM-01-LOG.md` … `SOL-SWARM-10-LOG.md`.
14. Evidence `SW-Nxx-EVIDENCE.md` del nodo relevante.

Si existe delta/evidence posterior verificado, prevalece.

## Fuente de verdad
`GitHub physical tree + manifests/hashes/runs/readback > STATE/deltas > CHECKPOINT/deltas > PLAN/deltas > Handoff > Recovery > owner/worker logs > chat`.
Para actividad viva: `claim file + worker log/evidence + HEAD chronology > static queue snapshot > registered capacity`.

## Estado físico preservado
- catálogo canónico: `117`.
- B01–B04: `17 VERIFIED_CLOSED / 23 FAILED / 0 pending`.
- `23 FAILED = 12 partial + 11 source-special/symlink`.
- partial universe: `12 components / 139 anomalies`.
- B05/B06: `20 researched / 0 downloaded`.

## Gates
`physical_repair_allowed=false`
`b05_b06_download_allowed=false`
`step3_allowed=false`
`canonical_motors=IMMUTABLE`

Reservados: `M06→ASTRA`, `M07→CLAUDE`, `M08→GROK`.
Bloqueados: `SW-N09..SW-N12`.

# Swarm history
## M47
`SW-N01..SW-N08` fueron worker-complete/released; resultados quedaron para fan-in/review, sin promoción automática a `VERIFIED_CLOSED`.

## M49
`SW-N13` spaCy polyleven forensic: upstream pinned muestra `spacy/matcher/polyleven.c` como blob regular, no symlink. No demuestra destino canónico correcto; no cierra spaCy.

## Terminales conocidos M48–M52
- `SW-N13`: RELEASED / PASS_PENDING_REVIEW.
- `SW-N14`: RELEASED / PASS_PENDING_SUPERVISOR_FANIN.
- `SW-N15`: RELEASED / PASS_PENDING_SUPERVISOR_FANIN; 87/87 sandbox fixture pass; fresh tracked-tree replay quedó pendiente.
- `SW-N16`: `BLOCKED_RELEASED`; simulaciones/refutaciones ejecutadas pero evidence file no pudo persistirse por write path normal. No PASS.
- `SW-N17`: RELEASED / PASS_PENDING_REVIEW; 7/7 full-tree fixture matrix + 3 refutations; detectó stale-head recuperado tras commit no solapado.
- `SW-N18`: RELEASED / PASS_PENDING_SUPERVISOR_FANIN; #108 historical source commit sigue no recuperable; current upstream confirma special symlink independently, sin sustituir historia.

Para `SW-N19..SW-N28`, NO usar esta lista como estado vivo: leer claims/logs frescos.

# Ola gap-derived M50–M52
- `SW-N23`: spaCy `website/.vscode/extensions.json` forensic.
- `SW-N24`: historical source-commit recovery feasibility 11/11.
- `SW-N25`: stale-head/concurrency protocol sandbox.
- `SW-N26`: fresh pinned tracked-tree replay sandbox.
- `SW-N27`: live-state reconciler queue/claims/logs sandbox.
- `SW-N28`: evidence persistence write-path diagnostic derivado del BLOCKED N16.

Estos nodos nacen de GAPs evidenciados; no se crearon sólo para ocupar workers.

## Anti-colisión
`1 CHAT = 1 ACTIVE NODE`
`1 NODE = 1 OWNER`
`1 PATH = 1 ACTIVE WRITER`
`EXACTLY 3 STEPS PER NODE`

Atomic claim:
`READ HEAD FRESH → READ latest queue/claims → verify SAFE/FREE → CREATE CLAIM → READBACK`.
Si ya existe: `COLLISION → NO OVERWRITE → RESCAN`.
Si HEAD cambió: `STALE_HEAD → ABORT WRITE → READ FRESH → REVALIDATE → RETRY`.

Workers sólo escriben claim/evidence/log propios. `SOL-0` es único writer de shared control plane.

## Watchdog
External automation activo: `Sharck Swarm Supervisor`, frecuencia horaria.
Watchdog documental vigente: `WATCHDOG-SWARM-10SOL-M52-2026-09-12.json`.
Loop: `READ FRESH → reconcile claim/log/evidence → detect stale/double-active/path-overlap → issue safe orders → verify terminal evidence → SOL-0 fan-in → readback → report`.

Capacidad registrada: 10 workers. **No afirmar 10 activos sin 10 claims vivos compatibles.**

## Recovery
Checkpoint: `CP-V2-M52-SWARM-EXPANSION-037`.
Reanudar siempre leyendo primero HEAD + M52 state/plan/checkpoint + queue + claims; luego actuar.

## Veredicto
`M52_10SOL_SWARM_CONTROL_ACTIVE / GAP_DERIVED_WORK_EXPANDED / N16_BLOCK_PRESERVED / PHYSICAL_STATE_17_VERIFIED_23_FAILED / NO_NEW_CANONICAL_DOWNLOADS / M06_M07_M08_RESERVED / STEP3_NOT_STARTED_PHYSICALLY / WATCHDOG_HOURLY_ACTIVE`.
