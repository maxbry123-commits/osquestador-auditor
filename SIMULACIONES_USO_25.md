# 25 SIMULACIONES DE USO — Interface Osquestador (BUCLE 1/200)

**Fecha**: 2026-07-19 18:35
**Modo SHERIFF v8.2**: input-block-reader literal
**Trigger**: Max "luego haces 25 simulaciónes de uso" (después de las 25 hipótesis)
**Relación**: cada simulación VALIDA o REFUTA una hipótesis del HIPOTESIS_USO_25.md

---

## Metodología de simulación

Cada simulación es un **walkthrough paso a paso** con:
- **Persona**: quién usa el sistema
- **Contexto inicial**: estado del panel antes de la acción
- **Acción**: qué hace el usuario
- **Resultado esperado**: qué debería pasar si la hipótesis es válida
- **Resultado real (en mi implementación actual)**: qué pasa hoy con el código que escribí
- **Gap**: qué falta implementar para que la hipótesis sea verdadera
- **Veredicto**: ✓ VÁLIDA / ✗ REFUTADA / ⚠ PARCIAL

---

## Grupo A — Onboarding y navegación

### SIM-01: Onboarding primer usuario (valida H01)
**Acción**: Max abre el panel por primera vez, ve el sidebar con "osquestador-auditor" como activo y el árbol del proyecto en el panel central.
**Esperado**: Sidebar 240px con 4 proyectos, breadcrumb, árbol con 9 tipos de nodos visibles.
**Real (mi código)**: Sidebar existe pero el árbol NO está como zona fija, los proyectos se listan en una vista "Dashboard" que no es el árbol del proyecto.
**Gap**: Falta zona central con árbol de conocimiento del proyecto (entidades + relaciones de Graphiti).
**Veredicto**: ⚠ PARCIAL — sidebar OK, árbol falta.

### SIM-02: Cambio de proyecto (valida H02)
**Acción**: Max click en "agentes" del sidebar.
**Esperado**: Panel central cambia, URL `/p/agentes`, browser back funciona.
**Real**: Hay tabs pero el cambio de URL no ocurre; el back del browser no navega entre proyectos.
**Gap**: Implementar History API para URLs por proyecto.
**Veredicto**: ✗ REFUTADA.

### SIM-03: Filtro de proyectos persistente (valida H03)
**Acción**: Max filtra "Archivados", refresca la página.
**Esperado**: Filtro persiste.
**Real**: No hay filtro de archivados, no hay localStorage.
**Gap**: Filtros + localStorage.
**Veredicto**: ✗ REFUTADA.

### SIM-04: Breadcrumb clickeable (valida H04)
**Acción**: Max click en "osquestador-auditor" del breadcrumb.
**Esperado**: Vuelve al árbol raíz.
**Real**: No hay breadcrumb.
**Gap**: Componente breadcrumb.
**Veredicto**: ✗ REFUTADA.

### SIM-05: Sidebar drawer mobile (valida H05)
**Acción**: Max en 360px toca ☰.
**Esperado**: Drawer entra con translateX, scrim oscuro.
**Real**: SÍ implementado en mi última versión (final_sidebar.png), con translateX(-100%) → 0.
**Veredicto**: ✓ VÁLIDA (verificado con Playwright screenshot).

## Grupo B — Bandeja Anthropic

### SIM-06: Modal nuevo proyecto (valida H06)
**Acción**: Max click "+ Nuevo proyecto".
**Esperado**: Modal centrado con 3 tabs, backdrop blur.
**Real**: En mi UI hay un botón "+ Proyecto" en el dashboard pero NO abre un modal con tabs.
**Gap**: Modal con 3 tabs (Conocimiento / Nuevo proyecto / Configuración).
**Veredicto**: ✗ REFUTADA.

