# 🦈 SHARCK INPUT — TAREA 2 M64 — ARQUITECTURA CORREGIDA / PARALELO TOTAL

Fecha: 2026-09-13
Estado: `TASK2_CORRECTED / ADDITIVE_ONLY / ALL_DIRECTOR_PROCESSES_PARALLEL / PRIOR_ARCHITECTURE_PRESERVED`
Raíz única: `maxbry123-commits/osquestador-auditor@main → ➡️📂 sharck imput/`

## 0. REGLA DE AUTORIDAD

Este archivo **NO reemplaza, NO recorta y NO reescribe** `📁 readme arquitectura sharck imput V2.1.md` ni las secciones 1–11 existentes. La arquitectura previa permanece completa y vigente.

Esta Tarea 2 sólo **ADICIONA mejoras** sobre esa arquitectura.

Reglas del Director para M64:
- todos los procesos/pasos del Director se mantienen disponibles y trabajan en paralelo según fueron definidos;
- no convertirlos en una secuencia monolítica;
- no introducir `dynamic fan-out`, `governor` de reducción de workers, reducción automática de paralelismo ni reglas de “bajar throughput”;
- no eliminar arquitectura previa, microkernels, componentes, pasos, procesos, motores, watchdogs, memoria, handoff, simulaciones o investigación ya definida;
- una mejora sólo se incorpora si suma capacidad, evidencia, aislamiento, velocidad, memoria, trazabilidad, verificación, robustez o calidad sin sustituir lo existente;
- los procesos condicionales definidos literalmente por el Director (por ejemplo noticias “si detecta que necesitas noticias”) conservan exactamente esa condición; una vez activados trabajan en paralelo con los demás y no detienen a los demás;
- `M63` queda como evidencia histórica del error; **sus reglas de paralelismo dinámico/reducción NO son operativas**. M64 es la corrección vigente de Tarea 2.

## 1. ARQUITECTURA PREVIA PRESERVADA 1:1 COMO BASE

Pipeline maestro previo que sigue vigente:

`INPUT_RAW → INPUT_LOCK → INTENT/CONSTRAINTS → ENTITY_RESOLUTION → RESEARCH_DECISION → FOCUS_A → QUESTIONS_0_12 || PRESEARCH → DOMAIN/ROLE/GEO/LANGUAGE ROUTER → RESEARCH_DAG → FAN_OUT SOURCES → CAPTURE/SNAPSHOT → EXTRACT/NORMALIZE → INDEX → BM25/SPARSE/DENSE → RRF/RERANK → EVIDENCE GRAPH → CONTRADICTION/COVERAGE/GAP → FOCUS_B → CODE/SKILL/TOOL POINTERS → CONTEXT_COMPRESSION → CONTEXT_PACKAGE → MAIN_LLM`

Loop previo preservado:

`MAIN_LLM → STRUCTURED_RESEARCH_REQUEST → RESEARCH_DAG → EVIDENCE_DELTA → CONTEXT_PATCH → MAIN_LLM`

Microkernels previos preservados:

`input_lock || focus || questions || role_router || geo_language || query_lattice || community || github || huggingface || labs || youtube || capture || extract || index || dedup || code_pointer || skill_pointer || tool_finder || evidence || gap_loop || context_compiler || checkpoint || verdict`

Capas/adapters previos preservados:

`capture.warc || provenance.lineage || observability.otel || policy.engine || supply_chain.sbom || supply_chain.vuln || supply_chain.secrets || structured_output || evidence.compute || evidence.rules || llm_policy_eval`

Nada de lo anterior se elimina ni se sustituye.

## 2. ARQUITECTURA COMPLETA INTEGRADA — TODO EN PARALELO

