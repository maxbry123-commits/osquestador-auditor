# GAP MAESTRO DEL OSQUESTADOR AUDITOR
# INPUT BLOCK DE PROGRAMACIÓN — LECTURA LITERAL OBLIGATORIA
# Consolidado de: SALIDA 1, 7, 8, 9, 10, 11 (Fables) + diseño Memory OS
# original + checklist de auditoría previo + estado real ya construido
# en este chat. Nada de lo pegado por el Director se resume ni se omite.

---

## 0. NOTA DE AUDITORÍA TÉCNICA (leer antes de programar)

Tres precisiones factuales necesarias para que esta guía sea ejecutable
de verdad — no son excusas, son correcciones de hecho:

1. **Obsidian NO es open source.** Es una app Electron de código cerrado.
   Lo que SÍ es público y auditable es: (a) el formato del vault
   (carpetas de `.md` con frontmatter YAML + wikilinks `[[...]]`,
   documentado públicamente) y (b) los plugins de la comunidad (esos sí
   son código abierto real, ej. "Relations", "Dataview", "Templater" —
   vistos en las capturas del Director). La descomposición en 11
   servicios de SALIDA 8 (Vault/Markdown/Backlinks/Canvas/Daily Notes/
   Tags/Wikilinks/Templates/Search/Metadata/Plugin Service) se construye
   contra ESE FORMATO, no contra código fuente de Obsidian que no existe
   públicamente.
2. **"Nunca decir que el sandbox no lo permite" se adopta así:** toda
   capacidad debe tener SIEMPRE una estrategia técnica concreta
   (adaptador / proceso separado / servicio en VPS / implementación
   equivalente). Lo que este documento NO hará es fingir que un servicio
   pesado (Neo4j, Kafka, Temporal) está corriendo cuando no lo está —
   eso rompería la Ley de auditoría del propio sistema (Provenance/
   Evidence Engine). Cada pieza se marca con su estado real: ✅ corriendo
   de verdad · 🔷 adaptador listo, activa con servicio real · 🔲 diseñado,
   pendiente de programar.
3. **Escala (80–500 microservicios):** se adopta como techo
   arquitectónico del sistema completo, no como entregable de una sola
   sesión. Se sigue el PLAN DE EJECUCIÓN de 4 pasos (sección 6) para que
   cada sesión de código sea verificable contra esta lista maestra.

---

## 1. JERARQUÍA DE NIVELES (arquitectura obligatoria, SALIDA 1)

```
Nivel 0 — Bootloader → Kernel → Meta Kernel → Capability Registry
Nivel 1 — Runtime, Scheduler, EventBus, SemanticBus, Checkpoint, State
Nivel 2 — Microservicios (Memory, OCR, Research, Graph, Search, Timeline,
          Compiler, Audit, Recovery, Project, Repository, Tag, Anchor,
          Classification, Planner, Council, Execution, Learning,
          Version, Cache — cada uno independiente, nunca mezclados)
Nivel 3 — Providers (Obsidian, Graphiti, Neo4j, Qdrant, OCR, GitHub,
          Claude, GPT, Gemini — NO conocen el kernel)
Nivel 4 — UI (toda la interfaz, sin lógica propia)
```

**Regla de oro repetida en SALIDA 1/8/9/11:** ningún microservicio conoce
a otro directamente. Toda comunicación pasa por EventBus/SemanticBus/
Capability Bus. Ningún Provider se acopla al Kernel — todos entran por
adaptador con contrato uniforme.

**Estado real:** Nivel 0-1 ✅ construidos (EventBus, CapabilityBus, Gate,
Dispatcher=Scheduler, CheckpointEngine). Meta Kernel explícito 🔲
pendiente (hoy el CapabilityBus cumple parte de su función pero le
faltan: descubrimiento dinámico de plugins por carpeta+manifest,
resolución de dependencias entre capacidades, verificación de
compatibilidad, control de permisos).

