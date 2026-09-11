# SOL / ChatGPT — LOG SHARCK INPUT V2

## 2026-09-10 — PRE-REVIEW BUILD
- Reconstruido estado V1 desde GitHub: 47/77 VERIFIED_CLOSED, 30 GAP.
- Creada V2 `➡️📂 sharck imput/` sin destruir V1 `➡️📂 Shack imput/`.
- Publicado método multiagente con 5 refutaciones, 12 GOALS, Council12 y 6 simulaciones.
- Investigados/catalogados 30 componentes adicionales; catálogo inicial V2=107.
- Creada arquitectura V2, PLAN, STATE, CHECKPOINT, Handoff, Recovery, Review Gate y memoria de búsqueda.
- Ejecutado run inicial `34514168678`: B01=3/7, B02=5/5, B03=2/8; total 10 VERIFIED_CLOSED / 20 FAILED.
- Corregido false-green del wrapper sin editar motores canónicos.

## 2026-09-10 — LOOP GAP X-RAY / STRATEGYDELTA READ-ONLY
- 20 FAILED B01–B03: 6 DESTINATION_EXISTS + 5 READBACK_TREE_HASH_GAP + 9 SOURCE_SPECIAL_FILE_GAP.
- Runs `34535896880`, `34536177351`: 0/11 recovered; 11/11 partial/incomplete.
- Operacional: 11 `PARTIAL_DESTINATION_READBACK_GAP` + 9 `SOURCE_SPECIAL_FILE_GAP`.
- No se borró, movió, reemplazó ni redescargó ningún destino parcial. Motores no modificados.
- Checkpoint: `CP-V2-POST-XRAY-006`; M06/M07/M08 pendientes.

## 2026-09-10 — WATCHDOG READ-ONLY REVIEW-GATE PASS
- Releídos Handoff/PLAN/STATE/CHECKPOINT/GAPS/X-Ray/Recovery/logs.
- No evidencia de claim/review/verdict M06/M07/M08.
- Run repo-wide ajeno a inventario V2 no se usó para reclasificar B01–B03.

## 2026-09-10 — M13 SIMULATION 01
### Reconciliación previa
- PLAN/STATE estaban desfasados en catálogo=107, pero el índice actual de `main` ya contenía **117 componentes** y B04.
- `B04-INDEX.md` / `B04-state.json`: **7 VERIFIED_CLOSED / 3 FAILED / 0 pending**.
- B04 VERIFIED_CLOSED: datasets, hf-mcp-server, LLMLingua, markitdown, chonkie, ragas, deepeval.
- B04 FAILED: huggingface_hub=`SOURCE_SPECIAL_FILE_GAP:CLAUDE.md`; spaCy=`DESTINATION_EXISTS`; unstructured=`SOURCE_SPECIAL_FILE_GAP`.
- No se ejecutó retry físico ni modificación de motor/destino/source/ref.

### Simulación por etapas
`SOURCE_AND_TOOL_DISCOVERY → WEB_CODE_SKILL_DATASET_RETRIEVAL → EVIDENCE_AND_CONTRADICTION → COVERAGE_AND_GAPS → CONTEXT_COMPRESSION → CONTEXT_PACKAGE`.

### FACT
1. OpenAI publica Responses/Agents con web search, file search, remote MCP, guardrails/tracing y sandbox/harness para traer contexto y operar de forma controlada.
   - https://openai.com/index/new-tools-for-building-agents/
   - https://openai.com/index/new-tools-and-features-in-the-responses-api/
   - https://openai.com/index/the-next-evolution-of-the-agents-sdk/
2. Anthropic recomienda tratar el contexto como recurso finito, usar retrieval just-in-time, referencias ligeras y sub-agentes que devuelven síntesis destiladas.
   - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
   - https://www.anthropic.com/engineering/multi-agent-research-system
