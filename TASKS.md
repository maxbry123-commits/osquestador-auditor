# TASKS.md — `osquestador-auditor`
**Pipeline DSL/DAG Sheriff v8.2 · Modo STRICT · Loop infinito hasta CERTIFIED**
**Fecha:** 2026-07-17 · **Owner:** Max · **Agente:** Mavis (M3)

---

## ══ ROADMAP EJECUTIVO ══

```
FASE 0 → INVESTIGACIÓN PURA (100+ fuentes/programa, sin código)
FASE 1 → CONSOLIDACIÓN DEL CONOCIMIENTO (INVESTIGACION.md + 5+ SKILL.md)
FASE 2 → DOC-GATE (README, INSTRUCCIONES, BITACORA, TASKS, CHECKPOINTS, state.json)
FASE 3 → REPOSITORIO (crear/subir docs a `osquestador-auditor`)
FASE 4 → DISEÑO DEL PANEL (estética fotos Claude/Anthropic — NO funciones router)
FASE 5 → PANEL HTML + MCP + VPS + MEMORIA AVANZADA
FASE 6 → DEPLOY CLOUDFLARE PAGES
FASE 7 → DEPLOY VPS (carpeta nueva, OpenClaw INTACTO)
FASE 8 → END-TO-END + GLOBAL VALIDATION
FASE 9 → CERTIFICACIÓN
```

---

## ══ FASE 0 — INVESTIGACIÓN PURA (NO_SKIP, 100+ fuentes/programa) ══

> **Regla SHERIFF:** ningún paso posterior arranca mientras esta fase no esté CERTIFICATED.

- **0.1** Investigar código fuente oficial **OpenClaw** (npm: `openclaw@2026.6.11`) — protocolo WS, contratos, modelos, scope operador
- **0.2** Investigar **LiteLLM** (puerto 4000) — providers, fallbacks, OpenAI-compat API
- **0.3** Investigar **MCP (Model Context Protocol)** — spec JSON-RPC 2.0, transports (stdio/HTTP/WS), tool discovery
- **0.4** Investigar **Haystack** (similitud/duplicados) — retrievers, embedders, pipelines
- **0.5** Investigar **Plandex** (planning/task decomposition) — cómo arma DAG de tareas
- **0.6** Investigar **Hermes** (documentación) — formato README raíz
- **0.7** Investigar **SWE-agent** (auditoría código) — frontier exploration
- **0.8** Investigar **Repomix** (empaquetado de repos) — output format
- **0.9** Investigar **Kanboard** (task index) — JSON-RPC API, project model
- **0.10** Investigar **Obsidian** (vault) — markdown + Dataview, plugin API
- **0.11** Investigar **Graphiti** (memoria grafo) — Neo4j schema, edges/entities
- **0.12** Investigar **Telegram Bot API** — getUpdates, sendMessage, long polling
- **0.13** Investigar **Anthropic Console / Claude.ai Project UI** (patrón visual para el panel)
- **0.14** Investigar **Cloudflare Pages** — wrangler, deploy, headers, redirects
- **0.15** Investigar **Cloudflare Tunnel** (cloudflared) — quick vs named, fallback rotation
- **0.16** Investigar **DuckDNS API** — update por IP
- **0.17** Investigar **systemd** — unit file, journalctl, Restart=always
- **0.18** Investigar **SQLite WAL** — journal_mode, atomic transactions
- **0.19** Investigar **Circuit Breaker pattern** (Hystrix, Polly, resilience4j) — thresholds
- **0.20** Investigar **JSON-RPC 2.0 spec** — request/response/error format
- **0.21** Investigar **hot-reload Python** (jurigged, reloadium, watchdog) — mtime vs inotify
- **0.22** Investigar **JSON-Agents / PAM**, **agent-registry**, **MOYA** — estándares plugin/agent
- **0.23** Investigar **patrones UI minimalista** estilo Anthropic/iOS — dark mode, jerarquía, densidad
- **0.24** Investigar **streaming** (SSE, WebSocket, fetch streams) — para panel en vivo
- **0.25** Investigar **persistencia de memoria local en VPS** — formatos, naming, RAG local
- **0.26** Investigar **OCR** (Tesseract, PaddleOCR, HF Spaces OCR, Baidu) — para binarios
- **0.27** Investigar **vector stores** (FAISS, Qdrant, Chroma) — embeddings
- **0.28** Investigar **memoria avanzada** (episódica / semántica / procedimiento) — patrones y casos
- **0.29** Investigar **Neo4j + Graphiti** — esquema de nodos/relaciones para el proyecto
- **0.30** Investigar **DAG runners** (Airflow, Prefect, Dagster) — patrones de task DAG
- **0.31** Investigar **conectores MCP existentes** (filesystem, github, git, memory) — qué hay
- **0.32** Investigar **Seguridad** (sandbox, capability-based, isolation en Linux) — para el workspace

