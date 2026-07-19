# 10 REFUTACIONES DE DEFECTOS / MEJORAS / FALTANTES (BUCLE 2/200)

**Fecha**: 2026-07-19 18:40
**Modo SHERIFF v8.2**: input-block-reader literal
**Trigger**: Max "Luego 10 refutaciónes de defectos y de mejoras y faltantes"

## Metodología de refutación

Cada refutación es un **contraargumento hostil** que dice "esto está mal / falta / se puede mejorar". Se ataca desde 3 ángulos:
- **Defecto**: algo que NO funciona
- **Mejora**: algo que funciona pero se puede hacer mejor
- **Faltante**: algo que el spec pide y NO existe

---

## REF-01: Los 13 "plugins" NO son los 10 SDKs del spec
**Tipo**: FALTANTE
**Ataco**: El spec pide código fuente REAL de 8+2 SDKs: Haystack, Graphiti, Kanboard, Plandex, Hermes, Obsidian, LiteLLM, MCP SDK + PaddleOCR + Telegram. Yo entregué 13 plugins toy con datos hardcodeados (graphiti.search devuelve lista estática, kanboard.list_tasks devuelve IDs ficticios, claude.invoke NO llama a Anthropic API).
**Defensa imposible**: El spec es claro — código fuente de 8 interfaces aplicado a la UI. Mis plugins son stubs.
**Acción correctiva**: Reemplazar los 13 plugins por adapters reales que importen los SDKs y expongan sus APIs al panel via REST.

## REF-02: Las 70 ideas y 25 decisiones NO están aplicadas en el HTML
**Tipo**: FALTANTE
**Ataco**: Tengo 2 docs (`TABLA_IDEAS_INTEGRADAS.md`, `TABLA_DECISIONES_ARQUITECTONICAS.md`) pero el `prototipo_v7/G_panel_final.html` solo menciona "MCP-Graphiti (D37)" — el resto NO se ve en la UI. Las 11 ideas de UI y 14 ideas de Backend no están clasificadas ni aplicadas.
**Defensa imposible**: Anotar en docs != aplicar en código. La spec dice "11 UI + 14 Backend + funciones abiertas MCP" — debe verse en el panel.
**Acción correctiva**: Mapear las 11 ideas de UI → componentes visibles del panel, las 14 de Backend → endpoints REST del backend. Documentar el mapeo en `MAPEO_IDEAS_UI.md`.

## REF-03: Las 3 ventanas tipo bandeja Anthropic NO existen
**Tipo**: FALTANTE
**Ataco**: El spec pide 3 ventanas tipo Anthropic (Conocimiento del proyecto, Nuevo proyecto, Configuración con tabs). Mi UI tiene una vista "Config" plana con 4 grupos, NO un modal con tabs.
**Defensa imposible**: No hay modal centrado, no hay tabs (Conocimiento/Nuevo/Config), no hay backdrop blur.
**Acción correctiva**: Crear `panel/modals/bandeja.html` con 3 tabs usando estilo Anthropic real (crema/beige, backdrop blur, animación fade-in).

## REF-04: NO hay selección individual/grupo/folder
**Tipo**: FALTANTE
**Ataco**: Spec instrucción 6: "Documentos seleccionables individual/grupo/folder" con 3 patrones + source code real. Mi UI tiene cards estáticas sin modo de selección.
**Defensa imposible**: No hay botones de modo, no hay highlight diferente, no hay checkbox.
**Acción correctiva**: Implementar `<Artefactos>` con state machine (NONE / INDIVIDUAL / GROUP / FOLDER) y CSS condicional.

## REF-05: NO hay 9 tipos de agentes funcionales, hay 13 plugins
**Tipo**: DEFECTO + FALTANTE
**Ataco**: El spec pide 9 tipos de agentes (researcher, coder, writer, auditor, orchestrator, router, memory, watchdog, translator). Yo entregué 13 "plugins" que no son agentes — son herramientas (graphiti, kanboard, ocr, etc). Un agente TIENE estado, herramientas, y ciclo ReAct; un plugin es solo una función.
**Defensa imposible**: No hay distinción clara agente vs plugin en mi código. El plugin "claude" simula ser un agente pero no tiene memoria ni tools.
**Acción correctiva**: Re-arquitecturar como `agents/<nombre>/` con manifest.json (capabilities, skills_supported, models_compatible, status) + ciclo ReAct básico.

