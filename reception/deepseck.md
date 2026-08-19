Osquestador de Memoria y Auditoría — Visión General para Agentes IA (Parte 2: Estado, Módulos y Despliegue)

Este documento complementa la Parte 1 (visión general y arquitectura). Aquí se detalla el estado actual de construcción, los módulos específicos (plugins, workflows, herramientas MCP), el despliegue real y los gaps pendientes del sistema, basado en las auditorías documentadas.

---

1. Estado actual del Osquestador (post‑auditoría)

Nivel Componente Estado Evidencia
N0‑1 Kernel (core.py, motor.py, managers.py) ✅ 100% 180 LOC, atomic_write_json, SIGTERM safe, hot‑reload
 EventBus / CapabilityBus ✅ managers.py + Registry + AgentManager
 Scheduler / Dispatcher ✅ pump() loop con polling configurable
 CheckpointEngine ✅ atomic_write_json + state.db WAL
 Meta Kernel formal 🔲 Pendiente separar de memoryos.py
N2 Memory Engine ✅ SQLite FTS5 (BM25) + JSON graph
 Knowledge Compiler ✅ agents/arbolista + agents/hermes
 Provenance Engine ✅ inventory + parents + journal
 Timeline Engine 🔷 state.db ts fields, falta visualización
 Search Engine ✅ FTS5 search + conflictos queries
 Graph Engine ✅ state/graph.json (networkx opcional)
 OCR Engine ✅ Tesseract + PaddleOCR adapter
 Tag Engine ✅ TagAnchor via commands.py + DB
 Council Engine 🔲 Pendiente #1 (más repetido en 3 textos)
 Context Compiler 🔷 Parcial: hermes genera README, falta build_context
N3 Obsidian Provider ✅ Vault filesystem + markdown frontmatter
 Graphiti Provider 🔷 graphiti adapter (local JSON) + Neo4j pendiente
 OCR Provider ✅ Tesseract/PaddleOCR
 Telegram Provider ✅ Input + notify (con CircuitBreaker)
 Kanboard Provider ✅ JSON‑RPC API + local fallback
N4 UI (panel V12) ✅ 45KB HTML, 5 zonas, iOS aesthetic, 7 funciones window.osquestador

---

2. Los 12 plugins del sistema (carpetas intercambiables)

Cada plugin implementa un contrato input.v1, output.v1 o agent.v1. El kernel los descubre por manifest.json.

Plugin Tipo Función Estado
inbox input Watcher de carpeta inbox/<proyecto>/ ✅
telegram input Bot Telegram: recibe comandos y documentos ✅
telegram_notify output Envía mensajes/alertas por Telegram ✅
obsidian output Guarda docs en vault markdown + frontmatter ✅
kanboard output Crea tareas vía JSON‑RPC API ✅
graphiti output Grafo local JSON (edges) + Neo4j remoto opcional ✅
handoff output Exporta paquete Fase 0 (handoff.json + README) ✅
ocr agent Extrae texto de binarios (PaddleOCR/Tesseract) ✅
persistir agent Hash SHA256 + guarda vault + inventario ✅
haystack agent Similitud Jaccard (5‑shingles) vs corpus ✅
auditor agent Duplicado/versión/conflicto/único ✅
arbolista agent Extrae objetivos/decisiones/tareas/urls/repos ✅
plandex agent Detecta objetivos sin tarea → crea "DEFINIR" ✅
hermes agent Genera README_RAIZ.md con tabla de tareas ✅
swe agent Audita frontera: conflictos=0, pendientes=0 ✅

Regla: añadir un plugin nuevo = crear carpeta + manifest.json + adapter.py. El kernel lo detecta en el siguiente ciclo (hot‑reload).

---

3. Los 4 workflows operativos (declarativos JSON)

Cada workflow se dispara por un trigger (evento). El kernel los ejecuta paso a paso.

Workflow 1 — document.new (INGESTA)

```
trigger: documento nuevo en inbox/telegram/chat
steps:
  1. hash SHA256 (idempotencia)
  2. ocr (si binario)
  3. persistir (guarda vault + inventory)
  4. auditor (duplicado/versión/conflicto)
  5. avisar_conflicto (Telegram)
  6. tarjeta_conflicto (Kanboard)
```

Estado: ✅ implementado, smoke test verificado.

Workflow 2 — document.audit (RE‑AUDITORÍA)

```
trigger: documento re‑ingresado (post‑conflicto)
steps:
  1. auditor (re‑evalúa contra corpus)
```

Estado: ✅ implementado, usado en _recover().

Workflow 3 — document.tree (ÁRBOL)

```
trigger: documento auditado como "único"
steps:
  1. extraer (objetivos, decisiones, tareas, urls, repos)
  2. grafo (bulk_edges a Graphiti)
```

Estado: ✅ implementado, genera state/graph.json.

Workflow 4 — project.taskindex (TASK INDEX)

