# SKILL: Panel UI con estética Claude / Anthropic (solo modelo visual)

## Objetivo
Construir la **interfaz de control del Orquestador** (HTML/CSS/JS estático, deployable en Cloudflare Pages) usando **únicamente el modelo visual** (paleta, tipografía, layout, jerarquía) de las fotos de Claude.ai / Anthropic Console y del HTML `654156ca`/`29fc122d`. **NO replicar funciones de router, conexiones, o cualquier UI ajena al orquestador.**

## Contexto
Investigación consolidada en `INVESTIGACION.md` sección 24 + fotos de Max en `docs/fotos/`.
Patrón validado por Anthropic (Apple HIG dark mode, claude-visual-style-guide) + jcmrs.

## Entradas
- Foto de Claude.ai Project (sidebar, artefactos, conectores).
- Foto de Anthropic Console (agente.minimax.io).
- HTML de referencia `docs/referencias/router-v1-lista.html`, `tarea-1-1.html`, `panel_router_3.html` (SOLO estética).
- MCP server del Orquestador en `127.0.0.1:8765`.

## Procedimiento

### 1. Extraer SOLO el modelo visual
**Conservar:**
- Paleta exacta: fondo `#0D0D0F`, cards `#1F1E1B`, texto `#F2EBD9`, gris `#B8B0A0`, azul `#3B82F6`, verde OK `#7FD1A8`, rojo `#FF3B30` (acento).
- Tipografía: **Fraunces** (serif para headings + numerales grandes) + **Inter** (sans para body).
- Cards redondeadas 18px, padding generoso, bordes sutiles `rgba(255,255,255,0.08)`.
- Switch on/off estilo iOS (36×20, knob blanco 16×16).
- Densidad media (no saturado, respirado).
- Jerarquía: H1 serif grande, body sans pequeño, labels uppercase 11px tracking 0.15em.

**PROHIBIDO:**
- Copiar funciones de router (toggle, search, filtro, eliminar, duplicar).
- Copiar nombres de items (GitHub, HuggingFace, etc.) — esos son del router viejo.
- Copiar la UI del "Conectar Mobile", "Skills", "Scheduled" — son de Claude, no nuestras.
- Replicar la pantalla de Artefactos con archivos tipo `DOC1 BOMBILL...` — son del proyecto viejo de Max.

### 2. Arquitectura del panel (nuestra, no del router)
```
+----------------------------------------------+
|  OpenClaw  ·  M3  ·  Chat                    |  ← header (breadcrumb + model selector)
+----------------------------------------------+
|  📊 Docs: 47 | Conflictos: 3 | Tareas: 12   |  ← summary bar
+----------------------------------------------+
|  Estado del Orquestador                      |
|  ┌──────────────┬──────────────┬──────────┐  |
|  │  Health      │  Heartbeat   │  Latency │  |
|  │  🟢 alive    │  hace 2s     │  45ms    │  |
|  └──────────────┴──────────────┴──────────┘  |
+----------------------------------------------+
|  Documentos del proyecto                     |
|  ┌────────────────────────────────────────┐  |
|  │  📄 DOC1.md · auditado · 4.2KB         │  |
|  │  📄 DOC2.md · conflicto · 1.8KB        │  |
|  │  📄 BOMBIL... · pendiente · 6.1KB      │  |
|  └────────────────────────────────────────┘  |
+----------------------------------------------+
|  Conflictos abiertos                         |
|  ┌────────────────────────────────────────┐  |
|  │  ⚠ abc vs def (sim 0.85)               │  |
|  │  [A] [B] [FUSION]                      │  |
|  └────────────────────────────────────────┘  |
+----------------------------------------------+
|  Tareas pendientes                           |
|  ┌────────────────────────────────────────┐  |
|  │  ○ [maxbry] objetivo X (DEFINIR)        │  |
|  │  ○ [maxbry] decidir provider OCR        │  |
|  └────────────────────────────────────────┘  |
+----------------------------------------------+
|  Conexiones (MCP + VPS + Memoria)            |
|  ┌─────────────┬─────────────┬───────────┐  |
|  │  MCP server │  VPS health │  Memoria  │  |
|  │  🟢 4 tools │  🟢 alive   │  🟢 47 ev │  |
|  └─────────────┴─────────────┴───────────┘  |
+----------------------------------------------+
|  Chat AI: enviarMensajeChat()                |
|  ┌────────────────────────────────────────┐  |
|  │  tú: estado del proyecto               │  |
|  │  ai: ...                               │  |
|  │  [____________________________] [enviar]│  |
|  └────────────────────────────────────────┘  |
+----------------------------------------------+
```

