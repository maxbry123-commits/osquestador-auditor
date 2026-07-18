# INVESTIGACION_COMUNIDAD.md — Patrones de uso por la comunidad de devs

**Investigación de cómo la comunidad usa Obsidian + Graphiti + AI/agentes como memoria + ventanas por proyecto + anti-alucinación.**
**Owner:** Mavis · **Fecha:** 2026-07-18 · **Sesión:** `418434919792827`

---

## Patrón #1 — Vault = carpeta de .md + wikilinks + frontmatter

**Fuente:** forum.obsidian.md (RTFM workflow) + bitsofchris.com + datasciencedojo.com + claude-blog.md

- El vault es solo una **carpeta de archivos markdown** locales con `[[wikilinks]]` + YAML frontmatter.
- Cualquier AI/agent lo lee directo via filesystem o MCP.
- El vault **ES** el contexto, no necesita base de datos extra.
- Plugin **Dataview** permite queries SQL-like sobre frontmatter.
- **Graph View** muestra hubs, orphans, conexiones.

**Aplicación al Osquestador:** `~/.osquestador/vault/<proyecto>/` con la misma estructura (markdown + frontmatter + wikilinks).

---

## Patrón #2 — AGENTS.md / CLAUDE.md = constitución del agente

**Fuente:** mindstudio.ai + claude-blog.md (claude-obsidian plugin) + Reddit r/ClaudeCode

- En la **raíz del vault** o por proyecto, un archivo `CLAUDE.md` o `AGENTS.md` define la constitución.
- Lo lee en cada sesión, sabe cómo comportarse en ese vault.
- Contiene: identidad, proyectos activos, decisiones finalizadas, reglas, session protocol.
- **SessionStart hook** lo carga automáticamente al inicio de cada sesión.

**Aplicación al Osquestador:** un `AGENTS.md` por proyecto en el vault, leído por el agente en cada invocación.

---

## Patrón #3 — Memory en capas (episódica / semántica / procedimiento)

**Fuente:** bitsofchris.com (augi) + Reddit r/ClaudeCode + bipi.in + atlan.com + AdMem (arXiv:2606.06787)

- `memory.md` = **índice breve, siempre en contexto** (qué hay, dónde está).
- Resúmenes de proyecto + daily notes = **lazy load** (solo si el tema es relevante).
- Un archivo por hecho importante = creado por el agente durante la conversación.
- Procedimientos/skills = **versionados**, recuperados por task signature.
- 3 tipos: **episódica** (eventos), **semántica** (hechos/entidades), **procedimiento** (workflows).

**Aplicación al Osquestador:** `~/.osquestador/memoria/{episodica,semantica,procedimiento}/` con RAG local (FAISS) y lazy load por proyecto.

---

## Patrón #4 — Lazy loading por proyecto = "ventanas separadas"

**Fuente:** Reddit r/ClaudeCode (comentario clave de un dev senior) + claude-obsidian + Graphiti Memory Operator docs

> "I identify the topic from my initial message and only retrieve the relevant project context. When I begin a session focused on a specific project, information from other projects remains unloaded."

- Claude/agent **NO lee todo al inicio** — identifica el tema del mensaje y solo carga el proyecto relevante.
- Aislamiento por:
  - **Vaults separados físicamente** (uno por proyecto) → más seguro
  - **Namespaces lógicos** (carpetas por proyecto con AGENTS.md propio) → más flexible
  - **Session ID en Graphiti** → ya soportado nativamente

**Aplicación al Osquestador:** cada proyecto = un namespace en Graphiti + carpeta propia en el vault + AGENTS.md propio. El orquestador enruta al namespace correcto al recibir el primer mensaje.

---

## Patrón #5 — MCP server para vault

**Fuente:** MarkusPfundstein/mcp-obsidian + azuma520/obsidian-graph-query + bitsofchris (augi) + community.obsidian.md (graph-context-for-claude-code) + qed42.com

