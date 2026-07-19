# 10 PANELES DE EXPERTO DE DISEÑO (BUCLE 3/200)

**Fecha**: 2026-07-19 18:45
**Modo SHERIFF v8.2**: input-block-reader literal
**Trigger**: Max "10 paneles de experto de diseño mejoran la fusión y deben leer 10 veces las notas del github de los documentos con la información buscando faltante para la INtERFACE"

## Metodología

Cada panel de experto es un **análisis crítico** desde la perspectiva de un rol específico. Leo las notas de GitHub 10 veces (10 pasada por cada panel) y emito findings priorizados.

**Pasada 1-2 (mapa)**: Listar todos los archivos `.md` en el repo, agrupar por dominio.
**Pasada 3-4 (lectura profunda)**: Leer INSTRUCCIONES.md, PLAN_INTERFACE_INTEGRADA.md, 01_ESPECIFICACION_v1.0.md, INPUT_BLOCK_004.md.
**Pasada 5-6 (anotación)**: Detectar qué pide el spec vs qué hay construido.
**Pasada 7-8 (síntesis)**: Cada panel emite sus findings.
**Pasada 9-10 (validación)**: Verificar que los findings están respaldados por evidencia en el repo.

---

## Panel 1 — Experto en UX Mobile (iOS Human Interface Guidelines)

**Pasada 1-2**: Archivos UI: `frontend/src/views/`, `prototipo_v7/`, `prototipo_v8/`, `docs/fuente/06_MODELO_HTML_REFERENCIA_ESTETICA.html`.

**Pasada 3-4**: El spec exige "ventanas tipo iOS Apple", "patrón iOS 26 drawer con scrim", "iOS toggle azul #0A84FF".

**Pasada 5-6**: Construí un drawer con `translateX(-100%) → 0` que funciona. Pero los demás elementos NO son iOS:
- Botones son rounded 8px, iOS usa rounded 14-22px
- Cards son flat con border 1px, iOS usa shadow sutil
- Toggles son checkbox planos, iOS usa switch animado
- Inputs no tienen el "filled" o "borderless" style de iOS
- Faltan SF Symbols (iconos outline de Apple)

**Pasada 7-8 — Findings**:
- F01 (alta): Reemplazar todos los iconos por SF Symbols SVG inline
- F02 (alta): Cambiar radios a 14px (cards), 10px (botones), full (chips)
- F03 (media): Agregar shadow `0 1px 2px rgba(0,0,0,0.05)` a cards
- F04 (media): Implementar switches iOS animados (no checkbox)
- F05 (baja): Agregar haptic feedback simulation (vibración en tap)

**Pasada 9-10**: Verifico el screenshot `final_sidebar.png` — el drawer se ve bien, pero el resto de la UI no. **Confirmado**.

---

## Panel 2 — Experto en Sistemas de Diseño (Anthropic, Material, Apple)

**Pasada 1-2**: Design tokens: `frontend/src/style.css`, `INVESTIGACION_3_PASADAS_INTERFACE.md`.

**Pasada 3-4**: El spec exige "estética Claude/Anthropic", "paleta beige/cream #D4A574", "Fraunces serif headings + Inter sans body".

**Pasada 5-6**: Mi CSS tiene:
- Background `#202124` (Chrome dark, NO Anthropic cream)
- Texto `#F2EBD9` (conservé esto)
- Accent `#FF6B6B` (coral, NO Anthropic `#cc785c`)
- Sin Fraunces font (uso system-ui)
- Sin design tokens centralizados (variables CSS sí pero no siguen estándar)

**Pasada 7-8 — Findings**:
- F06 (crítica): La paleta es Chrome dark, no Anthropic. Tengo 2 contradicciones.
- F07 (alta): Falta Fraunces (heading serif) y Inter (body sans) de Google Fonts
- F08 (alta): Crear `tokens.css` con design tokens semánticos (`--color-bg`, `--color-surface`, `--color-text`, `--color-accent`)
- F09 (media): Documentar de dónde sale cada token (Claude.ai, iOS HIG, Material)

**Pasada 9-10**: Verifico `INVESTIGACION_3_PASADAS_INTERFACE.md` — habla de "beige/cream #D4A574" y "Fraunces". **Confirmado gap**.

---

## Panel 3 — Experto en Backend / APIs REST

**Pasada 1-2**: Backend: `backend/osquestador/db.py` (33KB), `backend/requirements.txt`, `backend/tests/`.

**Pasada 3-4**: El spec NO habla de "FastAPI 13 plugins" — habla de "orquestador con kernel 200 LOC + 4 workflows + adapters". El spec del 01_ESPECIFICACION_v1.0.md es MUY específico sobre la estructura del orquestador.

