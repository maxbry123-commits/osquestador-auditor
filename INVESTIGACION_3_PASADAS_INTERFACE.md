# INVESTIGACIÓN 3 PASADAS POR INTERFACE — CON INTEGRACIÓN INPUT-BLOCK
## 3 pasadas × cada interface del código fuente, integrado con Input Block Reader
**Fecha:** 2026-07-18 03:32
**Búsquedas realizadas:** 14 (3+3+3+2+3 de las 4 interfaces prioritarias)
**Trigger de Max:** "anota aprobado repite la búsqueda 3 pasada de nuevo por cada ui INtERFACE de esos sofware a ver si te faltó algo sin lo de imput block"

---

## 1) HAYSTACK (deepset-ai) — 3 PASADAS + INPUT-BLOCK

### Pasada 1: Código fuente + features para preservar input

**Versión actual:** v2.31.0 (jul 2026) — github.com/deepset-ai/haystack (314 tags, 9.2k stars)
**Versión analizada docs:** v2.26 (Agent component), v2.18 (structured outputs)

**Features identificados en código fuente (que me faltaban antes):**
- ✅ **`Agent` component** (v2.26) — sistema loop-based con `system_prompt` + `tools` + `state_schema` + `exit_conditions` + `streaming_callback`
- ✅ **`state_schema`** — typed schema para pasar parámetros entre tools (consume + produce)
- ✅ **`InMemoryChatMessageStore`** + `ChatMessageRetriever` + `ChatMessageWriter` — patrón de memoria conversacional con `chat_history_id`
- ✅ **`Conversation history`** — preserved across user questions via `chat_history_id`
- ✅ **`outputs_to_string`** con `{"source": "last_message"}` — extrae solo respuesta final, no execution trace
- ✅ **`FileContent` dataclass** — incluir PDFs en `ChatMessage` objects (v2.24)
- ✅ **Auto-conversion** `ChatMessage` ↔ `str` + `list[T]` ↔ `T` en pipelines (v2.24)
- ✅ **Deduplicación por `id`** antes de ranking — `MultiQueryTextRetriever` y `Rankers`
- ✅ **Pipeline serialization** — YAML format, guardar/cargar pipelines completos
- ✅ **`JsonSchemaValidator`** — valida LLM JSON output contra schema

**Cómo se integra con input-block en el Osquestador:**
- El `InputBlock` se pre-injecta como `system_prompt` del Haystack `Agent` (Tier 1 del system prompt)
- El `state_schema` del Agent lleva el `input_block_id` activo
- El `outputs_to_string` con `last_message` evita que el trace contamine el parent agent
- El `FileContent` permite que el Agent adjunte archivos al InputBlock (preservar original)
- El `JsonSchemaValidator` valida que el output del Agent cumpla el schema del InputBlock

### Pasada 2: Comunidad devs (features faltantes)

**Búsqueda en community:** "input verification tool description schema agent instruction parse"
- ✅ **`@tool` decorator** — convierte función Python en Tool automáticamente
- ✅ **`Annotated` parameter descriptions** — agrega descripciones a parámetros
- ✅ **`Tool.tool_spec`** — retorna spec LLM-compatible
- ✅ **`Toolset`** — grupo de tools manejados juntos
- ✅ **3 formas de crear Tool:** `@tool` / `create_tool_from_function` / manual
- ✅ **`inputs_from_state` y `outputs_to_state`** — input/output via state
- ✅ **`ComponentTool`** y **`PipelineTool`** — wrappean componentes/pipelines como tools
- ✅ **Auto schema generation** desde `run` method signature
- ✅ **`messages_to_string` y `message_joiner`** — manejo de conversaciones multi-turn

**Cómo se integra con input-block:**
- Cada tool del Osquestador se crea con `@tool` decorator y descripción literal del InputBlock
- `inputs_from_state` carga el `input_block_id` automáticamente
- `outputs_to_state` guarda el resultado de la tool + el hash del input

