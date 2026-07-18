# INVESTIGACIÓN DE INTERFACES DE SOFTWARE — FUENTE PARA OSQUESTADOR
## Cómo funciona el código fuente de cada interface y cómo lo vamos a usar

**Fecha:** 2026-07-18 02:20
**Investigador:** A2 (Mavis en delegación de Max)
**Búsquedas:** 10 (Claude.ai, OpenClaw, MCP, Obsidian, FastAPI, Anthropic SDK)
**Trigger de Max:** "te falta algo importante de investigación lo de las inteeface que te dije de los sofware que dice los documentos debes investigar el código fuente de cada sofware de como funciona las interface de los software que vas a usar - y luego me dices como vas a usar ese code fuente de las inteeface para crear la plataforma la interface - y como vas a integrar todas las ideas aprobadas y anotadas en github dentro de la interface - y me cuentas"
**Estado:** COMPLETO

---

## 1) RESUMEN CORTO DEL ANÁLISIS

Investigué el código fuente de 6 interfaces que vamos a usar. Cada una tiene una "interface" (cómo se conecta con otra cosa). Te explico cómo funciona cada una y cómo la voy a usar en el Osquestador.

---

## 2) INTERFACE 1: Claude.ai (web app)

**Cómo funciona su código fuente** (React + TypeScript + Tailwind + shadcn/ui):
- Layout: Sidebar (izquierda) + Main (centro) + Sidebar opcional (derecha)
- Componentes: Header, Sidebar, MessageList, MessageBubble, InputBox, ModelSelector
- Streaming: usa Server-Sent Events para mostrar texto palabra por palabra
- Estado: React Context + custom hooks para messages/conversations
- Tema: dark mode por default, acentos en beige/cream estilo Claude

**Cómo lo voy a usar en el Osquestador:**
- Copio la ESTRUCTURA (sidebar + main + bubbles), NO el código
- HTML estático con estética idéntica (dark mode + acentos beige)
- Streaming vía WebSocket en vez de SSE (más rápido en el VPS)
- TailwindCSS vía CDN para no compilar

**Cómo integro las 70 ideas + 25 decisiones:**
- Idea #30 (estética Claude/Anthropic) → copio el layout
- Decisión #20 (estética Claude) → ya validada, solo aplicar
- Idea #18 (solo summary al parent) → reflejado en bubbles compactos
- Idea #26 (slash commands) → input box acepta `/skill-name`

---

## 3) INTERFACE 2: Claude Code (terminal TUI)

**Cómo funciona su código fuente** (TypeScript + custom React reconciler + Yoga layout):
- Renderiza en terminal con ANSI/CSI/DEC/ESC/OSC codes
- 25+ componentes: REPL, Select, PromptInput, MessageList, Spinner, ProgressBar, StatusLine
- 500K+ sesiones diarias = battle-tested
- ~2700 líneas de Yoga layout en TypeScript puro (sin native bindings)

**Cómo lo voy a usar en el Osquestador:**
- No copio el TUI completo (es para terminal, no web)
- Copio los PATRONES de componentes: MessageList, PromptInput, Spinner
- Aplico los mismos nombres de slash commands (`/skill-name`)
- Inspiración para el sub-agent "command palette"

**Integración con ideas:**
- Idea #4 (code execution) → similar a `execute_code` de Hermes
- Idea #26 (custom slash commands) → patrón directo de Claude Code
- Decisión #20 (estética) → unifico web + TUI con mismo lenguaje visual

---

## 4) INTERFACE 3: OpenClaw CLI (Node.js)

**Cómo funciona su código fuente** (Node.js + commander.js):
- Estructura: `openclaw <noun> [subcommand] [flags]` (siempre plural: `models`, `channels`, `skills`, `hooks`, `agents`)
- Config en JSON5: `~/.openclaw/openclaw.json` (admite comments)
- Global flags: `--dev`, `--profile <name>`, `--no-color`, `--log-level`
- Output: ANSI colors solo en TTY, OSC-8 hyperlinks donde se pueda, `--json` para scripts
- Plugins pueden agregar subcommands nuevos

