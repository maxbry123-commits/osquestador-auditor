# ORQUESTADOR FASE 0 — Especificación Completa v1.0
## (Salida 2 — documento de diseño para implementación por Claude Code)

---

## 1. FILOSOFÍA

El orquestador es un **kernel pequeño y estable (~200 líneas)** que nunca crece.
Toda la inteligencia vive fuera: en agentes, skills, roles, entradas y conectores — todos como **carpetas intercambiables**.

**Regla de oro (obligatoria para Claude Code):**
> El núcleo del orquestador debe permanecer pequeño, estable y agnóstico de las implementaciones. Toda funcionalidad específica reside en módulos externos (agentes, skills, roles, políticas, entradas, conectores). Para añadir, sustituir o eliminar cualquier módulo, solo debe ser necesario agregar, reemplazar o eliminar su carpeta y actualizar el registro correspondiente — sin modificar una sola línea del kernel.

**Alcance estricto:** este orquestador SOLO controla la Fase 0 (P1+P2). Termina cuando el contenedor está listo (árbol Graphiti completo + Kanboard con tareas completas). No ejecuta código de proyectos, no toca el DSL de 15 nodos, no hace push a GitHub de proyectos. Esa es Fase 1 (OpenClaw).

---

## 2. ESTRUCTURA DE CARPETAS (repo separado: `orchestrator-core`)

```
orchestrator-core/
├── kernel/
│   ├── main.py              # loop principal (~200 líneas máximo)
│   ├── state.py             # estado persistente (atomic_write_json)
│   └── router.py            # despacho evento→workflow
├── inputs/                  # ENTRADAS plugin (cada carpeta = un canal)
│   ├── telegram/
│   ├── drive/
│   ├── chat-mcp/
│   ├── kanboard-ui/         # webhook desde la UI de Kanboard
│   └── _template/           # plantilla para entradas futuras
├── agents/                  # AGENTES (cada carpeta = un agente)
│   ├── ocr/
│   ├── haystack/
│   ├── repomix/
│   ├── plandex/
│   ├── hermes/
│   ├── swe-agent/
│   └── _template/
├── skills/                  # SKILLS del sistema (no pertenecen a agentes)
│   ├── research/
│   ├── audit/
│   ├── architecture/
│   ├── documentation/
│   ├── reuse/
│   └── _template/
├── roles/                   # ROLES intercambiables
│   ├── classifier/
│   ├── auditor/
│   ├── planner/
│   ├── documenter/
│   └── _template/
├── registries/              # REGISTROS (solo JSON, sin lógica)
│   ├── capability.json      # capacidad → proveedor actual → fallback
│   ├── agents.json          # agentes instalados + estado
│   ├── skills.json          # skills disponibles + Skill DNA
│   └── providers.json       # LLM providers (Cerebras/Groq/etc vía LiteLLM)
├── policies/
│   ├── knowledge.policy.md  # reglas anti-síntesis (sección 6)
│   ├── conflict.policy.md   # conflictos siempre al usuario
│   └── phase0.policy.md     # frontera de Fase 0
├── outputs/                 # CONECTORES de salida (control remoto)
│   ├── kanboard-api/
│   ├── obsidian-api/
│   ├── graphiti-mcp/
│   └── _template/
├── workflows/
│   ├── ingesta.workflow.json
│   ├── auditoria.workflow.json
│   ├── arbol.workflow.json
│   └── taskindex.workflow.json
├── state/
│   ├── workflow_state.json  # atomic write, reanudable
│   ├── health.json
│   ├── dead_letter.json
│   └── inventory.json       # hash SHA256 de todo documento procesado
└── README.md + PLAYBOOK.md + checkpoint.json + module.context.json + knowledge.index
```

---

## 3. CONTRATOS (interfaces únicas)

### 3.1 Agent Adapter — TODA carpeta de agente implementa exactamente:
```
initialize(config) -> ok/error
execute(task, context) -> result
cancel(task_id) -> ok
health() -> {status, latency}
capabilities() -> [lista de capacidades que ofrece]
shutdown() -> ok
```

