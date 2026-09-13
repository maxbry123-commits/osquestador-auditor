# M63 — TAREA 2 — INVESTIGACIÓN 100X / ARQUITECTURA PARALELA SHARCK INPUT

Fecha: 2026-09-13
Estado: `RESEARCH_COMPLETE / ARCHITECTURE_DELTA_READY / 100X_TARGET_NOT_ASSUMED / ROOT_ONLY`
Raíz única: `➡️📂 sharck imput/`

## Regla de medición 100x

`100x` es objetivo de optimización, NO un resultado declarado por diseño. Para aceptar `100X_PASS` debe existir baseline y candidato ejecutados sobre el mismo fixture/host/versiones y demostrar >=100x en la métrica explícita sin degradación material de cobertura, evidencia, exactitud, seguridad o gates.

Métricas mínimas: `E2E p50/p95`, `TTFT`, `evidence/sec`, `useful-context/sec`, `context tokens delivered`, `duplicate-search %`, `coverage %`, `citation precision/recall`, `contradiction detection`, `tool success %`, `user actions/friction`, `API/token/compute cost`.

## Evidencia externa investigada

### Oficial
- OpenAI — Agents API, 2026-09-10: https://openai.com/index/introducing-the-agents-api/ — sesiones largas, context management, herramientas y subagents paralelos dentro de un harness administrado.
- OpenAI Developer Community — Agents API announcement: https://community.openai.com/t/introducing-the-agents-api-and-hosted-sandboxes/1396481 — agent loop, orchestration, long-running sessions y context management.
- Anthropic — Multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system — 3–5 subagents paralelos + 3+ tools por subagent; hasta 90% reducción de tiempo en queries complejas; mejor en breadth-first; guardrails/evals obligatorios.
- Anthropic — Effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — subagents con contextos aislados, compaction, notes y retorno condensado al lead agent.
- MiniMax — Agent Team 2026-05-27: https://www.minimax.io/blog/minimax-agent-team-long-running-1779893953 — múltiples agents en paralelo y roles/equipos para tareas largas.
- Kimi — Agent Swarm: https://www.kimi.com/en/help/agent/agent-swarm — hasta 300 subagents y 4,000+ tool calls; hasta 4.5x frente a ejecución secuencial en búsqueda masiva.
- Kimi Code — AgentSwarm: https://www.kimi.com/code/docs/en/kimi-code-cli/reference/tools.html — subagents aislados, timeout, resume, concurrency cap configurable.
- Kimi Code — What's New: https://www.kimi.com/code/docs/en/kimi-code/whats-new.html — swarm, progress, rate-limit-aware retries y micro-compaction.
- MCP Registry: https://modelcontextprotocol.io/registry/about — metadata estándar server.json, REST discovery, namespace verification, instalación/configuración.
- MCP Registry API v1.0.0: https://registry.modelcontextprotocol.io/docs — endpoints servers/publish/auth/health/ping/version/validate y schemas.

### Hugging Face / datasets útiles para validación
- Agent usage: https://huggingface.co/datasets/huggingface/agent-usage — señales reales de uso de agentes sobre Hub; útil para freshness/adoption, no como benchmark de calidad.
- ATBench: https://huggingface.co/datasets/AI45Research/ATBench — 1,000 trayectorias long-horizon/tool-use con auditoría humana para seguridad/evaluación.
- SynthTools Tasks: https://huggingface.co/datasets/SynthTools/SynthTools-Tasks — ground-truth tool calls + initial/final state; permite evaluar end-state, no sólo texto.
- Verified Tool-Use: https://huggingface.co/datasets/protogonos/verified-tool-use-dataset — trayectorias con schema validation; pequeño, usar sólo como slice auxiliar.

