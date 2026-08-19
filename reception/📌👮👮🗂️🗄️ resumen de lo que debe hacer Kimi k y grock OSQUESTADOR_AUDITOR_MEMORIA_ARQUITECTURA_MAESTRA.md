---

# 🧠 OSQUESTADOR AUDITOR CON MEMORIA
## Arquitectura Maestra Consolidada — Documento de Referencia para Diseño e Implementación por IA


INTEGRACIÓN FINAL DEL WORKFLOW + MEMORY/AUDIT ORCHESTRATOR
Esta salida cierra las dos anteriores: define qué debe programarse en el Workflow, qué debe programarse en el Memory/Audit Orchestrator, el contrato entre ambos, el ciclo completo y las reglas que deben quedar congeladas antes de escribir código.
BLOQUE 1/3 — WORKFLOW Y MOTOR DE EJECUCIÓN


# SALIDA 3 — WORKFLOW + MEMORY/AUDIT ORCHESTRATOR
## BLOQUE 1/3 — WORKFLOW

# 1. RESPONSABILIDAD DEL WORKFLOW

El Workflow es el cerebro determinista de ejecución.

No almacena todo el conocimiento del proyecto.

No razona por sí mismo.

No sustituye a la LLM.

Su función es convertir:

MASTER INPUT
    ↓
GOALS
    ↓
REQUIREMENTS
    ↓
PLAN
    ↓
TASK GRAPH
    ↓
EXECUTION
    ↓
VALIDATION
    ↓
CONSOLIDATION
    ↓
FINAL OUTPUT

Debe controlar todo el ciclo.

---

# 2. MASTER INPUT

El Master Input original debe ser:

- inmutable;
- versionado;
- trazable;
- siempre recuperable.

Debe conservarse literalmente.

No debe ser resumido como sustituto del original.

El sistema puede crear derivados, pero nunca reemplazar:

MASTER INPUT ORIGINAL

---

# 3. QUESTION ENGINE

Antes de ejecutar una tarea compleja debe existir una fase de interrogación estructurada.

El sistema debe generar preguntas para descubrir:

- qué se quiere conseguir;
- cuál es el objetivo;
- qué restricciones existen;
- qué información falta;
- qué debe investigarse;
- qué dependencias existen;
- qué riesgos existen;
- qué resultado se considera correcto;
- qué puede bloquear la ejecución.

Las preguntas no deben ser solamente preguntas para el usuario.

Deben ser también preguntas internas de planificación.

---

# 4. GOAL ENGINE

Las preguntas producen:

- objetivos;
- subobjetivos;
- criterios de éxito;
- criterios de fracaso.

Debe existir:

GOAL TREE

Ejemplo:

GOAL
 ├── GOAL A
 │    ├── TASK A1
 │    └── TASK A2
 │
 ├── GOAL B
 │    ├── TASK B1
 │    └── TASK B2
 │
 └── GOAL C

---

# 5. REQUIREMENT ENGINE

Cada objetivo debe convertirse en requisitos verificables.

Cada requirement necesita:

- ID;
- descripción;
- prioridad;
- origen;
- dependencia;
- criterio de cumplimiento;
- estado;
- tareas asociadas.

Estados:

DISCOVERED
PLANNED
IN_PROGRESS
SATISFIED
FAILED
BLOCKED
SUPERSEDED

---

# 6. PLAN ENGINE

El Planner no debe generar simplemente un texto de planificación.

Debe producir un objeto estructurado:

PLAN

que contenga:

- goals;
- requirements;
- phases;
- tasks;
- dependencies;
- resources;
- validation;
- checkpoints;
- recovery;
- expected artifacts.

---

# 7. TASK DAG

La tarea debe representarse como DAG cuando sea posible.

TASK A
 ├── TASK B
 ├── TASK C
 │     └── TASK E
 └── TASK D

TASK E no puede comenzar hasta que las dependencias requeridas estén satisfechas.

Pero el DAG debe poder modificarse.

Nueva información puede producir:

NEW REQUIREMENT
    ↓
NEW TASK
    ↓
NEW DEPENDENCY
    ↓
UPDATED DAG

---

# 8. TASK CONTRACT

Cada tarea debe tener un contrato.

Debe definir:

- input;
- contexto requerido;
- objetivo;
- restricciones;
- herramientas;
- worker;
- output schema;
- validadores;
- criterio de éxito;
- retry;
- timeout;
- escalamiento.

La LLM recibe el contrato.

No decide el contrato.

---

# 9. TASK FUNNEL

El Workflow debe convertir una tarea grande en unidades progresivamente pequeñas:

PROJECT
 ↓
PHASE
 ↓
GOAL
 ↓
TASK
 ↓
SUBTASK
 ↓
WORK UNIT
 ↓
LLM CALL

La unidad enviada a la LLM debe ser suficientemente pequeña para que pueda razonar correctamente.

---

# 10. CONTEXT REQUEST

Antes de cada Work Unit:

WORKFLOW
    ↓
REQUEST CONTEXT
    ↓
MEMORY ORCHESTRATOR
    ↓
CONTEXT PACK
    ↓
WORK UNIT

El Workflow indica:

- qué tarea está ejecutando;
- qué información necesita;
- qué objetivo persigue;
- qué evidencia necesita.

Memory Orchestrator recupera la información.

---

# 11. INPUT BLOCK

El Runtime construye un Input Block estructurado.

Debe contener:

MASTER INPUT
CURRENT GOAL
CURRENT TASK
TASK CONTRACT
RELEVANT CONTEXT
EVIDENCE
CURRENT STATE
CURRENT CONSOLIDATION
OPEN QUESTIONS
CONSTRAINTS
OUTPUT SCHEMA

La LLM recibe esto.

---

# 12. PINNED INPUT

Debe existir una sección de información que acompañe cada ventana.

PINNED:

- instrucciones críticas;
- objetivo principal;
- restricciones;
- requisitos críticos;
- decisiones importantes;
- políticas.

Esto evita que la segmentación destruya el enfoque.

---

# 13. CARRY FORWARD

Cada ventana debe producir:

CARRY_FORWARD_STATE

Debe contener:

- objetivo actual;
- tarea actual;
- hechos descubiertos;
- decisiones;
- errores;
- preguntas abiertas;
- dependencias;
- progreso;
- siguiente acción;
- consolidación actual.

El siguiente Input Block recibe este estado.

---

# 14. LLM OUTPUT

La salida no debe ser considerada automáticamente como verdad.

Debe pasar por:

LLM OUTPUT
 ↓
NORMALIZER
 ↓
SCHEMA VALIDATION
 ↓
AUDIT
 ↓
STATE DELTA
 ↓
CONSOLIDATION

---

# 15. STATE DELTA

La LLM propone cambios.

No modifica directamente el estado global.

Debe producir:

STATE DELTA

Ejemplo:

- fact_added;
- decision_added;
- task_completed;
- task_created;
- issue_detected;
- evidence_added;
- contradiction_detected.

El Runtime decide si aplica el delta.

---

# 16. CONTINUOUS EXECUTION LOOP

Mientras existan tareas ejecutables:

GET NEXT TASK
 ↓
GET CONTEXT
 ↓
CREATE SANDBOX
 ↓
EXECUTE
 ↓
VALIDATE
 ↓
UPDATE STATE
 ↓
CHECKPOINT
 ↓
CONSOLIDATE
 ↓
NEXT TASK

El sistema continúa automáticamente.

---

# 17. STOP CONDITIONS

Debe detenerse cuando:

- no existen tareas;
- existe conflicto crítico;
- falta autorización;
- existe violación de policy;
- no existe progreso;
- se alcanzan límites;
- existe fallo repetitivo;
- se necesita intervención humana.

No debe detenerse simplemente porque una LLM terminó una respuesta.

---

# 18. RETRY

Un retry no debe repetir ciegamente el mismo prompt.

Debe registrar:

ATTEMPT 1
 ↓
FAILURE ANALYSIS
 ↓
STRATEGY CHANGE
 ↓
ATTEMPT 2

Si continúa:

ATTEMPT 3
 ↓
ESCALATE

---

# 19. CHECKPOINT

Después de cada unidad significativa:

STATE
TASK STATE
MEMORY VERSION
ARTIFACTS
CONSOLIDATION
AUDIT
NEXT ACTION

→ CHECKPOINT

Esto permite continuar después de errores.

---

# 20. ROLLBACK

Si un estado es inválido:

CURRENT
 ↓
INVALID
 ↓
FIND LAST VALID CHECKPOINT
 ↓
ROLLBACK
 ↓
REPAIR / BRANCH
 ↓
CONTINUE

Nunca:

ERROR
 ↓
START FROM ZERO

---

# 21. BRANCHING

Si existen varias estrategias:

PLAN A
PLAN B
PLAN C

pueden ejecutarse aisladamente.

Después:

COMPARE
 ↓
AUDIT
 ↓
JUDGE
 ↓
SELECT VALIDATED BRANCH

---

# 22. CONVERGENCE

Cada ciclo debe medir:

