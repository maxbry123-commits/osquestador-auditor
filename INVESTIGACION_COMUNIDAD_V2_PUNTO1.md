# INVESTIGACIÓN COMUNITARIA V2 — PUNTO 1
## Memoria extendida: raíz temporal/permanente vía GitHub + DB separada por tarea/agente

**Fecha:** 2026-07-18
**Investigador:** A2 (Mavis en delegación de Max)
**Búsquedas realizadas:** 10 (5 prior + 5 de respaldo)
**Estado:** COMPLETO — listo para revisión de Max antes de pasar al Punto 2
**Constraint:** OpenClaw INTACTO (REGLA #0)

---

## Pregunta de Max
> "Sistema de memoria extendida — Osquestador como raíz de memoria temporal/permanente con GitHub como fuente, base de datos separada por tarea/agente sin mezclar info"

## Síntesis ejecutiva (5 bullets)
1. **Git es la mejor raíz de memoria permanente** — Letta Code Context Repositories, GitOfThoughts, mnem y GCC demuestran que tratar el repo como VCS de la memoria (cada thought/decision = commit, scores = notes, outcomes = tags) da auditabilidad, diff, merge y replay gratis.
2. **Tres sustratos de memoria se complementan, NO se reemplazan**: scratchpad efímero (working memory) + vault markdown navegable (semantic) + repo versionado (episodic/permanent). La raíz GitHub es el **log de eventos**; el vault es el **contenido navegable**; SQLite/Postgres por proyecto es el **índice de búsqueda**.
3. **Aislamiento por proyecto = namespace, no base de datos separada obligatoria**. Producción 2026 converge a: vector namespaces (Pinecone/Qdrant namespaces) + metadata `project_id`/`tenant_id` con filter obligatorio en cada query. Solo para regulated tenants (healthcare/finance) se justifica índice físico separado. Nuestra decisión: namespace + Postgres schema separado por proyecto (híbrido, balance costo/aislamiento).
4. **Memory tiering HOT/WARM/COLD con redistribución automática** es la práctica dominante 2026. HOT = <500 tokens working state; WARM = 1-3K facts estables; COLD = repo GitHub con summaries firmados. Trigger automático: cada `/compact`, cada 800 tokens HOT excedidos, cada fin de sesión.
5. **Project isolation por base de datos NO es exagerado para nosotros** — Max pidió "DB separada por tarea/agente sin mezclar info". El patrón Workspace-per-Tenant de Microsoft / zylos coincide. Patrón concreto: `~/.osquestador/db/<proyecto_id>/{episodica.sqlite, vault.sqlite, vector.faiss}` — un directorio = un proyecto, schema idéntico, datos incomunicados.

---

## Evidencia cruda (10 búsquedas)

### Búsqueda 1 — `memory split brain context engineering AI agent short term long term`
**Fuentes:** jatinbansal.com, max-gherman.dev, hidekazu-konishi.com, medium/@deolesopan, scribd/Context-Engineering-Anthropic
**Hallazgo clave:** "Working memory gives the harness a structured task state that can be updated and re-injected independently of chat history… It may use typed fields, a key-value store, a graph node, or a file." — 3 mecanismos composables: **Summarization (compaction)**, **Pruning (context editing)**, **Just-in-time retrieval**. Regla: *prune what can be re-fetched, summarize what cannot, retrieve rather than carry*. Cuarto mecanismo: **structured note-taking** (scratchpad file que sobrevive compactación y se reusa como bootstrap de la siguiente sesión).
**Aplicación al Osquestador:** el scratchpad es un archivo `.md` por sesión en `~/.osquestador/memoria/working/<session_id>.md`, cargado al inicio de cada turno, actualizado por el agente vía tool `scratchpad_write`. Al cerrar sesión, items durables se promueven a vault o se commitean al repo GitHub.

### Búsqueda 2 — `project isolation multi-tenant database agent workspace namespace`
**Fuentes:** fast.io, learn.microsoft.com (Azure), zylos.ai, dev.to/whoffagents
**Hallazgo clave:** Tres estrategias de aislamiento:
- **Row-level (shared schema, tenant_id predicate)** — más barato, más difícil de auditar
- **Schema isolation (shared DB, separate schema)** — balance
- **Database isolation (separate DB instance)** — máxima garantía, máximo costo
Patrón dominante 2026: **Workspace-per-Tenant** = cada operación de archivo linkeada a Workspace ID, cada chunk con metadata `tenant_id`, cada query al vector store filtrada por namespace. Production guidance de zylos: "Ephemeral workspace isolation is the first line… destroy in finally block on completion".
**Aplicación al Osquestador:** Workspace por proyecto = directorio físico. `~/.osquestador/proyectos/<project_id>/` contiene TODO del proyecto (vault, db, .env, logs, scratchpads). Al destruir proyecto: rm -rf + commit final al repo GitHub con tag `archive:<project_id>` antes de borrar.

### Búsqueda 3 — `Git repository as memory brain agent persistent state commit log`
**Fuentes:** arxiv.org/pdf/2606.14470 (GitOfThoughts), github.com/Uranid/mnem, arxiv.org/html/2508.00031 (GCC), reddit.com/r/AI_Agents (2y memory system), youtube.com Letta Code Context Repositories
**Hallazgo clave (oro puro):**
- **GitOfThoughts**: "Each scored thought is a commit with author, timestamp, and content-hash metadata; scores are git notes; validation outcomes are tags (success_*, failed_*); pruned attempts remain in history rather than vanishing." Retrieval = `git log --grep -S tag_filter`.
- **mnem**: "Skills, decisions, and conventions live as nodes and typed edges in a queryable knowledge graph inside your project's `.mnem/` directory. Commit it alongside your code… Forgetting is first-class: revoke a fact and every retrieval path filters it out automatically, with the audit trail preserved."
- **GCC (Git-Context-Controller)**: "COMMIT, BRANCH, MERGE, and CONTEXT operations… `.GCC/` directory. Each project maintains a global roadmap (main.md), while each branch contains its own commit summaries, execution traces, and structured metadata."
- **Letta Code Context Repositories**: "Memory edits are now tracked… you can see what the agent did to its own memory and roll it back."
- **Reddit 2-year report**: "Each conversation is treated as a commit. Enables the agent to: observe how its comprehension of entities has developed (using git diff); identify precisely when new information was acquired (with git blame); reconstruct its knowledge at any given moment (through git checkout)."
**Aplicación al Osquestador (mapeo directo):**
- Repo `osquestador-memoria` (separado de `osquestador-auditor`, separado de `agentes`) — un repo por proyecto MAX → un repo por agente-team (auditor/ocr/etc) o un repo monorepo con branches por proyecto
- Estructura: `main.md` = roadmap del proyecto, branches = sesiones o experimentos, commits = cada interacción significativa con metadata estructurada
- Tool del Osquestador: `memoria_commit(contenido, tags=[...], score=N)` → git commit con mensaje estructurado
- Tool: `memoria_log(query)` → `git log --grep <query>` o `git log -S <query>` o tag filter
- Tool: `memoria_blame(fact)` → `git blame` para "cuándo supiste esto"
- Tool: `memoria_checkout(timestamp)` → reconstruir conocimiento en momento dado

### Búsqueda 4 — `multi-tenant SaaS data isolation PostgreSQL row level security policy`
**Fuentes:** dev.to/whoffagents, learn.microsoft.com, learn.microsoft.com/azure
**Hallazgo clave:** Patrón RLS (Row-Level Security) en PostgreSQL = garantía a nivel DB de que un query no puede retornar filas de otro tenant. Implementación: `ALTER TABLE projects ENABLE ROW LEVEL SECURITY; CREATE POLICY tenant_isolation ON projects USING (organization_id = current_setting('app.current_tenant')::uuid);` + middleware que setea `SET app.current_tenant = 'org_123';` al inicio de cada request.
**Aplicación al Osquestador:** Para nuestro caso (no SaaS, sino proyectos de Max), usamos **schema isolation en SQLite** (un .sqlite por proyecto) en lugar de RLS. Más simple, cero riesgo de cross-query, y cada proyecto es portable como un solo archivo que se puede copiar/respaldar/borrar independientemente.

### Búsqueda 5 — `AI agent hot warm cold memory tier routing context budget`
**Fuentes:** clawrxiv.io (HWC architecture), armalo.ai/cortex, flumes.ai, agenticskillset.org, kunalganglani.com
**Hallazgo clave (consenso producción 2026):**
- **HOT tier** (in-context, sub-10ms, <500 tokens target, session-lifetime): estado de tarea activo, in-progress creds, preguntas sin resolver
- **WARM tier** (vector search, 50-200ms, 1-3K tokens, 14-90 días): summaries de sesiones recientes comprimidos por LLM, preferencias user, configs estables
- **COLD tier** (archivo, retrieval on-demand, ilimitado): log completo con summaries firmados, raw events comprimidos
- **Reglas de redistribución** (clawrxiv 4-step): Ingest & Audit → Tier Redistribution (HOT: próximos 2-3 turnos; WARM: facts estables; COLD: completado) → Pruning & Summarization → Verification
- **Triggers automáticos**: después de `/compact`, HOT >800 tokens, session start post-long-session
- **Reducción de costo**: tiering 3-tier puede cortar costos de memoria 3-4x sin perder recall
**Aplicación al Osquestador (mapeo directo):**
- HOT: en RAM del orquestador, rotación por session_id
- WARM: SQLite en `~/.osquestador/memoria/warm/<proyecto>.sqlite` con tabla `summaries(session_id, ts, summary, embedding)`
- COLD: GitHub repo `osquestador-memoria` (uno por proyecto o monorepo con directorios por proyecto), cada commit = snapshot firmado

### Búsquedas 6-10 (respaldo) — confirman los mismos patrones desde ángulos distintos
- **B6** (context engineering / Anthropic): scratchpad = "one approach to persist information while an agent is performing a task. The idea is to save information outside the context window so that it's available to the agent."
- **B7** (semantic search + tags): metadata + tags + entidades canónicas + sinónimos = base de retrieval que embeddings solos no dan
- **B8** (Obsidian community): vault como segundo cerebro, plugins AI que leen/escriben el vault completo, MCP servers que exponen el vault a agentes externos
- **B9** (progressive skill disclosure — Anthropic spec): "Level 1: Metadata (always in context) → Level 2: SKILL.md body (when triggers) → Level 3: Bundled resources (as needed)". 100 tokens por skill, 50 skills = 10K idle tokens.
- **B10** (database per tenant Azure): confirmación patrón — para enterprise con riesgo regulatorio se justifica DB física separada; para uso interno nuestro, schema/namespaces + workspace dirs es suficiente.

---

## Decisión de arquitectura propuesta (basada en evidencia)

### Estructura física del Osquestador
```
~/.osquestador/
├── proyectos/
│   ├── <proyecto_id>/                  # AISLAMIENTO TOTAL por proyecto
│   │   ├── vault/                      # markdown + frontmatter + wikilinks
│   │   │   ├── 00_INDICE.md
│   │   │   ├── 01_objetivos.md
│   │   │   ├── 02_decisiones.md
│   │   │   ├── 03_repos.md
│   │   │   ├── sesiones/<sesion_id>.md
│   │   │   └── working/<scratch>.md    # scratchpad efímero
│   │   ├── db/
│   │   │   ├── warm.sqlite             # summaries + facts (WARM tier)
│   │   │   ├── faiss/                  # embeddings por proyecto (namespace)
│   │   │   └── episodic.sqlite         # log crudo (queries, tool calls)
│   │   ├── .env                        # secrets del proyecto (chmod 600)
│   │   ├── AGENTS.md                   # constitución del agente para este proyecto
│   │   └── .git/                       # ← raíz Git LOCAL, sync a GitHub
│   └── <otro_proyecto>/                # CERO comunicación entre proyectos
├── memoria/
│   ├── hot/                            # en RAM, rotación por session
│   ├── warm/                           # SQLite global de facts cross-project (opcional, no default)
│   └── cold/                           # archivo long-term
├── secrets/                            # API keys global, chmod 600
└── orchestrator/                       # kernel + plugins
```

### Repo GitHub `osquestador-memoria` (raíz de memoria permanente)
- **Un repo monorepo** con `dirs/<proyecto_id>/` para cada proyecto de Max
- **Alternativa:** un repo por proyecto si los proyectos son muy dispares (auditor, agentes, etc) — más limpio pero más overhead de sync
- **Mi recomendación:** empezar monorepo, dividir si crece
- **Estructura de cada proyecto dentro del repo:**
  ```
  dir/<proyecto_id>/
  ├── README.md                    # main.md roadmap del proyecto
  ├── commits/<YYYY-MM-DD>/<hash>.md    # cada commit = un evento con metadata
  ├── branches/<branch_name>/      # experimentos / sesiones alternativas
  ├── tags/                        # success_*, failed_*, milestone_*
  └── notes/                       # git notes para scores, importance
  ```
- **Operaciones que el Osquestador expone al agente:**
  - `memoria_commit(content, type, tags, score)` → git commit
  - `memoria_log(query, since, until, tag_filter)` → git log con filtros
  - `memoria_diff(from, to)` → qué cambió entre dos puntos
  - `memoria_blame(fact)` → cuándo se supo esto
  - `memoria_checkout(timestamp)` → reconstruir estado pasado
  - `memoria_branch(name, from)` → explorar alternativa
  - `memoria_merge(branch, strategy)` → sintetizar caminos divergentes

### Aislamiento por proyecto: garantía
- **Filesystem:** directorios separados, permisos 700 por proyecto
- **DB:** un .sqlite por proyecto, sin foreign keys cross-project
- **Vectores:** FAISS namespace o Qdrant collection por proyecto
- **Git:** branch por proyecto O repo por proyecto
- **En el orquestador:** cuando un agente se conecta, recibe `project_id` en su context. Toda tool call validada contra `project_id` antes de ejecutar. Si pide acceso cross-project → rechazo explícito (no error genérico, mensaje claro).

### Memory tiering aplicado
- **HOT** = scratchpad en RAM + últimos 15-25 turnos de la sesión activa
- **WARM** = SQLite del proyecto, vector search, summaries comprimidos por LLM
- **COLD** = GitHub repo, summaries firmados, retrieval on-demand via `git log`
- **Redistribución automática** cuando: HOT >800 tokens, fin de sesión, o comando manual `osquestador memoria redistribuir`

### Agente aislado del Osquestador (qué ve al conectarse)
Cuando un agente (auditor, plandex, swe, etc) se conecta al Osquestador:
1. Recibe `osquestador://hello` con: nombre, project_id asignado, capabilities disponibles, scratchpad inicial vacío
2. Puede hacer tool calls vía MCP: `vault_read`, `vault_write`, `memoria_commit`, `memoria_log`, `scratchpad_set`, etc
3. **NO puede** acceder a otros proyectos ni a `~/.osquestador/secrets/` global
4. **NO puede** ejecutar shell arbitrary — solo tools validadas por el orquestador

---

## Métricas de éxito del Punto 1
- [ ] Estructura `~/.osquestador/proyectos/<id>/` creada y poblada con un proyecto de prueba
- [ ] Repo `osquestador-memoria` creado en GitHub (privado) y sincronizado
- [ ] SQLite por proyecto funcionando (warm + episodic)
- [ ] FAISS namespace por proyecto con embeddings del vault
- [ ] Tools `memoria_commit/log/diff/blame/checkout` implementadas y operativas vía MCP
- [ ] Test E2E: crear proyecto, escribir 10 events, hacer log con grep, hacer diff entre 2 commits → todos retornan resultados correctos
- [ ] Confirmar aislamiento: intentar cross-project access desde agente A a proyecto B → rechazado

## Riesgos identificados
1. **Costo de tokens en summaries LLM** — el tiering automático necesita LLM para comprimir. Mitigación: usar M2.5 (cerebras barato) o un modelo local pequeño.
2. **Sincronización GitHub** — push async para no bloquear el agente. Si GitHub cae, cola local y reintento.
3. **Vectores por proyecto a escala** — si hay 100+ proyectos, FAISS namespaces pueden ser problemáticos. Mitigación: shuffle por similarity cluster en COLD, lazy load.
4. **Conflictos de merge en branches** — agentes concurrentes al mismo proyecto. Mitigación: cada sesión usa su propia branch, merge al final.
5. **Repo crece sin límite** — mitigación: archival policy (COLD tier), garbage collection de summaries redundantes, rotation de logs raw.

---

## Próximo paso (esperando luz verde de Max)
- **Punto 2:** Sistema de anclaje de skills — repo `memoria` con índice de clasificación tipo bibliotecario, Osquestador inyecta skills paulatinamente a agentes conectados.

**¿Apruebas este Punto 1 para que pase al Punto 2?**
