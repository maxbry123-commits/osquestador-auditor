# 🦈 HANDOFF README — SHARK IMPUT

## Fuente de verdad
Repo: `maxbry123-commits/osquestador-auditor`
Branch: `main`
Raíz: `➡️📂 Shack imput/`

## Orden de lectura obligatorio para SOL / ASTRA / GROK
1. `📁 readme arquitectura Shack imput.md`
2. `➡️📂 readme indice componentes.md`
3. `📂 Craxy wall bitácora stated JSON/STATE.json`
4. log propio del agente dentro de Craxy Wall
5. `📂 Craxy wall bitácora stated JSON/SALIDAS-CHATGPT.md`
6. `PARCHE-RECUPERACION-SHARK-IMPUT.md`
7. `➡️📂 shart imput code Run/README.md`
8. `➡️📂 shart imput code Run/memoria búsqueda.md`

## Contrato único de trabajo — 3 pasos
**1. ANOTAR + ARQUITECTURA** → registrar antes de tocar; INPUT literal inmutable.
**2. DESCARGAR + EXTRAER** → sólo motores canónicos; jobs/colas distintas, mismo code inmutable; destino explícito; read-back.
**3. CABLEAR + PODA MÍNIMA + CODE FALTANTE + TEST** → COPY-FIRST; no reescribir componentes sin necesidad demostrada.

## Arquitectura actual
`INPUT_RAW → INPUT_LOCK → FOCUS_AI_A → QUESTIONS_3_12 || PRESEARCH → ROLE/DOMAIN/GEO ROUTER → PARALLEL RESEARCH → SNAPSHOT/INDEX → RETRIEVAL/RRF → EVIDENCE/GAPS → FOCUS_AI_B → TOOL/SKILL/CODE POINTER → CONTEXT_COMPILER → MAIN_LLM`.

## Nodos activos
- SOL/ChatGPT: bootstrap, publicación, launcher de descarga y verificación.
- ASTRA: auditoría independiente de arquitectura, gaps y compatibilidad entre componentes. No duplicar nodo de SOL.
- GROK: validar alternativas OSS, comunidad dev, Code/Skill/Tool registries y contradicciones. No duplicar nodo de ASTRA.

## Regla Craxy Wall
Cada agente lee `STATE.json` antes de actuar, escribe sólo en su log y actualiza estado sin borrar entradas de otros. Si dos agentes reclaman el mismo nodo, el segundo debe escoger otro nodo independiente.

## Motores canónicos — NO EDITAR
Raíz externa ya existente en el mismo repo:
`➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/`

Blobs esperados:
- motor_1_extract_only.py `a52d5dc0e6ff26f75d753b848dcc1a40c5dd4500`
- motor_2_queue_download_extract.py `84d566e2ee4e98e42eb3a864026d067d48caabd9`
- hf_download_extract_engine.py `91e6e4486692eab314be5c7130d8310d3c855397`
- motor_3_copy_batches.py `3689924361ce4a1a9fde4ae2b6f6009c37a6042d`
- motor_copy_root_to_repo.py `8281211da76db3080fe1f1ea38b3eb0c45d655cb`
- motor_4_move_batches.py `9a21facfe11327cf60a2afca8f415ad52f0ecbe5`

## Descarga de componentes
Catálogo: **77 componentes** distribuidos en 6 lanes:
- `queues/01-search.json` — 13
- `queues/02-code.json` — 12
- `queues/03-rag.json` — 13
- `queues/04-skills.json` — 15
- `queues/05-media-input-router.json` — 18
- `queues/06-orchestration.json` — 6

Workflow:
`.github/workflows/shack-input-components.yml`

Runs de adquisición:
- `34470498878`: run inicial con checkout completo; identificado como cuello de botella por repo ~9.1 GB; NO PASS.
- `34470821525`: run optimizado con partial clone `--filter=blob:none` + sparse paths; verificar su estado real antes de actuar.

Destino físico:
`➡️📂 Shack imput/📂 Componentes para integración sharck imput/<lane>/<slug>/`

No declarar componente instalado sólo porque aparezca en el índice. Exigir `VERIFIED_CLOSED` del motor y read-back si se publicó.

## Gates
- INPUT_RAW intacto.
- componente fuente trazable a URL/ref.
- motor canónico no alterado.
- no LFS.
- no force push.
- no sobrescritura silenciosa.
- pruebas del Core pasan.
- GitHub read-back antes de DONE.

## Próximo nodo tras handoff
Leer `STATE.json`; reclamar una tarea PENDING que no tenga owner; escribir `RUNNING`; ejecutar; adjuntar evidencia; volver a escribir estado.
