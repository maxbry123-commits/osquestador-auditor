# 25 Simulaciones de uso (V2) — con métricas de éxito

**Fecha**: 2026-07-18
**Paso**: 3/10 v2

## S1: Comparar 3 modelos
**Métrica éxito**:
- Latencia primer token: <800ms
- 3 columnas visibles sin overflow horizontal en 1280px
- Tokens contados en tiempo real
- Sincronización <50ms drift entre columnas
- Botón "save comparison" genera JSON descargable

## S2: Retomar proyecto 14 días después
**Métrica éxito**:
- Header renderiza en <100ms tras click
- Auto-recall de Graphiti: <500ms
- Top-5 entities inyectadas con relevance score >0.7
- X button en cada entity: 0ms response
- Negative feedback persiste a Graphiti

## S3: Drag-drop 5 archivos
**Métrica éxito**:
- Preview thumbnails en <200ms
- Hash SHA-256 calculado en <100ms por archivo
- Total barra: 5 items max
- Validación: archivos >10MB bloqueados con mensaje
- Botón "Send all" habilitado con todos válidos

## S4: Búsqueda "D26"
**Métrica éxito**:
- Latencia total búsqueda: <300ms
- 4 fuentes consultadas: SQLite FTS5 + GitHub API + Chroma + Graphiti
- 4 tabs visibles con resultados
- Click tab: render <50ms
- Falla graceful si fuente no disponible

## S5: Skill auto-creación
**Métrica éxito**:
- Threshold detection: 5 usos en 3 días rolling window
- Diff visible: side-by-side nuevo vs actual
- Botones: Create (1 click) / Edit (abre editor) / Dismiss (hidden 7d)
- Cooldown respetado
- Setting para disable

## S6: Watchdog loop
**Métrica éxito**:
- Poll cada 60s ± 5s jitter
- Status bar actualiza sin flicker
- Log live: <100ms latency
- Pause: 0 queries en pause
- Resume: catch-up en <5s
- Heartbeat log rotado diariamente

## S7: Crear nota con wikilink
**Métrica éxito**:
- Auto-complete: <50ms al escribir `[[`
- Sugerencias de archivos vault (max 10)
- Wikilink creado: color #3b82f6 (CSS var)
- Hover: underline
- Click: navega al archivo
- Backlink detection en archivo destino

## S8: Drag-drop tarea Kanban
**Métrica éxito**:
- Animación: 200ms cubic-bezier(0.4, 0, 0.2, 1)
- Optimistic UI: <16ms visual feedback
- Graphiti update: background, <2s
- Rollback: si falla >5s, revertir + toast
- Status indicator: "syncing" / "synced" / "failed"

## S9: OCR foto pizarra
**Métrica éxito**:
- Upload: <1s para 5MB
- PaddleOCR: <3s
- BaiduOCR (si cloud): <2s
- Graphiti index: <1s
- Total: <7s
- Output markdown con entidades [[linkeadas]]
- Confidence score visible

## S10: Conectar 3 MCPs
**Métrica éxito**:
- 3 conexiones simultáneas sin lag
- Status indicators: 🟢🟡🔴 (en texto + color)
- Reconnect: exponential backoff 1s/2s/4s/8s max 30s
- Health check: cada 30s
- Tools list agrupados por MCP
- Errores no derruban panel

## S11: Cambiar entre 5 proyectos
**Métrica éxito**:
- Click → <100ms cambio contexto
- Vault/tareas/memory/secretos: reloaded
- Header: nuevo nombre <50ms
- Status bar: pulse "context switched" 200ms
- Persist en localStorage

## S12: Slash command no disponible
**Métrica éxito**:
- `/deploy` tachado: <16ms
- Tooltip: 200ms delay show
- Sugerencia: top 3 alternativas por context
- 50+ comandos totales
- Fuzzy search: <50ms por keystroke

## S13: Editar config
**Métrica éxito**:
- Diff side-by-side: <200ms render
- Botones Apply/Cancel: enabled solo si cambios
- Apply: persist + toast confirmation
- Cancel: revert
- Version history: timestamps legibles
- Rollback: 1 click

## S14: Crear template
**Métrica éxito**:
- Editor con badges required
- Live preview: <100ms debounce
- Save: valida required fields
- `/new <template>` pre-llena
- Templates en `templates/` git-tracked

## S15: Click nodo graph
**Métrica éxito**:
- Archivo abre: <100ms
- Nodo highlight: pulse animation 600ms
- Edges: glow animation 400ms
- Pan to node si fuera de viewport
- Sidebar detail auto-update

## S16: Telegram bridge
**Acción**: Max manda "hola" al bot.
**Métrica éxito**:
- Panel recibe: <3s
- Badge "Telegram" con timestamp
- Respuesta: streaming en panel + enviada a móvil
- Thread continuo: history preservado
- Encrypted en tránsito

## S17: Guardar API key
**Métrica éxito**:
- Campo password enmascarado
- "Test connection" antes save: <2s
- File creado: `~/.osquestador/secrets/` chmod 600
- EXCLUIDO: backup, git, export
- Audit log de accesos

## S18: Health check falla
**Métrica éxito**:
- Graphiti caído: status cambia <30s
- "❌ Graphiti: connection refused (3 retries)"
- Botón "Restart" + log link
- Backoff: 1s, 2s, 4s, 8s, 16s
- Alerta Telegram
- Auto-restart a los 5min

## S19: Backup programado
**Métrica éxito**:
- Trigger: cron 03:00 daily
- Status "in progress 30%" <1s
- Al terminar: "Saved X MB → /backups/..."
- Compression: gzip
- Retention: 30 days local, 90 days cold
- RPO: 6h max data loss
- 3-2-1 backup strategy

## S20: Seleccionar modelo
**Métrica éxito**:
- 9 modelos con metadata
- Dropdown: <100ms open
- Filtros por provider: 5 grupos
- Último usado: badge "recent"
- Status: 🟢 OK / 🔴 Error / 🟡 Limited
- Keyboard nav: ↑↓ + Enter

## S21: Slash command menu
**Métrica éxito**:
- Menu flotante al escribir `/`
- 50+ comandos en 8 categorías
- Fuzzy search: <50ms por keystroke
- Group headers visibles
- Highlight match: bold + accent color
- Keyboard: ↑↓ + Enter + Esc
- Cmd+/ muestra todos

## S22: Activar agente
**Métrica éxito**:
- Sidebar tree colapsable
- Click activa: <100ms
- Header badge: "Investigador activo" (texto, no emoji color)
- Chat: sutil color tint del agente
- System prompt: injected <200ms
- 9 tipos + 52 agentes visibles
- Stats: count por tipo

## S23: Diff en config
**Métrica éxito**:
- Modificación: detectada <100ms
- Diff render: <200ms
- Verde/rojo: WCAG AA contrast
- Botones: Apply (accent blue) / Cancel (neutral) / Open full file
- Apply: persist + audit log
- Cancel: revert + toast

## S24: Toggle light/dark
**Métrica éxito**:
- Toggle NO existe (intencional)
- Tooltip en settings: "Decisión arquitectónica: dark mode reduce eye strain + server resources"
- Dark mode AAA: contrast 7:1
- Sin flash blanco (FOUC prevention)
- Preload dark theme

## S25: Export completo
**Métrica éxito**:
- `Cmd/Ctrl+Shift+E`: trigger
- Genera ZIP en <2s
- Contiene: index.html, assets/, state.json
- Auto-guarda en `~/Downloads/`
- Naming: `osquestador-export-20260718-HHMMSS.tar.gz`
- Import wizard: detecta + restaura
- Versioning semántico en state.json
