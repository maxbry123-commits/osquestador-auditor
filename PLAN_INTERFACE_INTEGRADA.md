# PLAN DE INTERFACE INTEGRADA DEL OSQUESTADOR
## Cómo voy a UNIR las interfaces de los 12 programas + las 70 ideas + 25 decisiones en UNA sola UI

**Fecha:** 2026-07-18 02:27
**Trigger de Max:** "como vas a crear la interface integrando todo los ui de cada uno + los item que anotaste que aprobamos como piensas integrar todo en la interface"
**Estado:** PLAN COMPLETO — esperando OK para programar

---

## 1) IDEA CENTRAL (la más importante)

La interface del Osquestador es **UN SOLO PANEL WEB** dividido en **5 ZONAS VISUALES**. Cada zona muestra la info de un grupo de programas. No es un dashboard genérico — es un **panel de control del orquestador** con la estética de Claude.ai.

Cuando vos entrás al panel, ves TODO lo que está pasando en los 12 programas a la vez, organizado por zona.

---

## 2) LAS 5 ZONAS DEL PANEL

**Zona 1 — SIDEBAR IZQUIERDA** (fija, 240px de ancho, oscura)
- Lista de proyectos activos (viene de Kanboard vía JSON-RPC)
- Estado de cada proyecto: 🟢 corriendo / 🟡 pausado / 🔴 error
- Botón "+ Nuevo proyecto" arriba
- Filtros: todos / activos / archivados
- Inspirado en: **Claude.ai sidebar** (estructura) + **Kanboard API** (data)

**Zona 2 — HEADER SUPERIOR** (60px de alto)
- Logo Osquestador + nombre del proyecto actual
- Selector de modelo LLM (dropdown con los 5: Anthropic, OpenAI, Groq, Cerebras, NVidia)
- Estado de conexión MCP (semáforo)
- Avatar de usuario + settings
- Inspirado en: **Claude.ai header** (estética) + **LiteLLM** (selector)

**Zona 3 — CHAT CENTRAL** (área principal, ocupa el resto)
- Burbujas de chat estilo Claude (user derecha, asistente izquierda)
- Input box abajo con placeholder "Preguntale al Osquestador..."
- Slash commands: `/memory`, `/search`, `/projects`, `/audit`, etc
- Streaming token por token (vía WebSocket)
- Auto-scroll, copy button en cada mensaje
- Inspirado en: **Claude.ai chat** (estética) + **Hermes skills** (slash commands) + **Plandex REPL** (interactividad)

**Zona 4 — PANEL DERECHO CONTEXTUAL** (320px, plegable)
- Pestañas que cambian según el contexto:
  - **"Memoria"** → grafo de Graphiti (visualización simple de nodos/relaciones)
  - **"Documentos"** → lista de archivos del vault Obsidian
  - **"Tareas"** → tarjetas Kanboard del proyecto
  - **"Skills"** → catálogo de skills disponibles (estilo Hermes `~/.hermes/skills/`)
  - **"Logs"** → eventos en vivo (PaddleOCR procesó X, Haystack detectó duplicado, etc)
- Inspirado en: **Graphiti** (memoria) + **Obsidian** (docs) + **Kanboard** (tareas) + **Hermes** (skills) + **MCP** (logs)

**Zona 5 — STATUS BAR INFERIOR** (32px, fija abajo)
- Tokens consumidos hoy (de LiteLLM)
- Latencia del último call LLM
- Memoria usada por SQLite WAL
- Próximo backup restic
- Watchdog status (systemd heartbeat)
- Inspirado en: **LiteLLM tracking** + **SQLite stats** + **systemd** (watchdog)

---

## 3) CÓMO SE CONECTAN LOS 12 PROGRAMAS A LA INTERFACE

Cada zona de la interface es servida por un endpoint del backend FastAPI que internamente habla con un adapter del programa correspondiente. La UI solo ve JSON limpio, no las SDKs.

**Flujo concreto (formato manda/recibe/usa/modifica/guarda):**

**Cuando llega un documento nuevo al inbox:**

1. **SE MANDA** — usuario arrastra PDF al panel
2. **LO RECIBE** — FastAPI recibe POST `/api/v1/inbox/upload`
3. **LO USA** — el kernel decide: necesita OCR → llama al adapter de **PaddleOCR**
4. **LO MODIFICA** — el texto extraído pasa al adapter de **Haystack** (similitud)
5. **LO GUARDA** — el adapter de **Obsidian** escribe el `.md` en el vault
6. **LO USA** — el adapter de **Graphiti** extrae entidades y crea nodos
7. **LO MODIFICA** — si Haystack detecta duplicado → adapter de **Kanboard** crea tarea
8. **LO GUARDA** — todo queda registrado en **SQLite** + sync a **MCP tools**
9. **LO USA** — el adapter de **Telegram** manda notificación a tu teléfono
10. **LO RECIBE** — la UI refresca via WebSocket: nuevo doc en Zona 4, nueva tarea en Kanboard view

**Todo eso pasa en 1-2 segundos. La UI muestra el progreso en vivo en la Zona 4 (panel Logs).**

---

## 4) CÓMO SE INTEGRAN LAS 70 IDEAS (mapeo concreto)