**Entregable FASE 0:** `INVESTIGACION.md` con ≥100 fuentes clasificadas (sistema | versión | fuente | fecha | resumen | hallazgo | aplicación | dependencias | limitaciones | riesgos | evidencia | estado | referencia cruzada | uso futuro)

---

## ══ FASE 1 — CONSOLIDACIÓN + SKILLS ══

- **1.1** Crear `INVESTIGACION.md` (consolidado por sistema, no por link suelto)
- **1.2** Extraer patrones → 5 SKILLS (`/skills/*.md`):
  - `SKILL_orquestador_kernel.md` (patrón kernel + plugins)
  - `SKILL_mcp_integration.md` (cómo hablar MCP)
  - `SKILL_memoria_avanzada.md` (episódica/semántica/procedimiento)
  - `SKILL_panel_ui.md` (estética Claude/Anthropic, NO funciones de router)
  - `SKILL_evidence_collect.md` (cómo capturar evidencia reproducible)
- **1.3** Crear `SKILLS.md` índice de skills
- **1.4** Cross-references en README

---

## ══ FASE 2 — DOC-GATE (bloquea sin estos 6 docs) ══

- **2.1** `README.md` — visión, quickstart, árbol, links
- **2.2** `INSTRUCCIONES.md` — paso a paso despliegue + uso
- **2.3** `BITACORA.md` — log cronológico inmutable
- **2.4** `TASKS.md` ← **ESTE DOC**
- **2.5** `CHECKPOINTS.md` — snapshot por fase
- **2.6** `state.json` — fuente operativa del pipeline (machine-readable)

---

## ══ FASE 3 — REPOSITORIO GITHUB `osquestador-auditor` ══

- **3.1** ESPERAR PAT válido de Max (scope `repo`)
- **3.2** Verificar si el repo existe (`GET /repos/maxbry123-commits/osquestador-auditor`)
- **3.3** Si no existe → `POST /user/repos` con `private: true`
- **3.4** Subir los 7 adjuntos originales a `/docs/fuente/` (los que dieron el spec)
- **3.5** Subir los 3 nuevos adjuntos (`router-v1-lista`, `tarea-1-1`, `panel_router_3`) como **REFERENCIA DOCUMENTAL** en `/docs/referencias/` (NO como código a copiar)
- **3.6** Subir las 2 fotos del panel Claude/Anthropic como `/docs/panel-diseno.png`
- **3.7** Subir `INVESTIGACION.md`, `INSTRUCCIONES.md`, `BITACORA.md`, `TASKS.md`, `CHECKPOINTS.md`, `state.json`
- **3.8** Subir 5 `SKILL.md` y `SKILLS.md` índice
- **3.9** Tag `v0.1-investigacion` y commit firmado
- **3.10** Validar estructura, hashes, trazabilidad

---

## ══ FASE 4 — DISEÑO DEL PANEL ══

> **Regla:** el HTML que mandaste (`654156ca` + `29fc122d`) es **SOLO modelo estético** (paleta, tipografía, layout). Las funciones de router NO se replican. La foto de Claude.ai (Projectos / Artefactos / Conectores) es el patrón visual a imitar.

