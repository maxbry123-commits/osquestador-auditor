# INVESTIGACIÓN COMUNITARIA V2 — PUNTO 3
## Inyección de información al agente + Push/ping + Historial de chat + Tags/etiquetas

**Fecha:** 2026-07-18
**Investigador:** A2 (Mavis en delegación de Max)
**Búsquedas:** 10 (4 China/India + 6 mundo) + las 10 que ya hice del Punto 3 original
**Trigger de Max (formato pedido):** "el documento o informa lo manda o recibe y luego lo usa o lo modifica o lo guarda"
**Estado:** COMPLETO — listo para revisión final de Max

---

## 📚 FORMATO QUE MAX PIDIÓ (manda / recibe / usa / modifica / guarda)

**Explicación con ejemplo del Punto 1:**

Cuando llega un mensaje de WhatsApp:
1. **SE MANDA** desde el teléfono → llega al servidor (internet)
2. **LO RECIBE** el otro teléfono → aparece en la pantalla
3. **LO USA** la persona → lo lee
4. **LO MODIFICA** a veces → responde o lo edita
5. **LO GUARDA** otras veces → lo archiva o screenshot

En el Osquestador pasa IGUAL con cada documento. Te explico los 4 temas del Punto 3 con este formato.

---

## 🔔 TEMA 1: PUSH/PING (notificaciones en tiempo real)

### ¿Qué es?
El Osquestador le manda avisos al chat/agente SIN que el usuario pida nada. Como cuando WhatsApp te avisa "llegó un mensaje" sin que vos lo pidas.

### ¿Cómo lo manda/recibe/usa/modifica/guarda la comunidad?

**1. SE MANDA** (servidor → cliente):
- El servidor manda un mensaje JSON: `{"type": "notification", "evento": "deploy_failed", "data": {...}}`
- Lo manda por **SSE** (Server-Sent Events, unidireccional, simple) o **WebSocket** (bidireccional)
- Fuentes: Cloudflare Agents, websocket.org, SSE guides 2026

**Ejemplo real de la comunidad (LiveChat):**
```json
// El servidor MANDA este push cuando llega un chat nuevo:
{
  "type": "incoming_chat",
  "chat": {
    "id": "PJ0MRSHTDG",
    "users": [{"id": "smith@example.com"}],
    "thread": {"events": [...]}
  }
}
```

**2. LO RECIBE** (cliente):
- El cliente (navegador/app) escucha en `ws://osquestador:8080/sse/notifications`
- Cuando llega el JSON, el navegador lo muestra (toast notification, badge counter, etc)
- El cliente **NO pregunta** — el server le avisa

**3. LO USA** (cliente/UI):
- El chat UI muestra: "🔔 Nuevo mensaje del agente"
- El panel UI refresca el estado sin que el usuario pida
- El agente puede REACCIONAR a la notificación (ej: si llega "deploy_failed", el agente lo abre y propone fix)

**4. LO MODIFICA** (cliente → server):
- El cliente responde con ACK: `{"type": "ack", "id": "evt_123"}`
- Si el cliente quiere pausar: `{"type": "pause", "channel": "deploys"}`
- Si el cliente marca como visto: `{"type": "seen", "last_id": "evt_125"}`

**5. LO GUARDA** (server → DB):
- El Osquestador guarda cada notificación enviada en `~/.osquestador/proyectos/<id>/db/notifications.sqlite`
- Tabla: `notifications(id, project_id, type, payload, sent_at, ack_at)`
- Con TTL de 30 días por default

### Heartbeat (ping/pong) — para saber que la conexión sigue viva

**Cómo funciona (consenso community):**
- **Servidor MANDA** cada 30s: `{"type": "ping", "ts": 1234567890}`
- **Cliente RECIBE** y RESPONDE: `{"type": "pong", "ts": 1234567890}`
- Si en 10s no llega pong → **el servidor MODIFICA** el estado a "zombie" y cierra
- **El servidor GUARDA** el último heartbeat en memoria para stats

**Patrón community (3 fuentes coinciden):**
- Heartbeat interval: 30 segundos
- Pong timeout: 10 segundos
- Heartbeat perdido 3 veces → cerrar conexión
- Reconexión con exponential backoff + jitter (1s base, 30s max, ±1s)

---

## 💬 TEMA 2: HISTORIAL DE CHAT (chat history)

### ¿Qué es?
Cada conversación que el usuario tiene con el agente se guarda para que en sesiones futuras el agente recuerde qué se habló.

