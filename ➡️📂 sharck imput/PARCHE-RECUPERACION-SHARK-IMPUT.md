# 🦈 PARCHE DE RECUPERACIÓN — SHARCK INPUT V2

## Fuente de verdad
Repo `maxbry123-commits/osquestador-auditor` · branch `main` · raíz `➡️📂 sharck imput/` · code root `📂 input sharck code principal/`.
V1 `➡️📂 Shack imput/` preservada: último estado leído 47/77 VERIFIED_CLOSED + 30 GAP.

## Lectura obligatoria
`README-METODO-TRABAJO-MULTIAGENTE.md → 📁 readme arquitectura sharck imput.md → ➡️📂 readme indice de componentes sharck imput.md → PLAN.json → STATE.json → CHECKPOINT.json → log propio → GAPS-ACQUISITION-V2.md → READBACK-XRAY-2026-09-10.md → Handoff → recovery específico del entorno → REVIEW-GATE-ASTRA-ENGINEERING.md`.

## Método
`INPUT_RAW → INPUT_LOCK → CONTRACT → GOALS → TASK_GRAPH → ROLE_ROUTER → OWNER_LOCK → FAN_OUT → CHECKPOINTS → EVIDENCE → FAN_IN → CROSS_REVIEW → VERDICT → NEXT_NODE`.

Pasos: 1) anotar/arquitectura/inventario; 2) adquirir con motores canónicos en lotes ≤10; 3) wire/poda mínima/code faltante/test tras review gate.

## Estado recuperable
- Catálogo: 107 = 77 heredados + 30 nuevos.
- Método/arquitectura/índice/PLAN/STATE/CHECKPOINT/Handoff/Review Gate: publicados y read-back desde main.
- Recovery anti-colisión: `RECOVERY-GROK-SHARCK-INPUT.md` y `RECOVERY-MULTI-ENV-SHARCK-INPUT.md`.
- Memoria de búsqueda: `📂 input sharck code principal/memoria búsqueda.md`.
- Watchdog: `Sharck Input V2 Watchdog`, ENABLED HOURLY, America/Bogota.

## Adquisición inicial
Run `34514168678`:
- B01 3 VERIFIED_CLOSED / 7 FAILED.
- B02 5 VERIFIED_CLOSED / 5 FAILED.
- B03 2 VERIFIED_CLOSED / 8 FAILED.
- TOTAL 10 VERIFIED_CLOSED / 20 FAILED / 0 pending.
Veredicto semántico: `GAPS_PENDING` aunque la UI histórica quedó verde.

Wrapper fail-closed corregido en `1bb43ca45bd548278cb2074cb563bd2ece0cab43`; motores no modificados.

## X-Ray LOOP posterior
Clasificación exacta de los 20 FAILED iniciales:
- 6 DESTINATION_EXISTS;
- 5 READBACK_TREE_HASH_GAP;
- 9 SOURCE_SPECIAL_FILE_GAP.

SOL ejecutó una StrategyDelta estrictamente read-only con `.github/workflows/sharck-input-v2-readback-recover.yml`, importando `sha256()` + `tree_hash()` del HF engine canónico blob `91e6e4486692eab314be5c7130d8310d3c855397`.

Runs: `34535896880` y `34536177351`.
Resultado: **0/11 recoveries** de las primeras dos clases. Los 11 destinos tienen manifiesto/código parcial pero hash, conteo y/o bytes no coinciden con el manifiesto esperado. No se borraron, movieron ni redescargaron.

Estado operacional actual de los 20 GAP V2:
- **11 PARTIAL_DESTINATION_READBACK_GAP**;
- **9 SOURCE_SPECIAL_FILE_GAP**.

Detalle: `📂 Craxy wall bitácora stated JSON/READBACK-XRAY-2026-09-10.md`.

## Owners / anti-colisión
SOL = GAP_WATCHDOG + estado/consolidación/motor-watch; mientras reviews estén pendientes, sólo monitor/read-only evidence.
CLAUDE = M07 code/ports/adapters/typing/tests + diagnóstico técnico de GAPs.
GROK = M08 OSS/community/HF/labs/alternatives/licencias/mantenimiento/contradicciones.
ASTRA = M06 XRAY_ARQUITECTURA + EVALUACION_PREVIA + MEJORA_VERSIONADA + COMPONENT_GAP_RESEARCH + INDEPENDENT_VERIFY.
OTRO ENTORNO = owner NONE hasta una tarea libre/asignada.

Shared-write rule: PLAN/STATE/CHECKPOINT/Handoff/Recovery se actualizan secuencialmente y siempre con SHA fresco. Cada agente usa su log propio. Si otro owner ya reclama el nodo, NO WRITE y elegir sólo una tarea `parallel_safe` libre.

## Review gate
M06 ASTRA, M07 CLAUDE y M08 GROK = `READY_FOR_REVIEW`.
M09 revisión externa = `NOT_PERFORMED_NO_EVIDENCE`.
M10 integración = BLOCKED.
Paso 3 = BLOCKED.

No afirmar revisión/supervisión externa sin evidencia.

## Checkpoint
`CP-V2-POST-XRAY-006`
`last_verified_node=M11_READBACK_XRAY_11_PARTIAL_DESTINATIONS`
`resume_from=M06_M07_M08_REVIEW_AND_GAP_STRATEGY`.

## Reanudación exacta
1. Cada agente lee parche + Handoff + STATE + CHECKPOINT + log propio.
2. ASTRA/CLAUDE/GROK reclaman exclusivamente M06/M07/M08 y trabajan en paralelo.
3. Revisar 11 PARTIAL y 9 SPECIAL sin reintentos ciegos.
4. Candidatos, todavía NO ejecutados: partial → preserve/quarantine versionado con Motor4 + reacquisition 1×1; special → source/ref/subproject/dependency/alternative.
5. Cada review escribe evidencia en su log; consolidación sólo después.
6. Director decide/promueve StrategyDelta.
7. Watchdog continúa tareas `parallel_safe` autorizadas cada hora.
8. Sólo con review gate favorable se marca STEP3_READY y se integra 1×1.

## Cierre
VERIFIED_CLOSED exige evidencia material y read-back. Job verde, folder existente, propuesta LLM o revisión sin log no equivalen a PASS.
