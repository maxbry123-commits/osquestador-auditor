# 25 SIMULACIONES DE USO — SEGUNDA PASADA con V11 (BUCLE 6/200)

**Fecha**: 2026-07-19 19:00
**Modo SHERIFF v8.2**: input-block-reader literal
**Trigger**: Max repite "luego haces 25 simulaciónes de uso" (segunda pasada después del rediseño)

**Relación**: esta es la SEGUNDA pasada de las 25 hipótesis, ahora con el prototipo v11 aplicado. Verifica si los cambios de diseño efectivamente resolvieron los gaps de la primera pasada.

---

## Resultado ejecutivo (segunda pasada)

| Sim | Hipótesis | 1ra pasada | 2da pasada (V11) | Δ |
|---|---|---|---|---|
| SIM-01 | Onboarding primer usuario | ⚠ PARCIAL | ✓ VÁLIDA | ↑ (greeting + 4 cards + sidebar OK) |
| SIM-02 | Cambio de proyecto | ✗ REFUTADA | ⚠ PARCIAL | ↑ (state mgmt OK, falta URL routing) |
| SIM-03 | Filtro persistente | ✗ REFUTADA | ⚠ PARCIAL | ↑ (filtros existen, falta localStorage) |
| SIM-04 | Breadcrumb clickeable | ✗ REFUTADA | ✓ VÁLIDA | ↑↑ (breadcrumb en header OK) |
| SIM-05 | Sidebar drawer mobile | ✓ VÁLIDA | ✓ VÁLIDA | = |
| SIM-06 | Modal nuevo proyecto | ✗ REFUTADA | ✓ VÁLIDA | ↑↑↑ (bandeja 3 tabs implementada) |
| SIM-07 | Crear proyecto con SDKs | ✗ REFUTADA | ✓ VÁLIDA | ↑↑↑ (10 SDKs checkbox visibles) |
| SIM-08 | Configuración con toggles | ⚠ PARCIAL | ✓ VÁLIDA | ↑↑ (iOS toggles animados) |
| SIM-09 | Chat con streaming | ✓ VÁLIDA | ✓ VÁLIDA | = |
| SIM-10 | Slash commands | ✗ REFUTADA | ✓ VÁLIDA | ↑↑↑ (parser + helper text) |
| SIM-11 | Panel agentes activos | ✗ REFUTADA | ⚠ PARCIAL | ↑ (sidebar tiene 9 agentes, falta panel derecho live) |
| SIM-12 | Routing @agente | ✗ REFUTADA | ✓ VÁLIDA | ↑↑↑ (parser implementado) |
| SIM-13 | 9 tipos de agentes | ✗ REFUTADA | ✓ VÁLIDA | ↑↑↑ (researcher/coder/writer/auditor/orchestr/router/memory/watchdog/translator) |
| SIM-14 | Selección 3 modos | ✗ REFUTADA | ✓ VÁLIDA | ↑↑↑ (tabs Individual/Grupo/Folder) |
| SIM-15 | Drag&drop PDF | ✗ REFUTADA | ✗ REFUTADA | = (sigue faltando) |
| SIM-16 | File rows iOS | ⚠ PARCIAL | ✓ VÁLIDA | ↑↑ (icono + nombre + meta + chevron) |
| SIM-17 | Toast notifications | ✗ REFUTADA | ✗ REFUTADA | = (sigue faltando) |
| SIM-18 | Grafo Graphiti visible | ✗ REFUTADA | ✗ REFUTADA | = (solo stats, no visualización) |
| SIM-19 | Búsqueda 3 motores | ✗ REFUTADA | ✗ REFUTADA | = (solo 1 motor) |
| SIM-20 | Tier HOT/WARM/COLD | ⚠ PARCIAL | ⚠ PARCIAL | = (stats OK, sin filtro) |
| SIM-21 | Selector 5 modelos | ✗ REFUTADA | ✗ REFUTADA | = (no hay selector) |
| SIM-22 | 7 funciones window | ✗ REFUTADA | ✓ VÁLIDA | ↑↑↑ (vista API las muestra) |
| SIM-23 | pip install osquestador | ✗ REFUTADA | ✗ REFUTADA | = (no hay binario) |
| SIM-24 | Status bar live | ✗ REFUTADA | ✓ VÁLIDA | ↑↑↑ (7 métricas live) |
| SIM-25 | Alerta kernel down | ✗ REFUTADA | ✗ REFUTADA | = (sin WebSocket de health) |

## Resumen ejecutivo de la segunda pasada

| Veredicto | 1ra pasada | 2da pasada (V11) | Δ |
|---|---|---|---|
| ✓ VÁLIDA | 2 (8%) | 13 (52%) | +11 (+44pp) |
| ⚠ PARCIAL | 4 (16%) | 3 (12%) | -1 (-4pp) |
| ✗ REFUTADA | 19 (76%) | 9 (36%) | -10 (-40pp) |

**El rediseño v11 resolvió 11 hipótesis** (de 19 refutadas a 9). El cambio fue positivo pero todavía quedan 9 hipótesis que requieren código adicional.

## Las 9 que SIGUEN REFUTADAS (requieren BUCLE 7+)

1. **SIM-02**: Falta History API para URL routing
2. **SIM-03**: Falta localStorage para filtros persistentes
3. **SIM-11**: Falta panel derecho live de agentes activos
4. **SIM-15**: Falta drag&drop de PDF + PaddleOCR
5. **SIM-17**: Falta toast system
6. **SIM-18**: Falta renderizar grafo Graphiti (vis.js o D3)
7. **SIM-19**: Falta implementar 3 motores de búsqueda (BM25 + web + git)
8. **SIM-21**: Falta selector de 5 modelos LLM
9. **SIM-23**: Falta binario `pip install osquestador`
10. **SIM-25**: Falta WebSocket de health para alerta kernel down

**Próximo paso del spec**: 10 refutaciones segunda pasada (enfocadas en las 9 que faltan + 1 hallazgo nuevo).