3. OpenClaw documenta que una allowlist de Skills sólo filtra visibilidad/carga; para aislamiento real recomienda sandbox/OS-user isolation, host-exec restringido y credenciales por agente.
   - https://docs.openclaw.ai/tools/skills
   - https://docs.openclaw.ai/skills-config
4. Hermes Agent incorpora cliente MCP nativo con descubrimiento de tools y filtrado por servidor.
   - https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md
5. Hugging Face mantiene tres primitivas oficiales útiles para el bridge: `huggingface_hub` (cliente/CLI, Apache-2.0), `datasets` (load/stream/preprocess, Apache-2.0) y `hf-mcp-server` (MCP oficial, MIT). Ya estaban catalogadas en B04.
   - https://github.com/huggingface/huggingface_hub
   - https://github.com/huggingface/datasets
   - https://github.com/huggingface/hf-mcp-server

### INFERENCE
- El `CONTEXT_PACKAGE` de Sharck debe preferir un set mínimo de alta señal: `pointer + provenance + freshness + evidence_class + contradiction_state + deferred_retrieval_handle`, en lugar de precargar repos/datasets/tools completos.
- El bridge HF debe permanecer desacoplado en tres adapters: Hub discovery/pointers, dataset load/stream y MCP tool exposure. Esto reduce acoplamiento y respeta el scope PRE-LLM.
- Skills/tools deben aparecer por shortlist y cargar bajo demanda; el permiso de ejecución debe permanecer fuera de la simple capa de discovery.

### UNKNOWN
- Umbrales cuantitativos de cobertura, compresión y cuándo promover deferred retrieval requieren tests del carril M07/M10; no se fijan por intuición.
- Los tres FAILED de B04 requieren revisión owner/gate antes de reparación física o cambio source/ref/design.

### Control plane actualizado
- PLAN rev6 → catálogo 117, B04 registrado, M13 simulation_01 verified.
- STATE rev9 → 17 VERIFIED_CLOSED / 23 FAILED para B01–B04, sin alterar provenance B01–B03.
- CHECKPOINT → `CP-V2-M13-SIM01-B04-007`.
- Handoff e índice sincronizados.
- Paso 3 sigue BLOCKED; M06/M07/M08 siguen pendientes.

## 2026-09-10 — M13 SIMULATION 02
### Ownership/read-back previo
- INPUT-DIRECTOR, PLAN, STATE, CHECKPOINT, Handoff, GAPS y este log fueron releídos desde `main` antes de operar.
- ASTRA/CLAUDE/GROK logs siguen en `READY_TO_JOIN`; no existe evidencia nueva de claim/review/verdict M06/M07/M08.
- No se duplicó M06/M07/M08 y Paso 3 permanece bloqueado.

### Etapas simuladas
`INPUT_RAW_LOCK → INTENT_AND_CONSTRAINTS → ENTITY_RESOLUTION → RESEARCH_DECISION → SOURCE_AND_TOOL_DISCOVERY`.

### FACT
1. OpenAI: para conocimiento actual/privado, Web Search y File Search recuperan información dinámicamente; el input no debe asumir suficiencia del conocimiento interno del modelo.
   - https://help.openai.com/en/articles/6639781-do-the-openai-api-models-have-knowledge-of-current-events
2. Anthropic: contexto es un recurso finito; recomienda el menor conjunto de tokens de alta señal y retrieval just-in-time.
   - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
3. GitHub: Copilot CLI separa Explore, Task y General-purpose en contextos distintos; custom agents permiten restringir tools y tools MCP.
   - https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents
   - https://docs.github.com/en/copilot/reference/custom-agents-configuration
4. OpenClaw: una allowlist de Skills controla visibilidad/carga pero no constituye frontera de autorización del shell/host.
   - https://docs.openclaw.ai/skills
5. Hermes: Tool Search implementa progressive disclosure para MCP/plugin tools y evita cargar todos los schemas en cada turno.
   - https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/tool-search.md