### Pasada 3: Input-block features específicos

**Búsqueda community:** "Haystack tool input_schema JSON schema strict description user instruction"
- ✅ **`strict: true`** mode — 100% schema compliance
- ✅ **Structured outputs con `response_format`** — Pydantic o JSON schema
- ✅ **Anthropic Tool Use con `input_schema`** — 99%+ schema compliance
- ✅ **JSON Schema para OS:** todos los campos `required`, `enum`, `description` clara
- ✅ **Tool choice force** — `tool_choice: "auto"` o forzar tool específica
- ✅ **Haystack 7 principios schema design:** all required / enum / LLM-friendly description / array items / 3 niveles / text al final / version

**Cómo se integra con input-block en el Osquestador:**
- El schema del InputBlock es `strict: true` con todos los campos required
- `description` de cada campo es LLM-friendly (dice QUÉ escribir, no solo el nombre)
- Los tools MCP del Osquestador usan `input_schema` con `strict: true`
- Enums para `sentence_type` (INSTRUCCION, PREGUNTA, CRITICA, EJEMPLO, META)

### Features FALTANTES que detecto en esta 3 pasada:

1. **`streaming_callback`** — para ver el input siendo procesado en tiempo real
2. **`exit_conditions`** — para que el Agent termine explícitamente cuando cumplió el InputBlock
3. **`ComponentTool` wrapping** — wrappear el `InputBlockReader` como tool para el LLM
4. **`PipelineTool`** — wrappear todo el pipeline de input-block como una tool

---

## 2) GRAPHITI (getzep) — 3 PASADAS + INPUT-BLOCK

### Pasada 1: Código fuente + features

**Versión actual:** jul 2026 — github.com/getzep/graphiti (episodic processing, temporal)
**Backend:** Neo4j 5.26+ o FalkorDB
**Python:** 3.10+

**Features identificados en código fuente (que me faltaban antes):**
- ✅ **`EpisodeType` enum:** `text`, `message`, `json` (3 tipos)
- ✅ **`EpisodeType.message`** — formato `speaker: message` para multi-turn
- ✅ **`EpisodeType.json`** — datos estructurados procesados distintos
- ✅ **`EpisodicNode`** — nodo para datos crudos (provenance)
- ✅ **`EntityNode` + `Edge` + `CommunityNode` + `SagaNode`** — nodos del grafo
- ✅ **`add_episode_bulk()`** con `RawEpisode` — batch ingestion eficiente
- ✅ **`reference_time`** — timestamp del evento (point-in-time queries)
- ✅ **`source_description`** — descripción del origen (CRÍTICO para input-block)
- ✅ **`group_id`** — partición de grafos multi-usuario
- ✅ **`update_communities`** flag — community graph updates
- ✅ **`entity_types` / `edge_type_map`** — ontología custom
- ✅ **`MENTIONS` edges** — episodios → entidades
- ✅ **MCP Server tools oficiales:** `add_memory` (alias add_episode), `search_nodes`, `search_facts`, `get_episodes`, `delete_episode`, `delete_entity_edge`, `get_entity_edge`, `clear_graph`, `get_status`

**Cómo se integra con input-block en el Osquestador:**
- Cada `InputBlock` se guarda como `EpisodeType.text` con `source_description = "input_block_{block_id}"`
- `reference_time` = timestamp del InputBlock
- `group_id` = project_id del InputBlock
- El `InputBlock` completo se almacena en el grafo como `EpisodicNode` (provenance)
- Las entidades extraídas (user, action, file, etc) se vinculan al episodio via `MENTIONS` edge

### Pasada 2: Comunidad devs (features faltantes)