```
trigger: se añadió un documento al árbol
steps:
  1. planificar (detecta objetivos sin tarea → DEFINIR)
  2. documentar (genera README_RAIZ.md)
  3. guardar_raiz (vault)
  4. frontera (audita condiciones de salida)
  5. handoff (exporta paquete si frontera OK)
  6. avisar (Telegram)
```

Estado: ✅ implementado, genera handoff/<proyecto>/handoff.json.

---

4. Herramientas MCP expuestas (JSON‑RPC 2.0)

El orquestador expone un servidor MCP en 127.0.0.1:8765 con 4 tools principales:

Tool Parámetros Función
search_project proyecto Docs + tareas + conflictos del proyecto
get_doc hash Contenido íntegro del documento (vault)
list_conflicts proyecto? Conflictos abiertos
queue_doc proyecto, nombre, contenido Encola documento en inbox

Cliente MCP: mcp/client.py permite conectar a cualquier servidor MCP (stdio o HTTP) y llamar tools/list y tools/call.

---

5. Kernel y contratos (código real)

El kernel (orchestrator/kernel/core.py) es agnóstico: nunca nombra plugins por su nombre. Todo se descubre por carpeta + manifest.json.

Contratos universales (base/contracts.py)

```python
# InputAdapter — toda carpeta inputs/ implementa:
class InputAdapter:
    def discover(self) -> list[Document]   # -> [Document]
    def ack(self, doc: Document): pass

# OutputConnector — toda carpeta outputs/ implementa:
class OutputConnector:
    def call(self, accion: str, payload: dict) -> dict

# AgentAdapter — toda carpeta agents/ implementa:
class AgentAdapter:
    def capabilities(self) -> list[str]
    def execute(self, capability: str, payload: dict, ctx: dict) -> dict
```

Gestión de capacidades (kernel/managers.py)

· Registry: escanea inputs/ outputs/ agents/, hot‑reload por mtime.
· AgentManager: capability → cadena de agentes (prioridad), con CircuitBreaker por capacidad.
· OutputManager: capability de salida → conector. El kernel pide "notify", "taskboard", "graph", "vault", "handoff" — no "telegram" o "kanboard".

Estado persistente (store/db.py)

· SQLite con journal_mode=WAL.
· Tablas: inventory (hash, proyecto, estado, parents), conflictos, tareas (UNIQUE proyecto+titulo), journal, kv.
· Funciones: inv_add, inv_estado, conf_add, conf_resolver, tarea_add, tareas.

---

6. Despliegue real (VPS Contabo + GitHub)

Arquitectura de deploy

```
GitHub (maxbry123-commits/osquestador-auditor)
  ├─ orchestrator/ (kernel + plugins + workflows)
  ├─ prototipo_v12/index.html (panel UI)
  └─ DEPLOY.md / SALIDA_3_claude_code_despliegue.md
       ↓ VPS (root@95.111.232.89)
/opt/nct/
  ├─ orchestrator-core/ (clonado)
  ├─ fase0-projects/ (vault + handoff versionados)
  ├─ kanboard/ (Docker: puerto 8080)
  └─ graphiti/ (Neo4j Docker + graphiti-core)
       ↓ systemd
orchestrator.service (Type=simple, Restart=always)
       ↓ cloudflared (túnel)
https://*.trycloudflare.com/ (panel público)
```

Pasos de despliegue (resumen de SALIDA_3)

1. VPS: Ubuntu 22.04, Docker, Python 3.11, SQLite3, UFW.
2. Repos: orchestrator-core y fase0-projects clonados.
3. Kanboard: Docker compose en :8080, proyecto "Fase0", token API.
4. Graphiti: Neo4j Docker + graphiti-core pip, endpoint MCP en :8000.
5. Obsidian: vault = fase0-projects/vault/, cron cada 15 min git commit + push.
6. Telegram: bot token + chat_id en config.json.
7. OCR: scaffold agent ocr_remoto → HF Space o Baidu API.
8. systemd: orchestrator.service (WorkingDirectory /opt/nct/orchestrator-core, ExecStart python3 -m orchestrator).
9. Smoke test: 3 docs de prueba → 1 conflicto → resolver → handoff OK.
10. Tag: v2.0-fase0 commit + reporte al Director.

Scripts de soporte

· tools/check_kernel_isolation.py — linter: falla si kernel nombra plugins.
· tools/scaffold.py input|output|agent <nombre> — genera carpeta + manifest + adapter en 5 minutos.

---

7. Gaps reales confirmados (no inventados)

