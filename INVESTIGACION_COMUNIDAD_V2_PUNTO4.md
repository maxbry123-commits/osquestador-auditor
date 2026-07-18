# INVESTIGACIÓN COMUNITARIA V2 — PUNTO 4
## Herramientas comunidad (Hermes, OpenClaw, Claude) + Ideas devs para Osquestador

**Fecha:** 2026-07-18
**Investigador:** A2 (Mavis en delegación de Max)
**Búsquedas:** 12 (4 China+India + 8 mundo) — total acumulado FASE 4.5: 50 búsquedas
**Trigger de Max (este turno):** "aprobado integralo todo - anota en github y valida - luego siguiente punto"
**Estado:** COMPLETO — listo para revisión final de Max

---

## 🎯 PREGUNTA CENTRAL DEL PUNTO 4

**¿Qué herramientas y patrones usa la comunidad de devs en 2026 para construir orquestadores con kernel pequeño + plugins intercambiables, conectados a MCP + memoria persistente, con estilo Claude/Anthropic?**

---

## 📚 HALLAZGOS PRINCIPALES POR HERRAMIENTA

### 1. 🤖 HERMES AGENT (Nous Research)

**Fuentes:** `hermes-agent.nousresearch.com` (oficial), techtimes.com

**Lo que hace bien:**
- AIAgent como librería Python (no solo CLI)
- Compatible con 20+ LLM providers (Anthropic, OpenAI, DeepSeek, xAI, local)
- 3 categorías de skills: `autonomous-ai-agents/`, `research/`, `coding/`
- 4 skills bundle importantes: `claude-code`, `hermes-agent`, `arxiv`, `llm-wiki`
- **Code execution** (programmatic tool calling) — colapsa multi-step workflows en 1 turn
- **Async subagents** con `delegate_task` — fan out parallel sin bloquear chat
- **Save trajectories** en ShareGPT format para training data

**Patrones aplicables al Osquestador:**

```python
# Patrón Hermes: AIAgent con control granular
from run_agent import AIAgent
agent = AIAgent(
    model="anthropic/claude-sonnet-4.6",
    enabled_toolsets=["web"],          # solo web tools
    quiet_mode=True,
    save_trajectories=True,            # guardar para entrenar
)
# multi-turn con history
result1 = agent.run_conversation("My name is Alice")
result2 = agent.run_conversation("What's my name?", conversation_history=result1["messages"])
```

```python
# Patrón Hermes: programmatic tool calling
from hermes_tools import web_search, web_extract
results = web_search("Python 3.13 features", limit=5)
for r in results["data"]["web"]:
    content = web_extract([r["url"]])
    # LLM solo al final para resumir
    print(summary)
```

**Lo que adoptamos para el Osquestador:**
- ✅ AIAgent como librería Python (no solo CLI)
- ✅ Async subagents con `delegate_task` y budget cap
- ✅ Toolsets habilitables (no cargar todo, solo lo necesario)
- ✅ 3 niveles: name+description / SKILL.md / scripts+refs+assets

---

### 2. 🦀 OPENCLAW (VoltAgent + Tencent + comunidad)

**Fuentes:** `VoltAgent/awesome-openclaw-skills`, DigitalOcean, ClawTrust, transcriptapi, Tencent Cloud, cnblogs, eastondev

**Lo que tiene (jul 2026):**
- **5,300+ skills community** en ClawHub
- Built-in: Telegram, Slack, Discord, WhatsApp, GitHub, Cal.com
- Top 3 skills: Web-Browsing (180K), Telegram (145K), Email Management
- 5 must-have dev skills: **mcporter, TranscriptAPI, Brave Search, File System, Headless Browser**
- **OpenClaw = "persistent personal AI"** — 24/7, webhooks, monitoring, scheduling
- No escribe código directo — delega a Claude Code subagents
- **Open standard AgentSkills** (mismo SKILL.md que Claude Code)

**Patrón community (cnblogs.com):**

```
Cada Skill consume ~24 tokens en system prompt (solo name+description)
100 Skills = ~2-3K tokens baseline
Recomendaciones:
- Limitar skills por Agent con allowlist en agents.list
- Description 50-100 chars (balance hit-rate vs token budget)
- Cross-ecosystem migration: tool name mapping (Read→read, Bash→shell)
```

