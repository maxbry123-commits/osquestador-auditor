# 🦈 HANDOFF M64 — TAREA 2 CORREGIDA / PARALELO TOTAL

Fecha: 2026-09-13
Estado: `CURRENT_TASK2_HANDOFF / ADDITIVE_ONLY / PRIOR_ARCHITECTURE_PRESERVED / PARALLEL_ALL`
Repo: `maxbry123-commits/osquestador-auditor@main`
Raíz única: `➡️📂 sharck imput/`

## AUTORIDAD ACTUAL

Leer en este orden:
1. `➡️📂 sharck imput/📁 readme arquitectura sharck imput V2.1.md` — arquitectura previa completa; **no sustituir ni borrar**.
2. `➡️📂 sharck imput/📁 ARQUITECTURA-TAREA2-M64-CORREGIDA-PARALELO-TOTAL.md` — Tarea 2 corregida, sólo adiciones.
3. `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/M64-TASK2-CORRECTED-PARALLEL-ALL.json` — control vigente Tarea 2.
4. este Handoff M64.
5. código/estado/componentes exclusivamente dentro de `➡️📂 sharck imput/`.

## CORRECCIÓN DE M63

M63 permanece como trazabilidad histórica y **no debe borrarse**, pero quedan anuladas como reglas operativas las propuestas introducidas por SOL que no estaban en el INPUT del Director:
- `DynamicFanoutGovernor`;
- reducción de workers según criterio de SOL;
- regla de 1–3/3–10 workers;
- argumento de bajar throughput;
- cualquier interpretación que convierta el paralelismo del Director en opcional, escalado o reducido.

No se toca la arquitectura previa del proyecto para corregir esto. M64 sólo añade la interpretación correcta.

## REGLA CENTRAL

Todos los procesos/pasos del Director mantienen su paralelismo. Ningún paso espera a que termine otro para poder existir. Los procesos que el Director definió con condición propia —por ejemplo Reporter SHARCK cuando detecta necesidad de noticias— conservan esa condición literal; cuando se activan, corren junto a los demás.

`ALL_DIRECTOR_PARALLEL_PROCESSES=true`
`ADDITIVE_IMPROVEMENTS_ONLY=true`
`NO_DYNAMIC_FANOUT_POLICY=true`
`NO_WORKER_REDUCTION_POLICY=true`
`NO_THROUGHPUT_REDUCTION_ARGUMENT=true`

## ARQUITECTURA BASE QUE SE CONSERVA

Se mantiene completa:
`INPUT_RAW → INPUT_LOCK → INTENT/CONSTRAINTS → ENTITY_RESOLUTION → RESEARCH_DECISION → FOCUS_A → QUESTIONS_0_12 || PRESEARCH → DOMAIN/ROLE/GEO/LANGUAGE ROUTER → RESEARCH_DAG → FAN_OUT SOURCES → CAPTURE/SNAPSHOT → EXTRACT/NORMALIZE → INDEX → BM25/SPARSE/DENSE → RRF/RERANK → EVIDENCE GRAPH → CONTRADICTION/COVERAGE/GAP → FOCUS_B → CODE/SKILL/TOOL POINTERS → CONTEXT_COMPRESSION → CONTEXT_PACKAGE → MAIN_LLM`

Y todos sus microkernels/capas existentes.

## ADICIONES M64 SOBRE ESA BASE

En paralelo se mantienen todos los procesos del INPUT literal:
`A/B/C INPUT || P1 RESEARCH || P2 SKILLS || P3 DATASETS || P4 ADAPTERS || P5 TOOLS/PLUGINS || P6 CODA || P7 SHERIFF || P8 ERROR LENS || P8 SOLUTIONS || P10 MULTI-SHARCK || P11 ANTI-HALLUCINATION || P12 REPORTER* || P13 CONTINUOUS* || P14 WATCHDOGS* || P15 PERSISTENCE || MOTORS || HARNESS || 10/100 SEARCH || MEMORY/PROFILE/HANDOFF || SIMULATIONS`

Mejoras aceptadas sólo como suma:
- contexto/memoria aislada por microkernel;
- artefactos directos con pointers;
- evidence ledger append-only;
- source/date/version/hash/license por evidencia;
- checkpoints y recovery independientes;
- resultados/context-deltas versionados sin interrumpir ejecución;
- evidencia oficial/comunidad/negativa en paralelo;
- claim graphs;
- readback/hash de motores;
- EVIDENCIA/INFERENCIA/SIMULACIÓN separadas;
- búsqueda MCP/API/plugin/SDK en paralelo;
- skill/dataset/adapter discovery en paralelo;
- Reporter local/regional/nacional/internacional/redes en paralelo;
- error de un carril no apaga los demás.

## EVIDENCIA DE INVESTIGACIÓN

- OpenAI Agents API (2026-09-10): harness para sesiones largas, herramientas, contexto y subagentes en paralelo.
  https://openai.com/index/introducing-the-agents-api/
- Anthropic multi-agent research: subagentes y tools simultáneos; hasta 90% reducción del tiempo de investigación en queries complejas; contextos aislados y artefactos directos.
  https://www.anthropic.com/engineering/multi-agent-research-system
- MiniMax Agent Team: múltiples Agents en paralelo para tareas largas/complejas.
  https://www.minimax.io/blog/minimax-agent-team-long-running-1779893953
- Kimi Agent Swarm: hasta 300 subagentes simultáneos y 4.000+ tool calls; hasta 4.5× frente a secuencial en búsqueda masiva.
  https://www.kimi.com/en/help/agent/agent-swarm

La evidencia se usa para **fortalecer** el diseño del Director, no para sustituirlo.

## ESTADO ROOT-ONLY PRESERVADO

M64 no elimina componentes ni proyectos. Conserva la reubicación root-only ya realizada y los motores byte-idénticos dentro de la raíz SHARCK:
- Motor2 blob `84d566e2ee4e98e42eb3a864026d067d48caabd9`.
- Engine blob `91e6e4486692eab314be5c7130d8310d3c855397`.
- workflows preservados dentro de `➡️📂 sharck imput/📂 workflows reubicados/`.

## FRONTERA

Esta salida rehace **Tarea 2**. No abre Tarea 3, 4 ni 5 por sí sola.

## VEREDICTO

`M64_CURRENT / TAREA2_REHECHA / ARQUITECTURA_PREVIA_INTACTA / PARALELO_TOTAL_DEL_DIRECTOR / MEJORAS_SÓLO_ADITIVAS / M63_DYNAMIC_RULES_SUPERSEDED`
