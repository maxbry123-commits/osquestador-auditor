# M58 — 18 candidatos OSS para mejorar INPUT + búsqueda sin sobreingeniería

Estado: `RESEARCH_COMPLETE / 8 KEEP_FOR_ACQUISITION / 10 DEFER_OR_REJECT`  
Regla: **no añadir otro stack completo si un primitive pequeño + benchmark resuelve el GAP**. Adquirido ≠ wired ≠ tested ≠ promoted.

## Evidencia de comunidad aplicada

La revisión de experiencias de desarrolladores 2025–2026 muestra un patrón útil para Sharck:

- Hybrid BM25+dense+RRF puede mejorar exact terms, pero no garantiza mejora automática; hay casos donde el gain fue casi nulo.
- Un sistema de producción reportó que su supuesto hybrid quedó meses funcionando vector-only por aplicar un threshold después del RRF; la lección es exigir regression tests/telemetry por cada brazo de retrieval.
- Otro benchmark pequeño obtuvo 74% hit@3 con vector y empeoró al añadir hybrid + reranker; el threshold bien calibrado ayudó más.
- Otros sistemas sí reportan mejoras fuertes con BM25+vector+RRF+rerank, por lo que la decisión correcta es **benchmark por corpus**, no dogma.

Community refs:
- https://www.reddit.com/r/Rag/comments/1v7g3oe/hybrid_search_and_reranking_made_my_rag_worse/
- https://www.reddit.com/r/Rag/comments/1uvl9cx/my_hybrid_search_ran_vectoronly_for_months_and/
- https://www.reddit.com/r/Rag/comments/1sjpl95/hybrid_search_bm25_vectors_rrf_barely_improved/
- https://www.reddit.com/r/LocalLLaMA/comments/1q2seed/production_hybrid_retrieval_48_better_accuracy/

## 8 KEEP — adquisición M58

| # | Componente | Función específica para Sharck | Ref inmutable | Licencia repo | Destino | Decisión |
|---|---|---|---|---|---|---|
| 1 | `xhluca/bm25s` | BM25 local pequeño para brazo lexical/exact-term sin desplegar otro search server | `a213158181d4b3781ba06bc88840f89871f1c775` | MIT | B07 | KEEP |
| 2 | `qdrant/fastembed` | embeddings locales ONNX/CPU como adapter opcional de dense retrieval; evita asumir servicio pesado | `0dab99c23e659e630f642b42c5888af87befb6e2` | Apache-2.0 | B07 | KEEP |
| 3 | `rushter/selectolax` | parser HTML rápido para extracción/normalización antes de indexar | `54c4818d34a9e899aef64cd48bab325fac6c1b90` | MIT (repo; engines mantienen sus avisos propios) | B08 | KEEP |
| 4 | `chatnoir-eu/chatnoir-resiliparse` | parsing/extraction robusta para HTML/WARC adversarial como segundo extractor benchmarkable | `d54c54c445a58cf94f1f01808492b561ca7c61c0` | Apache-2.0 | B08 | KEEP |
| 5 | `FlagOpen/FlagEmbedding` | toolkit BGE para experimentar dense/sparse/multi-vector/rerank bajo evaluación, sin fijarlo como default | `fd1a2bdf69488ffebe0327999d4400d8c8058a0b` | MIT para código | B09 | KEEP |
| 6 | `AnswerDotAI/rerankers` | API pequeña/unificada para probar rerankers sin acoplar Sharck a un modelo/proveedor | `5b9cbb073335b0246bc33e939600f51f934c460d` | Apache-2.0 | B09 | KEEP |
| 7 | `AmenRa/ranx` | eval/comparison/fusion de rankings; permite demostrar si BM25/RRF/rerank mejora o empeora | `7363db0c35e92e90d6fa6fe73907b760678f765e` | MIT | B10 | KEEP |
| 8 | `terrierteam/ir_measures` | interfaz de métricas IR estándar para Recall/MRR/nDCG/MAP y comparabilidad | `64b5afd5cd14f7d8323f9b24a1bfd12afdd1e776` | Apache-2.0 | B10 | KEEP |

### Restricción de pesos/modelos
`FlagEmbedding`, `fastembed` y `rerankers` son adquisición de **código fuente** en M58. Ninguna licencia de repo autoriza automáticamente cualquier modelo/peso externo que el código pueda descargar. Pesos/modelos requieren ref + licencia + benchmark separados.

## 10 candidatos investigados pero NO adquiridos ahora