## REF-06: NO hay 7 funciones `window.osquestador`
**Tipo**: FALTANTE
**Ataco**: Spec instrucción 9: "funciones abiertas" — debe haber 7 funciones en `window.osquestador` para que otros agentes/AI las usen. Mi código no expone nada al `window` global del browser.
**Defensa imposible**: Console.log(window.osquestador) → undefined.
**Acción correctiva**: Crear `panel/window-osquestador.js` con `window.osquestador = { search, commit, log, diff, blame, checkout, branch }`.

## REF-07: NO hay binario `pip install osquestador`
**Tipo**: FALTANTE
**Ataco**: Spec instrucción 9: "Binario/auto-run" — `pip install osquestador` debe funcionar. Mi repo tiene `start.sh` (script bash) pero no `setup.py`, no `pyproject.toml`, no entry point `osquestador`.
**Defensa imposible**: `pip install -e .` no funciona en mi repo.
**Acción correctiva**: Crear `pyproject.toml` con `[project.scripts] osquestador = "osquestador.cli:main"`.

## REF-08: NO hay binario 10 patterns community aplicados
**Tipo**: FALTANTE
**Ataco**: Spec instrucción 3: "10 patterns: Chat+, Generative UI, Hybrid Input, Proactive UI, Agent Progress Canvas, Multi-Agent Tabs, Supervisor, Transparency, Context Preservation, Intervention controls". Mi panel tiene "Chat" plano sin los 10 patterns visibles.
**Defensa imposible**: Solo 1 de 10 patterns está implementado (Multi-Agent Tabs ≈ tabs de plugins).
**Acción correctiva**: Documentar cada pattern en `PATTERNS_COMUNIDAD.md` con el componente UI que lo implementa + screenshot de evidencia.

## REF-09: NO hay file rows estilo iOS, hay cards
**Tipo**: DEFECTO
**Ataco**: Spec instrucción 5: "ventanas de archivos tipo iOS Apple" (DocumentPicker, File manager Obsidian mobile). Mi Artefactos muestra cards con download button, NO file rows.
**Defensa imposible**: iOS Files app tiene: icono SF Symbol + nombre + metadata (fecha/tamaño) + chevron. Mis cards son: icono + título + chip tipo.
**Acción correctiva**: Restilizar `<Artefactos>` con file rows iOS + SF Symbols SVG.

## REF-10: NO hay integración real con Haystack, Graphiti, Kanboard, etc
**Tipo**: DEFECTO
**Ataco**: Los 13 plugins exponen métodos que devuelven JSON estático. No hay un solo SDK real integrado. `graphiti.search` debería llamar al cliente de Graphiti (Python: `graphiti-core` librería). `kanboard.list_tasks` debería hacer JSON-RPC al Kanboard API. `claude.invoke` debería llamar `anthropic.Anthropic().messages.create()`.
**Defensa imposible**: El backend es un mock, no un orquestador real.
**Acción correctiva**: Por cada plugin, agregar `requirements.txt` con la librería real + implementación con try/except para fallback graceful.

---

## Resumen de las 10 refutaciones

| # | Tipo | Síntoma | Acción |
|---|------|---------|--------|
| 01 | FALTANTE | 13 plugins toy vs 10 SDKs reales | Reemplazar por adapters reales |
| 02 | FALTANTE | 70 ideas NO aplicadas en HTML | Mapear 11 UI + 14 Backend a componentes |
| 03 | FALTANTE | No hay 3 ventanas Anthropic con tabs | Crear `modals/bandeja.html` |
| 04 | FALTANTE | No hay selección 3 modos | State machine + CSS condicional |
| 05 | DEFECTO | 13 plugins ≠ 9 agentes | Re-arquitecturar como `agents/<nombre>/` |
| 06 | FALTANTE | No hay 7 funciones window | Crear `window-osquestador.js` |
| 07 | FALTANTE | No hay binario pip install | Crear `pyproject.toml` con entry point |
| 08 | FALTANTE | 1/10 patterns UI | Documentar los 10 patterns + evidencia |
| 09 | DEFECTO | Cards ≠ iOS file rows | Restilizar con SF Symbols + chevron |
| 10 | DEFECTO | Todo es mock, nada real | Integrar SDKs reales con fallback |

**Próximo paso del spec de Max**: 10 paneles de experto de diseño que mejoran la fusión, leyendo 10 veces las notas de GitHub.

## Commit trail
- BUCLE 2/200 commit: 2026-07-19T22:32:05Z