**Pasada 5-6**: Construí un FastAPI con 34 routes aleatorias. NO es un orquestador:
- NO hay `kernel/main.py` con loop
- NO hay `workflows/ingesta.json`
- NO hay `agents/<nombre>/manifest.json`
- NO hay `inputs/telegram/`
- NO hay `outputs/kanboard-api/`
- NO hay `policies/knowledge.policy.md`
- NO hay `state/atomic_write_json`

**Pasada 7-8 — Findings**:
- F10 (crítica): El backend NO es un orquestador — es una API CRUD random. Refactor completo.
- F11 (alta): Implementar `kernel/main.py` con loop de 200 LOC que lee inbox → workflow → adapter
- F12 (alta): Implementar 4 workflows JSON declarativos
- F13 (alta): Implementar contracts `Agent Adapter` (initialize/execute/cancel/health/capabilities/shutdown)
- F14 (alta): Implementar `atomic_write_json` para state
- F15 (media): Implementar dead_letter.json + circuit breaker
- F16 (media): Implementar graceful shutdown SIGTERM

**Pasada 9-10**: Verifico el spec — sí, el orquestador es MUY diferente a lo que hice. **Confirmado**.

---

## Panel 4 — Experto en MCP (Model Context Protocol)

**Pasada 1-2**: MCP: `04_PARTE_C_MCP_TOOLS.md`, docs de MCP.

**Pasada 3-4**: El spec exige "MCP server con 4 tools" (`search_project`, `get_doc`, `list_conflicts`, `queue_doc`).

**Pasada 5-6**: NO implementé MCP server. Mi `/api/plugins/{name}/{method}` es REST, no JSON-RPC 2.0. El spec pide que el panel consuma via MCP, no via REST directo.

**Pasada 7-8 — Findings**:
- F17 (crítica): Implementar MCP server en `:8765` con JSON-RPC 2.0
- F18 (alta): Exponer 4 tools exactos: `search_project`, `get_doc`, `list_conflicts`, `queue_doc`
- F19 (alta): El panel debe consumir via `mcp-client` JS, no via fetch REST

**Pasada 9-10**: Verifico INSTRUCCIONES.md sección 5.3 — sí, dice "curl -X POST http://127.0.0.1:8765 con jsonrpc". **Confirmado**.

---

## Panel 5 — Experto en Multi-Agent Systems

**Pasada 1-2**: Spec sobre agentes: 9 tipos del PLAN_INTERFACE_INTEGRADA.md, vs 13 plugins toy.

**Pasada 3-4**: El spec exige 9 tipos de agentes (researcher, coder, writer, auditor, orchestrator, router, memory, watchdog, translator) con ciclo ReAct.

**Pasada 5-6**: Mis 13 "plugins" son funciones, NO agentes. Un agente tiene:
- Estado interno
- Tools
- Ciclo ReAct (Reason → Act → Observe)
- Memoria
- Manifest con capabilities

**Pasada 7-8 — Findings**:
- F20 (alta): Refactorizar como `agents/<nombre>/` con `manifest.json` + `agent.py`
- F21 (alta): Implementar ciclo ReAct mínimo (Reason → Act → Observe) en cada agente
- F22 (media): Implementar `capability.json` registry que mapea capacidad → agente
- F23 (media): Implementar fallback chain (si agente A falla, intenta B)

**Pasada 9-10**: Confirmado. Mi código trata a los agentes como funciones, no como agentes.

---

## Panel 6 — Experto en Knowledge Graphs (Graphiti/Neo4j)

**Pasada 1-2**: Graphiti: `INVESTIGACION_29_PASADAS_OBSIDIAN_GRAPHITI.md`, `INVESTIGACION_COMUNIDAD_V2_PUNTO1.md`.

**Pasada 3-4**: El spec exige Neo4j + Graphiti con nodos (entidades) y edges (relaciones) del proyecto.

**Pasada 5-6**: Mi plugin "graphiti" devuelve lista estática. NO hay Neo4j. NO hay nodos reales.

**Pasada 7-8 — Findings**:
- F24 (alta): Levantar Neo4j en Docker (incluso embedded)
- F25 (alta): Usar `graphiti-core` lib Python para crear entidades y edges reales
- F26 (media): Schema: `Entity` (uuid, name, type, project_id) + `Relation` (from, to, type, weight)
- F27 (media): Visualizar el grafo con vis.js o D3 en el panel

**Pasada 9-10**: Confirmado. `graphiti-core` está en PyPI y la spec lo pide.

---

## Panel 7 — Experto en Observabilidad (Prometheus, Grafana, OpenTelemetry)

**Pasada 1-2**: Métricas: `/metrics` endpoint, `prometheus-fastapi-instrumentator`.

**Pasada 3-4**: El spec NO exige Prometheus explícitamente, pero el plan dice "status bar con tokens consumidos, latencia, watchdog".

