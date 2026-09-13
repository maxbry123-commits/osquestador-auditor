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

---

# 11. INPUT BLOCK DEL DIRECTOR — PRESERVACIÓN LITERAL 1 A 1 — 2026-09-13

Los bloques siguientes son instrucciones del Director incorporadas **literalmente**. No sustituyen ni borran las secciones 1–10 anteriores. No corregir, resumir, reordenar, renumerar ni reinterpretar su texto.

## INPUT BLOCK 11-A — PROPUESTA SHARCK

```text
Vamos a mejora el sistema imput sharck conl los los siguientes sistemas.   
  
El sistema tiene que activar siempre pasos y todos al mismo tiempo   
  
Papa 1 📌   
Investigación y búsqueda avanzadabdd contextol que ya venimos haciendo   
  
Paso 2 📌   
Busqueda de aprendizaje en paralelos que busca   
Skills mínimo lee 20 distintos y selecciona 3 para usar para descargar usa mínimo 3 bibliotecas de skills Huggueface y otras 2 más   
  
Paso 3 📌   
Dataset busca Información dataset disponible de cada caso mínimo 3 dataset y se lo presenta a la llm como cala externa antes de procesar la información y durante el procesos del imput durante el razonamiento el sistema de búsqueda de dataset y información continua entendído hasta corroborar que la llm tiene la información necesaria pero mantiene activo 5 opciones lista para añadir   
  
Paso 4 📌   
Adaptadores o acopladores capa externa también de la llm mismo procesos que paso 3   
  
Paso 5 📌.  
Tools plugins enchufe universal el sistema detecta que va necesitar conectarse detecta investiga analiza y aprende que necesita conectarse busca como se puede conectar descraga la información y aprende y se lo da al agente para que lo pueda usar le dice que tiene disponible y como usarlo   
  
Paso 6 📌 Sistema de coda de super persistencia  y bucle mientas corre las tareas y el trabajo el sistema continua aprendiendo y investiga ➡️ analiza 12 goals de entrada y salida y ask cónsil también 12 pasos y 3 refutaciónes y debate y 4 simulaciónes ➡️ analiza estudia y aprende compara la información ya aportada y inyecta nuevo IMPUT de información de contexto   
  
Paso 7 📌 validador sharck que hace busca evidencia valida si el contexto suministrado esta comprobado que funciona el método aplicado busca evidencia ejemplo se va hacer un sdk para poder instalar las claves para open ai no solo busca como se hace busca evidencia en la comunidad de desarrolladores de programación y comunidad de open ai para refutar el primer proceso de contexto suministrado y aporta 10 nuevas alternativas y clasifica 1 priorida evitar 0 fricción al usuario 2 menor tiempo posible de solucionarlo 3 evita la sobre ingenieria 4 refuta cada proceso cada paso reactivando el sharck imput para cada paso no solo deja que el objetivo de cómo resolver queda en contexto reactiva paso 6 y paso 1 que sería la búsqueda pero es este proceso ubica más información para ejecutar cada paso de la ejecución de tareas es como un sentinela sheriff validador verificación sentinela supervisor juez guardián que sigue refutando y hasta tener na evidencia necesaria para evitar errores en cualquier proceso y evitar 0 fricción para el usuario del agente doble paso 7 extra de paso 7 para conseguir evidencia de la comunidad forun guía blog redes sociales YouTube para poder corroborar la mejor vía de solucionarlo y anticipar errores y activa   
  
Paso 8 📌 sistema lupa 🔍🕵️ búsqueda  sharck errores que hace investiga posible errores se anticipa busca todos los comentarios negativos y todos los componentes de la comunidad en redes sociales relacionados con el tema del contexto para localizar posibles errores en el procesos buscar evidencia que determine que la vía que se va usar puede ser un error o si se necesita algo más para evitar el error   
  
Paso 10 📌 multi Shack activa una comparación un debate usando 12 goals de entrada y salida y ask cónsil en cada uno hace refutaciónes para conseguir una mejore opción busque investiga debate y analiza porque sería mejor otra opción y la propone en el sistema de preguntas de imput como el que usa Claude debatiendo con el usuario otras opciones y le da contexto al agente y a la llm que existe otras rutas otras vías para conseguir el objetivo del imput es un refutador se opone al contexto primario basado en evidencia busa   
 actualizaciones o versiones nuevas y anteriores de los resultados de búsqueda indaga y sigue refutando hasta conseguir evidencia   
  
Paso 11 📌 sistema anti alucinaciones imput block leer literal es un sheriff schema validador verificación sentinela supervisor juez guardián del imput su única función es filtrar si el el contexto final que va a recibir el agente o la llm realmente está enfocado y alineado con el IMPUT y no deja pasar el contexto sin hacer una lista de verificación de cada punto del imput valida que se cumple las instrucciones   
  
Porque te explico se supone que en pocos pasos el sistema imput sharck en general funciona así   
  
A imput recibido   ➡️ B el imput se descompone debe tener unas descomposición literal para crear el contexto de busqueda si no existe investiga con el sistema de preguntas para el usuario tipo Claude o genera lo que sería una lista de posibles requerimientos de lo que puede necesitar el usuario ejemplo si un usuario le dice en el imput ayúdame a preparar un postre el imput es ambigua no tiene detalles no tiene características necesarias para investigar requiere poder definir el enfoque de que tipo de postre quieres y hace una lista para conseguir el contexto de busqueda ➡️ C todo el imput ya definido de descompone en objetivos tareas características subtítulos desarrollo pasos instrucciones adjetivos subjetivos nombres alternativos del diccionario detalles descripciónes una descomposición literal de gramática y literatura una búsqueda de diccionario y web con Google buscador y Wikipedia toda esto le permite a un micro kernel entender que es el imput y poder hacer una lista enumera de lo que requiere para activar el imput sharck ➡️ D luego input sharck todo el proceso de pasos  ➡️ E procesos activos continuos de investigación ➡️ proceso de paso 11 📌 que valida la lista evitando alucinaciones o pérdida del enfoque y evitando en el momento en que el agente y llm razonan evitan ruido y información corrupta que requieran Múltiples imput muchos PROMT para poder resolver este proceso evita tiempo y ahorra token inecesarios. ➡️E la salida para la llm para el agente para poder razonar y analizar el contexto   
  
  
  
  
Paso 8 📌  
Sistema de soluciones busca investiga en paralelo guías manuales instrucciones y comentarios de la comunidad según la especialidad del tema en curso ejemplo si se necesita instalar open claw o configurar un vps este sistema se adelanta busca todo el manual oficial y compara con el evidencia para buscar y descargar una guía la guía le permite diseñar la ruta exacta para solucionar luego reactiva   
  
  
Motor extracción y descarga   
Trazable para ubicar donde almacena la información paso   
  
Usa arnés universal   
  
Sistema paralelo nunca es una sola búsqueda el sistema paralelo arranca 10 o 100 búsqueda para minimizar latencia de investigación el sistema de minimax permite que todos los 11 pasos además de lo que yo te di para hicieras en le proyecto ocurran al mismo tiempo sin pisarse el proceso debe tener un mini router que está conectado a un router local y uno en la web vía api  que le pide  tiene hasta 10 y 100 api key si es necesario para procesar en paralelo   
  
El sistema imput sharck debe generar un archivo de memoria y de perfil en cada trabajo este archivo de memoria y perfil tiene todo el contexto de la información de todos los pasos el resultado y se lo entrega con del imput al agente y llm y le entrega un handoff.md para trazabilidad de información adicional pero también tiene   
1. Copias de varios Micro kernel que activa los pasos en paralelo no 1 micro kernel un mini agente con api llm el sistema en paralelo no espera que el micro kernel y la api se desocupen tiene su propio micro kernel wordflow y api en paralelo   
2. Sistema de motor de descarga y extracción copiar y mover el mismo motor que usas para descragar componente lo activas para descragar en cada procesos en paralelo la información que necesita activa y crea el micro kernel su en cada procesos por separado su propio motor de búsqueda o varios si es mucha la información   
  
3. Sistema handoff phyton ejecutable el sistema triangulan  y hace la ubicación y trazabilidad de información no necesita reiniciar búsqueda puede activar en handoff y acceder a la información necesaria en la web donde ya hizo la búsqueda   
  
4. Paso 12 📌
Noticias activa si el sistema detecta que necesitas noticias de algún suceso el sistema de reportero sharck 📰📢 que hace busca hilos de información y trazabilidad de noticias luego busca en redes sociales no búsqueda general sectotiza la zona el Estado el país ubica todos los medios de comunicación de la zona luego va subiendo el rango local a país y medios internacionales usa lo mismo con redes sociales busca huellas rastros y pistas de información cualquier dato que le pueda servir para usar como hilo de búsqueda y contexto luego mantiene activo con wachdog la búsqueda según la prioridad del usuario 5 minutos en adelante repite el ciclo y clasifica la información genera el paso de  handoff activo para mantener las fuentes ubicada y va acrulizando el archivo de perfil de memoria y el handoff sharck según va encontrando nueva información cuando el IMPUT llega a la llm y al agente todo ya está el contexto completo de lo que necesita preparar solo analiza y calidifia para la salida 

Paso 13 📌 Sisteme de trabajo continuo si detecta que el usuario mantiene el trabajo continuo de trabajo activa el imput sharck de manera activa mientras ocurren tareas en curso y va suministrando en cola al agente nueva información y contexto sin interrumpir el procesos de trabajo como hace minimax está procesando pero mientras recibe información nueva en paralelo y usa para mejorar las tareas en curso así como 
Sistema de estudio académico y investigación para tareas o aprender


Paso 14 📌
Wachdog Activo puede activar en casa paso o en contexto global wachdog activos que permiten mantener desde 1 minuto después de la salida o el tiempo que del agente vea necesario o el usuario lo solicite todos los wachdog necesarios 

Paso 15 📌
Coda bucle de persistencia activo en un sistema que se pueda activar como el que usa minimax y Kimi k el sistema de imput sharck puede estar encendidos todos sus procesos y pasos sin apagar el usuario puede mantener el proceso activo no solo lo activa el imput y el agente también puede mantenerlo encendidos sin importar el tiempo de cómputo 

Vas a crear todos los motores determinetista que se ejecuten de manera automática sentir del imput block en paralelo 

Vas a crear todos los micro kernel necesarios para que se ejecuten en paralelo al mismo tiempo donde sea necesario 

Vas a crear para cada paso que sea necesario un sistema de simulación donde ocurren 3 hipótesis se hacen las simulaciones y ese resulta será parte del contexto permitiendo mejorar el resultado 

Tarea 1 📌 
Debes buscar todos los procesos y pasos que yo te he dado y luego vas actulizar el archivo 📂readme arquitectura IMPUT sharck.md

📂Actualizar el Craxy wall bitácora stated JSON 

Todo con mi información imput block leer literal 1 a 1 en los archivos 

Tares 2 📌 
Vas a investigar como puedes mejorar 100 veces más cada paso validando tu propuesta de mejores resultados sin caer en sobre ingeniería solo todo lo que aporte valor lo incluyes y actulizas de nuevo los archivos y arquitectura diseñando una nueva arquitectura editando quirúrgicamente los archivos sin reescribrir nada ni borrar información de nada 

Vas a diseñar un diagrama de pasos cada uno con micro diagrama de flujo wordflow en formato trasversal horizontal debajo de cada paso y me lo vas a mostrar en el chat 

Me das la información en el chat más los enlaces del proyecto de los archivos arquitectura handoff Craxy wall todo enlaces visibles 

Tarea 3 📌 
Vas a investigar todos los componentes necesarios que sirvan para poder crear el code que necesito y vas a crear varios motores de descarga y extracción y lo incorporas a su destino 

Tarea 4 📌 vas a incorporar toda la tarea de máximo 3 pasos  como nodos descargables dentro de Craxy wall como shema para luego mandar el ejambre de trabajo 

Tarea 5 📌 resolver componentes faltantes y los Gaps Pendientes 

Debes convertir todo en proyecto ejecutable 
Dieme si  entiendes todo alguna duda y si entiendes tus 5 tareas  
```