6. Comunidad Hermes: existen issues abiertos sobre herramientas MCP descubiertas pero no disponibles por el dispatch principal y timeouts de herramientas largas con progress notifications; discovery no debe equivaler a operational PASS.
   - https://github.com/NousResearch/hermes-agent/issues/84772
   - https://github.com/NousResearch/hermes-agent/issues/94723
7. Hugging Face: el repo oficial `huggingface/skills` está activo, es Apache-2.0 y publica Skills oficiales. `huggingface-datasets` usa Dataset Viewer API para operaciones read-only de availability, splits, rows, search/filter, parquet, size y statistics.
   - https://huggingface.co/docs/hub/agents-skills
   - https://github.com/huggingface/skills
   - https://github.com/huggingface/skills/tree/main/skills/huggingface-datasets

### INFERENCE
- `INPUT_RAW_LOCK` debe conservar bytes/texto literal antes de cualquier limpieza, resumen o entity normalization.
- `INTENT_AND_CONSTRAINTS` + `ENTITY_RESOLUTION` deben producir un contrato intermedio verificable antes de abrir búsqueda.
- `RESEARCH_DECISION` debe ser un gate explícito: abrir retrieval por necesidad explícita, freshness, ambigüedad, missing evidence o contradiction; si no, continuar sin búsqueda externa.
- `SOURCE_AND_TOOL_DISCOVERY` debe usar shortlist/progressive disclosure; exponer todos los schemas/tools por defecto aumenta ruido de contexto y decisiones ambiguas.
- `tool_discovered` debe permanecer distinto de `tool_operationally_verified`; issues de Hermes respaldan un read-back/health check antes de confiar en la capacidad.

### UNKNOWN
- Threshold cuantitativo de `RESEARCH_DECISION`.
- Threshold de confianza para entity resolution/alias matching.
- Presupuesto máximo de schemas/tools por request.
- Estos valores requieren tests M07/M10; SOL no los fijó por intuición.

### Candidato detectado y gate aplicado
- Candidato: `huggingface-datasets` Skill.
- Ya existe el parent `Hugging Face Skills` como componente #40; no se creó componente duplicado ni cambió el total 117.
- Fuente oficial verificada: `huggingface/skills`.
- Mantenimiento: repo activo, push observado 2026-09-10.
- Licencia: Apache-2.0.
- Utilidad: retrieval read-only de datasets para discovery/evidence.
- Estado: `INDEXED_CANDIDATE_NO_INSTALL`.
- No se instaló, adquirió ni activó.

### Mutaciones realizadas
Sólo control plane/documentación: PLAN, STATE, CHECKPOINT, Handoff, índice y SOL log. Cero cambios en componentes, destinos parciales, source/ref o motores canónicos.

### Balance preservado
- B01–B03: 10 VERIFIED_CLOSED / 20 FAILED.
- B04: 7 VERIFIED_CLOSED / 3 FAILED.
- B01–B04: 17 VERIFIED_CLOSED / 23 FAILED / 0 pending.
- M06/M07/M08: pendientes; Paso 3 bloqueado.
- Checkpoint objetivo: `CP-V2-M13-SIM02-HFSKILL-008`.

## 2026-09-10 — M13 SIMULATION 03
### Read-back/ownership previo
- Releídos `INPUT-DIRECTOR-2026-09-10T2024-05.json`, PLAN, STATE, CHECKPOINT, Handoff, GAPS, SOL-LOG y logs ASTRA/CLAUDE/GROK desde `main`.
- ASTRA/CLAUDE/GROK siguen `READY_TO_JOIN`; no existe evidencia verificable de claim/review/verdict M06/M07/M08.
- Paso 3 continúa bloqueado. No se tocó M06/M07/M08.

### Etapas simuladas
`WEB_CODE_SKILL_DATASET_RETRIEVAL → EVIDENCE_AND_CONTRADICTION → COVERAGE_AND_GAPS → CONTEXT_COMPRESSION → CONTEXT_PACKAGE`.

