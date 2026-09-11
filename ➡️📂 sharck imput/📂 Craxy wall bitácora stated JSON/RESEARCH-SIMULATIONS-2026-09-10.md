# 🦈 RESEARCH + SIMULATIONS — SHARCK INPUT

Fecha: 2026-09-10 / 2026-09-11 UTC boundary.
Owner: SOL (research orchestration, parallel-safe).
Scope lock: **INPUT + CONTEXT ONLY**. No full workflow orchestration.
Fuente operativa: Craxy Wall + archivos del proyecto + fuentes externas trazables.

## Simulación transversal 1 — 10 puntos del INPUT

1. `INPUT_RAW_LOCK` — mantener bytes/texto original + hash + provenance. No mutar el INPUT.
2. `INTENT_CONSTRAINTS` — separar hechos del usuario, objetivos, restricciones y preguntas abiertas. Mejora: NLP/rules local antes de LLM cuando sea posible.
3. `ENTITY_RESOLUTION` — resolver entidades/fechas/alias sin sobrecargar contexto. Mejora: spaCy + reglas; Duckling queda candidato manual por licencia GitHub NOASSERTION.
4. `RESEARCH_DECISION` — decidir qué necesita búsqueda, qué ya está demostrado y qué debe preguntarse. Mantener Focus LLM advisory, no autoridad de PASS.
5. `SOURCE_TOOL_SKILL_DATASET_DISCOVERY` — no cargar catálogos completos. Usar progressive disclosure / tool search / pointers.
6. `RETRIEVAL` — federar web, GitHub, HF, skills/datasets y fuentes primarias con referencias, no una sola búsqueda.
7. `EVIDENCE_CONTRADICTION` — claims con soporte, contradicción, independencia, freshness y fuente.
8. `COVERAGE_GAPS` — cerrar sólo cuando slots alcancen reglas; si no, StrategyDelta.
9. `CONTEXT_COMPRESSION` — comprimir sólo después de conservar pointers/provenance; evitar resumen irreversible del RAW.
10. `CONTEXT_PACKAGE` — entregar a la LLM únicamente contexto de alta señal + pointers recuperables on-demand.

## Investigación cruzada — hallazgos

### OpenAI
Fuente: https://openai.com/index/new-tools-for-building-agents/
Hallazgo FACT: OpenAI expone web search, file search y herramientas integradas con citas/observabilidad. Para Shark esto refuerza `source discovery -> retrieval -> citation/provenance`, no un monolito.

### Anthropic
Fuentes:
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.anthropic.com/engineering/advanced-tool-use
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
Hallazgos FACT: contexto es recurso finito; recomiendan contexto just-in-time mediante identificadores/pointers y descubrimiento de tools bajo demanda; evals deben acompañar cambios. Mejora Shark: `Context Pointer Store + deferred tool/skill expansion + eval gate`.

### Hermes Agent / comunidad
Fuentes:
- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/configuration.md
Hallazgos FACT: skills por progressive disclosure, Skills Hub, context compression y límites de lectura; los skills completos se cargan sólo cuando son relevantes. Mejora Shark: metadata corta siempre disponible y cuerpo del skill recuperado on-demand.

### OpenClaw
Fuentes:
- https://github.com/openclaw/openclaw
- https://github.com/openclaw/clawhub
Hallazgo FACT: OpenClaw mantiene inventario/registry de plugins y permite seleccionar Skills/Connectors por sesión. Mejora Shark: construir snapshot de capabilities y seleccionar un subconjunto antes de entregar contexto a la LLM.

### Hugging Face
Fuentes verificadas en GitHub:
- https://github.com/huggingface/huggingface_hub
- https://github.com/huggingface/datasets
- https://github.com/huggingface/hf-mcp-server
Hallazgo FACT: las tres repos son oficiales, no archivadas y activas al revisar. `huggingface_hub` y `datasets` usan Apache-2.0; `hf-mcp-server` MIT. El conector HF de esta sesión rechazó `dataset_search` por configuración del servidor; por eso no se inventaron datasets específicos. El bridge se diseña para usar Hub/MCP/datasets cuando el runtime tenga esa capacidad habilitada.

## Simulaciones de fallo y mejora

S1 — INPUT enorme: RAW queda intacto; extraer facts/constraints/pointers y no enviar todo el corpus a la LLM.
S2 — 1000 tools/skills disponibles: sólo metadata searchable; expandir 3–8 relevantes on-demand.
S3 — fuente web contradice repo oficial: Evidence Graph conserva ambas; autoridad/freshness/independencia decide sin borrar contradicción.
S4 — dataset HF requiere código remoto: default `trust_remote_code=false`; bloquear hasta policy explícita.
S5 — compresión elimina detalle necesario: Context Package conserva pointer/hash/URL para recuperar original.
S6 — investigación produce más ruido que señal: eval de context relevance/faithfulness + token budget antes de promoción.

## Batch B04 — 10 candidatos aprobados para adquisición aislada

Todos: repo público no archivado + utilidad directa al INPUT/context + licencia SPDX clara en GitHub al revisar.

1. `huggingface/huggingface_hub` — Hub client/discovery — Apache-2.0.
2. `huggingface/datasets` — dataset loading/streaming/catalog — Apache-2.0.
3. `huggingface/hf-mcp-server` — puente MCP oficial HF — MIT.
4. `microsoft/LLMLingua` — compresión de contexto/prompt — MIT.
5. `explosion/spaCy` — tokenización/NER/rule matching — MIT.
6. `microsoft/markitdown` — normalización documental a Markdown — MIT.
7. `Unstructured-IO/unstructured` — parsing/partitioning documental — Apache-2.0.
8. `feyninc/chonkie` — chunking ligero/semántico — MIT.
9. `vibrantlabsai/ragas` — evaluación de retrieval/context — Apache-2.0.
10. `confident-ai/deepeval` — evals de contexto/LLM — Apache-2.0.

## Candidatos NO automáticos

- `facebook/duckling` — técnicamente útil para fechas/cantidades, pero GitHub devuelve licencia `NOASSERTION`; requiere revisión manual antes de cualquier adquisición.
- `Arize-ai/phoenix` — útil para observabilidad/evals, pero GitHub devuelve licencia `NOASSERTION`; no entra en B04 automático.
- `protectai/llm-guard` — repo encontrado archivado; excluido del batch.

## Gates B04

`RESEARCHED -> OFFICIAL_SOURCE_OK -> ACTIVE_REPO_OK -> LICENSE_SPDX_OK -> INDEXED -> QUEUED_B04 -> CANONICAL_MOTOR -> READBACK -> VERIFIED_CLOSED|GAP`.

B04 debe usar workflow independiente para no reejecutar B01/B02/B03.