## INPUT BLOCK 11-B — ACLARACIÓN PARALELO / AGENCIA

```text
Los papsos son solo referenciales para que separes procesos en paralelo no paras una secuencia tu busca la arquitectura anterior y llevas mi nueva propuesta y íntegras como todo un conjunto lo importante es poder separar procesos en paralelo y procesos continuos y de persistencia para bajar la latencia no es una procesos monolítico de un solo wordflow no puede ser un proceso continuo de pasos so 10 o 100 procesos corriendo al mismo tiempo y algunos pasos de repiten usan el mismo validador o se activa persistencia 
Luego todo lo organizas como si fuera un equipo de el fbi y la CIA  con más de 100 micro agentes en paralelo y imput sharck es el director de la agencia de investigación es como el osquestador el resultado y la información actualizada se la da al equipo SWAT táctico como los Navy seals  que va ser el equipo de agente YAIWES que va a ejecutar es un proyector ya avanzado que está en proceso tu eres un eslabón necesario 🔗⛓️‍💥para magnificar el proceso 

Busca investigación de open ai antrophy y mínimax y Kimi k investiga y analiza el tema del imput como tú objetivo recaída información y incorporas para las 100x mejoras de tu propuesta 

Busca siempre en cada uno de los puntos y pasos que te di una investigación individual de cada uno en la comunidad de desarrolladores de programación de code y de comunidad de agente y Github y huggueface 

Incia con las tareas 1 a 5 y activa tu wachdog 

Una salida por tarea 

Inicia tarea 1 salida 1  
```

