# 🦈 SHARCK INPUT V3 — CONCURRENT INTELLIGENCE AGENCY ARCHITECTURE

Fecha: 2026-09-13  
Estado: `TASK1_ARCHITECTURE / M59_CODE_CANDIDATE / M60_TARGET / FAIL_CLOSED / NOT_PRODUCTION_PROMOTED`

> Esta V3 es **aditiva**. No borra V2.1, no borra el pipeline transversal anterior, no abre gates físicos y no convierte los procesos del INPUT en una secuencia rígida.

## 1. Objetivo

SHARCK Input sigue siendo la capa universal **PRE-LLM**, pero su modelo operativo se amplía: es el **director de una agencia de investigación**. Recibe el INPUT literal, organiza inteligencia, dispara equipos especializados en paralelo, mantiene procesos continuos, refuta, valida, persiste evidencia y entrega contexto táctico actualizado a `MAIN_LLM / YAIWES_AGENTS`.

Metáfora funcional del INPUT:
- `SHARCK_DIRECTOR` = dirección de inteligencia / orquestación de contexto.
- `BUREAUS + MICROAGENTS` = investigadores especializados estilo FBI/CIA.
- `YAIWES_AGENTS` = equipo táctico de ejecución estilo SWAT/Navy SEALs.
- SHARCK **no sustituye** a YAIWES: le entrega objetivo, evidencia, herramientas, rutas, riesgos, alternativas y contexto actualizado para que ejecute.

Regla raíz preservada:
`LLM propone/razona; runtime controla; retriever encuentra; auditor cuestiona; evidence ledger prueba; verdict determinista autoriza`.

## 2. Regla estructural: NO es un workflow monolítico

Los números/pasos del INPUT son referencias de capacidades. **No son barreras secuenciales.**

Sólo existe un bootstrap determinista mínimo:
`INPUT_RAW → INPUT_LOCK/SHA256 → LITERAL_DECOMPOSITION/InputSpec`.

Después se publica el mismo `InputSpec` inmutable y los procesos elegibles se ejecutan según su modo:
- `FAN_OUT_POOL`: muchos especialistas independientes en paralelo.
- `EVENT_DRIVEN`: se activa cuando el INPUT exige esa capacidad.
- `CONTINUOUS`: permanece activo mientras exista el job.
- `WATCHDOG`: reconsulta por tiempo/condición/frescura.
- `REACTIVATABLE`: un GAP/refutación vuelve a disparar investigación.
- `FAN_IN_GATE`: consolida sin detener bureaus no relacionados.
- `TACTICAL_HANDOFF`: contexto validado/deltas hacia YAIWES.

Objetivo: **reducir el critical path**, no alcanzar un número decorativo de agentes.

## 3. Escala de microagentes

La arquitectura soportará `10..100+` especialistas concurrentes y un target inicial global configurable de `128` microagentes. La concurrencia es adaptativa:
- 1 request si una búsqueda simple resuelve el GAP;
- decenas de especialistas para investigaciones independientes;
- 100+ sólo cuando la amplitud del problema lo justifique.

Control obligatorio: semaphore/backpressure, dedup, idempotency key, timeout, retry/circuit-breaker, rate-limit, token/request/time budget y telemetría por microagente.

`recursive_spawn=false` por defecto. Un agente no puede multiplicar subagentes sin que el Director/ResourceGovernor lo autorice.

## 4. Bureaus concurrentes