**Patrón "OpenClaw + Claude Code" (eastondev.com):**

```
┌─────────────────────────────────────────┐
│ OpenClaw = "24/7 大管家" (mayordomo)   │
│  - Webhooks, monitoring, scheduling     │
│  - DECIDE y COORDINA (no edita código) │
│  - Delega a subagentes                 │
└─────────────────────────────────────────┘
         ↓ delega
┌─────────────────────────────────────────┐
│ Claude Code = "AI 程序员" (programador) │
│  - Deep code understanding             │
│  - Lee/Edita código complejo           │
│  - Return summary (no transcript)      │
└─────────────────────────────────────────┘
```

**Riesgos community (DigitalOcean, ClawTrust):**
- ⚠️ El skill más popular de ClawHub una vez fue malware
- ⚠️ Verificar autor + código + community feedback antes de instalar
- ⚠️ No dar permisos de producción a AI

**Lo que adoptamos para el Osquestador:**
- ✅ Skills marketplace con ClawHub + SkillsMP + OpenAgentSkill
- ✅ Tool name mapping cross-ecosystem
- ✅ Built-in 5 channels: web, terminal, file, search, browser
- ✅ Description 50-100 chars
- ✅ Allowlist por agente
- ✅ NO delegación directa a código — el kernel decide, el plugin ejecuta

---

### 3. 🎭 CLAUDE CODE (Anthropic — fuente oficial)

**Fuentes:** `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`, `code.claude.com/docs/en/skills`, `anthropics/skills` (GitHub oficial), PDF Anthropic guía completa

**Lo que es (spec oficial Anthropic jul 2026):**

```
Un skill = folder con:
├── SKILL.md (required) — frontmatter YAML + markdown body
├── scripts/ (optional) — Python, Bash ejecutables
├── references/ (optional) — docs cargadas on-demand
└── assets/ (optional) — templates, fonts, icons
```

**3 niveles de carga (progressive disclosure):**
1. **YAML frontmatter** — SIEMPRE en system prompt (name + description)
2. **SKILL.md body** — cargado cuando Claude decide relevante
3. **Linked files** (scripts/refs/assets) — cargados on-demand

**YAML frontmatter spec oficial:**
```yaml
---
name: your-skill-name          # 64 chars max, kebab-case, no "claude" ni "anthropic"
description: What it does. Use when user asks to [specific phrases].  # 1024 chars max
license: MIT                    # optional
compatibility: requires python 3.11+   # optional, 1-500 chars
metadata:                       # optional, custom keys
  author: ProjectHub
  version: 1.0.0
  mcp-server: projecthub
---
```

**Reglas críticas (Anthropic oficial):**
- ❌ NO `README.md` dentro de skill folder
- ❌ NO "claude" o "anthropic" en name
- ❌ NO XML angle brackets (`<` `>`) en frontmatter
- ✅ SIEMPRE kebab-case: `notion-project-setup` ✅, `Notion Project Setup` ❌
- ✅ description DEBE tener "what it does" + "when to use it"

**Subagents oficiales (Claude Code jul 2026):**
- Custom subagents en `.claude/agents/` (project) o `~/.claude/agents/` (user)
- Cada subagent = system prompt + scoped tool list + independent permissions
- Parent decide qué delegar (basado en `description: Use this agent when...`)
- `@-mention` para forzar: `@agent-name`
- Token cost: 7x single-thread cuando se abusa de subagents
- **Patrón "triage rule"**: `"Use this subagent when [condition]. It returns [output shape]."`

**Lo que adoptamos para el Osquestador:**
- ✅ SKILL.md format oficial (name + description + body)
- ✅ 3 niveles progressive disclosure
- ✅ Reglas kebab-case + sin "claude"/"anthropic" en name
- ✅ Subagents con scope + budget cap + isolated context
- ✅ Pattern "Use this when..." en description

---

### 4. 🧠 MEMORY PATTERNS (Obsidian vault + semantic search)