## INPUT BLOCK 11-C — RAÍZ ÚNICA DE TRABAJO

```text
Tu solo vas a trabajar dentro de esa raíz de sharck imput 

Todo lo que haces debe estar en esta raíz 

➡️ Osquestador auditor ➡️ main ➡️ 📂 imput sharck/

Es tu único lugar de trabajo no puedes usar más nada solo copiar el motor 

Todo los componentes del proyecto solo imput sharck sin mezclar otros componentes de los otros proyectos el código que haga va dentro de esa raíz 📂 IMPUT sharck /


Mi imput mis instrucciones van dentro de la arquitectura tu no puedes borrar reescribir la arquitectura solo puedes editar quirúrgicamente los archivos y todo debe estar cableado y con handoff a acrulizado 

Así que acomoda la mierda que hiciste y me das el enlace 
```

## INPUT BLOCK 11-D — INICIO TAREA 2 / UBICACIÓN AUTORIZADA

```text
Ok inicia tarea 2 📌 y asegurate que el code y componentes que ya está en curso estén en la raíz destino y ni en otro lugar no autorizado y lo resuelves y continuar con tarea 2 📌 seguir instrucciones 
```

---

# 12. TAREA 2 — DELTA DE ARQUITECTURA 100X INVESTIGADO — 2026-09-13