### Comunidad de desarrolladores / contra-evidencia
- Reddit LocalLLaMA, 2026-09-08: https://www.reddit.com/r/LocalLLaMA/comments/1wb35xo/how_many_agents_can_24090_actually_run_at_once/ — la concurrencia útil depende de contexto/hardware; más agents no implica más throughput.
- Reddit LocalLLaMA, 2026-08-11: https://www.reddit.com/r/LocalLLaMA/comments/1vl3frs/llamacpp_parallel_agents_fine_for_decode_but_one/ — prefill largo puede bloquear peers; exige scheduler/backpressure.
- Reddit ClaudeAI, 2026-06-16: https://www.reddit.com/r/ClaudeAI/comments/1u71d27/subagents_in_claude_code_arent_a_speed_trick/ — valor fuerte de subagents como aislamiento de contexto, no sólo velocidad.
- Reddit ClaudeAI, 2026-09-02: https://www.reddit.com/r/ClaudeAI/comments/1w52pbu/gone_in_60_seconds/ — contra-evidencia: swarm sin budget puede consumir cuotas de forma explosiva.
- GitHub community reference: https://github.com/madebyaris/agent-orchestration — shared memory, task queue, heartbeats, resource locks, research-first y handoff/recovery; referencia de patrones, NO componente seleccionado en Tarea 2.

## Delta por proceso/capacidad — mejora de valor real

### A/B/C — INPUT literal, ambigüedad y descomposición
Mejora: `INPUT_RAW immutable + SHA256` → descomposición lexical/entity/goal/constraint en paralelo → ambiguity score → sólo preguntas que cambian una decisión. Evita que una pregunta bloquee búsquedas independientes. Mantener hipótesis explícitas cuando el usuario no responde.
Microflujo horizontal: `INPUT_RAW → LOCK → {lexical | entities | goals | constraints | ambiguity} → InputSpec → FAN-OUT`.

### Paso 1 — investigación/búsqueda avanzada
Mejora: dynamic fan-out. No arrancar 100 workers por defecto: 3–5 para breadth complejo, escalar 10→100+ sólo cuando el query lattice tenga suficientes ramas independientes y el governor lo permita. Coverage stop + marginal-gain stop + dedup en vuelo.
Microflujo: `InputSpec → query lattice → independence score → N workers → evidence ledger → coverage/stop → context delta`.
Evidencia: Anthropic demuestra 3–5 subagents + herramientas paralelas y hasta 90% menos tiempo en investigación compleja; Kimi prueba que escala masiva puede ayudar en búsqueda masiva, pero no justifica 100 agents para tareas simples.

### Paso 2 — Skills
Mejora: progressive disclosure: catalog metadata → mínimo 3 bibliotecas → leer 20 SKILL.md completos en sandbox/cache → SHA/pin/license → rank por objetivo → 3 activos + 5 standby; sólo selected skill body/context entra al agente.
Microflujo: `intent → 3+ skill libs → 20 full reads → pin/license/hash → rank → 3 active + 5 standby → pointers`.
Valor: reduce ruido/context tokens y conserva aprendizaje verificable.

### Paso 3 — Datasets
Mejora: dataset scout paralelo en >=3 catálogos → dataset card/license/freshness/schema/size → sample-first → eval de utilidad → 3 activos +5 standby; dataset nunca se vuelca completo al prompt, se entrega por pointer/retrieval.
Microflujo: `goal → catalog fan-out → cards/licenses → sample → utility/eval → 3 active +5 standby → evidence pointer`.
Benchmarks: usar ATBench/SynthTools/verified-tool-use cuando el caso sea agent/tool-use; nunca asumir que sirven para todos los dominios.

### Paso 4 — Adaptadores/acopladores
Mejora: capability contract first; descubrir adapters por `input/output schema + transport + auth + version + permissions + license`; 3 activos +5 standby; read-only compatibility probe antes de permitir mutación.
Microflujo: `capability gap → adapter catalogs → contract score → auth/version check → readonly probe → active/standby`.

### Paso 5 — Tools/plugins / enchufe universal
Mejora: MCP/API-first. `capability → official registry/local registry → server/tool schema → auth/permission → version pin → readonly smoke → usage recipe para agente`. Cachear schemas con TTL y invalidar al cambiar versión.
Microflujo: `need → MCP/API discovery → metadata/schema → auth gate → readonly smoke → tool pointer + instructions`.
Evidencia: Official MCP Registry ya expone metadata estándar, REST discovery y validación/versionado.

