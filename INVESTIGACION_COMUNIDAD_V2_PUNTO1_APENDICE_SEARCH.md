# APÉNDICE PUNTO 1 — Motor de búsqueda auto-activado
## Activación on-connect del motor de búsqueda sobre documentos y memoria

**Fecha:** 2026-07-18
**Investigador:** A2 (Mavis en delegación de Max)
**Búsquedas:** 5 (perplexity/tavily/exa, on-connect bootstrap, hooks lifecycle, MCP search engine, cold start pre-warm)
**Trigger del pedido:** Max — "que se active un motor de búsqueda cada vez que el agente conectado o el chat se active"
**Estado:** COMPLETO — apéndice del Punto 1, listo para revisión

---

## Síntesis ejecutiva (4 bullets)
1. **El patrón "on-connect search" ya es práctica estándar en producción 2026** — Obsidian Hybrid Search MCP, Vault Semantic, Memori SDK, mistaike Memory Vault y Azure Agentic Retrieval TODOS auto-activan el search engine al primer tool call o al handshake. NO es un opt-in, es el default.
2. **Hay 3 tipos de search engines a orquestar** en el Osquestador: (a) **web search externo** (Tavily/Exa/Perplexity para traer info fresca al agente), (b) **local vault search** (BM25 + vector + hybrid sobre los markdown del proyecto), (c) **memoria histórica search** (sobre el log de commits + summaries comprimidos). El Osquestador expone los 3 vía MCP, el agente decide cuál usar.
3. **Hooks de lifecycle son el mecanismo correcto para auto-activación** — VSCode Copilot Chat, Gemini CLI, Claude Code y Trigger.dev usan el mismo patrón: `SessionStart` (bootstrap), `UserPromptSubmit` (auto-search antes de cada prompt), `PreToolUse`/`PostToolUse` (logging). El Osquestador implementa los 4 eventos clave para que el search engine se dispare sin que el usuario lo pida.
4. **Para evitar cold start, el Osquestador pre-carga en background** — siguiendo el patrón "seed context" de Atlan/Ailore: en `SessionStart`, lanza background pipeline que (1) embebe descripciones de tools/skills, (2) puebla mini vector index del vault, (3) carga facts session-independent. Mientras tanto, el seed set (search + calculator + read) está disponible en <200ms. El primer prompt del usuario ya tiene search engine listo.

---

## Búsqueda 1 — `perplexity exa tavily AI search engine API document retrieval agent`
**Fuentes:** alphacorp.ai, tavily.com, reddit.com/r/Rag, exa.ai, parallel.ai
**Hallazgo clave — los 3 grandes players 2026:**
- **Tavily** (adquirido por Nebius feb 2026): RAG-native, JSON estructurado con summaries/citations/highlights, ~998ms latencia, $0.008/credit, 93% accuracy SimpleQA. **Default recomendado para RAG/agents.**
- **Exa**: semantic embedding-based, 4 tiers (instant/fast/deep/deep-reasoning), 1B+ LinkedIn profiles indexados, p95 1.4-1.7s, $5/1k búsquedas. Specialized indexes (people, company, code). 87% accuracy SimpleQA, **81% vs Tavily's 71% en WebWalker** (multi-hop retrieval).
- **Perplexity Sonar**: LLM+search bundled, ranked results, ~$5/1k requests, 92% SimpleQA. Rate limit 50 calls/min = constraint para high-volume.
- **Brave Search**: $5-9/1k, bueno para keyword puro.
- **Linkup**: 3rd en quality ranking, 4to en latency.

**Para nuestro caso (agente conectado al Osquestador necesita buscar en docs/memoria LOCAL primero, web solo si no encuentra):**
- **Default interno: hybrid local search** (BM25 + FAISS + RRF fusion) — sin API key, sin latencia externa, zero costo
- **Web fallback: Tavily** (default RAG) o Exa (si Max necesita multi-hop / LinkedIn). Decisión la toma el Osquestador cuando el agente llama `osquestador://web_search` y el hybrid local retorna <N resultados relevantes.

**Aplicación al Osquestador:**
- Tool MCP `local_search(query, project_id, top_k, mode=hybrid|bm25|vector)` → busca en vault+memoria del proyecto
- Tool MCP `web_search(query, engine=tavily|exa|perplexity)` → fallback externo
- Tool MCP `deep_research(query, max_hops=3)` → Exa multi-hop, $0.015/query

---