- `mcp-obsidian` (MarkusPfundstein): expone **8 tools** sobre el vault via REST API del plugin Local REST API de Obsidian.
- `obsidian-graph-query` (azuma520): 7 templates JS para BFS, shortest path, connected components, Tarjan, degree, orphan scan, frontmatter relations — corre sobre `app.metadataCache.resolvedLinks` (índice live de Obsidian).
- `claude-obsidian` (AgriciDaniel): plugin Claude Code que implementa el **Karpathy LLM Wiki pattern** con `/wiki` command + vault pre-configurado.
- `recon`: MCP server que transforma conversaciones en knowledge graph con 10 tipos de nodos (personas, módulos, features, constraints) → CONTEXT.md por feature.
- `augi` (bitsofchris): pipeline ETL (`augi-update` + `augi-dispatch`) que extrae estructura + embeddings + tags + dispatch paralelo via tmux.
- `graph-context-for-claude-code`: plugin Obsidian que via Claude Code `/ide` envía el texto seleccionado + grafo expandido (embeds, wikilinks resueltos, heading path, frontmatter, backlinks) en un solo payload.

**Aplicación al Osquestador:** nuestro MCP server ya expone 4 tools del orquestador. Ampliamos a tools de vault (read/write/search) y graph (BFS, orphans, path) — propios, no copiando el código pero siguiendo el patrón.

---

## Patrón #6 — Anclaje AI ↔ Vault

**Fuente:** Reddit r/ClaudeCode + claude-obsidian + mindstudio.ai

- El agente se "ancla" al vault via AGENTS.md + MCP + filesystem.
- **Resultado:** sesiones nuevas empiezan con contexto completo (identidad, objetivos, decisiones) sin repetir nada.
- El agente escribe back al vault: cada sesión deja trazas (daily note, session summary, decisiones nuevas).
- **Loop cerrado:** lee → piensa → actúa → escribe → próximo agente lee.

**Aplicación al Osquestador:** el orquestador es el ancla. Cada agente que se conecta recibe AGENTS.md + memoria relevante + state.json. Después de ejecutar, escribe sus resultados al vault/memoria.

---

## Patrón #7 — Pipeline ETL de vault (augi-style)

**Fuente:** bitsofchris.com (augi)

- `augi-update` (ETL):
  - Extrae estructura del vault (tags, wikilinks, frontmatter, time metadata).
  - Crea embeddings (para RAG semántico).
  - Crea formato consumible por agentes.
  - Corre local.
- `augi-dispatch`:
  - Extrae tareas del vault (checkboxes, tags especiales).
  - Crea "task thread" por tarea con contexto relevante.
  - Lanza tmux session con Claude + acceso al MCP server del vault.
  - Paraleliza por tarea.

**Aplicación al Osquestador:** el orquestador tiene un agente `vault_etl` que corre antes del agente `auditor` (en el workflow de ingesta). Y un agente `dispatcher` que extrae tareas del vault + las pone en Kanboard.

---

## Patrón #8 — Project isolation (ventanas separadas por proyecto)

**Fuente:** Reddit r/ClaudeCode + Graphiti Memory Operator + bitsofchris + claude-blog.md

3 estrategias combinables:

1. **Vaults separados físicamente** — un vault por proyecto, máxima seguridad.
2. **Namespaces lógicos** — un vault con `proyecto-1/`, `proyecto-2/`, etc., cada uno con su AGENTS.md.
3. **Session ID / namespace en Graphiti** — ya soportado nativamente, aísla memoria por session_id o namespace.

**Aplicación al Osquestador:** combinación 2 + 3. Un vault único con carpetas por proyecto + namespaces en Graphiti por proyecto. El orquestador enruta al namespace correcto.

---

## Patrón #9 — Anti-alucinación

**Fuente:** Synthesized de Reddit r/ClaudeCode + mindstudio.ai + Augi + ATlan + bipi.in

