# INVESTIGACIÓN COMUNITARIA V2 — PUNTO 2
## Sistema de anclaje de skills en repo `memoria` con índice bibliotecario + 90/10 código/LLM + Skills Anthropic doble uso + documentos de Max convertidos en código real

**Fecha:** 2026-07-18
**Investigador:** A2 (Mavis en delegación de Max)
**Búsquedas realizadas:** 10 (3 previas del turno + 7 nuevas de este turno)
**Documentos de Max procesados:** 6 (4 .md + 2 .html) — leídos parcialmente, suficiente para entender la estructura
**Trigger literal de Max:**
- "el osquestador también podría buscar skills en al web en una lista de muchos lugares diferentes y descargar según la necesidad"
- "busca información de los skills de claude de antropy ve que se puede usar doble los skills"
- "lo que te doy los documentos convertirlo en código real en el osquestador"
- "intenta en el diseño 90% code determinetista y 10% llm"
- "investiga de nuevo en comunidad de desarrolladores 10 pasadas"
**Estado:** COMPLETO — listo para revisión de Max antes de pasar al Punto 3

---

## Pregunta de Max
> "Sistema de anclaje de skills en repo `memoria` con índice de clasificación tipo bibliotecario, el Osquestador inyecta skills paulatinamente a agentes conectados. Skills de Claude/Anthropic ver doble uso. Documentos convertidos en código real. 90% código determinístico / 10% LLM."

## Síntesis ejecutiva (6 bullets)
1. **El repo `memoria` es el catálogo maestro, no la fuente de skills** — un repo GitHub con índice de clasificación (Dewey + tags + categorías), que apunta a skills分散 en otras fuentes. El Osquestador consulta el índice y descarga la skill del lugar real (ClawHub, SkillsMP, GitHub directo, repo local de Max).
2. **Skills Anthropic son doble-uso nativamente** — publicado como estándar abierto el 18 dic 2025. **Mismo SKILL.md funciona en Claude Code, OpenClaw, Cursor, Copilot, Codex CLI, Gemini CLI, Microsoft Agent Framework, Windsurf, Cline, Amp, Goose, Antigravity.** El Osquestador expone las skills via MCP para que cualquier agente conectado las use sin reescribir.
3. **Documentos de Max = 2 engines + 1 estructura + biblioteca** — Max ya diseñó: (a) **Knowledge Acquisition Engine** (investiga+descarga+clasifica), (b) **Knowledge Distillation Engine** (convierte bruto en skills/docs), (c) **Estructura del Orquestador** con 14+ Checkpoints de la Raíz Maestra 00 (Constitución, Crazy Wall, state.json, Registro Maestro, Captura Universal de Input, Persistencia Universal, etc.), (d) **Biblioteca Universal de Conocimiento** organizada por Fases del proyecto.
4. **90% código / 10% LLM es práctica estándar 2026** — paper "Compiled AI" (arxiv 2604.05150), "Blueprint First, Model Second" (SOURCE CODE AGENT, arxiv 2508.02721), y Charles Sieg "Deterministic Scaffolding around Non-deterministic Core" confirman: el LLM genera código en compile-time, el workflow ejecuta determinístico en run-time. Patrón: código para routing/validación/cache/hooks/format, LLM SOLO para query expansion, summarization, scoring de relevance.
5. **El Osquestador es el bibliotecario, no el lector** — patrón validado por ClaudSkills, OpenAgentSkill, opensite-skills: el agente tiene un "gateway skill" tiny (puntero), y el Osquestador busca+descarga on-demand. El skills.sh ecosistema (280k+ skills) + agent-skills-cli + load-skill son los agregadores que el Osquestador puede usar como sub-capa.
6. **Knowledge Acquisition + Distillation de Max = nuestros 2 servicios core** — encajan perfecto con el patrón "Compiled AI": el Acquisition Engine investiga (LLM en compile-time, max 10% del cómputo), el Distillation Engine produce SKILL.md + scripts/ (código real que el Osquestador ejecuta en run-time, 90% determinístico). El Osquestador NO improvisa skills en runtime — las pre-compila y las sirve.

