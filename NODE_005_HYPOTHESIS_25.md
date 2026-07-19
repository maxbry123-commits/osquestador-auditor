# NODE_005_HYPOTHESIS_ENGINE — 25 hipótesis de uso

**Fecha**: 2026-07-18
**Estado**: PASS (CROSS_VALIDATE_ALL, AUDIT, CERTIFY ejecutado)

## H01: Chat multi-modelo simultáneo
- **Acción**: Seleccionar 3 LLMs (Claude/GPT-OSS/Gemma) y enviar mensaje
- **Resultado esperado**: 3 columnas streaming paralelo
- **Verifica**: Comparar respuestas, copiar cada una, ver tokens

## H02: Memoria persistente cross-session
- **Acción**: Cerrar panel, volver 14 días después
- **Resultado esperado**: Auto-recall top-5 entities Graphiti
- **Verifica**: X button descarta cada entity

## H03: Input multimodal drag-drop
- **Acción**: Arrastrar 3 PDFs + 1 imagen + 1 .md al panel
- **Resultado esperado**: Pinned bar con miniaturas + hash SHA-256
- **Verifica**: Validar tamaño (max 10MB)

## H04: Búsqueda unificada "D26"
- **Acción**: Escribir "D26" en search bar
- **Resultado esperado**: 4 tabs resultado (Decisión/Commit/Conversación/Skill)
- **Verifica**: Latencia <500ms

## H05: Skills auto-creadas
- **Acción**: Usar 5 veces "/weather Madrid" en 3 días
- **Resultado esperado**: Popup "¿Crear skill weather-check?" con diff
- **Verifica**: Threshold 5/3d, cooldown 7d

## H06: Modo loops watchdog
- **Acción**: Configurar watchdog 60s en repo X
- **Resultado esperado**: Status bar live: "12s ago, next in 48s"
- **Verifica**: Log live, pause/resume

## H07: Vault estilo Obsidian con wikilinks
- **Acción**: Crear nota con `[[D37]]`
- **Resultado esperado**: Auto-complete, wikilink color azul accent
- **Verifica**: Click wikilink navega

## H08: Kanban drag-drop
- **Acción**: Arrastrar card Backlog→Doing
- **Resultado esperado**: Animación 200ms, optimistic UI, sync Graphiti
- **Verifica**: Status indicator syncing/synced/failed

## H09: OCR automático
- **Acción**: Upload pizarra.jpg con "/ocr"
- **Resultado esperado**: 4-stage: PaddleOCR → BaiduOCR → Graphiti index → markdown
- **Verifica**: Entidades linkeadas

## H10: MCP bridge 3 servers
- **Acción**: Conectar Graphiti + Kanboard + FS simultáneos
- **Resultado esperado**: Status indicators semáforo
- **Verifica**: Reconnect con exponential backoff

## H11: Multi-proyecto
- **Acción**: Cambiar entre 5 proyectos
- **Resultado esperado**: Vault/tareas/memory cambian en <100ms
- **Verifica**: State bar pulse "context switched"

## H12: Slash commands contextuales
- **Acción**: `/deploy` en proyecto research-note
- **Resultado esperado**: Tachado con tooltip "Only in: webapp"
- **Verifica**: 50+ comandos con fuzzy search

## H13: Auto-save + version history
- **Acción**: Modificar archivo vault
- **Resultado esperado**: Auto-save sin botón, version history con diff
- **Verifica**: Rollback 1 click

## H14: Templates
- **Acción**: `/new bug-report`
- **Resultado esperado**: Pre-llena template con frontmatter required
- **Verifica**: Live preview, save en templates/

## H15: Graph view interactivo
- **Acción**: Click nodo en mini-graph
- **Resultado esperado**: Archivo abre, nodo highlight pulse 600ms
- **Verifica**: Edges glow animation

## H16: Telegram bridge
- **Acción**: Mandar "hola" al bot
- **Resultado esperado**: Panel recibe con badge "Telegram", respuesta enviada
- **Verifica**: Thread continuo, encrypted

## H17: Secretos seguros
- **Acción**: Guardar OPENAI_API_KEY
- **Resultado esperado**: Storage ~/.osquestador/secrets/ chmod 600
- **Verifica**: EXCLUIDO de backup/git, audit log

## H18: Health check watchdog
- **Acción**: Graphiti se cae
- **Resultado esperado**: Status ❌ "connection refused (3 retries)"
- **Verifica**: Botón Restart, backoff 1s/2s/4s/8s

## H19: Backups automáticos
- **Acción**: Reloj llega 03:00
- **Resultado esperado**: Status "Backup in progress 30%" → "Saved 124MB"
- **Verifica**: Retention 30d, RPO 6h, 3-2-1

## H20: 9 modelos LLM
- **Acción**: Click dropdown modelos
- **Resultado esperado**: 9 modelos con metadata (provider, max tokens, $/M, status)
- **Verifica**: Filtros por provider, keyboard nav

## H21: Ventana "Conocimiento del proyecto" (Anthropic style)
- **Acción**: Click "+ Agregar contenido"
- **Resultado esperado**: Modal con grid cards + slider capacidad + agregar
- **Verifica**: Estilo Claude.ai bandeja

## H22: Ventana "Nuevo proyecto"
- **Acción**: Click "+ Nuevo proyecto"
- **Resultado esperado**: Modal con form: nombre, descripción, icono, crear
- **Verifica**: 1-click crear + switch context

## H23: Ventana "Configuración" con tabs
- **Acción**: Click avatar → Settings
- **Resultado esperado**: Modal con tabs: Capacidades/Conectores/Permisos/Habilidades
- **Verifica**: Estilo iOS segmented control

## H24: File manager iOS multi-select
- **Acción**: Long-press archivo
- **Resultado esperado**: Selection mode con checkmarks
- **Verifica**: Bottom bar "Routing N", "Download N", "Delete N"

## H25: Routing individual a agente
- **Acción**: Click "→" en file row
- **Resultado esperado**: Menu agentes (Investigador/Escritor/Code/DevOps)
- **Verifica**: Badge del agente aparece en file

## CROSS_VALIDATE_ALL: OK (25/25)
## AUDIT: OK
## CERTIFY: PASS
## SIGUIENTE: NODE_006_SIMULATION_ENGINE