## Búsqueda 2 — `on connect search engine agent startup bootstrap query memory vault auto`
**Fuentes:** likelymalware.com (Agent Brain Obsidian), dev.to/filippo_venturini (CtxVault), agentstack.voostack (Memory Engine), dev.to/mistaike (Shared Brain), memorilabs.ai
**Hallazgo clave (oro puro):**
- **LikelyMalware Agent Brain**: "Claude Code auto-reads any `CLAUDE.md` in the working directory at session start… the agent reads the bootstrap, follows the pointers, and within 10 seconds it knows how the vault works, who you are, and how you like to work. The key insight: `CLAUDE.md` doesn't hold the context. It holds the pointers to the context." Smart Connections plugin + MCP server = semantic search exposed to external agents.
- **CtxVault**: "Each vault is just a folder on your machine. Drop documents in, index them, and they become semantically queryable." Tres interfaces: CLI humans, HTTP API agentes, MCP no-code.
- **Memory Engine (AgentStack)**: "Auto-initializes on first MCP connection… Incremental indexing (JSON manifest, only changed files re-indexed)… Git-aware synchronization (detects branch, HEAD commit, staged/modified files via safe read-only Git commands)… Branch-aware retrieval (prefers memory from the current branch)." **ESTE ES CASI LITERALMENTE LO QUE QUEREMOS.**
- **mistaike Shared Brain**: "On session start, search_memories for guardrails first… During work: search_memories before implementing anything. save_memory after discovering anything."
- **Memori SDK**: namespace por proyecto, conscious_ingest (short-term) + auto_ingest (dynamic memory search).

**Aplicación al Osquestador (este es el patrón EXACTO que pidió Max):**

```
[Agente se conecta al Osquestador]
  ↓
[Osquestador detecta connection: agent_id + project_id]
  ↓
[AUTO-TRIGGER SessionStart hook]
  ├─ 1. Lee ~/.osquestador/proyectos/<project_id>/AGENTS.md
  ├─ 2. Lee ~/.osquestador/proyectos/<project_id>/vault/00_INDICE.md
  ├─ 3. Pre-carga últimos 5 summaries de WARM tier (SQLite)
  ├─ 4. Lanza background: indexar vault (BM25 + FAISS si no está)
  ├─ 5. Lanza background: pull últimos 10 commits del repo memoria
  └─ 6. Responde al agente: "hello, tienes N tools, tu project es X, search engine listo en ~200ms"
  ↓
[Agente hace primer prompt]
  ↓
[AUTO-TRIGGER UserPromptSubmit hook]
  ├─ 1. Query expansion (si query corta, generar 3 variaciones)
  ├─ 2. Hybrid search local: BM25 + vector + RRF fusion
  ├─ 3. Top 5 results inyectados al contexto del agente
  └─ 4. Si <2 results relevantes: trigger web_search Tavily como fallback
```

**Implementación técnica (mapeo directo):**
- **Indice BM25**: SQLite FTS5 sobre el vault del proyecto (built-in, zero deps)
- **Vector index**: FAISS local por proyecto (sentence-transformers miniLM-L6-v2 offline, 384-dim, gratis)
- **Reciprocal Rank Fusion**: combina BM25 + vector scores en ranked list
- **Background indexing**: watchdog sobre `vault/` folder, re-index incremental
- **Search engine endpoint MCP**: `osquestador://search?query=X&project_id=Y&top_k=10&mode=hybrid`

---

## Búsqueda 3 — `hook trigger on chat activate proactive search engine AI agent context`
**Fuentes:** rajatpandit.com (Gemini CLI Hooks), feedback.clerk.chat (webhooks), github.com/microsoft/vscode-copilot-chat (hooks), trigger.dev
**Hallazgo clave:**
- **Gemini CLI Hooks**: 5 eventos lifecycle
  - `BeforeSession` — "pull the latest changes from your git repository"
  - `BeforeModel` — "Silently append file contents, database schemas, or issue tracker details to the system prompt based on what you typed" ← **ESTE ES EL TRIGGER DE SEARCH ON PROMPT**
  - `AfterModel` — log/audit
  - `BeforeTool` — guardrail
  - `AfterTool` — verification
- **VSCode Copilot Chat hooks**: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, `Stop`
- **Trigger.dev**: lifecycle hooks en cada stage de chat agent run: preload, turn start, turn complete, suspend, resume
- **Clerk Chat webhooks**: trigger agente por webhook externo

**Aplicación al Osquestador — los 4 hooks que implementamos:**