- progreso;
- cobertura;
- errores;
- contradicciones;
- tareas pendientes;
- incertidumbre.

Si existe progreso:

CONTINUE

Si no existe progreso:

CHANGE STRATEGY

Si existe fallo persistente:

ESCALATE

---

# 23. FINALIZATION

La tarea no termina cuando existe una respuesta.

Debe pasar:

TASK COMPLETION
 ↓
COVERAGE AUDIT
 ↓
CONTRADICTION AUDIT
 ↓
REQUIREMENT AUDIT
 ↓
GLOBAL CONSOLIDATION
 ↓
FINAL VALIDATION
 ↓
FINAL OUTPUT

# SALIDA 3
## BLOQUE 2/3 — MEMORY/AUDIT ORCHESTRATOR

# 24. RESPONSABILIDAD

El Memory/Audit Orchestrator administra el conocimiento externo necesario para que una LLM limitada pueda trabajar sobre proyectos mucho mayores que su ventana.

Debe administrar:

RAW DATA
MEMORY
EVIDENCE
INDEXES
TAGS
GRAPH
ARTIFACTS
HISTORY
CONSOLIDATIONS
CHECKPOINT REFERENCES
AUDIT

---

# 25. NO ES UNA BASE DE DATOS SIMPLE

Debe funcionar como:

MEMORY FABRIC
+
RETRIEVAL ENGINE
+
EVIDENCE GRAPH
+
CONTEXT FABRIC
+
AUDIT ENGINE

---

# 26. MEMORY LAYERS

L0 — RAW SOURCE

Fuente original.

L1 — WORKING MEMORY

Información de la ventana actual.

L2 — TASK MEMORY

Información de la tarea.

L3 — PROJECT MEMORY

Estado global del proyecto.

L4 — LONG-TERM KNOWLEDGE

Información reutilizable.

---

# 27. RAW SOURCE

Nunca eliminar la fuente original debido a una síntesis.

Debe poder recuperarse:

SOURCE
VERSION
HASH
LOCATION
PROVENANCE

---

# 28. CHUNKING

El sistema debe dividir información considerando:

- semántica;
- estructura;
- sección;
- entidad;
- dependencia;
- código;
- función;
- clase;
- requisito.

No solamente tamaño.

---

# 29. TAGGING

Cada objeto puede tener:

PROJECT
TOPIC
TASK
GOAL
REQUIREMENT
ENTITY
SOURCE
EVIDENCE
STATUS
PRIORITY
VERSION
DEPENDENCY

Y relaciones:

SUPPORTS
CONTRADICTS
DEPENDS_ON
DERIVED_FROM
IMPLEMENTS
VALIDATES
SUPERSEDES
RELATED_TO

---

# 30. RETRIEVAL

Debe existir Retrieval híbrido:

LEXICAL
+
SEMANTIC
+
TAG
+
GRAPH
+
ENTITY
+
TEMPORAL
+
TASK
+
EVIDENCE
+
HISTORY

Después:

RETRIEVE
 ↓
RERANK
 ↓
FILTER
 ↓
CONTEXT PACK

---

# 31. CONTEXT FABRIC

No debe devolver documentos indiscriminadamente.

Debe construir:

MINIMAL SUFFICIENT CONTEXT

Debe contener solamente lo necesario para ejecutar la unidad actual.

---

# 32. CONTEXT BUDGET

Debe conocer:

MODEL LIMIT
SYSTEM TOKENS
TASK TOKENS
OUTPUT RESERVE
PINNED TOKENS
MEMORY BUDGET
SAFETY MARGIN

Y nunca superar el límite.

---

# 33. MEMORY COMPACTION

Cuando la información crece:

WINDOW
 ↓
EXTRACT
 ↓
VALIDATE
 ↓
CONSOLIDATE
 ↓
STORE
 ↓
INDEX

La fuente original permanece.

La síntesis es una capa derivada.

---

# 34. CONSOLIDATION

Debe existir:

LOCAL CONSOLIDATION

y:

GLOBAL CONSOLIDATION

La consolidación global debe integrar:

facts
decisions
evidence
requirements
artifacts
dependencies
contradictions
task state

No solamente texto resumido.

---

# 35. CLAIM SYSTEM

Cada afirmación relevante debe poder tener:

CLAIM
SOURCE
EVIDENCE
CONFIDENCE
STATUS
PROVENANCE

Estados:

UNVERIFIED
SUPPORTED
CONFLICTED
VALIDATED
REJECTED
SUPERSEDED

---

# 36. EVIDENCE GRAPH

Debe representar:

CLAIM
 ↓
SOURCE
 ↓
EVIDENCE

y:

CLAIM
 ↓
SUPPORTS
 ↓
REQUIREMENT

o:

CLAIM A
 ↓
CONTRADICTS
 ↓
CLAIM B

---

# 37. MEMORY AUDIT

Debe ejecutarse continuamente.

Debe detectar:

- duplicados;
- contradicciones;
- información obsoleta;
- claims sin evidencia;
- referencias rotas;
- memoria huérfana;
- estados inconsistentes;
- artefactos sin procedencia.

---

# 38. MEMORY VERSIONING

Cada cambio importante debe producir una nueva versión.

No sobrescribir silenciosamente.

Debe poder reconstruirse:

VERSION N
 ↓
VERSION N+1
 ↓
VERSION N+2

---

# 39. HISTORY

Debe conservar eventos:

INPUT_RECEIVED
DOCUMENT_INGESTED
MEMORY_CREATED
MEMORY_UPDATED
RETRIEVAL_EXECUTED
CLAIM_CREATED
AUDIT_EXECUTED
CONFLICT_FOUND
CONSOLIDATION_CREATED
CHECKPOINT_CREATED
ROLLBACK_EXECUTED

---

# 40. TRACEABILITY

Cada elemento crítico debe responder:

¿De dónde salió?

¿Quién lo produjo?

¿Con qué versión?

¿En qué tarea?

¿Con qué evidencia?

¿En qué checkpoint?

¿Fue validado?

---

# 41. RESOURCE BRAIN

El Orchestrator debe mantener un catálogo de recursos:

MODELS
APIS
TOOLS
DATASETS
INDEXES
SKILLS
WORKERS
SANDBOXES
SERVICES

Estados:

DISCOVERED
REGISTERED
CONFIGURED
REACHABLE
HEALTHY
AUTHORIZED
AVAILABLE
DEGRADED
UNAVAILABLE

---

# 42. RESOURCE ROUTING

El Router puede consultar:

CAPABILITY
HEALTH
AUTHORIZATION
CONTEXT LIMIT
LATENCY
COST
SPECIALIZATION
POLICY

Pero la decisión final de ejecución pertenece al Runtime.

---

# 43. MEMORY RESPONSE

El resultado de Memory Orchestrator no debe ser una respuesta conversacional.

Debe ser:

CONTEXT PACK

con:

- relevant memory;
- evidence;
- relations;
- current state;
- consolidation;
- open questions;
- provenance;
- confidence;
- context budget.

---

# 44. REGLA FUNDAMENTAL

MEMORY ORCHESTRATOR

NO decide:

- objetivo;
- política global;
- estrategia final;
- finalización;
- autorización.

Entrega información estructurada al Runtime.

# SALIDA 3
## BLOQUE 3/3 — CONTRATO WORKFLOW ↔ MEMORY/AUDIT

# 45. INTERFAZ CONCEPTUAL

WORKFLOW
    │
    │ GET_CONTEXT
    ▼
MEMORY/AUDIT
    │
    ├── RETRIEVE
    ├── RERANK
    ├── AUDIT
    ├── RELATE
    └── BUILD_CONTEXT
    │
    ▼
CONTEXT PACK
    │
    ▼
WORKFLOW
    │
    ▼
SANDBOX
    │
    ▼
LLM
    │
    ▼
STATE DELTA
    │
    ▼
MEMORY/AUDIT
    │
    ├── VALIDATE
    ├── STORE
    ├── AUDIT
    └── CONSOLIDATE
    │
    ▼
WORKFLOW

---

# 46. OPERACIONES PRINCIPALES

El Workflow debe poder solicitar:

GET_CONTEXT
GET_MEMORY
GET_EVIDENCE
GET_STATE
GET_HISTORY
GET_ARTIFACT
GET_RELATIONS
AUDIT_MEMORY

Y enviar:

SAVE_STATE_DELTA
SAVE_ARTIFACT
SAVE_CLAIM
SAVE_EVIDENCE
SAVE_CONSOLIDATION
CREATE_CHECKPOINT

---

# 47. REGLA DE ESCRITURA

La LLM no escribe directamente en memoria canónica.

Siempre:

LLM
 ↓
OUTPUT
 ↓
NORMALIZER
 ↓
SCHEMA VALIDATION
 ↓
AUDIT
 ↓
STATE DELTA
 ↓
MEMORY UPDATE

Esto evita que una alucinación se convierta inmediatamente en memoria permanente.

---

# 48. REGLA DE LECTURA

La LLM tampoco decide libremente qué memoria utilizar.

El Runtime solicita:

CONTEXT FOR TASK X

Memory Orchestrator construye:

CONTEXT PACK

La LLM procesa:

CONTEXT PACK

---

# 49. CONTINUOUS COGNITIVE LOOP

El ciclo completo queda:

MASTER INPUT
 ↓
QUESTION ENGINE
 ↓
GOALS
 ↓
REQUIREMENTS
 ↓
PLAN
 ↓
TASK DAG
 ↓
TASK FUNNEL
 ↓
TASK CONTRACT
 ↓
MEMORY RETRIEVAL
 ↓
CONTEXT FABRIC
 ↓
SANDBOX
 ↓
LLM
 ↓
OUTPUT
 ↓
SCHEMA VALIDATION
 ↓
AUDIT
 ↓
STATE DELTA
 ↓
CONSOLIDATION
 ↓
MEMORY UPDATE
 ↓
CHECKPOINT
 ↓
COVERAGE CHECK
 ↓
NEXT TASK
 ↓
REPEAT

---

# 50. EL SISTEMA DEBE PODER CONTINUAR SIN NUEVO INPUT HUMANO

Si:

- existen tareas;
- existe autorización;
- existe contexto;
- existe progreso;
- no existe conflicto crítico;

entonces:

CONTINUE LOOP

No esperar:

USER → NUEVO PROMPT

para cada subtarea.

---

# 51. AUTO-PREGUNTAS

Durante la ejecución pueden generarse:

- preguntas de investigación;
- preguntas de validación;
- preguntas de integración;
- preguntas de contradicción;
- preguntas de dependencia.

Estas preguntas se convierten en tareas.

Ejemplo:

TASK A
 ↓
QUESTION Q1
 ↓
RESEARCH TASK R1
 ↓
ANSWER
 ↓
UPDATE TASK A

---

# 52. AUTO-RESEARCH

Cuando falta conocimiento:

UNKNOWN
 ↓
RESEARCH TASK
 ↓
RESOURCE ROUTER
 ↓
WORKER
 ↓
EVIDENCE
 ↓
AUDIT
 ↓
MEMORY
 ↓
ORIGINAL TASK

El sistema no debe inventar para llenar el vacío.

---

# 53. CONSOLIDACIÓN EN EMBUDO

El sistema debe consolidar progresivamente:

WORK UNIT
 ↓
TASK RESULT
 ↓
TASK CONSOLIDATION
 ↓
PHASE CONSOLIDATION
 ↓
PROJECT CONSOLIDATION
 ↓
FINAL CONSOLIDATION

Esto evita el problema:

"cada segmento funciona, pero nadie puede unirlos."

---

# 54. INTEGRATION CHECK

Antes de considerar terminado un proyecto:

Cada:

REQUIREMENT

debe apuntar a:

TASK
 ↓
ARTIFACT
 ↓
EVIDENCE
 ↓
VALIDATION

Si existe:

REQUIREMENT
 ↓
NO IMPLEMENTATION

entonces:

INCOMPLETE

---

# 55. CROSS-CHECK

Debe existir una comprobación bidireccional:

TOP-DOWN:

GOALS
 ↓
REQUIREMENTS
 ↓
TASKS
 ↓
ARTIFACTS

BOTTOM-UP:

ARTIFACTS
 ↓
TASKS
 ↓
REQUIREMENTS
 ↓
GOALS

Después comparar ambos.

---

# 56. FINAL JUDGE

El Judge debe decidir:

PASS
FAIL
REPAIR
ESCALATE
HUMAN_REQUIRED

No debe aceptar:

"la LLM dice que terminó".

Debe comprobar el estado objetivo.

---

# 57. FINAL AUDIT

Antes de producir la salida final:

AUDIT 1
→ REQUIREMENTS

AUDIT 2
→ EVIDENCE

AUDIT 3
→ CONTRADICTIONS

AUDIT 4
→ COVERAGE

AUDIT 5
→ TRACEABILITY

Después:

GLOBAL CONSOLIDATION

y finalmente:

FINAL OUTPUT

---

# 58. REGLA CONTRA ALUCINACIÓN

La arquitectura no debe intentar resolver alucinaciones solamente mediante prompts.

Debe reducirlas estructuralmente:

SOURCE
+
EVIDENCE
+
RETRIEVAL
+
SCHEMA
+
STATE
+
AUDIT
+
CROSS-CHECK
+
TRACEABILITY

La LLM puede equivocarse.

El sistema debe detectar el error antes de convertirlo en estado canónico.

---

# 59. REGLA CONTRA PÉRDIDA DE CONTEXTO

No intentar conservar todo dentro de la ventana.

Conservar externamente:

MASTER INPUT
+
MEMORY
+
STATE
+
ARTIFACTS
+
EVIDENCE
+
CONSOLIDATION
+
CHECKPOINTS
+
HISTORY

Y recuperar dinámicamente:

RELEVANT CONTEXT

---

# 60. REGLA CONTRA FRAGMENTACIÓN

La solución al problema:

"cada segmento funciona pero el proyecto completo falla"

es:

LOCAL RESULTS
 ↓
LOCAL CONSOLIDATION
 ↓
GLOBAL STATE
 ↓
INTEGRATION MAP
 ↓
GLOBAL CONSOLIDATION
 ↓
CROSS-CHECK
 ↓
FINAL VALIDATION

No basta con guardar resúmenes.

Debe existir una estructura global de relaciones.

---

# 61. ARQUITECTURA FINAL

                    USER
                     │
                     ▼
                MASTER INPUT
                     │
                     ▼
            ┌─────────────────┐
            │    WORKFLOW     │
            │                 │
            │ Goals           │
            │ Requirements    │
            │ Planner         │
            │ Task DAG        │
            │ Task Funnel     │
            │ Runtime         │
            │ Policy          │
            │ Router          │
            └────────┬────────┘
                     │
                     ▼
            MEMORY REQUEST
                     │
                     ▼
       ┌──────────────────────────┐
       │ MEMORY/AUDIT ORCHESTRATOR│
       │                          │
       │ Memory                   │
       │ Retrieval                │
       │ Tags                     │
       │ Graph                    │
       │ Evidence                │
       │ Audit                    │
       │ Context Fabric           │
       │ Resource Brain            │
       │ History                  │
       └────────────┬─────────────┘
                    │
                    ▼
              CONTEXT PACK
                    │
                    ▼
                 SANDBOX
                    │
                    ▼
                   LLM
                    │
                    ▼
              STATE DELTA
                    │
                    ▼
          AUDIT + VALIDATION
                    │
                    ▼
              CONSOLIDATOR
                    │
              ┌─────┴─────┐
              ▼           ▼
           MEMORY      CHECKPOINT
              │           │
              └─────┬─────┘
                    ▼
               NEXT TASK
                    │
                    ▼
                 LOOP


FRONTERA DEFINITIVA
WORKFLOW
Pregunta:
¿Qué debemos hacer?
Controla:
¿Qué hacemos ahora?
MEMORY/AUDIT
Pregunta:
¿Qué información necesitamos?
Controla:
¿Qué información recuperamos, conservamos y validamos?
SANDBOX
Controla:
¿Dónde ejecutamos esta unidad y con qué estado?
LLM
Hace:
Razonar y procesar la unidad asignada.
CONSOLIDATOR
Hace:
Integrar las piezas.
AUDITOR
Hace:
Comprobar si las piezas son confiables y completas.
CHECKPOINT
Hace:
Permitir continuar, recuperar o retroceder.
63. PRINCIPIO FINAL
LLM
= COGNITIVE PROCESSOR

WORKFLOW
= EXECUTION CONTROL

MEMORY ORCHESTRATOR
= EXTERNAL COGNITIVE MEMORY

AUDITOR
= VERIFICATION

SANDBOX
= ISOLATED WORKSPACE

CHECKPOINT
= RECOVERY

CONSOLIDATOR
= GLOBAL INTEGRATION

ROUTER
= RESOURCE SELECTION

POLICY
= AUTHORITY

STATE MACHINE
= DETERMINISTIC TRANSITIONS
Y la regla raíz:
THE MODEL THINKS.
THE RUNTIME CONTROLS.
THE MEMORY REMEMBERS.
THE RETRIEVER FINDS.
THE AUDITOR QUESTIONS.
THE CONSOLIDATOR CONNECTS.
THE CHECKPOINT RECOVERS.
THE POLICY AUTHORIZES.
THE JUDGE VALIDATES.
64. ORDEN DE PROGRAMACIÓN
No recomiendo comenzar programando la interfaz.
El orden correcto para construir el sistema sería:
01. CORE STATE MODEL
02. EVENT MODEL
03. TASK MODEL
04. TASK CONTRACT
05. STATE MACHINE
06. CHECKPOINT ENGINE
07. POLICY ENGINE
08. MEMORY CONTRACT
09. RETRIEVAL CONTRACT
10. CONTEXT FABRIC
11. SANDBOX CONTRACT
12. WORKER CONTRACT
13. OUTPUT SCHEMA
14. AUDIT ENGINE
15. CONSOLIDATOR
16. ROUTER
17. CONTINUOUS LOOP
18. RECOVERY
19. RESOURCE BRAIN
20. GLOBAL INTEGRATION
21. FIVE-PASS BUILD AUDITOR
22. API
23. UI
La UI debe ser la última capa, porque el comportamiento real debe existir independientemente de la interfaz.
65. CRITERIO DE ÉXITO DEL SISTEMA
El sistema estará realmente terminado cuando una LLM pequeña pueda recibir:
20 MILLONES DE CONTEXTO TOTAL
sin recibir los 20M simultáneamente y pueda:
LEER
 ↓
