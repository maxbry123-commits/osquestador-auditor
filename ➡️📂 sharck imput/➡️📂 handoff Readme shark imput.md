# 🦈 HANDOFF README — SHARCK INPUT V2

## Fuente de verdad
Repo: `maxbry123-commits/osquestador-auditor` · Branch: `main`
Raíz activa: `➡️📂 sharck imput/`
Código principal: `➡️📂 sharck imput/📂 input sharck code principal/`
V1 preservada: `➡️📂 Shack imput/` — 47/77 VERIFIED_CLOSED + 30 GAP como referencia read-only.

## Método — 3 pasos
1. ANOTAR + ARQUITECTURA + INVENTARIO.
2. ADQUIRIR sólo con motores canónicos, lotes máximo 10, destinos explícitos, NO LFS/force/silent overwrite y read-back.
3. CABLEAR + PODA MÍNIMA + CODE FALTANTE + TEST sólo después del review gate.

## Scope lock
Sharck Input transforma INPUT literal en contexto útil/verificable previo a la LLM. **No construir workflow completo.** `INPUT_RAW_LOCK` permanece inmutable.

## Estado reconciliado
- Catálogo actual: **117 = 77 V1 + 40 V2 investigados**.
- B01–B03: **10 VERIFIED_CLOSED / 20 FAILED**.
- X-Ray B01–B03: **11 PARTIAL_DESTINATION_READBACK_GAP + 9 SOURCE_SPECIAL_FILE_GAP**; runs `34535896880`, `34536177351`, recoveries `0/11`.
- B04 context/HF/eval: **7 VERIFIED_CLOSED / 3 FAILED / 0 pending**.
- B04 FAILED: `huggingface_hub=SOURCE_SPECIAL_FILE_GAP:CLAUDE.md`, `spaCy=DESTINATION_EXISTS`, `unstructured=SOURCE_SPECIAL_FILE_GAP`.
- Total B01–B04: **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**. No retry físico ciego; Paso 2 no es PASS global.

## M13 simulaciones read-only
### Simulación 01
Discovery → retrieval → evidence/contradiction → coverage/gaps → compression → context package. Resultado: contexto mínimo de alta señal con pointers, provenance, freshness y retrieval diferido.

### Simulación 02
`INPUT_RAW_LOCK → INTENT_AND_CONSTRAINTS → ENTITY_RESOLUTION → RESEARCH_DECISION → SOURCE_AND_TOOL_DISCOVERY`.

FACT: OpenAI soporta recuperación dinámica con Web/File Search; Anthropic recomienda mínimo contexto de alta señal + JIT retrieval; GitHub permite restringir tools/MCP; OpenClaw distingue skill visibility de aislamiento; Hermes usa progressive disclosure; Hugging Face publica Skills y MCP oficiales.

INFERENCE: conservar INPUT literal antes de normalización; resolver intent/constraints/entities antes de abrir búsqueda; retrieval sólo por necesidad/freshness/ambigüedad/evidence gap/contradiction; disclosure progresivo de schemas.

UNKNOWN: thresholds cuantitativos de research decision, entity confidence y tool-schema budget quedan para M07/M10.

### Simulación 03
Etapas: `WEB_CODE_SKILL_DATASET_RETRIEVAL → EVIDENCE_AND_CONTRADICTION → COVERAGE_AND_GAPS → CONTEXT_COMPRESSION → CONTEXT_PACKAGE`.

FACT:
- OpenAI documenta Web Search/File Search para contexto actual/privado y Web Search con citas: https://help.openai.com/en/articles/6639781-do-the-openai-api-models-have-knowledge-of-current-events
- Anthropic recomienda el menor conjunto de tokens de alta señal y retrieval just-in-time: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Hugging Face MCP/Hub aporta discovery y metadata del recurso.
- GitHub permite limitar tools MCP por custom agent y carga tools bajo demanda: https://docs.github.com/en/copilot/reference/custom-agents-configuration ; https://docs.github.com/en/copilot/concepts/agents/copilot-cli/tool-search
- OpenClaw trata third-party skills como código no confiable y recomienda sandbox: https://docs.openclaw.ai/skills
- Comunidad Hermes reportó un caso donde `tool_search` exitoso se repitió 1,523 veces y saturó contexto sin respuesta: https://github.com/NousResearch/hermes-agent/issues/96247

INFERENCE:
1. Cada evidencia del `CONTEXT_PACKAGE` debe portar `source_url/source_id + retrieved_at/freshness + evidence_class + contradiction_state + capability_state`.
2. `capability_state` debe diferenciar al menos `DISCOVERED → CONFIGURED → HEALTHCHECKED → OPERATIONALLY_VERIFIED`; discovery no es PASS.
3. `COVERAGE_AND_GAPS` debe terminar por suficiencia de evidencia + contradicciones tratadas, no por cantidad ilimitada de búsquedas exitosas.
4. `CONTEXT_COMPRESSION` debe preservar citations/provenance y contradicciones no resueltas.

