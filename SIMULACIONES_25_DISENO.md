# 25 Simulaciones de Diseño

**Fecha**: 2026-07-18
**Paso**: 6/10

## D1: Sidebar vacío
Vista: Solo logo + botón "+ Nuevo" + 0 proyectos. Empty state minimal: texto "No projects yet" + CTA "+ Create your first".

## D2: Sidebar 20 proyectos
Vista: Lista scroll vertical, status badges (🟢🟡🔴), search arriba filtra en tiempo real, colapsable por status.

## D3: Sidebar mobile
Vista: Bottom sheet que sube con tap. Lista de proyectos full-width, status indicator grande. Close button arriba derecha.

## D4: Header minimal
Vista: 60px alto. Logo serif izquierda, proyecto center, modelo LLM dropdown, MCP status, avatar. Sin decoración.

## D5: Header modelo error
Vista: Dropdown muestra "❌ Cerebras: 401". Click → modal de configuración. Otros modelos funcionan normalmente.

## D6: Chat con 1 modelo
Vista: Burbujas full-width, user derecha (gris oscuro), asistente izquierda (negro puro). Avatar circular. Copy button hover.

## D7: Chat con 3 modelos split
Vista: 3 columnas 33% cada una. Header de cada col: modelo + status + tokens. Sync start, async stream.

## D8: Chat input
Vista: Textarea autosize 1-6 líneas. Pinned bar arriba con attachments. Slash command menu flotante al escribir `/`. Send button right.

## D9: Pinned bar 5 archivos
Vista: Lista horizontal scroll. Cada item: thumbnail/icon + nombre + size + X. Botón "Send all" verde. "Clear all" rojo.

## D10: Pinned bar con error
Vista: 4 archivos OK + 1 con ⚠️ rojo. Tooltip: "File too large (15MB > 10MB)". X para remover.

## D11: Panel derecho 5 tabs
Vista: Tabs: Memoria | Documentos | Tareas | Skills | Logs. Activo con underline azul. Iconos monocromáticos.

## D12: Tab Memoria con grafo
Vista: Mini-graph interactivo. Nodos = entidades, edges = relaciones. Zoom/pan. Click nodo = sidebar detail.

## D13: Tab Documentos
Vista: Lista virtual scroll. Cada item: nombre, fecha mod, size, tag. Click = abre en chat. Drag = añade a input.

## D14: Tab Tareas Kanban
Vista: 3 columnas. Cards con title + status + assignee. Drag-drop animado. Optimistic update con rollback.

## D15: Tab Skills
Vista: Grid de cards. Cada skill: nombre, descripción corta, count usos. Click = expande con metadata. "+ Add" button.

## D16: Tab Logs live
Vista: Stream de eventos con timestamp. Color por tipo: info (gris), warn (amarillo sutil), error (rojo sutil). Filter dropdown.

## D17: Status bar
Vista: 32px alto. Items: tokens hoy | latencia | SQLite size | próximo backup | watchdog. Color verde si todo OK.

## D18: Status bar error
Vista: Watchdog muestra ❌ rojo. Click → modal con detalle + botón "Restart". Otros items siguen funcionando.

## D19: Modal genérico
Vista: Overlay oscuro 60% opacity. Card centrado max 600px. Header con title + X. Body con form. Footer con Cancel + Action.

## D20: Modal accesible
Vista: `role="dialog" aria-modal="true" aria-labelledby="title"`. Focus trap. Escape cierra. Click overlay cierra.

## D21: Toast notification
Vista: Bottom-right stack. Auto-dismiss 5s. Action button opcional. Icon + texto + close X.

## D22: Dropdown modelo
Vista: Click header abre lista. Cada item: nombre, provider, max tokens, $/M, status badge. Filtros por provider. ↑↓ nav.

## D23: Slash command menu
Vista: Flota sobre input. 50+ comandos. Fuzzy search. Highlight match. Group headers. Arrow keys + Enter.

## D24: Empty graph
Vista: Mini-graph con 0 nodos. Texto "Build your knowledge graph by chatting". CTA "Learn more".

## D25: Loading state
Vista: Skeleton loaders gris oscuro pulsando. Shimmer effect. No spinner genérico (anti-pattern).
