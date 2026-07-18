# Investigación 29 pasadas Obsidian + Graphiti (Deep-Dive)

**Pasadas totales**: 29 (15 Obsidian + 14 Graphiti)
**Commit**: pendiente
**Fecha**: 2026-07-08

---

## OBSIDIAN (15 pasadas)

### Pasada 1: Mobile 1.11 (enero 2026) — Mobile 2.0
- **Lock Screen + Control Center widgets** (iOS 18+): New note, Open note, Daily note, Search, Open Obsidian
- **Home Screen widgets** (Android+iOS): Create note, View note, Daily note
- **Siri + Shortcuts** integration: "Capture using Obsidian", "Capture to Obsidian", "Open my daily note in Obsidian", "Search in Obsidian"
- **Android Quick Settings Tile** (Android 7.0+) + new shortcuts (Android 7.1+)
- **Refreshed mobile UI**: navigation auto-hide on scroll, sidebar migrated to bottom, pull-down gesture reconfigurable
- **Haptics** added to toggles + checkboxes
- **Double-tap** switches reading mode → editing mode
- **Android usa Google Sans Flex** font
- **Dialogs smaller border-radius** en tablet
- **Plugin developers** pueden pedir user location (para Maps)
- **URL panes param**: `paneType=tab` | `split` | `window`
- **Settings search** por nombre y descripción
- **Keychain** integrado: API SecretStorage + SecretComponent para plugins compartir secrets (Google API token, OpenAI key) — sin copy-paste

### Pasada 2: Publish website
- **Built-in** en Obsidian (no es servicio aparte)
- **100% Lighthouse accessibility score** out of the box
- **Mobile-friendly** first-class
- **Edit from mobile** apps
- **SEO built-in** + customizable metadata (description, slug, image)
- **Custom domains** + Permalinks
- **Analytics** support
- **Custom CSS** via `publish.css` (ej: ocultar footer)
- **Collaboration** invite team
- **Multi-site** management
- **Status page**: status.obsidian.md

**Pain points comunidad** (forum):
- SEO subpar → mejorar discoverability
- Performance → chunked loading
- Social Customization → no customizable
- Mobile Publish missing graph view
- Sin comentarios integrados
- No comments system
- No analytics built-in