ID Gap Estado Prioridad
G‑01 Detector de alucinaciones ❌ No existe Alta
G‑02 Council Engine (Consensus Runtime) ❌ No construido #1
G‑03 Meta Kernel formal (separar de memoryos.py) 🔲 Pendiente Media
G‑04 Universal Contract (8 métodos en cada motor) 🔲 Pendiente Media
G‑05 MCP server con todas las 7 tools 🔲 Parcial (4 tools) Media
G‑06 Plugins: llm_router, notification, scheduler, terminal, web_search, code_exec ❌ Pendientes Media
G‑07 Workflows 3 y 4 (árbol + taskindex) ✅ Hechos —
G‑08 Integración real de Graphiti/OCR Baidu/Kanboard 🔷 Verificar contenido interno Media
G‑09 pip install osquestador + entry point ❌ No existe Media‑baja
G‑10 systemd Type=notify + WatchdogSec=30s ❌ Pendiente Media
G‑11 restic + S3 backup (RPO 6h) ❌ Pendiente Baja
G‑12 Deploy real a /root/osquestador/ en VPS ❌ Pendiente (está en /opt/nct/) Media

Regla de oro: ningún gap se resuelve escalando a Max. Se investigan 200 búsquedas por gap antes de pedir ayuda.

---

8. Certificación actual (FASE 9 del spec)

Check Estado
100+ fuentes investigadas ✅
5+ skills documentados ✅
6 docs obligatorios en repo ✅
state.json actualizado ✅
CHECKPOINTS completos ✅
BITACORA con todas las acciones ✅
Panel renderiza + valida (V12) ✅
MCP server responde 4 tools 🔲 Pendiente
VPS health = alive ✅
Memoria operativa (HOT/WARM/COLD) ✅
OpenClaw INTACTO ✅
Cero FAIL / WARNING / PENDING ❌ Gaps pendientes

Estado: NO CERTIFICADO (7/12 checks pendientes). Próximo milestone: BUCLE 12‑30 (workflows 3 y 4) → 8/12 checks.

---

9. Cómo usar el Osquestador desde otro agente (MCP)

Cualquier agente (TEAM YAIWES, Mavis, otro) puede conectarse al servidor MCP en :8765 y llamar:

```python
# Ejemplo con HTTPBridge (mcp/client.py)
bridge = HTTPBridge("http://127.0.0.1:8765")
tools = bridge.tools()  # ["search_project", "get_doc", "list_conflicts", "queue_doc"]

# Buscar documentos de un proyecto
result = bridge.tool("search_project", {"proyecto": "mi-proyecto"})
# → {"docs": [...], "tareas": [...], "conflictos": [...]}

# Obtener contenido de un documento
doc = bridge.tool("get_doc", {"hash": "40f42ac26b11"})
# → {"meta": {...}, "contenido": "..."}
```

El agente no necesita conocer Telegram, Kanboard, Graphiti, Obsidian ni OCR. Solo habla con el orquestador vía MCP.

---

10. Conclusión para un agente IA

El Osquestador de Memoria y Auditoría está en Fase 0 operativa:

· ✅ Kernel agnóstico (180 LOC) que descubre plugins por carpeta.
· ✅ 4 workflows declarativos (ingesta, auditoría, árbol, taskindex).
· ✅ 12 plugins (inputs, outputs, agents) con contratos uniformes.
· ✅ MCP server con 4 tools para control remoto.
· ✅ Panel UI V12 con 5 zonas, 9 agentes, 7 funciones window.osquestador.
· ✅ Idempotencia por SHA256 (nada se procesa dos veces).
· ✅ Conflictos detectados y resueltos por usuario (nunca auto‑fusiona).
· ✅ Handoff exporta paquete Fase 0 cuando la frontera está lista.

Lo que falta: Council Engine, detector de alucinaciones, MCP completo (7 tools), systemd con watchdog, backup restic, y el Meta Kernel formal. Todos los gaps se resolverán en los próximos 189 bucles de investigación e implementación, sin escalar a Max.

El sistema está diseñado para ser: un segundo cerebro determinista donde el LLM (≈5‑10%) solo interpreta lenguaje natural y genera texto; el resto (≈90‑95%) es código que garantiza reproducibilidad, trazabilidad y bajo consumo de recursos.

---

Documentos fuente (para consulta interna):

· AUDITORIA_MD_1_NUCLEO.md — 25 decisiones, stack, reglas duras.
· AUDITORIA_MD_2_INVESTIGACION.md — 32 fuentes + 4 Puntos comunidad.
· AUDITORIA_MD_3_INPUT_BLOCKS.md — 11 input blocks literales + DSL DAG.
· AUDITORIA_MD_4_PROTOTIPOS.md — Evolución V1‑V12 + 70 ideas + 25 decisiones.
· AUDITORIA_MD_5_BACKEND_DEPLOY.md — Backend MVP + deploy + bucle final.
· GAP_03_AUDITOR_DOCUMENTOS.md — Gaps reales confirmados.
· SALIDA_2_orquestador_fase0.md — Especificación completa.
· SALIDA_2_v2_A_nucleo.md — Código del kernel + contratos + store.
· SALIDA_2_v2_B_plugins.md — Código de los 12 plugins.
· SALIDA_2_v2_C_mcp_tools.md — MCP server + tools + despliegue.
· SALIDA_3_claude_code_despliegue.md — Instrucciones paso a paso para Claude Code.

