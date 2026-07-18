# TABLA DE 20 DECISIONES ARQUITECTÓNICAS — FASE 4.5 Punto 4
## Aprobado por Max 2026-07-18 02:10

**Trigger literal de Max:** "aprobado integra las 60 ideas y 20 decisiones aprobado todo"
**Confirmación:** ✅ ANOTADO en GitHub (commit por pushear al final)

---

## 🏗️ 20 DECISIONES ARQUITECTÓNICAS CONSOLIDADAS

| # | Decisión | Fuente community | Razón | LOC estimadas |
|---|----------|------------------|-------|---------------|
| 1 | **Kernel pequeño (~500 LOC)** | Beam.ai: "Start simplest" | Mantenibilidad + fácil auditar | 500 |
| 2 | **5-10 plugins intercambiables** | Hermes toolsets | Modularidad + hot-swap | 200 c/u |
| 3 | **MCP server con 7 tools** | Claude Code + ACP | Estándar cross-client | 300 |
| 4 | **5 channels built-in** | OpenClaw best practices | Cubre 90% de casos uso | 150 |
| 5 | **SKILL.md format oficial** | Anthropic jul 2026 spec | Compatibilidad nativa | 100 |
| 6 | **3 niveles progressive disclosure** | Anthropic jul 2026 | Ahorro tokens | 200 |
| 7 | **Subagents con ACP primitives** | agenticcontrolplane.com | Costo controlado | 250 |
| 8 | **Depth cap = 5** | ACP default | Anti-explosión recursion | 50 |
| 9 | **SQLite-first checkpoints** | Google ADK | Zero-config por default | 400 |
| 10 | **Idempotency keys** | zylos + kunalganlani | Safe replay | 150 |
| 11 | **Vault = filesystem** | Obsidian 5 fuentes | Git-friendly, legible | 100 |
| 12 | **Review folder separados** | Mandalivia bilateral sync | Human-in-the-loop | 80 |
| 13 | **5 context files (CTX-*)** | Mandalivia pattern | Constitución modular | 50 |
| 14 | **Retention prune-over-append** | Letta best practices | Memory bounded | 120 |
| 15 | **BM25 + vector hybrid search** | fountaincity consensus | Recall + precision | 350 |
| 16 | **90 días TTL WARM** | checkpointing best practice | Storage bounded | 50 |
| 17 | **Async checkpointing** | Dapr pattern | No bloquea next step | 100 |
| 18 | **Solo summary al parent** | Hermes + Claude Code | Context protection | 80 |
| 19 | **Token cost awareness** | Claude Code 7x warning | Budget visible | 100 |
| 20 | **Estética Claude/Anthropic** | Lo que Max pidió | UX consistente | 0 (es UI) |

---

## 📐 ARQUITECTURA FINAL (consenso 60 ideas + 20 decisiones)

```
┌────────────────────────────────────────────────────────────┐
│ KERNEL (~500 LOC)                                          │
│ - spawn_subagent()  - checkpoint()  - resume()            │
│ - inject_context()  - route_skill() - audit_log()         │
└────────────────────────────────────────────────────────────┘
         ↓ MCP protocol (Decision 3, 5, 6)
┌────────────────────────────────────────────────────────────┐
│ MCP SERVER — 7 TOOLS                                       │
│ memoria_commit/log/diff/blame/checkout/branch/merge       │
│ osquestador_search_hybrid/keyword/vector/recent/tags       │
└────────────────────────────────────────────────────────────┘
         ↓ conectores
┌────────────────────────────────────────────────────────────┐
│ PLUGINS (5-10 intercambiables)                             │
│ 1. filesystem (vault read/write)         [Idea 31-40]     │
│ 2. web_search (Tavily/Exa)              [Idea 12]         │
│ 3. terminal (sandbox shell)             [Idea 12]         │
│ 4. file_processor (PDF/OCR)             [Idea 22]         │
│ 5. memory_engine (FAISS + SQLite)       [Idea 35]         │
│ 6. llm_router (5 providers)             [Idea 7]          │
│ 7. notification (SSE/WebSocket)         [Idea 17, 18]     │
│ 8. checkpoint (Dapr-style)              [Idea 51-60]      │
│ 9. scheduler (cron + interval)          [Idea 19]         │
│ 10. code_exec (programmatic calling)    [Idea 4]          │
└────────────────────────────────────────────────────────────┘
         ↓ storage
┌────────────────────────────────────────────────────────────┐
│ STORAGE (filesystem-first, Decision 11)                    │
│ ~/.osquestador/proyectos/<id>/                            │
│ ├── vault/ (markdown + frontmatter + wikilinks)           │
│ │   ├── _review/  (agent writes, human promotes)          │
│ │   ├── CTX-*.md (5 context files)                        │
│ │   ├── facts/<uuid>.md (atomic memory)                   │
│ │   └── 00_INDICE.md (auto-generated)                     │
│ ├── db/                                                   │
│ │   ├── warm.sqlite (chat history + tags)                 │
│ │   ├── checkpoints.db (workflow state)                   │
│ │   ├── notifications.sqlite (push log)                   │
│ │   └── faiss/ (vector index)                             │
│ ├── .env (chmod 600)                                      │
│ ├── AGENTS.md (constitución)                              │
│ └── .git/ (sync a osquestador-memoria)                    │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 MÉTRICAS DE LAS 20 DECISIONES

| Categoría | # decisiones | LOC total |
|-----------|--------------|-----------|
| Kernel core | 8 | ~2000 |
| Storage | 5 | ~500 |
| Sub-agents | 3 | ~400 |
| UI/UX | 1 | ~200 (HTML) |
| Search | 2 | ~450 |
| Hooks | 1 | ~150 |
| **TOTAL** | **20** | **~3,700 LOC** |

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN (FASE 5)

- [ ] Decisión 1: Kernel 500 LOC con 6 primitivos
- [ ] Decisión 2: 5-10 plugins intercambiables via MCP
- [ ] Decisión 3: MCP server con 7 tools
- [ ] Decisión 4-5: 5 channels + SKILL.md spec oficial
- [ ] Decisión 6: 3 niveles progressive disclosure
- [ ] Decisión 7-8: Subagents con ACP + depth cap
- [ ] Decisión 9-10: SQLite checkpoints + idempotency
- [ ] Decisión 11-13: Vault filesystem + review folder + 5 CTX files
- [ ] Decisión 14-16: Retention + hybrid search + 90d TTL
- [ ] Decisión 17-19: Async + summary-only + token awareness
- [ ] Decisión 20: Panel UI estilo Claude/Anthropic

---

**CONFIRMACIÓN DE ANOTACIÓN EN GITHUB:** Se commitea en este turno.
