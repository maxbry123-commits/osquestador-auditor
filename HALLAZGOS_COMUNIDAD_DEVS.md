# HALLAZGOS DE LA COMUNIDAD DE DEVS
## Lo que la comunidad de desarrolladores ya resolvió (aplicado al Osquestador)

**Fecha:** 2026-07-18
**Investigador:** A2 (Mavis en delegación de Max)
**Total de búsquedas:** 25 (15 del Punto 1 + 10 del Punto 2)
**Trigger literal de Max:** "no me dijiste que conseguiste de la comunidad... que hace la comunidad de desarrolladores"
**Propósito:** Consolidar SOLO los hallazgos de la comunidad (no la visión de Max) para incluirlos en la programación del Osquestador.

---

## PUNTO 1 — MEMORIA EXTENDIDA (15 búsquedas comunidad devs)

### Hallazgo 1: Git como memoria de agente (4 fuentes, mismo patrón)

**Fuentes comunidad:**
- **Letta Code Context Repositories** — memoria de agente con git tracking nativo. Cada edit es auditable, rollback posible, subagentes que modifican la memoria en background quedan tracked.
- **GitOfThoughts** (arxiv 2606.14470) — "Each scored thought is a commit with author, timestamp, and content-hash metadata; scores are git notes; validation outcomes are tags (success_*, failed_*). Retrieval = git log --grep -S tag_filter." Branch `main` = session tree, branch `memory` = cross-problem insights.
- **mnem** (Uranid/mnem GitHub) — "Skills, decisions, and conventions live as nodes and typed edges in a queryable knowledge graph inside your project's `.mnem/` directory. Commit it alongside your code." Append-only op-log. Forgetting = first-class (revoke + audit trail).
- **GCC - Git-Context-Controller** (arxiv 2508.00031) — operaciones COMMIT, BRANCH, MERGE, CONTEXT explícitas. `.GCC/` directorio. Cada proyecto = roadmap (main.md) + branches con commit summaries + execution traces + metadata estructurada.
- **Reddit r/AI_Agents** — 2 años construyendo memoria, terminó con git: "Each conversation is treated as a commit. Enables: git diff (cómo evolucionó la comprensión), git blame (cuándo se adquirió info), git checkout (reconstruir conocimiento en momento dado)."

**Aplicación al Osquestador:**
- Repo `osquestador-memoria` con `memoria_commit/log/diff/blame/checkout/branch/merge` tools
- Cada evento significativo del agente = commit con metadata estructurada
- Hot tier = scratchpad efímero · Warm = SQLite summaries · Cold = git commits firmados

### Hallazgo 2: Multi-tenant isolation = directorio + namespace, no DB separada

**Fuentes comunidad:**
- **fast.io** — "Tenant A's agent must never access Tenant B's RAG index or history. They might share the same LLM and servers, but the data stay apart."
- **Microsoft Azure architecture** — 3 niveles: row-level (compartido schema, tenant_id predicate), schema isolation (DB compartido, schemas separados), DB isolation (instancias separadas)
- **zylos.ai** (Resource Governance 2026) — "Production platforms converge on: namespace or container isolation for the runtime, vector-namespace or separate-database isolation for memory, credential vaulting with per-tenant scopes, and token-bucket rate limiting per tenant. Ephemeral workspace isolation is the first line."
- **dev.to/whoffagents** — RLS en PostgreSQL: `ALTER TABLE projects ENABLE ROW LEVEL SECURITY; CREATE POLICY tenant_isolation ON projects USING (organization_id = current_setting('app.current_tenant')::uuid);`
- **Agent Sandbox** (kubernetes-sigs/agent-sandbox) — pods aislados por run, reset entre tenants

**Patrón dominante 2026: Workspace-per-Tenant** (directorio + metadata filter, DB física separada solo para regulated)

**Aplicación al Osquestador:**
- `~/.osquestador/proyectos/<project_id>/` con TODO dentro
- SQLite FTS5 + FAISS namespace por proyecto
- Validación en cada tool call: project_id match antes de ejecutar
- OpenClaw queda aislado (no comparte workspace)

### Hallazgo 3: HWC memory tiering con redistribución automática