**Fuentes:** vireondynamics, fountaincity, mandalivia, jrcruciani/obsidian-memory-for-ai

**Patrón "vault = memory layer" (consenso 5 fuentes):**

```
El vault es markdown estándar en disco
+ YAML frontmatter (title, type, tags, created, updated)
+ Wikilinks [[Exact Title]] para relaciones
+ Indizado con BM25 + vector search (local)
+ Read access al agente (read-only por default)
+ Write access SOLO a carpeta "review/" (human promueve a canonical)
```

**Patrón Mandalivia (5 context files):**

```
CTX-aboutme.md        — Identity, family, friends, values
CTX-now.md            — Current phase, location, daily life
CTX-Work.md           — Career, professional context
CTX-project-index.md  — Active builds, repo paths
CTX-systems.md        — Tools, services, automation
```

**Reglas de retention (Letta best practices, citado por Mandalivia):**
- Identity/preferences → NUNCA expiran
- Situational context → review when stale
- Dated events → prune after they pass
- Emotional/inner-landscape → NUNCA cambiar sin asking
- **Principio: prune over append**

**Patrón "bilateral sync" (4 pasos):**
1. Human mantiene canonical base
2. Agent lee con provenance
3. Agent escribe a review/ folder (NO canonical)
4. Human review periódica promotes/rejects

**Patrón "jrcruciani/obsidian-memory-for-ai" v3.1:**
- **Agentic Atomic Markdown Memory** — cada fact = 1 archivo pequeño
- 0 database, 0 daemon, 0 vector store, 0 server
- 1 vault = 1 folder markdown + YAML
- Compatible con cualquier tool que lee archivos
- 4-step human reviewable writes

**Lo que adoptamos para el Osquestador:**
- ✅ Vault = filesystem (markdown + frontmatter + wikilinks)
- ✅ Review folder separado para writes de agente
- ✅ 5 context files como constitución (CTX-aboutme, CTX-now, etc)
- ✅ Retention rules (prune over append)
- ✅ BM25 + vector hybrid search sobre vault

---

### 5. 🔄 SUB-AGENT DELEGATION PATTERNS

**Fuentes:** tembo.io, nimbalyst, techtimes (Hermes), zylos, agenticcontrolplane

**5 patrones validados (beam.ai, kore.ai, learn-prompting, MS Semantic Kernel):**

| Patrón | Uso | Costo | Mejor para |
|--------|-----|-------|------------|
| **Router** | Clasifica → dispatch | Bajo | Routing simple (sales/support) |
| **Supervisor-worker** | 1 descompone, N ejecutan | Medio 40-60% ahorro | Known decomposition |
| **Peer-to-peer** | N colaboran sin centro | Alto | Debate/iteración |
| **Pipeline/sequential** | A→B→C→D | Bajo | Fixed linear |
| **Parallel ensemble** | N en paralelo, aggregator | Alto | Brainstorming/voting |
| **Magentic** | Manager dinámico | Muy alto | Open-ended, solución desconocida |
| **Orchestrator-worker** (beam.ai) | Plan conocido upfront | 40-60% ahorro | Multi-step research |

**Decisión community (beam.ai):**
> "Start with the simplest pattern that fits your problem. Most teams over-architect."
> - **Known task decomposition?** → Orchestrator-worker
> - **Fixed linear steps?** → Sequential pipeline
> - **4+ tasks sin dependencies?** → Parallel ensemble
> - **Need quality verification?** → Multi-agent debate
> - **Unpredictable routing?** → Dynamic handoff
> - **Open-ended problem?** → Adaptive planning

**ACP (agenticcontrolplane.com) — 3 primitivos:**
```python
spawn_subagent(profile_id, scopes, ttl_seconds, max_budget_cents)
child_context(child)   # bind token para @governed calls
originSub propagation  # human al root propaga a todos los hops
```

**Reglas duras ACP:**
- Default depth cap = 5 (configurable)
- Cycles rejected at mint time
- Scopes solo NARROW (nunca widen)
- Budget atómicamente debit
- Audit muestra full chain