| Hook | Cuándo | Qué hace el Osquestador |
|------|--------|------------------------|
| `SessionStart` | Agente/chat se conecta | Lee AGENTS.md, pre-indexa vault, carga summaries, responde capabilities |
| `UserPromptSubmit` | Usuario/Agente envía prompt | Auto-search hybrid sobre vault+memoria, inyecta top-5 al contexto |
| `PreToolUse` | Antes de cada tool call del agente | Valida project_id, log, rate limit |
| `PostToolUse` | Después de tool call | Index resultado si es nuevo knowledge, update WARM tier si relevante |
| `Stop` | Sesión termina | Commit final al repo memoria, redistribuir HOT→WARM si HOT>800 tokens |

**Diferencia vs Gemini CLI:** el Osquestador NO usa scripts externos, ejecuta los hooks nativamente en el kernel. Más rápido, sin IPC overhead.

---

## Búsqueda 4 — `MCP server search engine local documents vault semantic hybrid retrieval`
**Fuentes:** mcpmarket.com (Semantic Vault Search, Vault Semantic), reddit.com/r/vibecoding, reddit.com/r/Rag, learn.microsoft.com (Azure Arc), mcpmarket.com/server/vault-semantic
**Hallazgo clave:**
- **Semantic Vault Search (qmd)**: BM25 + vector similarity + LLM re-ranking. Local-first, zero API key, privacy-conscious.
- **Vault Semantic** (sidecar MCP server para OpenClaw): "indexes Markdown files within a specified vault root, chunking content by headings and paragraphs, then embedding these chunks using OpenAI's text-embedding-3-small… hybrid search FTS5 + cosine-similarity + folder-based ranking. Original Markdown remains source of truth, SQLite database is derived search index that can be rebuilt at any time." ← **PATRÓN CONFIRMADO, no reinventar la rueda.**
- **Reddit MCP server (FAISS + FTS5)**: "FAISS index (384-d, all-MiniLM-L6-v2)… hybrid retrieval through Reciprocal Rank Fusion, combining semantic and keyword searches, followed by cross-encoder re-ranking… 12 distinct 'brain regions', allowing queries to be directed to the relevant areas instead of scanning everything at once. Auto-classifier that adapts based on corrections received."
- **Obsidian Hybrid Search**: BM25 + trigram fuzzy + vector embeddings + RRF, single SQLite, offline, MCP server + CLI.
- **Azure Arc indexed-sources MCP server**: 6 search tools (`search_hybrid`, `search_vector`, `search_text`, `search_image`, `search_multimodal`, `get_available_collections`), runs on port 8080, MCP JSON-RPC.

**Aplicación al Osquestador — ya NO diseñamos desde cero, adoptamos patrón Vault Semantic:**
- Vault por proyecto = source of truth (markdown files)
- SQLite local = derived search index (FTS5 BM25 + embeddings table)
- Re-indexable en cualquier momento desde los markdown
- 6 search tools vía MCP, mismo naming que Azure Arc:
  - `osquestador_search_hybrid(query, project_id, top_k)` — default
  - `osquestador_search_keyword(query, project_id, top_k)` — exact match
  - `osquestador_search_vector(query, project_id, top_k)` — semantic
  - `osquestador_search_recent(query, project_id, since, top_k)` — freshness
  - `osquestador_search_tags(tags, project_id, top_k)` — filter by tags
  - `osquestador_collections_list()` — qué proyectos tiene el agente disponibles

---