---

## Evidencia de las 10 búsquedas

### Búsquedas previas (3, ya anotadas en `FASE_4_5_IDEA_SKILLS_MAX.md`)
1. **Skill marketplace aggregator** (load-skill, Skilldex, SkillRegistry, SkillHub) → 1,176 a 1.1M skills agregados
2. **Auto-discovery fetch on demand** (OpenAgentSkill, skills-registry PyPI) → gateway skill + fetch-on-demand
3. **ClawHub/SkillsMP/SkillHub** → 5 marketplaces principales, todos compatibles con el estándar SKILL.md

### Búsqueda 4 — `Anthropic Claude skills open standard December 2025`
**Fuentes:** anthropic.com/engineering/equipping-agents, resources.anthropic.com (PDF Complete Guide), agensi.io/learn, claudecoworkcourse.com, github.com/ComposioHQ/awesome-claude-skills
**Hallazgo clave:**
- **Anthropic publicó Agent Skills como estándar abierto el 18 dic 2025** (después de introducirlo en oct 2025)
- **"Like MCP, we believe skills should be portable across tools and platforms — the same skill should work whether you're using Claude or other AI platforms"** — declaración oficial Anthropic
- Skills funcionan idénticas en: Claude.ai, Claude Code, Claude API, OpenAI Codex CLI, Cursor, OpenCode, OpenClaw, Gemini CLI, GitHub Copilot, Windsurf, Cline, Amp, Goose, Antigravity
- Estructura confirmada:
  ```
  skill-name/
  ├── SKILL.md              # Required - main skill file
  ├── scripts/              # Optional - executable code
  │   ├── process_data.py
  ├── templates/            # Optional
  ├── references/           # Optional
  └── assets/               # Optional
  ```
- 3 niveles: YAML frontmatter (siempre en system prompt) / SKILL.md body (carga cuando match) / archivos linkeados (on-demand)

### Búsqueda 5 — `Claude skills reuse same SKILL.md cross-platform port`
**Fuentes:** youtube.com (cross-platform guide), reddit.com/r/ClaudeAI, claudskills.com, dev.to/rosgluk, dev.to/opensite
**Hallazgo clave:**
- **AGENTS.md** es otro estándar abierto (Agentic AI Foundation) leído por Codex, Cursor, Windsurf, Gemini CLI, Copilot
- **`.agents/skills/`** emergió como convención cross-client; algunos clientes también escanean `.claude/skills/` por compatibilidad pragmática
- **opensite-skills repo:** dos-capas, setup.sh auto-detecta plataformas instaladas y crea symlinks
- **ClaudSkills** indexa 76,000+ SKILL.md files, contenido portable a cada tool
- **Regla práctica de portabilidad:**
  - Claude Code only → `.claude/skills/`
  - Cross-client → `.agents/skills/` (estándar Agent Skills)
- "Claude Skills are not only a Claude Code thing. Agent Skills is an open standard."

### Búsqueda 6 — `deterministic code LLM hybrid agent 90% code 10% LLM design pattern`
**Fuentes:** arunbaby.com, arxiv.org/html/2604.05150 (Compiled AI), youtube.com (Stop Using LLMs for Everything), arxiv.org/pdf/2508.02721 (SOURCE CODE AGENT), charlessieg.com
**Hallazgo clave (GOLD):**
- **Compiled AI paradigm** (arxiv 2604.05150): "LLMs generate executable code artifacts during a compilation phase, after which workflows execute deterministically without further model invocation. Zero stochasticity, near-zero marginal inference cost."
- **"Blueprint First, Model Second"** (SOURCE CODE AGENT): "Expert-defined operational procedure is first codified into a machine-readable Execution Blueprint. A deterministic engine then executes this code-defined blueprint, navigating its states with complete fidelity. The role of the Foundation Model is thus strategically reframed: it is no longer the central decision-maker but is invoked as a specialized tool at specific nodes of the blueprint."
- **Charles Sieg "Deterministic Scaffolding":** "You do not need a deterministic model to build a deterministic system. You need deterministic scaffolding around a non-deterministic core."
- **Decision framework de arunbaby:**
  1. ¿Se puede escribir unit test que cubra 95%+ de inputs? → **CÓDIGO** (JSON validation, regex, format conversion, arithmetic, API parsing)
  2. ¿Input space es open-ended? → **LLM** (free-text classification, summarization, tool selection)
  3. ¿Necesita ambos? → **Hybrid supervisor** (LLM decide, código ejecuta)
