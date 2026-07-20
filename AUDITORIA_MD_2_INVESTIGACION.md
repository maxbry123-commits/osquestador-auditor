# AUDITORÍA 2/5 — INVESTIGACIÓN (32 fuentes + 4 Puntos comunidad devs)

**Fecha**: 2026-07-19 21:30
**Modo SHERIFF v8.2**: input-block-reader literal
**Trigger**: Max "audita lo que tengas sobre el osquestador... 5 Documentos máximo"

---

## 1. INVESTIGACIÓN FASE 0 — 32 NODOS CONSOLIDADOS

De `INVESTIGACION.md` (consolidado por sistema) y `INVESTIGACION_INTERFACES_SPEC.md`:

### 32 fuentes investigadas
- 0.1 OpenClaw (npm: `openclaw@2026.6.11`) — protocolo WS, contratos
- 0.2 LiteLLM (puerto 4000) — providers, fallbacks, OpenAI-compat
- 0.3 MCP (Model Context Protocol) — spec JSON-RPC 2.0
- 0.4 Haystack — retrievers, embedders, pipelines
- 0.5 Plandex — DAG de tasks
- 0.6 Hermes — formato README raíz
- 0.7 SWE-agent — auditoría código, frontier exploration
- 0.8 Repomix — output format
- 0.9 Kanboard — JSON-RPC API
- 0.10 Obsidian — markdown + Dataview
- 0.11 Graphiti — Neo4j schema
- 0.12 Telegram Bot API — getUpdates, sendMessage
- 0.13 Anthropic Console / Claude.ai Project UI
- 0.14 Cloudflare Pages — wrangler
- 0.15 Cloudflare Tunnel (cloudflared)
- 0.16 DuckDNS API
- 0.17 systemd — unit file, journalctl
- 0.18 SQLite WAL — journal_mode
- 0.19 Circuit Breaker (Hystrix, Polly, resilience4j)
- 0.20 JSON-RPC 2.0 spec
- 0.21 hot-reload Python (jurigged, reloadium, watchdog)
- 0.22 JSON-Agents, agent-registry, MOYA
- 0.23 patrones UI minimalista Anthropic/iOS
- 0.24 streaming (SSE, WebSocket, fetch streams)
- 0.25 persistencia memoria local en VPS
- 0.26 OCR (Tesseract, PaddleOCR, HF Spaces, Baidu)
- 0.27 vector stores (FAISS, Qdrant, Chroma)
- 0.28 memoria avanzada (episódica/semántica/procedimiento)
- 0.29 Neo4j + Graphiti
- 0.30 DAG runners (Airflow, Prefect, Dagster)
- 0.31 conectores MCP (filesystem, github, git, memory)
- 0.32 Seguridad (sandbox, capability-based, Linux)

---

## 2. INVESTIGACIÓN EXTENDIDA — 4 PUNTOS COMUNIDAD DEVS (50 búsquedas)

### PUNTO 1: Memoria extendida con raíz GitHub + DB por proyecto (15 búsquedas)
**Archivos**: `INVESTIGACION_COMUNIDAD_V2_PUNTO1.md` + `_APENDICE_SEARCH.md`
**APROBADO por Max 2026-07-18 01:19**

Decisiones de arquitectura finales:
- **Workspace**: `~/.osquestador/proyectos/<id>/` con vault/ db/ .env AGENTS.md .git/ (aislamiento total por proyecto)
- **Repo GitHub**: `osquestador-memoria` monorepo con `dirs/<project_id>/` (raíz de memoria permanente)
- **Storage**: SQLite FTS5 (BM25) + FAISS MiniLM-L6-v2 (384-dim) namespace por proyecto
- **Memory tiering**: HOT <500 tokens working / WARM 1-3K facts comprimidos / COLD repo GitHub summaries firmados
- **3 search engines**: local hybrid (BM25+FAISS+RRF) / web Tavily-Exa fallback / memoria histórica git
- **5 hooks nativos en kernel**: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop
- **Tools MCP**: `memoria_commit/log/diff/blame/checkout/branch/merge` + `osquestador_search_hybrid/keyword/vector/recent/tags` + `osquestador_collections_list`
- **Métricas éxito**: cold start <200ms, search local <500ms, recall >85% test, cross-project isolation verified
- **Stack**: SQLite FTS5 + FAISS + RRF + watchdog background + Haystack QueryExpander con M2.5

### PUNTO 2: Sistema de anclaje de skills en repo `memoria` con índice bibliotecario (10 búsquedas)
**Archivos**: `INVESTIGACION_COMUNIDAD_V2_PUNTO2.md` + `FASE_4_5_IDEA_SKILLS_MAX.md` + `HALLAZGOS_COMUNIDAD_DEVS.md` + `docs/fuente_max/*`
**APROBADO por Max 2026-07-18 01:42**