**Zona 1 (Sidebar):** Idea #18 (solo summary al parent) — cada proyecto muestra solo el título + estado, no el detalle.
**Zona 2 (Header):** Idea #7 (multi-LLM) — el selector tiene los 5 providers validados.
**Zona 3 (Chat):** Ideas #30, #22-29 (Claude Code patrones) + #26 (slash commands) + #18 (summary).
**Zona 4 (Panel derecho):** Ideas #31-40 (memory patterns) + #22 (provenance tracking) + #34 (retention prune).
**Zona 5 (Status bar):** Ideas #19 (token cost) + #17 (24/7) + #55 (TTL 90d) + watchdog.

**Detrás de la interface (no se ve pero hace todo):**
- Idea #1 (kernel pequeño) — el FastAPI backend es ~400 LOC
- Ideas #41-50 (sub-agents) — cada adapter es un sub-agent del kernel
- Ideas #51-60 (checkpoint) — el status del checkpoint se ve en Zona 5

---

## 5) CÓMO SE INTEGRAN LAS 25 DECISIONES (mapeo concreto)

- **D1 (kernel pequeño)** — el backend FastAPI es chico, 1 archivo
- **D2 (5-10 plugins intercambiables)** — cada adaptador es un plugin cargable
- **D3 (MCP server con 7 tools)** — el panel consume via MCP, no via REST directo
- **D4 (5 channels built-in)** — web, terminal, file, search, browser como botones
- **D5-D6 (SKILL.md + progressive disclosure)** — el catálogo de skills en Zona 4
- **D7-D8 (sub-agents + depth cap)** — los adapters son sub-agents nivel 1
- **D9-D10 (SQLite + idempotency)** — el botón "reintentar" usa idempotency keys
- **D11-D14 (vault + review + CTX + retention)** — la Zona 4 muestra el vault
- **D15 (BM25+vector hybrid)** — el search de Zona 3 usa los 2
- **D16 (90 días TTL)** — la Zona 4 muestra "expira en X días"
- **D17 (async checkpoint)** — la Zona 5 muestra "checkpointing..."
- **D19 (token awareness)** — la Zona 5 muestra tokens consumidos
- **D20 (estética Claude)** — toda la UI sigue ese estilo
- **D21-D25 (nohup/watchdog/backup)** — la Zona 5 muestra el estado de todo eso

---

## 6) ESTÉTICA Y UX (cómo se ve)

**Tema visual:**
- Dark mode por default (como Claude.ai)
- Color de acento: beige/cream (`#D4A574`) estilo Anthropic
- Tipografía: sans-serif moderna (Inter o system-ui)
- Iconos: línea simple (Lucide o Heroicons)
- Espaciado: generoso, sin clutter
- Responsive: mobile-first (stack vertical en celular)

**Interacciones clave:**
- **Hover** en sidebar → muestra tooltip con descripción
- **Click** en proyecto → carga contexto en Zona 3
- **Cmd+K** → command palette (estilo VSCode/Hermes)
- **Drag&drop** → upload a inbox
- **Right-click** en nodo de memoria → opciones (abrir, eliminar, ver relaciones)
- **Auto-save** → todo cambio se persiste en SQLite sin botón "guardar"

---

## 7) STACK TÉCNICO DE LA INTERFACE

**Frontend (1 archivo HTML, ~400 LOC):**
- HTML5 + TailwindCSS (vía CDN, sin build step)
- Vanilla JS (sin React, sin Vue — más simple, más rápido)
- WebSocket nativo para streaming
- localStorage para preferencias de UI
- Marked.js para renderizar markdown (vía CDN)

**Backend (1 archivo FastAPI, ~400 LOC):**
- FastAPI con dependency injection
- WebSocket endpoint `/ws/{project_id}` para streaming
- REST endpoints: `/api/v1/{conversations,messages,tags,search,inbox,projects}`
- OpenAPI auto en `/docs`

**Por qué tan simple:**
- El Osquestador NO es una SPA compleja
- Es un panel de control con 5 zonas fijas
- La complejidad está en el backend (los 12 adapters), no en la UI
- 1 archivo HTML se deploya en Cloudflare Pages en 1 click

---

## 8) PLAN DE IMPLEMENTACIÓN (orden)

1. **Stub HTML** con las 5 zonas vacías (puro layout, 1 archivo)
2. **Stub FastAPI** con los endpoints vacíos (retornan `{}`)
3. **Adapter LiteLLM** → el chat funciona con 1 modelo
4. **Adapter SQLite** → sidebar muestra proyectos
5. **Adapter Obsidian** → Zona 4 muestra documentos
6. **Adapter Kanboard** → Zona 4 muestra tareas
7. **Adapter Graphiti** → Zona 4 muestra grafo
8. **Adapter Haystack** → Zona 3 muestra resultados de búsqueda
9. **Adapter PaddleOCR** → drag&drop de PDFs funciona
10. **Adapter Telegram** → notificaciones en Zona 5
11. **Adapter Hermes** → slash commands en Zona 3
12. **Adapter Plandex** → planificación de tareas
13. **Adapter MCP** → expone todo como tools
14. **Adapter Neo4j** → backend de Graphiti
15. **Polishing** → estética final Claude/Anthropic
16. **Deploy** → Cloudflare Pages + VPS

**Total:** 16 pasos, ~1,600 LOC (ya estimado).

---

## 9) RESUMEN FINAL (1 frase)

**La interface del Osquestador es UN panel web con 5 zonas fijas (Sidebar + Header + Chat + Panel derecho + Status bar) que integra las interfaces de los 12 programas del spec detrás de adapters Python uniformes, consume todo via MCP + REST, y muestra el estado en vivo del orquestador con la estética de Claude.ai.**

Esperando tu OK para arrancar la programación.