### FACT
1. OpenAI mantiene Web Search y File Search para recuperar contexto actual/privado dinámicamente; Web Search devuelve citas y puede combinarse con otras tools.
   - https://help.openai.com/en/articles/6639781-do-the-openai-api-models-have-knowledge-of-current-events
   - https://openai.com/index/new-tools-for-building-agents/
2. Anthropic recomienda tratar contexto como recurso finito y seleccionar el menor conjunto de tokens de alta señal, con retrieval just-in-time.
   - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
3. Hugging Face MCP devuelve recursos con metadata, links y context; `hf_fs` es una herramienta primaria para navegar Hub. Skills y MCP permanecen superficies separables.
   - https://huggingface.co/docs/hub/en/agents-mcp
   - https://huggingface.co/docs/hub/en/agents-skills
4. GitHub custom agents permiten restringir tools/MCP. En Copilot cloud, una vez configurado un MCP, sus tools pueden ejecutarse autónomamente; además hay diferencias de soporte por superficie/auth.
   - https://docs.github.com/en/copilot/reference/custom-agents-configuration
   - https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers
5. OpenClaw trata third-party skills como código no confiable, recomienda leerlos antes de habilitar y preferir sandbox para inputs/tools riesgosos.
   - https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md
6. Comunidad Hermes: issue #96247 reporta una sesión con 1,523 llamadas `tool_search` exitosas sobre 17 tools diferidas que llenó ~130k de contexto y terminó por context-length sin respuesta. Es evidencia comunitaria de que `search_success` no equivale a `coverage_sufficient` ni a ejecución operacional sana.
   - https://github.com/NousResearch/hermes-agent/issues/96247

### INFERENCE
- Cada item del `CONTEXT_PACKAGE` debe incluir como mínimo `source_url/source_id`, `retrieved_at/freshness`, `evidence_class`, `contradiction_state` y `capability_state` además del pointer/contenido comprimido.
- `capability_state` debe separar `DISCOVERED`, `CONFIGURED`, `HEALTHCHECKED` y `OPERATIONALLY_VERIFIED`. Un tool descubierto/configurado no debe promocionarse a PASS sin read-back/health/evidence de ejecución cuando sea relevante.
- `COVERAGE_AND_GAPS` necesita un stop condition basado en suficiencia de evidencia y tratamiento de contradicciones. El éxito repetido de búsqueda no debe incrementar cobertura indefinidamente.
- `CONTEXT_COMPRESSION` debe conservar referencias, provenance y contradicciones no resueltas; una síntesis que borre estas relaciones no es un package verificable.

### UNKNOWN
- Número máximo de search/tool-discovery calls por request.
- Threshold cuantitativo de coverage sufficiency.
- Freshness TTL por clase de fuente.
- Compression ratio que conserva calidad downstream.
- Todos quedan pendientes de tests M07/M10; SOL no asignó números por intuición.

### Catálogo/gate
- No apareció componente/skill/dataset nuevo con evidencia suficiente para ampliar el catálogo.
- Índice permanece en **117** y sólo recibió anotación de la política de capability/coverage.
- `huggingface-datasets` permanece `INDEXED_CANDIDATE_NO_INSTALL`; no se instaló.

### Mutaciones
- Sólo control plane/documentación: PLAN rev8, STATE rev11, CHECKPOINT `CP-V2-M13-SIM03-EVIDENCE-009`, Handoff, índice y este SOL log.
- Cero adquisición, delete, move, overwrite de componentes, cambio source/ref o edición de motores canónicos.
- Balance preservado: B01–B04 = **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.

## Regla de continuidad
No reintentar B01–B04 a ciegas. SOL continúa únicamente con simulaciones/read-only evidence y monitor de reviews hasta que el gate correspondiente habilite una mutación física. No instalar `huggingface-datasets` Skill hasta review/gate aplicable.