Osquestador de Auditoría y Memoria — Plan de Construcción (12 Pasos · 12 Simulaciones · 12 Inputs · 12 Outputs)

Sistema 90% Código Determinista · 10% LLM · Memoria Avanzada para cualquier Agente IA

---

PREÁMBULO — Filosofía del Sistema

El Osquestador no es un chat, no es una base de datos, no es un orquestador de LLMs. Es un Sistema Operativo del Conocimiento donde:

· 90% del trabajo es código determinista: búsquedas, relaciones, auditorías, workflows, versionado, indexación.
· 10% del trabajo usa LLM: interpretar lenguaje natural, generar resúmenes, resolver ambigüedades, crear explicaciones.

Cualquier agente IA (TEAM YAIWES, Mavis, OpenClaw, Claude Code, etc.) se conecta vía MCP y obtiene:

· Memoria persistente (conversaciones, decisiones, soluciones).
· Grafo de conocimiento (entidades, relaciones, dependencias).
· Búsqueda híbrida (textual, semántica, estructural, por grafos).
· Auditoría automática (integridad, conflictos, procedencia, frescura).
· Workflows reanudables (DAG determinista).
· Recursos auto-descubiertos y auto-registrados.

---

PARTE 1 — 12 PASOS PARA CONSTRUIR EL OSQUESTADOR

Paso 1 — Kernel Agnóstico (Núcleo Determinista)

Objetivo: Crear el núcleo de ~500 LOC que nunca crece y nunca nombra plugins.

```
orchestrator/
├── kernel/
│   ├── core.py          # boot → pump → shutdown (event loop)
│   ├── motor.py         # intérprete de workflows declarativos
│   ├── managers.py      # Registry (descubre plugins) + AgentManager + OutputManager
│   └── commands.py      # comandos de usuario (/estado, /conflictos, /resolver)
├── base/
│   ├── contracts.py     # InputAdapter, OutputConnector, AgentAdapter
│   └── resilience.py    # atomic_write_json, CircuitBreaker, backoff, health
└── store/
    └── db.py            # SQLite WAL + inventory + conflictos + tareas + journal
```

Reglas:

· El kernel NUNCA importa un plugin por nombre.
· Todo se descubre por carpeta/manifest.json.
· Hot‑reload por mtime (sin reiniciar).
· atomic_write_json para SIGKILL‑safe.
· Graceful shutdown con SIGTERM/SIGINT.

Código clave: contracts.py (interfaces universales), resilience.py (atomic_write_json, CircuitBreaker), managers.py (Registry + AgentManager).

---

Paso 2 — Sistema de Plugins (Inputs/Outputs/Agents)

Objetivo: Cada plugin es una carpeta con manifest.json + adapter.py. El kernel los descubre y carga.

Estructura de un plugin:

```
inputs/telegram/
├── manifest.json   # {"type":"input","name":"telegram","iface":"input.v1","status":"active"}
└── adapter.py      # class TelegramInput(InputAdapter): discover() -> [Document], ack(doc)
```

Plugins mínimos para Fase 0:

Tipo Plugin Función
Input inbox Watcher de carpeta inbox/<proyecto>/
Input telegram Bot Telegram (comandos + documentos)
Output obsidian Guarda docs en vault markdown + frontmatter
Output kanboard Crea tareas vía JSON‑RPC API
Output graphiti Grafo local JSON + Neo4j remoto opcional
Output handoff Exporta paquete Fase 0
Agent ocr Extrae texto de binarios (PaddleOCR/Tesseract)
Agent persistir Hash SHA256 + guarda vault + inventario
Agent haystack Similitud Jaccard vs corpus
Agent auditor Duplicado/versión/conflicto/único
Agent arbolista Extrae objetivos/decisiones/tareas/urls/repos
Agent plandex Detecta objetivos sin tarea → crea "DEFINIR"
Agent hermes Genera README_RAIZ.md
Agent swe Audita frontera (conflictos=0, pendientes=0)

Regla de oro: añadir un plugin = crear carpeta + 2 archivos. El kernel lo detecta solo.

---

Paso 3 — Workflows Declarativos (DAG Determinista)

Objetivo: El kernel ejecuta workflows escritos en JSON/YAML. Sin lógica de negocio en el kernel.

Workflow 1 — INGESTA (document.new):