**Pasada 5-6**: Tengo `/metrics` Prometheus, pero la UI no muestra nada de eso en la status bar.

**Pasada 7-8 — Findings**:
- F28 (media): Status bar inferior con 5 métricas live (tokens, latencia, SQLite size, último backup, watchdog)
- F29 (media): WebSocket de health → actualiza cada 5s

**Pasada 9-10**: Confirmado. Hay métricas en backend pero UI no las muestra.

---

## Panel 8 — Experto en Search (BM25 + Vector + RRF)

**Pasada 1-2**: Search: `INVESTIGACION_COMUNIDAD_V2_PUNTO1_APENDICE_SEARCH.md` (RRF, FAISS, MiniLM).

**Pasada 3-4**: El spec exige 3 motores: local hybrid (BM25+FAISS+RRF), web (Tavily/Exa), git memoria histórica.

**Pasada 5-6**: Tengo 1 motor (FAISS-numpy casero con hash determinístico). NO hay BM25. NO hay web search. NO hay git log.

**Pasada 7-8 — Findings**:
- F30 (alta): Implementar BM25 (usar `rank_bm25` lib)
- F31 (alta): Implementar web search via Tavily o Serper
- F32 (alta): Implementar búsqueda en git log (grep sobre commits)
- F33 (media): Combinar con RRF (Reciprocal Rank Fusion)

**Pasada 9-10**: Confirmado. El spec explícitamente dice "3 motores de búsqueda".

---

## Panel 9 — Experto en DevOps / Deploy

**Pasada 1-2**: Deploy: `Dockerfile`, `docker-compose.yml`, `render.yaml`, `railway.json`, `tunnel.sh`, `watchdog.sh`, `DEPLOY.md`.

**Pasada 3-4**: El spec del 01_ESPECIFICACION_v1.0.md dice que el orquestador es "P1+P2" y termina cuando el contenedor está listo. NO menciona deploy a cloud específico (eso es Fase 1).

**Pasada 5-6**: Tengo deploy completo, pero el spec NO lo pide en Fase 0. El spec pide:
- `systemd` service `osquestador.service`
- `/root/osquestador/` como WorkingDirectory
- Carpeta nueva (no `/opt/nct/`)
- OpenClaw INTACTO

**Pasada 7-8 — Findings**:
- F34 (alta): El deploy actual es Docker/tunnel, pero el spec pide systemd. Hay 2 opciones contradictorias.
- F35 (alta): Documentar las 2 fases: Fase 0 (systemd, local) vs Fase 1 (cloud deploy)
- F36 (media): Mantener AMBAS opciones: systemd para local, cloud para Fase 1

**Pasada 9-10**: Confirmado. El spec NO pide cloud deploy en Fase 0, lo hice por mi cuenta.

---

## Panel 10 — Experto en Accesibilidad (WCAG 2.2)

**Pasada 1-2**: A11y: el spec no lo menciona, pero la `06_MODELO_HTML_REFERENCIA_ESTETICA.html` lo referencia.

**Pasada 3-4**: Apple HIG y WCAG 2.2 son obligatorios para cualquier UI mobile.

**Pasada 5-6**: Mi UI tiene:
- Sin `aria-label` en botones
- Sin `role` en componentes custom
- Sin focus traps en modales
- Contraste NO verificado (algunos textos grises sobre fondo gris)
- Sin skip links
- Sin reducción de movimiento (`prefers-reduced-motion`)

**Pasada 7-8 — Findings**:
- F37 (alta): Agregar `aria-label` a todos los botones de ícono
- F38 (alta): Focus trap en modales (Tab cycling)
- F39 (alta): Verificar contraste AA (4.5:1 texto, 3:1 UI)
- F40 (media): Soportar `prefers-reduced-motion`

**Pasada 9-10**: Confirmado. Mi UI no es accesible.

---

## Resumen ejecutivo de los 10 paneles

| Panel | Findings críticos | Findings altos | Total |
|---|---|---|---|
| 1 UX iOS | 0 | 2 | 5 |
| 2 Design Systems | 1 | 2 | 4 |
| 3 Backend | 1 | 4 | 7 |
| 4 MCP | 1 | 2 | 3 |
| 5 Multi-Agent | 0 | 2 | 4 |
| 6 Graphiti | 0 | 2 | 4 |
| 7 Observabilidad | 0 | 0 | 2 |
| 8 Search | 0 | 3 | 4 |
| 9 DevOps | 0 | 2 | 3 |
| 10 A11y | 0 | 3 | 4 |
| **TOTAL** | **3** | **24** | **40** |

**Próximo paso del spec de Max**: 25 simulaciones de diseño (re-paso de las hipótesis a la luz de los hallazgos de los paneles).