**Fuentes comunidad:**
- **clawrxiv 2603.00037** — "Memory Tiering solves this with a principled hierarchical approach: HOT (current session + 2-3 next turns, <500 tokens) / WARM (stable persistent facts, 1000-3000 tokens) / COLD (long-term archive, unbounded)"
- **armalo.ai/cortex** — "HWC divides agent memory into three layers with distinct storage characteristics, retrieval latencies, update frequencies, and retention policies. Hot is never the only memory. At session start, Warm is searched for relevant context."
- **flumes.ai** — "Tiered memory model: Hot (high-relevance low-latency), Warm (summarized threads), Cold (archived logs). System does the routing."
- **agenticskillset.org** — "Tier 1 Hot (last 15-25 turns, <500 tokens target) / Tier 2 Warm (running summary 600-1200 tokens, every 15-25 turns) / Tier 3 Cold (project archive 1500-2500 tokens, session boundaries)"
- **kunalganglani.com** (production guide 2026) — 4 tiers reales: in-context + external KV + episodic log + semantic vector. "Tiered storage can cut agent memory costs 3-4x without sacrificing recall."

**Reglas de redistribución (consenso):**
- HOT >800 tokens → trigger redistribución
- Session end → redistribute
- Manual command: "run memory tiering"
- After `/compact` operation

**Aplicación al Osquestador:**
- HOT = RAM del orquestador, rotación por session_id
- WARM = SQLite `~/.osquestador/memoria/warm/<proyecto>.sqlite` con summaries
- COLD = GitHub repo `osquestador-memoria` con summaries firmados
- Hook `Stop` ejecuta redistribución automática

### Hallazgo 4: Working memory scratchpad (Anthropic cookbook + Microsoft)

**Fuentes comunidad:**
- **jatinbansal.com** — "Working memory gives the harness a structured task state. It may use typed fields, a key-value store, a graph node, or a file. The agent updates it through an explicit tool or structured directive, and it survives eviction of the messages that produced it."
- **max-gherman.dev** — "Short-term memory is what happened in this conversation. It's the agent's working memory, the scratchpad that lets it reason across multiple turns."
- **hidekazu-konishi.com** — "Within a session it anchors the plan against compaction. Across sessions it becomes the bootstrap: the next session starts by reading the notes instead of replaying the transcript."
- **Microsoft Agent Framework** — LangGraph uses checkpointing for "scratchpad" — write to state, fetch at any step

**Regla universal:** "Prune what can be re-fetched, summarize what cannot, retrieve rather than carry."

**Aplicación al Osquestador:**
- Scratchpad: `~/.osquestador/proyectos/<id>/vault/working/<session_id>.md`
- Tool `scratchpad_write` del agente → kernel persiste
- Al cerrar sesión, items durables se promueven a vault o se commitean al repo

### Hallazgo 5: Motor de búsqueda on-connect es estándar 2026

**Fuentes comunidad:**
- **Vault Semantic** (mcpmarket.com) — "Local semantic search server as a sidecar for MCP-enabled agents. Indexes Markdown files, chunking by headings and paragraphs, embedding with OpenAI text-embedding-3-small. Hybrid search FTS5 + cosine-similarity + folder-based ranking. Original Markdown = source of truth, SQLite = derived index. All exposed via stdio as MCP tools."
- **Obsidian Hybrid Search** (Reddit r/Rag) — "BM25 + trigram fuzzy + vector embeddings + RRF, single SQLite, offline, MCP server + CLI"
- **Reddit MCP server (FAISS + FTS5)** — "FAISS index 384-d all-MiniLM-L6-v2. Hybrid retrieval through Reciprocal Rank Fusion. 12 brain regions, auto-classifier. After 159 tests, 2 seconds."
- **Memori SDK** (memorilabs.ai) — namespace por proyecto, conscious_ingest + auto_ingest
- **mistaike Shared Brain** — "On session start, search_memories for guardrails first. During work: search_memories before implementing anything. save_memory after discovering anything."
- **LikelyMalware Agent Brain** — "Claude Code auto-reads any `CLAUDE.md` in the working directory at session start. The key insight: CLAUDE.md doesn't hold the context. It holds the pointers to the context."
- **Azure Arc indexed-sources MCP** — 6 search tools: search_hybrid / search_vector / search_text / search_image / search_multimodal / get_available_collections
- **Atlan Context Bootstrapping** — "RAG retrieves documents. Bootstrapping builds infrastructure. With RAG, you're hoping retrieval surfaces the right definition. With bootstrapping, you're ensuring the canonical definition exists, is versioned, and is delivered to agents at inference time."

