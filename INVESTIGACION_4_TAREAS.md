# INVESTIGACIÓN 4 TAREAS — Max trigger 2026-07-18 04:54
## 1) Kanban dashboard AI+agentes · 2) Obsidian · 3) Graphiti · 4) 10 mejores arneses AI
**Búsquedas:** 8 (4+4)

---

## TAREA 1 — Kanban dashboard con AI y agentes de programación

### 5 sistemas encontrados en GitHub:

| # | Repo | Stars | Función |
|---|------|-------|---------|
| 1 | **DanWahlin/ai-agent-board** | activo | Drag&drop Kanban que delega a Copilot/Claude Code/Codex/OpenCode con streaming en vivo |
| 2 | **Justmalhar/AgentsBoard** | activo | JIRA/Trello-style para AI agents, ejecutar task con model + token length |
| 3 | **saltbo/agent-kanban** | activo | Agent-first: cryptographic identity + role + skills; agents crean tasks y se auto-organizan |
| 4 | **TuckerTucker/TaskBoardAI** | activo | File-based kanban + web HIL collaboration + Claude |
| 5 | **GreenSheep01201/Claw-Kanban** | activo | 6 agentes (Claude Code, Codex CLI, Gemini CLI, OpenCode, Copilot, Antigravity) con role-based auto-assign + Telegram dispatch |

### Qué funciones mejorarían nuestro Osquestador:
- ✅ **Task Groups** (batch de tasks en 1 form) de ai-agent-board
- ✅ **Agent cryptographic identity + skills loadable** de agent-kanban
- ✅ **Telegram dispatch `# fix bug`** de Claw-Kanban
- ✅ **Streaming live progress** en el panel
- ✅ **HIL (Human-in-the-Loop) web interface** de TaskBoardAI
- ✅ **Role-based auto-assignment** de Claw-Kanban

---

## TAREA 2 — Obsidian (plugins AI + funciones avanzadas)

### 5 plugins AI oficiales:

| # | Plugin | Función |
|---|--------|---------|
| 1 | **Obsilo Agent** (pssah4) | AI que aprende vault + rules + workflows, 40 tools, semantic search, persistent memory, continuous learning, plugins as skills, full safety controls |
| 2 | **AI Agents** | Vault como ecosystem de AI agents definidos por markdown files (YAML frontmatter con prompt/tools/memory) |
| 3 | **Intelligence Assistant** (qwai-tech) | SPAR loop (Sense-Plan-Act-Reflect) autonomous, streaming chat, multi-provider (OpenAI/Anthropic/Google/DeepSeek), RAG, CLI+MCP agents |
| 4 | **Copilot for Obsidian** | Chat vault search, web/YouTube parsing, Agent Mode Plus con tool calling, OpenRouter recomendado |
| 5 | **Agent Fleet** | Claude Code o OpenAI Codex CLI, agents como markdown folders, schedule tasks, Slack/Telegram/Discord, MCP hooks |

### Plugins complementarios críticos:
- **Frontmatter Operator** — bulk edit YAML + AI generator con 12 providers + 11 languages
- **OpenAgent** — BYOK + cross-platform desktop+mobile + vault tools
- **MCP for Obsidian** — `obsidian_search_notes`, `obsidian_read_notes`, `obsidian_list_tags`, `obsidian_backlinks`, `obsidian_get_frontmatter`, `obsidian_search_content`, `obsidian_query`

### Qué funciones mejorarían nuestro Osquestador:
- ✅ **Agents como markdown files** (AI Agents plugin) — pattern replicable
- ✅ **SPAR loop** (Sense-Plan-Act-Reflect) — para nuestros agentes
- ✅ **MCP for Obsidian** con 7 tools — mismos tools en nuestro Osquestador
- ✅ **Plugins as skills** (Obsilo) — nuestro `~/.osquestador/skills/`
- ✅ **Frontmatter Operator** AI generation con 12 providers
- ✅ **Agent Fleet** markdown folders + cron + Slack/Telegram/Discord
- ✅ **Continuous learning** pattern de Obsilo

---

## TAREA 3 — Graphiti (getzep) funciones avanzadas

### Funciones NO anotadas antes:

| Función | Detalle | Integración Osquestador |
|---------|---------|------------------------|
| `EpisodeType.message` con `extract_message` prompt | Multi-turn conversation processing | Chat inputs del Osquestador |
| `EpisodeType.json` con `extract_json` prompt | Structured data processing distinto | API responses, metadata |
| `previous_episode_uuids` | Context control manual | Link InputBlock con episodio previo |
| `update_communities` flag | Community graph updates | Community detection post-ingest |
| `entity_types` dict | User-defined ontology | Custom entity types del Osquestador |
| `edge_type_map` | Type constraints en edges | Schema validation |
| `excluded_entity_types` list | Skip entities específicas | Filter de private data |
| `clear_graph` + rebuild | Reset completo + reindex | Reset manual del Osquestador |
| `get_status` MCP tool | Health check del server | `/healthz` endpoint |
| `add_episode_bulk` SIN edge invalidation | Fast bulk populate | Migración inicial |
| `entity_subset` param | Limitar extracción a subset | Performance optimization |
| `uuid` opcional | Custom episode UUID | Deterministic replay |

### MCP tools oficiales (10):
- `add_memory` (alias add_episode)
- `get_episodes` (group_ids, max_episodes)
- `search_nodes`
- `search_facts`
- `delete_episode`
- `delete_entity_edge`
- `get_entity_edge`
- `clear_graph`
- `get_status`
- `add_episode_bulk`

### Qué funciones mejorarían nuestro Osquestador:
- ✅ **`get_status` MCP tool** — health check del grafo
- ✅ **`previous_episode_uuids`** — context linking
- ✅ **`entity_types` custom** — ontology del Osquestador (decision, tech, etc)
- ✅ **`add_episode_bulk`** — migración inicial
- ✅ **Custom `uuid`** — deterministic replay del InputBlock

---

## TAREA 4 — 10 mejores arneses (frameworks) AI para agentes

### Top 10 frameworks 2026:

| # | Framework | Stars | Tipo | Mejor para |
|---|-----------|-------|------|-----------|
| 1 | **LangGraph 1.0** (LangChain) | 27.1k/月 | Directed graph + typed state | Producción stateful con branching/HITL |
| 2 | **Claude Agent SDK** (Anthropic) | activo | Tool-use chain + sub-agents | Producción Anthropic-native con hooks/MCP/skills |
| 3 | **CrewAI 1.14** | 49.2k | Role-based crews | Multi-agent prototypes rápido |
| 4 | **OpenAI Agents SDK** | activo | Handoffs + guardrails | Producción OpenAI-native con sandbox |
| 5 | **AutoGen/AG2** (Microsoft) | activo | Conversational GroupChat | Research/iteración abierta |
| 6 | **Pydantic AI** | 16.8k | Type-safe FastAPI-style | Producción con type safety |
| 7 | **Google ADK** (Agent Dev Kit) | activo | Hierarchical agent tree | Gemini-optimized + multi-cloud |
| 8 | **Semantic Kernel** (Microsoft) | activo | Enterprise .NET + Python | M365/Azure stack |
| 9 | **LlamaIndex** | activo | Data framework | RAG + data agents |
| 10 | **Mastra** | activo | TypeScript-native | TS apps con agents + workflows |

### Otros 6 a considerar (mencionados en comparativa):
- CopilotKit (in-app agent UX con React)
- Agno (fast lightweight agents)
- LangFlow (no-code)
- SmolAgents (HuggingFace)
- Letta (memory-first)
- Atomic Agents

### Comparativa clave:
- **Determinism:** LangGraph=High · Claude SDK=Low-Med · CrewAI=Low-Med · OpenAI=Low
- **State persistence:** LangGraph=built-in checkpoints · Claude SDK=vía MCP · OpenAI=context variables
- **Model dependency:** LangGraph/CrewAI/AutoGen=agnostic · OpenAI SDK=OpenAI only · Claude SDK=Claude only
- **Production readiness:** LangGraph=High · Claude SDK=High · CrewAI=Medium

### Qué arneses vamos a incorporar al Osquestador:

✅ **PRIORIDAD ALTA — incorporar:**
1. **Haystack 2.31** (ya en spec) — pipelines + SuperComponent + PipelineTool
2. **Hermes** (ya en spec) — agent loop + /undo + skills
3. **Pydantic AI** — type-safety para nuestros tools MCP + state schemas
4. **Claude Agent SDK** — hooks (5 nativos ya planeados) + MCP + sub-agents
5. **OpenAI Agents SDK** — guardrails para validar InputBlock antes/después