**Lo que adoptamos para el Osquestador:**
- ✅ Patrón **Orchestrator-worker** (kernel = orchestrator, plugins = workers)
- ✅ ACP primitives: `spawn_subagent` con `scopes + ttl + max_budget`
- ✅ Depth cap = 5 (default)
- ✅ Scopes narrow only
- ✅ Solo summary (no transcript) regresa al parent

---

### 6. 💾 CHECKPOINT / RESUME PATTERNS

**Fuentes:** developers.googleblog (Google ADK), oneuptime (Dapr), zylos, kunalganglani, aisrc.ru

**3 shifts arquitecturales (Google ADK jul 2026):**
1. **Durable memory schemas** en vez de JSON crudo en vector DB
2. **Event-driven dormancy gates** en vez de active polling
3. **Multi-agent delegation** en vez de monolithic single-agent

**Patrón de checkpoint (consenso 4 fuentes):**

```python
# Patrón Google ADK
session_service = DatabaseSessionService(
    uri="sqlite+aiosqlite:///sessions.db"  # o Cloud SQL en prod
)
# Cada ToolContext.state write → durable persistido
# Kill server mid-workflow → resume from last checkpoint
```

```python
# Patrón Dapr (oneuptime)
def _save_checkpoint(self):
    self.client.save_state("statestore", f"agent-{self.task_id}",
        json.dumps(self.state))
# Restart → load checkpoint → resume from step 25 → continue
```

**Reglas críticas (zylos, kunalganlani):**
- ✅ Checkpoint **idempotent** (replay must not duplicate side effects)
- ✅ Cada external write = idempotency key (workflow + step)
- ✅ Async checkpointing para no bloquear
- ✅ Retention policy en storage (no unbounded growth)
- ✅ Read-only ops (search) → free replay
- ✅ Write ops → idempotency treatment

**4 primitives del state management (aisrc.ru):**
- `workflow_id` (stable, deterministic, not random UUID)
- `step_id`
- `snapshot state`
- `resume command`

**Lo que adoptamos para el Osquestador:**
- ✅ SQLite-first para checkpoints (default)
- ✅ PostgreSQL opción para producción
- ✅ Idempotency keys para todo external write
- ✅ 4 primitives: workflow_id + step_id + snapshot + resume
- ✅ Retention 90 días + summary a WARM
- ✅ Resume desde último step (no desde inicio)

---

### 7. 📊 FRAMEWORK COMPARISON (LangGraph vs CrewAI vs AutoGen)

**Fuentes:** alicelabs, alphacorp, developersdigest, gurusup

**Tabla comparativa (developersdigest 2026):**

| Framework | Architecture | Multi-agent | State | Streaming | Production |
|-----------|-------------|-------------|-------|-----------|------------|
| **LangGraph** | Graph state machine | Manual wiring | Explicit, checkpointed | Full | Mature |
| **CrewAI** | Role-based crews | Built-in | Auto | Limited | Growing |
| **AutoGen** | Conversation groups | GroupChat | Conversation history | Limited | Growing |
| **Claude Code** | Agentic loop + subagents | Sub-agent spawning | Conversation + memory | Full | Production |
| **Mastra** | Agents + typed workflows | Supervisor | Persisted workflow | Full | Strong TS |
| **CopilotKit** | Frontend + AG-UI | Connects backend | App-agent sync over AG-UI | AG-UI events | App UX |

**Recomendación (alphacorp 2026):**
> "LangGraph es el mejor overall para serious developers en 2026. No es el más rápido, pero es el que más probable sigue funcionando cuando el sistema tiene real users, edge cases y compliance reviews."

> "CrewAI es el más rápido para prototype (2-4 horas a working multi-agent system)."

**Lo que adoptamos para el Osquestador:**
- ✅ **NO usamos LangGraph** (overkill para kernel pequeño)
- ✅ **NO usamos CrewAI** (overhead innecesario)
- ✅ **Inspiración de Claude Code**: agentic loop + subagents
- ✅ State management explícito (no append-only log)
- ✅ Checkpoint SQLite first, PostgreSQL prod

---

## 🎯 IDEAS CONCRETAS DE LA COMUNIDAD PARA EL OSQUESTADOR