### Paso 6 — persistencia/contexto continuo
Mejora: event-sourced ledger + checkpoints + idempotency key + heartbeat + stale recovery. Los 12 goals entrada/salida, Council12, 3 refutaciones, debate y 4 simulaciones corren como celdas paralelas, no como bloqueo serial; fan-in produce `ContextDelta` versionado.
Microflujo: `{goals12 | council12 | refute3 | debate | sim4 | fresh research} → ledger → delta scorer → CONTEXT_PATCH`.

### Paso 7 — Evidence Sheriff / Sentinel / Juez
Mejora: cada claim se representa `claim_id → official evidence → independent evidence → contra-evidence → version/freshness → verdict`. Generar 10 rutas alternativas y rankearlas exactamente por `0 fricción → menor tiempo → menor sobreingeniería → evidencia`.
Microflujo: `candidate route → claim graph → official+community+negative evidence → 10 alternatives → rank → PASS/GAP/REFUTE`.

### Paso 8A — Lupa de errores
Mejora: lane adversarial independiente que busca issues, regressions, breaking changes, version drift, comentarios negativos y failure reports antes de ejecución; findings nunca se mezclan silenciosamente con evidencia positiva.
Microflujo: `route/version → issues/forums/social/releases → negative evidence → failure taxonomy → risk score → sheriff`.

### Paso 8B — Soluciones/guías
Mejora: official manual first + implementación comunitaria + troubleshooting + known failures → runbook mínimo ejecutable. Stop cuando ruta y prerrequisitos tienen evidencia suficiente.
Microflujo: `objective → official manual → community implementation → pitfalls → exact runbook → validation checklist`.

### Paso 10 — Multi-SHARCK/refutador
Mejora: rutas rivales con contextos aislados; no comparten una única narrativa inicial. Fan-in sólo comparte claims/evidence/pointers. Selección por score reproducible; no por mayoría de LLMs.
Microflujo: `primary route ─┬→ challenger A ─┐ | ├→ challenger B ─┤→ evidence scorer → best route + unresolved dissent | └→ challenger C ─┘`.

### Paso 11 — Anti-alucinaciones / literal alignment
Mejora: gate determinista `literal requirement → evidence/context pointer → output obligation`. Si falta cualquier requisito material: `CONTEXT_GAP_LOOP`, nunca CONTEXT_READY. Separar evidencia, inferencia y simulación.
Microflujo: `INPUT checklist × ContextPackage → requirement coverage → contradiction/gap → BLOCK | RELEASE`.

### Paso 12 — Reporter SHARCK noticias
Mejora: activar sólo si FreshnessDetector detecta tiempo/evento. Búsqueda geográfica `local→estado/región→país→internacional` + social traces; construir source-thread graph y TTL según volatilidad. Watchdog condition-driven, no polling indiscriminado.
Microflujo: `freshness trigger → geo router → local/regional/national/international fan-out → social traces → thread graph → delta/watchdog`.

### Paso 13 — trabajo continuo / estudio académico
Mejora: ContextDelta Bus desacopla investigación de ejecución YAIWES. El agente táctico consume patches versionados en safe points sin reiniciar trabajo. Academic lane: papers→citations→datasets→method/benchmark linkage.
Microflujo: `running task || continuous research → verified delta queue → safe-point merge → updated memory/profile/handoff`.

### Paso 14 — Watchdog activo
Mejora: watcher por condición/TTL/freshness/dependency; heartbeat, stale detection, retry classification y circuit breaker. Frecuencia sólo tan alta como cambia la fuente; jamás spin-loop sin condición.
Microflujo: `watch condition → schedule/heartbeat → fetch delta → compare version → notify/patch only on change`.

### Paso 15 — CODA/bucle persistente
Mejora: persistent job state, budgets y cancellation. Lo persistente es el estado/cola/sesión, no CPU girando. Resume desde checkpoint/handoff; retry sólo transient; quota/auth/schema errors quedan GAP.
Microflujo: `job state → queue → worker → checkpoint → WAIT|RETRY|PATCH → resume → terminal verdict`.

### Motores de descarga/extracción
Mejora Tarea 2: NO crear un motor alternativo. Copiar byte-idéntico Motor 2 + engine dentro de raíz SHARCK y usar source pin/license/readback. Esto elimina dependencia runtime de la ruta externa sin tocar el motor canónico.
Microflujo: `queue inside root → copied Motor2 → copied engine → pinned source → extract/hash → root destination → readback/verdict`.
Blobs internos: Motor2 `84d566e2ee4e98e42eb3a864026d067d48caabd9`; engine `91e6e4486692eab314be5c7130d8310d3c855397`.

