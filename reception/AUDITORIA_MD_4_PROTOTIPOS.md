# AUDITORÍA 4/5 — PROTOTIPOS UI (V1 a V12) + IDEAS + DECISIONES

**Fecha**: 2026-07-19 21:30
**Modo SHERIFF v8.2**: input-block-reader literal
**Trigger**: Max "audita lo que tengas sobre el osquestador... 5 Documentos máximo"

---

## 1. EVOLUCIÓN DE LOS 12 PROTOTIPOS

| Versión | Archivo | Tamaño | Highlights | Estado |
|---|---|---|---|---|
| v1 | prototipo/G_*.html | ~12KB | 8 HTMLs estáticos | DEPRECADO |
| v2 | prototipo_v2/G_*.html | ~14KB | 8 mobile-first | DEPRECADO |
| v4 | prototipo_v4/AUDITORIA_V4.md + DESIGN_TOKENS.md | ~16KB | Design tokens | DEPRECADO |
| v5 | prototipo_v5/ | ~22KB | Dark mode v1 | DEPRECADO |
| v6 | prototipo_v6/ | ~25KB | iOS HIG v1 | DEPRECADO |
| v7 | prototipo_v7/ | ~28KB | Matching foto Max | DEPRECADO |
| v8 | prototipo_v8/ | ~31KB | iOS drawer + scrim | DEPRECADO |
| v9 | prototipo_v9/ | ~34KB | UI Claude mobile | DEPRECADO |
| v10 | prototipo_v10/ | ~36KB | Dark mode exacto | DEPRECADO |
| v10b | prototipo_v10b/ | ~38KB | Grey #202124 Chrome | DEPRECADO |
| **v11** | **prototipo_v11/index.html** | **39KB** | **Anthropic cream/dark + 5 zonas** | **CERTIFICADO** |
| **v12** | **prototipo_v12/index.html** | **45KB** | **+10 correcciones V11 + kbd + toast** | **CERTIFICADO** |

---

## 2. PROTOTIPO V11 (BUCLE 5) — `prototipo_v11/index.html`

### 5 zonas fijas (per spec)
- **Sidebar 280px** con 4 proyectos + 9 agentes + filtros
- **Header 60px** con logo + breadcrumb + search + acciones + avatar
- **Main centro** con dashboard / artefactos / chat / api
- **Right panel 320px** con 4 tabs (Memoria / Documentos / Tareas / Logs)
- **Status bar 32px** con 7 métricas live

### Design system
- Background cream `#FAF9F5` (light) / `#0D0D0F` (dark)
- Accent `#CC785C` (Anthropic oficial)
- Tipografía: Fraunces (serif headings) + Inter (sans body) + JetBrains Mono (data)
- Geometry: iOS HIG (radius 14-18, shadow 0 1px 2px)
- SF Symbols SVG inline (30+ iconos)

### Componentes
- Modal bandeja Anthropic con 3 tabs (Conocimiento / Nuevo proyecto / Configuración)
- File rows iOS (icono 28x28 + nombre + meta + chevron `>`)
- iOS toggle animado 44x26
- Multi-select tabs (Individual / Grupo / Folder)
- Composer con auto-grow + slash commands
- `window.osquestador` 7 funciones expuestas
- @agente routing dispatch
- Mobile drawer con translateX + scrim blur

### 8 screenshots V11 (Playwright)
- V11_desktop_light.png (1280x800 cream)
- V11_desktop_dark.png (1280x800 dark)
- V11_desktop_light_proj.png (project change state)
- V11_bandeja_modal.png (modal 3 tabs Anthropic)
- V11_api_window.png (7 funciones window)
- V11_chat_slash.png (/memory status composer)
- V11_mobile_dashboard.png (390x844 responsive)
- V11_mobile_drawer.png (drawer + scrim)

### Audit score V11: **57%** del spec cumplido
- ✅ Interface visual 100%
- ⚠️ Backend 5% (1 workflow, 5 adapters in-process)
- ❌ MCP server, systemd, binario pip install

---

## 3. PROTOTIPO V12 (BUCLE 7-8) — `prototipo_v12/index.html` (REDISEÑO)