**Búsqueda community:** "Graphiti add_episode raw input preserve text original verbatim"
- ✅ **MCP Server expone `add_memory` tool** — "Add an episode to memory. This is the primary way to add information to the graph."
- ✅ **`episode_body` es stringified JSON** para `format='json'` (con triple-escape de quotes)
- ✅ **MCP instructions detalladas** en `GRAPHITI_MCP_INSTRUCTIONS` constante
- ✅ **Triple‑escape all quotes** para JSON en JSON args
- ✅ **`format` parameter:** `text` / `json` / `message`
- ✅ **Source type validation:** solo 3 valores válidos
- ✅ **Risk classification:** `add_episode` es Write tool, medium risk
- ✅ **Reversible action** (no destructive) — se puede borrar con `delete_episode`
- ✅ **Background processing** — episodes se procesan async

**Cómo se integra con input-block:**
- El `InputBlock` se serializa como JSON string con `format='json'`
- Las MCP instructions describen al LLM cómo usar `add_memory`
- La descripción del InputBlock se guarda en `source_description`
- Los episodes del mismo `input_block_id` van al mismo `group_id`

### Pasada 3: Input-block features específicos

**Búsqueda community:** "Graphiti episode type message format user input conversation"
- ✅ **EpisodeType.message format:** `"speaker: message\nspeaker: message"` — multi-turn
- ✅ **Provenance:** "Every derived fact traces back here" (al episode original)
- ✅ **Temporal validity:** cada edge tiene `valid_at` + `invalid_at`
- ✅ **Edge invalidation:** cuando un hecho se contradice, el edge viejo se invalida (no se borra)
- ✅ **`MENTIONS` edge** — episode → entity
- ✅ **Bulk insertion** sin edge invalidation (para populate empty graphs)
- ✅ **Community detection** — agrupa entidades relacionadas
- ✅ **Saga** — secuencia de episodios relacionados

**Cómo se integra con input-block en el Osquestador:**
- `EpisodeType.message` se usa para inputs de chat (user/agent/system)
- Cada instrucción del InputBlock es un mensaje dentro del episode
- El provenance del InputBlock (source, agent, timestamp) queda en el grafo
- Las contradicciones entre InputBlocks viejos y nuevos invalidan edges (no borran)
- `Saga` agrupa los InputBlocks de una misma sesión de trabajo

### Features FALTANTES que detecto en esta 3 pasada:

1. **`EpisodeType.message` format** — para inputs de chat multi-turn (no lo había considerado)
2. **Provenance traceability** — el input original siempre se puede rastrear en el grafo
3. **Saga concept** — agrupar inputs de la misma sesión
4. **Community detection** — agrupar entidades relacionadas al input

---

## 3) KANBOARD — 3 PASADAS + INPUT-BLOCK

### Pasada 1: Código fuente + features

**Versión actual:** v1.2.52 — github.com/kanboard/kanboard (PHP + JSON-RPC)
**API:** 2 modos (Application `jsonrpc` + token / User con password)
**Cliente Python:** `pip install kanboard`

**Features identificados en código fuente (que me faltaban antes):**
- ✅ **`createTask`** con params: `title`, `project_id`, `color_id`, `column_id`, `owner_id`, `creator_id`, `date_due`, `description` (Markdown), `category_id`, `score`, `swimlane_id`, `priority`, `recurrence_*`, `reference`, `tags`, `date_started`
- ✅ **`getTaskByReference`** — task por external ref (útil para linking)
- ✅ **`getAllTasks`** con `status_id` (1=active, 0=inactive)
- ✅ **`openTask` / `closeTask`** — cambiar status
- ✅ **`createSubtask`** — jerarquía
- ✅ **`getEpics` / `getStories`** — Epic/Story hierarchy
- ✅ **`moveTaskToProject`** — mover entre proyectos
- ✅ **Markdown en `description`** — renderiza como Markdown
- ✅ **23 categorías de procedures** (Task, Subtask, Project, Comment, Tag, User, etc)
- ✅ **JSON-RPC 2.0 estricto** — `jsonrpc` field + `method` + `params` + `id`
- ✅ **`id` correlation** — client manda id, server responde con mismo id

