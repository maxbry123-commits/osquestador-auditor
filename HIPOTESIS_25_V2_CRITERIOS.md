# 25 Hipótesis de uso (V2) — con criterios de aceptación verificables

**Fecha**: 2026-07-18
**Paso**: 2/10 v2 (con criterios)

## H1: Chat multi-modelo simultáneo
**Acción**: Max selecciona 3 LLMs en paralelo.
**Criterio verificable**:
- [ ] Split-view 3-way visible en viewport ≥1280px
- [ ] Cada columna muestra: nombre modelo, provider, status, tokens contados
- [ ] Streaming sincronizado (no async start)
- [ ] Botón "save comparison" funcional

## H2: Memoria persistente cross-session
**Acción**: Max retoma proyecto 2 semanas después.
**Criterio**:
- [ ] Header muestra "Last session: X days ago, Y messages"
- [ ] Auto-recall de Graphiti inyecta top-5 entities
- [ ] Cada entity con X button para descartar
- [ ] Negative feedback loop a Graphiti

## H3: Input multimodal
**Acción**: Drag-drop 3 PDFs + 1 imagen.
**Criterio**:
- [ ] Pinned bar muestra miniaturas
- [ ] Hash SHA-256 visible por archivo
- [ ] Botón "send all" + "clear all"
- [ ] Validación tamaño (max 10MB)

## H4: Búsqueda unificada "D26"
**Acción**: Buscar "D26" en search bar.
**Criterio**:
- [ ] 4 tabs resultado: Decisión | Commit | Conversación | Skill
- [ ] Click cada tab abre resultado
- [ ] Latencia <500ms

## H5: Skills auto-creadas
**Acción**: 3+ usos de "/weather Madrid".
**Criterio**:
- [ ] Threshold 5 usos / 3 días
- [ ] Cooldown 7 días
- [ ] Diff visible antes de aceptar
- [ ] Botones Create/Edit/Dismiss

## H6: Watchdog loop
**Acción**: Configurar watchdog 60s en repo X.
**Criterio**:
- [ ] Status bar: "X ago, next in Y"
- [ ] Log live actualiza cada segundo
- [ ] Botón pause/resume
- [ ] Heartbeat log persiste

## H7: Vault estilo Obsidian
**Acción**: Crear nota con wikilink.
**Criterio**:
- [ ] Auto-complete dropdown para `[[`
- [ ] Wikilinks color azul accent
- [ ] Frontmatter YAML editable
- [ ] Daily note automático

## H8: Kanban drag-drop
**Acción**: Arrastrar card Backlog→Doing.
**Criterio**:
- [ ] Animación 200ms
- [ ] Optimistic UI (no espera servidor)
- [ ] Graphiti actualiza Task.status
- [ ] Rollback si falla

## H9: OCR automático
**Acción**: Upload foto con "/ocr".
**Criterio**:
- [ ] Progress 4-stage: Upload → PaddleOCR → BaiduOCR → Graphiti
- [ ] Output markdown
- [ ] Entidades linkeadas
- [ ] Latencia <5s

## H10: MCP bridge
**Acción**: Conectar 3 MCPs simultáneos.
**Criterio**:
- [ ] Status indicators en header (semáforo)
- [ ] Tools list en sidebar
- [ ] Reconnect con exponential backoff
- [ ] Health check cada 30s

## H11: Multi-proyecto
**Acción**: Cambiar entre 5 proyectos.
**Criterio**:
- [ ] Sidebar lista 5 proyectos
- [ ] Click cambia contexto (vault, tasks, memory)
- [ ] Header muestra nuevo nombre
- [ ] State bar "context switched"

## H12: Slash commands contextuales
**Acción**: `/deploy` en proyecto research-note.
**Criterio**:
- [ ] Aparece tachado con tooltip "Only in: webapp, api"
- [ ] Sugiere `/export`
- [ ] 50+ comandos totales
- [ ] Fuzzy search

## H13: Auto-save + version history
**Acción**: Modificar archivo vault.
**Criterio**:
- [ ] Sin botón "guardar" (auto)
- [ ] Version history accesible
- [ ] Diff side-by-side
- [ ] Botón rollback

## H14: Templates
**Acción**: Crear template `bug-report.md`.
**Criterio**:
- [ ] Frontmatter required badges
- [ ] `/new bug-report` pre-llena
- [ ] Live preview
- [ ] Save en `templates/`

## H15: Graph view interactivo
**Acción**: Click nodo en mini-graph.
**Criterio**:
- [ ] Archivo abre en chat
- [ ] Nodo se ilumina
- [ ] Edges animan
- [ ] Zoom/pan funcional

## H16: Telegram bridge
**Acción**: Max manda "hola" al bot.
**Criterio**:
- [ ] Panel recibe con badge "Telegram"
- [ ] Respuesta se envía al móvil
- [ ] Latencia <3s
- [ ] Thread continuo

## H17: Secretos seguros
**Acción**: Guardar OPENAI_API_KEY.
**Criterio**:
- [ ] Campo password enmascarado
- [ ] Botón "Test connection" antes save
- [ ] Storage `~/.osquestador/secrets/` chmod 600
- [ ] EXCLUIDO de git/backup

## H18: Health check watchdog
**Acción**: Graphiti se cae.
**Criterio**:
- [ ] Status bar cambia a "❌ Graphiti: refused"
- [ ] Botón "Restart" + log link
- [ ] Reintento 3x con backoff
- [ ] Alerta Telegram

## H19: Backups automáticos
**Acción**: Reloj llega 03:00.
**Criterio**:
- [ ] Status "Backup in progress 30%"
- [ ] Al terminar: "Saved 124MB → /backups/..."
- [ ] Retención 30 días
- [ ] RPO 6h

## H20: 9 modelos LLM
**Acción**: Click dropdown modelos.
**Criterio**:
- [ ] 9 modelos con metadata
- [ ] Filtros por provider
- [ ] Último usado marcado
- [ ] Status badge (OK/Error)

## H21: Slash commands UI
**Acción**: Escribir `/` en chat.
**Criterio**:
- [ ] Menu flotante 50+ comandos
- [ ] Fuzzy search en tiempo real
- [ ] Group headers
- [ ] Arrow keys + Enter

## H22: Agentes especializados
**Acción**: Click "Investigador" en sidebar.
**Criterio**:
- [ ] Header muestra "🤖 Investigador activo" (en texto, no emoji color)
- [ ] System prompt inyectado
- [ ] Chat cambia color sutil
- [ ] 9 tipos visibles

## H23: Diff visual para cambios
**Acción**: Modificar config.
**Criterio**:
- [ ] Diff verde/rojo antes aplicar
- [ ] Botones Apply/Cancel/Open full file
- [ ] Auto-save después Apply
- [ ] Rollback con Ctrl+Z

## H24: Dark mode único
**Acción**: Buscar toggle light/dark.
**Criterio**:
- [ ] Toggle NO existe
- [ ] Tooltip explica decisión arquitectónica
- [ ] Dark mode AAA contrast (7:1)
- [ ] Sin flash blanco en load

## H25: Export panel completo
**Acción**: `Cmd/Ctrl+Shift+E`.
**Criterio**:
- [ ] Descarga `osquestador-export-YYYYMMDD.tar.gz`
- [ ] Incluye index.html + assets + state.json
- [ ] Auto-guarda en `~/Downloads/`
- [ ] Import wizard restaura
