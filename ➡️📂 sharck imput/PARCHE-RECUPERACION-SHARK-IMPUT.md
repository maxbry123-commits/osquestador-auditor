# 🦈 PARCHE DE RECUPERACIÓN — SHARCK INPUT V2

## Fuente de verdad
Repo `maxbry123-commits/osquestador-auditor` · branch `main` · raíz `➡️📂 sharck imput/` · code root `📂 input sharck code principal/`.
V1 `➡️📂 Shack imput/` se preserva: último estado leído 47/77 VERIFIED_CLOSED + 30 GAP.

## Lectura obligatoria
`README-METODO-TRABAJO-MULTIAGENTE.md → 📁 readme arquitectura sharck imput.md → ➡️📂 readme indice de componentes sharck imput.md → PLAN.json → STATE.json → CHECKPOINT.json → log propio → GAPS-ACQUISITION-V2.md → Handoff → REVIEW-GATE-ASTRA-ENGINEERING.md`.

## Método
`INPUT_RAW → INPUT_LOCK → CONTRACT → GOALS → TASK_GRAPH → ROLE_ROUTER → OWNER_LOCK → FAN_OUT → CHECKPOINTS → EVIDENCE → FAN_IN → CROSS_REVIEW → VERDICT → NEXT_NODE`.

Pasos: 1) anotar/arquitectura/inventario; 2) adquirir con motores canónicos en lotes ≤10; 3) wire/poda mínima/code faltante/test tras review gate.

## Estado recuperable actual
Catálogo V2 = 107 (77 heredados + 30 nuevos).
Workflow = `.github/workflows/sharck-input-v2-components.yml`.
Run = `34514168678`.
Motor hash gate + sparse checkout NO LFS = PASS 3/3.

Balance read-back:
- B01 = 3 VERIFIED_CLOSED / 7 FAILED / 0 pending.
- B02 = 5 VERIFIED_CLOSED / 5 FAILED / 0 pending.
- B03 = IN_PROGRESS / 10 todavía sin verdict persistido.
- Total demostrado = 8 VERIFIED_CLOSED / 12 FAILED / 10 en ejecución.

No convertir job-success en component-success: usar índices/state de cada batch.

## GAPs
Ledger: `📂 Craxy wall bitácora stated JSON/GAPS-ACQUISITION-V2.md`.
Clases ya vistas: DESTINATION_EXISTS, READBACK_TREE_HASH_GAP, SOURCE_SPECIAL_FILE_GAP.
No borrar destinos ni editar motores para hacer PASS. Usar StrategyDelta documentada y review.

## Owners
SOL = control/estado/consolidación/motor-watch.
CLAUDE = code/ports/adapters/typing/tests.
GROK = OSS/community/HF/labs/alternatives/contradictions.
ASTRA = XRAY_ARQUITECTURA + EVALUACION_PREVIA + MEJORA_VERSIONADA + COMPONENT_GAP_RESEARCH + INDEPENDENT_VERIFY.

## Watchdog
`Sharck Input V2 Watchdog` habilitado cada hora en America/Bogota. Reanuda desde checkpoint y no salta el review gate.

## Review gate
M06 ASTRA, M07 CLAUDE, M08 GROK pendientes. Paso 3 bloqueado. Revisión externa = NOT_PERFORMED_NO_EVIDENCE; no atribuir supervisión/aprobación sin prueba.

## Checkpoint
`CP-V2-PARTIAL-ACQUISITION-004`
`resume_from=MONITOR_B03_AND_REVIEW_GAPS`.

## Reanudación exacta
1. Leer B03 job/state/index.
2. Actualizar balance real en STATE/CHECKPOINT/Handoff.
3. Ejecutar/recibir revisiones M06/M07/M08.
4. Resolver/aceptar/rechazar GAPs por evidencia.
5. Gate director/revisión externa que sea requerida.
6. Sólo después marcar STEP3_READY y trabajar 1×1.

## Cierre
VERIFIED_CLOSED exige URL/ref + ruta + commit/SHA/diff + test/log + read-back. Presencia física sola nunca basta.