**Aplicación al Osquestador:**
- 6 search tools MCP: `osquestador_search_hybrid/keyword/vector/recent/tags/collections_list`
- SessionStart hook dispara pre-carga + background indexing
- Cold start <200ms via seed context strategy

### Hallazgo 6: Web search engines 2026 (Tavily/Exa/Perplexity)

**Fuentes comunidad:**
- **alphacorp.ai** benchmark 2026 — Tavily 5th overall (Agent Score 13.67), Perplexity 7th (12.96), pero Tavily 998ms vs Perplexity 11+ segundos
- **exa.ai/versus/tavily** — Exa p95 1.4-1.7s, WebWalker 81% vs Tavily 71%
- **parallel.ai** — Tavily 93% SimpleQA, Exa 87%, Perplexity 92%, Tavily $0.110/req, Exa $7/1k, Perplexity $5/1k
- **Reddit r/Rag** — calidad: 1. Linkup 2. Tavily 3. Exa · latencia: 1. Exa 2. Tavily 3. Linkup

**Aplicación al Osquestador:**
- Default web search: Tavily (latencia + RAG-native)
- Multi-hop: Exa
- Cheap fallback: Perplexity
- Cache local 24h en `~/.osquestador/cache/web/`

### Hallazgo 7: Hooks lifecycle (Gemini CLI, VSCode, Trigger.dev)

**Fuentes comunidad:**
- **Gemini CLI Hooks** — 5 eventos: BeforeSession, BeforeModel, AfterModel, BeforeTool, AfterTool
- **VSCode Copilot Chat** — SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PreCompact, SubagentStart, SubagentStop, Stop
- **Trigger.dev** — preload, turn start, turn complete, suspend, resume

**Aplicación al Osquestador:**
- 5 hooks nativos: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop

### Hallazgo 8: Cold start mitigation (Ailore, Atlan, Memory Engine)

**Fuentes comunidad:**
- **Ailore** — "Lazy registration: register tools on first demand. Synthetic priming: pre-seed vector store with common documents. Hybrid initialization: static + dynamic. Seed context strategy: inject minimal guaranteed-available tools."
- **Atlan** — "Context bootstrapping = Harvest (30d) → Enrich (30d) → Validate (30d). 90 days to production-ready."
- **Memory Engine (AgentStack)** — "Auto-initializes on first MCP connection. Incremental indexing (JSON manifest). Git-aware synchronization. Branch-aware retrieval."

**Aplicación al Osquestador:**
- Seed context al SessionStart: AGENTS.md + 00_INDICE.md + last 3 summaries
- Background: re-indexar vault, pull últimos 10 commits
- Ready en <200ms

---

## PUNTO 2 — ANCLAJE DE SKILLS (10 búsquedas comunidad devs)

### Hallazgo 9: 5 marketplaces principales de skills

**Fuentes comunidad:**
- **ClawHub** (oficial OpenClaw) — "App store for Claude Code capabilities. Curated, versioned, installable via clawhub CLI. `clawhub install seo`"
- **SkillsMP** — "1.1M+ skills aggregated from public GitHub. Community-aggregated. Open-source MIT license. agent-skills-cli universal CLI across Claude Code, Cursor, Copilot, Codex."
- **SkillHub** — "87K+ ranked skills with S/A/B grading (Practicality, Clarity, Automation, Quality, Impact). S-rank = 9.0+. CLI install, desktop app, Skill Stacks."
- **OpenAgentSkill** — "Decision and install layer. GitHub auto-discovery pipeline expands registry hourly. Agent Proven Score from real outcome reports. Trust scores + audit signals."
- **skillhu** — "Computer Use Skills Marketplace — browse, share, install automation skills"
- **load-skill** (npm) — "Aggregates skills from multiple sources into single searchable registry. 1,176 skills pre-indexed. Multi-tool support."
- **SkillRegistry** (UBOS) — "Centralized AI skill marketplace. Aggregates 'skills' into single searchable directory. Registry of SKILLS.md files."