SEGMENTAR
 ↓
INVESTIGAR
 ↓
RAZONAR
 ↓
RESOLVER
 ↓
GUARDAR
 ↓
CONSOLIDAR
 ↓
RECUPERAR
 ↓
CONTINUAR
 ↓
INTEGRAR
 ↓
AUDITAR
 ↓
REPARAR
 ↓
FINALIZAR
sin perder:
objetivo;
instrucciones originales;
decisiones;
evidencia;
dependencias;
resultados anteriores;
estado;
trazabilidad.
Y, sobre todo:
una solución parcial no se considera automáticamente una solución global.
La integración global, cobertura y validación son fases obligatorias.

### Resultado de las 3 salidas

Con esto quedan separadas las tres capas que no conviene mezclar:

**Workflow/Runtime**
→ transforma el problema en trabajo ejecutable.

**Memory/Audit Orchestrator**
→ transforma almacenamiento masivo en contexto relevante, verificable y recuperable.

**Sandbox + LLM**
→ ejecuta unidades cognitivas aisladas y devuelve cambios candidatos.

Y el **Consolidator** es el puente que evita precisamente el problema que señalaste: que el modelo sea capaz de resolver 100 fragmentos individualmente pero sea incapaz de construir correctamente **el proyecto completo**.

SALIDA 2 — ORQUESTADOR AUDITOR DE MEMORIA

En esta salida voy a separar qué debe vivir dentro del Orquestador de Memoria/Auditor, qué debe quedar en el Workflow y cómo se conectan ambos, sin mezclar responsabilidades.

La regla central es:

Workflow decide qué trabajo ejecutar. Memory/Audit Orchestrator decide qué información recuperar, cómo conservarla, cómo auditarla y qué contexto estructurado entregar al Workflow/Runtime.

1. Qué debe ser el Orquestador de Memoria/Auditor

No debe ser simplemente una base de datos con búsqueda.

Debe funcionar como una Memory & Evidence Fabric:

MEMORY/AUDIT ORCHESTRATOR │ ┌──────────────────────┼──────────────────────┐ │ │ │ INGESTION MEMORY AUDIT │ │ │ documentos estado claims mensajes hechos evidencia código decisiones conflictos outputs artefactos cobertura eventos historial consistencia │ │ │ └──────────────────────┼──────────────────────┘ │ CONTEXT FABRIC │ CONTEXT PACK │ WORKFLOW 

2. Las 12 funciones principales

El Orquestador debe tener como mínimo:

01. INGESTION 02. NORMALIZATION 03. CHUNKING 04. INDEXING 05. TAGGING 06. RETRIEVAL 07. RERANKING 08. MEMORY STATE 09. EVIDENCE GRAPH 10. AUDIT 11. CONSOLIDATION 12. CONTEXT FABRICATION 

Pero deben existir además mecanismos transversales:

VERSIONING CHECKPOINTING TRACEABILITY PROVENANCE DEDUPLICATION CONFLICT MANAGEMENT STALE-DATA DETECTION ACCESS CONTROL RESOURCE HEALTH REPAIR 

3. INGESTION

Todo material que entra debe convertirse en objetos manejables.

Ejemplos:

USER INPUT DOCUMENT PDF MARKDOWN CODE CHAT API RESPONSE LLM OUTPUT RESEARCH RESULT ARTIFACT EVENT CHECKPOINT 

Cada elemento recibe un identificador estable.

No debe depender exclusivamente del nombre del archivo.

4. NORMALIZATION

Antes de indexar:

RAW ↓ NORMALIZE ↓ IDENTIFY ↓ CLASSIFY ↓ VERSION ↓ INDEX 

Debe conservarse siempre el original.

Nunca reemplazar silenciosamente la fuente original por una versión resumida.

5. CHUNKING INTELIGENTE

No utilizar solamente:

cada N tokens 

El chunking debe considerar:

estructura semántica secciones dependencias entidades código funciones clases tablas requisitos relaciones 

Un documento puede convertirse en:

DOCUMENT ├── SECTION │ ├── SUBSECTION │ │ ├── CLAIM │ │ ├── EVIDENCE │ │ └── RELATION │ └── ... └── ... 

Esto permite recuperar unidades pequeñas sin perder su procedencia.

6. TAG ENGINE

El sistema que propusiste de Tags debe convertirse en un componente formal.

Cada objeto puede tener:

PROJECT TASK MODULE ENTITY TOPIC REQUIREMENT GOAL EVIDENCE STATUS PRIORITY VERSION DATE SOURCE DEPENDENCY CONFIDENCE 

Pero además:

supports contradicts depends_on derived_from implements validates supersedes related_to 

Los Tags sirven para reducir brutalmente el espacio de búsqueda.

7. BÚSQUEDA MULTICAPA

No depender de un solo buscador.

El Retrieval Engine debe combinar:

LEXICAL SEARCH + SEMANTIC SEARCH + TAG SEARCH + ENTITY SEARCH + GRAPH SEARCH + TEMPORAL SEARCH + TASK SEARCH + EVIDENCE SEARCH + HISTORY SEARCH 

Después:

CANDIDATES ↓ RERANK ↓ FILTER ↓ CONTEXT PACK 

Esto es mucho más robusto que simplemente hacer RAG.

8. MEMORY STATE

La memoria debe distinguir diferentes tipos de información.

RAW FACT EVIDENCE DECISION INFERENCE HYPOTHESIS ASSUMPTION REQUIREMENT TASK RESULT UNKNOWN CONFLICT REJECTED SUPERSEDED 

Esto es crítico para reducir alucinaciones.

Por ejemplo:

"X funciona así" 

no debería almacenarse automáticamente como:

FACT 

Puede comenzar como:

CLAIM STATUS = UNVERIFIED 

Después el Auditor determina su estado.

9. EVIDENCE GRAPH

Cada afirmación importante debe poder apuntar hacia su origen.

CLAIM │ ├── derived_from → SOURCE │ ├── supported_by → EVIDENCE │ ├── related_to → CLAIM │ └── affects → TASK 

Esto permite contestar:

¿De dónde salió esta conclusión?

sin depender de que la LLM lo recuerde.

10. AUDITOR DE MEMORIA

Debe realizar auditorías continuas.

No solamente al final.

Debe buscar:

DUPLICATES CONTRADICTIONS STALE INFORMATION UNVERIFIED CLAIMS ORPHAN MEMORY BROKEN REFERENCES INVALID RELATIONS MISSING EVIDENCE INCONSISTENT STATE 

Y generar:

MEMORY_AUDIT_RESULT 

con estados como:

VALID UNVERIFIED CONFLICT STALE ORPHAN INVALID REVIEW_REQUIRED 

11. CONSOLIDACIÓN DE MEMORIA

Aquí está una diferencia importante.

Consolidar no significa resumir.

El sistema debe conservar:

SOURCE MATERIAL ↓ ATOMIC FACTS ↓ RELATIONS ↓ LOCAL CONSOLIDATION ↓ MODULE CONSOLIDATION ↓ GLOBAL CONSOLIDATION 

La síntesis es una capa derivada.

Nunca debe destruir la fuente.

12. CONTEXT FABRIC

Esta es probablemente una de las partes más importantes del sistema.

El Memory Orchestrator no debería entregar simplemente:

top_k documents 

Debe construir:

CONTEXT PACK 

para la tarea concreta.

Ejemplo:

CURRENT TASK + TASK REQUIREMENTS + RELEVANT FACTS + RELEVANT EVIDENCE + RELEVANT DECISIONS + CURRENT STATE + CURRENT CONSOLIDATION + OPEN QUESTIONS + CONSTRAINTS + REQUIRED OUTPUT SCHEMA 

El resultado debe respetar el límite de contexto de la LLM.

13. CONTEXT BUDGETER

Debe existir un componente que conozca:

MODEL_CONTEXT_LIMIT RESERVED_OUTPUT SYSTEM_CONTEXT TASK_CONTEXT MEMORY_CONTEXT SAFETY_MARGIN 

Y calcule:

AVAILABLE_CONTEXT 

Por ejemplo conceptualmente:

TOTAL - SYSTEM - TASK - OUTPUT_RESERVE - SAFETY_MARGIN = MEMORY_BUDGET 

La memoria no debe llenar arbitrariamente la ventana.

14. CONTEXT PRIORITY

Si no cabe todo:

P0 = instrucciones críticas P1 = tarea actual P2 = requisitos P3 = estado actual P4 = evidencia directa P5 = decisiones P6 = consolidación P7 = contexto relacionado P8 = información secundaria 