### Microkernels / 10–100+ microagentes
Mejora: separar `brain/session/hands`. Cada specialist recibe InputSpec/pointers/budget/output schema y contexto aislado. `DynamicFanoutGovernor` decide worker count por independencia, expected information gain, latency budget y cost budget. No recursive spawn por defecto. Locks sólo para recursos mutables; evidence ledger append-only.
Microflujo: `Director → governor → {kernel1...kernelN} → append-only ledger → deterministic fan-in → YAIWES handoff`.
Evidencia: OpenAI separa harness/entorno y permite subagents; Anthropic usa context isolation; Kimi expone concurrency cap/timeouts/resume; comunidad reporta quota explosion y prefill contention cuando el swarm carece de governor.

### Memoria / perfil / Handoff ejecutable
Mejora: raw evidence permanece externa al LLM; `memory.md + profile.json + HANDOFF.md + handoff-index.json + evidence-ledger.jsonl` contienen pointers/hashes/status. Compaction nunca destruye provenance.
Microflujo: `lane outputs → artifact store/ledger → profile+memory → pointer index → minimal ContextPackage`.

### Simulación de hipótesis
Mejora: cuando uncertainty/risk supera threshold, lanzar 3 hipótesis independientes y escenarios; etiquetar outputs `SIMULATION`, nunca `EVIDENCE`. Paso 6 conserva además las 4 simulaciones exigidas literalmente.
Microflujo: `uncertainty trigger → H1 | H2 | H3 → simulation → compare → hypothesis ranking → evidence request`.

## Governor transversal — evita sobreingeniería

Variables de decisión: `task_independence`, `uncovered_goals`, `source_diversity`, `marginal_information_gain`, `latency_budget`, `token_budget`, `API_budget`, `rate_limits`, `provider_health`, `context_pressure`.

Reglas:
- simple/local task → 1–3 workers;
- complex breadth research → 3–10 workers initially;
- massive independent enumeration → grow 10→100+ only while marginal gain > threshold;
- 100+ is capability ceiling/dynamic expansion, not minimum;
- cap concurrency independently of total worker count;
- dedup identical requests; shared in-flight futures;
- timeout/circuit-breaker/provider-health; fallback route is explicit;
- no recursive spawning unless policy explicitly allows it;
- stop on coverage + evidence sufficiency, not fixed number of searches.

## Arquitectura transversal resultante

`INPUT_LOCK → InputSpec → DIRECTOR/GOVERNOR → {RESEARCH || SKILLS || DATASETS || ADAPTERS || TOOLS || PERSISTENCE || SHERIFF || ERROR_LENS || GUIDES || MULTI_SHARCK || NEWS? || ACADEMIC? || WATCHDOGS || SIMULATION?} → append-only EVIDENCE LEDGER + CONTEXT DELTA BUS → LITERAL ALIGNMENT/FAN-IN → minimal CONTEXT_PACKAGE → YAIWES`

Procesos reactivables: research, datasets, adapters, sheriff, error lens, guides, Multi-SHARCK.
Procesos continuos: persistence/context delta, continuous work, memory/handoff, condition watchdogs.
Procesos event-driven: news, academic, tools/plugins, simulations.

## GAPs explícitos para fases siguientes
1. Tarea 2 diseña/valida arquitectura; NO equivale a implementar todos los lanes.
2. B08 y B09 no aparecen físicamente en el último listado de `componentes open source`; no afirmar adquisición cerrada.
3. Los workflows SHARCK fueron reubicados dentro de raíz y ya no son GitHub Actions automáticos; preservar como plantillas históricas hasta que un runtime root-only reemplace su disparo.
4. Los copied motors son byte-idénticos, pero las plantillas antiguas todavía contienen referencias históricas a la ruta externa; son `NON_AUTHORITATIVE_TEMPLATE`.
5. 100x necesita benchmark físico; evidencia externa muestra mejoras importantes pero no 100x universal.
6. Tarea 3 (componentes nuevos) y Tarea 4 (nodos descargables) no se abren en Tarea 2.