```json
{
  "id": "ingesta_auditoria",
  "trigger": "document.new",
  "steps": [
    {"id": "hash", "capability": "hash"},
    {"id": "ocr", "capability": "ocr", "on_error": "stop"},
    {"id": "skip_binario", "when": {"campo": "requiere_ocr", "truthy": true},
     "connector": "notify", "accion": "send"},
    {"id": "persistir", "when": {"campo": "requiere_ocr", "truthy": false},
     "capability": "persistir"},
    {"id": "auditar", "when": {"campo": "requiere_ocr", "truthy": false},
     "capability": "auditoria"},
    {"id": "avisar_conflicto", "when": {"campo": "resultado_auditoria", "eq": "conflicto"},
     "connector": "notify", "accion": "send"},
    {"id": "tarjeta_conflicto", "when": {"campo": "resultado_auditoria", "eq": "conflicto"},
     "connector": "taskboard", "accion": "crear_tarea"}
  ]
}
```

Workflow 2 — AUDITORÍA (document.audit):

```json
{"id": "re_auditoria", "trigger": "document.audit",
 "steps": [{"id": "auditar", "capability": "auditoria"}]}
```

Workflow 3 — ÁRBOL (document.tree):

```json
{"id": "arbol", "trigger": "document.tree",
 "steps": [
   {"id": "extraer", "capability": "arbol"},
   {"id": "grafo", "connector": "graph", "accion": "bulk_edges"}
 ]}
```

Workflow 4 — TASK INDEX (project.taskindex):

```json
{"id": "taskindex", "trigger": "project.taskindex",
 "steps": [
   {"id": "planificar", "capability": "planificar"},
   {"id": "documentar", "capability": "documentar"},
   {"id": "guardar_raiz", "connector": "vault", "accion": "save"},
   {"id": "frontera", "capability": "frontera"},
   {"id": "handoff", "when": {"campo": "frontera_ok", "truthy": true},
    "connector": "handoff", "accion": "export"}
 ]}
```

Regla: el kernel NO sabe qué hacen los pasos. Solo ejecuta capability o connector.

---

Paso 4 — Memoria Persistente (SQLite + JSON + Git)

Objetivo: Tres niveles de memoria que sobreviven a reinicios.

Nivel Tecnología Contenido Retención
HOT RAM + state.db WAL Contexto activo (<500 tokens) Sesión
WARM SQLite FTS5 (BM25) + FAISS Hechos comprimidos (1‑3K) 90 días
COLD Vault markdown + Git Documentos íntegros Indefinido

Tablas SQLite:

```sql
CREATE TABLE inventory(
  hash TEXT PRIMARY KEY, proyecto TEXT, nombre TEXT, vault TEXT,
  estado TEXT, parents TEXT DEFAULT '', ts TEXT);
CREATE TABLE conflictos(
  id TEXT PRIMARY KEY, proyecto TEXT, doc_a TEXT, doc_b TEXT,
  similitud REAL, estado TEXT, ts TEXT);
CREATE TABLE tareas(
  id TEXT PRIMARY KEY, proyecto TEXT, titulo TEXT, etiqueta TEXT,
  estado TEXT, remoto_id TEXT, ts TEXT, UNIQUE(proyecto, titulo));
CREATE TABLE journal(
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, wf TEXT, step TEXT, payload TEXT);
CREATE TABLE kv(k TEXT PRIMARY KEY, v TEXT);
```

Reglas:

· atomic_write_json para state/ (SIGKILL‑safe).
· journal_mode=WAL para recuperación.
· Git commit automático del vault cada 15 min.

---

Paso 5 — Auditoría Automática (Duplicados · Conflictos · Procedencia)

Objetivo: Cada documento pasa por un pipeline de auditoría antes de entrar al árbol.

Flujo de auditoría:

```
Documento nuevo
    ↓
Hash SHA256 (idempotencia)
    ↓
¿Ya existe en inventory?
    ↓ (NO)
OCR si binario (PaddleOCR/Tesseract)
    ↓
Comparar contra corpus del proyecto (Jaccard 5‑shingles)
    ├─ sim ≥ 0.98 → DUPLICADO (archivar)
    ├─ 0.70 ≤ sim < 0.98 → CONFLICTO (tarjeta en Kanboard)
    └─ sim < 0.70 → ÚNICO (pasa al árbol)
```

Resolución de conflictos (SIEMPRE por usuario):

· /resolver <id> A → gana doc A, doc B archivado (lineage).
· /resolver <id> B → gana doc B, doc A archivado.
· /resolver <id> FUSION → solicita doc fusionado (nuevo).

Procedencia (lineage):

· Cada entidad guarda parents (documentos que la generaron).
· Cada documento guarda hash, ts, origen.
· journal registra cada paso de workflow.

Regla: el sistema NUNCA fusiona ni descarta solo. Siempre pregunta al usuario.

---

Paso 6 — Grafo de Conocimiento (Entidades + Relaciones)

Objetivo: Construir un grafo liviano (JSON + opcional Neo4j) con entidades y relaciones.

Entidad (archivo JSON):

```json
{
  "id": "parser_python",
  "type": "function",
  "proyecto": "kernel",
  "metadata": {"file": "parser.py", "line": 42}
}
```

