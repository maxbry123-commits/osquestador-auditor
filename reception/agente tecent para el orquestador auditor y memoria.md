Sistema de mejora con tecent para el orquestador agente de memoria y auditor 

Sí. Con esa arquitectura, no convertiría Tencent Memory en el kernel de TEAM. Lo convertiría en un módulo interno del orquestador de memoria, expuesto hacia TEAM mediante MCP.

La idea correcta sería:

TEAM AGENT
                        │
                        │ MCP
                        ▼
              ┌─────────────────────┐
              │ MEMORY ORCHESTRATOR │
              │                     │
              │  MCP Server         │
              │  Memory Router      │
              │  Policy/Auditor     │
              │  Resource Manager   │
              └──────────┬──────────┘
                         │
          ┌──────────────┼────────────────┐
          ▼              ▼                ▼
      Tencent         Graphiti          Graphify
      Memory          / Graph            / Graph
          │              │                │
          ├──────────────┤                │
          ▼              ▼                ▼
       L0-L3         Temporal/Graph    OCR / Knowledge
       Memory           Memory             │
          │              │                 │
          └──────────────┼─────────────────┘
                         ▼
                  Unified Memory
                         │
                         ▼
                  HNSW / BM25 / RRF
                         │
                         ▼
                  Context Builder
                         │
                         ▼
                    TEAM Agent

1. La función de Tencent dentro de tu sistema

Yo le daría a Tencent una responsabilidad muy concreta:

> gestionar la memoria cognitiva derivada de las interacciones y convertir experiencias en memoria reutilizable.



No le permitiría controlar todo el almacenamiento.

Quedaría:

Tencent Memory
        │
        ├── Conversation Memory
        ├── Atomic Memory
        ├── Scenario Memory
        ├── Core Memory
        ├── Skills
        └── Memory Assets

Mientras que Graphiti/Graphify podrían encargarse principalmente de:

Graph Layer
    │
    ├── entities
    ├── relationships
    ├── temporal facts
    ├── events
    └── provenance

Y OCR:

OCR Layer
    │
    ├── images
    ├── documents
    ├── scanned PDFs
    └── extracted text

El orquestador decide cuándo utilizar cada uno.


---

2. El punto fundamental: no instalar los programas

Esto coincide con lo que estás buscando.

El usuario debería ver solamente:

TEAM
 +
Memory Orchestrator

No:

TEAM
├── Graphiti
├── Graphify
├── Tencent Memory
├── OCR
├── HNSW
├── BM25
├── ...

El usuario instala tu Memory Orchestrator.

Internamente:

Memory Orchestrator
├── Tencent adapter
├── Graph adapter
├── OCR adapter
├── Vector adapter
├── Search adapter
└── MCP server

Los componentes pueden ser implementaciones internas, librerías embebidas o servicios opcionales.


---

3. Yo lo diseñaría como un "Memory Operating Layer"

No como una base de datos.

MEMORY ORCHESTRATOR
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     INGEST          STORE         RETRIEVE
        │              │              │
        ▼              ▼              ▼
     OCR/API       Graph/Vector    Hybrid Search
        │              │              │
        └──────────────┼──────────────┘
                       │
                    AUDITOR
                       │
                    POLICY
                       │
                  MCP SERVER
                       │
                       ▼
                    AGENTS

Eso te permite cambiar componentes posteriormente sin cambiar TEAM.


---

4. La interfaz que debe conocer TEAM

TEAM no debería saber que existe Tencent.

TEAM solamente debería conocer MCP:

memory.search
memory.store
memory.update
memory.forget
memory.get
memory.timeline
memory.related
memory.skills
memory.context
memory.audit

Por ejemplo:

TEAM
 │
 │ memory.context(
 │   task="modificar módulo X"
 │ )
 ▼
Memory Orchestrator

El orquestador decide:

¿Necesito?