## Búsqueda 5 — `AI agent startup search index pre-warm context bootstrap query expansion`
**Fuentes:** atlan.com (Context Bootstrapping), learn.microsoft.com (Agentic Retrieval Azure), ailore.ai (Cold Start), haystack.deepset.ai (Query Expansion), nexuscybernetwork.com (AGT006/AGT007)
**Hallazgo clave:**
- **Atlan Context Bootstrapping**: "Automated generation of a governed context layer from existing enterprise data signals. Not a memory tool. Not RAG. Not a bigger context window. RAG retrieves documents. Bootstrapping builds infrastructure. With RAG, you're hoping retrieval surfaces the right definition. With bootstrapping, you're ensuring the canonical definition exists, is versioned, and is delivered to agents at inference time." 90-day rollout: Harvest (30d) → Enrich (30d) → Validate (30d).
- **Azure Agentic Retrieval**: "Multi-query pipeline designed for complex questions… LLM to break down a complex query into smaller, focused subqueries for better coverage… Subqueries can include chat history for extra context. All subqueries run simultaneously and can be keyword, vector, or hybrid search. Each subquery undergoes semantic reranking."
- **Ailore Cold Start**: "Lazy registration (register tools on first demand), seed context strategy (inject minimal guaranteed-available tools), hybrid initialization (static + dynamic), synthetic priming (pre-seed vector store with common documents). Tradeoff: seed set must be handpicked per domain. Missing a critical tool forces slow dynamic discovery."
- **Haystack Query Expansion**: "Expand keyword queries to improve recall. User Query: 'open source NLP frameworks' → After: ['natural language processing tools', 'free nlp libraries', 'open-source language processing platforms', 'NLP software with open-source code', 'open source NLP frameworks']. Use BM25 + query expansion to increase recall."
- **AGT006 Context-Aware Query Expansion**: "Augments agent's initial context search query with related terms, associated entities, and semantically adjacent concepts derived from the agent's own stored memory graph." Bounded scope to prevent over-retrieval.
- **AGT007 Memory Search Index**: "Persistent, retrieval-optimized data structure… typically combining inverted indices for keyword search with vector indices for semantic similarity lookup. Must be maintained in sync with the underlying memory store, with incremental update mechanisms that avoid full re-indexing on each memory write."

**Aplicación al Osquestador — cold start strategy definitivo:**

```
[SessionStart hook] (target: <200ms to first response)
├─ INMEDIATO (sync, <50ms):
│  ├─ Load AGENTS.md (punt + index paths)
│  ├─ Load 00_INDICE.md (vault TOC)
│  ├─ Load last 3 summaries de WARM tier
│  └─ Register seed tools: search, read, write, commit, log
│
├─ BACKGROUND (async, <200ms target):
│  ├─ Verify/refresh FAISS index del vault (incremental)
│  ├─ Verify/refresh FTS5 BM25 index
│  ├─ Pull últimos 10 commits del repo memoria (si hay red)
│  └─ Expand query embedding cache (top 100 queries frecuentes)
│
└─ READY STATE: agente puede buscar en <200ms
```

**Query expansion integrada en el Osquestador (auto, transparente al agente):**
- Cada query del agente se pasa por `QueryExpander` que genera 3 variaciones
- Search corre en paralelo sobre las 4 (original + 3) usando hybrid
- RRF fusion combina resultados
- Top-5 se inyectan al contexto del agente ANTES de que el LLM genere respuesta

---

## Decisión de arquitectura final (motor de búsqueda integrado al Punto 1)

### Los 3 search engines del Osquestador

| Engine | Scope | Trigger | Latencia target | Costo |
|--------|-------|---------|-----------------|-------|
| **Local hybrid** (BM25 + FAISS + RRF) | vault + memoria del proyecto | Auto en cada `UserPromptSubmit` | <200ms | $0 |
| **Web search** (Tavily default, Exa si multi-hop) | internet abierto | Fallback si local <2 resultados | ~1s | $0.008/query |
| **Memoria histórica** (git log + WARM summaries) | log completo del proyecto | Auto cuando query contiene "remember"/"antes"/"ayer" | <500ms | $0 |

### Hooks de lifecycle del Osquestador (implementación nativa en kernel)

```python
# osquestador/kernel/hooks.py
class OsquestadorHooks:
    async def on_session_start(self, agent_id, project_id):
        """<50ms sync + <200ms background"""
        # 1. Cargar AGENTS.md
        # 2. Pre-cargar summaries
        # 3. Background: re-indexar si hace >1h
        # 4. Responder capabilities

    async def on_user_prompt(self, query, project_id, context):
        """Auto-search ANTES de que el LLM responda"""
        # 1. Query expansion (3 variations)
        # 2. Hybrid search local
        # 3. Si <2 resultados: web_search fallback
        # 4. Inyectar top-5 al contexto

    async def on_pre_tool(self, tool_name, args, project_id):
        """Validación + rate limit + log"""
        # 1. Validar project_id match
        # 2. Rate limit check
        # 3. Audit log

    async def on_post_tool(self, tool_name, result, project_id):
        """Index si es nuevo knowledge"""
        # 1. Si result es markdown/doc: index para futuro search
        # 2. Si supera threshold importance: WARM tier update

    async def on_session_stop(self, session_id, project_id):
        """Commit final + redistribuir tiers"""
        # 1. Commit scratchpad al repo
        # 2. Si HOT>800 tokens: redistribuir
        # 3. Update 00_INDICE.md
```

