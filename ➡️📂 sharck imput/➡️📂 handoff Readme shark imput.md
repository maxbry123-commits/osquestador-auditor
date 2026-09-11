# 🦈 HANDOFF README — SHARCK INPUT V2

## Fuente de verdad
Repo: `maxbry123-commits/osquestador-auditor` · Branch: `main`
Raíz activa: `➡️📂 sharck imput/`
Código principal: `➡️📂 sharck imput/📂 input sharck code principal/`
V1 preservada: `➡️📂 Shack imput/` — 47/77 VERIFIED_CLOSED + 30 GAP como referencia read-only.

## Método — 3 pasos
1. ANOTAR + ARQUITECTURA + INVENTARIO.
2. ADQUIRIR sólo con motores canónicos, lotes máximo 10, destinos explícitos, NO LFS/force y read-back.
3. CABLEAR + PODA MÍNIMA + CODE FALTANTE + TEST sólo después del review gate.

## Estado reconciliado
- Catálogo actual: **117 = 77 V1 + 40 V2 investigados**.
- B01–B03: **10 VERIFIED_CLOSED / 20 FAILED**.
- X-Ray B01–B03: **11 PARTIAL_DESTINATION_READBACK_GAP + 9 SOURCE_SPECIAL_FILE_GAP**; runs `34535896880`, `34536177351`, recoveries `0/11`.
- B04 context/HF/eval: **7 VERIFIED_CLOSED / 3 FAILED / 0 pending**.
- B04 FAILED observados: `huggingface_hub`=`SOURCE_SPECIAL_FILE_GAP:CLAUDE.md`; `spaCy`=`DESTINATION_EXISTS`; `unstructured`=`SOURCE_SPECIAL_FILE_GAP`. No reintentar a ciegas.
- Total B01–B04: **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**. Paso 2 no es PASS global.

## M13 simulación read-only 01
Discovery → retrieval → evidence/contradiction → coverage/gaps → compression → context package.

### FACT
- OpenAI: web/file search + remote MCP para recuperación dinámica de contexto.
- Anthropic: contexto finito, recuperación just-in-time y síntesis compacta.
- OpenClaw: Skills allowlist controla visibilidad, no autorización de host.
- Hermes: MCP nativo, auto-discovery y filtros.
- Hugging Face: `huggingface_hub`, `datasets` y MCP Server oficial forman un bridge desacoplable.

### INFERENCE
Context package mínimo de alta señal: `pointer + provenance + freshness + evidence_class + contradiction_state + deferred_retrieval_handle`.

### UNKNOWN
Umbrales cuantitativos de cobertura/compresión pendientes de tests M07/M10.

## M13 simulación read-only 02
Etapas ejercidas: `INPUT_RAW_LOCK → INTENT_AND_CONSTRAINTS → ENTITY_RESOLUTION → RESEARCH_DECISION → SOURCE_AND_TOOL_DISCOVERY`.

### FACT
- OpenAI documenta recuperación dinámica de información actual/privada mediante Web Search y File Search, por lo que el input no debe asumir que el conocimiento del modelo basta: https://help.openai.com/en/articles/6639781-do-the-openai-api-models-have-knowledge-of-current-events
- Anthropic recomienda el conjunto mínimo de tokens de alta señal y retrieval just-in-time: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- GitHub separa agentes Explore/Task/general-purpose en contextos distintos y permite restringir herramientas/MCP por agente: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents ; https://docs.github.com/en/copilot/reference/custom-agents-configuration
- OpenClaw confirma que allowlists de skills son visibilidad y no frontera de autorización: https://docs.openclaw.ai/skills
- Hermes Tool Search reemplaza schemas MCP/plugin no-core por herramientas puente y carga schemas bajo demanda: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/tool-search.md
- La comunidad Hermes mantiene issues abiertos sobre desincronización/longevidad MCP, por lo que discovery exitoso no equivale automáticamente a disponibilidad operacional estable: https://github.com/NousResearch/hermes-agent/issues/84772 ; https://github.com/NousResearch/hermes-agent/issues/94723
- Hugging Face publica Skills oficiales y el sub-skill `huggingface-datasets`; el repo `huggingface/skills` está activo y Apache-2.0. El skill usa Dataset Viewer API read-only para disponibilidad, splits, rows, search/filter, parquet, size y statistics: https://huggingface.co/docs/hub/agents-skills ; https://github.com/huggingface/skills/tree/main/skills/huggingface-datasets

### INFERENCE
1. Preservar el INPUT literal antes de cualquier normalización.
2. Resolver intent/constraints y entidades de forma determinista antes de decidir investigación.
3. Abrir retrieval sólo por necesidad explícita, freshness, ambigüedad, falta de evidencia o contradicción.
4. Exponer schemas de tools/skills progresivamente después de seleccionar fuente/herramienta, no todo el catálogo de una vez.

### UNKNOWN
- threshold cuantitativo de `RESEARCH_DECISION`;
- threshold de confianza de `ENTITY_RESOLUTION`;
- presupuesto máximo de schemas/tools por request.
Estos valores quedan para tests M07/M10, no se fijan por intuición.

## Candidato de skill — NO INSTALADO
`huggingface-datasets` queda indexado como sub-skill candidato dentro del componente ya existente **Hugging Face Skills**. Fuente oficial, mantenimiento activo, Apache-2.0, utilidad read-only para discovery/retrieval de datasets. No aumenta el total de 117 componentes y no se adquiere sin gate.

## Ownership anti-colisión
- SOL: state/control/consolidation/motor-watch + M13 research orchestration read-only.
- CLAUDE: M07 code/ports/adapters/typing/tests + diagnóstico técnico.
- GROK: M08 OSS/comunidad/HF/labs/alternativas/licencias/mantenimiento/contradicciones.
- ASTRA: M06 auditoría independiente/arquitectura/mejora versionada/component gap/verify.

## Review gate
M06 ASTRA = READY_FOR_REVIEW. M07 CLAUDE = READY_FOR_REVIEW. M08 GROK = READY_FOR_REVIEW. M09 external = NOT_PERFORMED/NO_EVIDENCE. **Paso 3 = BLOCKED**.

## Motores canónicos — NO EDITAR
Raíz: `➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/`.
No LFS · no force · no silent overwrite · read-back obligatorio.

## Checkpoint vivo
`CP-V2-M13-SIM02-HFSKILL-008`
`last_verified_node=M13_SIMULATION_02_AND_HF_SUBSKILL_CANDIDATE_INDEXED`
`resume_from=M06_M07_M08_REVIEW_AND_GAP_STRATEGY_WITH_M13_READ_ONLY_PARALLEL`.

## Próximo nodo permitido
SOL: continuar simulación read-only/monitor de reviews. ASTRA/CLAUDE/GROK conservan M06/M07/M08. No reparación física B01–B04, instalación del sub-skill HF ni Paso 3 hasta evidencia/review/gate correspondiente.