```text
INPUT_RAW → INPUT_LOCK → DESCOMPOSICIÓN LITERAL A/B/C → INPUT SPEC / OBJETIVOS / REQUERIMIENTOS
                                      ↓
┌───────────────────────────────────── SHARCK INPUT DIRECTOR ─────────────────────────────────────┐
│                                                                                                 │
│  ARQUITECTURA PREVIA ACTIVA                                                                     │
│  INTENT/CONSTRAINTS || ENTITY_RESOLUTION || RESEARCH_DECISION || FOCUS_A || QUESTIONS_0_12     │
│  PRESEARCH || DOMAIN/ROLE/GEO/LANGUAGE || RESEARCH_DAG || FAN_OUT SOURCES || CAPTURE/SNAPSHOT   │
│  EXTRACT/NORMALIZE || INDEX || BM25/SPARSE/DENSE || RRF/RERANK || EVIDENCE GRAPH               │
│  CONTRADICTION/COVERAGE/GAP || FOCUS_B || CODE/SKILL/TOOL POINTERS || CONTEXT_COMPRESSION       │
│                                                                                                 │
│  PROCESOS DEL DIRECTOR ACTIVOS EN PARALELO                                                      │
│  PASO 1 INVESTIGACIÓN || PASO 2 SKILLS || PASO 3 DATASETS || PASO 4 ADAPTADORES                │
│  PASO 5 TOOLS/PLUGINS || PASO 6 CODA/PERSISTENCIA || PASO 7 SHERIFF/VALIDADOR                   │
│  PASO 8 LUPA ERRORES || PASO 8 SOLUCIONES/GUÍAS || PASO 10 MULTI-SHARCK                         │
│  PASO 11 ANTI-ALUCINACIONES || PASO 12 REPORTERO NOTICIAS* || PASO 13 TRABAJO CONTINUO*         │
│  PASO 14 WATCHDOGS* || PASO 15 CODA BUCLE PERSISTENTE                                           │
│                                                                                                 │
│  SISTEMAS TRANSVERSALES EN PARALELO                                                             │
│  10/100 BÚSQUEDAS || MINI ROUTER LOCAL || ROUTER WEB/API || MICROKERNELS DEDICADOS              │
│  MOTORES DESCARGA/EXTRACCIÓN || ARNÉS UNIVERSAL || MEMORIA || PERFIL || HANDOFF PYTHON          │
│  12 GOALS INPUT || 12 GOALS OUTPUT || ASK CONSIL 12 || 3 REFUTACIONES || DEBATE || SIMULACIONES│
│  EVIDENCIA OFICIAL || COMUNIDAD || FOROS || GUÍAS || BLOGS || REDES || YOUTUBE || GITHUB/HF     │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                      ↓
                     EVIDENCE LEDGER + MEMORIA + PERFIL + HANDOFF
                                      ↓
                PASO 11 CHECKLIST LITERAL / VERIFICACIÓN / SENTINELA
                                      ↓
                         CONTEXT_PACKAGE COMPLETO Y TRAZABLE
                                      ↓
                               MAIN LLM / AGENTE YAIWES
```

`*` Los procesos que el INPUT literal condiciona a una necesidad/evento conservan su condición exacta. No se serializan respecto de los demás.

## 3. MEJORAS 100X — SÓLO ADICIONES, SIN CAMBIAR LOS PASOS

### A/B/C — INPUT, DESCOMPOSICIÓN Y DEFINICIÓN
Mejoras adicionales: SHA del input literal; matriz `objetivo→restricción→detalle→evidencia`; análisis gramatical, entidades, sinónimos/diccionario y ambigüedad en microkernels paralelos; snapshot inmutable antes de cada reactivación; preguntas al usuario sólo como canal adicional, sin detener investigación independiente ya posible.

Microflujo horizontal:
`INPUT_RAW → LOCK/HASH → {gramática || entidades || objetivos || restricciones || adjetivos || sinónimos || diccionario || web básica} → INPUT SPEC → TODOS LOS PASOS EN PARALELO`

### PASO 1 📌 — INVESTIGACIÓN Y BÚSQUEDA AVANZADA
Se preserva la ejecución paralela. Mejora: cada rama usa microkernel propio, fuentes oficiales + comunidad + repos + papers + foros + redes; 10 o 100 búsquedas pueden ejecutarse simultáneamente; resultados se guardan como artefactos con URL, fecha, hash, versión y claim relacionado; búsquedas nuevas pueden añadirse sin apagar las ya activas.

Microflujo:
`OBJETIVO → {WEB || GOOGLE || WIKIPEDIA || GITHUB || HF || DOCS || FOROS || BLOGS || REDES || YOUTUBE || PAPERS} × 10/100 → EVIDENCIA → LEDGER`

### PASO 2 📌 — SKILLS
Se conserva: mínimo 3 bibliotecas, leer mínimo 20 skills completos, seleccionar mínimo 3 para usar/descargar. Mejora: las 3+ bibliotecas se investigan a la vez; los 20+ skills se leen/valoran en paralelo; cada skill conserva source/ref/hash/licencia/compatibilidad y receta de uso; mantener candidatos adicionales como respaldo sin sustituir los 3 elegidos.

Microflujo:
`OBJETIVO → {LIB SKILLS A || LIB B || LIB C || MÁS} → 20+ FULL READS EN PARALELO → EVIDENCIA/COMPATIBILIDAD → 3+ SELECCIONADOS + RESPALDOS`