Graphiti       → relaciones temporales
Tencent        → memoria cognitiva
OCR            → documentos/imágenes
HNSW           → similitud
BM25           → coincidencia textual
RRF            → fusionar resultados
CodeGraph      → relaciones de código

TEAM recibe solamente:

Context Package


---

5. Aquí está la parte realmente importante

Yo introduciría un Memory Resource Graph.

Cada recurso que entra al sistema obtiene una identidad:

{
  "resource_id": "mem_01...",
  "type": "memory",
  "source": "tencent",
  "layer": "L1",
  "scope": "project",
  "agent": "team",
  "created_at": "...",
  "updated_at": "...",
  "provenance": [],
  "confidence": 0.94,
  "version": 3
}

Pero un documento OCR tendría:

{
  "resource_id": "doc_01...",
  "type": "document",
  "source": "ocr",
  "provenance": []
}

Y una relación Graphiti:

{
  "resource_id": "edge_01...",
  "type": "temporal_relation",
  "source": "graphiti"
}

El orquestador unifica la identidad, no necesariamente los formatos internos.


---

6. Tencent funcionaría como "Memory Cognitive Engine"

Yo lo aislaría así:

memory/
│
├── orchestrator/
│
├── cognitive/
│   └── tencent/
│       ├── l0/
│       ├── l1/
│       ├── l2/
│       ├── l3/
│       ├── skills/
│       └── assets/
│
├── graph/
│   ├── graphiti/
│   └── graphify/
│
├── vision/
│   └── ocr/
│
├── retrieval/
│   ├── hnsw/
│   ├── bm25/
│   └── rrf/
│
├── audit/
│
└── mcp/

Esto es mucho más limpio que fusionar los proyectos físicamente.


---

7. Cómo funcionaría una consulta real

Supongamos que TEAM pregunta:

> "¿Qué decidimos anteriormente sobre la arquitectura de memoria?"



El flujo sería:

TEAM
 │
 ▼
memory.context()
 │
 ▼
ORCHESTRATOR
 │
 ├── Tencent L2/L3
 │
 ├── Graphiti temporal search
 │
 ├── Graphify relationship search
 │
 ├── BM25
 │
 └── HNSW
 │
 ▼
RRF
 │
 ▼
AUDITOR
 │
 ├── duplicate?
 ├── conflict?
 ├── stale?
 ├── provenance?
 └── confidence?
 │
 ▼
CONTEXT BUILDER
 │
 ▼
TEAM

TEAM nunca tiene que saber qué backend encontró cada cosa.


---

8. El auditor es crítico

Tu idea de orquestador auditor de memoria puede ser incluso más importante que Tencent.

Porque tener cinco sistemas de memoria puede generar:

Graphiti:
"X ocurrió en enero."

Tencent:
"X ocurrió en febrero."

OCR:
"Documento dice marzo."

No quieres mandar las tres afirmaciones directamente al LLM.

El auditor debe detectar:

CONFLICT

y conservar:

claim A
claim B
source A
source B
timestamp
confidence

Entonces TEAM puede recibir:

> Existen dos registros contradictorios; el documento X es la fuente más reciente.



Eso es mucho más robusto.


---

9. MCP sería solamente la frontera

No usaría MCP como mecanismo interno entre todos los módulos.

Sería:

MCP
                   │
                   ▼
              ORCHESTRATOR
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    Tencent      Graph       OCR
        │          │          │
        └──────────┼──────────┘
                   ▼
              AUDITOR

Así puedes reemplazar Tencent mañana:

Tencent
   ↓
Otro Memory Engine

sin tocar TEAM.


---

10. Y esto permite evolución futura

Hoy:

TEAM
 ↓
Memory Orchestrator
 ↓
Tencent + Graphiti + Graphify + OCR + HNSW

Mañana:

TEAM
 ↓
Memory Orchestrator
 ↓
20 memory providers

Y después:

MEMORY ORCHESTRATOR
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
   LOCAL MODE       SERVER MODE       HYBRID
       │                │                │
       ▼                ▼                ▼
    SQLite          PostgreSQL       Local cache
    HNSW             Graph DB        + remote
    OCR              Vector DB       memory

TEAM permanece igual.

Ese es precisamente el beneficio de convertir Tencent en un provider/plugin de memoria, no en una dependencia estructural del agente.


---

Arquitectura que considero correcta para tu proyecto

┌──────────────────┐
                         │    TEAM AGENT    │
                         └────────┬─────────┘
                                  │
                              MCP API
                                  │
                                  ▼
                 ┌────────────────────────────────┐
                 │      MEMORY ORCHESTRATOR       │
                 │                                │
                 │  Router                       │
                 │  Auditor                      │
                 │  Policy                        │
                 │  Resource Registry             │
                 │  Context Builder               │
                 │  Cost/Latency Governor         │
                 └───────────────┬────────────────┘
                                 │
       ┌─────────────────────────┼─────────────────────────┐
       │                         │                         │
       ▼                         ▼                         ▼
┌──────────────┐          ┌──────────────┐         ┌──────────────┐
│ COGNITIVE    │          │ KNOWLEDGE    │         │ PERCEPTION   │
│ MEMORY       │          │ GRAPH        │         │              │
│              │          │              │         │ OCR          │
│ Tencent      │          │ Graphiti     │         │ Documents    │
│ L0-L3        │          │ Graphify     │         │ Images       │
│ Skills       │          │ CodeGraph    │         │ PDFs         │
└──────┬───────┘          └──────┬───────┘         └──────┬───────┘
       │                         │                         │
       └─────────────────────────┼─────────────────────────┘
                                 ▼
                       ┌──────────────────┐
                       │ RETRIEVAL ENGINE │
                       │                  │
                       │ HNSW             │
                       │ BM25             │
                       │ Graph            │
                       │ RRF              │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ MEMORY AUDITOR   │
                       │                  │
                       │ provenance       │
                       │ conflicts        │
                       │ confidence       │
                       │ freshness        │
                       │ deduplication     │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ CONTEXT BUILDER  │
                       └────────┬─────────┘
                                │
                                ▼
                            TEAM AGENT

Esta es la arquitectura que usaría. Tencent sería una pieza intercambiable dentro de COGNITIVE MEMORY; Graphiti/Graphify serían la capa de relaciones; OCR la capa de ingestión; HNSW/BM25/RRF la recuperación; y tu Orchestrator + Auditor sería el verdadero núcleo que mantiene todo unificado.

El siguiente paso técnico no sería programar todavía. Haría una auditoría archivo-por-archivo del repositorio actual de Tencent, específicamente para separar: qué código reutilizar, qué adaptar, qué descartar y qué exponer mediante MCP, y produciría un mapa de integración contra la estructura de tu Memory Orchestrator.


Sí. Revisé de nuevo el repositorio oficial y, esta vez, la conclusión cambia en un punto importante respecto a mi respuesta anterior: Tencent ya tiene una separación Core ↔ Gateway ↔ adapters bastante cercana a lo que tú estás diseñando. Por eso no lo trataría como una simple biblioteca dentro de tu orquestador; lo convertiría en un microservicio especializado de memoria cognitiva, detrás de tu Memory Orchestrator. 

Además, el repositorio oficial que estoy tomando como referencia es TencentCloud/TencentDB-Agent-Memory, actualmente con la rama main y release v0.3.6; hay otra ruta histórica/duplicada bajo Tencent/TencentDB-Agent-Memory, por lo que para una integración real hay que fijar el repositorio y commit exactos, no main. 

1. Qué es realmente Tencent dentro de tu arquitectura

Tu sistema debería tener dos niveles:

AGENTE TEAM
                         │
                         │ MCP
                         ▼
             ┌─────────────────────────┐
             │ MEMORY ORCHESTRATOR     │
             │                         │
             │ Router                  │
             │ Auditor                 │
             │ Policy                  │
             │ Registry                │
             │ Context Builder         │
             │ MCP Server              │
             └────────────┬────────────┘
                          │
             ┌────────────┼─────────────┐
             │            │             │
             ▼            ▼             ▼
       Tencent       Graphiti/      OCR/document
       Memory        Graphify          service
       Service         Service
             │
             ▼
       L0 → L1 → L2 → L3

El Orchestrator es el cerebro. Tencent es un especialista.

No quiero que Tencent decida qué memoria recibe TEAM. Esa decisión pertenece a tu orquestador.


---

2. Qué descubrí en el código que cambia el diseño

El repositorio tiene un TdaiCore que funciona como fachada independiente de la plataforma. La documentación de integración del propio proyecto identifica explícitamente:

src/core/tdai-core.ts → fachada de Core.

src/core/hooks/auto-recall.ts → recuperación antes del turno.

src/core/hooks/auto-capture.ts → captura después del turno.

src/utils/pipeline-manager.ts → programación de L1/L2/L3.

src/utils/pipeline-factory.ts → creación de almacenamiento, embeddings y runners.

src/gateway/server.ts → exposición HTTP.

src/adapters/standalone/host-adapter.ts → adaptación para ejecución independiente. 


Eso es exactamente la separación que necesitamos.

El Core ya tiene conceptos equivalentes a:

capture()
recall()
search()
session_end()
destroy()

y el Gateway los convierte en operaciones accesibles desde otros procesos. 

Por tanto, no debemos arrancar Tencent dentro de TEAM.


---

3. Cómo lo convertiría

Yo haría esto:

memory-platform/
│
├── orchestrator/
│
├── services/
│   │
│   ├── tencent-memory/
│   │
│   ├── graph-memory/
│   │
│   ├── ocr-memory/
│   │
│   └── retrieval/
│
├── registry/
│
├── auditor/
│
└── mcp/

Y Tencent quedaría:

services/tencent-memory/
│
├── adapter/
├── service/
├── worker/
├── storage/
└── manifest.json

No copiaría el plugin de OpenClaw.

Extraería el Core y su modelo de pipeline.


---

4. Qué función exacta tendría Tencent

Le daría cinco responsabilidades.

A. Captura

Recibir:

conversation
tool result
task result
agent event
workflow result

y convertirlos en memoria L0.


---

B. Destilación

Ejecutar la progresión:

L0 Conversation
       ↓
L1 Atom
       ↓
L2 Scenario
       ↓
L3 Persona/Core

Esta es una de las piezas centrales del proyecto Tencent. No es simplemente almacenamiento vectorial. 


---

C. Recuperación cognitiva

Cuando el Orchestrator pregunta:

recall(query)

Tencent busca en sus capas superiores y devuelve memoria estructurada.


---

D. Memoria simbólica de corto plazo

Esta es otra pieza que conservaría.

Tencent toma resultados voluminosos de herramientas, los descarga a almacenamiento externo y conserva una representación compacta mediante un canvas Mermaid con node_id, permitiendo volver al contenido original cuando hace falta. 

Para TEAM:

10 MB tool output
       ↓
Tencent
       ↓
compact symbolic state
       ↓
TEAM context

Y si TEAM necesita un detalle:

node_id
   ↓
raw evidence

Esto es especialmente útil para tu idea de auditoría.


---

5. El Orchestrator no debería duplicar la memoria de Tencent

Esta es una decisión arquitectónica importante.

No hagas:

TEAM
 ↓
Orchestrator
 ↓
guardar memoria
 ↓
Tencent
 ↓
volver a guardar memoria

Haz:

TEAM
 ↓
Orchestrator
 ↓
Tencent Memory Service
 ↓
Tencent storage

El Orchestrator guarda solamente:

resource_id
source
version
provider
provenance
audit result

Es decir, registro y gobierno, no necesariamente otra copia de todo.


---

6. Registry de recursos

Crearía un registro central:

{
  "resource_id": "mem_8f21",
  "provider": "tencent-memory",
  "type": "long_term_memory",
  "layer": "L2",
  "scope": "team",
  "agent_id": "team",
  "version": 12,
  "created_at": "2026-08-09T00:00:00Z",
  "provenance": {
    "source_event": "turn_812",
    "source_service": "team"
  },
  "status": "verified"
}

Así tu Orchestrator sabe:

qué existe
dónde está
quién lo produjo
qué versión tiene
qué agente puede utilizarlo


---

7. El flujo de escritura

Yo lo programaría así:

TEAM
 │
 │ event
 ▼
Memory Orchestrator
 │
 ├── validate
 ├── identify agent
 ├── identify session
 ├── classify resource
 └── route
       │
       ▼
Tencent Memory Service
       │
       ▼
L0
       │
       ├──────────────┐
       ▼              ▼
    L1 pipeline     raw evidence
       │
       ▼
      L2
       │
       ▼
      L3

Tencent ya implementa una lógica de pipeline para disparar extracción L1, procesamiento L2 y generación L3 con umbrales/intervalos. 

Tu Orchestrator no tiene que reconstruir esa lógica.


---

8. El flujo de lectura

Aquí es donde tu sistema mejora Tencent.

TEAM
 │
 │ "¿qué sabemos de X?"
 ▼
ORCHESTRATOR
 │
 ├── Tencent
 ├── Graphiti
 ├── Graphify
 ├── OCR
 └── otros providers
       │
       ▼
   NORMALIZER
       │
       ▼
     AUDITOR
       │
       ├── deduplicate
       ├── conflict detection
       ├── provenance
       ├── freshness
       └── confidence
       │
       ▼
   CONTEXT BUILDER
       │
       ▼
      TEAM

Aquí Tencent no devuelve directamente el prompt final.

Devuelve candidatos de memoria.

Tu Orchestrator decide cuáles sobreviven.


---

9. Esto permite que Tencent sea reemplazable

Por ejemplo:

memory.search()

puede consultar:

TencentMemoryProvider
GraphitiProvider
GraphifyProvider
OCRProvider
VectorProvider

Todos implementan:

MemoryProvider

Conceptualmente:

interface MemoryProvider {

    capture(event): Promise<MemoryReceipt>;

    recall(query): Promise<MemoryCandidate[]>;

    search(query): Promise<MemoryCandidate[]>;

    get(id): Promise<MemoryRecord>;

    delete(id): Promise<void>;

    health(): Promise<HealthStatus>;
}

Tencent implementa esa interfaz.

Graphiti implementa la misma interfaz.

OCR implementa una variante de ingestión.

TEAM no conoce ninguno de ellos.


---

10. El MCP estaría encima del Orchestrator

Esto es fundamental.

No haría:

TEAM
 ├── MCP Tencent
 ├── MCP Graphiti
 ├── MCP OCR
 └── MCP ...

Eso derrota tu objetivo.

Haría:

TEAM
 │
 ▼
ONE MCP
 │
 ▼
Memory Orchestrator
 │
 ├── Tencent
 ├── Graphiti
 ├── Graphify
 ├── OCR
 └── Retrieval

El agente ve una sola memoria.

Por ejemplo:

memory.search
memory.recall
memory.store
memory.context
memory.related
memory.timeline
memory.evidence
memory.audit


---

11. Tencent también puede funcionar como microservicio HTTP

Aquí el propio proyecto nos da una pista muy fuerte.

Su Gateway expone las operaciones de memoria por HTTP, y el proyecto ya contempla autenticación Bearer, health check y CORS. GET /health queda disponible para probes mientras las rutas protegidas pueden exigir Authorization: Bearer. 