1. `RESEARCH_INTELLIGENCE` — búsqueda avanzada oficial/comunidad/web/GitHub/Hugging Face; lattice de queries; fan-out 10–100 por ronda cuando aporte valor.
2. `SKILLS_LEARNING` — mínimo 3 bibliotecas; gate estricto M59: leer 20 `SKILL.md` completos, hash/cache externo, seleccionar 3, conservar 5 standby, progressive disclosure.
3. `DATASET_INTELLIGENCE` — mínimo 3 datasets utilizables + 5 standby; card/license/schema/freshness/sample/fit; streaming/sample antes de adquisición completa.
4. `ADAPTER_COUPLERS` — buscar 3 adapters compatibles + 5 standby cuando aplique; contract/schema/auth/version/read-only smoke.
5. `TOOLS_PLUGINS` — detectar conexiones necesarias y enseñar al agente qué tiene disponible y cómo usarlo; preferir MCP/API; inspect/auth/permissions antes de tool exposure.
6. `PERSISTENCE_CONTEXT_LOOP` — proceso continuo: 12 goals input/output + Council12 + 3 refutaciones + debate + 4 simulaciones; compara evidencia nueva y emite `CONTEXT_DELTA`.
7. `EVIDENCE_SHERIFF` — sentinel/sheriff/validator/judge/guardian; evidencia oficial + comunidad desarrolladora independiente; 10 alternativas ordenadas: cero fricción → menor tiempo → mínima sobreingeniería → evidencia.
8. `ERROR_LENS` — busca fallos, regresiones, breaking changes, comentarios negativos, contra-evidencia y errores previsibles antes de ejecutar.
9. `SOLUTION_GUIDES` — manuales oficiales, guías, runbooks, troubleshooting, evidencia de implementación y ruta exacta de menor fricción.
10. `MULTI_SHARCK_COUNTERINTEL` — rutas independientes y debate; versiones nuevas/anteriores, opción más simple, refutación del contexto primario, preguntas alternativas al usuario.
11. `LITERAL_ALIGNMENT_GUARD` — sheriff anti-alucinación; cada requerimiento literal debe mapear a evidencia/contexto/output o bloquea el release.
12. `NEWS_REPORTER` — sólo si actualidad/noticias importan; local→región/estado→país→internacional + redes/social traces; source-thread graph y watchdog configurable.
13. `ACADEMIC_STUDY` — papers, datasets, benchmarks, métodos y citas; activa cuando el caso sea académico/aprendizaje/investigación.
14. `CONTINUOUS_WORK` — sigue investigando mientras YAIWES ejecuta y publica deltas sin interrumpir la tarea táctica en curso.
15. `WATCHDOG_SCHEDULER` — watchers por bureau o global; detecta staleness, resultados externos y nuevos GAPs; nunca abre por sí mismo gates físicos.
16. `MEMORY_HANDOFF` — `memory.md`, `profile.json`, evidence ledger, source graph, `HANDOFF.md`, executable handoff index y pointers para reusar búsquedas previas.

Estos son **departamentos lógicos**, no 16 procesos únicos. Cada bureau puede fanoutear múltiples microagentes aislados.

## 5. Universal Harness / runtime transversal

No crear un mini sistema operativo distinto por agente. Todos implementan un contrato común inspirado también en los adjuntos de paralelización:

`Job/MicroAgent = validate → execute → checkpoint → verify → publish_artifact → resume/cleanup`.

Servicios reutilizados transversalmente:
- persistent worker pools;
- priority queue;
- async fan-out/fan-in;
- smart batching API;
- dedup in-flight;
- LRU/mmap cache;
- streaming + backpressure;
- idempotency;
- ContextDeltaBus;
- append-only EvidenceLedger;
- artifact/pointer store;
- ResourceGovernor;
- observability/tracing/evals.

Los archivos adjuntos `📌MAVIS-PARALLEL-100X.md` y `📌MAX-SYSTEM-100X-FINAL-1.md` se consideran referencias técnicas para estas primitivas; sus multiplicadores de rendimiento son hipótesis/expectativas hasta benchmark en este repo.

## 6. Arquitectura de información: blackboard + artifacts

Evitar que 100 agentes reinyecten megabytes al Director.

Cada microagente publica:
- resultado estructurado corto;
- evidence pointers;
- SHA/digest;
- métricas;
- GAP/refutación;
- path a artefacto grande.

El `ContextDeltaBus` transporta deltas pequeños y el `EvidenceLedger` preserva provenance. El Director hace fan-in incremental. El paquete final recibe sólo contexto suficiente; el resto permanece recuperable por pointers.

## 7. Memoria/perfil/Handoff por job

Cada job debe persistir al menos:
- `INPUT_RAW.txt` + SHA256;
- `input_spec.json`;
- `memory.md`;
- `profile.json`;
- `evidence-ledger.jsonl`;
- `source-graph.json`;
- `context-deltas.jsonl`;
- artifacts por bureau/microagente;
- `HANDOFF.md`;
- `handoff-index.json` ejecutable;
- `CONTEXT_PACKAGE.json`;
- `validation-checklist.json`;
- `gaps-and-counterevidence.json`.

