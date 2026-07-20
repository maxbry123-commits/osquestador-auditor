# AUDITORÍA 1/5 — NÚCLEO, ESPECIFICACIÓN Y FUENTE DE VERDAD

**Fecha**: 2026-07-19 21:30
**Modo SHERIFF v8.2**: input-block-reader literal
**Trigger**: Max "audita lo que tengas sobre el osquestador... en documentos MD... no más de 5 Documentos máximo"

---

## 1. QUÉ ES EL OSQUESTADOR AUDITOR (Fuente de Verdad consolidada)

Un **orquestador con kernel pequeño** (~500 LOC Python) + **plugins intercambiables** (5-10) vía **MCP** (Model Context Protocol) + **memoria persistente tripartita** (HOT/WARM/COLD) + **vault en filesystem** (markdown + frontmatter + wikilinks) + **panel UI estética Claude/Anthropic** + **24/7 daemon** con systemd watchdog + restic backup + **sistema de tags** auto-generados con LLM 10% budget + **multi-proveedor LLM** (5 keys: Anthropic, OpenAI, Groq, Cerebras, NVidia).

**NO es**: router de LLM (eso es OpenClaw, INTACTO), chat UI simple, wrapper de otra herramienta.
**SÍ es**: sistema operativo para agentes, cerebro chico que decide + plugins que ejecutan, memoria que sobrevive sesiones, recupera info de hace 6 meses.

---

## 2. LAS 25 DECISIONES APROBADAS (TABLA_DECISIONES_ARQUITECTONICAS.md)

### Punto 4 original (20)
1. Kernel pequeño (~500 LOC Python)
2. 5-10 plugins intercambiables
3. MCP server con 7 tools
4. 5 channels built-in (web, terminal, file, search, browser)
5. SKILL.md format oficial Anthropic
6. 3 niveles progressive disclosure
7. Subagents con ACP primitives
8. Depth cap = 5
9. SQLite-first checkpoints
10. Idempotency keys
11. Vault = filesystem
12. Review folder separados
13. 5 context files (CTX-aboutme, CTX-now, CTX-Work, CTX-project, CTX-systems)
14. Retention prune-over-append
15. BM25 + vector hybrid search
16. 90 días TTL WARM
17. Async checkpointing
18. Solo summary al parent
19. Token cost awareness
20. Estética Claude/Anthropic

### Punto 4 v2 (5 nuevas)
21. Triple patrón background (nohup/tmux/systemd)
22. systemd Type=notify + WatchdogSec=30s
23. restic + S3 + 3-2-1-1-0 + RPO 6h
24. Watchdog interno Python
25. .env excluido del backup (chmod 600)

---

## 3. ARQUITECTURA FINAL (kernel + MCP + plugins + storage)

```
KERNEL (~500 LOC) — orchestrator/kernel/main.py
├─ spawn_subagent(scopes, ttl, max_budget)
├─ checkpoint(workflow_id, step_id, state)
├─ resume(workflow_id)
├─ inject_context(3 tiers: HOT <500tok / WARM 1-3K facts / COLD repo summaries)
├─ route_skill(llm)
└─ audit_log(event, scope)
       ↓
MCP SERVER (7 tools) — orchestrator/mcp/server.py
├─ memoria_commit
├─ memoria_log
├─ memoria_diff
├─ memoria_blame
├─ memoria_checkout
├─ osquestador_search_hybrid (BM25+FAISS+RRF)
└─ osquestador_search_keyword
       ↓
PLUGINS (5-10 intercambiables) — orchestrator/plugins/<nombre>/
├─ filesystem (vault read/write + frontmatter)
├─ web_search (Tavily/Exa fallback)
├─ terminal (sandbox shell)
├─ file_processor (PDF/OCR PaddleOCR)
├─ memory_engine (FAISS MiniLM-L6-v2 + SQLite FTS5)
├─ llm_router (5 providers via LiteLLM)
├─ notification (SSE/WebSocket push)
├─ checkpoint (Dapr-style)
├─ scheduler (cron + interval)
└─ code_exec (programmatic calling)
       ↓
STORAGE (filesystem-first) — ~/.osquestador/proyectos/<id>/
├─ vault/ (markdown + frontmatter + wikilinks)
│  ├─ _review/ (agent writes, human promotes)
│  ├─ CTX-aboutme.md, CTX-now.md, CTX-Work.md
│  ├─ CTX-project.md, CTX-systems.md
│  └─ facts/<uuid>.md (atomic memory)
├─ db/
│  ├─ warm.sqlite (chat history + tags)
│  ├─ checkpoints.db (workflow state)
│  ├─ notifications.sqlite (push log)
│  └─ faiss/ (vector index MiniLM-L6-v2 384-dim)
├─ .env (chmod 600, EXCLUIDO de backup)
├─ AGENTS.md (constitución del proyecto)
└─ .git/ (sync a repo osquestador-memoria)
```