### ¿Cómo lo manda/recibe/usa/modifica/guarda la comunidad?

**1. SE MANDA** (usuario → agente):
- El usuario escribe un mensaje → el chat UI lo manda al Osquestador
- Formato: `{"role": "user", "content": "Hola, ¿cómo configuro X?", "session_id": "abc123"}`
- Fuentes: Pydantic AI, OpenAI Agents SDK, Microsoft Agent Framework, Chainlit

**2. LO RECIBE** (agente / LLM):
- El agente junta el mensaje nuevo + historial anterior
- Lo mete en el system prompt antes de llamar al LLM
- **Patrón community:** últimas 10-30 mensagens siempre visibles, el resto resumidas

**3. LO USA** (LLM responde):
- El LLM lee todo el contexto y genera respuesta coherente con la conversación previa
- El LLM puede decir "como mencionaste antes..." porque tiene el historial

**4. LO MODIFICA** (agente → DB):
- Después de cada turno, el agente GUARDA el mensaje nuevo
- **Schema community (consenso 4 fuentes):**
  ```sql
  CREATE TABLE conversations (id, user_id, project_id, title, created_at, updated_at);
  CREATE TABLE messages (id, conversation_id, role, content, token_count, created_at);
  CREATE TABLE tool_calls (id, conversation_id, message_id, tool_name, input, output, status);
  ```
- El agente también puede MODIFICAR el título de la conversación (auto-genera con LLM)

**5. LO GUARDA** (DB → retrieval):
- Cuando hay nueva sesión, el agente RECIBE las últimas N mensajes del conversation_id
- **Patrón community (Microsoft, Pydantic, OpenAI, SQLAlchemy):** `limit=20` por default, configurable
- **Búsqueda en historial:** `WHERE conversation_id = ? ORDER BY created_at DESC LIMIT 20`
- Para búsqueda semántica: embed cada mensaje, guardar en vector store

### Storage patterns validados (5 fuentes)

| Fuente | Storage | Retrieval | Notas |
|--------|---------|-----------|-------|
| OpenAI Agents SDK | SQLiteSession | session.get_items(id) | Built-in, file-based |
| Pydantic AI | SQLAlchemy/SQLite | message_history param | Custom store |
| Microsoft Agent | HistoryProvider | ProvideOutputMessageFilter | Limita a N mensajes |
| Oracle AI | SQL + Vector | hybrid (SQL exact + vector semantic) | Para producción |
| Chainlit | PostgreSQL | auto-save + @cl.on_chat_resume | Resume thread |

**Decisión para Osquestador:** SQLite (default, simple) + opción PostgreSQL (producción). Schema con `conversations`, `messages`, `tool_calls`, `memory_chunks`, `summaries`.

---

## 🏷️ TEMA 3: TAGS/ETIQUETAS (para buscar después)

### ¿Qué es?
Cada conversación/mensaje/skills/documento lleva etiquetas (palabras clave) para encontrarlo después con un filtro.

### ¿Cómo lo manda/recibe/usa/modifica/guarda la comunidad?

**1. SE MANDA** (agente → DB):
- Al cierre de cada sesión importante, el agente genera 3-5 tags con LLM
- **Patrón community (legaled.ai):** prompt al LLM "¿qué keywords harían fácil encontrar esta conversación después?"
- **Patrón MemoClaw (kebab-case obligatorio):**
  ```yaml
  tags:
    - "user-pref"        # preferencias del usuario
    - "correction"       # algo que el agente hizo mal (importance ≥0.9)
    - "decision"         # decisión arquitectónica
    - "summary"          # resumen de sesión
    - "context"          # info background
    - "task"             # action items
  secondary:
    - "tech", "architecture", "ops", "session", "personal", "urgent"
  ```

**2. LO RECIBE** (agente o UI):
- El agente recibe la lista de tags via `osquestador://get_tags?conversation_id=X`
- La UI los muestra como badges de colores bajo el título

**3. LO USA** (búsqueda):
- El usuario busca: "muéstrame todas las conversaciones sobre PDFs"
- Sistema filtra: `WHERE 'pdf' IN tags` → retorna lista
- **Búsqueda híbrida:** tag filter PRIMERO, después vector search sobre el subset
- Fuentes: MemoClaw, SteelEngine, OpenAgentAGI, Bedrock Agents

**4. LO MODIFICA** (user → DB):
- El usuario puede agregar/quitar tags manualmente
- El agente puede actualizar tags si el contexto cambia
- Endpoint: `POST /tags/assign?conversation_id=X&tag=urgent`