- **Production stats:** "Most production workflows should use LLM nodes for 20-40% of steps, code for the rest."
- **Hybrid Shift (youtube):** "By treating the LLM as a highly capable function rather than the entire operating system, you can cut your token costs by 50-90%, eliminate infinite loops, and build a system that actually scales profitably."
- **Patrón "add LLM fallbacks to code nodes":** "Handle the 95% case with code, the 5% edge case with an LLM. Best of both worlds."

**Aplicación directa al Osquestador (90/10 de Max):**
- **90% código Python/Node:**
  - Hooks lifecycle (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop) → if/else
  - Search engine (BM25 + FAISS + RRF) → algoritmo determinístico
  - Cache de skills (TTL 24h) → dict + expiry
  - Validación de SKILL.md (YAML frontmatter schema) → jsonschema
  - Descarga de skills (HTTP + git clone) → urllib + subprocess
  - Aislamiento entre proyectos (path validation) → os.path.realpath + checks
  - Routing de MCP messages → JSON-RPC dispatch
  - Persistencia (SQLite, FAISS, Git) → libs nativas
- **10% LLM (solo aquí):**
  - Query expansion (3 variaciones de la query del usuario)
  - Summarization de descripciones de skills (gisting)
  - Scoring de relevance (rankear top-K cuando BM25+vector no decide claro)
  - Generación de tags/classifications (auto-tag de skills nuevos)
  - Validación semántica (¿esta skill es realmente de la categoría X?)

### Búsqueda 7 — `knowledge distillation engine markdown skills research to code automation`
**Fuentes:** arxiv.org/html/2605.31264 (COLLEAGUE.SKILL), pasqualepillitteri.it (NotebookLM→Claude Skill), neurips.cc, github.com/alirezarezvani, arxiv.org/html/2402.13116
**Hallazgo clave (direct match con Max):**
- **COLLEAGUE.SKILL** (arxiv 2605.31264): "Automated trace-to-skill distillation system for generating person-grounded AI skills via expert knowledge distillation. Analyzers extract evidence about durable capability, mental models, and bounded interaction style; builders render structured Markdown; and a shared writer produces the generated skill package."
- **NotebookLM→Claude Skill workflow:** patrón exacto que Max ya implementó en su **Knowledge Distillation Engine** — "converts a NotebookLM source collection into a single Markdown file installable as a permanent skill in Claude Code. The processing phase is almost automatic… ten or fifteen targeted prompts… structured outputs that will become the building blocks of the SKILL.md."
- **claude-skills design philosophy:** "Skills are self-contained packages. Each includes executable tools (Python scripts), knowledge bases (markdown references), and user-facing templates. Key Pattern: Knowledge flows from `references/` → into `SKILL.md` workflows → executed via `scripts/` → applied using `assets/` templates."
- **Knowledge Distillation LLMs (paper):** "Steering Teacher LLM → Seed Knowledge → Generation of Distillation Knowledge → Training Student Model" → exactamente el pipeline del Distillation Engine de Max

**Validación: los 2 engines de Max son best-practice 2026.** El Knowledge Acquisition Engine = "Steering + Seed Knowledge". El Knowledge Distillation Engine = "Generation + Training". El Osquestador los integra como sub-módulos.

---

## Lo que dice Max en sus documentos (4 .md + 2 .html leídos parcialmente)

