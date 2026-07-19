# NODE_011 V3 — Visual validation en CADA paso del pipeline

**Fecha**: 2026-07-18 22:16
**Modo SHERIFF v8.2**: VISUAL_VALIDATION v3 — validar CADA paso

## DIFERENCIA v3 vs v2

### v2 (falló)
- 32 screenshots AL FINAL del pipeline
- Certifiqué sin comparar con la foto de Max elemento por elemento

### v3 (reforzado)
- 1 screenshot por CADA paso del pipeline
- Comparación pixel-by-pixel con la foto de Max

## CHECKLIST VISUAL POR ELEMENTO (de la foto de Max)

### Sidebar
- [ ] "PROYECTO ACTIVO" card con border
- [ ] "osquestador-auditor" título mono
- [ ] "maxbry123-commits · privado · 28 commits" subtítulo
- [ ] "PROYECTOS (4)" header
- [ ] "osquestador-auditor" + badge 52
- [ ] "osquestador-memoria" + badge 23
- [ ] "agentes" + badge 18
- [ ] "openclaw" + badge 5
- [ ] "9 TIPOS DE AGENTES" header con icono rayo
- [ ] Grid 3x3 con 9 botones
- [ ] "AGENTES ACTIVOS" header
- [ ] "52 / 100" + progress bar
- [ ] "TAGS ACTIVOS" header
- [ ] Tags "decision" + "tech" + "process"

### Main panel
- [ ] "OSQUESTADOR" header (recortado por tab)
- [ ] Tab "block" + "Mem" + "Docs"
- [ ] "MEMORIA TRIPLA" header
- [ ] Card D-23 con icono nota
- [ ] Card Episodio Graphiti con icono cerebro
- [ ] Card Repo (COLD) con icono link
- [ ] Card vault/panel-file con icono folder
- [ ] Card Chat #1 (Hayes) con icono chat
- [ ] "FILTROS" header
- [ ] Checkbox verificados
- [ ] Checkbox INSTRUCCIONES
- [ ] Checkbox cross-project
- [ ] Checkbox OpenClaw INTACTO

### Status bar
- [ ] "tokens"
- [ ] "latencia 340ms"
- [ ] "SQLite"
- [ ] "FAISS"
- [ ] "Neo4j"

## PROTOCOLO DE VALIDACIÓN

```
Para cada elemento:
1. Generar screenshot del HTML en mobile 360x640
2. Leer el screenshot con `read`
3. Buscar el elemento en el screenshot
4. Comparar con la foto de Max
5. Marcar MATCH o MISMATCH con detalle
```

## OUTPUT

```
prototipo_v7/screenshots/
  ├── step_01_discovery.png
  ├── step_02_inventory.png
  ├── step_03_first_html.png
  ├── step_04_sidebar.png
  ├── step_05_main_panel.png
  ├── step_06_status_bar.png
  ├── final_G_panel_final_360.png
  ├── final_G_panel_final_1280.png
  └── match_report.md (MATCH/MISMATCH por elemento)
```

## ANTI_FAKE_PASS V3

- NO declaro PASS sin haber ejecutado el script Playwright
- NO declaro PASS sin haber LEÍDO el screenshot
- NO declaro PASS sin haber comparado elemento por elemento
- NO declaro PASS sin haber reportado MISMATCH explícito si hay diff

Procede TASK_015 V3 — generar G_panel_final.html.