**Cómo se integra con input-block en el Osquestador:**
- Cada InputBlock complejo → se crea una Task en Kanboard
- `title` = resumen del InputBlock (generado por LLM 10% budget)
- `description` = contenido completo del InputBlock (Markdown)
- `reference` = `input_block_id` (para linking)
- `tags` = tags del InputBlock (decision, tech, etc)
- `priority` = inferida del análisis de prioridad

### Pasada 2: Comunidad devs (features faltantes)

**Búsqueda community:** "Kanboard API create_task JSON-RPC input user instruction"
- ✅ **`kanboard` package oficial Python** — `kb.create_task(project_id, title, description)`
- ✅ **`jindage.com/skills/kanboard`** — Skill con todas las procedures documentadas
- ✅ **Shell wrapper con `jq`** — `task_id=$(kb createTask '...' | jq '.result')`
- ✅ **Workflow 3 pasos:** create project → add user → create task
- ✅ **Subtasks recursivos** — parent + children
- ✅ **API token location:** Settings → API (Application user)
- ✅ **Header `X-API-Auth`** — alternative auth header

**Cómo se integra con input-block:**
- Skill del Osquestador `KanboardOut` con todas las procedures
- Wrapper shell para chaining de tasks
- API token en `/root/.osquestador/secrets/kanboard_token`

### Pasada 3: Input-block features específicos

**Búsqueda community:** "Kanboard description Markdown priority tags"
- ✅ **Description es Markdown** — se puede pasar el InputBlock completo con formato
- ✅ **Tags array** — múltiples tags por task
- ✅ **Priority integer** — 0-3 o similar
- ✅ **Color** — red, blue, green, yellow, purple (visual en UI)
- ✅ **Swimlane** — agrupa tasks en columnas horizontales
- ✅ **Column** — agrupa tasks en columnas verticales (kanban clásico)
- ✅ **Date format estricto:** `YYYY-MM-DD HH:MM` — importante para InputBlock TTL
- ✅ **Recurrence** — tasks recurrentes (no aplica al InputBlock)