**Aplicación al Osquestador:**
- Consulta en paralelo: ClawHub + SkillsMP + OpenAgentSkill + GitHub + repo local
- Cache local 24h con TTL
- Trust scores para evitar supply-chain attacks

### Hallazgo 10: Skilldex = package manager + registry (arxiv 2604.16911)

**Fuentes comunidad:**
- **Skilldex** — "Package manager and registry for agent skill packages. Hierarchical scoping, agent-driven suggestion, community registry. Implements MCP server exposing skilldex_install/list/validate/search/suggest/uninstall. Three install paths: registry name / git URL / local path."

**Aplicación al Osquestador:**
- `osquestador://skill_install` con 3 paths
- MCP server con `skilldex_list/search/install/validate`

### Hallazgo 11: Anthropic Skills doble uso (estándar 18 dic 2025)

**Fuentes comunidad:**
- **anthropic.com/engineering** — "We've published Agent Skills as an open standard for cross-platform portability. Like MCP, we believe skills should be portable across tools and platforms — the same skill should work whether you're using Claude or other AI platforms."
- **agensi.io** — "The Agent Skills open standard is SKILL.md. Anthropic published the format, and Claude Code, Cursor, Codex CLI, OpenCode, OpenClaw, and 20+ other agents all read it. One skill file works everywhere."
- **claudecoworkcourse.com** — "In December 2025, Anthropic published the Skills spec as an open standard."
- **ComposioHQ/awesome-claude-skills** — "Supported by Claude Code, Claude.ai, Claude API, OpenAI Codex, Cursor, Gemini CLI, Antigravity, and Windsurf."

**Aplicación al Osquestador:**
- Acepta SKILL.md estándar sin modificar
- Expone via MCP para cualquier agente
- Una skill escrita para Claude Code funciona en el Osquestador tal cual

### Hallazgo 12: Cross-client `.agents/skills/` convention

**Fuentes comunidad:**
- **dev.to/rosgluk** — "If you are building for Claude Code first and only, author in `.claude/skills/`. If you genuinely want cross-client portability, target the open Agent Skills shape and use `.agents/skills/` as the canonical path."
- **reddit.com/r/ClaudeAI** — "Cursor, VS Code / GitHub Copilot, OpenAI's Codex CLI all share the same Skills format now. Similar to how .editorconfig unified formatting standards."
- **claudskills.com** — "AGENTS.md is now an open standard adopted by the Agentic AI Foundation and read by Codex, Cursor, Windsurf, Gemini CLI, and Copilot. ClaudSkills indexes 76,000+ SKILL.md files."

**Aplicación al Osquestador:**
- Skills se almacenan en `~/.agents/skills/` (estándar cross-client)
- Symlinks opcionales a `.claude/skills/`, `.cursor/skills/`, etc

### Hallazgo 13: Symlinks cross-platform (opensite-skills)

**Fuentes comunidad:**
- **dev.to/opensite** — "setup.sh auto-detects installed platforms (Claude Code, Codex, Cursor) and creates symlinks from each agent's skill directory back to the shared repo. `git pull` on shared repo propagates changes instantly."

**Aplicación al Osquestador:**
- setup.sh para que el Osquestador detecte agentes instalados y cree symlinks
- Una skill = múltiples consumidores sin duplicar

### Hallazgo 14: Knowledge distillation (COLLEAGUE.SKILL, NotebookLM workflow)

**Fuentes comunidad:**
- **COLLEAGUE.SKILL** (arxiv 2605.31264) — "Automated trace-to-skill distillation system. Analyzers extract evidence about durable capability, mental models, bounded interaction style; builders render structured Markdown; shared writer produces the skill package."
- **pasqualepillitteri.it** — "Knowledge-distillation workflow converts NotebookLM source collection into single Markdown file installable as permanent skill in Claude Code. NotebookLM becomes synthesis engine that produces structured operating manual."
- **alirezarezvani/claude-skills** — "Knowledge flows from `references/` → into `SKILL.md` workflows → executed via `scripts/` → applied using `assets/` templates."