### 3.2 Agent Manifest — `agents/<nombre>/manifest.json`:
```json
{
  "name": "", "version": "", "capabilities": [],
  "skills_supported": [], "models_compatible": [],
  "provider": "", "dependencies": [], "priority": 0,
  "status": "active|disabled"
}
```
El kernel **nunca inspecciona código del agente** — solo lee su manifest.

### 3.3 Input Adapter — TODA carpeta de entrada implementa:
```
listen() -> evento          # detecta archivo/mensaje nuevo
normalize(raw) -> Documento # formato único interno
ack(evento) -> ok           # confirma recepción
```
Formato único interno de Documento:
```json
{
  "doc_id": "sha256", "origen": "telegram|drive|...",
  "proyecto": "detectado|desconocido", "tipo": "pdf|md|img|docx",
  "ruta_original": "", "timestamp": "", "raw_path": ""
}
```

### 3.4 Output Connector — TODA carpeta de salida implementa:
```
connect() -> ok
call(accion, payload) -> result   # ej: call("crear_tarea", {...})
health() -> {status}
```
Esto permite usar Kanboard/Obsidian/Graphiti **sin abrir sus interfaces** — el orquestador es el control remoto. Mañana tu propia interface habla solo con el orquestador.

---

## 4. FLUJO INTERNO DEL KERNEL

```
Evento (de cualquier input/)
   ↓
Router → identifica workflow aplicable
   ↓
Workflow (JSON declarativo, pasos en orden)
   ↓
Skill Manager → selecciona la Skill del paso
   ↓
Agent Manager → consulta capability.json → mejor agente disponible
   ↓
Agente ejecuta la Skill (vía adapter)
   ↓
Resultado → siguiente paso del workflow
   ↓
Al cerrar: actualiza outputs (Kanboard/Obsidian/Graphiti) + state + health
```

El kernel NUNCA conoce agentes concretos. Pide capacidades:
- "necesito OCR" → capability.json → ocr/ (fallback: ocr-alternativo/)
- "necesito planificación" → plandex/ (fallback: otro)

Cambiar de agente = editar 1 línea en capability.json. Nada más.

---

## 5. PIPELINE FASE 0 (los 4 workflows)

### Workflow 1 — INGESTA (dispara: documento nuevo en cualquier input)
```
[Recibir] → [Hash SHA256] → [¿existe en inventory.json? → skip]
→ [OCR si es imagen/pdf escaneado] → [Clasificar por proyecto]
→ [Etiquetas] → [Guardar íntegro en Obsidian] → [Registrar en inventory.json]
```
Regla: **nada se procesa dos veces** (hash primero, siempre).

### Workflow 2 — AUDITORÍA 🥇 (dispara: lote de ingesta completo)
```
[Haystack compara cada doc contra el corpus del proyecto]
→ [Duplicado exacto (hash igual o similitud >98%)] → archiva, no procesa
→ [Versiones distintas del mismo contenido] → CONFLICTO → tarjeta en Kanboard
→ [Información contradictoria entre docs] → CONFLICTO → tarjeta en Kanboard
→ [Único] → pasa directo al árbol
```
**El usuario resuelve cada conflicto en Kanboard: aprobar A, aprobar B, o pedir fusión.**
El sistema NUNCA fusiona ni descarta solo. Prohibido resumir: el contenido original queda íntegro en Obsidian siempre, la auditoría solo CLASIFICA y SEÑALA.

### Workflow 3 — ÁRBOL DEL PROYECTO / P1 (dispara: conflictos resueltos)
```
[Crear/actualizar raíz: README del proyecto + tabla de tareas]
→ [Graphiti: crear entidades por doc (objetivos, decisiones, componentes, repos, recursos)]
→ [Graphiti: crear RELACIONES entre archivos del mismo proyecto]
→ [Detectar piezas faltantes (objetivo sin tareas, componente sin doc)]
→ [Cada faltante → tarea "DEFINIR" en Kanboard]
```
El árbol es la raíz que cualquier agente futuro consulta para tener TODO el proyecto: documentos, archivos, repos, recursos, método de trabajo (incluido el DSL/DAG/system prompt como parte del conocimiento del proyecto).