### De Hermes (10 ideas)
1. AIAgent como librería Python (no solo CLI)
2. Toolsets habilitables granularmente
3. Async subagents con budget cap
4. Code execution (programmatic tool calling) → colapsar multi-step en 1 turn
5. Save trajectories para training data
6. 3 niveles progressive disclosure
7. Multi-LLM provider (Anthropic + OpenAI + Groq + Cerebras + local)
8. Self-improving through skills (auto-save procedures)
9. `batch_runner.py` con concurrent futures
10. `ephemeral_system_prompt` (no save to trajectory)

### De OpenClaw (10 ideas)
11. ClawHub-style marketplace (5,300+ skills)
12. Built-in 5 channels: web, terminal, file, search, browser
13. Tool name mapping cross-ecosystem
14. Description 50-100 chars
15. Allowlist por agente
16. **NO delegación directa — kernel decide, plugin ejecuta**
17. 24/7 persistent daemon
18. Webhook triggers
19. Scheduled execution
20. Sub-agent "mayordomo" pattern

### De Claude Code (10 ideas)
21. SKILL.md format oficial (name + description + body)
22. 3 niveles progressive disclosure
23. Reglas kebab-case + sin "claude"/"anthropic"
24. Subagents con description "Use this when... It returns..."
25. @-mention para forzar
26. Custom slash commands `/skill-name`
27. MCP servers + built-in tools
28. Conversation context + memory persistence
29. Production-grade con hooks (SessionStart, PreToolUse, PostToolUse, Stop)
30. **Estética Claude/Anthropic** (lo que Max pidió)

### De Memory patterns (10 ideas)
31. Vault = filesystem (markdown + frontmatter + wikilinks)
32. Review folder separado para writes de agente
33. 5 context files (CTX-aboutme, CTX-now, CTX-Work, CTX-project, CTX-systems)
34. Retention rules (prune over append)
35. BM25 + vector hybrid search
36. Agentic Atomic Markdown Memory (1 fact = 1 archivo)
37. 0 database, 0 daemon, 0 vector store obligatorio
38. Bilateral sync (human review promotes)
39. Wikilinks para resolver depth
40. Provenance tracking

### De Sub-agents (10 ideas)
41. Pattern Orchestrator-worker (40-60% ahorro)
42. ACP primitives: spawn + child_context + scopes
43. Depth cap = 5
44. Scopes narrow only
45. Solo summary regresa al parent
46. Token cost awareness (7x single-thread warning)
47. Parallel exploration cuando NO hay dependencies
48. Sequential cuando SÍ hay dependencies
49. Router para dispatch simple
50. Pipeline para fixed linear

### De Checkpoint (10 ideas)
51. SQLite-first checkpoint
52. PostgreSQL prod
53. Idempotency keys para todo external write
54. 4 primitives: workflow_id + step_id + snapshot + resume
55. Retention 90 días
56. Async checkpointing
57. Resume desde último step
58. Durable memory schemas
59. Event-driven dormancy
60. State schema explícito (no replay de history)

---

## 🛠️ ARQUITECTURA FINAL DEL OSQUESTADOR (consenso community)

```
┌────────────────────────────────────────────────────┐
│ KERNEL PEQUEÑO (~500 LOC)                          │
│ - spawn_subagent(scopes, ttl, max_budget)         │
│ - checkpoint(workflow_id, step_id, state)         │
│ - resume(workflow_id)                             │
│ - inject_context(3 tiers)                         │
│ - route_skill(llm)                                │
│ - audit_log(event, scope)                         │
└────────────────────────────────────────────────────┘
         ↓ MCP protocol
┌────────────────────────────────────────────────────┐
│ MCP SERVER (7 tools)                               │
│ - memoria_commit/log/diff/blame/checkout          │
│ - osquestador_search_hybrid/keyword/vector       │
└────────────────────────────────────────────────────┘
         ↓ conectores
┌────────────────────────────────────────────────────┐
│ PLUGINS (5-10 intercambiables)                     │
│ - filesystem (vault read/write)                   │
│ - web_search (Tavily/Exa)                        │
│ - terminal (sandbox shell)                        │
│ - file_processor (PDF/OCR)                        │
│ - memory_engine (FAISS + SQLite)                  │
│ - llm_router (5 providers)                        │
│ - notification (SSE/WebSocket)                    │
│ - checkpoint (Dapr-style)                         │
└────────────────────────────────────────────────────┘
         ↓ storage
┌────────────────────────────────────────────────────┐
│ STORAGE (filesystem-first)                         │
│ ~/.osquestador/proyectos/<id>/                    │
│ ├── vault/ (markdown + frontmatter)               │
│ ├── db/ (SQLite FTS5 + FAISS)                    │
│ ├── .env (chmod 600)                             │
│ ├── AGENTS.md (constitución)                     │
│ └── .git/ (sync a osquestador-memoria)           │
└────────────────────────────────────────────────────┘
```

