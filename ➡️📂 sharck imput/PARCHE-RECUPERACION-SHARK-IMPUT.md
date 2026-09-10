# 🦈 PARCHE DE RECUPERACIÓN — SHARCK INPUT V2

## Fuente de verdad
Repo `maxbry123-commits/osquestador-auditor` · branch `main` · raíz `➡️📂 sharck imput/` · code root `📂 input sharck code principal/`.
V1 `➡️📂 Shack imput/` preservada: último estado leído 47/77 VERIFIED_CLOSED + 30 GAP.

## Lectura obligatoria
`README-METODO-TRABAJO-MULTIAGENTE.md → 📁 readme arquitectura sharck imput.md → ➡️📂 readme indice de componentes sharck imput.md → PLAN.json → STATE.json → CHECKPOINT.json → log propio → GAPS-ACQUISITION-V2.md → Handoff → REVIEW-GATE-ASTRA-ENGINEERING.md`.

## Método
`INPUT_RAW → INPUT_LOCK → CONTRACT → GOALS → TASK_GRAPH → ROLE_ROUTER → OWNER_LOCK → FAN_OUT → CHECKPOINTS → EVIDENCE → FAN_IN → CROSS_REVIEW → VERDICT → NEXT_NODE`.

Pasos: 1) anotar/arquitectura/inventario; 2) adquirir con motores canónicos en lotes ≤10; 3) wire/poda mínima/code faltante/test tras review gate.

## Estado recuperable
- Catálogo: 107 = 77 heredados + 30 nuevos.
- Método/arquitectura/índice/PLAN/STATE/CHECKPOINT/Handoff/Review Gate: publicados y leídos desde main.
- Memoria de búsqueda: `📂 input sharck code principal/memoria búsqueda.md`.
- Watchdog: `Sharck Input V2 Watchdog`, ENABLED HOURLY, America/Bogota.

## Adquisición
Run inicial `34514168678` completó los tres jobs. La UI de Actions indica `success`, pero los state/index del motor dan:
- B01 3 VERIFIED_CLOSED / 7 FAILED.
- B02 5 VERIFIED_CLOSED / 5 FAILED.
- B03 2 VERIFIED_CLOSED / 8 FAILED.
- TOTAL 10 VERIFIED_CLOSED / 20 FAILED / 0 pending.
Veredicto semántico: `GAPS_PENDING`.

El false-green del wrapper fue corregido sin tocar motores en commit `1bb43ca45bd548278cb2074cb563bd2ece0cab43`: futuras ejecuciones leen STATE y fallan si el batch no es 10/10. La edición del workflow ya no auto-dispara una nueva adquisición.

## GAP ledger
`📂 Craxy wall bitácora stated JSON/GAPS-ACQUISITION-V2.md` contiene las 20 StrategyDelta.
Clases: DESTINATION_EXISTS, READBACK_TREE_HASH_GAP, SOURCE_SPECIAL_FILE_GAP, WORKFLOW_FALSE_GREEN_GAP corregido.
No borrar destinos ni modificar motores para intentar pasar.

## Owners
SOL = estado/consolidación/motor-watch.
CLAUDE = code/ports/adapters/typing/tests + diagnóstico técnico de GAPs.
GROK = OSS/community/HF/labs/alternatives/licencias/contradicciones.
ASTRA = XRAY_ARQUITECTURA + EVALUACION_PREVIA + MEJORA_VERSIONADA + COMPONENT_GAP_RESEARCH + INDEPENDENT_VERIFY.

## Review gate
M06 ASTRA, M07 CLAUDE y M08 GROK están `READY_FOR_REVIEW` y deben registrar evidencia en sus logs/Craxy Wall.
Paso 3 bloqueado. Revisión externa = `NOT_PERFORMED_NO_EVIDENCE`; este paquete sólo habilita la revisión que organice el director.

## Checkpoint
`CP-V2-PRE-REVIEW-005`
`resume_from=M06_M07_M08_REVIEW_AND_GAP_STRATEGY`.

## Reanudación exacta
1. Cada agente lee este parche + Handoff + STATE + CHECKPOINT.
2. ASTRA/CLAUDE/GROK reclaman exclusivamente M06/M07/M08.
3. Revisar los 20 FAILED y las 20 StrategyDelta; no reintentar colisiones sin diagnóstico.
4. Registrar review/evidencia en Craxy Wall y actualizar checkpoint.
5. Director decide StrategyDelta/review adicional.
6. Watchdog continúa GAPs autorizados.
7. Sólo con review gate favorable se marca STEP3_READY y se integra 1×1.

## Cierre
VERIFIED_CLOSED exige URL/ref + ruta + commit/SHA/diff + test/log + read-back. Job verde o presencia física nunca bastan por sí solos.
