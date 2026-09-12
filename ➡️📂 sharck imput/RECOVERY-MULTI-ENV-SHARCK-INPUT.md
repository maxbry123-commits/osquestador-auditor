# 🦈 RECOVERY PATCH — MULTI-ENV — SHARCK INPUT V2.1

Schema: `sharck.recovery.multi-env.v2`  
Mode: `OWNER_LOCK_FAIL_CLOSED`

## Fuente de verdad
- Repo: `maxbry123-commits/osquestador-auditor`
- Branch: `main`
- Root única: `➡️📂 sharck imput/`
- Handoff operativo: `HANDOFF-MULTIENV-3STEP-20X-2026-09-11.md`
- STATE base + último delta: `STATE.json` + `STATE-DELTA-032-M43-WATCHDOG-SEMANTIC-RECONCILIATION.json`
- CHECKPOINT base + último delta: `CHECKPOINT.json` + `CHECKPOINT-DELTA-030-M43-WATCHDOG-SEMANTIC-RECONCILIATION.json`
- PLAN base + último delta: `PLAN.json` + `PLAN-DELTA-014-M42-CONTROL-RECONCILIATION.json`
- DAG: `MULTIENV-DAG-3STEP-v1.json` + `MULTIENV-DAG-3STEP-v2-DELTA.json`
- Watchdog vigente: `WATCHDOG-3STEP-M43-SEMANTIC-RECONCILIATION-2026-09-12.json`

Fuente de verdad relativa: `GitHub physical tree + manifests/hashes/runs > STATE/deltas > CHECKPOINT/deltas > PLAN/deltas > Handoff > agent logs > chat`.

## Boot sequence obligatorio
`HANDOFF MULTIENV → latest CHECKPOINT delta → latest STATE delta → PLAN + delta → DAG + delta → LOG PROPIO → owner check → claim propio → execute → evidence/read-back → checkpoint delta`.

## Método único 3 pasos
1. `INVENTORY_XRAY_ARCHITECTURE`
2. `RESEARCH_PREFLIGHT_PLUS_ACQUISITION_STRATEGYDELTA_READBACK`
3. `WIRE_PRUNE_MIN_CODE_TEST`

Paso 3 sólo puede abrir después de `M06 ASTRA + M07 CLAUDE + M08 GROK + director gate`.

## Ownership
- SOL: `state/control/evidence/motor-watch`; no duplicar M06/M07/M08.
- ASTRA: owner exclusivo `M06` — arquitectura/gates/StrategyDelta/rollback/independent review.
- CLAUDE: owner exclusivo `M07` — code/ports/adapters/tests/criticidad/repairability.
- GROK: owner exclusivo `M08` — OSS/package/subtree/API alternatives/license/maintenance/contradiction.

Claim sólo por el propietario en su propio log usando SHA fresco.

## Protocolo anti-colisión
1. Fetch fresh STATE/CHECKPOINT/Handoff.
2. Verificar owner y estado del nodo.
3. Claim únicamente en log propio.
4. Ejecutar máximo 3 pasos por nodo.
5. Shared writes secuenciales con SHA fresco.
6. Ante 409: releer, mergear, nunca sobrescribir.
7. Read-back obligatorio antes de cualquier VERIFIED_CLOSED.

## Locks actuales
- `INPUT_RAW=IMMUTABLE`
- `canonical_motors=IMMUTABLE`
- `NO_LFS`
- `NO_FORCE`
- `NO_SILENT_OVERWRITE`
- `physical_repair_allowed=false`
- `b05_b06_download_allowed=false`
- `step3_allowed=false`

## Estado físico verificado para recovery
- Catálogo canónico: `117`.
- B01–B04: `17 VERIFIED_CLOSED / 23 FAILED / 0 pending`.
- 23 FAILED = `12 partial + 11 source-special/symlink`.
- Partial universe: `12 components / 139 exact anomalies`.
- M25 sandbox coverage: `3/12 components` y `4/139 anomalies`; no autoriza producción.
- B05/B06: `20 RESEARCHED_CANDIDATE_NO_DOWNLOAD`, `0 downloaded`.
- M06/M07/M08: `OPEN_UNCLAIMED` al último read-back.

## Frontier operativo
- Último nodo verificado: `M43_WATCHDOG_3STEP_SEMANTIC_RECONCILED`.
- Checkpoint vigente: `CP-V2-M43-WATCHDOG-SEMANTIC-RECONCILIATION-030`.
- M42 reconcilió PLAN M37–M41 mediante `PLAN-DELTA-014-M42-CONTROL-RECONCILIATION.json`.
- M43 corrigió el watchdog para que Step2 conserve adquisición/StrategyDelta/readback y Step3 sea sólo wire/prune/min-code/test.

## Recovery rule
Si M06/M07/M08 siguen sin claim, SOL sólo puede continuar tareas `parallel_safe/read-only` que conviertan GAP desconocido en evidencia nueva o reparen drift del control plane. No repetir X-Ray M21/M22/M23 ni redocumentar el mismo estado sin cambio.

Prohibido antes del fan-in + director gate: reparación física de los 23 FAILED, descarga B05/B06, source/ref redesign, activar MultiSOL futuro o ejecutar Step3.

## Nota histórica
La versión anterior de este Recovery conservaba el estado inicial `10 VERIFIED_CLOSED / 20 FAILED` y el handoff histórico. Esa sección quedó obsoleta tras B04 y los deltas M37–M43; esta revisión actualiza sólo control/recovery, sin mutación física.