### SIM-07: Crear proyecto con SDKs (valida H07)
**Acción**: Max tab "Nuevo proyecto", escribe nombre, elige 3 SDKs, click Crear.
**Esperado**: Aparece en sidebar en <1s.
**Real**: No existe el modal.
**Gap**: Mismo gap que SIM-06.
**Veredicto**: ✗ REFUTADA.

### SIM-08: Configuración con toggles iOS (valida H08)
**Acción**: Max abre Configuración.
**Esperado**: 4 grupos con toggle azul iOS, persiste en localStorage.
**Real**: Hay una vista Config con 4 grupos, pero los toggles NO son estilo iOS azul y NO persisten.
**Gap**: Restilizar toggles a iOS + localStorage.
**Veredicto**: ⚠ PARCIAL.

## Grupo C — Chat y agentes

### SIM-09: Chat con streaming (valida H09)
**Acción**: Max escribe "hola" y Enter.
**Esperado**: WebSocket envía, respuesta token a token.
**Real**: ✓ IMPLEMENTADO — verificado E2E con mensaje "estado del sistema" → respuesta del plugin Claude.
**Veredicto**: ✓ VÁLIDA.

### SIM-10: Slash commands (valida H10)
**Acción**: Max escribe `/mem`.
**Esperado**: Autocomplete muestra `/memory`.
**Real**: NO hay autocomplete de slash commands.
**Gap**: Implementar parser de slash commands en el composer.
**Veredicto**: ✗ REFUTADA.

### SIM-11: Panel agentes activos (valida H11)
**Acción**: Max dispara una tarea de un agente.
**Esperado**: Aparece en panel derecho con estado live.
**Real**: NO hay panel derecho de agentes activos (tengo "Plugins" como grid pero no panel contextual).
**Gap**: Panel derecho plegable con tabs.
**Veredicto**: ✗ REFUTADA.

### SIM-12: Routing @agente (valida H12)
**Acción**: Max escribe `@auditor revisa el panel`.
**Esperado**: El agente "auditor" recibe el mensaje.
**Real**: NO implementado. El plugin "audit" existe pero NO se rutea por @.
**Gap**: Parser de @agente en el composer + dispatch.
**Veredicto**: ✗ REFUTADA.

### SIM-13: 9 tipos de agentes (valida H13)
**Acción**: Max abre el panel de agentes.
**Esperado**: 9 agentes visibles (researcher, coder, writer, auditor, orchestrator, router, memory, watchdog, translator).
**Real**: Tengo 13 "plugins" que no son agentes del spec (son herramientas: graphiti, kanboard, etc).
**Gap**: Implementar los 9 agentes del spec, no los 13 plugins toy.
**Veredicto**: ✗ REFUTADA.

## Grupo D — Documentos y archivos

### SIM-14: Selección individual/grupo/folder (valida H14)
**Acción**: Max selecciona 1 doc, luego "grupo", luego "folder".
**Esperado**: Highlight cambia según modo.
**Real**: Hay vista "Artefactos" con cards pero NO hay modos de selección.
**Gap**: Implementar 3 modos de selección con highlight diferente.
**Veredicto**: ✗ REFUTADA.

### SIM-15: Drag&drop PDF + OCR (valida H15)
**Acción**: Max arrastra PDF al panel.
**Esperado**: PaddleOCR procesa, aparece nodo en Graphiti.
**Real**: NO hay drag&drop. El plugin paddleocr existe pero no se invoca desde UI.
**Gap**: Drag&drop handler + integración paddleocr en UI.
**Veredicto**: ✗ REFUTADA.

### SIM-16: File rows estilo iOS (valida H16)
**Acción**: Max ve lista de docs del vault.
**Esperado**: Cada doc = file row (icono + nombre + tipo + fecha + tamaño).
**Real**: Hay cards (no file rows), con chip icon + título + descarga.
**Gap**: Cambiar cards a file rows estilo iOS.
**Veredicto**: ⚠ PARCIAL — cards similares pero no son file rows.