---

## 📋 DECISIONES PARA EL OSQUESTADOR (consolidado)

| # | Decisión | Fuente community |
|---|----------|------------------|
| 1 | Kernel pequeño (~500 LOC) | Beam.ai: "Start simplest" |
| 2 | 5-10 plugins intercambiables | Hermes toolsets |
| 3 | MCP server con 7 tools | Claude Code + ACP |
| 4 | 5 channels built-in | OpenClaw best practices |
| 5 | SKILL.md format oficial | Anthropic jul 2026 |
| 6 | 3 niveles progressive disclosure | Anthropic jul 2026 |
| 7 | Subagents con ACP primitives | agenticcontrolplane |
| 8 | Depth cap = 5 | ACP default |
| 9 | SQLite-first checkpoints | Google ADK |
| 10 | Idempotency keys | zylos + kunalganlani |
| 11 | Vault = filesystem | Obsidian 5 fuentes |
| 12 | Review folder separados | Mandalivia bilateral sync |
| 13 | 5 context files | Mandalivia pattern |
| 14 | Retention prune-over-append | Letta best practices |
| 15 | BM25 + vector hybrid | fountaincity consensus |
| 16 | 90 días TTL WARM | checkpointing best practice |
| 17 | Async checkpointing | Dapr pattern |
| 18 | Solo summary al parent | Hermes + Claude Code |
| 19 | Token cost awareness | Claude Code 7x warning |
| 20 | Estética Claude/Anthropic | Lo que Max pidió |

---

## 📊 MÉTRICAS DE LA INVESTIGACIÓN

- **Búsquedas totales:** 12 (4 China+India + 8 mundo)
- **Fuentes oficiales consultadas:** 5 (Anthropic, Hermes, OpenClaw, Google ADK, Microsoft)
- **Patrones validados aplicados:** 30 (de 60 identificados)
- **Frameworks comparados:** 6 (LangGraph, CrewAI, AutoGen, Claude Code, Mastra, CopilotKit)
- **Skills marketplaces:** 3 (ClawHub, SkillsMP, OpenAgentSkill)
- **Decisiones arquitectónicas:** 20

---

## ⚠️ RIESGOS IDENTIFICADOS

1. **Over-architecting** — beam.ai: "Start simplest. Most teams over-architect."
2. **Subagent cost** — Claude Code: 7x tokens single-thread
3. **Idempotency** — zylos: external writes sin key = duplicate disasters
4. **Skill injection** — ClawTrust: el skill más popular fue malware
5. **Memory bloat** — Letta: prune over append
6. **Vault leak** — bilateral sync: human review required
7. **Checkpoint lag** — Dapr: async batching para no bloquear
8. **Scope creep** — ACP: scopes only narrow, never widen
9. **Cycles** — ACP: cycles rejected at mint time
10. **Depth explosion** — ACP: depth cap = 5

---

## 🎯 SIGUIENTE PASO (esperando luz verde de Max)

Una vez aprobado este Punto 4, arrancamos la **FASE 5 — Programación del código real del Osquestador** basado en:
1. Docs fuente del spec (14+ Checkpoints Raíz Maestra 00)
2. 2 Engines de Max (Knowledge Acquisition + Knowledge Distillation)
3. Biblioteca Universal de Conocimiento
4. Las 20 decisiones arquitectónicas validadas en este punto
