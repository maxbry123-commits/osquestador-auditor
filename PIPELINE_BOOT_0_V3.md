# PIPELINE_BOOT_0 V3 — Reinicio desde 0 (v3, post-desaprobación)

**Fecha**: 2026-07-18 22:10
**Trigger**: Max desaprobó v2 ("no seguiste el PIPELINE", "no revisaste los captures")
**Modo SHERIFF v8.2**: RE-INIT estricto + validar CADA paso

## LECCIÓN DE FALLA v1 + v2

### v1 (desaprobado 1ra vez)
- 8 HTMLs estáticos sin validar visualmente
- Certifiqué por grep/wcag

### v2 (desaprobado 2da vez)
- 8 HTMLs mobile-first + 32 screenshots Playwright
- PERO Max enseñó "G_panel_final.html" que NO existe en mi repo
- **Diagnóstico real**: Max tiene SU APP FUNCIONAL, no un mockup

## DIFERENCIA FUNDAMENTAL

| v1+v2 (mío) | Lo que Max quiere (foto) |
|-------------|---------------------------|
| 8 HTMLs estáticos separados | 1 panel funcional integrado |
| Datos hardcodeados | Sidebar con 4 proyectos reales + commits |
| 9 agentes como "lista" | 9 agentes como **botones seleccionables** |
| Sin memoria real | Memoria triple (HOT/WARM/COLD): D-XX decisions, Episodio Graphiti, Repo COLD, vault, Chat |
| Sin filtros | Filtros reales: verificados, INSTRUCCIONES, cross-project, OpenClaw INTACTO |
| Sin tabs | Tabs: block, Mem, Docs |
| Status bar básica | Status: tokens, latencia 340ms, SQLite, FAISS, Neo4j |

## SOURCE OF TRUTH V3

1. **INPUT_BLOCK_004** — 9 instrucciones de Max (preservado)
2. **INPUT_BLOCK_007** — foto de G_panel_final.html (NUEVO spec visual)
3. **REGLAS_DURAS** — REGLA #0 OpenClaw intacto
4. **TABLA_DECISIONES_ARQUITECTONICAS** — D1-D37
5. **FUENTE_DE_VERDAD_OSQUESTADOR** — spec canónico

## NUEVA ESTRATEGIA

### Validar en CADA paso (no al final)

```
PIPELINE_BOOT_0 V3 (este)
   ↓ screenshot
NODE_001 V3 — discovery (lee foto de Max)
   ↓ screenshot
NODE_002-009 V3 — 17 tasks
   ↓ screenshot por task
NODE_010 V3 — mobile-first
   ↓ screenshot mobile-first
NODE_011 V3 — visual validation
   ↓ screenshot match vs foto Max
TASK_015 V3 — 1 solo HTML G_panel_final.html
   ↓ screenshot vs foto Max pixel-by-pixel
TASK_022 V3 — final cross-validation
PIPELINE_END_3 — solo si PASS
```

### Anti-Fake-Pass v3

NO avanzo al siguiente nodo sin:
1. Haber ejecutado el nodo actual
2. Haber generado screenshot
3. Haber LEÍDO el screenshot con la herramienta `read`
4. Haber comparado con el spec (foto de Max o doc)
5. Haber reportado MATCH/MISMATCH explícito

## DECISIONES D46-D52 (NUEVAS v3)

- **D46**: 1 solo HTML integrado `G_panel_final.html` (no 8 separados)
- **D47**: Sidebar con 4 proyectos reales del repo
- **D48**: 9 tipos de agentes como botones (researcher, coder, writer, auditor, orchest., router, memory, watchdog, translator)
- **D49**: Memoria triple HOT/WARM/COLD indexada
- **D50**: Filtros: verificados, INSTRUCCIONES, cross-project, OpenClaw INTACTO
- **D51**: Tabs: block, Mem, Docs
- **D52**: Status bar con 5 fuentes (tokens, latencia, SQLite, FAISS, Neo4j)

## SECUENCIA

```
1. PIPELINE_BOOT_0 V3 (este)
2. NODE_001 V3 (lee foto de G_panel_final.html)
3. NODE_002-009 V3 (17 tasks + gaps)
4. NODE_010 V3 (mobile-first)
5. NODE_011 V3 (visual validation por paso)
6. TASK_015 V3 (1 HTML G_panel_final.html)
7. TASK_022 V3 (cross-validation visual)
8. PIPELINE_END_3 (solo si PASS)
```

Procede NODE_001 V3.
