# FUENTE DE LA VERDAD — OSQUESTADOR AUDITOR
## Documento único que define TODO lo que se va a hacer
**Aprobado por Max — 2026-07-18 02:14**

⚠️ **ESTE DOCUMENTO ES LA FUENTE DE LA VERDAD** ⚠️
Cualquier código, decisión o cambio DEBE coincidir con esto.
Si algo cambia, se actualiza ESTE documento PRIMERO, después el código.

---

## 1) QUÉ ES EL OSQUESTADOR AUDITOR

Un orquestador con:
- **Kernel pequeño** (~500 LOC) escrito en Python
- **Plugins intercambiables** (5-10) vía MCP (Model Context Protocol)
- **Memoria persistente** tripartita (HOT/WARM/COLD)
- **Vault en filesystem** (markdown + frontmatter + wikilinks)
- **Panel UI** con estética Claude/Anthropic
- **24/7 daemon** con systemd watchdog + restic backup
- **Sistema de tags** auto-generados con LLM 10% budget
- **Multi-proveedor LLM** (5 keys: Anthropic, OpenAI, Groq, Cerebras, NVidia)

**NO es:**
- ❌ Router de LLM (eso es OpenClaw, INTACTO)
- ❌ Chat UI simple
- ❌ Wrapper de otra herramienta

**SÍ es:**
- ✅ Sistema operativo para agentes
- ✅ Cerebro chico que decide + plugins que ejecutan
- ✅ Memoria que sobrevive sesiones
- ✅ Recupera info de hace 6 meses

---

## 2) DECISIONES APROBADAS (25 TOTALES)

### Del Punto 4 original (20)
1. Kernel pequeño (~500 LOC)
2. 5-10 plugins intercambiables
3. MCP server con 7 tools
4. 5 channels built-in
5. SKILL.md format oficial Anthropic
6. 3 niveles progressive disclosure
7. Subagents con ACP primitives
8. Depth cap = 5
9. SQLite-first checkpoints
10. Idempotency keys
11. Vault = filesystem
12. Review folder separados
13. 5 context files (CTX-*)
14. Retention prune-over-append
15. BM25 + vector hybrid search
16. 90 días TTL WARM
17. Async checkpointing
18. Solo summary al parent
19. Token cost awareness
20. Estética Claude/Anthropic

### Del Punto 4 v2 (5 nuevas)
21. Triple patrón background (nohup/tmux/systemd)
22. systemd Type=notify + WatchdogSec=30s
23. restic + S3 + 3-2-1-1-0 + RPO 6h
24. Watchdog interno Python
25. .env excluido del backup

---

## 3) 70 IDEAS INTEGRADAS (resumen por fuente)

- **10 ideas de Hermes** (Nous Research) — AIAgent librería, async subagents, code execution, save trajectories
- **10 ideas de OpenClaw** — ClawHub marketplace, 5 channels, mayordomo pattern
- **10 ideas de Claude Code oficial** — SKILL.md spec, progressive disclosure, hooks, subagents
- **10 ideas de Memory patterns** — vault filesystem, 5 CTX files, BM25+vector hybrid
- **10 ideas de Sub-agents** — Orchestrator-worker, ACP primitives, depth cap
- **10 ideas de Checkpoint** — SQLite-first, idempotency keys, 4 primitives
- **10 ideas ADICIONALES (Punto 4 v2)** — triple background, watchdogd, restic, append-only, etc.

---

## 4) ARQUITECTURA FINAL

```
KERNEL (~500 LOC)
├─ spawn_subagent(scopes, ttl, max_budget)
├─ checkpoint(workflow_id, step_id, state)
├─ resume(workflow_id)
├─ inject_context(3 tiers)
├─ route_skill(llm)
└─ audit_log(event, scope)
       ↓
MCP SERVER (7 tools)
├─ memoria_commit
├─ memoria_log
├─ memoria_diff
├─ memoria_blame
├─ memoria_checkout
├─ osquestador_search_hybrid
└─ osquestador_search_keyword
       ↓
PLUGINS (5-10 intercambiables)
├─ filesystem (vault read/write)
├─ web_search (Tavily/Exa)
├─ terminal (sandbox shell)
├─ file_processor (PDF/OCR)
├─ memory_engine (FAISS + SQLite)
├─ llm_router (5 providers)
├─ notification (SSE/WebSocket)
├─ checkpoint (Dapr-style)
├─ scheduler (cron + interval)
└─ code_exec (programmatic calling)
       ↓
STORAGE (filesystem-first)
~/.osquestador/proyectos/<id>/
├─ vault/ (markdown + frontmatter + wikilinks)
│  ├─ _review/ (agent writes, human promotes)
│  ├─ CTX-aboutme.md, CTX-now.md, CTX-Work.md
│  ├─ CTX-project.md, CTX-systems.md
│  └─ facts/<uuid>.md (atomic memory)
├─ db/
│  ├─ warm.sqlite (chat history + tags)
│  ├─ checkpoints.db (workflow state)
│  ├─ notifications.sqlite (push log)
│  └─ faiss/ (vector index)
├─ .env (chmod 600, EXCLUIDO de backup)
├─ AGENTS.md (constitución)
└─ .git/ (sync a osquestador-memoria)
```

