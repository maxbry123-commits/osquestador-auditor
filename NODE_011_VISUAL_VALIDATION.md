# NODE_011_VISUAL_VALIDATION — Playwright + screenshots

**Fecha**: 2026-07-18 21:59
**Modo SHERIFF v8.2**: VISUAL_VALIDATION (NUEVO v2)

## HERRAMIENTAS

- `webapp-testing` skill (Playwright) — disponible en este agente
- Viewports: 360x640 (mobile S), 414x896 (mobile L), 768x1024 (tablet), 1280x800 (desktop)
- Screenshots a PNG para evidencia

## CHECKS VISUALES (5)

### CV-01: Mobile S (360x640)
- Cada HTML en `prototipo_v6/`
- Verificar:
  - Sin overflow-x
  - Sin texto cortado
  - Botones ≥ 44x44
  - Touch targets accesibles
  - Sin overlapping de elementos

### CV-02: Mobile L (414x896)
- Cada HTML
- Verificar:
  - Grid cards colapsa a 1 col
  - Tipografía legible
  - Inputs full-width

### CV-03: Tablet (768x1024)
- Cada HTML
- Verificar:
  - Sidebar visible
  - 2 cols en grids
  - Modales centrados

### CV-04: Desktop (1280x800)
- Cada HTML
- Verificar:
  - Layout 5 zonas en 00
  - Sidebar 280px
  - Panel 360px

### CV-05: Pixel-perfect vs fotos de Max
- Comparar screenshots v6 con 4 fotos de Max
- Match: 0 header overlapping, 0 input cortado, 0 botón suelto
- Output: tabla de matches/mismatches

## OUTPUTS

```
prototipo_v6/screenshots/
  ├── 00_main_dashboard_360.png
  ├── 00_main_dashboard_414.png
  ├── 00_main_dashboard_768.png
  ├── 00_main_dashboard_1280.png
  ├── ... (8 HTMLs x 4 viewports = 32 PNGs)
```

## CERTIFICACIÓN v2

PASS = 32/32 screenshots sin defectos visuales
+ 5/5 checks comparativos con fotos de Max
+ 8/8 gaps G-V2-01..08 cerrados

FAIL = cualquier defecto visual no resuelto

## CÓMO EJECUTAR

```bash
# Con webapp-testing skill
python3 -c "
from playwright.sync_api import sync_playwright
import os
os.makedirs('prototipo_v6/screenshots', exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    for vp_name, w, h in [('360', 360, 640), ('414', 414, 896), ('768', 768, 1024), ('1280', 1280, 800)]:
        for html in ['00_main_dashboard', '01_conocimiento', '02_nuevo', '03_configuracion', '04_file_manager', '05_routing', '06_kanban', '07_panel']:
            ctx = browser.new_context(viewport={'width': w, 'height': h})
            page = ctx.new_page()
            page.goto(f'file:///workspace/osquestador-auditor/prototipo_v6/{html}.html')
            page.screenshot(path=f'prototipo_v6/screenshots/{html}_{vp_name}.png', full_page=True)
            ctx.close()
    browser.close()
"
```

## ANTI-FAKE-PASS v2

No declarar PASS sin haber ejecutado el script y revisado los 32 PNGs.

Procede TASK_015_REVISED (generar v6 con mobile-first + D38-D45 aplicados).