Por tanto:

Memory Orchestrator
       │
       │ HTTP
       ▼
Tencent Memory Service
       │
       ▼
TdaiCore

Es una arquitectura natural para él.


---

12. Yo NO usaría el Gateway Tencent directamente como API pública

Lo pondría detrás de tu propio gateway:

TEAM
 │
 ▼
YOUR MCP
 │
 ▼
YOUR MEMORY ORCHESTRATOR
 │
 ├── policy
 ├── audit
 ├── routing
 ├── rate limit
 └── provenance
       │
       ▼
Tencent Gateway

Así Tencent no necesita conocer:

TEAM;

otros agentes;

Graphiti;

OCR;

tus reglas;

tu política global.



---

13. Qué conservaría del código Tencent

Después de revisar la estructura actual, mi extracción sería aproximadamente:

CONSERVAR

src/core/
    tdai-core
    hooks
    capture
    recall

src/utils/
    pipeline-manager
    pipeline-factory

storage/
    L0
    L1
    L2
    L3

embedding/
retrieval/
persona/
scene/
conversation/
record/

La nomenclatura exacta de carpetas puede cambiar entre commits, por lo que para implementar el fork fijaría primero el commit exacto y construiría el mapa contra ese snapshot. El repositorio actual es TypeScript mayoritariamente y declara Node >=22.16; también usa SQLite/sqlite-vec, Zod, tiktoken y servicios opcionales de embedding/LLM. 

NO CONSERVAR COMO PARTE DEL SERVICIO

OpenClaw plugin
OpenClaw manifest
Hermes-specific adapter
OpenClaw hooks
OpenClaw runtime patch
Tencent-specific UI

Esas piezas son adaptadores de plataforma, no el núcleo cognitivo.


---

14. HNSW no debería sustituir el motor Tencent

Aquí también corregiría nuestra arquitectura anterior.

Tencent actualmente utiliza almacenamiento local SQLite + sqlite-vec y ofrece recuperación híbrida keyword / embedding / hybrid, con RRF como estrategia recomendada. 

Yo haría:

Tencent Memory
      │
      ▼
Memory Store Interface
      │
 ┌────┴─────┐
 ▼          ▼
SQLite    HNSW
 │          │
 ▼          ▼
BM25     semantic
 │          │
 └────┬─────┘
      ▼
     RRF

Así HNSW es un backend/indexador, no el cerebro.


---

15. El verdadero valor de tu sistema aparece aquí

Tencent tiene:

L0 → L1 → L2 → L3

Tu plataforma tendría:

MEMORY ORCHESTRATOR
                            │
              ┌─────────────┼──────────────┐
              ▼             ▼              ▼
          COGNITIVE       GRAPH          PERCEPTION
          MEMORY          MEMORY          MEMORY
              │             │              │
           Tencent       Graphiti         OCR
              │          Graphify           │
              │             │              │
              └─────────────┼──────────────┘
                            ▼
                       NORMALIZATION
                            ▼
                         AUDITOR
                            ▼
                       RETRIEVAL
                            ▼
                       RANK / RRF
                            ▼
                     CONTEXT BUILDER
                            ▼
                         AGENTS

Eso convierte tu Orchestrator en una capa de memoria universal para cualquier agente, no solamente TEAM.


---

16. Un agente nuevo no necesita instalar Tencent

Esto cumple exactamente tu objetivo.

AGENTE A
   │
   └── MCP
          │
AGENTE B ─┤
          ▼
     MEMORY ORCHESTRATOR
          │
          ├── Tencent
          ├── Graphiti
          ├── OCR
          └── ...

Todos comparten el mismo sistema.

Y puedes decidir:

agent=A → memoria privada
agent=B → memoria privada
team    → memoria compartida
project → memoria compartida
global  → memoria global


---

17. Scope debería ser obligatorio

Yo añadiría al contrato:

{
  "scope": {
    "tenant": "default",
    "agent": "TEAM",
    "project": "project-x",
    "session": "session-123",
    "visibility": "team"
  }
}

Esto evita que una memoria de un agente termine accidentalmente en otro.


---

18. Y aquí entra tu Auditor

El flujo final sería:

WRITE

event
 ↓
classify
 ↓
Tencent
 ↓
memory candidate
 ↓
AUDIT
 ↓
ACCEPT / REJECT / CONFLICT
 ↓
registry

Para lectura:

QUERY
 ↓
providers
 ↓
Tencent + Graph + OCR
 ↓
normalize
 ↓
deduplicate
 ↓
conflict detection
 ↓
provenance
 ↓
rank
 ↓
budget
 ↓
context

Ese es el componente que Tencent no debe sustituir.


---

19. Cómo lo programaría por fases

No intentaría fusionar el repositorio entero.

Fase A — Tencent Adapter

TencentMemoryProvider

Implementa:

capture()
recall()
search()
get()
session_end()
health()

Fase B — Tencent Service

HTTP
 ↓
TdaiCore
 ↓
Tencent storage

Fase C — Orchestrator

Provider Registry
Memory Router
Policy
Auditor

Fase D — MCP

MCP
 ↓
Orchestrator

Fase E — TEAM

TEAM
 ↓
MCP
 ↓
Memory Orchestrator


---

Mi diseño final

┌─────────────┐
                         │    TEAM     │
                         └──────┬──────┘
                                │
                               MCP
                                │
                                ▼
                 ┌──────────────────────────┐
                 │   MEMORY ORCHESTRATOR    │
                 │                          │
                 │ Router                   │
                 │ Registry                 │
                 │ Policy                   │
                 │ Auditor                  │
                 │ Retrieval                │
                 │ Context Builder          │
                 └────────────┬─────────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
      ┌─────────────┐  ┌─────────────┐  ┌────────────┐
      │   TENCENT   │  │   GRAPH     │  │    OCR     │
      │   MEMORY    │  │   MEMORY    │  │  SERVICE   │
      │             │  │             │  │            │
      │ L0          │  │ Graphiti    │  │ Documents  │
      │ L1          │  │ Graphify    │  │ Images     │
      │ L2          │  │ CodeGraph   │  │ PDF        │
      │ L3          │  │             │  │            │
      │ Symbolic    │  │             │  │            │
      └──────┬──────┘  └──────┬──────┘  └─────┬──────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                       MEMORY AUDITOR
                              │
                     ┌────────┼────────┐
                     ▼        ▼        ▼
                   SOURCE  CONFLICT  FRESHNESS
                     │        │        │
                     └────────┼────────┘
                              ▼
                       HYBRID RETRIEVAL
                              │
                         BM25 + HNSW
                              │
                             RRF
                              │
                              ▼
                       CONTEXT BUILDER
                              │
                              ▼
                           AGENT

Veredicto

Sí: Tencent debe ser un microservicio adicional de tu plataforma, no una dependencia interna de TEAM.

Su papel sería memoria cognitiva y destilación de experiencia: captura L0, genera L1/L2/L3, mantiene memoria simbólica de corto plazo y ofrece recuperación estructurada. El Memory Orchestrator sería quien gobierna todos los proveedores, audita conflictos, controla permisos/proveniencia, combina resultados y decide qué llega a cualquier agente. El diseño del propio Tencent —Core independiente, Gateway HTTP y adapters separados— hace que esta integración sea técnicamente razonable. 

Y hay una ventaja importante: el proyecto ya contempla un Gateway independiente y adaptadores para varios agentes/frameworks, incluyendo Hermes y, en cambios recientes, integraciones mediante MCP/hooks para Codex y Claude Code. Eso demuestra que la separación que propones —memoria independiente + adaptador hacia el agente— es compatible con la arquitectura que Tencent ya está siguiendo. 