Aplica las 10 refutaciones del BUCLE 7 sobre V11:

### REF-11 — Scrim con backdrop blur real
```css
.scrim {
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}
```
iOS HIG: contenido detrás debe quedar "atrás", no solo cubierto.

### REF-12 — kbd shortcuts (Cmd+N abre, Esc cierra)
```js
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'n') { e.preventDefault(); openBandeja(); }
  if (e.key === 'Escape') { closeBandeja(); closeToast(); }
});
```

### REF-13 — Token counter live en composer
```js
function updateTokenCount(el) {
  const tokens = Math.ceil(el.value.length / 4);
  document.getElementById('token-count').textContent = tokens.toLocaleString() + ' / 200K';
}
```

### REF-14 — 9 agentes con onclick funcional
```js
function openAgent(name) {
  showView('chat');
  const input = document.getElementById('chat-input');
  input.value = '@' + name + ' ';
  input.focus();
  showToast('Agente ' + name, 'Conectado y listo', 'Ver');
}
```

### REF-15 — Breadcrumb + URL routing
```js
function selectProject(el) {
  history.pushState({p: el.dataset.project}, '', '/p/' + el.dataset.project);
  ...
}
```

### REF-16 — Filtro Todos/Activos/Archivados persistente
```js
function setFilter(f, btn) {
  document.querySelectorAll('.sidebar__project').forEach(p => {
    const status = p.dataset.status;
    p.classList.toggle('is-hidden', f !== 'all' && status !== f);
  });
  localStorage.setItem('osq.filter', f);
}
```

### REF-17 — Crear proyecto persiste en localStorage
```js
function createProject() {
  const name = document.getElementById('np-name').value.trim();
  const sdks = Array.from(...).map(c => c.value);
  const projs = JSON.parse(localStorage.getItem('osq.projects') || '[]');
  projs.push({name, sdks, ts: Date.now()});
  localStorage.setItem('osq.projects', JSON.stringify(projs));
  // append to sidebar
}
```

### REF-18 — Theme sync entre tabs
```js
window.addEventListener('storage', (e) => {
  if (e.key === 'theme') {
    if (e.newValue === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    else document.documentElement.removeAttribute('data-theme');
  }
});
```

### REF-19 — Search global con toast
```js
function search(form) {
  const q = document.getElementById('global-search').value.trim();
  showToast('Búsqueda: "' + q + '"', '3 hits local · 12 BM25 · 5 git', 'Ver');
}
```

### REF-20 — Greeting dinámico por hora
```js
function setGreeting() {
  const h = new Date().getHours();
  let g = 'Hola';
  if (h >= 5 && h < 12) g = 'Buenos días';
  else if (h >= 12 && h < 19) g = 'Buenas tardes';
  else g = 'Buenas noches';
  document.getElementById('greeting').innerHTML = g + ', <em>Max</em>';
}
```