El Context Fabric elimina o posterga P8 antes de sacrificar P0–P4.

15. MEMORY COMPACTION

Cuando una sesión se hace demasiado grande:

OLD WINDOW ↓ EXTRACT ↓ VALIDATE ↓ CONSOLIDATE ↓ STORE ↓ INDEX 

Después la siguiente ventana recibe:

MASTER INPUT + CURRENT STATE + CONSOLIDATION + RELEVANT RETRIEVED MEMORY 

No recibe necesariamente todo el historial.

16. EL "ARRASTRE" QUE PROPUSISTE

Debe formalizarse como:

CARRY FORWARD STATE 

Cada ventana genera:

CARRY_FORWARD 

que contiene únicamente:

CURRENT OBJECTIVE CURRENT TASK DECISIONS FACTS OPEN QUESTIONS DEPENDENCIES ERRORS NEXT ACTION CURRENT CONSOLIDATION 

La siguiente ventana recibe ese estado.

Así se obtiene el efecto de:

leer página → tomar notas → continuar → actualizar notas → leer siguiente página.

Pero de forma estructurada.

17. PUSH-PIN

También incorporaría tu concepto de "push/pin".

Debe existir:

PINNED_CONTEXT 

Información que nunca debe desaparecer durante determinada tarea.

Por ejemplo:

MASTER REQUIREMENT CRITICAL CONSTRAINT USER INSTRUCTION SAFETY POLICY CURRENT GOAL KEY DECISION 

Mientras que:

EPHEMERAL_CONTEXT 

puede ser sustituido.

18. MEMORY LAYERS

Propongo cinco niveles:

L0 — RAW L1 — WORKING MEMORY L2 — TASK MEMORY L3 — PROJECT MEMORY L4 — LONG-TERM KNOWLEDGE 

L0 RAW

Fuente original.

L1 WORKING

Ventana actual.

L2 TASK

Información necesaria para completar la tarea.

L3 PROJECT

Estado global del proyecto.

L4 LONG-TERM

Conocimiento persistente reutilizable.

19. HISTORIAL

Todo cambio importante debe producir:

EVENT 

Ejemplo:

TASK_CREATED TASK_STARTED MEMORY_RETRIEVED LLM_EXECUTED OUTPUT_RECEIVED AUDIT_FAILED REPAIR_CREATED CHECKPOINT_CREATED STATE_UPDATED TASK_COMPLETED 

Esto permite reconstruir lo sucedido.

20. CONEXIÓN CON CHECKPOINTS

El Memory Orchestrator no debe guardar únicamente archivos.

Debe relacionarse con:

CHECKPOINT │ ├── STATE ├── MEMORY VERSION ├── TASK VERSION ├── ARTIFACT VERSION ├── CONSOLIDATION VERSION └── AUDIT VERSION 

Entonces un rollback puede recuperar el estado cognitivo completo.

21. CONEXIÓN CON WORKFLOW

La interfaz conceptual debe ser:

WORKFLOW │ │ request_context() ▼ MEMORY ORCHESTRATOR │ ├── retrieve ├── rerank ├── audit ├── assemble └── validate │ ▼ CONTEXT PACK │ ▼ WORKFLOW │ ▼ LLM │ ▼ STATE DELTA │ ▼ MEMORY ORCHESTRATOR 

El ciclo se repite.

22. CONEXIÓN CON EL CONSOLIDATOR

Después de cada unidad:

LLM OUTPUT ↓ NORMALIZER ↓ AUDIT ↓ STATE DELTA ↓ CONSOLIDATOR ↓ MEMORY 

El Consolidator no debe inventar información faltante.

Si dos resultados dicen:

A = X A = Y 

debe registrar:

CONFLICT 

y crear una tarea de resolución.

23. CONEXIÓN CON SENTINEL / SHERIFF / JUDGE

SENTINEL

Observa.

detect anomaly 

SHERIFF

Ejecuta control.

pause retry rollback branch block 

JUDGE

Evalúa resultado.

PASS FAIL REPAIR ESCALATE 

El Memory Orchestrator conserva todas esas decisiones.

24. QUÉ NO DEBE HACER EL MEMORY ORCHESTRATOR

No debe:

decidir el objetivo global; crear arbitrariamente tareas; controlar el loop principal; autorizar acciones peligrosas; decidir qué modelo debe ganar; modificar instrucciones del usuario; convertir hipótesis en hechos; borrar conflictos silenciosamente. 

Eso pertenece al Runtime/Workflow/Policy/Audit según corresponda.

25. CONTRATO ENTRE AMBOS SISTEMAS

El Workflow debe poder solicitar:

GET_CONTEXT GET_MEMORY GET_EVIDENCE GET_ARTIFACTS GET_STATE GET_HISTORY GET_RELEVANT_RELATIONS AUDIT_MEMORY SAVE_STATE SAVE_ARTIFACT SAVE_CONSOLIDATION CREATE_CHECKPOINT 

El Memory Orchestrator debe responder con objetos estructurados, no con texto libre únicamente.

26. CICLO COMPLETO

USER ↓ MASTER INPUT ↓ WORKFLOW ↓ QUESTIONS ↓ GOALS ↓ PLAN ↓ TASK ↓ MEMORY REQUEST ↓ RETRIEVAL ↓ AUDIT MEMORY ↓ CONTEXT FABRIC ↓ SANDBOX ↓ LLM ↓ STATE DELTA ↓ AUDIT OUTPUT ↓ CONSOLIDATION ↓ MEMORY UPDATE ↓ CHECKPOINT ↓ NEXT TASK ↓ REPEAT 

27. EL PRINCIPIO MÁS IMPORTANTE

El sistema debe conseguir que una LLM de:

120K 

o:

250K 

pueda trabajar sobre:

1M 5M 20M 100M+ 

sin convertir mágicamente su ventana en 100M.

La capacidad adicional proviene de:

EXTERNAL MEMORY + RETRIEVAL + TASK DECOMPOSITION + STATE + CHECKPOINTS + CONSOLIDATION + AUDIT + CONTEXT FABRICATION 

La LLM nunca necesita "recordar" los 20M.

El Runtime y la Memory Fabric hacen que pueda acceder nuevamente a cualquier pieza cuando la necesita.

28. DIFERENCIA ENTRE "RECORDAR" Y "PODER PROCESAR"

Este es un principio que conviene congelar en la arquitectura:

MEMORY ≠ CONTEXT WINDOW 

y:

CONTEXT WINDOW ≠ TOTAL COGNITIVE WORKSPACE 

El Workspace total puede ser:

MEMORY + INDEX + GRAPH + ARTIFACTS + TASK STATE + CHECKPOINTS + CONTEXT PACK + CURRENT LLM WINDOW 

La ventana de la LLM es solamente el área de procesamiento activo.

29. RESULTADO FINAL DEL ORQUESTADOR DE MEMORIA/AUDITOR

Debe convertirse en:

MEMORY + RETRIEVAL + EVIDENCE + GRAPH + AUDIT + CONTEXT FABRIC + STATE HISTORY + CHECKPOINT REFERENCES + TRACEABILITY 

Y entregar al Workflow:

"ESTE ES EL CONTEXTO MÍNIMO, RELEVANTE, VERIFICADO, TRAZABLE Y SUFICIENTE PARA EJECUTAR LA SIGUIENTE UNIDAD." 

Ese es el punto donde tu idea deja de ser simplemente "darle memoria a una LLM pequeña" y pasa a convertirse en un sistema externo de memoria cognitiva + ejecución incremental + consolidación verificable.



**Versión:** 1.0 — Fusión final de 4 fuentes documentales (Auditoría 14 pasadas, Fusión Kernel/Plugins, Auditoría de Repos Externos, Sistema C01–C08 Resource Brain)
**Principio rector:** 90% código determinista / 10% LLM ("Compiled AI")
**Propósito de este documento:** que **cualquier IA** (Claude, GPT, Kimi, DeepSeek, etc.) pueda leerlo y derivar un plan de programación completo y coherente, sin ambigüedad, sin alucinar componentes que no estén aquí descritos.

---

## 0. Cómo usar este documento (instrucciones para la IA constructora)

1. Este documento es la **única fuente de verdad**. No inventes componentes, nombres de archivo, ni capacidades que no aparezcan aquí.
2. Sigue el orden de capas de la sección 2 (Kernel → Plugins → MCP → Memoria → Resource Brain → UI → Deploy). **Nunca** empieces por la UI o el deploy.
3. Respeta la regla de oro: **el kernel nunca se modifica** para añadir funcionalidad nueva; todo se extiende vía plugins, workflows JSON o registries.
4. Todo componente de "razonamiento" (LLM) debe ser aislable y sustituible — nunca debe estar en el *path* crítico de persistencia, auditoría o enrutamiento.
5. Antes de escribir código, verifica en qué **estado de recurso** (sección 5.3) se encuentra cada dependencia. Solo se ejecuta contra recursos `AVAILABLE`.
6. Si falta información para una decisión, no la inventes: márcala como `GAP` y continúa (ver sección 9).

---

## 1. Resumen Ejecutivo