### PASO 3 📌 — DATASETS
Se conserva: mínimo 3 datasets por caso y 5 opciones listas. Mejora: búsqueda en múltiples catálogos a la vez; validar card/licencia/schema/freshness/tamaño/calidad; muestreo y comparación paralelos; entregar pointers y muestras trazables a la LLM antes y durante razonamiento; mantener búsqueda activa mientras el trabajo continúa.

Microflujo:
`CASO → {CATÁLOGO 1 || CATÁLOGO 2 || CATÁLOGO 3 || MÁS} → DATASET CARD/LICENCIA/SCHEMA → 3 ACTIVOS + 5 LISTOS → CONTEXTO`

### PASO 4 📌 — ADAPTADORES / ACOPLADORES
Se conserva el mismo proceso que Dataset. Mejora: evaluar simultáneamente schema entrada/salida, protocolo, autenticación, permisos, versión, licencia y compatibilidad; hacer pruebas de lectura/compatibilidad sin retirar otras opciones; 3+ candidatos útiles y 5 listos cuando aplique.

Microflujo:
`NECESIDAD → {ADAPTER A || B || C || MÁS} → SCHEMA/AUTH/VERSION/COMPAT → PRUEBAS → ACTIVOS + RESPALDOS`

### PASO 5 📌 — TOOLS / PLUGINS / ENCHUFE UNIVERSAL
Se conserva detección→investigación→aprendizaje→conexión→instrucciones. Mejora: búsqueda simultánea en MCP/API/plugins/SDK/docs/repos; registrar schema, auth, permisos, versión, ejemplos y fallos conocidos; entregar al agente “qué está disponible + cómo usarlo + evidencia”.

Microflujo:
`NECESIDAD → {MCP || API || PLUGIN || SDK || DOCS || REPO} → SCHEMA/AUTH/EJEMPLOS → PRUEBA → TOOL POINTER + RECETA`

### PASO 6 📌 — CODA / SUPER PERSISTENCIA
Se conserva el loop mientras corren tareas. Mejora: ejecutar simultáneamente `12 goals entrada || 12 goals salida || Ask Consil 12 || 3 refutaciones || debate || 4 simulaciones || investigación continua`; cada salida crea ContextDelta versionado; checkpoints independientes impiden que el fallo de un carril pare los otros.

Microflujo:
`TRABAJO EN CURSO → {GOALS12-IN || GOALS12-OUT || CONSIL12 || REFUTA3 || DEBATE || SIM4 || RESEARCH} → CONTEXT DELTAS → MEMORIA/HANDOFF`

### PASO 7 📌 — VALIDADOR / SHERIFF / SENTINELA / JUEZ
Se conserva búsqueda de evidencia y 10 alternativas. Mejora: claim graph trazable; evidencia oficial + comunidad + contraevidencia en paralelo; cada alternativa clasificada exactamente por `1) 0 fricción 2) menor tiempo 3) evitar sobreingeniería 4) evidencia`; vuelve a activar investigación y persistencia sin parar los otros procesos.

Microflujo:
`CADA CLAIM/RUTA → {OFICIAL || COMUNIDAD || FORO || GUÍA || BLOG || REDES || YOUTUBE || CONTRAEVIDENCIA} → 10 ALTERNATIVAS → RANK → VEREDICTO`

### PASO 8 📌 — LUPA DE ERRORES
Se conserva búsqueda anticipada de errores/comentarios negativos. Mejora: issues, releases, breaking changes, changelogs, CVEs, discusiones, fallos reales y experiencias de usuarios se buscan simultáneamente; cada riesgo queda ligado al paso/ruta que puede afectar.

Microflujo:
`RUTA/COMPONENTE → {ISSUES || RELEASES || CHANGELOGS || CVE || FOROS || REDES || NEGATIVOS} → MAPA DE RIESGOS → PASO 7`

### PASO 8 📌 — SISTEMA DE SOLUCIONES / GUÍAS
Se conserva búsqueda de manuales oficiales + comunidad. Mejora: múltiples guías se recuperan al mismo tiempo; se comparan requisitos, versiones, comandos, fallos y alternativas; se genera runbook exacto con fuentes y checklist verificable.

Microflujo:
`OBJETIVO → {MANUAL OFICIAL || GUÍAS || FOROS || BLOGS || VIDEOS || REPOS} → COMPARACIÓN → RUNBOOK + CHECKLIST`

### PASO 10 📌 — MULTI SHARCK
Se conserva comparación/debate/refutación y rutas alternativas. Mejora: varias copias SHARCK trabajan en paralelo con contextos separados para evitar contaminación; cada una produce evidencia, refutación y propuesta; el resultado conserva disenso y fuentes, no borra rutas minoritarias.