---

## 2. CONCEPTOS DE ARQUITECTURA FALTANTES (A–T, SALIDA 1, literal)

| # | Concepto | Función exacta pedida | Estado |
|---|---|---|---|
| A | Meta Kernel | descubre capacidades, registra microservicios, carga plugins, gestiona versiones, resuelve dependencias, verifica compatibilidad, controla permisos, administra ciclo de vida | 🔲 parcial (CapabilityBus cubre registro; falta versiones/permisos/ciclo de vida) |
| B | Universal Contract | todo microservicio implementa: init, validate, execute, checkpoint, rollback, audit, metrics, shutdown | 🔲 hoy solo existe `.resolver()` — falta el contrato de 8 métodos completo |
| C | Dependency Resolver | motor DEDICADO que construye el DAG real (no el Dispatcher) | 🔲 no construido — el Dispatcher hoy decide activación, no dependencias entre microservicios |
| D | State Manager | estado vivo: servicios activos, trabajos, colas, bloqueos, recursos, checkpoints, sesiones | 🔲 no construido — hoy el estado vive disperso en cada motor |
| E | Resource Scheduler | administra CPU/RAM/GPU/disco/red/VPS/HF/Cloudflare/límites de API | 🔲 no construido |
| F | Policy Engine | reglas obligatorias (nunca tocar GitHub directo, nunca borrar memoria, nunca saltar Council, nunca escribir sin auditoría) | 🔲 no construido — hoy son reglas de proceso, no motor ejecutable |
| G | Capability Registry | base VIVA: versión, autor, dependencias, permisos, entradas, salidas, consumo, pruebas por capacidad | 🔲 CapabilityBus hoy solo guarda nombre+descripción+prioridad |
| H | Knowledge ABI | mismo formato de intercambio venga de PDF/OCR/GitHub/Chat/API/Imagen | 🔲 parcial — KnowledgeCompiler normaliza a "bloques" pero sin ABI formal versionado |
| I | Semantic Bus | bus separado del EventBus, específico para conocimiento | 🔲 no construido — hoy todo pasa por el EventBus genérico |
| J | Artifact Runtime | artefactos como ciudadanos de primera clase, no archivos | 🔲 no construido |
| K | Capability Sandbox | aislamiento no solo DSL — también Python/Docker/Node/Rust | 🔷 parcial — LoopEngine ya aísla Python real (subprocess -I, env vacío, timeout); Docker/Node/Rust 🔲 |
| L | Planner Compiler | convierte objetivos en DAG — NO debe hacerlo el LLM | 🔲 no construido — hoy el Dispatcher usa reglas regex, no un compilador formal de planes |
| M | Cost Engine | calcula tokens/tiempo/CPU/memoria/coste ANTES de ejecutar | 🔲 no construido |
| N | Test Runtime | pruebas/benchmark/validación automática por capacidad | 🔲 no construido (hoy las pruebas son manuales por motor) |
| O | Feature Flags | activar/desactivar motores sin recompilar | 🔲 no construido |
| P | Runtime Analytics | medir rendimiento/errores/cuellos de botella | 🔷 parcial — EventBus.historial guarda eventos, falta análisis |
| Q | Plugin SDK | plugins + documentación para construirlos | 🔲 no construido — G7 bridge es ad-hoc, no un SDK formal |
| R | Data Lineage | más allá de Provenance — seguir la transformación COMPLETA | 🔷 parcial — ProvenanceEngine cubre origen, no la cadena de transformaciones |
| S | Consensus Runtime | Council como runtime independiente | 🔲 no construido — es la pieza más repetida en los 3 textos y aún no existe |
| T | Mission Lifecycle | estados: Draft→Planning→Executing→Review→Completed→Archived | 🔲 no construido — hoy una misión no tiene estados formales |

---