El **Osquestador Auditor con Memoria** es un sistema operativo para agentes de IA que orquesta la ingesta, auditoría, construcción de conocimiento (árbol/grafo) y generación de tareas de un conjunto de proyectos documentales o de código. Se compone de:

- Un **kernel minimalista** (~500–900 LOC) agnóstico de plugins, que descubre dinámicamente inputs, agentes, outputs y workflows declarativos en JSON.
- Una **capa de plugins intercambiables** (12 identificados) para entradas, salidas y agentes de procesamiento.
- Un **servidor MCP** (JSON-RPC 2.0) como interfaz estándar hacia cualquier agente externo (TEAM, Mavis, OpenClaw, Claude Code, etc.).
- Una **memoria tripartita** (HOT/WARM/COLD) con búsqueda híbrida BM25+vectorial y, opcionalmente, una capa de memoria cognitiva avanzada (Tencent Memory L0–L3, Attestor, GrayMatter) con replay bi-temporal auditable.
- Un **Resource Brain (C01–C08)** que gobierna qué recursos existen, están sanos y autorizados antes de que el orquestador los use.
- Un **sistema de refutación y consenso** (4 refutaciones deterministas + Ask Council de 12 pasos) que evita que el LLM "mienta" sobre el estado de una tarea.
- Una **UI** de panel único (estética Claude/Anthropic) y un **despliegue** productivo (systemd + watchdog + backups + túnel).

**Regla 90/10:** todo lo que puede resolverse con código determinista (orquestación, persistencia, hashing, similitud, validación de estructura, enrutamiento, estado, auditoría, backup) se resuelve con código. El LLM se reserva para: planificación de tareas complejas, redacción de resúmenes, consenso multi-modelo (Ask Council) y auto-etiquetado de baja confianza.

---

## 2. Arquitectura Unificada — Vista de Capas

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                         AGENTES EXTERNOS (MCP Clients)                            │
│   TEAM YAIWES · MAVIS M3 · OpenClaw · Claude Code · NCT · cualquier cliente MCP  │
└───────────────────────────────────────────────────────────────────────────────────┘
                                      │  MCP JSON-RPC 2.0 (:8765)
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│  MCP SERVER                                                                       │
│  Tools: search_project, get_doc, list_conflicts, queue_doc, create_task,         │
│         list_tasks, move_task, list_projects, create_project, health,            │
│         kernel_status                                                            │
│  Cliente MCP (stdio/HTTP) → servicios externos (Kanboard, Graphiti, Telegram)    │
└───────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│  RESOURCE BRAIN (C01–C08) — Gobierno de recursos, previo a toda ejecución         │
│  descubre → registra → mapea → verifica → selecciona → prepara → carga → ejecuta │
│  (detalle completo en sección 5)                                                  │
└───────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│  KERNEL (~500–900 LOC, Python 3.11+, 100% código, 0% LLM)                        │
│  - pump() → loop principal                                                       │
│  - Registry → descubre plugins por carpeta+manifest (hot-reload)                │
│  - AgentManager → capability → cadena de agentes con fallback                    │
│  - OutputManager → capability → conector de salida                              │
│  - Motor → intérprete de workflows JSON declarativos                            │
│  - Commands → /estado /conflictos /resolver /frontera /handoff                  │
│  - State → atomic_write_json + SQLite WAL (inventory, conflictos, tareas,       │
│    journal, kv)                                                                  │
│  - contracts.py (InputAdapter / OutputConnector / AgentAdapter)                 │
│  - resilience.py (CircuitBreaker, backoff, health.json)                         │
└───────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│  PLUGINS (12) — inputs / outputs / agents (detalle sección 4)                    │
│  INPUTS: inbox, telegram                                                         │
│  OUTPUTS: obsidian, kanboard, graphiti, handoff, telegram_notify                 │
│  AGENTS: ocr, persistir, auditor(haystack), arbolista, plandex, hermes, swe     │
└───────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│  MEMORIA PERSISTENTE (3 niveles + capa cognitiva opcional)                        │
│  HOT   → RAM + state.db WAL (<500 tokens, contexto inmediato)                    │
│  WARM  → SQLite FTS5 (BM25) + FAISS MiniLM-L6-v2 (1–3K facts, TTL 90 días)      │
│  COLD  → Vault markdown + frontmatter + wikilinks + Git (indefinido)             │
│  COGNITIVA (opcional) → Tencent Memory L0–L3 / Attestor / GrayMatter            │
│    · Replay bi-temporal, ledger inmutable, 0% LLM en path crítico               │
└───────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│  CAPA DE VALIDACIÓN Y CONSENSO (donde vive el 10% LLM)                           │
│  4 Refutaciones deterministas · Ask Council (12 pasos, multi-LLM) ·             │
│  4 Paneles de Expertos (Planificación / Auditoría / Memoria / Verificación)      │
│  5 Simulaciones de estrés (detalle sección 6)                                    │
└───────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│  UI — Panel único (HTML estático, ~45KB, estética Claude/Anthropic, iOS HIG)      │
│  Sidebar · Header · Main (Dashboard/Artefactos/Chat/API) · Right panel           │
│  (Memoria/Documentos/Tareas/Logs) · Status bar · window.osquestador (7 fn)       │
└───────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│  DESPLIEGUE (systemd + watchdog + backup + túnel)                                │
│  systemd Type=notify · WatchdogSec=30s · restic cada 6h a S3 · cloudflared      │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Stack Tecnológico de Referencia

| Capa | Tecnología | Función |
|---|---|---|
| Lenguaje kernel | Python 3.11+ | Async nativo, ecosistema rico |
| Protocolo agentes | MCP (mcp-sdk oficial) | Estándar cross-client Anthropic |
| Vector store | FAISS MiniLM-L6-v2 (384-dim) | Búsqueda semántica liviana |
| Texto completo | SQLite FTS5 (BM25) | Built-in, sin dependencias externas |
| LLM routing | LiteLLM (multi-provider: Anthropic, OpenAI, Groq, Cerebras, NVIDIA) | Abstracción de proveedor |
| Web framework | FastAPI | Async, OpenAPI automático |
| Orquestación durable | Temporal / Hatchet (Postgres-only, `SELECT FOR UPDATE SKIP LOCKED`) | Durabilidad de workflows largos |
| Background/producción | systemd `Type=notify` + `WatchdogSec=30s` | Auto-recovery en Linux |
| Backup | restic + almacenamiento S3-compatible | Incremental, cifrado |
| Frontend | HTML estático, sin framework pesado | Ligereza y control |
| Deploy | Cloudflare Pages + VPS puente | Costo cero + control total |
| Túnel | cloudflared (trycloudflare) | Bridge efímero VPS→público |
| Memoria avanzada (opcional) | Tencent Memory Cognitive Engine (L0–L3) | Memoria cognitiva por capas |
| Memoria auditable (opcional) | Attestor (Python/MCP) | Recuperación determinista, replay bi-temporal, ~200 tokens planos |
| Memoria de bajo consumo (opcional) | GrayMatter (Go/MCP) | -90% consumo de tokens, zero-dependency |
| Grafo de conocimiento | Graphiti/Graphify (Neo4j opcional o grafo local JSON) | Entidades y relaciones |
| OCR | PaddleOCR / Tesseract / Baidu OCR | Extracción de texto de binarios |
| Base de datos relacional | Postgres + pgvector (para escala) o SQLite WAL (para MVP) | Persistencia estructurada |
| Cache/estado corto plazo | Redis (opcional, ver `app-service-agent-memory`) | Memoria dual corto/largo plazo |

---

## 4. Capa de Plugins (12) — Contratos y Función

Todos los plugins implementan uno de tres contratos definidos en `base/contracts.py`: `InputAdapter`, `OutputConnector`, `AgentAdapter`. El kernel los descubre por convención de carpeta + `manifest.json`, **nunca se registran a mano en el kernel**.

### 4.1 Inputs

| Plugin | Función |
|---|---|
| `inbox` | Escanea `inbox/<proyecto>/` en filesystem, produce `Document`, mueve a `archive/` tras `ack()` |
| `telegram` | Polling `getUpdates` con offset persistente en KV; comandos `/` se enrutan a Commands, texto libre se materializa como nota en `inbox/<proyecto>/` |

### 4.2 Outputs (capability → conector)

| Plugin | Capability | Función |
|---|---|---|
| `obsidian` | `vault` | Persiste markdown en vault del proyecto |
| `kanboard` | `taskboard` | Crea tareas vía RPC remoto, con fallback local en SQLite si falla |
| `graphiti` | `graph` | Bulk edges a grafo local JSON + remoto MCP si disponible |
| `handoff` | `handoff` | Exporta paquete `handoff.json` (docs + tareas + conflictos + flag `frontera_ok`) para la Fase 1 |
| `telegram_notify` | `notify` | Envío de notificaciones al chat configurado |

### 4.3 Agents (capability → cadena de agentes con fallback)