### Workflow 4 — TASK INDEX / P2 (dispara: árbol completo)
```
[Generar tareas completas con Task DNA:]
  {uuid, proyecto, prioridad, dependencias, agente_recomendado,
   contexto_necesario (links al árbol), criterio_aceptacion, estado}
→ [Escribir en Kanboard vía outputs/kanboard-api]
→ [Roadmap → Plane | Portafolio → OpenProject (si instalados)]
→ [Hermes: documenta el cierre + actualiza estado]
```

### FRONTERA — el orquestador se detiene cuando:
```
✔ inventory.json cubre el 100% de los docs subidos
✔ 0 conflictos abiertos en Kanboard
✔ Árbol Graphiti: todo doc tiene ≥1 relación con el proyecto
✔ Toda tarea en Kanboard tiene Task DNA completo o etiqueta "DEFINIR"
```
Resultado: **contenedor listo** → lo toma Fase 1 (OpenClaw + DSL 15 nodos → GitHub).
El orquestador Fase 0 NO participa en Fase 1.

---

## 6. POLÍTICAS OBLIGATORIAS

**knowledge.policy** (anti-síntesis, anti-pérdida):
1. Ningún agente resume contenido — solo clasifica, relaciona, señala.
2. El original íntegro vive en Obsidian; Graphiti solo guarda relaciones y metadata.
3. Nada entra al árbol sin clasificación y hash.
4. Ninguna tarea se cierra sin actualizar Graphiti + Obsidian + Kanboard.
5. Ningún doc se procesa dos veces (inventory.json es ley).

**conflict.policy:**
1. Todo duplicado no-exacto, versión o contradicción → tarjeta en Kanboard.
2. Solo el usuario aprueba/fusiona/descarta.
3. Fusiones: el agente propone el texto fusionado como NUEVO doc, los originales se archivan (nunca se borran).

**phase0.policy:**
1. Prohibido ejecutar código de proyectos.
2. Prohibido invocar el DSL de 15 nodos.
3. Prohibido hacer push a repos de proyectos.
4. Único destino de escritura: Obsidian, Graphiti, Kanboard/Plane/OpenProject, y su propio state/.

---

## 7. ROBUSTEZ (heredada de tu DSL, misma filosofía)

- `atomic_write_json` en todo state (SIGKILL-safe).
- Graceful shutdown (SIGTERM/SIGINT → persist + exit).
- Reanudación: workflow_state.json guarda paso actual; al reiniciar continúa donde quedó.
- Reintentos: máx 3 con exponential backoff → luego dead_letter.json + notificación Telegram.
- CircuitBreaker en conectores externos (Kanboard API, Telegram, Drive).
- health.json refrescado en cada paso.
- Loops de revisión: cualquier workflow puede re-ejecutarse N veces sobre el mismo proyecto — el hash/inventory garantiza que solo procesa lo nuevo o lo corregido.

---

## 8. LO QUE EL KERNEL NO HACE (para que nunca crezca)

- No parsea documentos (eso es skill de OCR/ingesta).
- No compara contenidos (eso es Haystack).
- No decide fusiones (eso es el usuario).
- No conoce Telegram ni Drive (eso son inputs/).
- No conoce Kanboard ni Obsidian (eso son outputs/).
- No contiene prompts (viven en skills/ y roles/, versionados).

---

## 9. CRITERIO DE ÉXITO DEL MVP

Con 1 solo proyecto de prueba y ~10 documentos reales tuyos:
1. Subes docs por Telegram o Drive.
2. El sistema detecta 1 duplicado y 1 conflicto → te pregunta → resuelves en Kanboard.
3. El árbol queda en Graphiti/Obsidian navegable.
4. Kanboard queda con tareas completas + tareas "DEFINIR".
5. Repites el loop (subes 1 doc corregido) → solo procesa lo nuevo.

Si esos 5 pasos funcionan, escalar a 50 docs es solo volumen, no diseño nuevo.
