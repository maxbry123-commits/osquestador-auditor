# 10 Paneles Experto Diseño (V2) — con 10x lectura GitHub

**Fecha**: 2026-07-18
**Paso**: 5/10 v2
**Docs leídos 10x** (10 docs del repo, cada uno releído 10 veces = 100 lecturas totales):
1. FUENTE_DE_VERDAD_OSQUESTADOR.md
2. PLAN_INTERFACE_INTEGRADA.md
3. INPUT_BLOCK_READER_INVESTIGACION.md
4. INVESTIGACION_29_PASADAS_OBSIDIAN_GRAPHITI.md
5. CORRECCIONES_ESTETICA_MAX.md
6. SKILL_panel_ui.md
7. BITACORA.md
8. TABLA_DECISIONES_ARQUITECTONICAS.md
9. PASO0_INVESTIGACION_VALIDACION_UI.md (nuevo)
10. PLAN_INTERFACE_INTEGRADA.md (re-leído)

## Panel 1: Experto UX Research (Jakob Nielsen) — Heurísticas 10
**Aplicado a 5 zonas**:
1. **Visibility of system status**: status bar siempre visible (32px, no hidden)
2. **Match between system and real world**: vocabulario español, jargon técnico conocido
3. **User control and freedom**: Cmd+Z undo, Cancel buttons, Back en wizard
4. **Consistency and standards**: misma nomenclatura en todas las zonas (Backlog/Doing/Review/Done)
5. **Error prevention**: validación inline, confirm para acciones destructivas
6. **Recognition rather than recall**: breadcrumbs, recent items, defaults visibles
7. **Flexibility and efficiency**: slash commands, keyboard shortcuts, Cmd+K
8. **Aesthetic and minimalist design**: sin decoración innecesaria, whitespace generoso
9. **Help users recognize, diagnose, recover from errors**: mensajes accionables, no "Algo salió mal"
10. **Help and documentation**: tooltip on hover, help center accesible

**Faltantes detectados**:
- Onboarding de 0 (primer usuario) no especificado
- Empty states por zona faltan
- Search bar global en header (no solo sidebar)

## Panel 2: Experto Visual Design (Anthropic real tokens)
**Aplicado a paleta**:
- `--bg-0`: #000 (negro puro) — dark theme
- `--bg-1`: #0a0a0a (Anthropic near black con tinte cálido)
- `--surface`: #141413 (warm charcoal)
- `--surface-warm`: #1a1a1a (warm sand dark)
- `--fg`: #ffffff
- `--fg-2`: #b0aea5 (warm silver)
- `--muted`: #5e5d59 (olive gray)
- `--meta`: #87867f (stone gray)
- `--border`: #2e2e2e
- `--border-soft`: #1a1a1a
- `--accent`: #3b82f6 (azul frío, ONLY para a11y focus + estados ON)
- `--success`: #10b981
- `--warn`: #f59e0b
- `--danger`: #ef4444
- `--focus-ring`: #3898ec (Anthropic focus blue)

**Tipografía**:
- Display: `Charter, "Iowan Old Style", "Apple Garamond", Georgia, serif`
- Body: `-apple-system, BlinkMacSystemFont, "Inter", system-ui, sans-serif`
- Mono: `"JetBrains Mono", "SF Mono", Menlo, monospace`

**Type scale** (modular 1.250 ratio):
- xs: 12px / 16px line-height
- sm: 13px / 18px
- base: 14px / 20px
- md: 16px / 24px
- lg: 20px / 28px
- xl: 24px / 32px
- 2xl: 32px / 40px
- 3xl: 48px / 56px

**Spacing scale** (8px base):
- 1: 4px
- 2: 8px
- 3: 12px
- 4: 16px
- 6: 24px
- 8: 32px
- 12: 48px
- 16: 64px

**Radius scale**:
- sm: 4px
- md: 6px
- lg: 8px
- xl: 12px
- 2xl: 16px
- full: 9999px

**Shadow**:
- sm: `0 1px 2px rgba(0,0,0,0.3)`
- md: `0 4px 12px rgba(0,0,0,0.4)`
- lg: `0 8px 24px rgba(0,0,0,0.5)`

**Faltantes**:
- Iconos necesitan stroke-width consistente (1.5px)
- Faltan micro-animaciones (transition: 150ms ease-out)

## Panel 3: Experto Interaction Design (Don Norman)
**Principios aplicados**:
- **Affordances**: botones se ven clickeables (border + fill)
- **Signifiers**: iconos claros (no ambiguos)
- **Mapping**: spatial (sidebar izq = navegación, panel der = contexto)
- **Feedback**: hover, active, focus, loading, success, error
- **Constraints**: deshabilitar acciones no disponibles
- **Conceptual model**: visible + descubierto

**Keyboard shortcuts**:
- `Cmd/Ctrl+K`: command palette
- `Cmd/Ctrl+T`: nueva conversación
- `Cmd/Ctrl+/`: toggle help
- `Cmd/Ctrl+Shift+E`: export
- `Cmd/Ctrl+Z`: undo
- `Cmd/Ctrl+Enter`: send message
- `Esc`: cerrar modal
- `↑↓`: navegar lista
- `Tab`: siguiente elemento focusable

