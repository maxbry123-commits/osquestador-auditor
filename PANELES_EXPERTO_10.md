# 10 Paneles de Experto en Diseño (lectura 10x GitHub)

**Fecha**: 2026-07-18
**Paso**: 5/10
**Docs leídos 10x**: FUENTE_DE_VERDAD, PLAN_INTERFACE_INTEGRADA, INPUT_BLOCK_READER, INVESTIGACION_29_PASADAS, CORRECCIONES_ESTETICA, SKILL_panel_ui, BITACORA, INSTRUCCIONES, TABLA_DECISIONES, TABLA_IDEAS

## Panel 1: Experto UX Research (Jakob Nielsen)
**Faltantes detectados**:
- No hay empty states definidos (qué pasa al abrir un proyecto nuevo sin notas)
- Falta feedback visual en acciones async (drag-drop sin confirmación inmediata)
- Sin breadcrumbs (Max pierde ubicación en proyectos anidados)
- Onboarding de 0 → no documentado
**Mejoras**:
- Empty state en cada zona: ilustración minimal + 1 CTA
- Skeleton loaders durante fetch
- Breadcrumb `home > proyecto > archivo`
- Wizard 3 pasos al primer login

## Panel 2: Experto Visual Design (Anthropic)
**Faltantes**:
- Estética no especificada pixel-perfect (sigue directrices generales)
- Falta definir scale tipográfico (1rem=16px o 14px)
- Sin grilla 8px definida
- Sin dark mode/light mode spec
**Mejoras**:
- Tipo scale: 12/14/16/20/24/32/48 (px)
- Spacing scale: 4/8/12/16/24/32/48/64
- Grid: 12 cols, gutter 16px
- Dark mode único (#0a0a0a base, #1a1a1a cards)

## Panel 3: Experto Interaction Design
**Faltantes**:
- Sin definir shortcuts keyboard (solo Cmd+K mencionado)
- No hay undo/redo para acciones destructivas
- Modal vs side-drawer inconsistente
**Mejoras**:
- Cmd+K palette, Cmd+Shift+T new tab, Cmd+/ help
- Confirm dialog para delete
- Modal para forms, drawer para details

## Panel 4: Experto Accessibility (a11y)
**Faltantes**:
- Sin ARIA labels en zonas
- Focus trap no definido en modals
- Color contrast no medido
- Sin skip-to-content link
**Mejoras**:
- `role="region" aria-label="..."` en cada zona
- Focus trap en modals
- Contrast ratio ≥4.5:1 (texto), ≥3:1 (UI)
- Skip link primer elemento focusable

## Panel 5: Experto Performance
**Faltantes**:
- WebSocket reconnection strategy no documentado
- Sin virtual scrolling en listas largas (tareas, mensajes)
- Sin lazy loading de imágenes
**Mejoras**:
- Exponential backoff reconnection (1s/2s/4s/8s max)
- Virtual scroll para >100 items
- Lazy load fotos con IntersectionObserver

## Panel 6: Experto State Management
**Faltantes**:
- Single source of truth no claro
- Sin optimistic UI para Kanban
- localStorage vs server state no separado
**Mejoras**:
- Store central: `window.osquestador.state`
- Optimistic update con rollback en error
- localStorage solo para prefs UI (theme, sidebar collapsed)

## Panel 7: Experto Information Architecture
**Faltantes**:
- Sidebar 280px fija, pero ¿qué pasa con proyectos >20? Scroll? Paginación?
- 9 modelos LLM en dropdown — sin grouping por provider
- Skills list — sin jerarquía clara
**Mejoras**:
- Sidebar collapsible sections + search dentro
- Dropdown modelos agrupado: Anthropic / OpenAI / Groq / Cerebras / NVidia
- Skills grouped by category (Memoria/Tareas/Vault/Skills/Deploy)

## Panel 8: Experto Mobile Design
**Faltantes**:
- Bottom toolbar no especificado
- Touch targets ≥44px no definidos
- Gestures (swipe to delete) no documentados
**Mejoras**:
- Bottom toolbar en mobile (estilo Obsidian 1.11)
- Touch targets mínimo 44x44px
- Swipe left = delete (con confirm)

## Panel 9: Experto Security
**Faltantes**:
- Secretos en `~/.osquestador/secrets/` chmod 600 — bien
- Falta HTTPS forzado
- Sin CSP headers
- Tokens de sesión no definidos
**Mejoras**:
- HTTPS obligatorio en deploy
- CSP: `default-src 'self'; script-src 'self'`
- Tokens JWT 24h expiry, refresh 7d

## Panel 10: Experto Design Systems
**Faltantes**:
- Design tokens no en JSON
- Sin Storybook para components
- Sin theming system
**Mejoras**:
- `tokens.json` con todos los design tokens
- Componentes reutilizables: Button, Input, Modal, Tabs, Card
- Theming via CSS custom properties
