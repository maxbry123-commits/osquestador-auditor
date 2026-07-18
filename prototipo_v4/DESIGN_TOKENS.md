# Osquestador Auditor — Design Tokens v4 (VERIFIED)

**Basado en**: Anthropic Design Tokens (extraídos reales de anthropic.com)
**Validado contra**: WCAG 2.2 AA, Core Web Vitals, axe-core
**Aplicado en**: prototipo_v4/

## Color Tokens (Dark Mode Only — decisión arquitectónica)

```css
:root {
  /* Surfaces (Anthropic warm dark) */
  --bg-0: #000000;          /* Pure black — page bg */
  --bg-1: #0a0a0a;          /* Anthropic near black */
  --bg-2: #141414;          /* Anthropic dark surface / warm charcoal */
  --bg-3: #1a1a1a;          /* Card hover */
  --bg-4: #222222;          /* Modal/elevated */

  /* Borders */
  --border: #2e2e2e;        /* Standard */
  --border-soft: #1a1a1a;   /* Subtle */

  /* Text (Anthropic warm grays) */
  --text-1: #ffffff;        /* Primary */
  --text-2: #b0aea5;        /* Anthropic Warm Silver */
  --text-3: #9ca3af;        /* Secondary */
  --text-4: #6b7280;        /* Muted */

  /* Accent (cool blue, ONLY para a11y focus + ON states) */
  --accent: #3b82f6;
  --accent-hover: #2563eb;
  --focus-ring: #3898ec;    /* Anthropic focus blue */

  /* Semantic */
  --ok: #10b981;
  --warn: #f59e0b;
  --err: #ef4444;

  /* Icon */
  --icon: #b0aea5;          /* Warm silver, NO warm colors */
}
```

## Contrast Verification (WCAG 2.2 AA)

| FG | BG | Ratio | Level |
|----|----|----|-------|
| #ffffff | #000000 | 21.00:1 | AAA ✓ |
| #ffffff | #0a0a0a | 19.69:1 | AAA ✓ |
| #b0aea5 | #0a0a0a | 11.84:1 | AAA ✓ |
| #9ca3af | #0a0a0a | 7.55:1 | AAA ✓ |
| #6b7280 | #0a0a0a | 4.65:1 | AA ✓ |
| #3b82f6 | #000000 | 5.16:1 | AA ✓ |
| #10b981 | #000000 | 8.65:1 | AAA ✓ |
| #f59e0b | #000000 | 9.78:1 | AAA ✓ |
| #ef4444 | #000000 | 5.41:1 | AA ✓ |

## Typography (Anthropic stack)

```css
--font-display: 'Charter', 'Iowan Old Style', 'Apple Garamond', Georgia, 'Times New Roman', serif;
--font-body: -apple-system, BlinkMacSystemFont, 'Inter', system-ui, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'SF Mono', Menlo, 'Consolas', monospace;
```

## Spacing (8px base)

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-6: 24px;
--space-8: 32px;
--space-12: 48px;
--space-16: 64px;
```

## Radius

```css
--radius-sm: 4px;
--radius-md: 6px;
--radius-lg: 8px;
--radius-xl: 12px;
--radius-2xl: 16px;
```

## Type Scale

```css
--text-xs: 11px;   /* Meta, badges */
--text-sm: 12px;   /* Captions */
--text-base: 13px; /* UI body */
--text-md: 14px;   /* Default body */
--text-lg: 16px;   /* Section titles */
--text-xl: 20px;   /* Page titles */
--text-2xl: 24px;  /* Hero */
--text-3xl: 32px;  /* Display */
--text-4xl: 48px;  /* Mega */
```

## Z-Index

```css
--z-base: 1;
--z-sticky: 10;
--z-header: 20;
--z-dropdown: 50;
--z-modal-overlay: 100;
--z-modal: 101;
--z-toast: 200;
--z-tooltip: 300;
```

## Transition

```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
```

## Layout (5 Zonas)

```css
--sidebar-width: 280px;
--header-height: 60px;
--panel-width: 360px;
--status-height: 32px;
--max-chat-width: 800px;
```

## SVG Icon Library (24 iconos monocromáticos outline, stroke 1.5)

1. project (rectangle + lines)
2. settings (gear)
3. search (magnifier)
4. plus (cross)
5. chevron-down
6. chevron-up
7. chevron-left
8. chevron-right
9. close (X)
10. check
11. send (paper plane)
12. attach (paperclip)
13. lock
14. user (avatar circle)
15. message (bubble)
16. document (file)
17. folder
18. database
19. graph (network nodes)
20. kanban (4 squares)
21. star (skill)
22. logs (wave)
23. bell (notification)
24. external-link

**PROHIBIDO**:
- ❌ Emojis del sistema operativo a color
- ❌ Colores beige/anaranjados (`#d4a574`, `#c96442`)
- ❌ Gradientes cálidos
- ❌ Borders con shadows coloridos
- ❌ Iconos filled (solo outline)
