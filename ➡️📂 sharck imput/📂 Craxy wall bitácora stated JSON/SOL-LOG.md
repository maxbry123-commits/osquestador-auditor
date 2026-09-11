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

## Regla de continuidad
No reintentar B01–B04 a ciegas. SOL continúa únicamente con simulaciones/read-only evidence y monitor de reviews hasta que el gate correspondiente habilite una mutación física.
