# 25 Simulaciones de diseño (V2) — con criterios pixel-perfect

**Fecha**: 2026-07-18
**Paso**: 6/10 v2

## D1: Sidebar vacío
**Pixel-perfect**:
- Width: 280px exact
- Background: #0a0a0a
- Border-right: 1px solid #2e2e2e
- Logo: 18px Charter, font-weight 400, letter-spacing -0.01em
- Empty state: text "No projects yet" centered, color #6b7280, font 12px
- CTA button: "+ Create your first" centered, 12px Inter, bg #3b82f6, padding 8×16, radius 6px

## D2: Sidebar 20 proyectos
**Pixel-perfect**:
- Status dot: 6px circle, color según status
- Item padding: 8px horizontal, 4px vertical
- Hover: bg #141414
- Active: bg #1a1a1a + border-left 2px solid #3b82f6
- Text: 13px Inter, color #d1d5db (active: #ffffff)
- Badge: 10px, padding 2×6, radius 10px, bg #222

## D3: Sidebar mobile
**Pixel-perfect**:
- Bottom sheet, height 70vh max
- Tap target ≥ 44×44px
- Full-width items
- Status indicator 12px
- Close button: 44×44px, top-right
- Slide-up animation: 200ms ease-out

## D4: Header minimal
**Pixel-perfect**:
- Height: 60px exact
- Background: #0a0a0a
- Border-bottom: 1px solid #2e2e2e
- Logo: 16px Charter, 400 weight
- Padding: 0 16px

## D5: Header modelo error
**Pixel-perfect**:
- Error dot: 6px, color #ef4444
- Tooltip on hover: bg #1a1a1a, border #2e2e2e, padding 8×12, radius 6px
- Dropdown panel: max-width 320px, shadow 0 8px 24px rgba(0,0,0,0.5)

## D6: Chat 1 modelo
**Pixel-perfect**:
- Bubble padding: 12px 16px
- Border-radius: 12px
- User bubble: bg #1a1a1a, align right
- Assistant bubble: bg #141414, align left
- Avatar: 28×28px, border-radius 50%, bg #1a1a1a
- Max-width bubble: 80% del chat
- Line-height: 1.6
- Font-size: 14px

## D7: Chat 3 modelos split
**Pixel-perfect**:
- 3 cols 33.33% cada una
- Border-right 1px entre cols
- Header de col: 12px font, padding 8×12
- Tokens counter: mono 11px

## D8: Chat input
**Pixel-perfect**:
- Border-top: 1px solid #2e2e2e
- Pinned bar height: 48px
- Input padding: 8px
- Textarea: font 14px, line-height 20px
- Send button: 32×32px, bg #3b82f6

## D9: Pinned bar 5 archivos
**Pixel-perfect**:
- Item padding: 4×8
- Gap: 8px
- Overflow-x: auto
- Item bg: #141414
- Border: 1px solid #2e2e2e
- Font: 11px
- Border-radius: 6px
- Total bar height: 48px

## D10: Pinned bar con error
**Pixel-perfect**:
- Error item: border-color #ef4444
- ⚠️ icon: 12px, color #ef4444
- Tooltip: bg #1a1a1a, color #ef4444

## D11: Panel derecho 5 tabs
**Pixel-perfect**:
- Tab height: 56px
- Active: border-bottom 2px solid #3b82f6
- Icon: 16px SVG, color #d1d5db
- Label: 11px
- Gap: 4px entre icon y label
- Border-bottom en tab list: 1px solid #2e2e2e

## D12: Tab Memoria con grafo
**Pixel-perfect**:
- Container height: 100% de panel
- Search box: 12px padding, top-left absolute
- Controls: bottom-right absolute, 32×32px buttons
- Nodes: 8px padding, bg #141414, border #2e2e2e, radius 8px
- Node hover: border-color #3b82f6
- Decision node: border-left 3px solid #3b82f6
- Entity node: border-left 3px solid #10b981
- Skill node: border-left 3px solid #f59e0b