Decisiones de arquitectura finales:
- Repo `osquestador-memoria` con REGISTRY.yaml + indice/ + skills/<cat>/<id>/
- Skills Anthropic doble uso (.agents/skills/ estándar cross-client, 20+ tools compatibles)
- 90% código / 10% LLM (Compiled AI arxiv 2604.05150, SOURCE CODE AGENT 2508.02721)
- Multi-fuente: ClawHub + SkillsMP + OpenAgentSkill + GitHub + repo local Max
- Stack: SKILL.md + load-skill + agent-skills-cli + YAML + SQLite FTS5 + jsonschema
- 2 engines de Max validados: Acquisition + Distillation
- 10 patrones comunidad aplicados: Git-as-memory, Workspace-per-Tenant, HWC tiering, scratchpad, search on-connect, web search engines, hooks lifecycle, cold start, multi-marketplace skills, Compiled AI 90/10

### PUNTO 3: Osquestador handshake al agente (10 búsquedas) — `INVESTIGACION_COMUNIDAD_V2_PUNTO3.md`
**Formato pedido por Max**: "el documento o información lo manda o recibe y luego lo usa o lo modifica o lo guarda"

#### TEMA 1: PUSH/PING (notificaciones en tiempo real)
El Osquestador le manda avisos al chat/agente SIN que el usuario pida nada. Como WhatsApp "llegó mensaje". Implementación: SSE (Server-Sent Events) + WebSocket fallback. Patrones comunidad: Firebase Cloud Messaging, Pusher, Ably, OneSignal. Decisión: SSE primary, WebSocket para chat bidireccional.

#### TEMA 2: HISTORIAL DE CHAT (persistencia)
Guardar cada mensaje con: id, role (user/assistant/system), content, timestamp, project_id, agent_id, metadata (tokens, model, latency). Stack: SQLite warm.sqlite + búsqueda FTS5 + paginación cursor-based. Decisión: append-only, retención 90 días, exportable a JSONL.

#### TEMA 3: TAGS/ETIQUETAS (auto-generados)
Auto-tag con LLM 10% budget. Tags incluyen: categoría (decision/tech/process/idea), proyecto, agente, prioridad, status. Stack: tagger local con MiniLM zero-shot + LLM solo para tags complejos. Decisión: dual approach (local + LLM).

#### TEMA 4: INYECCIÓN DE INFORMACIÓN AL AGENTE
Cuando el agente arranca, se le inyecta contexto en 3 tiers: HOT (system prompt base, <500 tokens), WARM (resúmenes comprimidos, 1-3K), COLD (referencias con links, on-demand). Patrones: Anthropic context caching, MemGPT paging, LangChain Memory.

### PUNTO 4: Herramientas comunidad (Hermes, OpenClaw, Claude) + Ideas devs (12 búsquedas) — `INVESTIGACION_COMUNIDAD_V2_PUNTO4.md` + `V4_V2.md`
**APROBADO por Max**

#### HALLAZGOS POR HERRAMIENTA

**1. HERMES AGENT (Nous Research)**
- AIAgent como librería Python (no solo CLI)
- Async subagents nativos
- Code execution sandboxed
- Save trajectories JSONL para replay
- Skill format: `~/.hermes/skills/<nombre>/SKILL.md` + `load_skill()` runtime

**2. OPENCLAW**
- ClawHub marketplace de skills
- 5 channels built-in (chat, terminal, file, search, browser)
- "Mayordomo pattern" — un agente central despacha
- WS protocol en puerto 18789

**3. CLAUDE CODE oficial**
- SKILL.md spec (frontmatter YAML + body markdown)
- Progressive disclosure (3 niveles: name+description / full body / resources)
- 12 hooks lifecycle (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, etc)
- Subagents con Task tool + depth cap

**4. MEMORY PATTERNS (community)**
- Vault = filesystem con markdown + frontmatter + wikilinks `[[link]]`
- 5 CTX files: aboutme, now, Work, project, systems
- BM25 + vector hybrid con RRF (Reciprocal Rank Fusion)
- 90 días TTL WARM, prune-over-append

**5. SUB-AGENTS (Anthropic pattern)**
- Orchestrator-worker topology
- ACP (Agent Communication Protocol) primitives
- Depth cap = 5 para evitar recursion infinita
- A2A (Agent-to-Agent) protocol para inter-agente

**6. CHECKPOINT (Dapr-style)**
- SQLite-first, journal_mode=WAL
- Idempotency keys para reintentos seguros
- 4 primitives: save, load, list, delete
- Resume desde workflow_id + step_id