### Pasada 3: JotBird alternative publishing
- **Zero-friction** disposable web pages
- **Plugin + web service** combo
- **3 métodos** de publish: ribbon icon, command palette, context menu
- **Free anonymous**: links expiran 30 días
- **Free account**: dashboard + cross-device + 90 días expiration
- **Pro $29/año**: links permanent
- **Usa BRAT** (Beta Reviewer's Auto-Update Tool) para instalar plugins en queue

### Pasada 4: Desktop 1.11 (enero 2026)
- **Cookie encryption** enabled en installer
- **Markdown links en properties** + auto-update cuando se mueve/renombra file
- **Daily note format** selector predefinido
- **Filename sanitization** automático al importar
- **New commands**: "Copy path", "Copy current file path from system root"
- **Plugin updates** auto-check (cada 3 días o post-app update)
- **Default file to open** setting: Last opened / New note / Specific note / Daily note
- **Keychain settings** section
- **Markdown link conversion** al pegar URL sobre texto seleccionado
- **Electron 39.2.6** + Wayland default en Linux
- **Inter Variable font** bundled
- **`SettingGroup` API** + `SecretStorage`/`SecretComponent` API

### Pasada 5: 1.10.0 (octubre 2025) — Bases
- **Breaking**: "Use light mode"/"Use dark mode" commands eliminados → "Toggle light/dark mode"
- **Bases API initial** + muchas features nuevas
- **Group by** en Sort menu
- **Table summaries** (built-in o custom formula)
- **List view** (bullets + numbered) multiline
- **New Maps plugin** oficial open source (visualiza Bases en mapa)
- **Table selection** + full keyboard navigation
- **Copy/paste** + basic edit history (undo/redo)
- **Formulas nuevas**: `reduce()`, `html()`, `random()`
- **Timezone offset** en ISO 8601 datetime
- **View refresh** periódico de formulas stale (file.backlinks)
- **Modifier+ribbon click** = new tab / new split / new window
- **Indeterminate checkboxes** ordenados con `false`
- **"Switch view..."** command (antes "Change view")
- **Reading mode** Ctrl/Cmd-C copia full source si no hay selección
- **`open-link` event** fired en active element

### Pasada 6: Sync v1 collaboration
- **Real-time** updates across team devices
- **Shared vault** invite via email
- **End-to-end encryption** opcional (password required al join)
- **Max 20 collaborators** por vault
- **Max attachment size**: 5MB Standard / 200MB Plus
- **No live co-editing** mismo file (cursors not visible)
- **Conflict resolution** auto-merge + version history
- **Fine-grained permissions** not supported (todos owner-level menos invite)
- **No live multiplayer** aún (roadmap)
- **obsidian-headless client** (feb 2026) para sync sin GUI

### Pasada 7: Web Clipper browser extension
- **Reader mode** <50ms, limpia ads/banners/headers
- **Highlighter** block-level con yellow outline + click → highlight full block
- **YouTube transcripts** con chapter breakdown + timestamps
- **Defuddle** open source engine standalone (defuddle.md)
- **Mobile**: iOS (Orion browser) + Android (Kiwi)
- **Templates** + auto-apply por website
- **Keyboard shortcuts**
- **Variables** + Filters + Logic (conditionals, loops, set vars)
- **Highlighter export** JSON
- **3 vault config** + folders

### Pasada 8: Web Clipper UI 4 secciones
- **Header**: template switcher, more (variables), highlighter, reader, embed (PiP), settings
- **Properties**: metadata extraída → Obsidian Properties
- **Note content**: markdown preview
- **Footer**: vault dropdown, folder field, "Add to Obsidian" button, Interpreter (natural language)

### Pasada 9: Obsidian Web (Chrome extension alt)
- **Local REST API** plugin requirement
- **Templates** con Entry Details
- **Note Recall** — detecta si ya tienes notes sobre esa URL
- **Periodic Notes** support (daily/weekly/monthly/yearly)
- **Insert to specific section** en daily note

### Pasada 10: Mobile toolbar
- **Bottom toolbar** en mobile (en vez de top)
- **Customizable** con `Configure mobile toolbar`
- **Swipe left/right** para revelar más acciones
- **Global commands** addable (incluyendo "Change theme")
- **Default**: Add internal link, Add tag, etc.
- **Quick Action** pull-down gesture (default: open Command palette)
- **Mobile navigation bar**: back, forward, plus (new note), tab count, menu
- **No Ribbon en mobile** (reemplazado por menu)
- **Toggle keyboard** toggle option en toolbar
- **Tablet**: toolbar center aligned

### Pasada 11: Canvas core plugin
- **JSON Canvas format** open spec (portable, Git-friendly)
- **3 creation methods**: ribbon icon, command palette, folder right-click
- **Cards**: text (Markdown), note (live preview), media (images/PDFs/audio/video)
- **Drag from File Explorer** o drag a folder
- **Drag-and-drop from outside** (webpage image, desktop file)
- **Edges**: drag from card edge (filled dot) to another card
- **Edge features**: label (double-click), direction (none/one-way/bidirectional), color
- **Right-click on edge** → delete or jump
- **Groups**: right-click "Create group" o select+group
- **Pan**: Space+drag, middle mouse, two-finger trackpad
- **Zoom**: Ctrl/Cmd+scroll, pinch, + / - buttons
- **Zoom to fit** (maximize icon)
- **JSON Canvas spec** abierto y portable

### Pasada 12: Canvas Bases plugin
- **Canvas-style layout para Obsidian Bases**
- **Live board edges** (wikilinks, properties, all)
- **JSON Canvas export**
- **Draggable, resizable file cards** + group frames + relationship edges + assignment zones
- **TaskNotes integration** (dependency/subtask edges)
- **Manual cards/groups** preservados al regenerar
- **Stable Canvas-owned node IDs**
- **Configurable properties** edge names (`depends_on, related`)

### Pasada 13: Properties UI (v1.4+)
- **Visual interface** sobre YAML frontmatter
- **Property types**: text, list, number, checkbox, date, date+time
- **Auto-infer** type from value (date → date type)
- **Cmd/Ctrl+;** shortcut para add property
- **All Properties panel** (right sidebar) con count por property
- **Rename property across vault** desde All Properties panel
- **Source mode** toggle: visible / source / hidden
- **3 modes**: source (raw), hidden, visible (UI panel)
- **Default Tags property** built-in
- **Multi-line list values** con X para remove
- **Date picker** en date property
- **Property type change** retroactivo (puede romper data)
- **Type per name** (key=type) across vault
- **Settings > Editor > Properties in document** controla display

### Pasada 14: Roadmap 2026
- **In flight**: Kanban view para Bases, Obsidian for Work, Settings search, Background Sync mobile, Bases para Publish, Calendar view, Canvas support Publish, Multiplayer, Open individual .md, PDF annotation, Sort search por relevance
- **Launched may 2026**: Community directory + automated review
- **Launched mar 2026**: Obsidian Reader (distraction-free)
- **Launched feb 2026**: Headless client Sync, Template logic Web Clipper, **Obsidian CLI** ← KEY
- **Launched jan 2026**: Siri+Shortcuts, Mobile widgets, Mobile UI refresh, **Keychain**

### Pasada 15: Bases API details
- **Initial Bases API** en 1.10
- **Group by** + table summaries + List view
- **New view types** via plugin (ej: Maps)
- **Filters**, **sorting**, **grouping**, **visible properties** en `.base` file
- **Edit history** undo/redo
- **Multi-line** content
- **HTML render** via `html()` function
- **`random()`** function para sort randomization
- **List view** con bullets/numbered

---

## GRAPHITI (14 pasadas)

### Pasada 1: Production deployment
- **Median latency**: good
- **p99 latency**: fine
- **Cost-per-request**: competitive, contingente en deployment model
- **Self-hosted**: control + unpredictable ops cost
- **Managed**: predictability + vendor-priced ceiling
- **Break-even**: ~half-FTE ops cost
- **<100k req/day**: managed wins
- **>1M req/day**: self-hosted makes sense
- **3 traits equipos exitosos**:
  1. Instrument cost desde día 1
  2. Cache agresivo multi-layer
  3. Single primary model, no mezclar expensive ones

### Pasada 2: API decoupled (FastAPI wrap)
- **graphiti-core** library inestable en async apps
- **Process isolation** = solución
- **FastAPI service standalone** wrap todo
- **Microservice architecture**:
  - Independent scaling (CPU-bound agent vs I/O-bound graph)
  - Multiple agent instances contra single graph service
  - Technology-agnostic API boundary
  - Asyncio event loop conflicts solved

### Pasada 3: Performance tuning
- **SEMAPHORE_LIMIT** critical setting
- **MCP server default**: 10
- **Core library default**: 20
- **Por LLM provider tier**:
  - OpenAI Tier 1 (3 RPM) → 1
  - OpenAI Tier 2 (60 RPM) → 5
  - OpenAI Tier 3 (500 RPM) → 10
  - OpenAI Tier 4 (5K RPM) → 30
  - OpenAI Tier 5 (10K+ RPM) → 50
  - Anthropic default (50 RPM) → 5
  - Anthropic mid (500 RPM) → 15
  - Anthropic high (1K+ RPM) → 30
  - Azure → 10-20
  - Ollama CPU → 2
  - Ollama GPU → 5
  - Groq → 30-50
- **Neo4j heap**: 50% RAM max 32GB
- **Neo4j page cache**: remaining RAM
- **Vector indices** for embeddings (1536 dim cosine)
- **Fulltext search** indices
- **Property indices**: uuid, group_id, created_at
- **PROFILE query** to identify bottlenecks
- **Redis maxmemory** 8gb LRU
- **Kuzu driver** SSD path + max_concurrent_queries
- **CHUNK_TOKEN_SIZE** default 3000, overlap 200, min 1000
- **ENTITY_DENSITY_THRESHOLD** 0.15
- **Horizontal scaling** via Kubernetes replicas

### Pasada 4: MCP Server 1.0 (20K stars)
- **Multi-provider support**
- **YAML configuration** replaces env vars
- **Health check endpoints** para Docker + load balancers
- **Single container stack** con FalkorDB bundled
- **Neo4j** sigue siendo separate docker-compose
- **Neo4j team assisted** con query optimization

### Pasada 5: MCP-Graphiti deep dive
- **Decoupled API** architectural pattern = critical insight
- **asyncio event loop conflicts** solved por process isolation
- **FastAPI standalone wrapper** = best practice
- **Microservice architecture**:
  - Independent scaling
  - Multiple agent instances vs single graph service
  - Cost-effective + responsive
- **Setup steps**:
  - Docker + Compose
  - Neo4j or FalkorDB
  - uv for Python deps
  - LLM API key (default OpenAI)
- **Run**:
  - Local: `uv run graphiti_mcp_server.py --transport sse`
  - Docker: `docker compose up`
- **Common errors**:
  - LLM 429 → lower SEMAPHORE_LIMIT
  - Verify .env vars (NEO4J_URI, password, OPENAI_API_KEY)
  - Run `graphiti_mcp_server.py` not other FastAPI app

### Pasada 6: Memory architecture comparison
- **Mem0**:
  - Hybrid: vector + property graph + KV
  - Two-phase: extract (LLM) + retrieve (fuse semantic+keyword+entity)
  - LOCOMO 92.5 / LongMemEval 94.4 / BEAM, ~7K tokens/retrieval
  - Managed cloud, free tier, $249/mo Pro para graph
- **Zep/Graphiti**:
  - Temporal knowledge graph
  - Bi-temporal: valid time + transaction time
  - Superseded facts marked, not deleted
  - Hybrid: embeddings + BM25 + graph traversal
  - Episodes con provenance
  - Deep Memory Retrieval 94.8% (vs 93.4 MemGPT)
  - LongMemEval +18.5% vs full context
  - 90% latency reduction
- **Letta (MemGPT)**:
  - Stateful agents platform
  - Memory blocks (labeled text in context, editable)
  - Archival memory (searchable, query on demand)
  - Agent self-edits memory
  - 3 tiers: core (RAM) / recall (search) / archival (cold)
  - LongMemEval 83.2%

### Pasada 7: Memory framework ranking 2026
- **Mem0**: best general-purpose, 66.9% LOCOMO, 0.71s median, 1800 tokens
- **Mem0g** (graph variant): 68.4% LOCOMO, 1.09s latency
- **Full context baseline**: 72.9% / 9.87s / 26K tokens
- **Zep/Graphiti**: 63.8% LongMemEval vs Mem0 49% = 15-pt gap on temporal
- **Letta**: LongMemEval 83.2% overall
- **Cognee**: best unstructured-document ingestion
- **LangMem**: best para LangChain teams
- **Pattern taxonomy**:
  - Vector-only (fast, simple, weak temporal)
  - Vector + knowledge graph (better multi-hop, "what changed when")
  - Tiered agent-managed (flexible, harder to reason)

### Pasada 8: Picking framework
- **Graphiti**: cuando el agente necesita razonar sobre cómo los hechos cambiaron en el tiempo
- **Mem0**: cuando necesitas retrieve contexto correcto barato a escala
- **Letta**: para long-horizon agent-managed memory
- **No single benchmark comparable** entre vendors 2026
- **LOCOMO**: ~300 turns hasta 35 sessions, single/multi-hop/temporal/adversarial
- **LongMemEval**: 500 questions IE/multi-session/temporal/knowledge updates/abstention, ~30% drop en sustained interaction

### Pasada 9: Mem0 vs Zep vs Letta deep
- **Mem0 tokens/retrieval**: ~7K vs 25K+ full context
- **Zep scores higher en temporal** (acknowledged by Mem0 team)
- **Mem0 wins on token efficiency + ecosystem breadth** (acknowledged by Zep team)
- **Letta = RAM/disk OS model**
- **Multi-hop benchmark**:
  - Mem0 66.9% LLM-as-judge
  - Mem0g 68.4% (1.5pt improvement)
  - Graphiti/Zep wins on temporal questions

### Pasada 10: Production metrics
- **100k-user agent product**: $low-to-mid 4-figures monthly (embedding API + vector storage)
- **Strict tenant isolation**:
  - Memory records keyed by user_id
  - Recall query filters enforced at storage layer
  - Multi-tenant bugs silent + dangerous
  - Tests prove isolation, not code review
- **Cost optimization traits**:
  - Instrument cost from day 1
  - Cache aggressive multi-layer
  - Single primary model (not mix of expensive)

### Pasada 11: Zep paper benchmarks
- **Deep Memory Retrieval**: Graphiti 94.8% vs MemGPT 93.4%
- **LongMemEval temporal-reasoning slice**: Graphiti +15pts vs Mem0
- **Accuracy gain**: 18.5% vs full context
- **Latency reduction**: 90% vs full context
- **LOCOMO**: 92.5%
- **LongMemEval**: 94.4%
- **BEAM scores**: included
- **Token usage**: ~7K per retrieval

### Pasada 12: Spraypaint JS Client
- **Isomorphic, framework-agnostic** Graphiti ORM
- **Fetch underneath** → polyfill recomendado
- **TypeScript >=2.8** supported
- **Strict Class Initialization** workaround: `"strictPropertyInitialization": false`
- **URL pattern**: `baseUrl + apiNamespace + jsonapiType`
- ⚠️ **NOTA**: Este es un Graphiti **diferente** (orm de jsonapi) vs el de Zep (knowledge graph). Mismo nombre, distinto producto.

### Pasada 13: Graphiti (Zep) SDK comparison
- **Zep** (commercial) tiene Dashboard + debug logs + API logs + SDKs Python/TypeScript/Go
- **Graphiti** (OSS) build your own tools
- **Spraypaint** (graphiti.dev) es **OTRO** Graphiti (JSONAPI ORM)

### Pasada 14: Graphiti MCP integration con Claude Desktop
- **Config path**:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- **3 setup options**:
  1. Local Docker (ghcr.io/github/github-mcp-server)
  2. SSE gateway (mcp-remote package)
  3. Native integration (Settings > Integrations)
- **Graphiti MCP server**:
  - `git clone https://github.com/getzep/graphiti`
  - `cd graphiti/mcp_server`
  - `docker-compose up` (FalkorDB + browser UI + Graphiti MCP)
  - SSE endpoint: `http://localhost:8000/sse`
  - Claude Desktop: usa `mcp-remote` gateway (no soporta SSE nativo)
- **Cursor IDE config**:
  ```json
  {
    "mcpServers": {
      "graphiti-memory": {
        "url": "http://localhost:8000/sse"
      }
    }
  }
  ```
- **Logs**: `~/Library/Logs/Claude/mcp.log`
- **CORS**: localhost puede ser bloqueado, usar ngrok o Cloudflare Tunnel

---

## DECISIONES DERIVADAS (D33-D37)

### D33: Stack de plugins Obsidian a integrar en panel
- **JSON Canvas** spec nativo (open, portable, Git-friendly) → render nativo en panel Osquestador
- **Web Clipper templates** (4-section UI) → nuestro `/selectFiles` lo imita
- **Keychain API** → usar para store API keys centralizado (no copy-paste entre plugins)
- **Bases API** → integrar filter/sort/group/view (table, list, maps, calendar)
- **Sync headless** → nuestro `obsidian-headless` para background sync del vault del proyecto
- **Mobile UI patterns** → sidebar bottom + pull-down gesture (mobile-friendly)

### D34: Production deployment Graphiti en nuestro Osquestador
- **Self-hosted** (vps 95.111.232.89, es <100k req/day → managed sería overkill)
- **FalkorDB** single container (más simple que Neo4j separado)
- **SEMAPHORE_LIMIT=5** (mix de providers + rate limits tier 2-3)
- **FastAPI wrapper** standalone con `/add_episode`, `/search`, `/search_graph` endpoints
- **Health check** endpoint `/health` para watchdog
- **CHUNK_TOKEN_SIZE=3000** default
- **Vector index** FalkorDB embedding dimension 384 (MiniLM-L6-v2)
- **Tenant isolation** desde día 1 (group_id = project_id, filter enforced en storage)
- **Cost instrumentation** por proyecto (token tracking, embedding spend)

### D35: Memory architecture híbrida
- **Graphiti (Zep OSS)** = long-term temporal knowledge graph (FalkorDB)
- **Mem0** no necesario (overlap con Graphiti, sería doble costo)
- **Letta** no necesario (overlap con Graphiti + complexity)
- **SQLite WAL + FTS5** = conversation history search (verbatim + summary)
- **FAISS MiniLM-L6-v2** = fast semantic search local (384-dim)
- **Triple layer**:
  1. Hot: SQLite WAL verbatim (<500 tokens)
  2. Warm: SQLite summaries (1-3K tokens) + FAISS embeddings
  3. Cold: Graphiti knowledge graph + GitHub repo (osquestador-memoria)

### D36: Adopción Canvas + Bases spec
- **JSON Canvas format** 1.0 spec → renderizar `.canvas` en panel Osquestador (nodos + edges + grupos)
- **Bases API patterns** → nuestro panel filter/sort/group con `.base` file format
- **Edge features**: label + direction + color (semantic relationships)
- **Group frames** para organizar secciones
- **Pan/Zoom/Zoom-to-fit** idéntico UX
- **Cards**: text, note, media (drag-drop)

### D37: Integración MCP-Graphiti con nuestro Orquestador
- **3 transports** soportados: stdio (Claude Desktop) / SSE (Cursor) / HTTP (nuestro panel)
- **Decoupled FastAPI** wrap graphiti-core (best practice production)
- **Endpoint HTTP** propio: `http://localhost:8000` con auth
- **No usar mcp-remote gateway** (nativo es más simple)
- **Container único** FalkorDB + Graphiti MCP
- **Logs centralizados** vía nuestro sistema (no `~/Library/Logs/Claude/`)

---

## TOTAL INVESTIGACIÓN ACUMULADA OSQUESTADOR
- **~280+ búsquedas** comunidad devs (29 nuevas en este turno)
- **+5 features input-block** integrados
- **+5 decisiones** (D33-D37)
- **5 patterns nuevos Obsidian**: Widgets/Siri/Canvas/Bases/Keychain
- **5 patterns nuevos Graphiti**: Temporal KG/Decoupled API/Performance tuning/MCP/Hybrid memory
- **Total decisiones**: D1-D37 (37 decisiones arquitectónicas)
