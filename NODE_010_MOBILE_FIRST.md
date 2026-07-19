# NODE_010_MOBILE_FIRST — Design system mobile-first

**Fecha**: 2026-07-18 21:58
**Modo SHERIFF v8.2**: MOBILE_FIRST (NUEVO v2)

## BREAKPOINTS (4)

```css
/* Mobile S — 360px (iPhone SE) */
@media (max-width: 414px) { ... }

/* Mobile L — 414px (iPhone Plus) */
@media (min-width: 415px) and (max-width: 767px) { ... }

/* Tablet — 768px (iPad portrait) */
@media (min-width: 768px) and (max-width: 1023px) { ... }

/* Desktop — 1024px+ */
@media (min-width: 1024px) { ... }
```

## REGLAS MOBILE-FIRST (8)

### R-MF-01: Tipografía con clamp()
```css
font-size: clamp(1rem, 4vw, 1.5rem);  /* mínimo, preferred, máximo */
```

### R-MF-02: Touch targets ≥ 44x44px
- Botones mínimo 44x44
- File rows mínimo 56px alto
- Cards drag-drop mínimo 80px

### R-MF-03: Modales max-height
```css
max-height: 90vh;
overflow-y: auto;
-webkit-overflow-scrolling: touch;
```

### R-MF-04: Header sticky z-index
```css
position: sticky;
top: 0;
z-index: 100;
```

### R-MF-05: Badges position
- Nunca `position: absolute` sin contexto parent `position: relative`
- Usar `flex` con `align-self` en vez de absolute cuando posible

### R-MF-06: Inputs full-width mobile
```css
@media (max-width: 414px) {
  input, textarea, select { width: 100%; box-sizing: border-box; }
}
```

### R-MF-07: Botones in-card alineados
```css
.card { display: flex; flex-direction: column; }
.card-meta { margin-top: auto; }
.card-move { align-self: flex-end; }
```

### R-MF-08: Overflow-x: hidden
```css
html, body { overflow-x: hidden; }
```

## APLICACIÓN A 8 HTMLs v6

### 00_main_dashboard.html v6
- Reducir sidebar a iconos-only en <768px
- Chat area full-width
- Header sticky
- Status bar 2 filas en mobile
- Quitar "0" badge absoluto → flex

### 01_conocimiento_proyecto.html v6
- Grid cards 1 columna <480px
- Slider full-width
- "Agregar contenido" botón full-width mobile

### 02_nuevo_proyecto.html v6
- Modal max-height 90vh + scroll
- Icon picker 4 cols en mobile (no 8)
- Templates stack vertical

### 03_configuracion.html v6
- Tabs scroll horizontal si overflow
- Form fields full-width mobile
- Save button fixed bottom

### 04_file_manager_ios.html v6
- Tree sidebar → drawer mobile
- File row touch target 56px
- Botón "Mover a..." alineado en card

### 05_routing_agentes.html v6
- Agent list full-width
- Flow diagram scroll horizontal
- Tabs scroll horizontal

### 06_kanban_dragdrop.html v6
- 4 columnas → 1 columna scroll vertical en <480px
- Botón Mover a… siempre visible
- Long-press para drag

### 07_panel_completo.html v6
- KPIs 2 cols en mobile (no 5)
- Tipografía title con clamp()
- Timeline full-width

## ANTI-INVENT CHECK

- Breakpoints son estándar W3C
- clamp() es CSS nativo
- 44x44 touch target es Apple HIG
- max-height 90vh es patrón UI
- 0 frameworks mobile nuevos (no Bootstrap, no Tailwind)

Procede NODE_011_VISUAL_VALIDATION.