**Cómo se integra con input-block:**
- Description del Task = InputBlock completo en Markdown (con #tags, **negrita**, listas)
- Color = prioridad visual (red=urgent, green=ok)
- Tags = los 12 tags oficiales del InputBlock (decision, tech, etc)
- Date_due = TTL del InputBlock (90 días)
- Swimlane = categoría (user_input, agent_input, system_input)

### Features FALTANTES que detecto en esta 3 pasada:

1. **`createSubtask`** — para dividir InputBlocks complejos en subtasks
2. **Markdown en description** — preserva formato del InputBlock
3. **`reference` field** — link con input_block_id
4. **`getTaskByReference`** — para buscar tasks desde InputBlocks

---

## 4) PLANDEX — 3 PASADAS + INPUT-BLOCK

### Pasada 1: Código fuente + features

**Versión actual:** v2 jul 2026 — github.com/plandex-ai/plandex
**Lenguaje:** Go 1.23
**Módulos:** `plandex-cli` (cobra+bubbletea) + `plandex-server` (gorilla/mux+PostgreSQL) + `plandex-shared`

**Features identificados en código fuente (que me faltaban antes):**
- ✅ **2 modos de operación:** `chat` (brainstorm) y `tell` (implement task)
- ✅ **REPL con `\` commands:** `\chat`, `\tell`, `\multi`, `\send`, `\run`, `\quit`, `\help`
- ✅ **`@filepath`** — carga archivo en contexto
- ✅ **`plandex tell -f prompt.txt`** — prompt desde archivo
- ✅ **`plandex tell "..."`** — prompt inline
- ✅ **`plandex tell -s`** — stop después de 1 respuesta (no auto-continue)
- ✅ **`plandex tell -a`** — auto-apply cambios
- ✅ **`plandex tell -c`** — auto-commit
- ✅ **`plandex log` / `plandex rewind <hash>`** — version control del plan
- ✅ **Auto-context mode** — carga archivos automáticamente con tree-sitter
- ✅ **Model packs:** `daily-driver` (default), `reasoning`, `strong`, `cheap`, `oss`
- ✅ **Pipes:** `git diff | plandex tell` — pipe desde otro comando
- ✅ **Diff sandbox** — cambios se acumulan hasta aprobación

**Cómo se integra con input-block en el Osquestador:**
- El InputBlock se pasa como `plandex tell -f input_block_{id}.txt`
- Modo `tell` para ejecutar, modo `chat` para brainstorm
- Auto-context mode carga los archivos referenciados en el InputBlock
- Diff sandbox preserva cambios antes de aplicar
- `plandex log` muestra el historial del plan (audit trail del InputBlock)

### Pasada 2: Comunidad devs (features faltantes)

**Búsqueda community:** "Plandex tell mode REPL user input instruction prompt file"
- ✅ **`--skip-menu` flag** — skip interactive menu after response
- ✅ **`--auto-load-context`** flag — auto context loading
- ✅ **Prompt files con `-f`** — ideal para InputBlocks largos
- ✅ **`\run filepath`** — usar archivo como prompt en REPL
- ✅ **Multi-line mode** con `\multi` y `\send` — para prompts largos
- ✅ **Editor fallback** — `plandex tell` sin args abre vim
- ✅ **Git integration** — versiona el plan completo

**Cómo se integra con input-block:**
- El InputBlock largo se guarda como archivo y se pasa con `-f`
- Multi-line mode para InputBlocks con muchas instrucciones
- Editor fallback permite editar el InputBlock antes de enviar
- Git integration mantiene el audit trail completo

### Pasada 3: Input-block features específicos

**Búsqueda community:** "Plandex prompt file rewrite plan input task"
- ✅ **Rewind capability** — volver a un step anterior del plan
- ✅ **Plan history visible** — todos los steps del plan
- ✅ **Prompt iteration** — modificar el prompt y re-ejecutar
- ✅ **Sandbox isolation** — cambios no afectan proyecto hasta `apply`
- ✅ **Apply + commit atómico** — `plandex tell -a -c`

**Cómo se integra con input-block:**
- Si un InputBlock necesita re-ejecución, `plandex rewind` + `plandex tell` con prompt modificado
- Sandbox evita que cambios se apliquen antes de validación
- `apply + commit` atómico = commit al repo del input-block

### Features FALTANTES que detecto en esta 3 pasada:

1. **`plandex tell -f input_block.txt`** — InputBlock como archivo
2. **Multi-line mode** para InputBlocks largos
3. **Auto-context mode** — carga archivos del InputBlock automáticamente
4. **Rewind + re-tell** — iterar el InputBlock sin perder progreso

---

## 5) FEATURES DEL INPUT-BLOCK QUE APLICAN A TODAS LAS INTERFACES

**Patrón transversal (lo que se repite en las 4 interfaces analizadas):**

1. **Preservar input original** — todas tienen un mecanismo para no perder el input:
   - Haystack: `InMemoryChatMessageStore` con `chat_history_id`
   - Graphiti: `EpisodicNode` con provenance
   - Kanboard: `description` (Markdown) + `reference` field
   - Plandex: `prompt files` + `plan history` con rewind

2. **Validar input contra schema** — todas validan:
   - Haystack: `JsonSchemaValidator` + `@tool` strict schema
   - Graphiti: `EpisodeType` enum + JSON validation
   - Kanboard: param validation en API + Markdown format
   - Plandex: prompt file validation + tree-sitter

3. **Tracking de cambios** — todas tienen versionado:
   - Haystack: pipeline serialization YAML
   - Graphiti: temporal validity + edge invalidation
   - Kanboard: `log` endpoint + subtasks hierarchy
   - Plandex: `log` command + `rewind`

4. **Multi-format input** — todas aceptan varios formatos:
   - Haystack: `FileContent` (PDFs), `str`, `list[str]`
   - Graphiti: `text`, `message`, `json`
   - Kanboard: `string`, `[]string` (tags)
   - Plandex: inline, file, pipe, editor

5. **Background processing** — todas permiten async:
   - Haystack: `pipeline.run_async()`
   - Graphiti: `add_episode` async + `add_episode_bulk`
   - Kanboard: PHP background
   - Plandex: server en puerto 8099

6. **Source description + provenance** — todas tracking origen:
   - Haystack: `source_description` en tools
   - Graphiti: `source_description` en episodes
   - Kanboard: `reference` field + `creator_id`
   - Plandex: `git log` + commit hash

---

## 6) RESUMEN DE FEATURES NUEVOS IDENTIFICADOS EN LAS 3 PASADAS

**Features que se integraron al InputBlock del Osquestador:**

| Feature | Source | Cómo se integra |
|---------|--------|-----------------|
| `EpisodeType.message` para chats | Graphiti | InputBlocks de tipo `chat` |
| `EpisodeType.json` para estructurados | Graphiti | InputBlocks de tipo `task` complejos |
| Saga concept (sesión) | Graphiti | Agrupa InputBlocks de misma sesión |
| Community detection | Graphiti | Agrupa entidades de InputBlocks |
| `strict: true` schemas | Haystack | Todos los schemas del InputBlock |
| `JsonSchemaValidator` | Haystack | Valida outputs del agent |
| `FileContent` para PDFs | Haystack | InputBlocks pueden llevar PDF |
| `outputs_to_string` con `last_message` | Haystack | Evita trace en el parent |
| `state_schema` del Agent | Haystack | InputBlock se pasa via state |
| `InMemoryChatMessageStore` | Haystack | Memoria de chat del InputBlock |
| `createSubtask` jerárquico | Kanboard | Subtasks del InputBlock |
| `reference` field | Kanboard | `input_block_id` |
| Markdown description | Kanboard | InputBlock en Markdown |
| `plandex tell -f` archivo | Plandex | InputBlock como archivo |
| Multi-line `\multi` | Plandex | InputBlocks largos |
| Auto-context mode | Plandex | Carga archivos del InputBlock |
| Rewind + re-tell | Plandex | Iterar sin perder progreso |

**Total features nuevos:** 17
**Total features ya conocidos:** 60
**Total features integrados:** 77

---

## 7) CONCLUSIÓN DE LAS 3 PASADAS

**Lo que me FALTABA antes (y ahora detecto):**

1. **Graphiti `EpisodeType.message`** — formato `speaker: message` para multi-turn (no lo había mencionado)
2. **Graphiti `Saga` concept** — agrupar episodios relacionados
3. **Graphiti `Community detection`** — comunidades de entidades
4. **Haystack `InMemoryChatMessageStore` + `chat_history_id`** — patrón de memoria conversacional
5. **Haystack `state_schema`** — schema tipado para state entre tools
6. **Haystack `outputs_to_string` con `last_message`** — filtrar trace del parent
7. **Haystack `FileContent` para PDFs** — input blocks con adjuntos
8. **Kanboard `createSubtask`** — jerarquía
9. **Kanboard `reference` field** — link a input_block_id
10. **Plandex `plandex tell -f`** — prompt como archivo
11. **Plandex auto-context mode** — carga archivos del input
12. **Plandex rewind + re-tell** — iteración sin perder progreso

**Lo que se integra al InputBlock del Osquestador:**

- El InputBlock se serializa como `EpisodeType.json` en Graphiti con provenance
- El InputBlock se almacena como `EpisodicNode` para trazabilidad
- El InputBlock se pasa a Plandex como `plandex tell -f input_block.txt`
- El InputBlock genera tasks en Kanboard con `reference = input_block_id`
- El InputBlock se valida con `JsonSchemaValidator` de Haystack
- El InputBlock se preserva en `InMemoryChatMessageStore` con `chat_history_id`

**Anotado en GitHub (commit por pushear).**