El Handoff evita rehacer investigación: resuelve pointers anteriores y sólo refresca cuando la fuente/versión/frescura lo exija.

## 8. Tool/plugin/data acquisition

`Research/Skill/Dataset/Adapter/Tool bureaus` descubren y califican; **no se convierten automáticamente en autoridad de instalación**.

Flujo:
`candidate → source/license/version/schema/security gate → acquisition request → canonical immutable Motor 2 → extraction → readback/hash → available pointer`.

MCP/API es el puerto preferente para tools. El contexto entregado al agente incluye `capability + how_to_use + auth/schema + evidence pointer`, nunca secrets.

## 9. Simulación/refutación

Cuando el riesgo o ambigüedad lo amerita, cada bureau puede solicitar una `SimulationCell` con 3 hipótesis diferentes. `MULTI_SHARCK` y `EVIDENCE_SHERIFF` comparan resultados.

Las 4 simulaciones globales del persistence loop se conservan. Una simulación no prueba verdad: alimenta el ledger y debe cruzarse con evidencia real.

## 10. Investigación externa incorporada

- OpenAI: Agents SDK/Responses → handoffs, guardrails, tracing/evals, tools, MCP y harness/sandbox.
- Anthropic: orchestrator-worker multi-agent, búsquedas paralelas, artefactos externos, memoria/context engineering; también evidencia de coste/coordination overhead que obliga a paralelismo adaptativo.
- MiniMax: Agent Teams + operación long-running + context/memory/triggers + dynamic tool/skill search.
- Kimi: Agent Swarm, 100+ subagents en diseños publicados, background tasks/goals/questions, skill discovery y rate-aware retries.
- Hugging Face: skills/tools/MCP, datasets, cards/provenance y streaming.
- Comunidad dev: runaway swarms/context duplication son un riesgo real; hard budgets/telemetry/spawn limits son parte del diseño, no opcionales.

Cross-check completo: `📂 Craxy wall bitácora stated JSON/M60-TASK1-RESEARCH-CROSSCHECK.md`.

## 11. Relación con M59 actual

M59 ya materializó una base útil y **se reutiliza**:
- 11 `LaneKernel` concurrentes + continuous research;
- router 10..100 con semaphore/dedup;
- adapters local/web + pool de claves por entorno;
- skills strict gate;
- datasets/adapters/tools catalogs;
- memory/profile/evidence/Handoff/context artifacts;
- executable handoff pointer resolver;
- request bridge a Motor 2;
- tests/CI candidate.

M59 sigue `SANDBOX_CANDIDATE / NOT_PRODUCTION_WIRED`.

GAPs respecto de esta arquitectura V3 completa: 100+ bureau runtime dinámico, News Reporter explícito, Academic Study, durable queue/restart-resume real, ContextDeltaBus hacia YAIWES, watchdog runtime por proceso/global, ResourceGovernor token/cost, simulaciones de 3 hipótesis realmente ejecutadas, smoke live de providers y wiring de producción.

## 12. Gates preservados

Esta actualización documental NO cambia:
- `physical_repair_allowed=false`;
- `b05_b06_download_allowed=false`;
- `step3_allowed=false`;
- canonical motors `IMMUTABLE`.

No se declara 100x, producción ni integración YAIWES hasta tests/benchmarks/readback/gates posteriores.

## 13. Source of truth de esta ampliación

1. INPUT literal: `📂 Craxy wall bitácora stated JSON/M60-INPUT-BLOCK-LITERAL-2026-09-13.md`.
2. Control machine-readable: `M60-TASK1-SHARCK-AGENCY-ARCHITECTURE.json`.
3. Research cross-check: `M60-TASK1-RESEARCH-CROSSCHECK.md`.
4. Runtime candidate vigente: `📂 input sharck code principal/📂 sharck-v3-parallel-candidate/STRICT-ENTRYPOINT-M59.md`.
5. Arquitectura anterior V2.1 permanece vigente para ADN físico/gates/historial y se amplía, no se reemplaza.

**TASK 1 VERDICT:** `LITERAL_INPUT_PRESERVED / PRIOR_ARCHITECTURE_RECONCILED / PARALLEL_CONTINUOUS_PERSISTENT_AGENCY_TARGET_DEFINED / M59_REUSED / IMPLEMENTATION_GAPS_EXPLICIT / NO_FAKE_PASS`.