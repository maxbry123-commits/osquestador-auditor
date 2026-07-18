# PROTOTIPO OSQUESTADOR — 9 HTMLs
## Modelo visual de la interface con estética Anthropic
**Trigger de Max:** "me vas a presentar un modelo prototipo de la interface con todo lo que tienes anotado en github y mis instrucciones de como vas hacer los 9 pasos para hacer la interface y me muestras un modelo dividido en varios documentos htlm que muestre como va ser la interface"

**Fecha:** 2026-07-18 03:45
**Anotado en GitHub:** commit `5d7d685` (FASE 4.5 cerrada)
**Repo:** `maxbry123-commits/osquestador-auditor`

---

## LOS 9 PASOS DE LA INTERFACE

### Paso 1 — `01_login.html`
**Objetivo:** Pantalla de login con credenciales
- GitHub Personal Access Token (scope `repo`)
- Selector de proyecto (4 proyectos: osquestador-auditor, osquestador-memoria, agentes, openclaw)
- Selector de modelo LLM por defecto
- Token almacenado en `/root/.osquestador/secrets/` (chmod 600)

### Paso 2 — `02_layout_base.html`
**Objetivo:** Layout de 5 zonas fijas (CSS Grid)
- **Sidebar 280px** (izquierda)
- **Header 60px** (superior)
- **Chat central** (flexible)
- **Panel derecho 360px**
- **Status bar 32px** (inferior)
- Dark mode puro `#1a1a1a` + acento beige Anthropic `#d4a574`

### Paso 3 — `03_sidebar_proyectos.html`
**Objetivo:** Sidebar con 4 secciones
- ▣ Proyectos (4 items con badges de conteo)
- ⚡ 9 tipos de agentes (researcher, coder, writer, auditor, orchestrator, router, memory, watchdog, translator)
- 📊 Contador agentes 52/100 con barra de progreso
- 🏷 Tags activos (6 principales visibles)

### Paso 4 — `04_header_modelos.html`
**Objetivo:** Header con 9 modelos LLM
- Selector de modelo con ping latency en vivo
- Status pills: MCP · 3 servers + VPS · 95.111.232.89
- Avatar de usuario
- 9 modelos: Claude Sonnet 4.6, MiniMax-M3, DeepSeek V3.1, Gemini 2.5 Pro, gpt-oss-120b, Qwen3-235B, Llama-4-Maverick, GPT-5, Mistral-Large-2

### Paso 5 — `05_chat_inputblock.html`
**Objetivo:** Chat con 4 tabs + Input-block pinned bar
- 4 tabs simultáneos (Chat #1, #2, #3, #4 + "+ Nuevo")
- **Pinned bar fija** con candado 🔒 + hash SHA-256 truncado + tags
- Bubbles user/agent diferenciados (user = beige con borde naranja, agent = gris oscuro)
- Streaming animation con `▋` parpadeante
- Composer con textarea + botón send

### Paso 6 — `06_panel_derecho.html`
**Objetivo:** Panel derecho con 5 pestañas
- 📚 **Memoria** — vault + grafo + repo (tripartita HOT/WARM/COLD)
- 📄 **Docs** — archivos seleccionables (individual/grupo/folder)
- ✓ **Tareas** — Kanboard sync
- ⚡ **Skills** — 70 ideas integradas
- 📜 **Logs** — watchdog + cron + audit
- Filtros: solo verificados 🔒, sentence type, cross-project

### Paso 7 — `07_status_bar.html`
**Objetivo:** Status bar 32px con telemetría
- Tokens (12.4k / 200k) + barra
- Latencia en vivo
- SQLite WAL ✓ + FAISS vectores + Neo4j nodos
- Backup último + Watchdog uptime
- MCP servers + VPS + Disco + RAM
- Input-blocks verificados (247) + hash-chain OK

### Paso 8 — `08_input_block_modal.html`
**Objetivo:** Modal accesible de confirmación
- `role="dialog"` + `aria-modal="true"` + `aria-labelledby`
- Muestra: block_id (SHA-256), sentence_type, source, tags, priority
- **Content verbatim preservado** (caja con borde naranja izquierdo)
- **Integrity check:** SHA-256 verificado + append-only + no_update_inputs trigger
- 3 botones: Descartar / Editar / Confirmar y enviar

### Paso 9 — `09_panel_completo.html` ⭐
**Objetivo:** TODO integrado en 1 HTML funcional
- Las 5 zonas conectadas
- Header + Pinned bar + Chat + Panel + Status
- Composer abajo
- Sidebar completo
- Estética Anthropic exacta (dark mode + acento beige)

---

## CÓMO USAR LOS 9 HTMLs

### Localmente
1. Abre `01_login.html` en el navegador
2. Click "Entrar →" te lleva a `02_layout_base.html`
3. Sigue los pasos del 1 al 9 haciendo click en los links
4. El paso 9 (`09_panel_completo.html`) es el modelo final integrado

### Para producción (FASE 5)
1. Los 9 HTMLs se consolidan en 1 solo `panel_osquestador_final.html`
2. Se conecta con FastAPI backend (800 LOC) en `http://localhost:8000`
3. WebSocket para streaming de chat
4. MCP server expone 7 tools del Osquestador

---

## FUNCIONES UI ABIERTAS (window.osquestador)

```js
window.osquestador = {
  search: (query) => { /* buscar en vault + grafo + repo */ },
  routing: (target, payload) => { /* route a agente/modelo */ },
  openModal: (modalId) => { /* abrir modal accesible */ },
  selectFiles: (mode) => { /* individual/grupo/folder */ },
  sendMessage: (inputBlock) => { /* enviar input-block al kernel */ },
  getState: () => { /* estado actual del panel */ }
};
```

---

## ESTÉTICA ANTHROPIC EXACTA

- **Dark mode puro:** `#1a1a1a` background, `#232323` paneles, `#2e2e2e` borders
- **Texto:** `#e8e8e8` primary, `#9a9a9a` secondary
- **Acento:** `#d4a574` (naranja/beige Anthropic)
- **Tipografía:** SF Pro Display / system-ui
- **Espaciado:** generoso, minimalista
- **Emoji:** minimalista, sin colores brillantes
- **Sin gradientes**, sin shadows pesados, bordes finos 1px

---

## BINARIO / AUTO-RUN

El usuario final solo hace:
```bash
pip install osquestador
osquestador
```

Y se abre automáticamente el panel HTML con FastAPI backend conectado.

---

## ESTADO

- ✅ 9 HTMLs creados en `/prototipo/`
- ✅ Estética Anthropic (dark mode + beige)
- ✅ 5 zonas fijas
- ✅ Input-block pinned bar con SHA-256
- ✅ Modal accesible (role=dialog)
- ✅ Composer con streaming animation
- ✅ Sidebar con 9 tipos agentes + 52/100 contador
- ✅ Header con 9 modelos LLM
- ✅ Panel derecho 5 pestañas
- ✅ Status bar con telemetría
- ✅ OpenClaw INTACTO (REGLA #0)

**Próximo:** FASE 5 — ensamblar el FastAPI backend (800 LOC) + conectar con MCP + VPS.
