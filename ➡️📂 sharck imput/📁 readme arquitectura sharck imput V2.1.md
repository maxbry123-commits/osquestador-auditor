# 🦈 SHARCK INPUT V2.1 — ARQUITECTURA MAESTRA ACTUALIZADA

Fecha de corte: 2026-09-11
Estado: `ACTIVE_LOOP_REVIEW_GATE / STEP2 / FAIL_CLOSED`
Fuente de verdad física: `maxbry123-commits/osquestador-auditor@main` → `➡️📂 sharck imput/`.
Control plane base verificado: `STATE rev25`, `PLAN rev13`, `CHECKPOINT CP-V2-CONTROL-PLANE-RECONCILED-023`.
Esta V2.1 **versiona** la arquitectura anterior; no la destruye.

## 1. Objetivo inmutable
Sharck Input es una capa universal **PRE-LLM**. Preserva el input literal, decide qué conocimiento/contexto falta, investiga, captura provenance, recupera código/skills/tools mediante pointers, verifica evidencia y entrega un `CONTEXT_PACKAGE` mínimo suficiente al LLM principal.

Regla raíz:
`LLM propone/razona; runtime controla; retriever encuentra; auditor cuestiona; evidence ledger prueba; verdict determinista autoriza`.

## 2. Pipeline transversal
`INPUT_RAW → INPUT_LOCK → INTENT/CONSTRAINTS → ENTITY_RESOLUTION → RESEARCH_DECISION → FOCUS_A → QUESTIONS_0_12 || PRESEARCH → DOMAIN/ROLE/GEO/LANGUAGE ROUTER → RESEARCH_DAG → FAN_OUT SOURCES → CAPTURE/SNAPSHOT → EXTRACT/NORMALIZE → INDEX → BM25/SPARSE/DENSE → RRF/RERANK → EVIDENCE GRAPH → CONTRADICTION/COVERAGE/GAP → FOCUS_B → CODE/SKILL/TOOL POINTERS → CONTEXT_COMPRESSION → CONTEXT_PACKAGE → MAIN_LLM`

GAP dinámico:
`MAIN_LLM → STRUCTURED_RESEARCH_REQUEST → RESEARCH_DAG → EVIDENCE_DELTA → CONTEXT_PATCH → MAIN_LLM`.

## 3. Invariantes incorporadas del cross-check metodológico
Los adjuntos de referencia refuerzan —sin sustituir el repo— estas reglas:
1. `MASTER INPUT`/`INPUT_RAW` es inmutable; working context es derivado.
2. Fan-out/fan-in sólo para nodos independientes; el estado común usa locks/versionado/checkpoints.
3. DAG/DSL predefinido: ningún modelo improvisa topología durante ejecución.
4. Una tarea = un nodo; un nodo tiene máximo 3 pasos operativos en el contrato multi-entorno.
5. Resultados locales no equivalen a PASS global; existe consolidación y cross-check top-down/bottom-up.
6. Memoria/contexto se recuperan just-in-time mediante pointers; no se intenta cargar todo el universo en la ventana del LLM.
7. Batching/cache/backpressure/dedup son optimizaciones de runtime, nunca atajos a gates de evidencia.

## 4. Microkernels V2.1
Base V2 preservada: `input_lock`, `focus`, `questions`, `role_router`, `geo_language`, `query_lattice`, `community`, `github`, `huggingface`, `labs`, `youtube`, `capture`, `extract`, `index`, `dedup`, `code_pointer`, `skill_pointer`, `tool_finder`, `evidence`, `gap_loop`, `context_compiler`, `checkpoint`, `verdict`.

Capas V2.1 propuestas como adapters/ports, no monolito:
- `capture.warc` → Browsertrix/warcio candidate adapters.
- `provenance.lineage` → OpenLineage; Marquez opcional.
- `observability.otel` → OpenTelemetry Collector.
- `policy.engine` → OPA **o** Cedar tras comparación.
- `supply_chain.sbom` → Syft.
- `supply_chain.vuln` → OSV/Grype/Trivy tras pruning.
- `supply_chain.secrets` → Gitleaks.
- `structured_output` → Instructor/Guardrails/LMQL evaluados contra Pydantic/JSON Schema existentes.
- `evidence.compute` → DuckDB/Polars.
- `evidence.rules` → Soufflé candidate.
- `llm_policy_eval` → DSPy sólo para evaluación/optimización advisory; sin autoridad de PASS.

## 5. ADN físico actual verificado
Catálogo canónico: **117 = 77 legacy + 40 V2**.
Adquisición B01–B04: **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.

Los 23 FAILED se descomponen en:
- **12 partial destinations**: 11 B01–B03 + spaCy B04.
- **11 source-special/symlink**: 9 B01–B03 + huggingface_hub + unstructured.

Exact diff B01–B03, run `34567075204`: `130 missing + 7 changed + 0 extra`.
spaCy B04: 2 missing exactos (`spacy/matcher/polyleven.c`, `website/.vscode/extensions.json`).
Universo partial exacto: **12 componentes / 139 anomalías**.