| Plugin | Capability | Función |
|---|---|---|
| `ocr` | `ocr` | Si el archivo es texto plano lo lee directo; si es binario, invoca motor OCR (Paddle/Tesseract) |
| `persistir` | `persistir` | Hash SHA256 → si ya existe en `inventory`, no duplica; si no, escribe en vault con frontmatter y registra |
| `haystack` | `similitud` | Similitud Jaccard sobre 5-shingles (determinista, sin LLM) |
| `auditor` | `auditoria` | Compara contra corpus del proyecto: ≥0.98 = duplicado, 0.70–0.98 = conflicto (crea ticket), <0.70 = único |
| `arbolista` | `arbol` | Extrae objetivos/decisiones/URLs por regex y genera `edges` para el grafo |
| `plandex` | `planificar` | Detecta objetivos sin tarea asociada y crea tarea `DEFINIR` (constraint `UNIQUE` evita duplicados) |
| `hermes` | `documentar` | Consolida `README_RAIZ.md` con listado de documentos y tabla de tareas |
| `swe` | `frontera` | Verifica condición de cierre: 0 conflictos abiertos, 0 pendientes, ≥1 documento — devuelve `frontera_ok` |

**Regla de extensión:** para añadir un plugin nuevo, se crea la carpeta con `manifest.json` + `adapter.py` implementando el contrato correspondiente. El kernel lo detecta en caliente. Nunca se toca el kernel.

---

## 5. Resource Brain (C01–C08) — Gobierno de Recursos

Esta capa se ejecuta **antes** de que el kernel invoque cualquier agente o conector. Su función es evitar que el sistema use un recurso que no está realmente disponible ("mentiras de disponibilidad").

### 5.1 Los 8 componentes

| Código | Nombre | Función | Flujo |
|---|---|---|---|
| C01 | Controller Registry | Registro determinista de controladores y orden de inicialización (5 niveles) | `descubre → REGISTRA` |
| C02 | AgentDB Tools Bridge | Traduce peticiones de alto nivel a operaciones concretas sobre backends de memoria | `registra → MAPEA` |
| C03 | Plugin/MCP Discovery Registry | Escanea y registra plugins/capacidades disponibles, valida firmas | `descubre → REGISTRA → mapea` |
| C04 | Capability Selection Guidance | "Cerebro" que recomienda qué recurso usar para una tarea dada (`guidance_brain`) | `mapea → verifica → SELECCIONA` |
| C05 | Resource Map | Inventario completo de módulos, dependencias y relaciones del sistema | `descubre → MAPEA → verifica` |
| C06 | Preload Resource Loading | Precarga y predicción de recursos que se necesitarán (cache warming) | `selecciona → PREPARA → carga` |
| C07 | Unified Lazy Loading Bridge | Carga bajo demanda, singleton TOCTOU-safe, degradación graceful | `prepara → CARGA → ejecuta` |
| C08 | Capability Health & Resource Status | Verifica el estado operativo real antes de autorizar uso | `mapea → VERIFICA → selecciona` |

### 5.2 Flujo integrado

```
DESCUBRE  → C03 (Plugin Discovery) + C05 (Resource Map)
REGISTRA  → C01 (Controller Registry) + C03 (Plugin Registry)
MAPEA     → C02 (AgentDB Bridge) + C05 (Resource Map)
VERIFICA  → C08 (Health/Capability Status)
SELECCIONA→ C04 (guidance_brain, solo recursos AVAILABLE)
PREPARA   → C06 (Preload / Predictive)
CARGA     → C07 (Lazy Loading Bridge)
EJECUTA   → Orquestador / Auditor de Memoria / Router
```

### 5.3 Estados de recurso (principio de separación crítico)

```
DISCOVERED → REGISTERED → CONFIGURED → REACHABLE → HEALTHY → AUTHORIZED → AVAILABLE
```

| Estado | ¿Ejecutable? |
|---|---|
| DISCOVERED / REGISTERED / CONFIGURED / REACHABLE / HEALTHY / AUTHORIZED | ❌ No |
| **AVAILABLE** | ✅ Sí |
| DEGRADED | ⚠️ Solo con política explícita de fallback |
| UNAVAILABLE | ❌ No |

**Regla dura:** `REGISTERED ≠ AVAILABLE ≠ HEALTHY ≠ AUTHORIZED`. El orquestador **solo** actúa sobre recursos en estado `AVAILABLE`.

### 5.4 Asignación por proyecto

| Proyecto | Rol | Componentes que usa |
|---|---|---|
| Orquestador principal | Orquestación general | C01, C02, C03, C04, C06, C07, C08 |
| Auditor de Memoria | Auditoría de memoria | C01, C02, C04, C05, C08 |
| Agente TEAM | Ejecución de agente | C02, C04 (indirecto vía orquestador) |
| Router Inteligente | Enrutamiento | C03, C04, C06, C08 |

---

## 6. Workflows Declarativos (4) — Motor de Ejecución

Los workflows viven como JSON en `workflows/*.workflow.json` y son interpretados por el `Motor` del kernel. **Nunca se codifican en Python directamente** — esto permite que cualquier IA los edite sin tocar el núcleo.

### 6.1 INGESTA (`document.new`)
1. Hash SHA256 → verificar en `inventory` (idempotencia)
2. OCR si es imagen/PDF
3. Clasificar proyecto
4. Persistir en vault con frontmatter (origen, hash, fecha)
5. Registrar en SQLite con estado `ingresado`
6. Si falla OCR → notificación, no bloquea el pipeline (`on_error: continue`)

### 6.2 AUDITORÍA (`document.audit`)
1. `haystack` calcula similitud Jaccard contra el corpus del proyecto
2. similitud ≥ 0.98 → duplicado → se archiva, no pasa al árbol
3. 0.70 ≤ similitud < 0.98 → conflicto → tarjeta en Kanboard + notificación
4. similitud < 0.70 → único → estado `auditado`
5. **Nunca se fusiona automáticamente** — siempre requiere decisión humana vía `/resolver`

### 6.3 ÁRBOL DEL PROYECTO (`document.tree`)
1. `arbolista` extrae objetivos, decisiones, tareas y URLs
2. `graphiti` (o grafo local) crea entidades y relaciones (`pertenece_a`, `define_objetivo`, etc.)
3. Objetivo sin tarea asociada → se crea tarea `DEFINIR`
4. `hermes` actualiza `README_RAIZ.md`

### 6.4 TASK INDEX (`project.taskindex`)
1. `plandex` genera tareas con Task DNA (uuid, prioridad, dependencias, agente recomendado, criterio de aceptación)
2. `kanboard` crea las tareas
3. `hermes` consolida el README con tabla de tareas
4. `swe` verifica frontera (0 conflictos, 0 pendientes, todo en árbol)
5. `handoff` exporta el paquete final para la fase siguiente

---

## 7. Capa de Validación y Consenso (el 10% LLM vive aquí)

### 7.1 Las 4 Refutaciones (deterministas — 0% LLM)
1. **Por hash** — documento ya en `inventory` → se salta (idempotencia)
2. **Por similitud** — contenido >98% igual a otro → se archiva, no pasa a árbol
3. **De conflicto no resuelto** — no se avanza a `taskindex` si hay conflictos abiertos
4. **De frontera** — antes de exportar `handoff`, verificar que todos los documentos estén en el árbol y no haya pendientes

*(Variante ampliada de otra fuente: validación de AST, verificación de tipos, checks de seguridad tipo OWASP — aplicable cuando el sistema procesa código en vez de documentos.)*

### 7.2 Ask Council — 12 pasos (multi-LLM, consenso)
1. Recibir solicitud de planificación
2. Consultar modelo A (p. ej. Claude)
3. Consultar modelo B (p. ej. GPT)
4. Consultar modelo C (p. ej. Groq)
5. Consultar modelo D (p. ej. Cerebras)
6. Consultar modelo E (p. ej. NVIDIA/otro)
7. Recopilar respuestas
8. Normalizar formato de salida
9. Detectar consenso (mayoría)
10. Si no hay consenso → segunda ronda con más contexto
11. Generar propuesta final
12. Registrar en journal (auditable)

**Regla:** el voto y la integración de resultados son código; solo la generación de cada respuesta individual es LLM.

### 7.3 4 Paneles de Expertos
| Panel | Agentes | Función |
|---|---|---|
| Planificación | `plandex` + `hermes` | Descompone objetivos en tareas y documenta |
| Auditoría | `haystack` + `auditor` | Detecta duplicados, versiones, conflictos |
| Memoria | `graphiti` + `arbolista` | Construye grafo de conocimiento y relaciones |
| Verificación | `swe` + `handoff` | Valida frontera y prepara el paquete de salida |

### 7.4 5 Simulaciones de estrés obligatorias antes de certificar
1. **Alta carga** — 50 documentos simultáneos, verificar cola sin pérdida de datos
2. **Fallo de agente** — OCR falla → fallback a motor secundario, registro en dead-letter
3. **Conflicto** — dos versiones del mismo documento → tarjeta + notificación
4. **Recuperación tras `kill -9`** — el estado se reconstruye desde SQLite + JSON atómicos
5. **Despliegue en VPS** — caída de túnel/proceso → recuperación automática en ≤30s vía watchdog