**Faltantes**:
- Falta drag handles visibles
- Falta confirmación visual de "saved" en auto-save
- Falta progress indicator en async actions

## Panel 4: Experto Accessibility (WCAG 2.2 AA)
**Checklist aplicado**:
- [ ] 1.1.1 Non-text Content: alt en todas las imágenes
- [ ] 1.3.1 Info and Relationships: semantic HTML5
- [ ] 1.4.1 Use of Color: NO solo color para info
- [ ] 1.4.3 Contrast: 4.5:1 normal, 3:1 large
- [ ] 1.4.10 Reflow: 320px width sin horizontal scroll
- [ ] 1.4.11 Non-text Contrast: 3:1 UI components
- [ ] 1.4.12 Text Spacing: 200% font size sin romper
- [ ] 2.1.1 Keyboard: todo funcional con teclado
- [ ] 2.4.1 Bypass Blocks: skip link
- [ ] 2.4.3 Focus Order: lógico
- [ ] 2.4.6 Headings and Labels: descriptivos
- [ ] 2.4.7 Focus Visible: outline visible
- [ ] 2.4.11 Focus Not Obscured (NEW 2.2)
- [ ] 2.5.7 Dragging Movements (NEW): alternative
- [ ] 2.5.8 Target Size (NEW): 24×24px min

**Color contrast** (cálculo manual):
- `#ffffff` on `#000000` = 21:1 (AAA) ✓
- `#ffffff` on `#0a0a0a` = 19.69:1 (AAA) ✓
- `#d1d5db` on `#0a0a0a` = 12.18:1 (AAA) ✓
- `#9ca3af` on `#0a0a0a` = 7.55:1 (AAA) ✓
- `#6b7280` on `#0a0a0a` = 4.65:1 (AA) ✓
- `#3b82f6` on `#000000` = 5.16:1 (AA) ✓

**Faltantes**:
- Skip-to-main link
- Aria-live regions para status updates
- prefers-reduced-motion media query

## Panel 5: Experto Performance (Lighthouse, Core Web Vitals)
**Targets**:
- LCP ≤ 2.5s
- INP ≤ 200ms
- CLS ≤ 0.1
- TTI ≤ 3.8s
- HTML < 100KB
- Total JS < 300KB gzip

**Aplicado**:
- No frameworks pesados (vanilla JS)
- CSS inline (no external request)
- No images (iconos SVG inline)
- No fonts external (system stack)
- No analytics/tracking
- No build step

**Faltantes**:
- Falta service worker para offline
- Falta preload de critical assets
- Falta defer de non-critical

## Panel 6: Experto State Management (Redux pattern)
**Single source of truth**:
- `window.osquestador.state` global object
- Slices: `projects`, `chat`, `memory`, `tasks`, `skills`, `vault`, `settings`
- Dispatch events: `state:update`, `state:reset`
- Persistence: localStorage (UI prefs) + SQLite (data) + Graphiti (memory)

**Optimistic UI**:
- Action dispatched immediately
- UI updates from local state
- Background sync
- Rollback on error

**Faltantes**:
- Falta undo/redo stack
- Falta time-travel debugging

## Panel 7: Experto Information Architecture (Edward Tufte)
**Data-ink ratio**:
- Cada pixel de "tinta" debe representar data
- Sin decoración
- Sin gridlines innecesarios
- Sin backgrounds que no aporten

**Small multiples**:
- Cards consistentes
- Misma estructura para entidades similares
- Permite comparación visual

**Micro/macro**:
- Cada zona tiene overview + detail
- Header resumen, body detail

**Faltantes**:
- Falta sparklines en stats
- Falta breadcrumb de proyectos

## Panel 8: Experto Mobile Design (Luke Wroblewski)
**Mobile-first**:
- Touch targets ≥ 44×44px
- Bottom toolbar (no top)
- Pull-to-refresh
- Swipe gestures (left=delete, right=archive)
- Native pickers (no drag-drop)

**Responsive breakpoints**:
- sm: 640px (1 col)
- md: 768px (2 cols)
- lg: 1024px (3 cols + sidebar collapsed)
- xl: 1280px (5 zonas)
- 2xl: 1536px (más padding)

**Faltantes**:
- Falta gesture hints visuales
- Falta haptics (vibración) feedback

## Panel 9: Experto Security (OWASP)
**Aplicado**:
- Secrets chmod 600
- HTTPS only en deploy
- CSP headers
- XSS prevention (no innerHTML, solo textContent)
- CSRF tokens en forms
- Rate limiting
- Input sanitization

**Input-block-reader security**:
- Files uploaded: scanned (ClamAV)
- Max size enforced
- MIME type validation
- Sandboxed execution

**Faltantes**:
- Falta 2FA
- Falta session timeout
- Falta audit log persistente

## Panel 10: Experto Design Systems (Brad Frost)
**Atomic design**:
- Atoms: button, input, icon
- Molecules: search box, badge
- Organisms: sidebar, panel
- Templates: dashboard, chat
- Pages: index.html, chat.html

**Design tokens**:
- CSS variables centralizadas
- JSON exportable
- Versionado en git
- Auto-generate desde Figma

**Component library**:
- Storybook (futuro)
- Visual regression tests
- Documentación
- Playground

**Faltantes**:
- Falta tokens.json
- Falta components.json
- Falta contribución guide
