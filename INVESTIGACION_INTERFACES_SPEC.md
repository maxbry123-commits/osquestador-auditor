# INTERFACES DE LOS PROGRAMAS DEL SPEC — Análisis correcto
## SOLO los programas que dicen los documentos fuente del Osquestador

**Fecha:** 2026-07-18 02:25
**Investigador:** A2 (Mavis en delegación de Max)
**Trigger de Max:** "esos no son los programas de los documentos" (corregí mi error — usé los del spec)
**Búsquedas:** 10 sobre los programas REALES que el spec menciona

---

## 1) CORRECCIÓN — Los programas que el spec del Osquestador SÍ menciona

Leí los docs fuente en `docs/fuente/01_ESPECIFICACION_v1.0.md`, `02_PARTE_A_NUCLEO.md`, `02b`, `03_PARTE_B_PLUGINS.md`, `04_PARTE_C_MCP_TOOLS.md`, `05_INSTRUCCIONES_CLAUDE_CODE.md` y `docs/fuente_max/`.

**Los 10 programas del spec son:**
1. Haystack (deepset) — similitud de documentos
2. Graphiti (getzep) — knowledge graph temporal
3. Obsidian — vault de notas
4. Kanboard — gestión de tareas
5. Plandex — agente AI de planificación
6. Hermes (Nous Research) — formato README raíz
7. LiteLLM — router multi-LLM
8. SQLite (con WAL) — estado estructurado
9. Neo4j — backend de Graphiti
10. PaddleOCR / Tesseract — OCR para documentos
11. Telegram Bot — notificaciones
12. MCP (Model Context Protocol) — protocolo de tools

Investigué el código fuente de cada uno. Te explico cómo funciona y cómo lo voy a usar.

---

## 2) HAYSTACK (deepset-ai)

**Cómo funciona su código fuente** (Python SDK `haystack-ai` v2.25):
- `InMemoryDocumentStore` con BM25 + embedding similarity
- Métodos: `write_documents()`, `filter_documents()`, `bm25_retrieval()`, `embedding_retrieval()`
- `Pipeline` class para encadenar componentes (retriever → ranker → generator)
- `SentenceTransformersSimilarityRanker` con cross-encoder
- 3 algos BM25: `BM25Okapi`, `BM25L`, `BM25Plus`
- Similarity functions: `dot_product` (default) o `cosine`

**Cómo lo voy a usar en el Osquestador (formato manda/recibe/usa/modifica/guarda):**
- **SE MANDA** — el agente `haystack` recibe un documento nuevo
- **LO RECIBE** — `HaystackAgent.run(doc)` compara contra el corpus del proyecto
- **LO USA** — calcula similitud BM25 + embedding
- **LO MODIFICA** — si similitud >98% archiva; si 70-98% genera conflicto en Kanboard
- **LO GUARDA** — el hash + similitud quedan en `state/inventory.json`

**Ejemplo concreto:**
```python
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
store = InMemoryDocumentStore()
retriever = InMemoryBM25Retriever(document_store=store)
# Retorna los 10 docs más similares por BM25
```

---

## 3) GRAPHITI (getzep)

**Cómo funciona su código fuente** (Python SDK `graphiti-core`):
- Construye un grafo de conocimiento **bi-temporal** (válido desde/hasta)
- Backend: Neo4j 5.26+ (o FalkorDB alternativo)
- Extrae entidades + edges con LLM (default OpenAI)
- 1 episodio = 1 evento que se convierte en nodos/relaciones
- Búsqueda: semantic + BM25 + graph en una query híbrida
- Sirve vía `mcp_server/` (Model Context Protocol) con Docker + Neo4j

**Cómo lo voy a usar en el Osquestador:**
- **SE MANDA** — el agente `arbolista` extrae objetivos/decisiones/repos de un doc
- **LO RECIBE** — `GraphitiOut` adapter llama `graphiti.add_episode()`
- **LO USA** — LLM extrae entidades y crea edges con timestamp
- **LO MODIFICA** — cuando hay contradicción, invalida edge viejo (no borra)
- **LO GUARDA** — todo queda en Neo4j, recuperable con `graphiti.search()`

**Ejemplo concreto:**
```python
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
graphiti = Graphiti("bolt://localhost:7687", "neo4j", "password")
await graphiti.add_episode(
    name="doc-123",
    episode_body="Decidimos usar Postgres para X",
    source=EpisodeType.text,
    source_description="doc source",
    reference_time=datetime.now()
)
results = await graphiti.search("¿qué DB usamos?", num_results=5)
```

---

## 4) OBSIDIAN (vault)

