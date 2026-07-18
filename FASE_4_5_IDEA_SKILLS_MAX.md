# FASE 4.5 — Anotación de la idea de Max (2026-07-18)

**Trigger literal de Max (en este turno):**
1. "el osquestador también podría buscar skills en al web en una lista de muchos lugares diferentes y descargar según la necesidad"
2. "investiga en la comunidad de desarrolladores como lo hacen mientras te paso una información de la idea para los skills"
3. "investiga de nuevo en comunidad de desarrolladores 10 pasadas"
4. "busca información de los skills de claude de antropy ve que se puede usar doble los skills"
5. "lo que te doy los documentos convertirlo en código real en el osquestador"
6. "intenta en el diseño 90% code determinetista y 10% llm"

**Adjuntos recibidos de Max (6 archivos, no leídos aún):**
- `GURACIÓN DEL ORQUESTADOR la estructura completa de programación de un proyecto de programación web app y software de NCT NEURONAS CODE TURBO.md`
- `8Fnct neuronas code turbo biblioteca de skills y otros elementos que se puede usar para programar como conocimiento de información para los agentes.md`
- `biblioteca-conocimiento.html`
- `Jason de destilación de skillss y de otros elementos nct neuronas code turbo.md`
- `Jason de investigacion de skills y otros elementos de programación y descargar en biblioteca de nct neuronas code turbo.md`
- `orquestador-estructura.html`

**Búsquedas previas (5, ya hechas):**
- skill marketplace aggregator multi-source registry search download install npm
- agent skill auto discovery fetch install on demand registry API 2025 2026
- Claude skills marketplace ClawHub skillsmp skillhub aggregator download install

**Hallazgos consolidados (3 fuentes principales):**
1. **load-skill** (npm) — agregador que junta skills de múltiples fuentes en un solo comando (`load-skill install <name>`)
2. **Skilldex** (arxiv 2604.16911) — package manager + registry con hierarchical scoping, agent-driven suggestion, MCP server
3. **ClawHub** + **SkillsMP** + **SkillHub** + **OpenAgentSkill** + **agent-skills-cli** — los 5 marketplaces principales que la comunidad ya usa
4. Patrón confirmado: gateway skill (tiny puntero) se carga al inicio; el resto se descarga on-demand
5. Trust scores + audit signals son el estándar 2026 para evitar supply-chain attacks

**Decisiones de arquitectura del Osquestador (a confirmar con el código de Max):**

### A) Búsqueda multi-fuente
- El Osquestador consulta en paralelo: ClawHub, SkillsMP, SkillHub, OpenAgentSkill, GitHub directo
- Si Max tiene su propio repo `biblioteca-conocimiento` (visto en el .html), se incluye como fuente #6
- Cache local en `~/.osquestador/skills/cache/` con TTL 24h
- El Osquestador decide qué fuente usar según: (a) match semántico, (b) trust score, (c) si Max ya validó la skill

### B) Skills Anthropic reutilizables (skills doble uso)
- Anthropic publicó Agent Skills como estándar abierto (18 dic 2025)
- Mismo SKILL.md funciona en: Claude Code, OpenClaw, Cursor, GitHub Copilot, OpenAI Codex CLI, Gemini CLI, Microsoft Agent Framework
- **Doble uso confirmado:** una skill escrita para Claude Code se puede cargar en OpenClaw sin reescribir nada
- El Osquestador expone las skills via MCP para que cualquier agente conectado las use

### C) Skills = código real, no solo markdown
- Anthropic permite `scripts/` y `assets/` en el folder de la skill
- En el Osquestador, esos scripts son **código ejecutable real** (Python/Node) que el agente puede invocar
- Ejemplo: skill `git-commit` tiene un `scripts/commit.py` que se ejecuta de verdad, no es LLM fingiendo

### D) 90% código determinístico / 10% LLM (regla de Max)
- **90% código:** routing, validación, cache, hooks, formato de skills, descarga, instalación, pre-filtrado BM25/vector, search engine,隔离 entre proyectos
- **10% LLM:** query expansion (3 variaciones), summarization de descriptions, scoring de relevance, generación de tags/classifications
- El LLM SOLO se invoca donde la decisión es genuinamente ambigua; el resto es if/else/while en Python/Node
- Patrón validado por el paper "Reusable Patterns for Classifying AI Work With Claude": "Never regex a label out of prose. Use Claude's tool-use to define the output shape and let the model fill it." → estructurar el LLM para que complete campos, no para que decida flujos

### E) Skills library = repositorio
- Repo GitHub `osquestador-skills` (separado de `osquestador-memoria` y de `osquestador-auditor`)
- Estructura del repo:
  ```
  osquestador-skills/
  ├── skills/
  │   ├── <categoria>/<skill-name>/
  │   │   ├── SKILL.md          # YAML frontmatter + markdown
  │   │   ├── scripts/          # código ejecutable real
  │   │   ├── references/       # docs profundos (lazy load)
  │   │   └── assets/           # archivos auxiliares
  ├── indice/
  │   ├── por_categoria.yaml    # clasificación Dewey-style
  │   ├── por_tag.yaml
  │   └── por_fuente.yaml
  ├── README.md
  └── REGISTRY.yaml             # índice maestro
  ```
- El Osquestador clona este repo en `~/.osquestador/skills/` y lo indexa en el SessionStart hook
- Cuando un agente pide una skill → el Osquestador la carga (no el LLM, el kernel)

### F) Próximas 10 búsquedas (a ejecutar)
Pendiente aprobación + lectura de los 6 adjuntos de Max para extraer la estructura real del orquestador que él ya diseñó.

**Siguiente paso:** leer los 6 adjuntos de Max para extraer la estructura, luego 10 búsquedas más (skills Anthropic, doble uso, código determinístico), luego documento final de Punto 2.
