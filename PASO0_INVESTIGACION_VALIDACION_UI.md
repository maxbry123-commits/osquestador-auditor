# PASO 0: Investigación de validación/verificación UI

**Fecha**: 2026-07-18
**Búsquedas realizadas**: 20+ (mínimo cumplido)
**Modo**: loops sin parar hasta 20 pasadas

## HALLAZGOS CLAVE

### 1. Visual Regression Testing (VRT)
**Herramientas líderes 2026**:
- **Percy** (BrowserStack): full-page testing, CI/CD integration, AI Visual Review Agent (3x faster review, 40% less false positives)
- **Chromatic** (Storybook team): component-level, dependency analysis, ~2-4s/snapshot
- **Applitools Eyes**: enterprise AI diffing
- **BackstopJS**: open source
- **Playwright `toHaveScreenshot()`**: built-in

**Workflow**:
1. Capture baseline screenshot
2. Run tests after each code change
3. Diff against baseline
4. Human reviews diffs (Accept/Reject)
5. Block PR on failures

### 2. Accesibilidad WCAG 2.2
**Thresholds críticos**:
- **Normal text** (< 18pt regular, < 14pt bold): contrast ratio **4.5:1** AA / **7:1** AAA
- **Large text** (≥ 18pt regular, ≥ 14pt bold): **3:1** AA / **4.5:1** AAA
- **UI components/graphics**: **3:1** (WCAG 1.4.11)
- **Focus visible** (2.4.7): clearly visible
- **Focus not obscured** (2.4.11, NEW in 2.2): focused element must remain visible
- **Target size minimum** (2.5.8, NEW): 24×24 CSS pixels
- **Dragging movements** (2.5.7, NEW): provide alternative
- **Consistent help** (3.2.6, NEW)
- **Redundant entry** (3.3.7, NEW)
- **Accessible authentication** (3.3.8/3.3.9, NEW)

**Automation**: axe-core catches 30-57% WCAG issues. Manual testing catches 30-45% more. Screen reader testing final.

### 3. HTML5 Semantic Landmarks
**Reglas W3C/WCAG**:
- `<header>` (banner role) — page or section header
- `<nav>` (navigation role) — navigation links
- `<main>` (main role) — primary content, ONE per page
- `<aside>` (complementary role) — tangential content
- `<footer>` (contentinfo role) — page or section footer
- `<section>` with aria-label — only then exposed as landmark
- `<form>` with accessible name — only then landmark
- `<article>` — self-contained content
- `<h1>` ONE per page, logical heading order

### 4. Core Web Vitals (Lighthouse)
**Targets**:
- **LCP** (Largest Contentful Paint): ≤ 2.5s good
- **INP** (Interaction to Next Paint): ≤ 200ms good
- **CLS** (Cumulative Layout Shift): ≤ 0.1 good
- **Performance score**: ≥ 0.85 mobile
- **Total JS**: ≤ 300 KB gzip
- **HTML size**: < 100 KB ideal (median mobile 2.5MB)
- **Lighthouse CI**: fail merge if mobile LCP > 2.5s or CLS > 0.1

### 5. Anthropic Design Tokens (reales, extraídos de anthropic.com)
**Light mode (homepage)**:
- `bg`: `#f5f4ed` (Parchment)
- `surface`: `#faf9f5` (Ivory)
- `surface-warm`: `#e8e6dc` (Warm Sand)
- `fg`: `#141413` (Near Black)
- `fg-2`: `#3d3d3a` (Dark Warm)
- `muted`: `#5e5d59` (Olive Gray)
- `meta`: `#87867f` (Stone Gray)
- `border`: `#f0eee6` (Border Cream)
- `border-soft`: `#e8e6dc`
- `accent`: `#c96442` (Terracotta)
- `accent-on`: `#faf9f5`
- `success`: `#17a34a`
- `warn`: `#eab308`
- `danger`: `#b53333`
- `focus`: `#3898ec` (cool blue, ONLY for a11y)

**Dark mode (Claude chat)**:
- `bg`: `#141413` (Near Black)
- `surface`: `#30302e` (Dark Surface / warm charcoal)
- `fg`: `#faf9f5` (Ivory)
- `fg-2`: `#b0aea5` (Warm Silver)
- `border`: `#30302e`

**Typography**:
- `--font-display`: "Anthropic Serif", Georgia, "Times New Roman", serif
- `--font-body`: "Anthropic Sans", "Arial", system-ui, -apple-system, sans-serif
- `--font-mono`: "Anthropic Mono", ui-monospace, "JetBrains Mono", Menlo, monospace
- Hero: 96px / 400 weight
- Body: 20px / 400
- Button: 24px / 400