### 7.5 12 Goals de Entrada → 12 Goals de Salida (contrato de E/S del sistema)

| # | Entrada | Salida |
|---|---|---|
| 1 | Documento nuevo (cualquier formato) | Hash SHA256 + registro en inventory |
| 2 | Imagen/PDF escaneado | Texto extraído por OCR |
| 3 | Documento duplicado | Archivado, no procesado |
| 4 | Versión distinta de un doc existente | Conflicto detectado + tarjeta |
| 5 | Documento único | Estado `auditado`, pasa a árbol |
| 6 | Conflicto resuelto por el usuario (A/B/Fusión) | Actualización de estado + re-ingesta del ganador |
| 7 | Proyecto sin tareas definidas | Tareas `DEFINIR` creadas |
| 8 | Árbol de proyecto completo | `README_RAIZ.md` actualizado |
| 9 | Frontera lista (0 conflictos, todo procesado) | Paquete `handoff` exportado |
| 10 | Comando de usuario (`/estado`, `/conflictos`...) | Respuesta en Telegram/UI |
| 11 | Solicitud de búsqueda (MCP) | Resultados híbridos BM25+FAISS |
| 12 | Solicitud de creación de proyecto | Estructura de carpetas + repo de memoria |

---

## 8. Memoria — Diseño Detallado

### 8.1 Los 3 niveles base
| Nivel | Tecnología | Capacidad | Retención |
|---|---|---|---|
| HOT | RAM + `state.db` WAL | <500 tokens | Sesión actual |
| WARM | SQLite FTS5 (BM25) + FAISS MiniLM-L6-v2 | 1–3K facts | TTL 90 días |
| COLD | Vault markdown + frontmatter + wikilinks + Git | Ilimitado | Indefinida |

### 8.2 Capa cognitiva opcional (para escalar más allá del MVP)
- **Tencent Memory Cognitive Engine**: memoria por capas L0→L1→L2→L3, como microservicio con `MemoryProvider` interface + Resource Registry + Memory Auditor propio.
- **Attestor**: memoria auditable con recuperación determinista (0% LLM en path crítico), replay bi-temporal, reduce tokens de O(n²) a ~200 planos.
- **GrayMatter**: servidor MCP zero-dependency en Go, -90% consumo de tokens.
- **agent-memory / app-service-agent-memory**: memoria dual corto plazo (Redis) + largo plazo (Postgres+pgvector o Cosmos DB), con modo fake determinista para testing.

### 8.3 Estructura de almacenamiento (filesystem-first)
```
~/.osquestador/proyectos/<id>/
 ├─ vault/       (markdown + frontmatter + wikilinks)
 ├─ db/          (warm.sqlite, checkpoints.db, faiss/)
 ├─ .env         (excluido de backup)
 ├─ AGENTS.md    (constitución del proyecto)
 └─ .git/        (sincroniza con osquestador-memoria)
```

---

## 9. Regla 90/10 — Tabla de Reparto Código/LLM

| Componente | % Código | % LLM | Descripción |
|---|---|---|---|
| Kernel (pump, registry, managers, motor) | 100 | 0 | Orquestación, descubrimiento, ejecución de workflows |
| Persistencia (SQLite, atomic_write_json) | 100 | 0 | Almacenamiento y recuperación de estado |
| Auditoría (duplicados/versiones) | 100 | 0 | Similitud Jaccard, reglas deterministas |
| Extracción de entidades (arbolista) | 100 | 0 | Regex y parseo de markdown |
| Búsqueda híbrida (BM25+FAISS) | 100 | 0 | SQLite FTS5 + FAISS, fusión RRF |
| Comandos de usuario | 100 | 0 | `/estado`, `/resolver`, etc. |
| Resource Brain (C01–C08) | 100 | 0 | Descubrimiento, verificación, carga de recursos |
| 4 Refutaciones deterministas | 100 | 0 | Validación dura antes de aceptar salida |
| Generación de tareas (`plandex`) | 50 | 50 | LLM propone, código estructura y valida |
| Consolidación de README (`hermes`) | 50 | 50 | LLM redacta, código formatea |
| Auto-etiquetado | 90 | 10 | Solo si confianza <0.7 se usa LLM; resto zero-shot con MiniLM |
| Planificación avanzada (Ask Council) | 80 | 20 | Consulta a múltiples LLMs; voto e integración son código |

**Total agregado: ~90% código determinista / ~10% LLM.**

---

## 10. Plan de Programación — Orden de Construcción (para cualquier IA)

> Sigue este orden estrictamente. No saltar pasos ni empezar por UI/deploy.

1. **Contratos base** (`base/contracts.py`): definir `InputAdapter`, `OutputConnector`, `AgentAdapter` como interfaces abstractas.
2. **Resiliencia** (`base/resilience.py`): `CircuitBreaker`, backoff exponencial, `atomic_write_json`, `health.json`.
3. **Store** (`store/db.py`): SQLite en modo WAL — tablas `inventory`, `conflictos`, `tareas`, `journal`, `kv`.
4. **Kernel mínimo** (`kernel/*.py`): `pump()` loop, `Registry` (descubrimiento por carpeta+manifest), `AgentManager`, `OutputManager`, `Motor` (intérprete de JSON), `Commands`.
5. **Cadena determinista núcleo**: implementar y probar Harness→Sandbox→Validator→Sheriff→Adapter de salida antes de tocar nada de LLM.
6. **Workflow INGESTA** (sección 6.1) end-to-end con al menos un input (`inbox`) y un output (`obsidian`).
7. **Workflow AUDITORÍA** (sección 6.2): agente `haystack`+`auditor`, umbrales 0.70/0.98.
8. **Plugins restantes**: completar los 12 según sección 4, cada uno aislado y testeable por separado.
9. **Resource Brain (C01–C08)**: implementar antes de exponer MCP — sin esto, el orquestador no debe ejecutar nada externo.
10. **MCP Server**: exponer las tools solo sobre recursos ya gobernados por el Resource Brain.
11. **Memoria**: primero HOT+WARM (SQLite FTS5+FAISS); COLD (vault+Git) en paralelo; capa cognitiva avanzada (Tencent/Attestor/GrayMatter) es una fase posterior, opcional, no bloqueante.
12. **Workflow ÁRBOL** y **Workflow TASK INDEX** (secciones 6.3–6.4).
13. **Capa de validación y consenso**: 4 refutaciones primero (código puro), luego Ask Council (agrega LLM) — nunca al revés.
14. **5 simulaciones de estrés** (sección 7.4) — condición de certificación antes de UI/deploy.
15. **UI** (panel único, estética Claude/Anthropic).
16. **Despliegue**: systemd + watchdog + restic + cloudflared, solo al final.

**Regla de extensión permanente:** nuevo input → carpeta en `inputs/`; nuevo agente → carpeta en `agents/` + entrada en `registries/capability.json`; nuevo output → carpeta en `outputs/`; nuevo workflow → JSON en `workflows/`; nuevo comando → rama en `kernel/commands.py`; nuevo LLM → sección `providers` en `config.json` vía LiteLLM. **El kernel no se toca nunca para esto.**

---

## 11. Gaps Confirmados (pendientes explícitos — no alucinar soluciones)

1. **Detector de alucinaciones**: validar afirmaciones de un agente contra fuentes antes de aceptarlas — no existe implementación todavía.
2. **Integración real de plugins**: adaptadores escritos pero no probados contra servicios reales (Kanboard, Graphiti, Obsidian, Telegram).
3. **Credenciales**: `config.json` sin llenar con credenciales reales.
4. **Workflows ÁRBOL y TASK INDEX**: especificados, implementación parcial.
5. **MCP server**: código de referencia existe, no integrado ni probado end-to-end.
6. **Deploy y backup**: pendientes de ejecución en VPS real.
7. **Decisión abierta**: OCR "Baidu" — confirmar si es Baidu OCR API o motor equivalente.
8. **Decisión abierta**: si la capa de memoria cognitiva avanzada (Tencent/Attestor/GrayMatter) se integra como microservicio separado o como agente más dentro del kernel existente.

---

## 12. Conclusión

Este documento consolida en una sola arquitectura coherente: (a) el kernel + 12 plugins + MCP + memoria tripartita de la auditoría de 14 pasadas, (b) el sistema de refutación/consenso/simulaciones de la auditoría de repos externos, y (c) el Resource Brain de 8 componentes que gobierna qué recursos pueden usarse. El sistema completo es ejecutable siguiendo el orden de la sección 10, mantiene la proporción 90% código / 10% LLM en cada componente (sección 9), y no requiere que ninguna IA constructora invente piezas fuera de lo aquí descrito — cualquier vacío está listado explícitamente en la sección 11.



SALIDA 3 — INTEGRACIÓN FINAL DEL WORKFLOW + MEMORY/AUDIT ORCHESTRATOR
Esta salida cierra las dos anteriores: define qué debe programarse en el Workflow, qué debe programarse en el Memory/Audit Orchestrator, el contrato entre ambos, el ciclo completo y las reglas que deben quedar congeladas antes de escribir código.