Causa física confirmada para los partials:
- `130/130 missing` explicados por `.gitignore` root/importado/anidado al re-staging de archivos que eran tracked upstream.
- `7/7 changed` OpenSearch explicados por normalización `.gitattributes` CRLF→LF.
- canonical read-back se comportó fail-closed correctamente.

StrategyDelta M25: sandbox run `34568249222` = representative `SANDBOX_PASS`, pero M35 cuantificó cobertura en sólo **3/12 componentes y 4/139 anomalías**; por tanto `PRODUCTION_ALLOWED=false`.

Provenance GAP special-source: las 9 queues B01–B03 usaron `HEAD` y el flujo histórico no persistió `source_commit` antes del `SOURCE_SPECIAL_FILE_GAP`; el SHA histórico exacto no es recuperable de la persistencia canónica actual. No sustituirlo por HEAD moderno.

## 6. 20X improvements / candidatos B05–B06
Fuente detallada: `📂 Craxy wall bitácora stated JSON/20X-OSS-MEJORAS-2026-09-11.md`.

20 candidatos investigados y deduplicados contra 117 existentes: Browsertrix Crawler, warcio, ArchiveBox, OpenLineage, Marquez, OpenTelemetry Collector, OPA, Cedar, Syft, Grype, Trivy, OSV-Scanner, Gitleaks, Instructor, DSPy, LMQL, Guardrails, DuckDB, Polars, Soufflé.

Estado: `20 RESEARCHED_CANDIDATE_NO_DOWNLOAD / 0 DOWNLOADED / 0 WIRED / 0 TESTED`.
No se incrementa el catálogo canónico hasta pasar `license/ref/commit/overlap/security` y adquisición con read-back.

B05 destino propuesto:
`📂 input sharck code principal/📂 componentes open source/B05-capture-lineage-security/<slug>/`
B06 destino propuesto:
`📂 input sharck code principal/📂 componentes open source/B06-contracts-evidence-policy/<slug>/`

## 7. Multi-entorno / ownership
Agentes canónicos:
- `SOL`: control/state/evidence/motor-watch/consolidación.
- `ASTRA`: M06 auditoría independiente arquitectura/gates/StrategyDelta.
- `CLAUDE`: M07 code/ports/adapters/tests/coverage.
- `GROK`: M08 OSS/licencia/mantenimiento/overlap/contra-evidencia.

Protocolo anti-colisión:
`FETCH latest control → verify OPEN/owner → CLAIM en log propio → EXECUTE scope → EVIDENCE → REPORT → CHECKPOINT`.

Nadie puede reclamar el nodo de otro. `PLAN/STATE/CHECKPOINT/Handoff/Recovery` son shared writes **secuenciales** con SHA fresco. Logs por agente son independientes. Un `409` obliga releer, no overwrite.

Contrato operativo: `📂 Craxy wall bitácora stated JSON/MULTIENV-DAG-3STEP-v1.json`.
Handoff operativo: `HANDOFF-MULTIENV-3STEP-20X-2026-09-11.md`.

## 8. Método único de 3 pasos
**Paso 1 — INVENTARIO/X-RAY/ARQUITECTURA:** identificar estado físico, GAP causal, contratos y source-of-truth; no asumir cierre.
**Paso 2 — ADQUISICIÓN/StrategyDelta:** research → gate → motores canónicos → read-back/hash/state/index; fallos permanecen explícitos.
**Paso 3 — WIRE/PRUNE/MIN-CODE/TEST:** sólo tras M06+M07+M08 + decisión del director; integración 1×1, pruebas y evidence gate.

Cada tarea concreta dentro de un paso es un nodo con máximo 3 subpasos; esto no significa que todo el proyecto tenga sólo tres nodos.

## 9. Gates globales V2.1
`INPUT_HASH_OK`, `OWNER_LOCK_OK`, `SOURCE_TRACE_OK`, `SOURCE_COMMIT_PINNED`, `LICENSE_OK`, `MOTOR_HASH_OK`, `NO_LFS`, `NO_FORCE`, `NO_SILENT_OVERWRITE`, `SPECIAL_FILE_RECORDED`, `SBOM_IF_ACQUIRED`, `SECRET_SCAN_IF_ACQUIRED`, `READBACK_OK`, `TESTS_OK`, `CONTRADICTIONS_RECORDED`, `COVERAGE_OK`, `CHECKPOINT_WRITTEN`.

El LLM jamás promociona un artefacto a PASS por texto o por presencia física.

## 10. Frontera operativa actual
Canonical checkpoint leído: `CP-V2-CONTROL-PLANE-RECONCILED-023`.
Pendientes críticos:
1. `M06 ASTRA` review.
2. `M07 CLAUDE` review/coverage.
3. `M08 GROK` OSS/refutation, ahora incluyendo 20X B05/B06.
4. `M09 external review` sin evidencia.
5. `M10 integration` bloqueada.
6. 23 adquisiciones FAILED siguen sin VERIFIED_CLOSED.
7. StrategyDelta necesita cobertura completa representativa/por-clase antes de producción.
8. B05/B06 necesitan pruning + license/ref/commit gate antes de cualquier descarga.

`STEP3_ALLOWED=false`, `PHYSICAL_REPAIR_ALLOWED=false`, `20X_DOWNLOAD_ALLOWED=false` hasta gates correspondientes.