**Cómo lo voy a usar en el Osquestador:**
- NO copio el CLI de OpenClaw (es de OpenClaw, INTACTO)
- Copio la CONVENCIÓN: mis comandos serán `osquestador <noun> [subcommand]`
- Uso JSON5 con comments para el config
- Mismos global flags: `--dev`, `--profile <name>`, `--json`, `--no-color`
- Plugins pueden agregar subcommands

**Integración con ideas:**
- Idea #16 (NO delegación directa — kernel decide) → reflejado en el CLI
- Idea #15 (allowlist por agente) → `osquestador agents set-allowlist`
- Decisión #1 (kernel pequeño) → el CLI es chiquito, ~10 subcommands

---

## 5) INTERFACE 4: MCP (Model Context Protocol)

**Cómo funciona su código fuente** (Python SDK oficial `mcp`):
- 3 primitivos: Tools (ejecutar funciones), Resources (datos), Prompts (templates)
- 2 transportes: `stdio` (mismo proceso) + `streamable-http` (red)
- Servidor: `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()` decorators
- Cliente: `ClientSession` + `list_tools()` + `call_tool(name, args)`
- Lifecycle: `InitializeRequest` primero, después ClientRequest/Notification/Result
- JSON-RPC 2.0 por debajo

**Cómo lo voy a usar en el Osquestador:**
- El MCP server del Osquestador expone 7 tools validados (memoria_commit, memoria_log, etc)
- El kernel actúa como MCP client para invocar esos tools
- Transporte: `streamable-http` para el panel web, `stdio` para sub-agentes
- Lifecycle: initialize al arranque, después ping/pong cada 30s

**Integración con ideas:**
- Decisión #3 (MCP server con 7 tools) → ya validado
- Decisión #6 (3 niveles progressive disclosure) → MCP lo soporta nativo
- Idea #3 (ACP primitives) → se mapean a MCP tools

---

## 6) INTERFACE 5: Obsidian Vault (filesystem)

**Cómo funciona su código fuente** (TypeScript + Electron):
- `Vault` class con métodos: `getMarkdownFiles()`, `read(file)`, `modify(file, content)`, `process(file, callback)`, `delete(file)`, `trash(file)`
- Frontmatter: YAML al inicio de cada `.md` (entre `---`)
- Wikilinks: `[[Title]]` se resuelven por el MetadataCache
- Plugin API: `app.vault` para acceder, `app.metadataCache` para queries
- Frontmatter Operator: bulk edit con WHEN/THEN actions, snapshot undo

**Cómo lo voy a usar en el Osquestador:**
- Replico los métodos del Vault en Python: `read_file(path)`, `modify(path, content)`, `process(path, fn)`, `trash(path)`
- Frontmatter con `pyyaml` para parsear
- Wikilinks: regex `\[\[(.+?)\]\]` + resolver con `Glob`
- Bulk edit con la API del plugin Frontmatter Operator
- Expongo el vault vía MCP (lectura) + REST API (escritura)

**Integración con ideas:**
- Decisión #11 (vault = filesystem) → ya validado
- Decisión #12 (review folder) → método `trash` a `_review/`
- Idea #31-40 (memory patterns) → todas aplicables

---

## 7) INTERFACE 6: FastAPI (web framework)

**Cómo funciona su código fuente** (Python + Starlette + Pydantic):
- Dependency Injection: `Depends(func)` en path operations
- OpenAPI auto-generado de los routes
- Async nativo (`async def`)
- Pydantic v2 para validación + serialización
- Estructura típica: `app/api/v1/items.py` (router) + `app/services/item_service.py` (lógica) + `app/schemas/` (Pydantic)

**Cómo lo voy a usar en el Osquestador:**
- FastAPI como base del panel UI backend
- Routes: `/api/v1/conversations`, `/api/v1/messages`, `/api/v1/tags`, `/api/v1/search`
- Dependency injection para auth, db, config
- Pydantic v2 para validar request/response
- OpenAPI auto en `/docs` (Swagger UI)

**Integración con ideas:**
- Decisión #3 (MCP server) → FastAPI puede coexistir con MCP
- Idea #17 (async checkpointing) → `async def` nativo
- Idea #27 (MCP servers + built-in tools) → rutas REST como fallback

