# 🦈 SHARCK INPUT V2 — ARQUITECTURA MAESTRA

## Identidad

`Wanted Shark Web / Sharck Input` es una capa universal PRE-LLM para transformar un INPUT literal en contexto investigado, código/skills/tools recuperables y un paquete verificable antes de que el agente principal razone.

Raíz activa: `➡️📂 sharck imput/`
Código fuente: `➡️📂 sharck imput/📂 input sharck code principal/`
Método: `README-METODO-TRABAJO-MULTIAGENTE.md`

La V1 `➡️📂 Shack imput/` se conserva sin destrucción como fuente histórica y evidencia de adquisición 77 componentes.

## Pipeline transversal

`INPUT_RAW → INPUT_LOCK → FOCUS_A → QUESTIONS_0_12 || PRESEARCH → DOMAIN/ROLE/GEO/LANGUAGE ROUTER → RESEARCH_DAG → FAN_OUT SOURCES → SNAPSHOT → EXTRACT/NORMALIZE → INDEX → BM25/SPARSE/DENSE → RRF/RERANK → EVIDENCE GRAPH → COVERAGE/GAP → FOCUS_B → CODE/SKILL/TOOL POINTERS → CONTEXT COMPILER → MAIN LLM`

Si aparece un GAP durante razonamiento:
`MAIN_LLM → STRUCTURED_RESEARCH_REQUEST → SHARCK RESEARCH DAG → EVIDENCE DELTA → CONTEXT PATCH → MAIN_LLM`.

## Microkernels

El backend no será monolítico. Cada kernel implementa contrato pequeño `detect/plan/execute/verify/emit` y se conecta por interfaces/adapters/plugins.

1. `kernel.input_lock` — bytes originales + SHA-256 + version ref.
2. `kernel.focus` — orientación LLM advisory, sin autoridad de PASS.
3. `kernel.questions` — 0–12 preguntas según ambigüedad/impacto.
4. `kernel.role_router` — roles por dominio/capacidad.
5. `kernel.geo_language` — país/idioma/cultura/jurisdicción sin inferir identidad del usuario.
6. `kernel.query_lattice` — consultas exactas/AND/OR/alias/version/site/filetype/issues/benchmarks/contradicción.
7. `kernel.community` — registry permanente 50+ comunidades dev, activación selectiva.
8. `kernel.github` — repos/code/issues/PR/releases/docs/examples/tests/license.
9. `kernel.huggingface` — models/datasets/Spaces/cards/papers/commits.
10. `kernel.labs` — publicaciones de laboratorios y fuentes académicas.
11. `kernel.youtube` — metadata/captions/transcript/ASR fallback.
12. `kernel.capture` — snapshot/provenance/content hash.
13. `kernel.extract` — main-content/document parsers.
14. `kernel.index` — inverted/BM25/sparse/dense exact/hybrid.
15. `kernel.dedup` — SHA exact + MinHash/near-duplicate.
16. `kernel.code_pointer` — símbolos/call graph/source refs, lectura on-demand.
17. `kernel.skill_pointer` — skills versionadas recuperables bajo demanda.
18. `kernel.tool_finder` — capability → registry → shortlist → security/test → expose.
19. `kernel.evidence` — claims/support/contradictions/source classes.
20. `kernel.gap_loop` — coverage thresholds + StrategyDelta.
21. `kernel.context_compiler` — contexto mínimo suficiente + provenance.
22. `kernel.checkpoint` — estado durable por nodo/agente.
23. `kernel.verdict` — cierre por evidencia, no por texto de LLM.

## Cuatro universos + Capability Graph

- `KNOWLEDGE` → páginas, docs, papers, comunidad y evidencia.
- `CODE` → repos, funciones, clases, callers/callees, versiones.
- `SKILLS` → procedimientos/guías/skills bajo demanda.
- `TOOLS` → capacidades ejecutables vía MCP/API/plugins.
- `CAPABILITY_GRAPH` conecta necesidad → conocimiento → código → skill → tool.

## Modos de investigación

- `D0_STRICT`: reglas, índices, BM25, RRF, grafos, hashes; máxima reproducibilidad sobre snapshot fijo.
- `D1_FROZEN_NEURAL`: D0 + embeddings/rerankers fijados/versionados.
- `D2_ADVISORY_LLM`: Focus A/B propone preguntas/enfoque; nunca controla integridad, evidencia ni PASS.

## Research Slots

Cada entidad importante crea slots: definición, arquitectura, función, API, implementación, dependencias, compatibilidad, performance, seguridad, errores/issues, limitaciones, licencia, benchmarks, alternativas, mantenimiento, versión y contra-evidencia.

Gate de cierre de slot: fuentes mínimas + independencia + freshness + cobertura + contradicción evaluada o límite explícito.

## Router de roles

Ejemplos de roles combinables: `SOFTWARE_ARCHITECT`, `DEVELOPER`, `UI_UX_DESIGNER`, `VIDEO_ENGINEER`, `GRAPHIC_DESIGNER`, `CHEF`, `SCIENTIST`, `NEWS_RESEARCHER`, `LEGAL_RESEARCH`, `COUNTRY_SPECIALIST`, `LANGUAGE_SPECIALIST`, `CULTURE_RESEARCH`, `RELIGION_RESEARCH`.

Un tema religioso activa dominio de fuentes; no implica ni registra religión del usuario.

## Multiagente de ingeniería

- SOL: integra, consolida y mantiene control/estado.
- CLAUDE: code/ports/adapters/tests.
- GROK: OSS/comunidad/HF/labs/alternativas/contradicciones.
- ASTRA: auditoría independiente, arquitectura, mejora versionada y verificación.

Los cuatro escriben en Craxy Wall usando owner locks y checkpoints. Ningún agente puede borrar el trabajo de otro; una mejora crea versión nueva o patch.

## Adquisición física

Única lógica autorizada: motores canónicos ya existentes en:
`➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/`.

No se editan. Para los 30 nuevos componentes se crean tres jobs/instancias de 10 con queue/state/index independientes y destino explícito bajo:
`➡️📂 sharck imput/📂 input sharck code principal/📂 componentes open source/`.

## Gates globales

`INPUT_HASH_OK`, `OWNER_LOCK_OK`, `SOURCE_TRACE_OK`, `MOTOR_HASH_OK`, `NO_LFS`, `NO_FORCE`, `NO_SILENT_OVERWRITE`, `READBACK_OK`, `TESTS_OK`, `CONTRADICTIONS_RECORDED`, `CHECKPOINT_WRITTEN`.

El proyecto no pasa a integración de los 30 componentes hasta que cada adquisición tenga estado individual; los componentes fallidos pueden quedar en GAP mientras otros lotes independientes continúan.