**7. TRIPLE BACKGROUND (Punto 4 v2)**
- nohup (rápido, no supervisionado)
- tmux (interactivo, persistente)
- systemd Type=notify + WatchdogSec=30s (producción)
- Decisión: usar los 3 según contexto

**8. WATCHDOG INTERNO**
- Script Python cada 30s que verifica health.json
- Si status != alive → kill + restart
- Exponential backoff para no flapping

**9. RESTIC + S3 BACKUP**
- Regla 3-2-1-1-0 (3 copias, 2 medios, 1 offsite, 1 inmutable, 0 errores)
- RPO 6h (cada 6h backup)
- Append-only WORM bucket para inmutabilidad

**10. SISTEMA DE TAGS AVANZADO**
- Auto-tag con MiniLM zero-shot NLI (zero inference cost)
- Tag complejo con LLM solo si confidence < 0.7
- Tag index en SQLite FTS5 para búsqueda
- Tag graph en Graphiti para relaciones

---

## 3. HALLAZGOS COMUNIDAD DEVS (resumen ejecutivo — `HALLAZGOS_COMUNIDAD_DEVS.md`)

### Top 10 patrones validados
1. **Kernel pequeño + plugins intercambiables** (Anthropic, Hermes, LangChain)
2. **MCP como estándar cross-client** (Anthropic 2026 announcement)
3. **Vault = filesystem** (Obsidian, Logseq, Notion API alternative)
4. **Memoria tripartita HOT/WARM/COLD** (MemGPT, Anthropic context caching)
5. **3 motores de búsqueda** (BM25 keyword + vector semantic + git historical)
6. **Sub-agents con depth cap** (Claude Code Task tool, Plandex)
7. **SQLite-first checkpoint** (Dapr, Temporal lite alternative)
8. **Triple background** (nohup + tmux + systemd)
9. **Watchdog interno Python** (patrón Linux + health check)
10. **Compiled AI 90/10** (código determinístico + LLM solo para lo no-determinístico)

### Top 5 librerías validadas
1. **LiteLLM** — multi-provider LLM unificado
2. **FAISS** (MiniLM-L6-v2 384-dim) — vector store liviano
3. **PaddleOCR v3.5+** — OCR 100+ idiomas
4. **Anthropic SDK oficial** — Claude API con prompt caching
5. **FastAPI** + **Uvicorn** — async web framework

### Top 5 librerías pendientes validar
1. **graphiti-core** (Python Neo4j alternativo)
2. **Haystack** pipelines (similitud más sofisticada)
3. **Plandex** (DAG task decomposition)
4. **Repomix** (empaquetado repos)
5. **SWE-agent** (auditoría código con frontier exploration)

---

## 4. INVESTIGACIÓN INTERFACES (`INVESTIGACION_INTERFACES_SPEC.md` + `_SOFTWARE.md`)

### Análisis de 6 interfaces de programas del spec
1. **Haystack** — pipeline UI, drag&drop components, retriever lab
2. **Graphiti** — graph explorer con cytoscape/d3
3. **Kanboard** — kanban con cards drag&drop, columnas configurables
4. **Plandex** — chat + plan + diff, 3 columnas
5. **Hermes** — terminal CLI + TUI dashboard
6. **Obsidian** — graph view + backlinks + file tree

### Patrones UI community validados
- **iOS HIG** (Apple Human Interface Guidelines 2026)
- **Anthropic Claude.ai** (cream + dark mode, serif headings, Inter body)
- **Material Design 3** (elevation, surface tones)
- **Fluent 2** (Microsoft, mica + acrylic effects)

### 7 funciones `window.osquestador` (spec de Max)
1. `osquestador.search(query, opts) → {hits: []}`
2. `osquestador.commit(message, files) → {sha: string}`
3. `osquestador.log(projectId, n) → {events: []}`
4. `osquestador.diff(sha1, sha2) → {patch: string}`
5. `osquestador.blame(file) → {authors: []}`
6. `osquestador.checkout(branch) → {ok: bool}`
7. `osquestador.branch(name) → {ok: bool}`

---

## 5. FOTOS DE INTERFACES (3 docs analizados)

- `FOTOS_5_POR_PROGRAMA.md` — 5 fotos por cada uno de 5 programas
- `FOTOS_INTERFACES_6_PROGRAMAS.md` — 6 programas analizados
- `FOTOS_REBUSQUEDA_3_PROGRAMAS.md` — re-búsqueda 3 programas extra

Total: 218 imágenes descargadas y analizadas para extraer patrones UI.