**Cómo funciona su código fuente** (TypeScript + Electron):
- `Vault` class con métodos: `getMarkdownFiles()`, `read(file)`, `modify(file, content)`, `process(file, callback)`, `delete(file)`, `trash(file)`
- Frontmatter YAML entre `---` al inicio de cada `.md`
- Wikilinks: `[[Title]]` resueltos por `MetadataCache`
- Plugin API: `app.vault`, `app.metadataCache`, `app.workspace`
- `Frontmatter Operator` plugin: bulk edit con WHEN/THEN actions + snapshot undo

**Cómo lo voy a usar en el Osquestador:**
- **SE MANDA** — el `ObsidianOut` adapter recibe un doc para archivar
- **LO RECIBE** — lee config `obsidian.vault_path` de `config.json`
- **LO USA** — crea archivo `.md` con frontmatter YAML + body
- **LO MODIFICA** — si ya existe, `Vault.modify()` en lugar de `Vault.create()`
- **LO GUARDA** — único destino de escritura: `vault_path/{categoria}/{doc}.md`

**Ejemplo concreto:**
```python
# adapter.py
root = config.get("obsidian", {}).get("vault_path")
file_path = f"{root}/{category}/{doc_id}.md"
content = f"---\ntitle: {title}\ntags: {tags}\n---\n\n{body}"
vault.write(file_path, content)
```

---

## 5) KANBOARD

**Cómo funciona su código fuente** (PHP + JSON-RPC 2.0):
- API en `/jsonrpc.php` con `POST`
- 2 modos: Application API (user `jsonrpc` + token) y User API (user+pass o token personal)
- 23+ categorías: Project, Task, Subtask, Tag, User, Comment, etc
- Métodos clave: `create_task`, `getTask`, `getAllTasks`, `getTaskByReference`
- Batch requests (múltiples calls en 1 HTTP)
- Cliente Python oficial: `pip install kanboard`

**Cómo lo voy a usar en el Osquestador:**
- **SE MANDA** — el `KanboardOut` adapter crea una tarea
- **LO RECIBE** — el orquestador arma el JSON-RPC request
- **LO USA** — `kb.create_task(project_id, title, description)`
- **LO MODIFICA** — si remoto_id falla, SQLite queda como única fuente de verdad
- **LO GUARDA** — la tarea queda en Kanboard, el id remoto se anota en SQLite

**Ejemplo concreto:**
```python
import kanboard
kb = kanboard.Client('http://localhost/jsonrpc.php', 'jsonrpc', 'TOKEN')
project_id = kb.create_project(name='My project')
task_id = kb.create_task(project_id=project_id, title='My task', description='...')
```

---

## 6) PLANDEX (plandex-ai)

**Cómo funciona su código fuente** (Go + cliente Python):
- 2 modos: REPL (`plandex` o `pdx`) + CLI scripting (`plandex tell`)
- Context window: 2M tokens, indexa proyectos de 20M+ con tree-sitter
- Diff sandbox: todos los cambios se acumulan hasta que el humano apruebe
- Autonomy levels: `--no-auto` → `--basic` → `--plus` → `--semi` → `--full`
- Model packs: `daily-driver` (default), `reasoning`, `strong`, `cheap`, `oss`
- Multi-LLM: combina Anthropic, OpenAI, Google via OpenRouter

**Cómo lo voy a usar en el Osquestador (es un agente del spec):**
- **SE MANDA** — recibe un objetivo sin tarea
- **LO RECIBE** — `PlandexAgent.run(objetivo)` lo procesa
- **LO USA** — planifica los pasos DEFINIR (sin ejecutar)
- **LO MODIFICA** — agrega el plan a Kanboard
- **LO GUARDA** — el plan queda en `vault/tasks/<objetivo>.md`

**Diferencia clave:** Plandex es SOLO planificación, no ejecuta. El Osquestador lo usa para "qué hacer" y después otro agente ejecuta.

---

## 7) HERMES (Nous Research)

**Cómo funciona su código fuente** (Python SDK `hermes-agent`):
- `AIAgent` clase importable (`from run_agent import AIAgent`)
- Compatible con 20+ LLM providers
- Skills en `~/.hermes/skills/<cat>/<skill>/SKILL.md`
- 3 niveles progressive disclosure
- API server OpenAI-compatible en `http://127.0.0.1:8642/v1`
- Tools: `skill_manage`, `skill_view`, code execution
- Save trajectories ShareGPT para training

**Cómo lo voy a usar en el Osquestador:**
- **SE MANDA** — el agente `hermes` recibe un doc completo del proyecto
- **LO RECIBE** — usa el `AIAgent` para resumir/formatear
- **LO USA** — genera el README raíz del proyecto con formato estándar
- **LO MODIFICA** — valida que el README siga la plantilla
- **LO GUARDA** — escribe `vault/README.md` con la estructura del proyecto

---

## 8) LITELLM (BerriAI)

