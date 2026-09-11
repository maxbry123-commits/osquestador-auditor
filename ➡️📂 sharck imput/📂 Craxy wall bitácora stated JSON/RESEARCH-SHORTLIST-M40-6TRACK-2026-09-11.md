# SHARCK INPUT — M40 — 6-TRACK RESEARCH SHORTLIST

Fecha: 2026-09-11
Owner: `SOL-0`
Estado: `REVIEW_READY_WAITING_DIRECTOR_APPROVAL`
Regla: este documento es investigación. `RESEARCHED != APPROVED != DOWNLOADED != VERIFIED_CLOSED != WIRED`.
No autoriza descargas nuevas ni modifica el catálogo canónico 117.

Clasificación:
- `NEW_CANDIDATE`: candidato a revisión/aprobación.
- `EXISTING_117`: ya está en catálogo canónico; no duplicar.
- `EXISTING_20X`: ya está en la lista 20X no canónica; no duplicar.
- `REFERENCE_ONLY`: usar patrón/API/benchmark sin vendoring automático.
- `DEFER`: útil, pero no prioritario o con riesgo/mantenimiento/licencia.
- `REJECT`: no adquirir bajo estado actual.

## I04 — simulaciones, investigación cruzada, evals y oportunidades 100x
1. `Inspect AI` — NEW_CANDIDATE — framework OSS del UK AI Security Institute; evals multi-turn, tools, model grading y >200 evals. https://github.com/UKGovernmentBEIS/inspect_ai
2. `Promptfoo` — NEW_CANDIDATE — eval/red-team de prompts, agentes y RAG; CLI/CI, MIT; OpenAI anunció adquisición manteniendo OSS. https://github.com/promptfoo/promptfoo
3. `BrowserGym` — NEW_CANDIDATE — entorno extensible para automatización web con WebArena/WebArenaVerified/VisualWebArena/WorkArena/AssistantBench. https://github.com/ServiceNow/BrowserGym
4. `AgentLab` — NEW_CANDIDATE — desarrollo y benchmarking reproducible de web agents sobre BrowserGym, paralelización Ray y journal reproducible. https://github.com/ServiceNow/AgentLab
5. `SWE-bench` — NEW_CANDIDATE_EVAL — eval reproducible de agentes/código contra issues reales GitHub con Docker. https://github.com/SWE-bench/SWE-bench
6. `BFCL V4` — REFERENCE_ONLY — benchmark Berkeley para tool/function calling y evaluación agentic multi-turn; útil como batería externa. https://gorilla.cs.berkeley.edu/leaderboard
7. `MCPMark` — NEW_CANDIDATE — benchmark de uso real MCP sobre GitHub/Filesystem/Postgres/Playwright/Notion con verificación automática y entornos aislados. https://github.com/eval-sys/mcpmark
8. `tau2/tau3-bench` — NEW_CANDIDATE_EVAL — simulación agente↔usuario↔tools con políticas, dominios y seeds reproducibles; útil para failure-paths y tool-policy. https://github.com/sierra-research/tau2-bench
9. `AgentBench` — NEW_CANDIDATE_EVAL — benchmark de setup de agente con tareas reales y checks deterministas; usar tras revisión de alcance/overlap. https://github.com/agentbench/agentbench
10. `Ragas + DeepEval` — EXISTING_117 — ya #116/#117; mantener como baseline RAG/LLM para comparar los nuevos frameworks, no duplicar adquisición. https://github.com/vibrantlabsai/ragas ; https://github.com/confident-ai/deepeval

