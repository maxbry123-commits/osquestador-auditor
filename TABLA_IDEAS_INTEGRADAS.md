# TABLA DE 60 IDEAS INTEGRADAS — FASE 4.5 Punto 4
## Aprobado por Max 2026-07-18 02:10

**Trigger literal de Max:** "aprobado integra las 60 ideas y 20 decisiones aprobado todo"
**Confirmación:** ✅ ANOTADO en GitHub (commit por pushear al final)
**Origen:** Investigación comunitaria Punto 4 (12 búsquedas, 7 herramientas)

---

## 🤖 10 IDEAS DE HERMES (Nous Research)

| # | Idea | Cómo se integra al Osquestador |
|---|------|-------------------------------|
| 1 | AIAgent como librería Python | `kernel/orchestrator.py` importable, no solo CLI |
| 2 | Toolsets habilitables granularmente | `osquestador.enable_tools(["web","search"])` en config |
| 3 | Async subagents con budget cap | `spawn_subagent(scopes, ttl, max_budget)` |
| 4 | Code execution (programmatic tool calling) | Plugin `code_exec` que colapsa multi-step en 1 turn |
| 5 | Save trajectories para training data | `~/.osquestador/trajectories/<session>.jsonl` ShareGPT |
| 6 | 3 niveles progressive disclosure | Tier 1: name+desc / Tier 2: SKILL.md / Tier 3: scripts+refs |
| 7 | Multi-LLM provider | Router con 5 keys: Anthropic, OpenAI, Groq, Cerebras, NVidia |
| 8 | Self-improving through skills | Auto-crea SKILL.md cuando resuelve problema complejo |
| 9 | `batch_runner.py` con concurrent futures | Plugin `batch` con ThreadPoolExecutor |
| 10 | `ephemeral_system_prompt` (no save) | Flag `ephemeral=True` para prompts que no se persisten |

---

## 🦀 10 IDEAS DE OPENCLAW (VoltAgent + Tencent + comunidad)

| # | Idea | Cómo se integra al Osquestador |
|---|------|-------------------------------|
| 11 | ClawHub-style marketplace (5,300+ skills) | `osquestador_skills add <slug>` desde ClawHub + SkillsMP + OpenAgentSkill |
| 12 | Built-in 5 channels | Plugins core: web, terminal, file, search, browser |
| 13 | Tool name mapping cross-ecosystem | `tool_map = {read: 'filesystem.read', bash: 'terminal.exec'}` |
| 14 | Description 50-100 chars | Validator en skills, error si >1024 chars o <20 chars |
| 15 | Allowlist por agente | `agent.skills_allowlist = ['pdf', 'web', 'memory']` |
| 16 | NO delegación directa — kernel decide | `kernel.decide()` siempre, plugin solo ejecuta |
| 17 | 24/7 persistent daemon | systemd service + watchdog + heartbeat |
| 18 | Webhook triggers | Plugin `webhook` con FastAPI + signature validation |
| 19 | Scheduled execution | Plugin `scheduler` con APScheduler + cron syntax |
| 20 | Sub-agent "mayordomo" pattern | Patrón orchestrator-worker (kernel = mayordomo) |

---

## 🎭 10 IDEAS DE CLAUDE CODE (Anthropic oficial jul 2026)

| # | Idea | Cómo se integra al Osquestador |
|---|------|-------------------------------|
| 21 | SKILL.md format oficial (name + description + body) | Spec adoptada 1:1, no custom format |
| 22 | 3 niveles progressive disclosure | Loader carga Tier 1 siempre, Tier 2 on-demand, Tier 3 lazy |
| 23 | Reglas kebab-case + sin "claude"/"anthropic" | Validator rechaza nombres inválidos |
| 24 | Subagents con description "Use this when... It returns..." | Template de description obligatorio |
| 25 | @-mention para forzar | `@<agent>` en prompt dispara subagent específico |
| 26 | Custom slash commands `/skill-name` | `/<skill>` en chat UI ejecuta skill directamente |
| 27 | MCP servers + built-in tools | MCP server del Osquestador expone vault + memoria + state |
| 28 | Conversation context + memory persistence | 3 tiers context (stable/context/volatile) ya validado |
| 29 | Production-grade con hooks | 5 hooks: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop |
| 30 | Estética Claude/Anthropic (lo que Max pidió) | Panel UI idéntico a Claude.ai (sidebar, message bubbles, etc) |

