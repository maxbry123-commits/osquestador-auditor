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
- B04 context/HF/eval ya existe en `main`: **7 VERIFIED_CLOSED / 3 FAILED / 0 pending** según `B04-INDEX.md` y `B04-state.json`.
- B04 FAILED observados: `huggingface_hub`=`SOURCE_SPECIAL_FILE_GAP:CLAUDE.md`; `spaCy`=`DESTINATION_EXISTS`; `unstructured`=`SOURCE_SPECIAL_FILE_GAP`. No reintentar a ciegas.
- Total B01–B04: **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**. Esto no convierte Paso 2 en PASS global.

## M13 simulación read-only 01
Se recorrieron discovery → retrieval → evidence/contradiction → coverage/gaps → compression → context package con fuentes actuales y oficiales.

### FACT
- OpenAI Responses/Agents usan web search, file search, remote MCP, guardrails/tracing y sandbox/harness como primitivas para agentes y contexto: https://openai.com/index/new-tools-for-building-agents/ ; https://openai.com/index/new-tools-and-features-in-the-responses-api/ ; https://openai.com/index/the-next-evolution-of-the-agents-sdk/
- Anthropic recomienda tratar el contexto como recurso finito, recuperación just-in-time, referencias ligeras y sub-agentes con resúmenes destilados: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents ; https://www.anthropic.com/engineering/multi-agent-research-system
- OpenClaw advierte que allowlists de Skills no son frontera de autorización y recomienda sandbox/OS-user isolation y credenciales por agente: https://docs.openclaw.ai/tools/skills ; https://docs.openclaw.ai/skills-config
- Hermes dispone de cliente MCP nativo, auto-discovery y filtros por servidor: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md
- Hugging Face mantiene `huggingface_hub`, `datasets` y un MCP Server oficial; los tres ya estaban catalogados en B04. `hf-mcp-server` MIT; `huggingface_hub` y `datasets` Apache-2.0.

### INFERENCE
Sharck Input debe compilar un contexto mínimo de alta señal con `pointer + provenance + freshness + evidence class + deferred retrieval handle`, evitando cargar por adelantado repos/datasets/tools completos. El bridge HF debe quedar separado en tres adapters: Hub discovery/pointers, dataset load/stream, MCP tool exposure.

### UNKNOWN
Los umbrales cuantitativos de cobertura/compresión y la política exacta de deferred loading requieren tests M07/M10; no se fijan por intuición.

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
`CP-V2-M13-SIM01-B04-007`
`last_verified_node=M13_SIMULATION_01_AND_B04_CONTROL_PLANE_RECONCILE`
`resume_from=M06_M07_M08_REVIEW_AND_GAP_STRATEGY_WITH_M13_READ_ONLY_PARALLEL`.

## Próximo nodo permitido
SOL: siguiente simulación read-only por etapas y monitor de reviews. ASTRA/CLAUDE/GROK conservan M06/M07/M08. No reparación física B01–B04 ni Paso 3 hasta evidencia/review/gate correspondiente.
