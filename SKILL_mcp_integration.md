# SKILL: Integración MCP (Model Context Protocol)

## Objetivo
Exponer el Orquestador Fase 0 como **servidor MCP** y consumirlo desde un **panel / agente / IDE** (Claude Desktop, Cursor, panel custom del Osquestador) usando JSON-RPC 2.0 sobre stdio o Streamable HTTP.

## Contexto
Investigación consolidada en `INVESTIGACION.md` secciones 11, 22, 27.
MCP es el estándar abierto de Anthropic para conectar LLMs con data/tools. Ratificado 2025-06-18. Discovery vía `/.well-known/mcp.json` (SEP-1649, 2025-11-25).

## Entradas
- El Orquestador expone 4 tools nativas (`search_project`, `get_doc`, `list_conflicts`, `queue_doc`).
- Cliente que consume (panel HTML, Claude Desktop, Cursor, código custom).
- Configuración: `mode` (dev|staging|prod) + `mcp_server.port` (default 8765).

## Procedimiento

### Como SERVIDOR (orquestador expone)
1. Implementar endpoint HTTP que recibe `POST` con `Content-Type: application/json` y body JSON-RPC 2.0.
2. Despachar `tools/list` → lista de tools con `name`, `description`, `params`.
3. Despachar `tools/call` con `name` + `arguments` → invocar adapter real + devolver `result` o `error` con código JSON-RPC.
4. Servir en `127.0.0.1:8765` (loopback) por seguridad.
5. Validar contra JSON-RPC 2.0 spec: `id` correlacionado, `error.code` en rango reservado, `error.message` humano-legible.
6. Exponer discovery en `/.well-known/mcp.json` con transport, endpoint, capabilities.

### Como CLIENTE (panel / IDE consume)
1. Conectar al endpoint HTTP del orquestador con POST + `Accept: application/json, text/event-stream`.
2. Llamar `tools/list` para descubrir tools.
3. Llamar `tools/call` con los args de cada tool.
4. Manejar `result` o `error.code` (parse, method, params, internal, server).
5. Streaming via SSE para respuestas largas (opcional, no soportado por quick tunnel).

## Reglas
- ✅ Mensajes **SIEMPRE** UTF-8 encoded.
- ✅ `id` correlacionado entre request y response.
- ✅ `Accept` header DEBE incluir `application/json` y `text/event-stream`.
- ✅ Server **NO** escribe a stdout nada que no sea JSON-RPC válido.
- ✅ Side-effecting methods requieren **idempotency keys**.
- ❌ Server **NO** escribe a stdout de logs (usar stderr).
- ❌ NUNCA incluir en frames: tokens, cookies, secrets.

## Restricciones
- Puerto por defecto: `127.0.0.1:8765` (no exponer público sin reverse proxy).
- TLS: solo si se expone fuera de localhost (Cloudflare Tunnel con --url).
- Max payload: 64 KiB pre-auth, `hello-ok.policy.maxPayload` post-auth.
- Timeout recomendado: 30s para tools lentas (OCR, LLM calls).

## Ejemplos

### Tools list
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {"name": "search_project", "description": "Docs y estado de un proyecto", "params": ["proyecto"]},
      {"name": "get_doc", "description": "Contenido íntegro por hash", "params": ["hash"]},
      {"name": "list_conflicts", "description": "Conflictos abiertos", "params": ["proyecto?"]},
      {"name": "queue_doc", "description": "Encolar doc a inbox", "params": ["proyecto", "nombre", "contenido"]}
    ]
  }
}
```

### Tool call
```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "tools/call",
  "params": {
    "name": "search_project",
    "arguments": {"proyecto": "maxbry"}
  }
}
```

### Tool call response
```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "result": {
    "docs": [{"hash": "abc123", "nombre": "DOC1.md", "estado": "auditado"}],
    "tareas": [{"titulo": "[maxbry] objetivo X", "etiqueta": "DEFINIR", "estado": "pendiente"}],
    "conflictos": []
  }
}
```

### Error response
```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "error": {
    "code": -32601,
    "message": "Method not found",
    "data": {"method": "search_proyect"}
  }
}
```

## Fuentes
- Spec oficial: https://modelcontextprotocol.io/specification/2025-06-18
- Transports: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports
- Servers oficiales: https://github.com/modelcontextprotocol/servers
- JSON-RPC 2.0: https://www.jsonrpc.org/specification
- Anthropic announcement: https://www.anthropic.com/news/model-context-protocol
- SEP-1649 (discovery): https://agent-ready.dev/mcp-vs-a2a-vs-agents-json

## Dependencias
- Python 3.10+ stdlib (`http.server`, `json`, `threading`)
- `requests` (cliente HTTP)

## Cuándo utilizar
- El panel del Orquestador necesita controlar el kernel sin abrir su UI.
- Un IDE (Cursor, Claude Desktop) quiere que el orquestador le provea contexto.
- Dos orquestadores necesitan interoperar (Fase 1).
- Cualquier integración LLM ↔ herramientas internas.

## Cuándo NO utilizar
- Comunicación entre procesos en el mismo binario (usar función directa).
- Transferencia de archivos grandes (usar HTTP file upload directo).
- Eventos pub/sub (usar WebSocket nativo, no JSON-RPC over WS).

## Relación con otros Skills
- `SKILL_orquestador_kernel.md` — el kernel expone el MCP server.
- `SKILL_panel_ui.md` — el panel consume el MCP server.
- `SKILL_memoria_avanzada.md` — `search_project` retorna memoria + inventario.

## Versión
v1.0 — 2026-07-17 · Mavis.

## Historial
- v1.0 — extracción del spec Parte C + spec MCP 2025-06-18 + JSON-RPC 2.0.