Estado: `RESEARCH_COMPLETE / ARCHITECTURE_DELTA / 100X_TARGET_NOT_ASSUMED / ROOT_ONLY`.

Fuente detallada de investigación, evidencia y microflujos: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/M63-TASK2-100X-RESEARCH-ARCHITECTURE.md`.
Control de estado: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/M63-TASK2-100X-RESEARCH-ARCHITECTURE.json`.

## 12.1 Regla 100x
No se declara 100x por diseño ni por cantidad de agentes. `100X_PASS` requiere baseline/candidato en el mismo fixture/host/versiones, >=100x en una métrica explícita y sin degradar cobertura, exactitud, evidencia, seguridad o gates. Métricas: E2E p50/p95, TTFT, evidence/sec, useful-context/sec, context tokens, duplicate-search %, coverage %, citation precision/recall, contradiction detection, tool success %, user-friction actions y coste.

## 12.2 Arquitectura transversal no monolítica
`INPUT_LOCK → InputSpec → SHARCK_DIRECTOR + DynamicFanoutGovernor → {RESEARCH || SKILLS || DATASETS || ADAPTERS || TOOLS || PERSISTENCE || EVIDENCE_SHERIFF || ERROR_LENS || SOLUTION_GUIDES || MULTI_SHARCK || NEWS? || ACADEMIC? || WATCHDOGS || SIMULATION?} → append-only EVIDENCE_LEDGER + CONTEXT_DELTA_BUS → LITERAL_ALIGNMENT/FAN-IN → minimal CONTEXT_PACKAGE → YAIWES`.

Los números de “paso” del INPUT son referencias de capacidades, no una cadena serial. Los lanes independientes pueden arrancar a la vez; los procesos reactivables/continuos siguen activos según condition/freshness/budget.

## 12.3 Governor 10–100+
SHARCK soporta expansión dinámica 10→100+ especialistas cuando existen ramas independientes suficientes. No crea 100 workers para cumplir cuota. Variables: independencia, goals descubiertos/no cubiertos, diversidad de fuente, marginal information gain, latency/token/API budget, rate limits, provider health y context pressure. `no_recursive_spawn=true` por defecto; concurrency cap independiente del total; dedup de solicitudes; timeout/circuit breaker; stop por cobertura/evidencia suficiente.

Evidencia investigada: Anthropic reporta mejores resultados en breadth-first y hasta 90% reducción de research time usando 3–5 subagents + tools paralelas; Kimi documenta hasta 300 subagents/4000+ tool calls y hasta 4.5x en búsqueda masiva; OpenAI Agents API expone long-running harness/context/subagents; MiniMax Agent Team usa agents paralelos para trabajo largo. La comunidad también reporta quota explosion y contention cuando no hay governor, por lo que la escala es adaptativa y no fija.