### Stack técnico elegido (basado en evidencia, no en suposición)

| Componente | Tecnología | Justificación (fuente) |
|------------|-----------|------------------------|
| **BM25 keyword search** | SQLite FTS5 | Built-in, zero deps,probado por Vault Semantic + Obsidian Hybrid |
| **Vector embeddings** | FAISS + sentence-transformers/all-MiniLM-L6-v2 | 384-dim, offline, gratis, mismo stack que Reddit MCP server |
| **Embeddings (opcional upgrade)** | OpenAI text-embedding-3-small | Si Max quiere mejor quality (costo: $0.02/1M tokens) |
| **Hybrid fusion** | Reciprocal Rank Fusion (RRF) | Estándar 2026, usado por Vault Semantic + Obsidian Hybrid + Reddit |
| **Cross-encoder reranking (opcional)** | sentence-transformers/cross-encoder | Solo si budget permite, agrega ~200ms |
| **Query expansion** | Haystack QueryExpander con M2.5 (cerebras barato) | Patrón validado por Haystack |
| **Web search (default)** | Tavily API | Default RAG 2026, 998ms, 93% SimpleQA, $0.008/credit |
| **Web search (multi-hop)** | Exa API | Cuando query requiere razonamiento multi-paso |
| **Web search (cheap fallback)** | Perplexity Sonar | Cuando Tavily no está disponible |
| **Background indexing** | watchdog sobre vault/ | Patrón de Reddit MCP server, async, zero-blocking |
| **Cold start mitigation** | seed context + lazy registration | Patrón de Ailore + Memory Engine |

### Flujo end-to-end cuando un agente se conecta

```
1. Agente abre WS/MCP al Osquestador
   → handshake: agent_id, project_id (auto-asigna si nuevo), capabilities

2. Osquestador ejecuta SessionStart hook
   → Carga AGENTS.md, vault index, últimos 5 summaries
   → Background: re-index vault si hace >1h, pull últimos 10 commits
   → Responde: {tools_disponibles: [...], project: {...}, search_engine: "ready"}

3. Usuario o Agente envía primer prompt
   → Osquestador ejecuta UserPromptSubmit hook
   → Auto: query expansion (3 var) + hybrid search (BM25+FAISS+RRF)
   → Si <2 resultados: web_search Tavily fallback
   → Inyecta top-5 resultados al contexto del LLM

4. LLM genera respuesta con contexto relevante
   → PostTool hooks registran el tool call en audit log
   → Si fue un write al vault: re-indexa en background

5. Sesión termina
   → Stop hook: commit scratchpad al repo memoria
   → Si HOT>800 tokens: redistribuir a WARM/COLD
   → Update 00_INDICE.md del vault
```

---

## Métricas de éxito del motor de búsqueda

- [ ] **Latencia SessionStart → ready**: <200ms p95
- [ ] **Latencia UserPrompt → search results**: <500ms p95 (local), <2s p95 (con web fallback)
- [ ] **Recall hybrid search**: >85% en test set de 100 queries de Max
- [ ] **Cold start**: agente puede buscar en primer prompt sin warmup
- [ ] **Background indexing**: vault de 10k notas se re-indexa en <30s sin bloquear agente
- [ ] **Cross-project isolation**: search de proyecto A no retorna nada de proyecto B (verificado con test E2E)
- [ ] **Web fallback hit rate**: <10% de queries necesitan web (local es suficiente 90%+)

## Riesgos identificados

1. **Costo embeddings si usamos OpenAI** — mitigación: default all-MiniLM-L6-v2 local, OpenAI solo opt-in por proyecto
2. **Background indexing puede comerse CPU** — mitigación: throttle a 1 core, scheduled en horas de baja actividad
3. **FAISS namespace por proyecto a escala** — si >100 proyectos, switch a Qdrant cluster
4. **Tavily/Exa rate limits** — mitigación: cache local de web results por 24h en `~/.osquestador/cache/web/`
5. **Cold start con vault gigante (10k+ notas)** — mitigación: lazy load, top-K index primero, full index en background

---

## Próximo paso (esperando luz verde de Max)
- **Punto 2:** Sistema de anclaje de skills — repo `memoria` con índice de clasificación tipo bibliotecario, Osquestador inyecta skills paulatinamente a agentes conectados.

**¿Apruebas el Punto 1 + este apéndice del motor de búsqueda para que pase al Punto 2?**