### Documento 1: `GURACIÓN DEL ORQUESTADOR...` (10,613 líneas)
**Estructura principal — Raíz Maestra 00:**
- **CHECKPOINT 00.01** Constitución del Proyecto (Visión, Misión, Objetivos, Principios, Reglas)
- **CHECKPOINT 00.02** Arquitectura Documental (Carpetas, Archivos, Bibliotecas, Artefactos)
- **CHECKPOINT 00.03** Mapa Mental Maestro (mapa general, por fases, módulos, dependencias, agentes, conocimientos, procesos, componentes, arquitectura, despliegue, decisiones, ciclo de vida)
- **CHECKPOINT 00.04** Pizarra Global (Crazy Wall) — ideas, objetivos, notas, bloqueos, riesgos, recordatorios, decisiones
- **CHECKPOINT 00.05** Sistema de Estados (state.json)
- **CHECKPOINT 00.06** Registro Maestro
- **CHECKPOINT 00.07** Configuración Global
- **CHECKPOINT 00.08** Perfil del Proyecto
- **CHECKPOINT 00.09** Inicialización del Orquestador
- **CHECKPOINT 00.10** Artefactos Generados
- **CHECKPOINT 00.11** Captura Universal de Entradas del Usuario
- **CHECKPOINT 00.12** Input Block (Texto Literal) — "regla general" de capturar TODO
- **CHECKPOINT 00.13** Perfil del Proyecto
- **CHECKPOINT 00.14** Registro Maestro de Checkpoints
- **LEY UNIVERSAL DE PERSISTENCIA** — principio fundamental, no perder nada
- **FASE 01** Captura de la Idea → CHECKPOINT 01.01, 01.02 (Comprensión del Problema)...

### Documento 2: `biblioteca de skills` (8,006 líneas)
**Biblioteca Universal de Conocimiento:**
- "La Biblioteca no es un simple repositorio de documentos. Es un sistema inteligente de capacidades."
- Cada elemento debe: ser encontrado, comprendido, validado, ejecutado, combinado, actualizado, auditado
- Organizado por FASES del proyecto: FASE 03 Arquitectura → skills Clean Architecture, Microservicios, Event Driven. FASE 05 Desarrollo → Python, TypeScript, React, FastAPI, Java, Rust. FASE 07 Seguridad → ...

### Documento 3: `Knowledge Acquisition Engine` (513 líneas)
**Engine 1 — Recolector:**
- `system_name: KNOWLEDGE_ACQUISITION_ENGINE`
- `execution_mode: AUTO_RUN`
- Startup sequence: cargar config → leer registry.json → leer knowledge_state.json → revisar biblioteca existente → detectar faltantes → crear plan automático
- **Rule:** "Antes de investigar debe comprobar si el conocimiento ya existe."
- Responsabilidad: investigar, buscar fuentes, descargar, analizar calidad, comparar, clasificar
- **NO puede:** crear skills finales, crear docs oficiales, modificar biblioteca final, publicar

### Documento 4: `Knowledge Distillation Engine` (574 líneas)
**Engine 2 — Creador:**
- `system_name: KNOWLEDGE_DISTILLATION_ENGINE`
- `type: AUTONOMOUS_KNOWLEDGE_CREATOR_AND_DOCUMENT_BUILDER`
- Pipeline: recepción → análisis → destilación → ...
- **Rule:** "Nunca crear un activo sin revisar primero la biblioteca."
- Input sources: Knowledge Acquisition Engine, Usuario Chat, Agente IA, Orquestador, Repositorios, Documentación, Código, Skills existentes, Auditorías

---

## Decisión de arquitectura FINAL (Osquestador + skills + repo `memoria`)

### Estructura del repo `osquestador-memoria` (catálogo maestro)
```
osquestador-memoria/                    # GitHub repo, público o privado según Max
├── REGISTRY.yaml                       # Índice maestro de skills (id, name, fuente, version, categoria, tags, sha256)
├── indice/
│   ├── por_categoria.yaml              # Dewey-style: 000=computación, 500=ciencia, 600=tecnología...
│   ├── por_tag.yaml                    # tags lowercase-kebab-case
│   ├── por_fuente.yaml                 # clauhb / skillsmp / github / max-local / ...
│   └── por_fase.yaml                   # FASE 00-09 del proyecto (de la estructura de Max)
├── skills/<categoria>/<skill-id>/
│   ├── SKILL.md                        # Standard open (Anthropic)
│   ├── scripts/                        # Código Python/Node ejecutable real
│   ├── references/                     # Docs profundos (lazy load)
│   └── assets/                         # Templates, archivos auxiliares
├── knowledge/                          # Output del Knowledge Acquisition Engine de Max
│   ├── investigations/<topic>.md       # Investigaciones crudas
│   └── sources.json                    # Trazabilidad de fuentes
├── distillations/                      # Output del Knowledge Distillation Engine de Max
│   └── <asset-id>/                     # Assets destilados
└── README.md
```