**Aplicación al Osquestador:**
- Valida que los 2 engines de Max (Acquisition + Distillation) son best-practice 2026
- Acquisition Engine = Steering + Seed Knowledge (paper LLM KD)
- Distillation Engine = Generation + Training (paper LLM KD)

### Hallazgo 15: 90/10 código/LLM (Compiled AI, SOURCE CODE AGENT, Deterministic Scaffolding)

**Fuentes comunidad:**
- **Compiled AI** (arxiv 2604.05150) — "LLMs generate executable code artifacts during compilation phase, after which workflows execute deterministically without further model invocation. Zero stochasticity, near-zero marginal inference cost."
- **SOURCE CODE AGENT** (arxiv 2508.02721) — "Blueprint First, Model Second. Expert-defined operational procedure codified into machine-readable Execution Blueprint. Deterministic engine executes blueprint with complete fidelity. Foundation Model is no longer central decision-maker but is invoked as specialized tool at specific nodes."
- **arunbaby.com** — Decision framework:
  1. ¿Unit test cubre 95%+ de inputs? → CÓDIGO
  2. ¿Input space open-ended? → LLM
  3. ¿Ambos? → Hybrid supervisor
  "Most production workflows should use LLM nodes for 20-40% of steps, code for the rest."
- **Charles Sieg** — "Deterministic Scaffolding around Non-deterministic Core. You do not need a deterministic model. You need deterministic scaffolding."
- **Stop Using LLMs for Everything** (YouTube) — "By treating the LLM as a highly capable function rather than the entire operating system, you can cut your token costs by 50-90%."

**Aplicación al Osquestador (regla 90/10 de Max):**
- **90% código:** hooks, search, cache, validación, descarga, routing, persistencia, state machine
- **10% LLM:** query expansion, summarization, scoring, tag generation — todo en build-time

---

## RESUMEN EJECUTIVO (10 patrones aplicados al Osquestador)

| # | Patrón comunidad | Aplicado en módulo |
|---|------------------|---------------------|
| 1 | Git como memoria (Letta, GitOfThoughts, mnem, GCC) | `osquestador-memoria` repo + tools memoria_* |
| 2 | Workspace-per-Tenant (fast.io, Azure, zylos) | `~/.osquestador/proyectos/<id>/` + namespace SQLite |
| 3 | HWC tiering (clawrxiv, armalo, flumes) | HOT/WARM/COLD con redistribución automática |
| 4 | Working memory scratchpad (Anthropic, MS) | `vault/working/<session_id>.md` con tool scratchpad_write |
| 5 | Search engine on-connect (Vault Semantic, Obsidian Hybrid) | SessionStart hook + 6 search tools MCP |
| 6 | Web search engines (Tavily, Exa, Perplexity) | `osquestador://web_search` con cache 24h |
| 7 | Hooks lifecycle (Gemini, VSCode, Trigger.dev) | 5 hooks nativos en kernel |
| 8 | Cold start mitigation (Ailore, Atlan, Memory Engine) | Seed context strategy <200ms |
| 9 | 5 marketplaces skills (ClawHub, SkillsMP, etc) | Búsqueda paralela multi-fuente |
| 10 | Compiled AI 90/10 (arxiv) | Build-time vs run-time, código > LLM |

---

## INCLUSIÓN EN LA PROGRAMACIÓN

Estos 10 patrones son **requirements** del Osquestador. Se traducen en:

- **17+ módulos Python** (ver `docs/fuente_max/README.md` mapeo)
- **~2-3k líneas de código** (90% determinístico)
- **6 skills de skills** (mcp tools) + **2 engines** (acquisition + distillation)
- **3 search engines** (local / web / memoria histórica)
- **5 hooks** nativos en el kernel
- **3 tiers de memoria** (HOT/WARM/COLD) con redistribución

**Programación inicio:** después de aprobación de los 4 puntos + docs de Max commiteados.

---

**Aprobado por:** Max (turno 2026-07-18 01:42)
**Commits relacionados:** `1ecd437`, `cb07bc9`, `fb51ffc`, `a71dd5e`, `f7a9877`
**Próximo commit:** este archivo + integración en `TASKS.md` y `state.json`
