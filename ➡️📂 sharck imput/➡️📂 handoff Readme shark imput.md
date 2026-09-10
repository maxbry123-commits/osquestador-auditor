# 🦈 HANDOFF README — SHARCK INPUT V2

## Fuente de verdad
Repo: `maxbry123-commits/osquestador-auditor`
Branch: `main`
Raíz activa: `➡️📂 sharck imput/`
Código principal: `➡️📂 sharck imput/📂 input sharck code principal/`
V1 preservada: `➡️📂 Shack imput/` — referencia histórica, no destruir.

## Orden de recuperación obligatorio
1. `README-METODO-TRABAJO-MULTIAGENTE.md`
2. `📁 readme arquitectura sharck imput.md`
3. `➡️📂 readme indice de componentes sharck imput.md`
4. `📂 Craxy wall bitácora stated JSON/PLAN.json`
5. `📂 Craxy wall bitácora stated JSON/STATE.json`
6. `📂 Craxy wall bitácora stated JSON/CHECKPOINT.json`
7. log propio `SOL-LOG.md | ASTRA-LOG.md | GROK-LOG.md | CLAUDE-LOG.md`
8. `PARCHE-RECUPERACION-SHARK-IMPUT.md`
9. `REVIEW-GATE-ASTRA-ENGINEERING.md`
10. este Handoff

## Contrato de trabajo — 3 pasos
1. ANOTAR + ARQUITECTURA + INVENTARIO.
2. ADQUIRIR componentes usando únicamente motores canónicos, grupos de máximo 10, destino explícito y read-back.
3. CABLEAR + PODA MÍNIMA + CODE FALTANTE + TEST, únicamente después del gate de revisión.

## Estado comprobado heredado V1
Catálogo V1: 77.
`VERIFIED_CLOSED`: 47.
GAP residuales: 30.
No se declara V1 77/77.

## Estado V2 comprobado
Catálogo total documentado: 107 = 77 V1 + 30 nuevos investigados.
Los 30 nuevos están divididos exactamente en:
- B01 web/research/capture: 10.
- B02 IR/evidence/index: 10.
- B03 code intelligence/runtime: 10.

Workflow: `.github/workflows/sharck-input-v2-components.yml`
Commit de montaje: `c276f51a56f5c0bc433d2991240c72f14142d464`
Run inicial: `34514168678`
Último estado comprobado: `IN_PROGRESS`; conclusión `null`.
Jobs B01/B02/B03: los tres `IN_PROGRESS`.
Gates ya comprobados en los tres jobs:
- `Partial sparse checkout — NO LFS`: PASS 3/3.
- `Verify canonical motor blob SHAs`: PASS 3/3.
- `Execute canonical queue download + extraction motor`: IN_PROGRESS 3/3.

Por tanto: `MOTORES_MONTADOS_Y_EJECUTANDO`, pero todavía `0/30 VERIFIED_CLOSED` hasta que state/index/read-back demuestren resultados individuales.

## Motores canónicos — INMUTABLES
Raíz externa de control:
`➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/`

Blobs obligatorios:
- motor_1_extract_only.py `a52d5dc0e6ff26f75d753b848dcc1a40c5dd4500`
- motor_2_queue_download_extract.py `84d566e2ee4e98e42eb3a864026d067d48caabd9`
- hf_download_extract_engine.py `91e6e4486692eab314be5c7130d8310d3c855397`
- motor_3_copy_batches.py `3689924361ce4a1a9fde4ae2b6f6009c37a6042d`
- motor_copy_root_to_repo.py `8281211da76db3080fe1f1ea38b3eb0c45d655cb`
- motor_4_move_batches.py `9a21facfe11327cf60a2afca8f415ad52f0ecbe5`

No editar/refactorizar/adaptar estos motores. No LFS. No force. Destinos explícitos.

## Roles y ownership
### SOL
Control de estado, integración, consolidación, vigilancia de motores y gates.
### CLAUDE
Code Pointer RAG, contracts/ports/adapters/plugins, typing y tests.
### GROK
OSS, comunidad, Hugging Face/labs, alternativas, issues/benchmarks y contradicciones.
### ASTRA — scope separado
1. XRAY_ARQUITECTURA.
2. EVALUACION_PREVIA.
3. MEJORA_VERSIONADA.
4. COMPONENT_GAP_RESEARCH.
5. INDEPENDENT_VERIFY.
ASTRA no duplica implementación rutinaria de SOL/CLAUDE.

## Gate antes de integración
No iniciar Paso 3 mientras no estén registradas las revisiones M06 ASTRA, M07 CLAUDE y M08 GROK, además del gate que defina el director y los estados reales de adquisición.
`REVIEW-GATE-ASTRA-ENGINEERING.md` contiene la checklist de revisión.
Una revisión externa adicional puede usar este paquete, pero actualmente no existe evidencia de que un equipo externo haya revisado/aprobado el proyecto. No atribuir supervisión ni aprobación sin prueba.

## Watchdog
El watchdog horario de ChatGPT/SOL fue actualizado a V2. Lee método/PLAN/STATE/CHECKPOINT/Handoff/Recovery, vigila el run y reanuda desde `resume_from`. No puede saltar el review gate.

## Contrato de checkpoint
Cada agente: `READ → CLAIM → RUN → EVIDENCE → CHECKPOINT → READY_FOR_REVIEW`.
Si encuentra GAP: registrar evidencia, investigar StrategyDelta y continuar otra tarea independiente si existe. No loop CPU infinito; persistencia + watchdog reanudan el LOOP.

## Próximo nodo seguro
1. finalizar/leer run `34514168678` y state/index por batch;
2. sincronizar STATE/CHECKPOINT con resultados reales;
3. M06 ASTRA + M07 CLAUDE + M08 GROK independientes;
4. gate del director/revisión adicional indicada;
5. sólo entonces preparar Paso 3 1×1.