UNKNOWN: search-call budget, coverage threshold, freshness TTL por clase de fuente y compression ratio quedan para tests M07/M10; SOL no fija valores por intuición.

### Simulación 04 — ambigüedad/contradicción/abstención
Recorrido completo: `INPUT_RAW_LOCK → intent/constraints → entity resolution → research decision → source/tool/skill/dataset discovery → retrieval → evidence/contradiction → coverage/gaps → compression → context package`.

FACT:
- OpenAI mantiene Web/File Search para recuperar contexto actual o privado: https://help.openai.com/en/articles/6639781-do-the-openai-api-models-have-knowledge-of-current-events
- Anthropic recomienda contexto mínimo de alta señal y exploración just-in-time: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- GitHub permite limitar tools y usar tool-search bajo demanda: https://docs.github.com/en/copilot/reference/custom-agents-configuration ; https://docs.github.com/en/copilot/concepts/agents/copilot-cli/tool-search
- OpenClaw declara que allowlists de skills son filtros de visibilidad/carga y no frontera de autorización de shell; sandbox/OS-user/credenciales siguen siendo necesarias: https://docs.openclaw.ai/skills
- Hermes issue #96247 es evidencia comunitaria de un loop con 1,523 `tool_search` exitosos que agotó contexto sin respuesta: https://github.com/NousResearch/hermes-agent/issues/96247
- `MCP-Atlas` de ScaleAI expone 500 tareas públicas para tool-use con servidores MCP reales, está actualizado al 2026-08-03 y publica licencia CC-BY-4.0: https://huggingface.co/datasets/ScaleAI/MCP-Atlas ; https://github.com/scaleapi/mcp-atlas

INFERENCE:
1. Una entidad ambigua no debe resolverse silenciosamente; su ambigüedad sobrevive hasta que evidencia suficiente la desambigüe.
2. `research_outcome` debe ser explícito: `ANSWERABLE | ANSWERABLE_WITH_CAVEATS | ABSTAIN_NEEDS_REVIEW`.
3. `stop_reason` debe quedar dentro del contexto (`SATURATED_NO_NEW_EVIDENCE`, `CONTRADICTION_UNRESOLVED`, `SOURCE_AUTHORITY_INSUFFICIENT`, `FRESHNESS_UNMET` u otro equivalente validado).
4. Compresión no puede borrar contradicciones, provenance ni gaps.
5. MCP-Atlas puede servir como dataset de evaluación para validar la política de stop/abstención, pero no debe auto-instalarse.

UNKNOWN: thresholds numéricos de ambigüedad, número mínimo de fuentes independientes, search-call budget, coverage, freshness y compression ratio; quedan para M07/M10/tests, no se fijan por intuición.

## Candidatos verificados — NO INSTALADOS
- `huggingface-datasets`: sub-skill de **Hugging Face Skills**, oficial, Apache-2.0, activo, discovery/retrieval read-only; no aumenta los 117 componentes.
- `MCP-Atlas`: **dataset candidato**, no componente. Fuente HF `ScaleAI/MCP-Atlas`, repo `scaleapi/mcp-atlas`, CC-BY-4.0, actualizado 2026-08-03; utilidad propuesta = benchmark de tool-selection/coverage/stop/abstención. Estado `INDEXED_CANDIDATE_NO_INSTALL`.

## Ownership anti-colisión
- SOL: state/control/consolidation/motor-watch + M13 research orchestration read-only.
- CLAUDE: M07 code/ports/adapters/typing/tests + diagnóstico técnico.
- GROK: M08 OSS/comunidad/HF/labs/alternativas/licencias/mantenimiento/contradicciones.
- ASTRA: M06 auditoría independiente/arquitectura/mejora versionada/component gap/verify.

Logs releídos: ASTRA/CLAUDE/GROK continúan `READY_TO_JOIN`; no existe evidencia verificable de review/verdict nuevo.

## Review gate
M06 ASTRA = READY_FOR_REVIEW. M07 CLAUDE = READY_FOR_REVIEW. M08 GROK = READY_FOR_REVIEW. M09 external = NOT_PERFORMED/NO_EVIDENCE. **Paso 3 = BLOCKED**.

## Motores canónicos — NO EDITAR
Raíz: `➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/`.
No LFS · no force · no silent overwrite · read-back obligatorio.

## Checkpoint vivo
`CP-V2-M13-SIM04-ABSTAIN-010`
`last_verified_node=M13_SIMULATION_04_AMBIGUITY_CONTRADICTION_ABSTENTION`
`resume_from=M06_M07_M08_REVIEW_AND_GAP_STRATEGY_WITH_M13_READ_ONLY_PARALLEL`.

## Próximo nodo permitido
SOL: siguiente simulación/evidencia read-only y monitor de reviews. ASTRA/CLAUDE/GROK conservan M06/M07/M08. No reparación física B01–B04, instalación del sub-skill HF, adquisición de MCP-Atlas ni Paso 3 hasta evidencia/review/gate correspondiente.
