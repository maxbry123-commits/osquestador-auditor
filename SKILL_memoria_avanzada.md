# SKILL: Memoria Avanzada en VPS (episódica + semántica + procedimiento)

## Objetivo
Implementar y mantener una **carpeta de memoria local en el VPS** con 3 tipos según el patrón cognitivo de Tulving/AdMem, accesible vía MCP desde el panel del Orquestador, con RAG local y consulta previa obligatoria antes de responder.

## Contexto
Investigación consolidada en `INVESTIGACION.md` sección 29.
Patrón validado por AdMem (arXiv:2606.06787), Mem0, Letta, Zep, y los hallazgos de atlan.com + bipi.in.

## Entradas
- Eventos del orquestador (ingesta, auditoría, resolución, deploy).
- Hechos extraídos de documentos (entidades, reglas, relaciones).
- Procedimientos aprendidos (workflows exitosos, errores y recovery).
- RAG query (texto → recupera los K más relevantes).

## Procedimiento

### 1. Estructura de carpetas
```
~/.osquestador/memoria/
├── episodica/          # eventos con timestamp (SQLite o JSONL)
│   └── 2026-07/
│       ├── eventos_2026-07-17.jsonl
│       └── ...
├── semantica/          # hechos y entidades (vector store + JSON)
│   ├── facts.json      # entidades + relaciones (Neo4j export o json-ld)
│   ├── embeddings/     # FAISS index
│   └── faiss.index
├── procedimiento/      # skills + workflows + recovery
│   ├── skills/
│   │   └── SKILL_<nombre>.md
│   ├── workflows/
│   │   └── WF_<nombre>.json
│   └── recovery/
│       └── RC_<escenario>.md
└── indice/             # índice RAG local
    └── rag_index.json
```

### 2. Reglas de escritura
- **Episódica**: cualquier evento del orquestador → append a `eventos_YYYY-MM-DD.jsonl` con `{ts, tipo, payload, hash_doc, proyecto}`.
- **Semántica**: SOLO con señal explícita (usuario confirma, fact con confidence > 0.8, agregación de N≥3 episodios). NUNCA desde una sola observación.
- **Procedimiento**: cuando un workflow termina OK → guardar en `procedimiento/workflows/WF_<hash>.json` con `{trigger, steps, duration, success_rate}`.

### 3. RAG local (consulta previa obligatoria)
- Antes de responder, ejecutar `rag_query(text)`:
  1. Calcular embedding del query (sentence-transformers o similar).
  2. Buscar top-K en FAISS (`semantica/faiss.index`).
  3. Cargar hechos completos de `semantica/facts.json`.
  4. Cargar últimos 5 eventos de `episodica/`.
  5. Buscar procedimientos por signature match.
  6. Combinar y devolver los K más relevantes con metadata.
- El orquestador **siempre** ejecuta RAG antes de generar una respuesta LLM (consulta previa obligatoria).

### 4. Auto-consolidación (Fase 1)
- Cada 24h, ejecutar consolidación:
  - Episódica → Semántica: agregar N≥3 eventos similares → fact con confidence.
  - Procedimiento: workflows ejecutados >5 veces con success_rate >0.9 → promover a SKILL.md.
- No borrar eventos (lineage).

## Reglas
- ✅ Cada escritura tiene hash SHA256 + timestamp UTC.
- ✅ El panel puede listar/editar/borrar con confirmación.
- ✅ Backup diario (cron: `0 3 * * * tar czf /backup/memoria-$(date +%F).tgz ~/.osquestador/memoria`).
- ❌ NUNCA escribir a semántica sin cumplir las 3 reglas (confirmación, confidence, agregación).
- ❌ NUNCA borrar eventos (siempre archivar, no delete).
- ❌ NUNCA exponer secrets en embeddings (PII filter antes de embed).

## Restricciones
- Tamaño máximo: sin límite duro, pero monitorear `du -sh ~/.osquestador/memoria` y avisar si > 10 GB.
- Latencia RAG: < 500ms para top-K=10 con FAISS local.
- Vector store: FAISS para Fase 0 (local, sin server extra). Migrar a Qdrant si > 1M embeddings.
- Encoding: UTF-8, JSON Lines para eventos (1 evento = 1 línea).

## Ejemplos

### Evento episódico
```json
{"ts":"2026-07-17T22:55:30Z","tipo":"ingesta","payload":{"hash":"abc123","proyecto":"maxbry","nombre":"DOC1.md","estado":"auditado"}}
```

### Hecho semántico
```json
{"id":"fact-001","tipo":"entidad","nombre":"OpenClaw","categoria":"software","atributos":{"version":"2026.6.11","puerto":18789,"protocolo":"WS+JSON-RPC"},"fuente":["abc123"],"confidence":0.95,"created_at":"2026-07-17T22:55:30Z"}
```

### Procedimiento
```json
{
  "id": "WF-resolver-conflicto",
  "trigger": "/resolver <id> A|B|FUSION",
  "steps": [
    {"id": "lookup", "action": "db.conf_resolver(id)"},
    {"id": "apply", "action": "db.inv_estado(hash, 'auditado') o 'archivado'"},
    {"id": "notify", "action": "outputs.call('notify', 'send')"}
  ],
  "success_rate": 0.98,
  "executions": 47
}
```

### RAG query
```python
def rag_query(text, k=10):
    q_emb = embedder.encode(text)
    D, I = faiss_index.search(q_emb, k)
    sem = [load_fact(i) for i in I[0]]
    epi = load_last_episodic(5)
    proc = match_procedure(text)
    return {"semantica": sem, "episodica": epi, "procedimiento": proc}
```

## Fuentes
- AdMem (arXiv:2606.06787) — https://arxiv.org/html/2606.06787v1
- bipi.in — https://bipi.in/blog/agent-memory-persistence-patterns
- atlan.com — https://atlan.com/know/types-of-ai-agent-memory/
- Tulving (1972) — semantic vs episodic memory (cognitive science base)
- FAISS — https://zilliz.com/comparison/qdrant-vs-faiss

## Dependencias
- Python 3.10+
- `sentence-transformers` (embeddings)
- `faiss-cpu` o `faiss-gpu`
- `sqlite3` (stdlib)
- ~500 MB de RAM para FAISS con 1M embeddings

## Cuándo utilizar
- Cualquier sistema que necesite recordar interacciones previas.
- Cuando el usuario pide "como la última vez" o "lo que hablamos ayer".
- Cuando el orquestador arranca después de un crash y necesita recuperar estado.
- Cuando el panel quiere mostrar "decisiones recientes" o "reglas aprendidas".

## Cuándo NO utilizar
- Datos efímeros que se borran al cerrar sesión (usar context window).
- Información clasificada o PII sin filtro previo.
- Sistemas con latencia crítica sub-100ms (RAG agrega 50-200ms).

## Relación con otros Skills
- `SKILL_orquestador_kernel.md` — el kernel escribe en memoria desde cada step.
- `SKILL_mcp_integration.md` — el panel consulta la memoria vía `search_project` + `get_doc`.
- `SKILL_panel_ui.md` — el panel muestra la memoria en una vista dedicada.

## Versión
v1.0 — 2026-07-17 · Mavis.

## Historial
- v1.0 — patrón AdMem + Tulving + Mem0/Letta/Zep + FAISS.