## 3. LISTA MAESTRA DE MICROSERVICIOS (consolidada, deduplicada,
## cruzando SALIDA 1+7+8 contra el diseño original de Memory OS)

### 3.1 Kernel
Boot Manager · Meta Kernel · Lifecycle Manager · Configuration Manager ·
Registry Manager · **Capability Registry**✅base · Plugin Loader ·
Dependency Resolver · State Manager · Health Monitor · Metrics Engine ·
Logger Engine · Policy Engine · Permission Engine

### 3.2 Runtime
Execution Runtime · Memory Runtime · Project Runtime · Research Runtime ·
**Sandbox Runtime**✅(Python real) · Artifact Runtime · Plugin Runtime

### 3.3 Comunicación
**Event Bus**✅ · Semantic Bus · Command Bus · Query Bus ·
**Capability Bus**✅ · Knowledge Bus · Notification Bus · Audit Bus

### 3.4 Planificación
Planner Engine · DSL Compiler · DAG Runtime · **Scheduler**✅(=Dispatcher) ·
Mission Scheduler · Resource Scheduler · Parallel Scheduler ·
Retry Scheduler · Timeout Scheduler · Recovery Scheduler

### 3.5 Memoria
Memory Engine · **Knowledge Compiler**✅ · Knowledge Runtime ·
**Provenance Engine**✅ · **Timeline Engine**✅ · Context Compiler ·
Context Linker · Context Package Builder✅(parcial) · Version Engine ·
**Checkpoint Engine**✅ · **Score Engine**✅ · Pattern Engine ·
Learning Engine · Compression Engine · Synchronization Engine ·
Backup Engine · Security Engine · **Memory Auditor Engine**🔷(parcial,
solo detecta duplicado/conflicto — faltan 4 de sus 6 funciones pedidas
en el diseño original: recalcular índices, verificar enlaces rotos,
medir salud de la memoria, generar recomendaciones)

### 3.6 Conocimiento
Entity Engine · Relationship Engine · **Graph Engine**✅(networkx real) ·
Semantic Engine · Vector Engine · **Search Engine**✅(FTS5 real) ·
Index Engine · **Contradiction Engine**✅ · Knowledge Fusion Engine ·
Capability Memory Engine · Experience Memory Engine · Decision Graph Engine

### 3.7 Documentos
Document Engine · **OCR Engine**✅(tesseract real) · PDF Engine ·
Markdown Engine · Knowledge Extraction Engine · Transformation Engine ·
Import Engine · Export Engine · Diff Engine

### 3.8 Proyectos
Project Engine · Mission Engine · Goal Engine · Repository Engine ·
Repository Intelligence Engine · Architecture Engine · Roadmap Engine ·
Dependency Explorer · Project DNA Engine