Microflujo:
`CONTEXTO PRIMARIO → {SHARCK A || SHARCK B || SHARCK C || MÁS} → GOALS/CONSIL/REFUTACIONES/DEBATE → OPCIONES + EVIDENCIA`

### PASO 11 📌 — ANTI-ALUCINACIONES / INPUT LITERAL
Se conserva función exclusiva de filtrar alineación. Mejora: checklist determinista `requisito literal → contexto/evidencia → obligación de salida`; separar explícitamente `EVIDENCIA`, `INFERENCIA`, `SIMULACIÓN`, `PENDIENTE`; no autorizar contexto final si falta un requisito material del input.

Microflujo:
`INPUT LITERAL → CHECKLIST PUNTO×PUNTO → {EVIDENCIA || CONTEXTO || OBLIGACIÓN} → GAP? → REACTIVAR BÚSQUEDAS || CONTEXT READY`

### MOTOR DE DESCARGA Y EXTRACCIÓN / TRAZABILIDAD
Se conserva y se replica/copia dentro de la raíz autorizada. Mejora: cada proceso que descargue conserva source/ref/commit/hash/licencia/destino/readback; múltiples motores independientes pueden trabajar en paralelo en destinos distintos; ningún motor puede escribir fuera de `➡️📂 sharck imput/`.

Microflujo:
`PROCESO → MOTOR PROPIO/COPIA AUTORIZADA → SOURCE PIN → DOWNLOAD → EXTRACT → HASH → DESTINO SHARCK → READBACK`

### ARNÉS UNIVERSAL
Se conserva. Mejora: contrato común para microkernel/agente: `input literal pointer + objetivo + herramientas + fuentes + memoria + output schema + evidence refs + handoff`; aislamiento por agente para evitar mezcla de contexto; resultados persistidos directamente como artefactos/pointers.

Microflujo:
`DIRECTOR → ARNÉS → {AGENTE/MICROKERNEL 1 || 2 || ... || 100+} → ARTEFACTOS/EVIDENCIA → HANDOFF`

### SISTEMA PARALELO 10/100
Se conserva literalmente como capacidad simultánea. Mejora: microkernel, workflow, API y motor separados por proceso para que un proceso ocupado no bloquee a otro; router local y web en paralelo; múltiples API keys/providers según disponibilidad definida por el proyecto; resultados convergen por ledger/handoff sin detener los workers.

Microflujo:
`INPUT → {ROUTER LOCAL || ROUTER WEB/API} → {WORKER1 || ... || WORKER10 || ... || WORKER100+} → EVIDENCIA/PERFIL/HANDOFF`

### MEMORIA + PERFIL + HANDOFF
Se conserva creación por trabajo. Mejora: `memory.md || profile.json || HANDOFF.md || source-index.json || evidence-ledger.jsonl || context-deltas/`; cada entrada con timestamp/source/hash/status; cualquier agente puede continuar sin reiniciar investigación ya hecha.

Microflujo:
`TODOS LOS PASOS → {MEMORIA || PERFIL || LEDGER || SOURCE INDEX} → HANDOFF → AGENTE/LLM`

### HANDOFF PYTHON EJECUTABLE
Se conserva. Mejora: resolver pointers a fuentes/artefactos, verificar hash/readback, reactivar fuentes ya conocidas y entregar delta nuevo sin rehacer búsqueda completa.

Microflujo:
`HANDOFF → RESOLVER POINTERS → VERIFY HASH/STATUS → RECUPERAR CONTEXTO → CONTINUAR`

### PASO 12 📌 — REPORTERO SHARCK 📰📢
Se conserva exactamente su activación cuando se necesita noticia/suceso. Mejora: microagentes simultáneos por zona y medio; `local || estado/región || país || internacional || redes`; thread graph de personas/lugares/fechas/fuentes; watchdog y handoff actualizan memoria/perfil sin apagar investigación restante.

Microflujo:
`TRIGGER NOTICIAS → {LOCAL || REGIONAL || NACIONAL || INTERNACIONAL || REDES} → HILOS/PISTAS → CLASIFICAR → MEMORIA/HANDOFF/WATCHDOG`

### PASO 13 📌 — TRABAJO CONTINUO / ESTUDIO ACADÉMICO
Se conserva. Mejora: investigación paralela nunca interrumpe ejecución; contexto nuevo entra por cola versionada; carril académico puede buscar papers, citas, datasets, métodos y refutaciones simultáneamente.

Microflujo:
`TAREA EN CURSO || INVESTIGACIÓN CONTINUA || ACADÉMICO → CONTEXT DELTAS → COLA → AGENTE YAIWES`