**5. LO GUARDA** (DB):
- Schema community:
  ```sql
  CREATE TABLE tags (id, name, project_id, color);
  CREATE TABLE conversation_tags (conversation_id, tag_id);
  -- o un array de tags en conversations: tags TEXT[]
  ```
- En el Osquestador: `conversations.tags TEXT[]` (más simple) o tabla separada (más flexible)

### Workflow concreto de tags (consenso community)

```
1. Usuario termina sesión importante
   ↓ SE MANDA prompt al LLM
2. LLM genera tags: ["pdf", "urgent", "tech"]
   ↓ SE GUARDA
3. Osquestador persiste en conversations.tags
   ↓ SE RECIBE cuando se busca
4. Usuario busca: "conversaciones de PDF urgentes"
   ↓ SE USA el filtro
5. Hybrid search: tag filter 'pdf' AND 'urgent' → vector sobre subset
   ↓ SE MUESTRA
6. Usuario selecciona una → click → abre conversación completa
```

---

## 🧠 TEMA 4: INYECCIÓN DE INFORMACIÓN AL AGENTE (context injection)

### ¿Qué es?
El Osquestador mete documentos/info en el "cerebro" del agente antes de que responda. Como cuando le decís a alguien "leé este archivo antes de contestarme".

### ¿Cómo lo manda/recibe/usa/modifica/guarda la comunidad?

**1. SE MANDA** (Osquestador → agente):
- El Osquestador lee `AGENTS.md`, `SOUL.md`, `MEMORY.md`, etc del proyecto
- Los junta en un system prompt
- Los MANDA al LLM antes de que el usuario pregunte nada
- **Patrón community (Hermes + OpenClaw + Claude Code):**
  ```
  Tier 1 (stable, always loaded): SOUL.md + skills + platform hints
  Tier 2 (context, session-loaded): AGENTS.md + CLAUDE.md + .cursorrules
  Tier 3 (volatile, fresh): MEMORY.md + USER.md + last summaries
  ```

**2. LO RECIBE** (agente / LLM):
- El LLM lee todo el system prompt
- Ya "sabe" las reglas del proyecto, la personalidad, el contexto

**3. LO USA** (LLM responde):
- El LLM responde siguiendo las reglas inyectadas
- Ejemplo: si `AGENTS.md` dice "siempre usar TypeScript", el LLM lo respeta

**4. LO MODIFICA** (user/LLM → DB):
- Si el usuario cambia `AGENTS.md`, el Osquestador lo detecta y recarga
- El LLM puede sugerir cambios (vía herramienta `update_context_file`)

**5. LO GUARDA** (filesystem + Git):
- Los archivos viven en `~/.osquestador/proyectos/<id>/`
- Commitea al repo `osquestador-memoria` cuando cambian
- Backup automático antes de modificar

### Inyección condicional (community best practice)

```
ALWAYS INJECT (Tier 1, no negociable):
  SOUL.md
  TOOLS.md (herramientas del Osquestador)
  <available_skills> XML block

IF primera vez del proyecto:
  BOOTSTRAP.md (solo brand-new workspaces)

IF usuario tiene perfil guardado:
  USER.md

IF hay resúmenes recientes (<24h):
  last 3 summaries de WARM tier

IF prompt del usuario menciona "ayer/antes/recuerdas":
  memoria histórica (git log search)
```

### Threat scanning (community critical)

Antes de inyectar cualquier archivo:
- **Patrón community (Hermes):** regex patterns para detectar prompt injection
- Si matchea → bloquea con `[BLOCKED: filename contained potential prompt injection]`
- El agente recibe aviso de que el contenido fue bloqueado

---

## 📊 RESUMEN DE HALLAZGOS DE LA COMUNIDAD

| Tema | Comunidad referencia | Patrón validado |
|------|---------------------|-----------------|
| Push/Ping | Cloudflare, LiveChat, websocket.org | SSE/WebSocket + heartbeat 30s/timeout 10s |
| Chat history | OpenAI, Pydantic, Microsoft, Chainlit | SQLite + 5 tablas + limit=20 default |
| Tags | MemoClaw, SteelEngine, Bedrock | 6 core + 6 secondary, kebab-case, LLM 10% |
| Context injection | Hermes, OpenClaw, Claude Code, LangChain | 3 tiers + threat scanning + conditional |

---

## 💻 IMPLEMENTACIÓN PARA EL OSQUESTADOR (resumen final)

### Estructura física