Relación (edge):

```json
{
  "de": "parser_python",
  "a": "lexer",
  "tipo": "llama_a",
  "proyecto": "kernel",
  "ts": "2026-08-10T12:00:00Z"
}
```

Extracción automática (arbolista):

· Objetivos → define_objetivo
· Decisiones → define_decision
· Tareas → define_tarea
· URLs (GitHub) → repo / url
· Archivos mencionados → menciona_archivo

Consulta de grafo (determinista):

```python
def get_relations(entity_id, proyecto):
    return [e for e in graph["edges"] 
            if (e["de"] == entity_id or e["a"] == entity_id) 
            and e.get("proyecto") == proyecto]
```

---

Paso 7 — Motor de Búsqueda Híbrida (BM25 + Vector + Grafo)

Objetivo: Tres motores de búsqueda que se fusionan con RRF (Reciprocal Rank Fusion).

Motor Tecnología Uso
Keyword SQLite FTS5 (BM25) Búsqueda textual exacta
Semántico FAISS + MiniLM‑L6‑v2 (384‑dim) Búsqueda por embeddings
Estructural Grafo JSON Búsqueda por relaciones

Fusión (RRF):

```
score = Σ 1/(k + rank_i)
```

Búsqueda desde MCP:

```python
bridge.tool("search_project", {"proyecto": "kernel", "query": "parser"})
# → docs + tareas + conflictos + relaciones
```

---

Paso 8 — MCP Server (Exposición a Agentes)

Objetivo: Cualquier agente IA se conecta vía MCP y usa el Osquestador sin conocer su interior.

Tools MCP:

Tool Parámetros Función
search_project proyecto, query? Docs + tareas + conflictos
get_doc hash Contenido íntegro del documento
list_conflicts proyecto? Conflictos abiertos
queue_doc proyecto, nombre, contenido Encola documento
create_task proyecto, titulo, descripcion Crea tarea en Kanboard
list_tasks proyecto Tareas del proyecto
health — Estado del sistema

Ejemplo de uso desde agente:

```python
bridge = HTTPBridge("http://127.0.0.1:8765")
result = bridge.tool("search_project", {"proyecto": "kernel"})
# → {"docs": [...], "tareas": [...], "conflictos": [...]}
```

---

Paso 9 — Despliegue 24/7 (systemd + Watchdog + Backup)

Objetivo: El Osquestador corre en VPS, se auto‑recupera y hace backup.

systemd service:

```ini
[Unit]
Description=Osquestador Auditor
After=network.target docker.service

[Service]
WorkingDirectory=/opt/nct/orchestrator-core
ExecStart=/usr/bin/python3 -m orchestrator
Restart=always
RestartSec=5
KillSignal=SIGTERM
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
```

Watchdog interno (30s):

```python
# health.json refrescado en cada paso
if health["status"] != "alive":
    # reinicio automático por systemd
```

Backup (restic + S3, RPO 6h):

```bash
0 */6 * * * restic backup /opt/nct/fase0-projects/vault/ --tag osquestador
```

Túnel público (cloudflared):

```bash
cloudflared tunnel --url http://127.0.0.1:8765
```

---

Paso 10 — Auto‑Descubrimiento de Recursos (Ruflo C01‑C08)

Objetivo: El sistema descubre, registra, mapea, verifica, selecciona, prepara, carga y ejecuta recursos.

Estados de recursos:

```
DISCOVERED → REGISTERED → CONFIGURED → REACHABLE → HEALTHY → AUTHORIZED → AVAILABLE
```

Componentes Ruflo integrados:

ID Componente Función
C01 Controller Registry Registro de controladores
C02 AgentDB Tools Bridge Puente entre MCP y memoria
C03 Plugin Discovery Registry Descubrimiento de plugins
C04 Capability Selection Selección de capacidad
C05 Resource Map Mapeo de recursos
C06 Preload Precarga selectiva
C07 Lazy Loading Bridge Carga bajo demanda
C08 Health & Status Verificación de salud

Flujo:

```
descubre → registra → mapea → verifica → selecciona → prepara → carga → ejecuta
```

---

Paso 11 — Council Engine (Consensus Runtime)

Objetivo: Validación obligatoria antes/después de cada fase.

Funciones del Council:

1. Pre‑ejecución: verifica que el recurso esté AVAILABLE.
2. Post‑ejecución: valida que el resultado sea consistente.
3. Conflictos: detecta contradicciones entre fuentes.
4. Confianza: asigna puntuación de confianza a cada entidad.
5. Rollback: si falla la validación, revierte al checkpoint anterior.

Ejemplo de validación:

```python
def council_validate(resultado, contexto):
    # 1. ¿El resultado contradice alguna fuente previa?
    # 2. ¿La procedencia es completa?
    # 3. ¿La confianza supera el umbral?
    # 4. ¿Hay duplicados?
    return {"approved": True, "confidence": 0.92, "issues": []}
```

