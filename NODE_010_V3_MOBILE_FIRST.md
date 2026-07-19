# NODE_010 V3 — Mobile-first aplicado a G_panel_final.html

**Fecha**: 2026-07-18 22:14
**Modo SHERIFF v8.2**: MOBILE_FIRST con validación visual de la foto

## OBSERVACIÓN DE LA FOTO

La foto de Max está en mobile (360px). El sidebar está visible full-width con:
- "PROYECTO ACTIVO" card
- "PROYECTOS (4)"
- "9 TIPOS DE AGENTES" grid
- "AGENTES ACTIVOS 52/100"
- "TAGS ACTIVOS"
- Main panel a la derecha (también visible): "OSQUESTADOR", tabs, MEMORIA TRIPLA, FILTROS

**En la foto se ve TODO el panel en mobile sin scroll horizontal.** Esto significa que el layout es **sidebar + main stacked** (no side-by-side) o que el sidebar ocupa todo el ancho.

## BREAKPOINTS V3 (reforzados)

```css
/* Mobile S — 360px (iPhone SE) — el de la foto de Max */
@media (max-width: 414px) {
  .app { display:flex; flex-direction:column; }
  .sidebar { width:100%; }
  .main { width:100%; }
}

/* Mobile L — 414px (iPhone Plus) */
@media (min-width: 415px) and (max-width: 767px) { ... }

/* Tablet — 768px (iPad) */
@media (min-width: 768px) and (max-width: 1023px) { ... }

/* Desktop — 1024px+ */
@media (min-width: 1024px) {
  .app { display:grid; grid-template-columns:280px 1fr; }
  .sidebar { width:280px; }
}
```

## REGLAS V3 (las 8 v2 + 4 nuevas)

### De v2 (preservadas)
- R-MF-01: clamp() tipografía
- R-MF-02: touch targets ≥ 44x44
- R-MF-03: modales max-height 90vh
- R-MF-04: header sticky z-index
- R-MF-05: badges flex no absolute
- R-MF-06: inputs full-width mobile
- R-MF-07: botones in-card align-self
- R-MF-08: overflow-x hidden

### Nuevas v3
- **R-MF-09**: sidebar colapsable a drawer en mobile (botón hamburguesa)
- **R-MF-10**: main panel full-width mobile
- **R-MF-11**: tags/badges en grid responsive (3 cols mobile, 6+ desktop)
- **R-MF-12**: progress bar full-width mobile

## DECISIONES D53-D56 (NUEVAS v3)

- **D53**: Layout mobile = sidebar + main stacked (no side-by-side cramped)
- **D54**: Sidebar 100% en mobile, 280px en desktop
- **D55**: Hamburger button top-left en mobile
- **D56**: Tabs y filtros en columna en mobile, fila en desktop

## APLICACIÓN A G_panel_final.html

```
Layout mobile (≤414px):
┌────────────────────┐
│ ☰  OSQUESTADOR    │ ← header sticky
├────────────────────┤
│ PROYECTO ACTIVO    │
│ ────────────────   │
│ osquestador-audit. │
│                    │
│ PROYECTOS (4)      │
│ osq-auditor  [52]  │
│ osq-memoria  [23]  │
│ agentes      [18]  │
│ openclaw      [5]  │
│                    │
│ 9 TIPOS AGENTES    │
│ [researcher][coder]│
│ [writer][auditor] │
│ [orchest.][router]│
│ [memory][watchdog] │
│ [translator]       │
│                    │
│ AGENTES 52/100     │
│ ▓▓▓▓▓░░░░░░       │
│                    │
│ TAGS ACTIVOS       │
│ [decision][tech]   │
│ [process]...       │
├────────────────────┤
│ TABS: [block][Mem] │
│       [Docs]       │
│                    │
│ MEMORIA TRIPLA     │
│ 📝 D-23 decision   │
│ 2min · SHA a3f9c8  │
│ 🧠 Episodio Graph. │
│ user → crear prot. │
│ 🔗 Repo (COLD)     │
│ commit 7a0152a     │
│ 📁 vault/panel-file│
│ [[input_block_id]] │
│ 💬 Chat #1 (Hayes) │
│ InMemoryChatMess.  │
│                    │
│ FILTROS            │
│ ☑ verificados      │
│ ☑ INSTRUCCIONES    │
│ ☐ cross-project    │
│ ☐ OpenClaw INTACTO │
├────────────────────┤
│ tokens 340ms SQLi. │ ← status
│ FAISS  Neo4j       │
└────────────────────┘
```

## ANTI-INVENT CHECK

- 0 frameworks mobile nuevos
- 0 inventos de elementos UI
- 0 inventos de nombres
- Todo derivado literal de la foto de Max

Procede NODE_011 V3 (validar visualmente cada paso con Playwright + read).