---

## 5) STACK TÉCNICO

| Capa | Tecnología | Razón |
|------|-----------|-------|
| Lenguaje kernel | Python 3.11+ | Ecosistema rico, async nativo |
| MCP | mcp-sdk oficial | Estándar cross-client |
| Vector store | FAISS MiniLM-L6-v2 | Liviano, 384-dim |
| BM25 | SQLite FTS5 | Built-in, sin deps |
| LLM routing | LiteLLM | Multi-provider unificado |
| Web framework | FastAPI | Async, OpenAPI auto |
| Background | systemd + watchdogd | Producción Linux |
| Backup | restic + S3-compatible | Incremental, cifrado |
| Frontend | HTML estático (estética Claude) | Sin framework pesado |
| Deploy | Cloudflare Pages + VPS | Free + control |

---

## 6) CHECKLIST DE IMPLEMENTACIÓN (FASE 5)

- [ ] Crear `/root/osquestador/orchestrator/` (carpeta NUEVA, OpenClaw INTACTO)
- [ ] Kernel 500 LOC con 6 primitivos
- [ ] MCP server con 7 tools
- [ ] Plugin filesystem (vault read/write)
- [ ] Plugin memory_engine (FAISS + SQLite FTS5)
- [ ] Plugin llm_router (5 providers)
- [ ] Plugin notification (SSE/WebSocket)
- [ ] Plugin checkpoint (SQLite)
- [ ] Plugin scheduler (cron)
- [ ] Plugin terminal (sandbox)
- [ ] Plugin web_search
- [ ] Plugin file_processor
- [ ] Plugin code_exec
- [ ] Panel HTML con estética Claude/Anthropic
- [ ] systemd service con Type=notify + WatchdogSec=30s
- [ ] restic backup cada 6h a S3
- [ ] 5 context files (CTX-*) auto-creados
- [ ] Regla 3-2-1-1-0 con append-only
- [ ] .env excluido del backup
- [ ] Verificación E2E
- [ ] Certificación FASE 9

---

## 7) RUTAS Y ENDPOINTS

- **VPS:** `ssh root@95.111.232.89` (carpeta nueva `/root/osquestador/`)
- **Panel:** `https://b3fd4742.m3-vps-chat.pages.dev/`
- **Repo GitHub:** `https://github.com/maxbry123-commits/osquestador-auditor`
- **Repo memoria:** `maxbry123-commits/osquestador-memoria` (por crear)
- **Repo agentes:** `maxbry123-commits/agentes` (existente)

---

## 8) REGLAS DURAS (NO SE ROMPEN)

1. **OpenClaw INTACTO** (REGLA #0 firmada en REGLAS_DURAS.md)
2. **Todo en `/root/osquestador/`** (carpeta nueva)
3. **Anotar en GitHub PRIMERO** antes de continuar
4. **NO_SKIP / NO_ASSUME / NO_FAKE_PASS / NO_HALLUCINATION**
5. **NO_BUILD_WITHOUT_RESEARCH / NO_BUILD_WITHOUT_DOCS / NO_BUILD_WITHOUT_SKILLS**
6. **NO_CERTIFICATION_WITHOUT_EVIDENCE**
7. **200 búsquedas por gap** si es necesario
8. **Loop infinito** hasta CERTIFIED_OR_NOTHING
9. **Output máximo 8 líneas de texto** por respuesta a Max
10. **Explicar con ejemplos** del formato "manda/recibe/usa/modifica/guarda"

---

## 9) COMMITS CLAVE DE LA HISTORIA

- `1117cd2` — Punto 4 v2: nohup/watchdog/backup
- `29421c3` — Punto 4: 60 ideas + 20 decisiones integradas
- `80a8156` — Punto 4 primera versión
- `3685dfd` — state.json FASE 4.5 cerrada
- `7322e7b` — state.json punto_3 aprobado
- `e397405` — Aprobación Punto 3
- `6c02de8` — Punto 3 reformulado
- `51eb556` — Punto 4 (anclaje info+tags+push+chat)
- `1bdcc71`, `26a570c` — Punto 3 capability
- `9de0589` — Índice maestro FASE 4.5
- `6f74b4b`, `50f2afb`, `f7a9877`, `a71dd5e` — Punto 2 skills
- `cb07bc9`, `1ecd437` — Punto 1 memoria

---

## 10) FECHA DE PRÓXIMA ACCIÓN

**FASE 5 — Programación código real**
- Carpeta: `/root/osquestador/orchestrator/`
- Primer archivo: `kernel/orchestrator.py` (estructura vacía + 6 primitivos)
- Estimado: 3,700 LOC totales, 10-15 archivos Python

---

**FIN DEL DOCUMENTO**
**Este archivo es la fuente de verdad. Si algo cambia, actualizar PRIMERO este archivo.**