- **Memoria persistente** entre sesiones (vault + DB) → nunca arranca en blanco.
- **Lazy loading** del contexto relevante → no se confunde con info de otro proyecto.
- **RAG local** sobre el vault → busca hechos reales antes de responder.
- **AGENTS.md** con identidad y reglas → no inventa contexto.
- **Verificación cruzada** (haystack auditor) → detecta conflictos entre versiones.
- **User feedback** (Kanboard) → tarjeta cuando hay duda, no resuelve solo.

**Aplicación al Osquestador:** la combinación de todo lo anterior + el agente `auditor` (de Haystack) que detecta conflictos + el agente `plandex` que crea tareas DEFINIR cuando hay gaps.

---

## Patrón #10 — Hot cache / index para RAG rápido

**Fuente:** claude-blog.md (claude-obsidian) + YouTube "Claude Code + Obsidian"

- Cada vault tiene un `wiki/hot.md` = **resumen sintetizado de todo el wiki**.
- El agente lee primero el `hot.md` como context set inicial.
- Después drill-down en `index.md` y páginas individuales.
- Latencia: hot.md = 1 lectura rápida, vs leer todo el vault (lento).
- 1-2 KB de resumen vs 1000+ notas = mucho más eficiente.

**Aplicación al Osquestador:** `~/.osquestador/memoria/indice/hot.md` por proyecto, regenerado por el agente `hermes` cada 24h.

---

## Herramientas MCP / plugins identificados para Fase 1 (referencia)

| Herramienta | Repo | Patrón que aplica |
|-------------|------|-------------------|
| `mcp-obsidian` | MarkusPfundstein/mcp-obsidian | Patrón #5 |
| `obsidian-graph-query` | azuma520/obsidian-graph-query | Patrón #5 |
| `claude-obsidian` | AgriciDaniel/claude-obsidian | Patrón #2 + #5 |
| `recon` | (Reddit thread) | Patrón #5 + #7 |
| `augi` | bitsofchris/augi | Patrón #7 |
| `graph-context-for-claude-code` | community.obsidian.md | Patrón #5 |
| `rtfm` | forum.obsidian.md (RTFM) | Patrón #1 |
| `Local REST API` (Obsidian plugin) | obsidian.md | Patrón #5 (backend) |
| `Dataview` (Obsidian plugin) | obsidian.md | Patrón #1 |
| `Graphiti` | getzep/graphiti | Patrón #3 + #4 + #8 |
| `Zep` | getzep | Patrón #4 (Context Lake) |

**Decisión:** estos son REFERENCIA para nuestro diseño. NO copiamos el código — seguimos el patrón con nuestra propia implementación en el orquestador.

---

## Resumen ejecutivo

La comunidad converge en **5 patrones arquitectónicos**:

1. **Vault = filesystem + markdown** → accesible por cualquier AI/agent.
2. **AGENTS.md + MCP** → ancla el agente al vault con constitución + tools.
3. **Memory en 3 capas** (episódica/semántica/procedimiento) → entre sesiones.
4. **Lazy loading por proyecto** → ventanas aisladas, sin alucinación.
5. **Anti-alucinación por triangulación** → memoria + RAG + verificación + user feedback.

**Implicación para el Osquestador:**
- El Orquestador implementa los 5 patrones.
- El vault vive en `~/.osquestador/vault/<proyecto>/` (filesystem real, NO copia de Obsidian).
- El MCP server del orquestador expone tools de vault + memoria + state.
- AGENTS.md por proyecto.
- Memoria tripartita en `~/.osquestador/memoria/`.
- Lazy loading por namespace en Graphiti.
- Auditor (haystack) + Plandex (DEFINIR) + Hermes (hot cache) + SWE (frontera) = los 4 agentes de soporte del patrón.

---

**Próxima búsqueda:** profundizar en hot cache patterns, RAG chunking, RAG retrieval ranking, Graphiti session_id, Obsidian CLI para queries.