### 7 screenshots V12 (Playwright)
- V12_desktop_light.png (cream)
- V12_desktop_dark.png (#0D0D0F + "Buenas noches Max")
- V12_api.png (7 funciones window.osquestador)
- V12_bandeja.png (modal Anthropic 3 tabs)
- V12_chat_tokens.png (composer con contador)
- V12_mobile_dashboard.png (390x844)
- V12_mobile_drawer.png (drawer + scrim)

### Audit score V12: **57%** (igual que V11 — el rediseño es UI, no agrega backend)

---

## 4. TABLA DE 70 IDEAS INTEGRADAS (`TABLA_IDEAS_INTEGRADAS.md`)

70 ideas divididas en 7 fuentes de 10 ideas cada una:

### 1. HERMES (Nous Research) — 10 ideas
1. AIAgent como librería Python
2. Async subagents nativos
3. Code execution sandboxed
4. Save trajectories JSONL para replay
5. Skill format SKILL.md
6. load_skill() runtime
7. Context windowing automático
8. Error recovery con reintentos
9. Plugin marketplace ClawHub
10. CLI + TUI dual interface

### 2. OPENCLAW — 10 ideas
1. ClawHub marketplace de skills
2. 5 channels built-in
3. "Mayordomo pattern" — agente central despacha
4. WS protocol puerto 18789
5. INTACTO REGLA #0
6. Agent registry JSON
7. Capability-based security
8. Memory tiers (working/long-term/scratch)
9. Streaming SSE nativo
10. JSON-RPC 2.0 sobre WS

### 3. CLAUDE CODE OFICIAL — 10 ideas
1. SKILL.md spec (frontmatter YAML + body markdown)
2. Progressive disclosure (3 niveles)
3. 12 hooks lifecycle
4. Subagents con Task tool + depth cap
5. Agent Progress Canvas
6. Intervention controls
7. Context Preservation
8. Transparency (verbose mode)
9. Multi-Agent Tabs
10. Supervisor pattern

### 4. MEMORY PATTERNS — 10 ideas
1. Vault = filesystem markdown + frontmatter + wikilinks
2. 5 CTX files: aboutme, now, Work, project, systems
3. BM25 + vector hybrid con RRF
4. 90 días TTL WARM
5. Prune-over-append retention
6. Memory tiering HOT/WARM/COLD
7. Search on-connect
8. Web search fallback
9. Git historical memory
10. Hot/Warm/Cold memory cache (HWC)

### 5. SUB-AGENTS — 10 ideas
1. Orchestrator-worker topology
2. ACP (Agent Communication Protocol) primitives
3. Depth cap = 5
4. A2A (Agent-to-Agent) protocol
5. Subagent context isolation
6. Task delegation con scopes
7. TTL por subagent
8. Max budget per subagent
9. State passing via context
10. Error escalation paths

### 6. CHECKPOINT — 10 ideas
1. SQLite-first, journal_mode=WAL
2. Idempotency keys
3. 4 primitives: save, load, list, delete
4. Resume desde workflow_id + step_id
5. Dead letter queue
6. Circuit breaker
7. Atomic_write_json
8. Graceful shutdown SIGTERM
9. Reintentos con exponential backoff
10. Health.json refrescado

### 7. CHECKPOINT PUNTO 4 V2 — 10 ideas
1. Triple background (nohup/tmux/systemd)
2. systemd Type=notify
3. WatchdogSec=30s
4. restic + S3 backup
5. 3-2-1-1-0 rule
6. RPO 6h
7. Watchdog interno Python
8. .env chmod 600 excluido de backup
9. WORM append-only bucket
10. Cross-region replication

---

## 5. TABLA DE 25 DECISIONES ARQUITECTÓNICAS (`TABLA_DECISIONES_ARQUITECTONICAS.md`)

Cubierto en `AUDITORIA_MD_1_NUCLEO.md` sección 2.

---

## 6. UI vs BACKEND — Clasificación 70+25 ideas (per spec instrucción 8)

### 11 Ideas UI
- Agent Progress Canvas (Claude Code)
- Proactive UI
- Intervention controls
- Multi-Agent Tabs
- Generative UI
- Hybrid Input
- iOS HIG patterns
- Anthropic Claude.ai patterns
- Material Design 3 elevation
- Fluent 2 mica/acrylic
- SF Symbols SVG

### 14 Ideas Backend
- Kernel pequeño 500 LOC
- 5-10 plugins intercambiables
- MCP server 7 tools
- 4 workflows (ingesta, auditoria, arbol, taskindex)
- Atomic_write_json state
- SQLite WAL
- FAISS MiniLM-L6-v2 vector
- BM25 SQLite FTS5
- LiteLLM 5 providers
- Triple background (nohup/tmux/systemd)
- Watchdog interno
- restic backup
- WORM append-only
- 3-2-1-1-0 rule

### Funciones abiertas MCP
- `memoria_commit` / `memoria_log` / `memoria_diff` / `memoria_blame`
- `memoria_checkout` / `memoria_branch` / `memoria_merge`
- `osquestador_search_hybrid` / `osquestador_search_keyword` / `osquestador_search_vector` / `osquestador_search_recent` / `osquestador_search_tags`
- `osquestador_collections_list`
