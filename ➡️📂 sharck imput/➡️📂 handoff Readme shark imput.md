# 🦈 HANDOFF README — SHARCK INPUT V2

## Fuente de verdad
Repo: `maxbry123-commits/osquestador-auditor` · Branch: `main`
Raíz activa: `➡️📂 sharck imput/`
Código principal: `➡️📂 sharck imput/📂 input sharck code principal/`
V1 preservada: `➡️📂 Shack imput/` — último estado leído 47/77 VERIFIED_CLOSED + 30 GAP; no destruir.

## Orden de recuperación
1. `README-METODO-TRABAJO-MULTIAGENTE.md`
2. `📁 readme arquitectura sharck imput.md`
3. `➡️📂 readme indice de componentes sharck imput.md`
4. `📂 Craxy wall bitácora stated JSON/PLAN.json`
5. `STATE.json`
6. `CHECKPOINT.json`
7. log propio SOL/ASTRA/GROK/CLAUDE
8. `GAPS-ACQUISITION-V2.md`
9. `PARCHE-RECUPERACION-SHARK-IMPUT.md`
10. `REVIEW-GATE-ASTRA-ENGINEERING.md`
11. este Handoff

## Método aprobado — 3 pasos
1. ANOTAR + ARQUITECTURA + INVENTARIO.
2. ADQUIRIR sólo con motores canónicos, lotes máximo 10, destino explícito, NO LFS/force, read-back.
3. CABLEAR + PODA MÍNIMA + CODE FALTANTE + TEST sólo después de adquisición/review gate.

## V2 — arquitectura y componentes
Catálogo: 107 = 77 V1 + 30 nuevos investigados.
B01 web/research/capture = 10.
B02 IR/evidence/index = 10.
B03 code intelligence/runtime = 10.

Workflow: `.github/workflows/sharck-input-v2-components.yml`
Commit: `c276f51a56f5c0bc433d2991240c72f14142d464`
Run: `34514168678`.

### Último balance con read-back
- B01: `3 VERIFIED_CLOSED / 7 FAILED / 0 pending`.
- B02: `5 VERIFIED_CLOSED / 5 FAILED / 0 pending`.
- B03: `IN_PROGRESS`, 10 aún sin verdict remoto persistido al actualizar este handoff.
- Total V2 demostrado: `8 VERIFIED_CLOSED / 12 FAILED / 10 EN EJECUCIÓN`.

Gates de los tres jobs: sparse checkout NO LFS PASS 3/3 + blob SHA de motores PASS 3/3.
Los 12 fallos están registrados en `GAPS-ACQUISITION-V2.md`; clases observadas: `DESTINATION_EXISTS`, `READBACK_TREE_HASH_GAP`, `SOURCE_SPECIAL_FILE_GAP`.

## Motores canónicos — NO EDITAR
Raíz: `➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/`
Blobs:
- motor_1 `a52d5dc0e6ff26f75d753b848dcc1a40c5dd4500`
- motor_2 `84d566e2ee4e98e42eb3a864026d067d48caabd9`
- hf engine `91e6e4486692eab314be5c7130d8310d3c855397`
- motor_3 `3689924361ce4a1a9fde4ae2b6f6009c37a6042d`
- copy-root `8281211da76db3080fe1f1ea38b3eb0c45d655cb`
- motor_4 `9a21facfe11327cf60a2afca8f415ad52f0ecbe5`

## Ownership
- SOL: estado, consolidación, integración y motor-watch.
- CLAUDE: Code Pointer RAG, contracts/ports/adapters/plugins, typing/tests.
- GROK: OSS/comunidad/HF/labs/alternativas/contradicciones.
- ASTRA — separado: XRAY_ARQUITECTURA, EVALUACION_PREVIA, MEJORA_VERSIONADA, COMPONENT_GAP_RESEARCH, INDEPENDENT_VERIFY.

## Review gate
`REVIEW-GATE-ASTRA-ENGINEERING.md` está listo. M06 ASTRA, M07 CLAUDE y M08 GROK permanecen pendientes de revisión real. Paso 3 = BLOCKED.
No existe evidencia de revisión/aprobación externa todavía; este paquete sólo la habilita.

## Watchdog
`Sharck Input V2 Watchdog` está ENABLED cada hora (America/Bogota). Relee PLAN/STATE/CHECKPOINT/Handoff/Recovery, vigila batches y no salta el review gate.

## Checkpoint vivo
`CP-V2-PARTIAL-ACQUISITION-004` → `resume_from=MONITOR_B03_AND_REVIEW_GAPS`.

## Siguiente nodo
Leer B03 state/index cuando se publique → sincronizar balance → revisiones ASTRA/CLAUDE/GROK → gate director → sólo entonces Paso 3.