### PASO 14 📌 — WATCHDOG ACTIVO
Se conserva por paso o global y desde el intervalo solicitado por usuario/agente. Mejora: watchdog independiente por proceso; estado, heartbeat, source/version change, GAPs y handoff; ningún watchdog reemplaza o apaga los otros.

Microflujo:
`PASO/OBJETIVO → WATCHDOG PROPIO → REVISAR FUENTES/ESTADO → DELTA/GAP → MEMORIA/HANDOFF`

### PASO 15 📌 — CODA / BUCLE DE PERSISTENCIA
Se conserva encendido según trabajo continuo solicitado. Mejora: cola persistente por proceso + checkpoint + recovery + handoff; los procesos pueden permanecer activos simultáneamente durante toda la tarea y recibir contexto nuevo.

Microflujo:
`PROCESOS ACTIVOS → COLAS PERSISTENTES → WORKERS PARALELOS → CHECKPOINTS → NUEVO CONTEXTO → CONTINUAR`

### MOTORES DETERMINISTAS AUTOMÁTICOS
Se conserva la orden. Mejora: un contrato uniforme por motor (`input/schema/source/output/evidence/verdict`), logs y readback; motores no sustituyen microkernels y microkernels no sustituyen motores.

### MICROKERNELS EN PARALELO
Se conserva la orden. Mejora: contexto y memoria aislados por microkernel, artefactos directos, nombres/IDs persistentes, error aislado, handoff común.

### SIMULACIÓN DE 3 HIPÓTESIS
Se conserva para cada paso necesario. Mejora: `H1 || H2 || H3` simultáneas, resultado etiquetado `SIMULACIÓN`; se compara con evidencia real antes de incorporarlo al contexto. El Paso 6 conserva además sus 4 simulaciones literales.

## 4. MEJORAS VALIDADAS POR INVESTIGACIÓN — SIN MODIFICAR LA ARQUITECTURA DEL DIRECTOR

1. **OpenAI Agents API (2026-09-10):** el harness gestiona sesiones largas, herramientas y permite paralelizar trabajo con subagentes. Aporta respaldo para más paralelismo, no para reducirlo.
2. **Anthropic multi-agent research:** subagentes y tools simultáneos redujeron hasta 90% el tiempo de investigación en consultas complejas; también recomienda contextos separados y resultados persistidos en artefactos. Aporta `parallel tool use + isolated context + artifact pointers`.
3. **MiniMax Agent Team:** múltiples Agents en paralelo con roles/equipos para trabajos largos. Aporta evidencia para microagentes paralelos persistentes.
4. **Kimi Agent Swarm:** documenta hasta 300 subagentes simultáneos y 4.000+ tool calls, con mejoras hasta 4.5× frente a ejecución secuencial en búsqueda masiva. Aporta evidencia directa para el modelo 10/100+ simultáneo indicado por el Director.
5. **MCP Registry:** discovery/schema/versionado de herramientas aporta trazabilidad al Paso 5 sin sustituir API/plugins existentes.

Estas mejoras se incorporan **además** de lo que ya existe; no autorizan eliminar pasos, bajar paralelismo, reducir workers, convertir el sistema en secuencial ni reemplazar componentes anteriores.

## 5. GATES DE TAREA 2 CORREGIDOS

- `PRIOR_ARCHITECTURE_PRESERVED=true`
- `DIRECTOR_INPUT_LITERAL_PRESERVED=true`
- `ALL_DIRECTOR_PARALLEL_PROCESSES_PRESERVED=true`
- `DYNAMIC_FANOUT_RULE=REJECTED`
- `WORKER_REDUCTION_RULE=REJECTED`
- `THROUGHPUT_REDUCTION_ARGUMENT=REJECTED`
- `ADDITIVE_IMPROVEMENTS_ONLY=true`
- `ROOT_ONLY=true`
- `M63_DYNAMIC_PARALLELISM=SUPERSEDED_BY_M64`
- `TASK3_NOT_OPENED=true`
- `TASK4_NOT_OPENED=true`
- `TASK5_NOT_OPENED=true`

## 6. VEREDICTO

`TAREA2_M64_CORREGIDA / ARQUITECTURA_PREVIA_INTACTA / NUEVAS_CAPACIDADES_ADITIVAS / TODAS_LAS_TAREAS_Y_PROCESOS_DEL_DIRECTOR_PARALELOS / SIN_DYNAMIC_FANOUT / SIN_REDUCCIÓN_DE_WORKERS / SIN_THROUGHPUT_DOWN / LISTA_PARA_READBACK`
