# INVESTIGACIÓN COMUNITARIA V2 — PUNTO 3
## Capability Advertisement / Handshake Protocol — El Osquestador informa al agente qué funciones tiene al conectarse

**Fecha:** 2026-07-18
**Investigador:** A2 (Mavis en delegación de Max)
**Búsquedas realizadas:** 10
**Trigger literal de Max:** "el Osquestador también podría buscar skills... informa al agente qué funciones tiene disponibles al conectarse"
**Estado:** COMPLETO — listo para revisión de Max antes de pasar al Punto 4

---

## Pregunta de Max
> "El Osquestador también podría buscar skills en al web en una lista de muchos lugares diferentes y descargar según la necesidad... informa al agente qué funciones tiene disponibles al conectarse"

## Síntesis ejecutiva (5 bullets)
1. **El patrón A2A Agent Card (Google, abril 2025) es el estándar de facto** — JSON descriptor en `/.well-known/agent.json` con name, description, version, capabilities, skills[], authentication. Es lo que la comunidad ya implementa (Google A2A, AIsa, Agentium, AgentPatterns).
2. **MCP tiene su propio handshake** (`initialize` → `notifications/initialized`) con protocolVersion, capabilities, clientInfo/serverInfo. El Osquestador hereda este patrón y lo extiende con su propio `osquestador://hello` que incluye: agent_id, project_id, skills_catalog, search_engine_ready, scratchpad_vacío, capabilities detalladas.
3. **ACAP (IETF draft) + ATN (Agent Trust Negotiation) son los estándares formales** — capability manifest firmado JWS, well-known URI, 3 operaciones (GET/PUT/POST query), 4 artefactos (Capability Manifest, Delegation Chain, Provenance Attestation, Session Receipt). Nuestro handshake hereda este patrón pero no requiere firma criptográfica en V1 (opt-in por Max).
4. **AHP (Agent Handshake Protocol) es la opción web-friendly** — `/.well-known/agent.json` + HTTP `Link` header + `Accept: application/agent+json`. Funciona con HTTP simple, no requiere WebSocket. El Osquestador puede usar este patrón en su endpoint HTTP y el patrón WebSocket/MCP para conexiones live.
5. **El handshake debe ser 3-fases deterministico** — confirmado por MCP spec + A2A + AHP: (1) Discovery: cliente → server capabilities; (2) Negotiation: protocol version + scope + auth; (3) Session: ready + tokens + audit. El Osquestador implementa las 3 con código determinístico (JSON Schema validation), LLM solo si hay ambigüedad semántica.

---

## Evidencia cruda (10 búsquedas)