## I06 — Hugging Face: skills, datasets, recursos y bridge
1. `huggingface_hub` — EXISTING_117 (#108) — cliente oficial Hub/discovery/pointers; reparar GAP existente, no duplicar. https://github.com/huggingface/huggingface_hub
2. `Hugging Face Datasets` — EXISTING_117 (#109) — load/streaming/catálogo de datasets; VERIFIED_CLOSED existente. https://github.com/huggingface/datasets
3. `HF MCP Server` — EXISTING_117 (#110) — MCP oficial Hub + Gradio tools; VERIFIED_CLOSED. https://github.com/huggingface/hf-mcp-server
4. `HF Skills` — EXISTING_117 (#40) — skills estandarizados; `hf-cli` es bootstrap recomendado y hay workflows instalables on-demand. https://github.com/huggingface/skills
5. `Dataset Viewer REST API` — REFERENCE_ONLY_PORT — `/is-valid`, `/splits`, `/rows`, `/search`, `/filter`, `/parquet`, `/size`, `/statistics`, `/croissant`; ideal para `hf.dataset_viewer` sin bajar datasets completos. https://huggingface.co/docs/dataset-viewer/quick_start
6. `Spaces agents.md` — REFERENCE_ONLY_PORT — Gradio Spaces compatibles exponen esquema/call/poll/upload para agentes; crear `hf.space_tool` en vez de vendorizar cada Space. https://huggingface.co/docs/hub/en/spaces-agents
7. `Text Embeddings Inference (TEI)` — NEW_CANDIDATE — servidor OSS HF para embeddings/rerank/SPLADE, API OpenAI-compatible, health/metrics; candidato `hf.embedding_server`. https://github.com/huggingface/text-embeddings-inference
8. `Agent Traces / Session Traces Format` — REFERENCE_ONLY_PORT — HF renderiza JSONL de Claude Code/Codex/Pi; candidato de formato `trace.agent_run`, con redacción de secretos obligatoria. https://huggingface.co/docs/hub/agent-traces
9. `Inference Endpoints MCP Server` — REFERENCE_ONLY_INTEGRATION — inspecciona/crea/pausa/escala endpoints y obtiene logs/metrics; usar como integración MCP, no necesariamente vendorizar. https://huggingface.co/docs/inference-endpoints/guides/mcp_server
10. `Text Generation Inference (TGI)` — REJECT_NEW_ACQUISITION — HF lo marca maintenance mode y el repo fue archivado en 2026; preferir alternativas activas si se requiere serving. https://github.com/huggingface/text-generation-inference

## I07 — comunidad de programación/código: análisis, transformación y evidencia de cambios
1. `LibCST` — NEW_CANDIDATE — CST Python lossless que conserva comentarios/whitespace; fuerte para codemods y cambios auditables. https://github.com/Instagram/LibCST
2. `Comby` — NEW_CANDIDATE — búsqueda/rewrite estructural multi-lenguaje, más semántica que regex; Apache-2.0. https://github.com/comby-tools/comby
3. `Difftastic` — NEW_CANDIDATE — diff estructural basado en sintaxis; útil como verifier de cambios y para minimizar falsos diffs. https://github.com/Wilfred/difftastic
4. `tree-sitter-graph` — NEW_CANDIDATE — DSL para construir grafos desde código parseado por Tree-sitter; encaja con Evidence/Code Graph. https://github.com/tree-sitter/tree-sitter-graph
5. `jscodeshift` — NEW_CANDIDATE — codemods JS/TS, runner + recast, preserva estilo y soporta dry-run/stats. https://github.com/facebook/jscodeshift
6. `Joern` — NEW_CANDIDATE — Code Property Graph cross-language + query DSL + taint analysis; fuerte para relaciones/flujo y auditoría de código. https://github.com/joernio/joern
7. `CodeQL queries/libraries` — NEW_CANDIDATE_WITH_LICENSE_REVIEW — repo OSS de queries/libraries; separar licencia del CLI/engine antes de integrar. https://github.com/github/codeql
8. `ts-morph` — NEW_CANDIDATE — wrapper TypeScript Compiler API para navegar/analizar/modificar TS/JS programáticamente. https://github.com/dsherret/ts-morph
9. `srcML` — DEFER_LICENSE_GATE — representación XML y query/transform para C/C++/C#/Java; GPL-3.0 exige revisión de compatibilidad. https://github.com/srcML/srcML
10. `GitHub stack-graphs` — REJECT_NEW_ACQUISITION — repo archivado y no mantenido desde 2025; mantener sólo como referencia conceptual. https://github.com/github/stack-graphs

## I08 — OpenClaw, Hermes, GitHub/HF y comunidades de agentes
1. `Hermes Agent` — NEW_CANDIDATE — herramientas, skills, memoria persistente, MCP, gateways, subagentes y aislamiento; comparar contra runtime existente antes de adquirir. https://github.com/NousResearch/Hermes-Agent
2. `OpenClaw` — NEW_CANDIDATE_OR_REFERENCE — MCP server/client registry, Gateway, ACP y tool filtering; encaja especialmente como bridge/control-plane, no como autoridad de PASS. https://github.com/openclaw/openclaw
3. `Agent Skills open standard` — NEW_CANDIDATE_SPEC — formato abierto `SKILL.md` + scripts/resources, mantenido por Anthropic/comunidad; posible contrato común de skills. https://github.com/agentskills/agentskills
4. `MCP Registry` — EXISTING_117 (#46) — ya catalogado; usar API oficial como discovery, no duplicar. https://github.com/modelcontextprotocol/registry
5. `OpenHands Software Agent SDK` — NEW_CANDIDATE — Python/TS/REST, workspaces locales/efímeros, tools, conversations, server API; útil como referencia/adapter de coding agents. https://github.com/OpenHands/software-agent-sdk
6. `Cline` — NEW_CANDIDATE — Apache-2.0; SDK/CLI/headless, plugins/hooks, MCP y equipos multiagente; candidato fuerte para harness externo. https://github.com/cline/cline
7. `goose` — NEW_CANDIDATE — agente local/extensible, multi-model, MCP, desktop/CLI; revisar upstream oficial/AAIF y pin exacto antes de queue. https://github.com/block/goose
8. `OpenCode` — NEW_CANDIDATE — coding agent terminal con agentes build/plan y subagent general; verificar upstream/ref/licencia exactos antes de adquirir. https://github.com/sst/opencode
9. `mini-SWE-agent` — NEW_CANDIDATE — agente mínimo para issues GitHub, múltiples sandboxes y compatibilidad multi-model; valioso como baseline minimal-harness. https://github.com/SWE-agent/mini-swe-agent
10. `Continue` — EXISTING_117_MAINTENANCE_RISK (#103) — repo ahora read-only/no mantenido; no promover como runtime estratégico nuevo; conservar sólo hasta decisión de reemplazo. https://github.com/continuedev/continue
11. `Roo Code` — REJECT — repo archivado tras sunset 15-May-2026; no adquirir. https://github.com/RooCodeInc/Roo-Code

## I09 — puntos/tareas/componentes web adicionales
1. `Browsertrix Crawler` — EXISTING_20X (#118) — captura browser high-fidelity WARC/WACZ; mantener en gate de licencia/pin (AGPL). https://github.com/webrecorder/browsertrix-crawler
2. `warcio` — EXISTING_20X (#119) — lectura/escritura WARC para hashes/replay; no duplicar investigación.
3. `ArchiveBox` — EXISTING_20X (#120) — snapshot durable HTML/PDF/PNG/JSON/WARC/SQLite + API/webhooks; útil para evidence snapshot. https://github.com/ArchiveBox/ArchiveBox
4. `Newspaper4k` — NEW_CANDIDATE — extractor de artículos/títulos/autores/metadata, 80+ idiomas, tests/evaluation; MIT. https://github.com/AndyTheFactory/newspaper4k
5. `Goose3` — NEW_CANDIDATE — extracción de cuerpo, imagen principal, video embebido y metadatos; comparar calidad contra Trafilatura/Readability antes de KEEP. https://github.com/goose3/goose3
6. `selectolax` — NEW_CANDIDATE — parser HTML5 rápido con Lexbor y CSS selectors; candidato para normalize/extract determinista. https://github.com/rushter/selectolax
7. `curl_cffi` — NEW_CANDIDATE_WITH_POLICY_GATE — HTTP client sync/async con TLS/JA3/HTTP2/HTTP3 impersonation y retries; útil para fetch resiliente, sujeto a política de uso web. https://github.com/lexiforest/curl_cffi
8. `Camoufox` — DEFER_EXPERIMENTAL — Firefox orientado a scraping/agentes y fingerprinting; mantenimiento 2026 en recuperación y alto riesgo operacional/política. https://github.com/daijro/camoufox
9. `camofox-browser` — DEFER_EXPERIMENTAL — REST wrapper para Camoufox con accessibility snapshots y stable refs; evaluar sólo si navegación legítima falla con browser estándar. https://github.com/jo-inc/camofox-browser
10. `Patchright` — DEFER_POLICY_SECURITY — Playwright parchado para anti-detection; no default. Requiere revisión legal/policy/security y CVE de dependencias antes de cualquier queue. https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python
11. `Browserless` — NEW_CANDIDATE_LICENSE_GATE — browser-as-a-service Docker para Playwright/Puppeteer/REST; revisar licencia de uso antes de adquirir. https://github.com/browserless/browserless
12. `Whoogle` — REJECT — proyecto anunció fin de desarrollo 24-Jul-2026 y ya no devuelve resultados. https://github.com/benbusby/whoogle-search
13. `searx` clásico — REJECT_DUPLICATE_STALE — no mantenido; el catálogo ya tiene SearXNG (#1), que es la rama activa. https://github.com/searx/searx

## I10 — agentes de investigación + recomendaciones OpenAI/Anthropic sobre input/context/web
1. `OpenAI Agents SDK` — NEW_CANDIDATE — SDK OSS con agents, handoffs, guardrails y tracing; candidato para adapter/harness, no para sustituir runtime determinista. https://github.com/openai/openai-agents-python
2. `OpenAI Responses API tool model` — REFERENCE_ONLY_ARCH — herramientas built-in como web/file search + function calling + remote MCP; validar el patrón `tool pointer + provenance` en Sharck. https://platform.openai.com/docs/quickstart
3. `OpenAI sandbox/harness separation` — REFERENCE_ONLY_ARCH — en 2026 OpenAI recomienda separar harness de compute/sandbox para seguridad, durabilidad y escala; encaja con runtime controla/LLM razona. https://openai.com/index/the-next-evolution-of-the-agents-sdk/
4. `OpenAI manager vs handoffs` — REFERENCE_ONLY_ARCH — multi-agent como graph; manager conserva control del workflow, handoffs transfieren control. Para Sharck preferir supervisor/fan-in en shared writes. https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
5. `Promptfoo` — NEW_CANDIDATE_CROSS_TRACK — OpenAI anunció adquisición y la herramienta OSS sigue orientada a eval/red-team; también aparece en I04 para evaluación. https://github.com/promptfoo/promptfoo
6. `Anthropic effective context engineering` — REFERENCE_ONLY_ARCH — contexto mínimo de alta señal, retrieval just-in-time, compaction, notas/memoria y subagentes con resúmenes compactos. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
7. `Anthropic multi-agent research` — REFERENCE_ONLY_ARCH — lead researcher + subagents paralelos + síntesis/citation; útil para I04–I10, pero writes compartidos deben permanecer secuenciales. https://www.anthropic.com/engineering/multi-agent-research-system
8. `Anthropic advanced tool use` — REFERENCE_ONLY_ARCH — tool search/dynamic discovery y programmatic tool calling reducen contexto cargado y permiten miles de tools sin preinyectar schemas. https://www.anthropic.com/engineering/advanced-tool-use
9. `Anthropic Managed Agents` — REFERENCE_ONLY_ARCH — desacoplar brain/harness de hands/compute y usar interfaces estables; refuerza ports/adapters de Sharck. https://www.anthropic.com/engineering/managed-agents
10. `Anthropic tool/eval guidance` — REFERENCE_ONLY_ARCH — herramientas token-efficient, prototipos + evals y claridad de outputs; combinar con `Demystifying evals for AI agents`. https://www.anthropic.com/engineering/writing-tools-for-agents ; https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
11. `Anthropic simple/composable agents` — REFERENCE_ONLY_ARCH — empezar por patrones simples y elevar complejidad sólo cuando demuestra mejora; evita meter framework por framework sin necesidad. https://www.anthropic.com/engineering/building-effective-agents

## Shortlist provisional para aprobación del Director
Prioridad alta por aporte neto y baja duplicación conceptual: `Inspect AI`, `Promptfoo`, `BrowserGym`, `AgentLab`, `MCPMark`, `TEI`, `LibCST`, `Difftastic`, `tree-sitter-graph`, `Joern`, `ts-morph`, `Hermes Agent`, `OpenClaw`, `Agent Skills spec`, `OpenHands Software Agent SDK`, `Cline`, `mini-SWE-agent`, `Newspaper4k`, `selectolax`, `curl_cffi` (policy gate), `Browserless` (license gate), `OpenAI Agents SDK`.

No descargar todavía. Tras aprobación: deduplicar contra 117+20X, revisar licencia/ref/commit/special files/tamaño/destino, actualizar arquitectura versionada, adquirir sólo KEEP, read-back full tree y después integrar nodos/ports al DSL/DAG MultiSOL.