## 12.4 Context engineering
Cada microagente usa contexto aislado y devuelve evidence/pointers/resumen estructurado. Raw evidence permanece fuera de la ventana del LLM. `memory.md`, `profile.json`, `HANDOFF.md`, `handoff-index.json` y `evidence-ledger.jsonl` preservan estado/pointers; compaction no elimina provenance.

## 12.5 Skills/datasets/adapters/tools
Skills: >=3 bibliotecas → 20 full reads → pin/license/hash → 3 activos +5 standby → progressive disclosure.
Datasets: >=3 catálogos → cards/license/freshness/sample/eval → 3 activos +5 standby → pointers, no dump completo.
Adapters: contract/schema/auth/version/permission scoring → readonly probe → 3 activos +5 standby.
Tools/plugins: capability → MCP/API registry → schema/auth/version → readonly smoke → instrucciones al agente. Official MCP Registry es source preferente para metadata pública MCP.

## 12.6 Sheriff/refutación/anti-alucinación
Evidence Sheriff mantiene claim graph `claim→official→independent→contra-evidence→version/freshness→verdict` y 10 alternativas ordenadas por `0 fricción → menor tiempo → menor sobreingeniería → evidencia`.
Error Lens busca issues/regressions/breaking changes/comentarios negativos como carril adversarial.
Multi-SHARCK usa rutas rivales con contextos aislados y selección por score/evidencia, no por mayoría textual.
LiteralAlignment requiere `literal requirement → evidence/context pointer → output obligation`; GAP material bloquea `CONTEXT_READY`.

## 12.7 Persistencia/noticias/continuidad
Persistence Loop = event ledger + idempotency + checkpoints + heartbeat + stale recovery; 12 goals, Council12, 3 refutaciones, debate y 4 simulaciones pueden ejecutarse como celdas paralelas y fan-in a ContextDelta.
News Reporter se activa por freshness/event trigger, escala local→regional→nacional→internacional + social traces, con TTL/watchdog según volatilidad.
Continuous Work publica ContextDelta versionados a YAIWES en safe points sin reiniciar la tarea.
Watchdogs son condition/TTL-driven; persistencia significa estado/cola/sesión durable, no CPU spin infinito.

## 12.8 Simulación
Cuando uncertainty/risk supera threshold: 3 hipótesis independientes → simulación → comparación → nuevas solicitudes de evidencia. Toda simulación se etiqueta `SIMULATION`, nunca `EVIDENCE`. Paso 6 conserva las 4 simulaciones exigidas literalmente.

## 12.9 Ubicación física root-only corregida
Commit de reubicación: `eec96fc8cc324c09dbae8a8d26c2c257e99026cc`.
- 26 workflows históricos/activos SHARCK fueron retirados de `.github/workflows/` y preservados byte-idénticos en `➡️📂 sharck imput/📂 workflows reubicados/`.
- `.github/workflows/` ya no contiene nombres `sharck-` ni `shack-input` tras readback.
- Motor 2 fue copiado byte-idéntico a `➡️📂 sharck imput/📂 motores canónicos copiados/motor_2_queue_download_extract.py`, blob `84d566e2ee4e98e42eb3a864026d067d48caabd9`.
- Engine fue copiado byte-idéntico a `➡️📂 sharck imput/📂 motores canónicos copiados/hf_download_extract_engine.py`, blob `91e6e4486692eab314be5c7130d8310d3c855397`.
- Los workflows reubicados son `NON_AUTHORITATIVE_TEMPLATE`, porque desde la raíz ya no son entrypoints automáticos de GitHub Actions; no deben usar sus referencias históricas externas.
- Todo código M59 y componentes B01–B04/B07/B10 observados permanecen bajo `➡️📂 sharck imput/📂 input sharck code principal/`.
- B08/B09 no aparecen en el último listado físico de `componentes open source`; no se declaran adquiridos.

## 12.10 Frontera de esta tarea
Tarea 2 incorpora investigación y arquitectura; no abre descargas de Tarea 3 ni genera los nodos de enjambre de Tarea 4. Los gates históricos `physical_repair_allowed=false`, `b05_b06_download_allowed=false`, `step3_allowed=false` permanecen hasta decisión/gate posterior.