### 3. Conexión con el Orquestador
- Cargar el HTML como estático.
- JS hace fetch a `http://127.0.0.1:8765/mcp` con JSON-RPC 2.0.
- Si CORS bloquea, deploy el panel vía Cloudflare Pages + el orquestador accesible por tunnel.
- Streaming con SSE para respuestas largas (opcional, requiere que el quick tunnel soporte SSE — usar polling cada 5s como fallback).

### 4. Deploy
- Build: no build (HTML estático).
- Deploy: `wrangler pages deploy panel/ --project-name=osquestador-panel`.
- URL: `https://osquestador-panel.pages.dev`.

## Reglas
- ✅ Usar SOLO el modelo visual (paleta, tipografía, layout) de las fotos.
- ✅ El panel consume el MCP server del Orquestador (no el de OpenClaw).
- ✅ Responsive: mobile-first (max-width 520px) + desktop.
- ✅ Dark mode por defecto (no toggle — la app es dark only como Claude).
- ❌ NUNCA copiar funciones del router viejo.
- ❌ NUNCA importar librerías pesadas (React, Vue) — vanilla JS, max 50 KB.
- ❌ NUNCA hardcodear keys o secrets en el HTML (van en el MCP server).

## Restricciones
- Tamaño del HTML + CSS + JS: < 100 KB.
- Carga inicial: < 1s en 4G.
- Requests al MCP: max 1 por segundo, con cache de 5s.
- Sin frameworks externos (vanilla JS).

## Ejemplos

### Paleta CSS
```css
:root {
  --n: #0D0D0F;        /* fondo */
  --c: #1F1E1B;        /* card */
  --c2: #252320;       /* card elevated */
  --b: rgba(255,255,255,0.08);  /* border */
  --w: #F2EBD9;        /* texto principal */
  --g: #B8B0A0;        /* texto gris */
  --gd: #7E776B;       /* label */
  --az: #3B82F6;       /* azul */
  --ok: #7FD1A8;       /* verde OK */
  --r: 18px;           /* radius */
  --serif: 'Fraunces', serif;
  --sans: 'Inter', sans-serif;
}
```

### Card típica
```html
<div class="card">
  <span class="label">Documento</span>
  <h3 class="title">DOC1.md</h3>
  <span class="status ok">auditado</span>
</div>
```

### Fetch MCP
```js
async function mcpCall(method, params) {
  const r = await fetch('http://127.0.0.1:8765/mcp', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      jsonrpc: '2.0', id: Date.now(), method, params
    })
  });
  const j = await r.json();
  return j.result || j.error;
}
```

## Fuentes
- Apple HIG Dark Mode — https://developer.apple.com/design/human-interface-guidelines/dark-mode/
- claude-visual-style-guide — https://github.com/jcmrs/claude-visual-style-guide
- dark-mode-ui-designer skill — https://mcpmarket.com/tools/skills/dark-mode-ui-designer
- HTML `654156ca` (Max) — fondo `#0D0D0F`, Fraunces+Inter, cards 18px
- HTML `29fc122d` (Max) — modelo de panel con cards múltiples
- Fotos `docs/fotos/01-07` — patrón de Claude.ai sidebar + artefactos + conectores

## Dependencias
- Vanilla HTML/CSS/JS (sin frameworks)
- Google Fonts: Fraunces + Inter
- MCP server del Orquestador

## Cuándo utilizar
- Construir el panel de control del Orquestador.
- Construir cualquier UI tipo Claude/Anthropic para los proyectos de Max.
- Reutilizar la paleta/tipografía para futuras interfaces del ecosistema.

## Cuándo NO utilizar
- Para UI que no sea del Orquestador (usar la skill que corresponda).
- Para móvil nativo (usar skill de iOS Dev).
- Para UI que requiera interactividad compleja (usar framework).

## Relación con otros Skills
- `SKILL_orquestador_kernel.md` — el panel es el frontend del kernel.
- `SKILL_mcp_integration.md` — el panel consume el MCP server.
- `SKILL_memoria_avanzada.md` — el panel muestra la memoria.
- `SKILL_evidence_collect.md` — el panel captura evidencia de uso.

## Versión
v1.0 — 2026-07-17 · Mavis.

## Historial
- v1.0 — extracción del modelo visual de las fotos de Max + Apple HIG + claude-visual-style-guide.