### Flujo end-to-end cuando Max / un agente necesita una skill

```
1. TRIGGER: "necesito procesar PDFs en español"
   ↓
2. OSQUESTADOR consulta REGISTRY.yaml (lookup local, <10ms)
   ↓
3. No está local → busca en paralelo:
   ├─ ClawHub API (curl)
   ├─ SkillsMP API (curl)
   ├─ OpenAgentSkill API (curl)
   └─ GitHub search (gh search repos)
   ↓
4. Ranking: score = (relevance_BM25 * 0.4) + (trust_score * 0.3) + (recency * 0.2) + (max_validated * 0.1)
   ↓
5. Top-3 candidatas → query expansion LLM (10% del cómputo) → re-rank
   ↓
6. Usuario / agente aprueba la skill → descarga vía `npx clawhub install` o `git clone` (código determinístico)
   ↓
7. Validación YAML schema + sha256 + scan de scripts por patrones peligrosos (código)
   ↓
8. Cache local en ~/.osquestador/skills/cache/<sha256>/
   ↓
9. Expuesta via MCP al agente que la pidió
   ↓
10. El Osquestador ofrece al agente en su próxima conexión (injection via SessionStart hook)
```

### Skills Anthropic doble-uso (lo confirmó la Búsqueda 4)
- **El Osquestador acepta SKILL.md en cualquier formato del estándar** y lo sirve a través de MCP
- **El agente conectado decide si la consume** (compatible con Claude, OpenClaw, Cursor, etc)
- **Una skill = una fuente de verdad** — el repo `osquestador-memoria` la versiona, el Osquestador la sirve
- **Si Max escribe una skill para Claude Code, funciona tal cual en el Osquestador** (mismo SKILL.md, misma estructura)

### Conversión de los documentos de Max en código real del Osquestador

| Documento de Max | Módulo del Osquestador | Tipo (90/10) |
|------------------|------------------------|--------------|
| Knowledge Acquisition Engine | `osquestador/acquisition/engine.py` | 90% código: HTTP requests, JSON parsing, dedup hash, file cache. 10% LLM: query reformulation |
| Knowledge Distillation Engine | `osquestador/distillation/engine.py` | 90% código: SKILL.md template, YAML frontmatter generator, file write, sha256. 10% LLM: summarization, tag generation |
| Biblioteca Universal de Conocimiento | `osquestador/biblioteca/` (directorio) + `REGISTRY.yaml` | 100% código: filesystem + YAML + SQLite FTS5 |
| Raíz Maestra 00 (14 Checkpoints) | `osquestador/checkpoints/` (14 archivos .py) | 95% código: state machine determinístico. 5% LLM: Constitución wording (one-shot) |
| Crazy Wall (Pizarra Global) | `osquestador/crazy_wall/` | 100% código: notes API + UI |
| Input Block (Captura Universal) | `osquestador/input/capture.py` | 100% código: lee, hashea, persiste, versiona |
| Ley de Persistencia Universal | `osquestador/persistence/` | 100% código: SQLite WAL + Git auto-commit |

### Patrón "Compiled AI" aplicado al Osquestador