## D13: Tab Documentos
**Pixel-perfect**:
- Item: 8px padding, 12px font
- Meta: 10px font, color #6b7280
- Gap: 4px
- Border-bottom: 1px solid #2e2e2e entre items
- Hover: bg #141414

## D14: Tab Tareas Kanban
**Pixel-perfect**:
- 3 cols 33.33% width
- Card padding: 12px
- Card bg: #141414
- Card border: 1px solid #2e2e2e
- Card radius: 6px
- Gap entre cards: 8px
- Drag: opacity 0.5, scale 0.98
- Drop: bg #1a1a1a 200ms transition

## D15: Tab Skills
**Pixel-perfect**:
- Grid 2 cols, gap 8px
- Card padding: 12px
- Name: 14px, 500 weight
- Desc: 12px, #9ca3af
- Count badge: 10px, padding 2×6, radius 10px
- Tags: 10px mono

## D16: Tab Logs live
**Pixel-perfect**:
- Item: padding 4×0, border-bottom 1px solid
- Timestamp: 10px mono, #6b7280
- Type color:
  - info: #9ca3af
  - warn: #f59e0b
  - error: #ef4444
- Auto-scroll a top cuando nuevo log
- Max 200 logs visibles, virtual scroll

## D17: Status bar
**Pixel-perfect**:
- Height: 32px exact
- Background: #0a0a0a
- Border-top: 1px solid #2e2e2e
- Items: 11px, color #9ca3af
- Dot: 5px circle
- Gap: 16px entre items
- Mono font para números

## D18: Status bar error
**Pixel-perfect**:
- Error item: color #ef4444
- Bg: rgba(239,68,68,0.1) opcional
- Click: cursor pointer
- Hover: bg #1a1a1a
- Modal: max-width 600px, padding 24px

## D19: Modal genérico
**Pixel-perfect**:
- Overlay: rgba(0,0,0,0.7), backdrop-filter blur(4px)
- Modal: max-width 600px, padding 24px
- Border-radius: 12px
- Border: 1px solid #2e2e2e
- Shadow: 0 24px 48px rgba(0,0,0,0.5)
- Header: 20px font, border-bottom 1px

## D20: Modal accesible
**Pixel-perfect**:
- role="dialog"
- aria-modal="true"
- aria-labelledby="title"
- Focus trap: tab cicla dentro
- Esc: cierra
- Click overlay: cierra (con confirm si cambios)
- Initial focus: primer input
- Final focus: trigger element

## D21: Toast notification
**Pixel-perfect**:
- Position: bottom-right, 16px margin
- Width: 320px
- Padding: 12px 16px
- Bg: #1a1a1a
- Border: 1px solid #2e2e2e
- Border-radius: 8px
- Shadow: 0 8px 24px rgba(0,0,0,0.4)
- Auto-dismiss: 5s
- Stack max 3 visibles

## D22: Dropdown modelo
**Pixel-perfect**:
- Trigger: padding 6×10, bg #141414, border #2e2e2e
- Dropdown: max-height 400px, overflow-y auto
- Item: padding 8×12, hover bg #1a1a1a
- Provider label: 10px uppercase, #6b7280
- Status dot: 6px
- Filter chips: arriba, scroll horizontal

## D23: Slash command menu
**Pixel-perfect**:
- Position: absolute sobre input, 8px gap
- Max-width: 480px
- Max-height: 320px
- Bg: #1a1a1a
- Border: 1px solid #2e2e2e
- Border-radius: 8px
- Group header: 10px uppercase, #6b7280
- Item: padding 8×12
- Active item: bg #141414, border-left 2px #3b82f6
- Highlight: bold + color #3b82f6

## D24: Empty graph
**Pixel-perfect**:
- Centrado vertical y horizontal
- Texto: 14px, color #9ca3af
- CTA: 12px, color #3b82f6, hover underline

## D25: Loading state
**Pixel-perfect**:
- Skeleton: bg #1a1a1a, border-radius 6px
- Shimmer: linear-gradient 90deg transparent → rgba(255,255,255,0.05) → transparent
- Animation: 1.5s linear infinite
- NO spinner genérico
- Match content shape (texto = line, img = rect)