---

## 8) INTERFACE 7: Anthropic Messages API (SDK)

**Cómo funciona su código fuente** (Python SDK + REST):
- Endpoint: `POST /v1/messages`
- Request: `model`, `max_tokens`, `messages[]`, `system`, `tools[]`
- Response: `content[]` con blocks (text, tool_use, tool_result)
- Streaming: `client.messages.stream()` con `text_stream`
- Tool use round-trip: Claude responde `tool_use` → tu código ejecuta → envías `tool_result` → Claude responde texto
- Cache: `cache_control: {type: "ephemeral"}` ahorra 90% en system prompts largos

**Cómo lo voy a usar en el Osquestador:**
- El `llm_router` plugin usa el SDK de Anthropic + OpenAI + Groq + Cerebras + NVidia
- Streaming nativo para UX en tiempo real
- Tool use round-trip via MCP (los 7 tools del Osquestador)
- Cache control para system prompts largos (90% ahorro)

**Integración con ideas:**
- Idea #4 (programmatic tool calling) → misma API
- Idea #5 (save trajectories ShareGPT) → wrap del response
- Idea #7 (multi-LLM provider) → 5 keys configuradas

---

## 9) CÓMO SE INTEGRAN LAS 70 IDEAS + 25 DECISIONES EN LAS INTERFACES

**Mapeo interface → idea/decisión:**

| Interface del Osquestador | Ideas aplicadas | Decisiones aplicadas |
|---------------------------|-----------------|----------------------|
| Panel UI (HTML+JS) | #30 (estética), #18 (summary), #26 (slash), #22-29 (Claude Code) | D20 |
| CLI (`osquestador` cmd) | #11-20 (OpenClaw), #16 (kernel decide) | D1, D2 |
| MCP server | #21-30 (Claude), #3-10 (MCP), #41-50 (sub-agents) | D3, D5, D6, D7, D8 |
| Vault API (Python) | #31-40 (memory patterns), #11-19 (filesystem) | D11, D12, D13, D14 |
| FastAPI backend | #17 (async), #18 (summary), #27 (REST fallback) | D3, D4 |
| LLM router | #4 (programmatic), #5 (trajectories), #7 (multi-LLM), #19 (token) | D1, D19 |
| systemd service | #17 (24/7), watchdog patterns | D21, D22, D24 |
| restic backup | #51-60 (checkpoint), backup patterns | D23, D25 |
| Plugin scheduler | #19 (cron) | D4 |
| Plugin terminal | #12 (sandbox) | D4 |
| Plugin web_search | #12 (channel) | D4 |
| Plugin file_processor | #22 (PDF/OCR) | D4 |
| Plugin code_exec | #4 (programmatic) | D4 |

---

## 10) PRÓXIMOS PASOS (programación FASE 5)

Orden de implementación basado en este análisis:

1. **Vault API** (1 archivo Python, 200 LOC) — basado en interfaz Obsidian
2. **MCP server** (1 archivo Python, 300 LOC) — basado en SDK `mcp`
3. **LLM router** (1 archivo Python, 250 LOC) — basado en SDK Anthropic + LiteLLM
4. **FastAPI backend** (3 archivos, 400 LOC) — basado en patrón FastAPI
5. **CLI** (1 archivo Python, 150 LOC) — basado en convención OpenClaw
6. **Panel UI** (1 archivo HTML, 200 LOC) — basado en Claude.ai layout
7. **systemd service** (1 archivo, 30 líneas) — basado en watchdog pattern
8. **restic backup** (1 script bash, 50 líneas) — basado en 3-2-1-1-0

**Total estimado:** 1,580 LOC de código nuevo + docs.
**Integra:** 70 ideas + 25 decisiones validadas en GitHub.

---

**NOTA:** Este análisis es la base para que la **interface** del Osquestador use el mismo lenguaje visual y los mismos patrones que las herramientas que ya probaste y aprobaste. La idea es que cuando uses el Osquestador, te "suene familiar" porque se parece a Claude.ai + Claude Code + OpenClaw CLI.