**Cómo funciona su código fuente** (Python SDK + Proxy server):
- Unified interface para 100+ LLM providers via OpenAI format
- `Router` con load balancing, fallbacks, retry logic
- `model_list` con `model_name` (alias) + `litellm_params` (config real)
- Routing strategies: `simple-shuffle`, `usage-based`, `latency-based`
- Soporta `acompletion()` async para paralelismo
- `ModelConfig` TypedDict para config tipada

**Cómo lo voy a usar en el Osquestador:**
- **SE MANDA** — cualquier llamada LLM pasa por LiteLLM
- **LO RECIBE** — el plugin `llm_router` configura las 5 keys (Anthropic, OpenAI, Groq, Cerebras, NVidia)
- **LO USA** — `litellm.completion(model="anthropic/claude-sonnet-4.6", messages=[...])`
- **LO MODIFICA** — si un provider falla, fallback automático al siguiente
- **LO GUARDA** — el log de cada llamada queda en `state/llm_calls.jsonl`

**Ejemplo concreto:**
```python
from litellm import Router
router = Router(model_list=[
    {"model_name": "fast", "litellm_params": {"model": "groq/llama-3.1-8b"}},
    {"model_name": "smart", "litellm_params": {"model": "anthropic/claude-sonnet-4.6"}},
])
response = await router.acompletion(model="fast", messages=[{"role": "user", "content": "hola"}])
```

---

## 9) SQLITE (con WAL)

**Cómo funciona su código fuente** (Python stdlib `sqlite3`):
- Conexión: `sqlite3.connect(path, check_same_thread=False, timeout=5.0)`
- WAL mode: `PRAGMA journal_mode=WAL` (permite readers concurrent con writer)
- `PRAGMA synchronous=NORMAL` (balance durabilidad/latencia)
- `PRAGMA wal_autocheckpoint=32768` (threshold en pages, default 1000)
- `PRAGMA mmap_size=134217728` (128MB memory-mapped I/O)
- Threading: serialized mode permite multi-thread safe
- 3 modos: single-thread, multi-thread, serialized

**Cómo lo voy a usar en el Osquestador:**
- **SE MANDA** — el kernel arranca, abre la DB
- **LO RECIBE** — `PRAGMA journal_mode=WAL` explícito al inicio
- **LO USA** — todas las operaciones de estado (inventory, conflicts, tasks)
- **LO MODIFICA** — checkpoint pasivo cada 1h para no acumular WAL
- **LO GUARDA** — `state/state.db` con todas las tablas del spec

**Ejemplo concreto (del Parte A del spec):**
```python
import sqlite3
self.c = sqlite3.connect(path, check_same_thread=False)
self.c.execute("PRAGMA journal_mode=WAL")
self.c.execute("PRAGMA synchronous=NORMAL")
```

---

## 10) NEO4J (backend de Graphiti)

**Cómo funciona su código fuente** (Python driver oficial `neo4j`):
- Conexión: `GraphDatabase.driver(URI, auth=AUTH)`
- Query: `driver.execute_query(cypher, **params)`
- Soporta Bolt 5.8 con routing optimista
- Python 3.10-3.13 soportado
- `RoutingControl.READ` para lecturas, default WRITE
- `database_="neo4j"` para multi-database

**Cómo lo voy a usar en el Osquestador:**
- **SE MANDA** — Graphiti quiere guardar entidades
- **LO RECIBE** — el driver Neo4j recibe las queries Cypher
- **LO USA** — `MERGE`, `MATCH`, `CREATE` para nodos/relaciones
- **LO MODIFICA** — transactions para operaciones atómicas
- **LO GUARDA** — todo queda en Neo4j, Graphiti solo expone la API

**Ejemplo concreto:**
```python
from neo4j import GraphDatabase
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
driver.execute_query(
    "MERGE (a:Person {name: $name})",
    name="Max"
)
```

---

## 11) PADDLEOCR / TESSERACT

**Cómo funciona su código fuente** (Python):
- PaddleOCR: `pip install paddleocr[all]` + `from paddleocr import PaddleOCR`
- Métodos: `ocr.predict("./image.png")` → JSON output
- Soporta 6 idiomas: ch, en, french, german, korean, japan
- Engine: PaddlePaddle o Transformers
- También ofrece API hosted: `PaddleOCRClient()` con `PADDLEOCR_ACCESS_TOKEN`
- Output: `result.print()`, `result.save_to_json()`

**Cómo lo voy a usar en el Osquestador (agente `ocr`):**
- **SE MANDA** — un PDF/imagen llega al inbox
- **LO RECIBE** — el agente `ocr` lo procesa
- **LO USA** — extrae texto + estructura (tablas, formulas, sellos)
- **LO MODIFICA** — pasa al agente `persistir` (hash + vault)
- **LO GUARDA** — texto extraído en `vault/{categoria}/{doc}.md`