### 3.9 Auditoría
Audit Engine · Evidence Engine · **Classification Engine**✅ ·
Validation Engine · **Council Engine**🔲(no construido — pendiente #1) ·
Recovery Engine · Analytics Engine

### 3.10 Investigación
Research Engine · Query Compiler · Knowledge Gap Detector ·
Acquisition Planner · Parallel Collector · Evidence Validator ·
Multi Search Engine · Language Engine · Community Intelligence Engine ·
Official Source Priority · Failure Prediction Engine ·
Installation Intelligence Engine
*(bloqueo real documentado: requieren búsqueda web — se ejecuta desde
el lado del chat con `web_search`, no desde el sandbox aislado)*

### 3.11 Organización
**Tag Engine**✅ · **Anchor Engine**✅(=TagAnchor) · **Workspace
Engine**✅(=DocumentWindow) · Artifact Engine · File System Engine ·
Universal Object Engine

### 3.12 Integraciones (Providers, Nivel 3)
Provider Manager · **Obsidian Provider**✅(vault real) · **Graphiti
Provider**🔷(fallback local real + adapter Neo4j) · **OCR
Provider**✅(tesseract) · GitHub Provider · Browser Provider ·
Firecrawl Provider · LlamaIndex Provider · Haystack Provider · **Neo4j
Provider**🔷 · **Qdrant Provider**🔷 · MCP Provider · API Gateway

### 3.13 Clientes
Claude Connector · GPT Connector · Gemini Connector · OpenClaw
Connector · Hermes Connector✅(vía bridge G7) · NCT Connector ·
MiniMax Connector

### 3.14 Descomposición por producto (SALIDA 8, literal — no se resume)

**Obsidian → 11 servicios:** Vault✅ · Markdown✅ · Backlinks🔲 · Canvas🔲 ·
Daily Notes🔲 · Tags✅(vía TagAnchor) · Wikilinks🔲 · Templates🔲 · Search✅
· Metadata🔲 · Plugin Service🔲

**Graphiti → 7 servicios:** Entity🔲 · Relation✅(vía Graph) · Temporal
Graph✅(vía Timeline+Graph) · Graph Search✅ · Graph Update✅ · Graph
Merge🔲 · Graph Analytics✅(networkx: centralidad/comunidades)

**OCR → 7 servicios:** OCR✅(tesseract) · Layout🔲 · Table Detection🔲 ·
Formula Detection🔲 · Handwriting🔲 · Image Cleanup🔲 · PDF OCR🔲

**GitHub → 9 servicios:** Repository✅(adapter G2) · Release🔲 · Commit🔲
· Branch🔲 · Issue🔲 · Pull Request🔲 · Wiki🔲 · Discussion🔲 · Action🔲

---

## 4. REGLAS OBLIGATORIAS DE DESARROLLO (SALIDA 8+9+10+11, consolidadas
## sin pérdida — cada regla original queda representada)

1. **No desde cero si existe solución madura** — investigar estado del
   arte, auditar, comparar, reutilizar/adaptar/mejorar antes de escribir
2. **Capacidades, no tecnologías** — el sistema pide "OCR", no
   "Tesseract"; la implementación es intercambiable sin tocar el resto
3. **Descomposición completa** — cada proyecto se divide en TODAS sus
   capacidades, nunca solo las visibles; si tiene 80 funciones, las 80
   se listan (o se justifica por escrito cuál se descarta y por qué)
4. **Microservicio = 1 responsabilidad medible** — si hace demasiado, se
   divide
5. **Auditoría antes de implementar** — documento previo con: funciones
   encontradas, ventajas, límites, integración posible, mejoras,
   dependencias, licencia, mantenimiento activo
6. **Código reutilizable** — ningún componente acoplado exclusivamente
   al Osquestador; debe servir a otro orquestador/IA/sistema
7. **Ningún proveedor único** — si hay ≥2 implementaciones válidas, el
   sistema debe poder intercambiarlas
8. **Mejora acumulativa** — nunca sustituir si ambas implementaciones
   pueden convivir aportando valor
9. **Biblioteca permanente de capacidades** — cada auditoría deja
   registro reutilizable (algoritmos, patrones, estructuras, formatos)
10. **Comparar siempre ≥2 alternativas** — nunca la primera que aparece;
    justificar técnicamente la elección
11. **Fusionar ventajas** — si 2 proyectos aportan cosas distintas,
    combinar, no elegir uno solo
12. **Límite del entorno ≠ criterio de diseño** — documentar SIEMPRE una
    estrategia técnica (adaptador/proceso separado/servicio externo/
    implementación equivalente) antes de marcar algo como bloqueado —
    ver matiz honesto en Sección 0.2

---

## 5. MÉTODO OBLIGATORIO POR MICROSERVICIO (SALIDA 9, los 10 pasos,
## literal, en orden, nunca al revés)

```
1. Investigación completa   (open source, forks, papers, benchmarks)
2. Auditoría del software   (código, arquitectura, algoritmos, API, CLI,
                             config, eventos, docs, tests, changelog)
3. Ingeniería inversa       (entender el CÓMO y el POR QUÉ, no copiar)
4. Descomposición           (proyecto → N capacidades independientes)
5. Clasificación            (Motor/Parser/Runtime/Provider/Gateway/
                             Compiler/Indexer/Scheduler/Analyzer/
                             Transformer/Validator/Manager/Planner/
                             Watcher/Monitor/Controller/Service/Adapter/
                             Connector/Bridge/Registry)
6. Comparación               (buscar equivalentes, quedarse con lo mejor,
                             fusionar — nunca copiar 1 solo software)
7. Programación               (recién aquí se escribe código)
8. Validación                 (funcionalidad/rendimiento/consumo/
                             estabilidad/compatibilidad/reutilización)
9. Integración                 (se incorpora al Osquestador)
10. Evolución                   (re-auditar cuando aparezca algo mejor)
```

Regla transversal: **tratar cada repositorio como biblioteca de ideas**
(algoritmos/estructuras/motores/parsers/formatos/servicios/herramientas/
patrones/utilidades se evalúan uno por uno, no el proyecto como bloque).

---

## 6. PLAN DE EJECUCIÓN — 4 PASOS (literal, del mensaje del Director)

```
PASO 1 — Arquitectura y planificación (NO programar)
  Entregables: lista completa de microservicios · árbol del proyecto ·
  diagrama general · roadmap · proyectos OSS auditados · capacidades
  reutilizadas · componentes nuevos · orden exacto de implementación
  → ESTE DOCUMENTO ES PARTE DEL PASO 1

PASO 2 — Núcleo únicamente (500–1000 LOC)
  Solo: registrar microservicios · descubrir microservicios · ejecutar
  en paralelo · router de tareas · scheduler · auditoría · sentinel ·
  watchdog · health check · eventos · logging · configuración · carga
  dinámica. NADA de OCR/Graph/Memory aquí — eso es Nivel 2.
  → Estado real: el kernel actual (~900 LOC en bus.py+gate.py+
  dispatcher.py+memoryos.py) ya cumple la mayoría de esta lista, PERO
  mezcla algo de registro de motores dentro de memoryos.py que
  arquitectónicamente pertenece al Meta Kernel (sección 2.A) — requiere
  refactor menor, no reescritura

PASO 3 — Microservicios, uno por uno
  Mismo procedimiento de 10 pasos (Sección 5) para cada uno. No avanzar
  al siguiente sin validar el anterior.
  → Estado real: 20 capacidades ya construidas SIN pasar formalmente por
  los 10 pasos completos (se saltó investigación/comparación/
  clasificación formal en varias) — pendiente de auditoría retroactiva

PASO 4 — UI (solo al final, sin lógica propia)
  Debe permitir: ver microservicios · activar/detener · ver estado/
  auditoría/logs/consumo/procesos/documentos/proyectos/memoria/
  búsqueda/tareas/workflows/conexiones API/MCP · configurar servicios
  → 🔲 no iniciado
```

---

## 7. MAPEO HONESTO: DÓNDE ESTAMOS REALMENTE HOY

- **Paso 1 (arquitectura):** completado recién con este documento
- **Paso 2 (núcleo):** ~80% — falta separar formalmente el Meta Kernel
  (2.A) del resto, y añadir Universal Contract (2.B) a cada motor
- **Paso 3 (microservicios):** 20 construidos de forma real y probada,
  pero DE LOS ~140 nombrados en la lista maestra (sección 3) — sin
  seguir el procedimiento de 10 pasos completo en todos
- **Paso 4 (UI):** no iniciado
- **Pieza más repetida en los 3 textos y aún sin construir:** el
  **Council** (Consensus Runtime) — validación obligatoria antes/después
  de cada fase, mencionado en SALIDA original, SALIDA 1(S), y SALIDA 7 —
  es el siguiente candidato lógico de mayor prioridad