- **4.1** Extraer paleta: fondo `#0D0D0F`, cards `#1F1E1E`, texto `#F2EBD9`, azul `#3B82F6`, verde OK `#7FD1A8`
- **4.2** Tipografía: **Fraunces** (serif headings) + **Inter** (sans body)
- **4.3** Patrón de cards: rounded 18px, padding generoso, jerarquía clara
- **4.4** Definir layout del panel: sidebar con Proyectos | Artefactos | Conectores | main con documentos/tareas/conflictos/health
- **4.5** Validar el diseño con Max antes de codear

---

## ══ FASE 5 — PANEL HTML + INTEGRACIÓN ══

- **5.1** Construir `panel/index.html` con estética aprobada
- **5.2** **MCP connection:** consumir 4 tools (`search_project`, `get_doc`, `list_conflicts`, `queue_doc`) del orquestador vía JSON-RPC
- **5.3** **VPS connection:** health-check vía `sshpass` + `curl` a `127.0.0.1:8765` (MCP server del orquestador)
- **5.4** **Memoria avanzada:** carpeta `~/.osquestador/memoria/{episodica,semantica,procedimiento}/` con índice RAG local
- **5.5** Streaming de eventos del orquestador (SSE o WebSocket)
- **5.6** Mostrar: docs, conflictos, tareas, health, heartbeat, evidencias, handoff
- **5.7** `linter check_kernel_isolation.py` → "kernel limpio"

---

## ══ FASE 6 — DEPLOY CLOUDFLARE PAGES ══

- **6.1** Build estático del panel
- **6.2** `wrangler pages deploy` con `CLOUDFLARE_API_TOKEN` (cfat_6pZSRS...)
- **6.3** URL pública estable `*.pages.dev`
- **6.4** Verificar respuesta 200 + UI renderiza

---

## ══ FASE 7 — DESPLIEGUE VPS (sin tocar OpenClaw) ══

- **7.1** Clonar repo en **`/root/osquestador/`** (carpeta nueva, separada, NO `/opt/nct/agents/*`)
- **7.2** `pip install requests pyyaml` en venv
- **7.3** `python3 -m orchestrator` (modo local, sin credenciales al inicio)
- **7.4** Verificar `state/health.json` = `alive`
- **7.5** Crear `/etc/systemd/system/osquestador.service` con `WorkingDirectory=/root/osquestador`
- **7.6** `systemctl enable --now osquestador`
- **7.7** **VERIFICACIÓN OPENCLAW INTACTO:** `ss -tlnp | grep 18789` debe seguir mostrando OpenClaw sin cambios

---

## ══ FASE 8 — END-TO-END + GLOBAL VALIDATION ══

- **8.1** Subir 1 doc de prueba a `inbox/test/`
- **8.2** Esperar 1 ciclo de poll (10s) → aparece en `vault/test/`
- **8.3** Disparar conflicto → `list_conflicts` desde el panel → respuesta
- **8.4** Resolver → `inventory` actualiza estado
- **8.5** Health/heartbeat visibles en panel
- **8.6** MCP server responde 4 tools

---

## ══ FASE 9 — CERTIFICACIÓN ══

Certificar SOLO si TODO:
- □ 100+ fuentes investigadas y consolidadas
- □ 5+ skills documentados
- □ 6 docs obligatorios en repo
- □ state.json actualizado
- □ CHECKPOINTS completos
- □ BITACORA con todas las acciones
- □ Repositorio validado (estructura + hashes)
- □ Panel renderiza + valida
- □ MCP server responde 4 tools
- □ VPS health = alive
- □ Memoria avanzada operativa
- □ OpenClaw INTACTO
- □ Cero FAIL / WARNING / PENDING / BLOCKED / DEGRADED

---

## ══ REGLAS GLOBALES SHERIFF ══