🟡 **PRIORIDAD MEDIA — considerar:**
6. **LangGraph 1.0** — para stateful workflows con branching si el Osquestador lo necesita
7. **CrewAI** — para role-based multi-agent (researcher/writer/auditor pattern)
8. **Google ADK** — si usamos Gemini
9. **LlamaIndex** — para RAG avanzado

🔴 **BAJA PRIORIDAD — observar:**
10. **AutoGen/AG2** — investigación abierta (no encaja con nuestros needs)
11. **Semantic Kernel** — solo si Max decide usar .NET
12. **Mastra** — TypeScript, no es nuestro stack

### Funciones que mejorarían el Osquestador por framework:

**De Pydantic AI (NUEVO - incorporar):**
- ✅ `RunContext[Dependencies]` para dependency injection
- ✅ Type-safe `Agent` class con `@agent.tool`
- ✅ Pydantic Logfire integration para observability
- ✅ Graph API con type hints (typed state machines)
- ✅ Durable execution con Temporal
- ✅ 16,800 stars + 241 releases + Amazon Bedrock AgentCore integration

**De Claude Agent SDK (ya parcialmente):**
- ✅ Sub-agents pattern (5 hooks nativos)
- ✅ MCP server tool calling nativo
- ✅ Skills system (ya planeado)
- ✅ Human-in-the-loop tool approval

**De OpenAI Agents SDK (NUEVO - incorporar guardrails):**
- ✅ Input guardrails (validar InputBlock antes de ejecutar)
- ✅ Output guardrails (validar output contra schema)
- ✅ Tool guardrails (pre/post cada tool call)
- ✅ Handoffs (delegar entre agents)
- ✅ Parallel execution vs blocking
- ✅ Sessions (memory layer persistente)
- ✅ Sandbox agents (manifest-defined files + resumable)

**De LangGraph 1.0 (considerar):**
- ✅ Per-node timeouts
- ✅ Node-level error handlers
- ✅ DeltaChannel (corta checkpoint overhead)
- ✅ v2 typed streaming API
- ✅ Time travel debugging
- ✅ Checkpointing con state machines

**De CrewAI 1.14 (considerar):**
- ✅ Pluggable default backends para memory/knowledge/RAG
- ✅ Chat API para conversational flows
- ✅ Snowflake Cortex LLM provider
- ✅ Scoped runtime state (aislar concurrent runs)

---

## ESTADÍSTICAS TOTALES FASE 4.5 ACTUALIZADAS

- **~158 búsquedas** comunidad devs
- **101 features** input-block integrados
- **70 ideas** + **26 decisiones** (D1-D26)
- **13 programas** del spec
- **30 pasadas** × 10 interfaces
- **218 imágenes** descargadas
- **5 sistemas Kanban AI** encontrados
- **5 plugins Obsidian AI** analizados
- **12 features nuevas Graphiti** detectadas
- **10 frameworks AI** rankeados
- **4 frameworks a incorporar** (Pydantic AI, Claude SDK, OpenAI SDK, LangGraph)

## DECISIONES NUEVAS PROPUESTAS

### D27 — Incorporar Pydantic AI como type-safety layer
- Type-safe tools + state schemas
- RunContext[Dependencies] para DI
- Logfire para observability
- Migración gradual desde dataclasses

### D28 — Incorporar OpenAI Agents SDK para guardrails
- Input guardrails = validar InputBlock antes de enviar al LLM
- Output guardrails = validar output contra schema strict
- Tool guardrails = pre/post cada tool del Osquestador
- Handoffs = delegar entre agents (researcher → writer → auditor)

### D29 — Adoptar pattern de Claw-Kanban
- 6 agentes simultáneos con role-based auto-assign
- Telegram dispatch `# fix bug` → crea task automática
- Streaming live progress en panel
- 6-column kanban board

### D30 — Adoptar pattern de Agent Fleet
- Agents como markdown folders
- Cron + heartbeat schedules
- Slack/Telegram/Discord hooks
- MCP hooks para tools externas

### D31 — Adoptar SPAR loop (Intelligence Assistant)
- Sense → Plan → Act → Reflect
- Loop persistente con state machine
- Reflection aprende de errores

### D32 — Adoptar Obsilo continuous learning
- Plugin skills auto-creados
- Continuous learning del vault
- 40 tools listos para usar