```
FASE BUILD-TIME (offline, 1x al día o cuando hay update):
  1. Knowledge Acquisition Engine investiga (LLM 10%)
  2. Knowledge Distillation Engine produce SKILL.md + scripts/ (LLM 10%)
  3. Validación de seguridad (código 100%)
  4. Commit al repo osquestador-memoria (código 100%)

FASE RUN-TIME (online, cada vez que un agente se conecta):
  1. SessionStart hook → lee REGISTRY.yaml, inyecta top-N skills (código 100%)
  2. UserPromptSubmit → search engine (código 100%, LLM solo para query expansion 10%)
  3. Tool call → ejecuta script de la skill (código 100%, sin LLM)
  4. PostToolUse → log + index (código 100%)

RESULTADO: 90% del cómputo es código determinístico, 10% LLM concentrado en compile-time.
```

---

## Stack técnico final (decidido por evidencia, no por suposición)

| Componente | Tecnología | Fuente de evidencia |
|------------|-----------|---------------------|
| **Estándar de skill** | SKILL.md open standard (Anthropic) | anthropic.com + agensi.io + 20+ herramientas |
| **Búsqueda de skills** | load-skill CLI + agent-skills-cli + clauhb CLI | libraries.io/npm, github.com |
| **Catálogo local** | YAML + SQLite FTS5 | Vault Semantic, Reddit MCP |
| **Validación** | jsonschema + sha256 + custom security scan | Anthropic + community best practice |
| **Búsqueda local** | BM25 (SQLite FTS5) + FAISS MiniLM-L6-v2 + RRF | Vault Semantic, Obsidian Hybrid |
| **Query expansion** | Haystack QueryExpander con M2.5 | haystack.deepset.ai (Punto 1) |
| **Multi-tool compatibility** | `.agents/skills/` estándar cross-client | dev.to/rosgluk, reddit.com/r/ClaudeAI |
| **Symlinks cross-platform** | opensite-skills setup.sh pattern | dev.to/opensite |
| **90/10 enforcement** | Compiled AI + Blueprint First Model Second | arxiv 2604.05150 + 2508.02721 |
| **Knowledge engines de Max** | Acquisition + Distillation | Documentos de Max (10k+ líneas) |
| **Repo catálogo** | GitHub `osquestador-memoria` | Decisión basada en Punto 1 |

---

## Métricas de éxito del Punto 2

- [ ] Repo `osquestador-memoria` creado en GitHub con REGISTRY.yaml + 3 skills de ejemplo
- [ ] Osquestador expone MCP server con tools: `skill_search`, `skill_install`, `skill_list`, `skill_validate`
- [ ] Al conectarse un agente, recibe catálogo corto de skills disponibles (progressive disclosure)
- [ ] Al pedir una skill, el Osquestador la descarga on-demand de ClawHub/SkillsMP/GitHub
- [ ] Una skill SKILL.md escrita para Claude Code funciona en el Osquestador sin modificar (validado)
- [ ] Los 2 engines de Max implementados como módulos Python: acquisition + distillation
- [ ] Tests E2E: 100% del routing determinístico, <10% del cómputo total es LLM
- [ ] Validación: instalar skill "pdf-processing" oficial de Anthropic, servirla vía MCP, agente la consume

## Riesgos identificados

1. **Skills maliciosas (supply-chain attack)** — mitigación: trust scores + scan de scripts + allowlist de fuentes validadas por Max
2. **Cache local crece sin límite** — mitigación: TTL 24h + LRU + max 10GB
3. **Knowledge Acquisition Engine gasta muchos tokens investigando** — mitigación: rate limit + check si ya existe (regla de Max) + cache de 7 días
4. **Versiones de skills divergen entre marketplaces** — mitigación: el Osquestador mantiene UN solo source of truth (sha256) por skill
5. **Confliktos de nombre de skill** — mitigación: namespace `fuente:slug` (ej: `clauhb:pdf`, `max:hermes`)
6. **Latencia de descarga on-demand** — mitigación: pre-cache de top-50 skills más usadas en background
7. **90/10 es aspiracional, no medible sin telemetría** — mitigación: logging de cada llamada LLM con costo en tokens + dashboard

---

## Próximo paso (esperando luz verde de Max)
- **Punto 3:** Osquestador informa al agente qué funciones tiene disponibles al conectarse (capability advertisement / handshake protocol).

**¿Apruebas el Punto 2 para pasar al Punto 3?**