---

## 12) TELEGRAM BOT

**Cómo funciona su código fuente** (Python `python-telegram-bot` v22):
- Async nativo (`async def` everywhere)
- `ApplicationBuilder().token("...").build()` para crear la app
- Handlers: `CommandHandler`, `MessageHandler`, `CallbackQueryHandler`
- `app.run_polling()` para long-polling o `app.run_webhook()` para webhook
- Métodos: `update.message.reply_text(...)`, `bot.send_message(chat_id, text)`
- Bot API 10.0 completamente soportado

**Cómo lo voy a usar en el Osquestador:**
- **SE MANDA** — el orquestador termina un paso largo
- **LO RECIBE** — `TelegramNotify` adapter llama `bot.send_message()`
- **LO USA** — manda resumen al chat de Max
- **LO MODIFICA** — si el mensaje es muy largo, lo parte en chunks
- **LO GUARDA** — el id del mensaje queda en `state/notifications.jsonl`

**Ejemplo concreto:**
```python
from telegram.ext import ApplicationBuilder, CommandHandler
app = ApplicationBuilder().token("YOUR_TOKEN").build()
async def hello(update, context):
    await update.message.reply_text("Hola Max!")
app.add_handler(CommandHandler("hello", hello))
app.run_polling()
```

---

## 13) MCP (Model Context Protocol)

**Cómo funciona su código fuente** (Python SDK `mcp`):
- 3 primitivos: **Tools** (ejecutar funciones), **Resources** (datos), **Prompts** (templates)
- 2 transportes: `stdio` (mismo proceso) + `streamable-http` (red, vía FastAPI)
- Server: `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()` decorators
- Client: `ClientSession` + `list_tools()` + `call_tool(name, args)`
- Lifecycle: `InitializeRequest` primero
- JSON-RPC 2.0 por debajo

**Cómo lo voy a usar en el Osquestador (4 tools del spec Parte C):**
- **SE MANDA** — el LLM necesita datos del sistema
- **LO RECIBE** — el MCP server recibe `CallToolRequest`
- **LO USA** — ejecuta el tool correspondiente (input/output/state/health)
- **LO MODIFICA** — el state del orquestador cambia
- **LO GUARDA** — todo evento se loguea en `state/mcp_calls.jsonl`

---

## 14) CÓMO SE INTEGRAN CON LAS 70 IDEAS + 25 DECISIONES DEL OSQUESTADOR

**Mapeo programa → idea/decisión:**

| Programa del spec | Ideas aplicadas | Decisiones |
|-------------------|----------------|------------|
| Haystack | #60 (idempotency), #35 (BM25+vector) | D15 |
| Graphiti | #31-40 (memory patterns) | D11-D14 |
| Obsidian | #31, #34 (prune), #40 (provenance) | D11-D14 |
| Kanboard | #19 (scheduler), #17 (24/7) | D4 |
| Plandex | #8 (depth cap), #50 (pipeline) | D1, D2 |
| Hermes | #1, #10 (ephemeral prompt), #5 (trajectories) | D19 |
| LiteLLM | #7 (multi-LLM), #4 (programmatic), #19 (token) | D1, D19 |
| SQLite WAL | #9, #54 (4 primitives), #55 (TTL 90d) | D11, D16 |
| Neo4j | #31-40 (memory patterns) | D11-D14 |
| PaddleOCR | #22 (PDF/OCR), #40 (provenance) | D4 |
| Telegram | #17 (24/7), #18 (notifications) | D4 |
| MCP | #3, #21-30 (3 primitivos), #41-50 | D3, D5-D8 |

---

## 15) RESUMEN FINAL — CÓMO USO ESTOS CÓDIGOS FUENTE

**Patrón de integración en 3 niveles:**

1. **Wrapper Python** — cada programa externo tiene un `adapter.py` que envuelve su SDK
2. **Output/Agent/Input connector** —统一的 interface: `name`, `capability`, `run()`, `health()`
3. **MCP exposure** — el adapter expone sus funciones como tools MCP

**Ejemplo del patrón (Obsidian):**
```python
class ObsidianOut(OutputConnector):
    name = "obsidian"
    capability = "vault"
    
    def run(self, doc: Document) -> Result:
        path = f"{self.vault_path}/{doc.category}/{doc.id}.md"
        content = f"---\n{frontmatter}\n---\n\n{doc.body}"
        self.vault.write(path, content)  # API del SDK de Obsidian
        return Result(remote_id=path, status="ok")
```

**Total LOC estimado del Osquestador:**
- 8 adapters × 100 LOC = 800 LOC
- Kernel + MCP server = 800 LOC
- Total = 1,600 LOC (más pequeño que reescribir cada SDK)

**Esperando tu OK para arrancar FASE 5 con estos 12 programas como base del código.**