---

Paso 12 — Self‑Optimization (Aprendizaje Automático)

Objetivo: El sistema se mejora solo sin intervención humana.

Loops de optimización:

1. Compactación: fusiona entidades duplicadas.
2. Reindexación: actualiza índices cuando cambian patrones de acceso.
3. Poda: archiva información obsoleta (>90 días sin uso).
4. Refactor: reorganiza el grafo para reducir profundidad.
5. Predicción: aprende patrones de uso y precarga recursos.

Ejecución:

· Diaria (02:00 UTC): compactación + reindexación.
· Semanal: poda + refactor.
· Mensual: predicción + ajuste de umbrales.

---

PARTE 2 — 12 SIMULACIONES DE USO

Simulación 1 — Nuevo agente se conecta

```
Agente → MCP (`tools/list`) → Osquestador
Osquestador → devuelve 7 tools disponibles
Agente → `search_project({"proyecto": "kernel"})`
Osquestador → devuelve docs + tareas + conflictos
```

Resultado: el agente tiene contexto completo del proyecto en <200ms.

---

Simulación 2 — Usuario sube documento por Telegram

```
Usuario → envía PDF por Telegram
Telegram Input → Documento (PDF) → Workflow INGESTA
OCR → extrae texto → Hash → ¿existe? → NO
Auditor → compara contra corpus → CONFLICTO (sim 0.78)
Kanboard → crea tarjeta "CONFLICTO"
Telegram → avisa "⚠️ CONFLICTO detectado"
```

Resultado: el usuario recibe alerta, el conflicto está en Kanboard.

---

Simulación 3 — Usuario resuelve conflicto

```
Usuario → `/resolver c123 A` (elige documento A)
Commands → actualiza inventory: A=auditado, B=archivado (parents=A)
Workflow ÁRBOL → extrae entidades de A → actualiza grafo
Workflow TASK INDEX → detecta objetivos sin tarea → crea "DEFINIR"
Telegram → avisa "✅ Conflicto resuelto, árbol actualizado"
```

Resultado: el conflicto se resuelve, el árbol se actualiza.

---

Simulación 4 — Agente busca información

```
Agente → MCP `search_project({"proyecto": "kernel", "query": "parser"})`
FTS5 → 3 docs con "parser"
FAISS → 2 docs semánticamente similares
Grafo → 5 relaciones de "parser"
RRF → fusiona resultados → top 5
Osquestador → devuelve docs + relaciones + tareas
```

Resultado: el agente obtiene contexto relevante en <500ms.

---

Simulación 5 — Sistema se auto‑recupera de caída

```
Kernel recibe SIGTERM → `atomic_write_json` health.json → shutdown()
systemd → detecta exit → Restart=always → reinicia
Boot → `_recover()` detecta docs en "ingresado" → re‑audita
Workflow AUDITORÍA → completa docs pendientes
Health → "alive" → continúa
```

Resultado: el sistema se recupera sin pérdida de datos.

---

Simulación 6 — Usuario crea proyecto nuevo

```
Usuario → `/nuevo_proyecto "nct-core"`
Commands → crea proyecto en DB → crea vault/nct-core/
Workflow TASK INDEX → genera README_RAIZ.md → handoff/
Telegram → avisa "📦 Proyecto nct-core listo"
```

Resultado: el proyecto está listo en <1s.

---

Simulación 7 — Sistema detecta duplicado exacto

```
Usuario → sube documento ya existente
Ingesta → hash SHA256 → existe en inventory → SKIP (silencioso)
Telegram → avisa "⏭️ Documento duplicado, no procesado"
```

Resultado: el sistema no reprocesa, avisa al usuario.

---

Simulación 8 — Agente pide estado del sistema

```
Agente → MCP `health()`
Osquestador → devuelve {status:"alive", uptime:3600s, docs:142, conflicts:3}
```

Resultado: el agente conoce el estado del sistema.

---

Simulación 9 — Usuario solicita exportación (handoff)

```
Usuario → `/handoff kernel`
Commands → exporta handoff.json + README_RAIZ.md → handoff/kernel/
Telegram → avisa "📦 Handoff kernel listo"
```

Resultado: el paquete Fase 0 está listo para Fase 1.

---

Simulación 10 — Sistema hace backup automático

```
Cron → restic backup /opt/nct/fase0-projects/vault/ --tag osquestador
Backup → S3 (RPO 6h) → verifica integridad
Health → registra "backup_ok"
```

Resultado: el sistema tiene backup cada 6h.

---

Simulación 11 — Council bloquea acción no autorizada

```
Agente → `create_task({"proyecto":"kernel","titulo":"borrar todo"})`
Council → verifica permisos → NO AUTORIZADO → bloquea
Osquestador → devuelve error "Acción no permitida"
```