```
~/.osquestador/proyectos/<id>/
├── db/
│   ├── warm.sqlite           # chat history + summaries + tags
│   ├── notifications.sqlite  # push notifications log
│   └── episodic.sqlite       # log de eventos
├── vault/
│   ├── AGENTS.md             # reglas del proyecto (Tier 2)
│   ├── SOUL.md               # personalidad (Tier 1)
│   ├── MEMORY.md             # memoria persistente (Tier 3)
│   ├── USER.md               # perfil user (Tier 3)
│   └── working/<session>.md  # scratchpad (Tier 3)
└── .git/                     # sync a repo osquestador-memoria
```

### Schema de DB (SQLite)

```sql
-- Chat history
CREATE TABLE conversations (
  id TEXT PRIMARY KEY, project_id TEXT, user_id TEXT, agent_id TEXT,
  title TEXT, tags TEXT[], created_at, updated_at
);
CREATE TABLE messages (
  id TEXT PRIMARY KEY, conversation_id TEXT, role TEXT,
  content TEXT, token_count INT, model_name TEXT, latency_ms INT,
  metadata JSON, created_at
);
CREATE TABLE tool_calls (
  id TEXT PRIMARY KEY, conversation_id TEXT, message_id TEXT,
  tool_name TEXT, input JSON, output JSON, latency_ms INT, status TEXT, created_at
);

-- Tags
CREATE TABLE tags (id TEXT PRIMARY KEY, name TEXT UNIQUE, project_id TEXT, color TEXT);
CREATE TABLE conversation_tags (conversation_id TEXT, tag_id TEXT);

-- Notifications
CREATE TABLE notifications (
  id TEXT PRIMARY KEY, project_id TEXT, type TEXT, payload JSON,
  sent_at, ack_at, seen_at
);
```

### Endpoints HTTP

| Endpoint | Método | Propósito |
|----------|--------|-----------|
| `/sse/notifications/{project_id}` | GET | Push SSE (server → cliente) |
| `/ws/{project_id}/{agent_id}` | WS | Chat live (bi-directional) |
| `/api/conversations` | GET/POST | Historial de chat |
| `/api/conversations/{id}/messages` | GET/POST | Mensajes |
| `/api/conversations/{id}/tags` | GET/POST/PATCH | Tags |
| `/api/search?tags=...&q=...` | GET | Búsqueda híbrida |
| `/api/context/inject` | POST | Forzar inyección de contexto |

### WebSocket message types

```python
# Cliente → Servidor
{"type": "ping", "ts": 1234567890}
{"type": "chat", "text": "Hola", "conversation_id": "abc"}
{"type": "ack", "notification_id": "evt_123"}
{"type": "tag_add", "conversation_id": "abc", "tag": "urgent"}

# Servidor → Cliente
{"type": "pong", "ts": 1234567890}
{"type": "notification", "event": "deploy_failed", "data": {...}}
{"type": "stream_chunk", "content": "..."}
{"type": "context_injected", "files": ["AGENTS.md", "MEMORY.md"]}
{"type": "tag_added", "conversation_id": "abc", "tag": "pdf"}
```

---

## 🎯 MÉTRICAS DE ÉXITO

- [ ] Push notifications llegan en <500ms (SSE) o <100ms (WS) desde el evento
- [ ] Heartbeat ping cada 30s, timeout 10s, reconexión automática
- [ ] Chat history persiste con SQLite, query <50ms para últimos 20 mensajes
- [ ] Tags se generan automáticamente al cierre de sesión (LLM 10% budget)
- [ ] Búsqueda por tag retorna resultados en <200ms (BM25 + vector hybrid)
- [ ] Context injection respeta 3 tiers y threat scanning
- [ ] Cross-project isolation: notificaciones de proyecto A no leak a proyecto B

## ⚠️ RIESGOS

1. **Push notification spam** — mitigación: dedupe window 5 min, rate limit por usuario
2. **Chat history crece sin límite** — mitigación: TTL 90 días + summary a WARM
3. **Tag explosion** — mitigación: max 6-8 core tags + audit mensual
4. **Prompt injection en archivos** — mitigación: threat scanning + truncado
5. **WebSocket drop en mobile** — mitigación: SSE fallback + auto-reconnect
6. **SSE en proxy/firewall** — mitigación: WS como fallback

---

**Próximo paso (esperando luz verde de Max):**
Una vez aprobado este Punto 3, arrancamos la **programación del código real** del Osquestador, basado en las 4 estrategias validadas (push/ping + chat history + tags + context injection).