### Búsqueda 1 — `agent handshake protocol capability advertisement manifest well-known URI JSON-RPC`
**Fuentes:** agenthandshake.dev (AHP), agenthandshake.dev/whitepaper, ietf.org (ATN), ietf.org (agent://), ietf.org (ACAP)
**Hallazgo clave (3 protocolos hermanos):**
- **AHP (Agent Handshake Protocol):** site publica machine-readable manifest en `/.well-known/agent.json`. 3 discovery mechanisms: well-known URI (MUST) + HTTP Link header + Accept header. Manifest declara capabilities + content URL. 3 modos: MODE1 (read-only stateless) / MODE2 (conversational POST /agent/converse) / MODE3 (agentic delegation)
- **ATN (Agent Trust Negotiation, IETF):** 4 artefactos firmados JWS: (1) Capability Manifest, (2) Delegation Chain, (3) Provenance Attestation, (4) Session Receipt. Handshake state machine de 6 pasos. **"Discovery answers where and who. Application protocols (MCP, A2A) answer how. Nothing in the current stack answers what may we do together, and what evidence will remain. ATN fills that gap."**
- **ACAP (IETF draft-zahed-acap-00):** HTTP/3 well-known URI, 3 operaciones (GET retrieve / PUT register / POST query by capability), ACD firmado JWT. Inspira en RFC 8615 (well-known) y WebFinger
- **agent:// URI scheme (IETF draft-narvaneni):** "Agent Descriptor (agent.json) - machine-readable document describing identity, capabilities, behavior". Compatible con Agent2Agent. `.well-known/agent.json` para single-agent, `.well-known/agents.json` para multi-agent

**Aplicación al Osquestador:**
- Implementa `.well-known/agent.json` (estándar A2A) Y `.well-known/osquestador.json` (extensión propia con skills catalog + project_id)
- Sigue patrón AHP con 3 discovery mechanisms
- Sigue patrón MCP para handshake live

### Búsqueda 2 — `Agent Capability Advertisement Protocol ACAP registry discovery IETF standard`
**Fuentes:** ietf.org (ACAP), datatracker.ietf.org (RFC 6075, ARDP, draft-pioli)
**Hallazgo clave:**
- **ACAP** ya está en draft IETF (draft-zahed-acap-00). **"ACAP enables the discovery of AI agents deployed across different administrative domains on the Internet. Each agent exposes an ACAP endpoint, hosted at a well-known URI, that serves ACDs describing the capabilities, authentication requirements, and operational metadata for agents within that domain."**
- Well-known URI: `https://{domain}/.well-known/agents[/{agent-local-id}]/acap`
- Query endpoint: `https://{domain}/.well-known/agents/_query`
- **ARDP** (Agent Registration and Discovery Protocol) es otro draft complementario
- **RFC 6075** es la base histórica (ACAP = Application Configuration Access Protocol, IANA registry)

**Aplicación al Osquestador:** El endpoint HTTP del Osquestador sigue este patrón. Si en el futuro queremos exponer el Osquestador a otros agentes externos (no solo los internos de Max), ya cumplimos con el estándar IETF.

### Búsqueda 3 — `MCP initialize handshake protocol version negotiation capabilities client server`
**Fuentes:** modelcontextprotocol.io (Versioning), imti.co (Handshake), apxml.com (Capabilities Negotiation), cbruyndoncx.github.io (MCP Lifecycle), youtube.com (MCP Initialize Flow)
**Hallazgo clave (oro puro — ESTE ES EL PATRÓN EXACTO):**
- **MCP handshake es 3-pasos determinístico:**
  1. **Client → Server: `initialize`** con `protocolVersion`, `capabilities`, `clientInfo` (name, version)
  2. **Server → Client: result** con `protocolVersion` (acordado), `capabilities` (del server), `serverInfo` (name, version), `instructions` (opcional, hints)
  3. **Client → Server: `notifications/initialized`** (parameter-less, confirma aceptación)
- **Modern (post 2026-07-28):** per-request metadata, no negotiation handshake
- **Legacy (pre 2025-11-25):** `initialize` handshake obligatorio
- **Server MUST implement `server/discover`** (Modern) o client MAY call para aprender versiones up front
- **Capabilities intercambiadas:**
  - **Client:** `sampling` (allows server to request LLM completions), `roots` (filesystem roots), `experimental`
  - **Server:** `logging` (emit log messages), `prompts` (prompt templates), `resources` (data resources, con `subscribe`), `tools` (executable functions)
- **"The word 'negotiation' is slightly misleading. Each side declares what it will accept being asked for, and the declarations are complementary."**

**Aplicación DIRECTA al Osquestador (mapeo 1:1):**
```json
// Cliente (agente o chat) → Osquestador
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2026-07-18",
    "clientInfo": {"name": "claude-code", "version": "1.0.0"},
    "capabilities": {
      "sampling": true,
      "roots": true
    }
  }
}

// Osquestador → Cliente
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2026-07-18",
    "serverInfo": {"name": "osquestador", "version": "1.0.0"},
    "capabilities": {
      "tools": {"listChanged": true},
      "resources": {"subscribe": true, "listChanged": true},
      "logging": true,
      "prompts": {"listChanged": true},
      "osquestador_extensions": {
        "skills": true,
        "search_engine": true,
        "memory_tiers": ["HOT", "WARM", "COLD"],
        "projects": true
      }
    },
    "instructions": "Osquestador is the kernel. It exposes MCP tools, manages projects, and provides persistent memory. Skills load progressively. Search engine auto-activates on each prompt."
  }
}
```

### Búsqueda 4 — `agent hello announce capabilities on connect WebSocket JSON-RPC welcome message`
**Fuentes:** agentclientprotocol.com (Streamable HTTP & WebSocket), jsonrpc.org (spec), github.com (rpc-ws), mongoose.ws (JSON-RPC over WebSocket)
**Hallazgo clave:**
- **ACP (Agent Client Protocol) usa `Acp-Connection-Id`** header en HTTP + `sessionId` en JSON-RPC params (connection-scoped vs session-scoped)
- **JSON-RPC 2.0 spec:** transport-agnostic, soporta WebSocket nativamente, frames con `id` = request, sin `id` = notification
- **WebSocket chat pattern:** client se conecta → server asigna ID → server envía `{type: "connection", clientId, message: "Connected"}` (welcome message)
- **Notification pattern:** frames sin `id` se consideran notifications, no esperan respuesta

**Aplicación al Osquestador:**
- En WS: al aceptar conexión, Osquestador envía inmediatamente una notification `{type: "osquestador/hello", session_id, project_id, capabilities, skills_catalog_short, search_engine_status}`
- En HTTP+MCP: usa el patrón `initialize`/`initialized` clásico
- En ambos casos, el primer mensaje del server es siempre el advertisement de capabilities

### Búsqueda 5 — `OpenAPI JSON-RPC service description auto-generate tools API discovery contract`
**Fuentes:** spec.open-rpc.org (OpenRPC), openapi.tools, open-rpc.org/docs, apievangelist.com
**Hallazgo clave:**
- **OpenRPC = "OpenAPI for JSON-RPC"** — standard para describir JSON-RPC APIs. Trusted por Ethereum Foundation, MetaMask, Chainlink, Filecoin
- **Service discovery method:** `rpc.discover` (MUST, retorna OpenRPC schema)
- **Use cases:** interactive documentation, code generation for documentation/clients/servers, automation of test cases
- **Optic (open source):** genera OpenAPI definitions automáticamente del tráfico proxied

**Aplicación al Osquestador:**
- El Osquestador expone `osquestador://rpc.discover` que retorna OpenRPC schema de todos los tools
- Permite a clientes generar código automáticamente para usar el Osquestador
- Compatible con cualquier SDK OpenRPC existente

### Búsqueda 6 — `agent skills auto activate description trigger on connect system prompt injection 2026`
**Fuentes:** articsledge.com (Agent Skills Complete Guide 2026), docs.openhands.dev (Skills & Context), abdulaouwal.com (Build Skills), arxiv.org/pdf/2510.26328 (Skill prompt injection), arxiv.org/html/2602.14211 (SkillJect)
**Hallazgo clave (cómo se anuncian skills al agente):**
- **Stage 1 — Discovery:** agent lee YAML frontmatter (name + description) de TODAS las skills al iniciar sesión
- **Stage 2 — Activation:** cuando la request matchea una description, full SKILL.md se carga
- **Stage 3 — Execution:** scripts/ y references/ se cargan on-demand
- **OpenHands agrega:** `<available_skills>` con description only → agent llama `invoke_skill()` (model-mediated) o auto-inject si hay triggers
- **Trigger types:**
  - `triggers` field en SKILL.md → keyword activation
  - Sin triggers → solo manual (agent decide)
  - Path-triggered → cuando el agent toca un file matching
- **Activation accuracy problema:** "false activations (skill loads when it should not) y missed activations (skill does not load when it should). Test against 10 representative requests before deploying."
- **84% activation reliability** con hooks optimizados vs 20% con description pobre (paper enuno/14-Production-Grade-Skills)
- **Detection ceiling:** ~32-36 skills antes de que el sistema struggle
- **Security:** skills son inseguros per arxiv 2510.26328 — trivially simple prompt injections posibles

**Aplicación al Osquestador:**
- En el `osquestador://hello`, el campo `skills_catalog` es una lista de YAML frontmatter (name + description) de TODAS las skills disponibles
- Máximo 36 skills por respuesta (detection ceiling)
- Cada skill con `triggers` keywords se publica
- En la `instructions` field se avisa: "Skills activate by description match. Ask the agent to use a skill explicitly or rely on automatic matching."

### Búsqueda 7 — `Anthropic Console tool use function calling schema description tools available to model`
**Fuentes:** platform.claude.com (Tool use overview), platform.claude.com (Define tools), docs.aws.amazon.com (Bedrock), platform.claude.com (How tool use works), platform.claude.com (Programmatic tool calling)
**Hallazgo clave:**
- **Tool use = contract** entre application y model
- **Tool definition fields:**
  - `name` (regex `^[a-zA-Z0-9_-]{1,64}$`)
  - `description` (detailed plaintext — qué hace, cuándo usar, cómo se comporta)
  - `input_schema` (JSON Schema)
  - `input_examples` (opcional, hasta 20, validados contra schema)
  - `strict: true` (opcional, garantiza schema match exacto)
- **API constructs special system prompt** from tool definitions + tool configuration + user-specified system prompt
- **"If you're writing a regex to extract a decision from model output, that decision should have been a tool call."**
- **Programmatic tool calling:** `allowed_callers` field (`["direct"]` o `["code_execution_..."]`)
- **Default tool_choice:** `{"type": "auto"}` — model decide

**Aplicación al Osquestador:**
- Cada tool MCP tiene un JSON Schema estricto (jsonschema validation)
- Description es detailed plaintext, NO solo el nombre
- `strict: true` activado por default en tools críticos
- `input_examples` agregados en tools complejos

### Búsqueda 8 — `A2A protocol agent card skills declaration Google 2025 capabilities endpoint`
**Fuentes:** codelabs.developers.google.com (A2A intro), medium.com (Understanding A2A), docs.cloud.google.com (Vertex A2A), codelabs.developers.google.com (A2A multi-agent), dev.to (Google A2A)
**Hallazgo clave (ESTÁNDAR DE GOOGLE, abril 2025):**
- **A2A (Agent2Agent):** open standard, ahora Linux Foundation-governed
- **HTTP/JSON-RPC 2.0** transport
- **5 official SDKs** (Go, Python, JS, Java, .NET)
- **Agent Card en `/.well-known/agent.json`** — JSON metadata document
- **Agent Card estructura:**
  ```json
  {
    "capabilities": {"streaming": true, "pushNotifications": true},
    "defaultInputModes": ["text", "text/plain"],
    "defaultOutputModes": ["text", "text/plain"],
    "description": "Helps with creating burger orders",
    "name": "burger_seller_agent",
    "protocolVersion": "0.2.6",
    "skills": [
      {
        "description": "...",
        "examples": ["I want to order 2 classic cheeseburgers"],
        "id": "create_burger_order",
        "name": "Burger Order Creation Tool",
        "tags": ["burger order creation"]
      }
    ],
    "url": "https://...",
    "version": "1.0.0"
  }
  ```
- **4 key sections:** Capabilities, Modalities, Authentication, Endpoint
- **A2A = agents, MCP = tools** (oficial: "applications use MCP for tools and A2A for agents")
- **AgentSkill fields:** `id`, `name`, `description`, `tags[]`, `examples[]`, `inputModes[]`, `outputModes[]`

**Aplicación DIRECTA al Osquestador (el Osquestador es un Agent A2A):**
- Expone `/.well-known/agent.json` con la estructura A2A oficial
- El campo `skills[]` lista los capabilities (search, memory, skill_install, etc) con tags
- `capabilities` declara streaming, pushNotifications, custom extensions
- `url` apunta al endpoint del Osquestador (WebSocket o HTTP)
- `version` es SemVer del Osquestador

### Búsqueda 9 — `agent discoverable capabilities OpenAPI skill card tool description auto-register`
**Fuentes:** openagentskill.com (Registry), xhipment.mintlify.app (Discovery Cards Agentium), aisa.one (Agent Discovery), agentpatterns.ai (Agent Cards), openagentskills.dev (Integrating Skills)
**Hallazgo clave:**
- **OpenAgentSkill registry:** API para descubrir + comparar + auditar + instalar skills. Agent-native endpoints con trust signals
- **Agentium Discovery Cards:** auto-generated para cada agent registrado, sigue patrón A2A. Endpoints: `GET /agents/:name/card`. **Auto-detected capabilities:** memory, tools, structured_output, handoff, cost_tracking, caching, context_compaction, checkpointing, streaming
- **AIsa:** `/.well-known/agent-card.json` con 11 skills advertised. Bearer token auth declarado en card
- **AgentPatterns.ai:** "Agent cards live at `{base-url}/.well-known/agent-card.json`. Clients fetch with HTTP GET, following RFC 8615 well-known URI convention. The card works like an OpenAPI spec for HTTP APIs."
- **OpenAgentSkills.dev integration:** 6 steps para integrar skills: (1) discover, (2) load metadata at startup, (3) present via tool description, (4) activate on demand, (5) execute scripts, (6) enforce permissions

**Aplicación al Osquestador:**
- Auto-genera el Agent Card al boot basado en skills instaladas + capabilities del kernel
- Endpoint `/.well-known/osquestador.json` con la estructura A2A + extensiones propias
- Capabilities auto-detectadas: memory_tiers, search_engines, hooks, projects, skills, multi_source_skill_search

### Búsqueda 10 — `agent hello welcome message announce on connect WebSocket protocol pattern design`
**Fuentes:** websockets.readthedocs.io (Design patterns), websocket.org (Notifications), softwaresystemdesign.com (WebSockets), oneuptime.com (Chat with WebSockets), besser-agentic-framework (WebSocket platform)
**Hallazgo clave:**
- **Pattern:** al aceptar conexión, server envía welcome message inmediatamente con `{type: "connection", clientId, message: "Connected"}` + `type: "greeting_response"`
- **Notification vs Request:** frames sin `id` = notifications (no esperan respuesta), con `id` = requests
- **Heartbeat pattern:** ping/pong cada 25-30s para mantener conexión alive
- **Producer/Consumer pattern:** 2 tasks paralelas (consumer recibe, producer envía)
- **Channel separation:** control channel / work channel / scope channel (de Bridge ACE multi-agent)
- **Multi-agent WS:** agent A puede mandar a agent B conociendo su WS endpoint, "Agent B will receive the message and treat it the same way as if it was a human message. It will create a new session, detect the intent, transition to another state, etc."

**Aplicación al Osquestador:**
- WS al conectar → inmediato `osquestador://hello` notification (welcome + capabilities + skills catalog)
- Channel separation: control (handshake, ping) / work (tool calls) / stream (streaming responses)
- Producer/consumer pattern en asyncio para manejar bidireccional
- Ping/pong cada 30s con timeout 10s para forzar reconnect

---

## Decisión de arquitectura del Osquestador (handshake)

### 3 canales de advertisement según el transporte

#### A) HTTP (`.well-known/osquestador.json` + `/mcp`)
- Estándar A2A `/.well-known/agent.json` + extensión propia `/osquestador.json`
- Compatible con cualquier cliente que implemente A2A
- Authentication via Bearer token (API key por proyecto)
- Discovery via `Accept: application/agent+json` (AHP)
- MCP transport sigue handshake clásico `initialize`/`initialized`

#### B) WebSocket (handshake live)
- Conexión WS → server envía inmediatamente notification `osquestador://hello`
- Payload incluye: session_id, project_id, capabilities, skills_catalog (top-36), search_engine_status, scratchpad_inicial, instructions
- Cliente responde con `initialized` notification
- 3 canales: control (ping/pong/close) / work (tool calls) / stream (responses)

#### C) Stdio (procesos locales)
- Mismo handshake que HTTP, pero via stdin/stdout
- Usado por agentes locales (Claude Code, Cursor) que ejecutan el Osquestador como subprocess

### Estructura del `osquestador://hello` payload

```json
{
  "type": "osquestador/hello",
  "version": "1.0.0",
  "timestamp": "2026-07-18T01:45:00Z",
  "session_id": "uuid-v4",
  "project_id": "max-osquestador",
  "server": {
    "name": "osquestador",
    "version": "1.0.0",
    "protocol_version": "2026-07-18"
  },
  "capabilities": {
    "tools": true,
    "resources": true,
    "logging": true,
    "streaming": true,
    "push_notifications": true,
    "osquestador": {
      "skills_catalog": true,
      "search_engine": true,
      "memory_tiers": ["HOT", "WARM", "COLD"],
      "projects": true,
      "multi_source_skills": ["clauhb", "skillsmp", "openagentskill", "github", "max-local"],
      "hybrid_search": ["BM25", "vector", "RRF"],
      "web_search_engines": ["tavily", "exa", "perplexity"]
    }
  },
  "instructions": "Osquestador is the kernel. It exposes MCP tools, manages projects, and provides persistent memory. Skills load progressively. Search engine auto-activates on each prompt. Ask the agent to use a skill explicitly or rely on automatic matching.",
  "skills_catalog_short": [
    {
      "name": "pdf-processing",
      "description": "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs.",
      "tags": ["pdf", "documents"]
    },
    {
      "name": "git-commit",
      "description": "Create well-formatted git commits with conventional commit messages. Use after staging changes.",
      "tags": ["git", "version-control"]
    }
  ],
  "search_engine": {
    "status": "ready",
    "latency_p95_ms": 200,
    "modes": ["hybrid", "keyword", "vector", "tags"]
  },
  "memory": {
    "hot_size_tokens": 0,
    "warm_size_tokens": 0,
    "cold_commits": 0,
    "project_id": "max-osquestador"
  },
  "scratchpad": {
    "content": "",
    "tokens": 0,
    "path": "/root/.osquestador/proyectos/max-osquestador/vault/working/{session_id}.md"
  }
}
```

### Validación del handshake (jsonschema determinístico)

```python
# osquestador/handshake/schema.py
HELLO_SCHEMA = {
  "type": "object",
  "required": ["type", "version", "timestamp", "session_id", "project_id", "server", "capabilities"],
  "properties": {
    "type": {"enum": ["osquestador/hello"]},
    "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
    "timestamp": {"type": "string", "format": "date-time"},
    "session_id": {"type": "string", "format": "uuid"},
    "project_id": {"type": "string", "minLength": 1, "maxLength": 64},
    "server": {
      "type": "object",
      "required": ["name", "version", "protocol_version"],
      "properties": {
        "name": {"enum": ["osquestador"]},
        "version": {"type": "string"},
        "protocol_version": {"type": "string"}
      }
    },
    # ... etc
  }
}
```

### Endpoints HTTP del Osquestador

| Endpoint | Método | Propósito |
|----------|--------|-----------|
| `/.well-known/agent.json` | GET | A2A Agent Card estándar |
| `/.well-known/osquestador.json` | GET | Extensión con skills catalog + project_id |
| `/mcp` | POST/GET | MCP transport (streamable HTTP) |
| `/rpc.discover` | POST | OpenRPC schema del Osquestador |
| `/health` | GET | Health check (no auth) |
| `/metrics` | GET | Métricas (con auth) |

### WebSocket message types

| Type | Direction | Propósito |
|------|-----------|-----------|
| `osquestador/hello` | Server → Client | Welcome + capabilities + skills catalog |
| `initialized` | Client → Server | Confirma recepción del hello |
| `tool/call` | Bidirectional | MCP tool call |
| `tool/result` | Bidirectional | MCP tool result |
| `stream/chunk` | Server → Client | Streaming response chunk |
| `push/notification` | Server → Client | Push notification (Punto 4) |
| `ping` / `pong` | Bidirectional | Heartbeat |

---

## Stack técnico final

| Componente | Tecnología | Fuente de evidencia |
|------------|-----------|---------------------|
| **Handshake estándar** | MCP `initialize` + A2A Agent Card | modelcontextprotocol.io, codelabs.developers.google.com |
| **Discovery URI** | RFC 8615 well-known URI | agenthandshake.dev, agentpatterns.ai |
| **JSON-RPC transport** | JSON-RPC 2.0 + WebSocket | jsonrpc.org/specification, ACP spec |
| **Schema description** | OpenRPC + JSON Schema | spec.open-rpc.org, platform.claude.com |
| **Authentication** | Bearer token (API key por proyecto) | AIsa, A2A |
| **Heartbeat** | WS ping/pong cada 30s, timeout 10s | dev.to frus-ai, websocket.org |
| **Channel separation** | control / work / stream | Bridge ACE multi-agent |
| **Validation** | jsonschema determinístico | charlessieg.com (Deterministic Scaffolding) |
| **Multi-tenant isolation** | project_id en cada mensaje, namespace SQLite | fast.io, zylos.ai (Punto 1) |

---

## Métricas de éxito del Punto 3

- [ ] Handshake funciona en HTTP (`.well-known/osquestador.json`), WebSocket (`osquestador://hello`), y Stdio (subprocess)
- [ ] Cliente A2A externo puede descubrir el Osquestador via `/.well-known/agent.json` y usar skills
- [ ] Cliente MCP (Claude Code, OpenClaw) puede hacer `initialize` y recibir capabilities completas
- [ ] Auto-detección de capabilities (memory_tiers, search_engines, projects, etc) funciona sin config manual
- [ ] Skills catalog se sirve con progressive disclosure (top-36, frontmatter only)
- [ ] Search engine status se reporta en hello (ready/cold start <200ms)
- [ ] Heartbeat ping/pong funciona, forzar reconnect si timeout 10s
- [ ] JSON Schema validation rechaza payloads malformados (90% código)
- [ ] Test E2E: cliente fake se conecta, recibe hello, llama tool, recibe response, desconecta

## Riesgos identificados

1. **Versioning incompatible entre cliente/server** — mitigación: server MUST responder con `supported_versions` list si no puede usar la del cliente
2. **Hello payload >10KB con muchas skills** — mitigación: progressive disclosure (top-36 + paginación)
3. **WS connection drops sin heartbeat** — mitigación: ping/pong 30s + timeout 10s + reconnect logic
4. **Bearer token leak en logs** — mitigación: redactar tokens en audit log
5. **Race condition en concurrent connections** — mitigación: session_id UUID v4 + locking por session
6. **Skills catalog stale (no refleja nuevas skills)** — mitigación: refresh en cada SessionStart hook
7. **Cross-project leak en capabilities** — mitigación: cada proyecto tiene su propio scope_id, server valida antes de servir

---

## Próximo paso (esperando luz verde de Max)
- **Punto 4:** Sistema push/ping + historial de chat + tags/etiquetas para búsqueda.

**¿Apruebas el Punto 3 para pasar al Punto 4?**