---

## 4. STACK TÉCNICO

| Capa | Tecnología | Razón |
|------|-----------|-------|
| Lenguaje kernel | Python 3.11+ | Ecosistema rico, async nativo |
| MCP | mcp-sdk oficial | Estándar cross-client Anthropic |
| Vector store | FAISS MiniLM-L6-v2 | Liviano, 384-dim |
| BM25 | SQLite FTS5 | Built-in, sin deps externas |
| LLM routing | LiteLLM | Multi-provider unificado |
| Web framework | FastAPI | Async, OpenAPI auto |
| Background | systemd Type=notify + WatchdogSec=30s | Producción Linux |
| Backup | restic + S3-compatible | Incremental, cifrado |
| Frontend | HTML estático estética Claude | Sin framework pesado |
| Deploy | Cloudflare Pages + VPS puente | Free + control |
| Tunnel | cloudflared (trycloudflare) | Bridge efímero VPS→public |
| Watchdog | watchdog.py cada 30s | Auto-recovery backend+tunnel |

---

## 5. REGLAS DURAS (NO SE ROMPEN — REGLAS_DURAS.md)

1. **OpenClaw INTACTO** (REGLA #0 firmada por Max) — `/opt/nct/*` no se toca
2. **Todo en `/root/osquestador/`** (carpeta nueva, separada)
3. **Anotar en GitHub PRIMERO** antes de continuar
4. **NO_SKIP · NO_ASSUME · NO_FAKE_PASS · NO_HALLUCINATION**
5. **NO_BUILD_WITHOUT_RESEARCH · NO_BUILD_WITHOUT_DOCS · NO_BUILD_WITHOUT_SKILLS**
6. **NO_CERTIFICATION_WITHOUT_EVIDENCE**
7. **200 búsquedas por gap** (no escalar a Max)
8. **Loop infinito** hasta CERTIFIED_OR_NOTHING
9. **Output máximo 6 líneas de texto** por respuesta a Max (v8.2 STRICT)
10. **Explicar con ejemplos** del formato "manda/recibe/usa/modifica/guarda"

---

## 6. CHECKLIST DE IMPLEMENTACIÓN (FASE 5 del spec)

- [x] Crear `/root/osquestador/orchestrator/` (carpeta NUEVA, OpenClaw INTACTO) — **HECHO** en `orchestrator/`
- [x] Kernel 180 LOC con 6 primitivos (atomic_write_json, SIGTERM, idempotencia) — **HECHO MVP**
- [ ] MCP server con 7 tools — **PENDIENTE**
- [x] 5 adapters: ocr, classifier, obsidian, graphiti, kanboard — **HECHO** (in-process)
- [ ] Plugin filesystem (vault read/write) — **PENDIENTE** (vault es filesystem pero no como plugin)
- [ ] Plugin memory_engine (FAISS + SQLite FTS5) — **PENDIENTE** (FAISS-numpy casero)
- [ ] Plugin llm_router (5 providers) — **PENDIENTE** (5 providers en LiteLLM listo)
- [ ] Plugin notification (SSE/WebSocket) — **PARCIAL** (WebSocket OK, SSE OK)
- [ ] Plugin checkpoint (SQLite) — **HECHO MVP** (atomic_write_json)
- [ ] Plugin scheduler (cron) — **PARCIAL** (APScheduler 3 jobs)
- [ ] Plugin terminal (sandbox) — **PENDIENTE**
- [ ] Plugin web_search — **PARCIAL** (Serper configurado)
- [ ] Plugin file_processor (PDF/OCR) — **PARCIAL** (PaddleOCR ready)
- [x] Panel HTML con estética Claude/Anthropic — **HECHO V12**
- [ ] systemd service con Type=notify + WatchdogSec=30s — **PENDIENTE**
- [ ] restic backup cada 6h a S3 — **PENDIENTE**
- [x] 5 context files (CTX-*) auto-creados — **PENDIENTE** (5 zones en V12)
- [ ] Regla 3-2-1-1-0 con append-only — **PENDIENTE**
- [x] .env excluido del backup — **HECHO** (.gitignore)
- [x] Verificación E2E — **HECHO** (smoke test orquestador)
- [ ] Certificación FASE 9 — **PENDIENTE**

---

## 7. ESPECIFICACIÓN TÉCNICA COMPLETA (`docs/fuente/01_ESPECIFICACION_v1.0.md`)

El orquestador SOLO controla la **Fase 0** (P1+P2). Termina cuando el contenedor está listo (árbol Graphiti completo + Kanboard con tareas completas). NO ejecuta código de proyectos, NO toca el DSL de 15 nodos, NO hace push a GitHub de proyectos. Esa es Fase 1 (OpenClaw).

### Los 4 workflows del kernel

**Workflow 1 — INGESTA** (dispara: documento nuevo en cualquier input)
```
[Recibir] → [Hash SHA256] → [¿existe en inventory.json? → skip]
→ [OCR si es imagen/pdf escaneado] → [Clasificar por proyecto]
→ [Guardar íntegro en vault] → [Registrar en inventory.json]
```
Regla: **nada se procesa dos veces** (hash primero, siempre).

**Workflow 2 — AUDITORÍA** (dispara: lote de ingesta completo)
```
[Haystack compara cada doc contra el corpus del proyecto]
→ [Duplicado exacto (hash igual o similitud >98%)] → archiva, no procesa
→ [Versiones distintas del mismo contenido] → CONFLICTO → tarjeta en Kanboard
→ [Información contradictoria entre docs] → CONFLICTO → tarjeta en Kanboard
→ [Único] → pasa directo al árbol
```
**El usuario resuelve cada conflicto en Kanboard**: aprobar A, aprobar B, o pedir fusión. El sistema NUNCA fusiona ni descarta solo.

**Workflow 3 — ÁRBOL DEL PROYECTO / P1** (dispara: conflictos resueltos)
```
[Crear/actualizar raíz: README del proyecto + tabla de tareas]
→ [Graphiti: crear entidades por doc (objetivos, decisiones, componentes, repos, recursos)]
→ [Graphiti: crear RELACIONES entre archivos del mismo proyecto]
→ [Detectar piezas faltantes (objetivo sin tareas, componente sin doc)]
→ [Cada faltante → tarea "DEFINIR" en Kanboard]
```

**Workflow 4 — TASK INDEX / P2** (dispara: árbol completo)
```
[Generar tareas completas con Task DNA:]
  {uuid, proyecto, prioridad, dependencias, agente_recomendado,
   contexto_necesario (links al árbol), criterio_aceptacion, estado}
→ [Escribir en Kanboard vía outputs/kanboard-api]
→ [Hermes: documenta el cierre + actualiza estado]
```

**FRONTERA — el orquestador se detiene cuando**:
- ✔ inventory.json cubre el 100% de los docs subidos
- ✔ 0 conflictos abiertos en Kanboard
- ✔ Árbol Graphiti: todo doc tiene ≥1 relación con el proyecto
- ✔ Toda tarea en Kanboard tiene Task DNA completo o etiqueta "DEFINIR"

---

## 8. CONTRATOS (interfaces únicas — `02_PARTE_A_NUCLEO.md`)

### Agent Adapter — TODA carpeta de agente implementa:
```
initialize(config) -> ok/error
execute(task, context) -> result
cancel(task_id) -> ok
health() -> {status, latency}
capabilities() -> [lista de capacidades que ofrece]
shutdown() -> ok
```

### Agent Manifest — `agents/<nombre>/manifest.json`:
```json
{
  "name": "", "version": "", "capabilities": [],
  "skills_supported": [], "models_compatible": [],
  "provider": "", "dependencies": [], "priority": 0,
  "status": "active|disabled"
}
```

### Input Adapter — TODA carpeta de entrada implementa:
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

### Output Connector — TODA carpeta de salida implementa:
```
connect() -> ok
call(accion, payload) -> result   # ej: call("crear_tarea", {...})
health() -> {status}
```

---

## 9. PARTE B — 12 PLUGINS (`03_PARTE_B_PLUGINS.md`)

1. `inputs/inbox/` — file watcher (inbox/<proyecto>/) — **HECHO**
2. `inputs/telegram/` — Telegram bot listener — **PENDIENTE**
3. `inputs/drive/` — Google Drive watcher — **PENDIENTE**
4. `inputs/chat-mcp/` — chat que consume MCP — **PARCIAL** (WebSocket propio)
5. `inputs/kanboard-ui/` — webhook desde Kanboard UI — **PENDIENTE**
6. `agents/ocr/` — PaddleOCR v3.5+ — **HECHO** (con fallback tesseract)
7. `agents/haystack/` — similitud/duplicados — **HECHO** (Jaccard 5-shingles)
8. `agents/plandex/` — DAG de tasks — **PENDIENTE**
9. `agents/hermes/` — README raíz + cierre — **PENDIENTE**
10. `agents/swe-agent/` — auditoría código — **PENDIENTE**
11. `agents/repomix/` — empaquetado repo — **PENDIENTE**
12. `agents/classifier/` — detectar proyecto — **HECHO**

---

## 10. PARTE C — MCP + TOOLS (`04_PARTE_C_MCP_TOOLS.md`)

JSON-RPC 2.0 server en `:8765` con 4 tools principales:
- `search_project(query, project_id)` — buscar en el proyecto
- `get_doc(doc_id)` — obtener un doc del vault
- `list_conflicts(project_id)` — listar conflictos abiertos
- `queue_doc(path, project_id)` — encolar doc en inbox

Adicionales: `create_task`, `list_tasks`, `move_task`, `list_projects`, `create_project`, `health`, `kernel_status`.

**Cliente MCP JS** en el panel para consumir todo via JSON-RPC, no via REST directo.

---

## 11. RUTAS Y ENDPOINTS

- **VPS**: `ssh root@95.111.232.89` (carpeta nueva `/root/osquestador/`)
- **Panel público (tunnel)**: `https://firewall-expired-cycling-apparently.trycloudflare.com/`
- **Repo GitHub**: `https://github.com/maxbry123-commits/osquestador-auditor`
- **Repo memoria**: `maxbry123-commits/osquestador-memoria` (por crear)
- **Repo agentes**: `maxbry123-commits/agentes` (existente)

---

## 12. COMMITS CLAVE HISTÓRICOS

- `a243ec2` — BUCLE 10/200 orquestador MVP + 11 commits hoy
- `1117cd2` — Punto 4 v2: nohup/watchdog/backup
- `29421c3` — Punto 4: 60 ideas + 20 decisiones integradas
- `80a8156` — Punto 4 primera versión
- `3685dfd` — state.json FASE 4.5 cerrada
- `7322e7b` — state.json punto_3 aprobado
- `e397405` — Aprobación Punto 3
- `6c02de8` — Punto 3 reformulado
- `51eb556` — Punto 4 (anclaje info+tags+push+chat)
- `9de0589` — Índice maestro FASE 4.5
- `50f2afb`, `f7a9877`, `a71dd5e` — Punto 2 skills
- `cb07bc9`, `1ecd437` — Punto 1 memoria