```
NO_SKIP
NO_ASSUME
NO_FAKE_PASS
NO_HALLUCINATION
NO_INCOMPLETE
NO_OUTPUT_WITH_PENDING
NO_BUILD_WITHOUT_RESEARCH
NO_BUILD_WITHOUT_DOCUMENTATION
NO_BUILD_WITHOUT_SKILLS
NO_BUILD_WITHOUT_CHECKPOINT
NO_BUILD_WITHOUT_STATE
NO_CERTIFICATION_WITHOUT_EVIDENCE
NO_MODIFY_OPENCLAW
```

---

## ══ GATES OBLIGATORIOS ══

- **INVESTIGATION_GATE** → PASS antes de FASE 1
- **DOCUMENTATION_GATE** → PASS antes de FASE 3
- **HEALTH_GATE** + **HEARTBEAT_GATE** antes y después de cada nodo
- **CONNECTIVITY_GATE** antes de cualquier deploy
- **RESULT_GATE** después de cada nodo
- **AUTO_RECOVERY_GATE** si hay FAIL (hasta 200 estrategias, después escalamiento válido)
- **PHASE_APPROVAL_GATE** al cerrar cada fase
- **CHAT_REPLICATION_GATE** → todo documento en repo Y en chat
- **CERTIFICATION_GATE** → cero FAIL/WARNING/PENDING/BLOCKED

---

## ══ EVIDENCIA OBLIGATORIA POR NODO ══

```
TASK_ID | SESSION_ID | NODE_ID | CHECKPOINT_ID | STATE_VERSION
HEALTH_OK | HEARTBEAT_OK | LOGS | METRICAS | HASH | CHECKSUM
TIMESTAMP | RESULTADO | ESTADO | REPOSITORIO_ACTUALIZADO | CHAT_BACKUP
```

Sin TODA esta evidencia → `NO_PASS` (SHERIFF bloquea).

---

## ══ INPUT BLOCK ACTUAL ══

- **OBJECTIVE:** construir `osquestador-auditor` con panel conectado a MCP + VPS + Memoria Avanzada, estética Claude/Anthropic, OpenClaw aislado.
- **TASKS:** este documento (cascada de 9 fases).
- **CONSTRAINTS:** NO tocar OpenClaw · NO construir sin research · NO certificar sin evidencia.
- **SUCCESS_CRITERIA:** todos los checks de FASE 9 en verde.
- **PRIORITY:** investigación primero, panel después, deploy al final.
- **ATTACHMENTS:** 7 docs del Orquestador + 3 nuevos router/panel HTML + 2 fotos Claude/Anthropic.
- **DESIGN_REFERENCE:** fotos de Claude.ai (sidebar, artefactos, conectores).
- **DOCUMENT_REFERENCE:** `INVESTIGACION.md` (consolidado) + `SKILLS/` (5+ skills) + adjuntos fuente.

---

## ══ ESTADO ACTUAL ══

```
PRECHECK........
  [✓] Adjuntos identificados (7 originales + 3 nuevos + 2 fotos)
  [✓] Sandbox operativo
  [ ] PAT GitHub válido (BLOCKER — esperando de Max)
  [ ] VPS conexión verificada
  [ ] Cloudflare token verificado

FASE 0..........
  [ ] 32 nodos de investigación (0/32)
  [ ] INVESTIGACION.md (0%)

FASE 1..........
  [ ] 5 SKILL.md (0/5)

FASE 2..........
  [✓] TASKS.md (ESTE DOC) ← checkpoint actual
  [ ] README.md
  [ ] INSTRUCCIONES.md
  [ ] BITACORA.md
  [ ] CHECKPOINTS.md
  [ ] state.json

FASE 3..........
  [ ] Repo `osquestador-auditor` creado/subido
  [ ] Docs fuente en /docs/fuente/
  [ ] Referencias visuales en /docs/referencias/
  [ ] Fotos panel en /docs/

FASE 4-9........ [TODAS PENDING]
```

---

**Próximo nodo a ejecutar:** esperar confirmación de Max sobre el documento de tareas → arrancar FASE 0 nodo 0.1 (OpenClaw source).

**Decime: ¿aprobás este TASKS.md así, o querés que ajuste algo antes de FASE 0?**
