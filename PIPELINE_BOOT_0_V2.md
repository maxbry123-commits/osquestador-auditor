# PIPELINE_BOOT_0 — V2 RE-INIT desde 0

**Fecha**: 2026-07-18 21:56
**Trigger**: Max desaprobó v1 ("no cumpliste las instrucciones")
**Modo SHERIFF v8.2**: RE-INIT estricto

## LECCIÓN DE FALLA

v1 fue certificado con:
- ✅ 9/9 instrucciones Max (PASS por grep)
- ✅ 6/6 reglas estéticas (PASS por grep)
- ✅ 7/7 WCAG 2.2 AA (PASS por grep)
- ❌ 0/4 validación visual mobile (NO chequeado)

**Falla raíz**: Certifiqué por `grep` y `wcag`, no por `pixel-perfect mobile view`. Las 4 fotos de Max demuestran que mobile está roto.

## NUEVA ESTRATEGIA v2

### 2 nuevos nodos críticos
1. **NODE_010_MOBILE_FIRST** — todos los HTMLs diseñados mobile-first (≤414px), escalando a desktop (1024+)
2. **NODE_011_VISUAL_VALIDATION** — usar `webapp-testing` (Playwright) o `web_fetch` para screenshot de cada HTML y validación pixel-perfect

### 14 pasos de boot (vs 14 en v1)
- 1-9: mismos (componentes, managers)
- 10: cargar las 4 fotos de Max como gaps adicionales
- 11-14: nuevos para visual validation

### Source of truth extendido
v1: docs internos (INVESTIGACION_*, P0, REGLAS_DURAS)
v2: docs + 4 fotos de Max + screenshots de webapp-testing

### Certification rule reforzada
v1: 9+6+7=22 checks PASS → CERTIFIED
v2: 22 checks + VISUAL_PASS (4 fotos) + MOBILE_PASS (Playwright 360x640) → CERTIFIED

## SECUENCIA DE EJECUCIÓN

```
PIPELINE_BOOT_0  (este)
NODE_001_DISCOVERY_V2  (revisita spec + fotos)
NODE_002_004_REVISED  (inventario + memory + reqs)
NODE_005_007_REVISED  (hipótesis + sim + panel)
NODE_010_MOBILE_FIRST  (NUEVO - mobile breakpoints)
NODE_011_VISUAL_VALIDATION  (NUEVO - Playwright)
TASK_015_REVISED  (8 HTMLs v6 mobile-first)
TASK_022_REVISED  (visual cross-validation)
PIPELINE_END_2
```

## ESTADO

- v1 commits: 11 (TASK_015 → PIPELINE_END, commits `eef5946..628a420`)
- v2 commits: starting fresh
- v1 archivos: PRESERVADOS (no borrar evidencia)
- v2 archivos: NUEVOS con sufijo `_v6` para evitar confusión

## ANTI-REGLA ACTIVADA

**ANTI_FAKE_PASS v2**: si vuelvo a declarar CERTIFIED sin validación visual, fallaré la regla.

**NO_INVENT v2**: si invento métodos SDK, fallaré la regla.

**NO_SKIP v2**: si salto NODE_010 o NODE_011, fallaré la regla.

Procede NODE_001_DISCOVERY_V2.