### SIM-17: Toast nuevo documento (valida H17)
**Acción**: Se ingiere un doc.
**Esperado**: Toast con "Ver" / "Archivar".
**Real**: NO hay toast system.
**Gap**: Componente toast.
**Veredicto**: ✗ REFUTADA.

## Grupo E — Memoria y grafo

### SIM-18: Grafo Graphiti visible (valida H18)
**Acción**: Max abre tab "Memoria" del panel derecho.
**Esperado**: Ve nodos y edges del proyecto.
**Real**: Hay vista "Memoria" con cards HOT/WARM/COLD + búsqueda, pero NO grafo visual.
**Gap**: Renderizar grafo (usar vis.js o D3).
**Veredicto**: ✗ REFUTADA.

### SIM-19: Búsqueda en 3 motores (valida H19)
**Acción**: Max busca "graphiti".
**Esperado**: Resultados de local hybrid + web + git.
**Real**: Búsqueda semántica con score% pero solo 1 motor.
**Gap**: Implementar 3 motores con tabs.
**Veredicto**: ✗ REFUTADA.

### SIM-20: Tier HOT/WARM/COLD (valida H20)
**Acción**: Max filtra por tier HOT.
**Esperado**: Solo working memory visible.
**Real**: Hay stats HOT/WARM/COLD pero NO filtro.
**Gap**: Filtros por tier.
**Veredicto**: ⚠ PARCIAL.

## Grupo F — Configuración y funciones abiertas

### SIM-21: Selector de 5 modelos (valida H21)
**Acción**: Max elige Cerebras en Config.
**Esperado**: Cambio inmediato sin restart.
**Real**: NO hay selector de modelo en mi UI.
**Gap**: Dropdown con 5 providers + LiteLLM en backend.
**Veredicto**: ✗ REFUTADA.

### SIM-22: 7 funciones window.osquestador (valida H22)
**Acción**: Otro agente llama `window.osquestador.search("graphiti")`.
**Esperado**: Recibe JSON con resultados.
**Real**: NO existen las 7 funciones expuestas.
**Gap**: Implementar `window.osquestador` con las 7 funciones (search, commit, log, diff, blame, checkout, branch).
**Veredicto**: ✗ REFUTADA.

### SIM-23: pip install osquestador (valida H23)
**Acción**: Max corre `pip install osquestador && osquestador serve`.
**Esperado**: Server arranca + panel abre.
**Real**: NO hay binario, no hay setup.py, no hay entry point.
**Gap**: Crear setup.py + entry point `osquestador` + publicar en PyPI o GitHub Releases.
**Veredicto**: ✗ REFUTADA.

## Grupo G — Status bar y observabilidad

### SIM-24: Status bar live (valida H24)
**Acción**: Max mira la status bar mientras trabaja.
**Esperado**: Tokens, latencia, SQLite, backup, watchdog live.
**Real**: Hay un footer pero no muestra esas métricas.
**Gap**: Status bar inferior con 5 métricas live.
**Veredicto**: ✗ REFUTADA.

### SIM-25: Alerta kernel down (valida H25)
**Acción**: El kernel se cae.
**Esperado**: Alerta roja "KERNEL DOWN" en status bar.
**Real**: NO hay watchdog visual en la UI.
**Gap**: Componente de alerta en status bar + WebSocket de health.
**Veredicto**: ✗ REFUTADA.

---

## Resumen ejecutivo

| Veredicto | Cantidad | % |
|---|---|---|
| ✓ VÁLIDA | 2 | 8% |
| ⚠ PARCIAL | 4 | 16% |
| ✗ REFUTADA | 19 | 76% |

**Diagnóstico real**: el 76% de las hipótesis NO se cumplen con lo que tengo construido. El código actual es una demo visual parcial del spec. Faltan 19 features críticas.

**Próximo paso del spec de Max**: 10 refutaciones de defectos/mejoras/faltantes (de las 25 simulaciones).