**Components**:
- Button padding: `0px 12px 0px 8px` (asymmetric, icon-first)
- Button radius: 8px (secondary) / 12px (primary, white surface)
- Cards: 8px standard, 16px featured, 32px hero
- Shadow: `rgba(0,0,0,0.05) 0px 4px 24px`
- Ring shadow: `0px 0px 0px 1px`

### 6. shadcn/ui + Tailwind Best Practices
- **CSS variables** for theming (`:root` + `.dark`)
- **Semantic tokens**: `--background`, `--foreground`, `--primary`, `--muted`, `--border`
- **Dark mode**: redefine same variables in `.dark` selector
- **Never hardcode colors** outside tokens
- **Test contrast** both light and dark modes
- **Wrapper pattern** for component customization

### 7. Anthropic Frontend Design Plugin (nov 2025)
**Reglas explícitas del plugin oficial**:
- **Typography**: Never Inter/Roboto/Open Sans/Lato/Arial/system fonts
  - Body: Bricolage Grotesque
  - Display: Fraunces
  - Mono: JetBrains Mono
- **Color**: single dominant + sharp accent
- **Forbidden**: purple-to-blue gradients on white
- **Backgrounds**: layered CSS gradients or geometric patterns
- **Always shadcn/ui primitives** where they exist
- **Verification pattern**: write → screenshot → diff → refine

### 8. Playwright screenshot automation
**Comandos clave**:
```js
await page.screenshot({ path: 'shot.png' });
await page.screenshot({ path: 'full.png', fullPage: true });
await page.locator('.element').screenshot({ path: 'el.png' });
await expect(page).toMatchSnapshot();
```

### 9. axe-core CLI
**Install**: `npm install @axe-core/cli -g`
**Run**: `axe https://url.com --save results.json`
**Tags**: `--tags wcag2a,wcag2aa`
**Catches**: 30-57% WCAG issues

## CHECKLIST DE VALIDACIÓN A APLICAR

### A) Estética visual (manual + screenshot)
- [ ] Sin emojis a color (todos iconos SVG monocromáticos outline)
- [ ] Sin colores beige/anaranjados (`#d4a574`, `#c96442` decorativos)
- [ ] Paleta grayscale + accent azul sutil (`#3b82f6` o `#3898ec` solo en estados)
- [ ] Tipografía SERIF para títulos (Charter, Iowan Old Style, Georgia)
- [ ] Dark mode puro (`#000` base, `#0a0a0a` cards)
- [ ] Border radius consistente (8-12px)
- [ ] Iconos monocromáticos outline (stroke 1.5, fill none)

### B) Accesibilidad WCAG 2.2 AA (axe-core)
- [ ] Contrast ratio ≥ 4.5:1 texto normal
- [ ] Contrast ratio ≥ 3:1 texto large + UI components
- [ ] Focus visible (2.4.7)
- [ ] Focus not obscured (2.4.11)
- [ ] Target size ≥ 24×24px (2.5.8)
- [ ] Lang attribute on html
- [ ] Alt text on images
- [ ] ARIA labels on regions
- [ ] Keyboard navigation
- [ ] Skip to main content link

### C) HTML5 semántico (W3C)
- [ ] `<header>` (banner)
- [ ] `<nav>` (navigation)
- [ ] `<main>` (main, ONE per page)
- [ ] `<aside>` (complementary)
- [ ] `<footer>` (contentinfo)
- [ ] `<article>` for self-contained
- [ ] `<section>` with aria-label
- [ ] ONE `<h1>` per page
- [ ] Logical heading order (h1→h2→h3)

### D) Performance (Lighthouse)
- [ ] HTML size < 100KB
- [ ] No render-blocking JS
- [ ] No unused CSS
- [ ] Width/height on images (CLS)
- [ ] Lazy loading below-fold
- [ ] Total JS < 300KB gzip

### E) Contenido (manual)
- [ ] 13 programas del spec presentes
- [ ] 37 decisiones D1-D37 reflejadas
- [ ] 70 ideas integradas visibles
- [ ] 5 zonas fijas presentes
- [ ] Graphiti memoria referenciada
- [ ] 9 modelos LLM
- [ ] 52/100 skills
- [ ] Vault markdown con frontmatter

## HERRAMIENTAS QUE APLICARÉ EN ESTE TURNO

1. **Manual code review** (grep/lectura)
2. **Validación HTML5** (regex/sintaxis)
3. **Color contrast calculation** (luminance formula)
4. **Self-axe manual checklist** (no browser disponible)
5. **Playwright syntax** para scripts (sin ejecutar)
6. **File size check** (wc -c)
7. **Semantic landmark count** (grep)
8. **Token conformance** (CSS variables check)
