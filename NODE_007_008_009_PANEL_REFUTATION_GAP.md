# NODE_007 + NODE_008 + NODE_009 — Expert Panel + Refutaciones + Gap Analyzer

**Fecha**: 2026-07-18
**Estado**: PASS

## NODE_007_EXPERT_PANEL — 10 paneles de expertos

### Panel 1: UX Research (Jakob Nielsen)
- **Recomendación**: Empty states, breadcrumbs, search global
- **Aplica**: 5 zonas fijas con breadcrumb en header

### Panel 2: Visual Design (Anthropic real)
- **Recomendación**: Tokens extraídos de anthropic.com (palette warm dark)
- **Aplica**: --bg-0 #000, --surface #141414, --fg #b0aea5, --accent #3b82f6 (focus only)

### Panel 3: Interaction Design (Don Norman)
- **Recomendación**: Affordances, signifiers, feedback
- **Aplica**: Hover/active/focus states, keyboard shortcuts (Cmd+K, Cmd+T)

### Panel 4: Accesibilidad WCAG 2.2 AA
- **Recomendación**: 4.5:1 normal, 3:1 large, ARIA, focus visible, target 24×24px
- **Aplica**: Skip link, ARIA labels 60+, semantic HTML5

### Panel 5: Performance (Core Web Vitals)
- **Recomendación**: LCP <2.5s, HTML <100KB, 0 external resources
- **Aplica**: Vanilla JS, inline CSS, system fonts stack

### Panel 6: State Management
- **Recomendación**: Single source of truth, optimistic UI
- **Aplica**: window.osquestador.state global, rollback on error

### Panel 7: Information Architecture (Tufte)
- **Recomendación**: Data-ink ratio, small multiples, micro/macro
- **Aplica**: Cards consistentes, breadcrumb, overview+detail

### Panel 8: Mobile Design (Luke Wroblewski)
- **Recomendación**: Mobile-first, touch ≥44px, bottom toolbar
- **Aplica**: Drawer off-canvas, bottom sheet panel

### Panel 9: Security (OWASP)
- **Recomendación**: chmod 600 secrets, HTTPS, CSP, XSS prevention
- **Aplica**: ~/.osquestador/secrets/ excluido de backup/git

### Panel 10: Design Systems (Brad Frost)
- **Recomendación**: Atomic design, tokens, Storybook
- **Aplica**: CSS variables centralizadas, JSON exportable

## MERGE_RECOMMENDATIONS: 10 paneles unificados
## VALIDATE: OK
## AUDIT: OK
## CERTIFY: PASS

---

## NODE_008_REFUTATION_ENGINE — 10 refutaciones

### R01: 3 columnas split-view sin espacio
- **Severidad**: ALTA
- **Fix**: Default 1 modelo, "Compare" para split, modo compact 3 modelos

### R02: Memory auto-recall obsoleta
- **Severidad**: MEDIA
- **Fix**: Botón X en cada entity, negative feedback loop

### R03: Drag-drop no funciona mobile
- **Severidad**: ALTA
- **Fix**: Botón + con file picker nativo

### R04: Búsqueda unificada lenta
- **Severidad**: MEDIA
- **Fix**: Pre-cache indices al login, Web Worker

### R05: Skill auto-creación spam
- **Severidad**: BAJA
- **Fix**: Threshold 5/3d, cooldown 7d, snooze 24h

### R06: Watchdog log llena disco
- **Severidad**: MEDIA
- **Fix**: Log rotation daily, gzip >7d, delete >30d

### R07: Wikilinks rotos al renombrar
- **Severidad**: ALTA
- **Fix**: Hook PreToolUse rename → update all wikilinks

### R08: Kanban sin optimistic UI
- **Severidad**: MEDIA
- **Fix**: Optimistic move + background sync + rollback

### R09: OCR pierde estructura tablas
- **Severidad**: ALTA
- **Fix**: PaddleOCR mode table + Baidu OCR form-aware

### R10: Export sin state.json
- **Severidad**: ALTA
- **Fix**: Incluir state.json con TODO state serializado

## REGISTER_DEFECTS: 10
## REGISTER_IMPROVEMENTS: 10
## VALIDATE: OK

---

## NODE_009_GAP_ANALYZER

### COMPARACIONES:

#### Input Block vs State JSON:
- Input: 9 instrucciones + 16 pasos del flujo
- State: vacío (a crear)
- **Gap**: Crear state.json con tasks completados

#### Input vs GitHub Documents:
- 45+ docs cubren todas las 9 instrucciones ✓
- **Gap**: Pocos docs tienen el formato "9 puntos" literal

#### Prototype vs Input:
- HTMLs anteriores tenían solo datos estáticos
- **No cumplen**: 3 ventanas Anthropic, ventanas iOS, routing, selection, 7 funciones window.osquestador
- **Gap**: Rediseñar desde cero integrando TODO

#### Prototype vs Source Code (10 SDKs):
- Métodos SDKs NO integrados en UI actual
- **Gap**: Agregar UI que use métodos reales (Haystack.write_documents, Graphiti.add_episode, etc)

#### UI vs Backend:
- 11 ideas UI + 14 ideas Backend clasificadas
- **Gap**: Solo implementar las 11 UI en HTML

### IDENTIFY_GAPS:
1. 3 ventanas tipo Anthropic (Conocimiento, Nuevo, Configuración)
2. Ventanas iOS file manager con multi-select
3. Routing a agentes funcional
4. Selection mode (individual/grupo/folder)
5. 7 funciones window.osquestador abiertas
6. 10 patterns UI community integrados
7. Código fuente 10 SDKs aplicado a UI
8. Modales estilo Claude.ai iOS con tabs

### CLASSIFY_GAPS:
- **CRÍTICOS** (8): todos los gaps arriba

### REGISTER_GAPS: 8 gaps
### VERIFY_GAPS: OK

## ESTADO: PAS → CROSS_VALIDATION_MANAGER