---

## 🧠 10 IDEAS DE MEMORY PATTERNS (Obsidian vault + semantic search)

| # | Idea | Cómo se integra al Osquestador |
|---|------|-------------------------------|
| 31 | Vault = filesystem (markdown + frontmatter + wikilinks) | `~/.osquestador/proyectos/<id>/vault/` |
| 32 | Review folder separado para writes de agente | `vault/_review/` antes de promote a canonical |
| 33 | 5 context files (CTX-*) | `CTX-aboutme.md`, `CTX-now.md`, `CTX-Work.md`, `CTX-project.md`, `CTX-systems.md` |
| 34 | Retention rules (prune over append) | Background job revisa y limpia cada 24h |
| 35 | BM25 + vector hybrid search | Plugin `search` con SQLite FTS5 + FAISS MiniLM-L6-v2 |
| 36 | Agentic Atomic Markdown Memory (1 fact = 1 archivo) | `vault/facts/<uuid>.md` con frontmatter |
| 37 | 0 database, 0 daemon obligatorio | Solo SQLite (que es file, no server) + vault filesystem |
| 38 | Bilateral sync (human review promotes) | Workflow: agent write → review folder → human approve |
| 39 | Wikilinks para resolver depth | Parser `[[Title]]` → resolve via Glob |
| 40 | Provenance tracking | Frontmatter `provenance: {source, agent, ts}` |

---

## 🔄 10 IDEAS DE SUB-AGENT DELEGATION (5 patrones validados)

| # | Idea | Cómo se integra al Osquestador |
|---|------|-------------------------------|
| 41 | Orchestrator-worker (40-60% ahorro) | Kernel = orchestrator, plugins = workers |
| 42 | ACP primitives: spawn + child_context + scopes | `spawn_subagent(profile_id, scopes, ttl, max_budget)` |
| 43 | Depth cap = 5 | `MAX_AGENT_DEPTH = 5` en config, reject cycles |
| 44 | Scopes narrow only | Validator rechaza scope widening |
| 45 | Solo summary al parent | `return summary` no transcript completo |
| 46 | Token cost awareness (7x single-thread) | Monitoring: `tokens_per_session`, warning a 70% |
| 47 | Parallel cuando NO dependencies | `asyncio.gather(*tasks)` con budget compartido |
| 48 | Sequential cuando SÍ dependencies | Pipeline mode con checkpoint por step |
| 49 | Router para dispatch simple | Plugin `router` clasifica con LLM pequeño (M2.5) |
| 50 | Pipeline para fixed linear | Plugin `pipeline` con state machine |

---

## 💾 10 IDEAS DE CHECKPOINT / RESUME (Google ADK + Dapr + zylos)

| # | Idea | Cómo se integra al Osquestador |
|---|------|-------------------------------|
| 51 | SQLite-first checkpoints | Default storage = SQLite en `db/checkpoints.db` |
| 52 | PostgreSQL prod | Config `DATABASE_URL=postgresql://...` opcional |
| 53 | Idempotency keys | `idempotency_key = f"{workflow_id}:{step_id}"` |
| 54 | 4 primitives: workflow_id + step_id + snapshot + resume | State schema `Checkpoint(workflow_id, step_id, state, ts)` |
| 55 | Retention 90 días | Cron job limpia `WHERE ts < now() - 90d` |
| 56 | Async checkpointing | `await checkpoint.save()` no bloquea next step |
| 57 | Resume desde último step | `resume(workflow_id)` → load checkpoint → continue |
| 58 | Durable memory schemas | `ToolContext.state` typed, no JSON crudo |
| 59 | Event-driven dormancy | `await event.wait()` no polling |
| 60 | State schema explícito (no replay de history) | Pydantic models para state, no append-only log |

---

## 📊 RESUMEN DE INTEGRACIÓN

| Métrica | Valor |
|---------|-------|
| Total ideas | 60 |
| Fuentes | 7 (Hermes, OpenClaw, Claude Code, Memory, Sub-agents, Checkpoint, Frameworks) |
| Plugins del Osquestador que usarán estas ideas | 5-10 |
| Commits por pushear al final | 3 (BITACORA, state.json, TABLA_IDEAS_INTEGRADAS.md) |
| Listo para FASE 5 | ✅ Sí |

---

**CONFIRMACIÓN DE ANOTACIÓN EN GITHUB:** Se commitea en este turno (commit siguiente).