Resultado: acciones destructivas son bloqueadas.

---

Simulación 12 — Sistema se auto‑optimiza

```
Cron (02:00 UTC) → compactación de entidades duplicadas
→ reindexación de FTS5 → poda de >90 días
→ ajuste de umbrales de similitud
Health → registra "optimization_ok"
```

Resultado: el sistema mantiene su rendimiento.

---

PARTE 3 — 12 GOALS DE ENTRADA (Inputs)

# Goal Descripción
I‑01 Ingesta de documentos Recibir PDF, Markdown, Word, imagen, escaneado, email, mensaje de chat.
I‑02 Comandos de usuario /estado, /conflictos, /resolver, /frontera, /handoff.
I‑03 Búsqueda Query en lenguaje natural o estructurada.
I‑04 Preguntas sobre el sistema ¿Cuántos documentos? ¿Qué conflictos hay? ¿Cuál es el estado?
I‑05 Creación de proyectos Nuevo proyecto con su vault y handoff.
I‑06 Conexión de agentes MCP tools/list, tools/call.
I‑07 Actualización de documentos Nueva versión de un documento existente.
I‑08 Resolución de conflictos Elegir A, B o solicitar fusión.
I‑09 Auditoría manual Re‑auditar un documento o proyecto completo.
I‑10 Exportación de paquetes Generar handoff para Fase 1.
I‑11 Configuración Cambiar umbrales de similitud, proveedores, etc.
I‑12 Diagnóstico Health check, métricas, logs.

---

PARTE 4 — 12 GOALS DE SALIDA (Outputs)

# Goal Descripción
O‑01 Documentos en vault Markdown con frontmatter y wikilinks.
O‑02 Tareas en Kanboard Task DNA completo (título, descripción, dependencias, estado).
O‑03 Grafo en Graphiti Entidades y relaciones (JSON + Neo4j opcional).
O‑04 Notificaciones por Telegram Alertas de conflicto, estado, handoff.
O‑05 Respuestas a búsquedas Documentos + tareas + conflictos + relaciones.
O‑06 Handoff packages handoff.json + README_RAIZ.md para Fase 1.
O‑07 Health status health.json para watchdog y monitoreo.
O‑08 Logs estructurados journal en SQLite + log.jsonl.
O‑09 Métricas Cantidad de docs, conflictos, tareas, tiempo de respuesta.
O‑10 Backups Snapshots en S3 (RPO 6h).
O‑11 Auditoría de procedencia Linaje completo de cada entidad.
O‑12 Respuestas a comandos Confirmaciones de acciones del usuario.

---

PARTE 5 — RESUMEN EJECUTIVO

Lo que el Osquestador hace (90% código determinista)

Función Tecnología Entrada → Salida
Ingesta SHA256 + inventory Documento → ID + vault + inventory
OCR PaddleOCR/Tesseract Imagen/PDF → Texto
Auditoría Jaccard 5‑shingles Texto → Duplicado/Conflicto/Único
Árbol Regex + Graphiti Texto → Entidades + Relaciones
Task Index SQLite UNIQUE Entidades → Tareas DEFINIR
Búsqueda FTS5 + FAISS + Grafo + RRF Query → Documentos + Tareas + Relaciones
Comandos Commands handler Texto → Acción + Respuesta
Backup restic + S3 Vault → Snapshot cifrado
Recuperación atomic_write_json + WAL Crash → Reanudación desde último paso

Lo que el Osquestador NO hace (10% LLM)

Función Cuándo se usa Por qué no es 100% código
Interpretar consultas "¿Qué pasó con el parser?" El lenguaje natural es ambiguo
Generar resúmenes "Resume este proyecto" La síntesis requiere comprensión semántica
Explicar decisiones "¿Por qué se marcó como conflicto?" Requiere razonamiento sobre el contexto
Redactar documentación "Escribe un README" La redacción es una tarea generativa
Clasificar tags complejos Si confidence < 0.7 Los tags complejos requieren semántica
Responder preguntas abiertas "¿Cómo mejoro esto?" Requiere razonamiento y sugerencias
Fusión de documentos Cuando el usuario pide fusión Requiere comprensión de ambos textos
Explicación de errores "¿Qué falló en el workflow?" Requiere razonamiento sobre logs

Beneficios del sistema

1. Cualquier agente IA se conecta vía MCP y obtiene memoria avanzada.
2. Memoria persistente que sobrevive a reinicios y caídas.
3. Trazabilidad completa de cada decisión y documento.
4. Auditoría automática de duplicados, conflictos y procedencia.
5. Búsqueda híbrida (textual, semántica, estructural) en <500ms.
6. Auto‑recuperación con systemd + watchdog + backups.
7. Auto‑descubrimiento de recursos (Ruflo C01‑C08).
8. Council Engine para validación obligatoria.
9. Self‑optimization dia