| # | Candidato | Valor potencial | Riesgo/solapamiento | Veredicto |
|---|---|---|---|---|
| 9 | `embeddings-benchmark/mteb` | benchmark amplio de embeddings/retrieval | demasiado amplio para el primer gate; B10 + golden set interno cubren la necesidad inmediata | DEFER |
| 10 | `qdrant/qdrant` | dense+sparse+multi-vector + hybrid RRF/DBSF | duplica motores/vector/search ya presentes; implica servicio adicional | DEFER |
| 11 | `meilisearch/meilisearch` | keyword+semantic hybrid product search | otro servidor de búsqueda frente a Lucene/OpenSearch/Vespa/Tantivy existentes | DEFER |
| 12 | `typesense/typesense` | keyword+semantic hybrid + filtering/facets | servicio adicional y overlap; validar licencia/edición exacta antes de cualquier adquisición | DEFER |
| 13 | `paradedb/paradedb` | BM25/hybrid dentro de PostgreSQL | extensión/servicio más pesado y superficie operativa mayor | DEFER |
| 14 | `AnswerDotAI/RAGatouille` | ColBERT/late-interaction modular | útil sólo si benchmark demuestra que dense+sparse+simple rerank no basta | DEFER |
| 15 | `HKUDS/LightRAG` | graph/hybrid RAG completo | duplica graph/retrieval/orchestration existentes y aumenta complejidad | REJECT_NOW |
| 16 | `OpenRAG` / stacks RAG integrados similares | pipeline completo listo | overlap alto; usar como referencia de patrones, no dependencia | REFERENCE_ONLY |
| 17 | `neuml/txtai` | semantic search + workflows todo-en-uno | duplica demasiadas capas Sharck | REJECT_NOW |
| 18 | `PrithivirajDamodaran/FlashRank` | reranking CPU pequeño | `rerankers` ya da adapter más general; modelos externos requieren licencia separada | DEFER |

## Por qué NO descargar un quinto servidor de búsqueda ahora

Sharck ya posee Lucene, OpenSearch, Vespa, Tantivy y otras piezas. Qdrant/Meilisearch/Typesense/ParadeDB sólo pasan a KEEP si una prueba demuestra una capability que el inventario actual + adapters pequeños no pueden cubrir. La comunidad muestra que cambiar de store sólo para tener “hybrid” puede ser trabajo innecesario si BM25+dense+fusion ya se puede evaluar con la infraestructura existente.

## Acceptance tests antes de wiring

### Query/Search — B07
Baseline vs candidate sobre el mismo golden corpus:
- `Recall@3`, `Recall@10`, `MRR`, `nDCG@10`.
- exact-term/entity/code hit rate.
- multilingual query slice.
- p50/p95 latency y memoria.
- ningún claim de mejora si CI/paired test no separa ruido razonablemente.

### Web Parse/Extract — B08
- 24 fixtures o superior: clean HTML, malformed HTML, boilerplate, tables, unicode, scripts, long pages.
- extraction fidelity vs golden text/DOM anchors.
- failure rate + throughput + memory.
- fallback policy clara: parser rápido primero; extractor robusto sólo si aporta.

### Retrieval/Rerank — B09
- candidate recall debe estar medido **antes** de rerank.
- comparar no-rerank vs rerank con mismo candidate pool.
- detectar regresiones de rank-1/exact-term.
- p95 latency/cost budget.
- no activar reranker global si sólo mejora una clase de queries.

### Retrieval Eval — B10
- mismo qrels/run produce métricas deterministas.
- `ranx` e `ir_measures` deben concordar en métricas equivalentes dentro de tolerancia documentada.
- guardar corpus/query/qrels hash + tool SHA + config hash.

## Regla 10x

`10x` sólo puede escribirse si un before/after medido demuestra ≥10× en una métrica explícita (latencia, throughput, coste, memoria o error-rate inverso) **sin regresión material de calidad**. Si no, se reporta el delta real; no marketing.

## DO NOT BUILD / DO NOT WIRE

- No crear un nuevo mega-RAG.
- No migrar vector/search store sin evidencia.
- No activar hybrid/rerank por defecto sin golden eval.
- No descargar modelos externos en M58.
- No tocar B01–B06 ni reparar los 23 FAILED desde estas colas.
- No iniciar Step3 wiring; `step3_allowed=false`.

## Salida esperada de M58

`8 source repos pinneados → 4 motores serializados → download/extract/readback → ACQUIRED_READBACK_VERIFIED o GAP explícito → benchmark posterior 1×1 → sólo entonces seleccionar adapters para Step3.`
