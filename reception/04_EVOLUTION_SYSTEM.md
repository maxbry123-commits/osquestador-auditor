# Evolution System · 5 modos + agentes y binarios
**TEAM SEALS / Wordflow** · 2026-08-07

---

## 1. Pipeline universal (todos los modos)

```text
Fuente (agente | skill | software OS | dataset | acoplador)
  → Discovery (download determinista + SHA)
  → Inventory (decisión vs ejecución)
  → Distill (mínima capability útil)
  → Template (DSL + schema + sheriff)
  → Compile (package KER)
  → Tests + benchmark + security
  → Council opcional
  → Approval
  → Canary
  → Capability Registry
  → Production mount
```

**Nunca:** source → production directo.  
**Siempre:** Evolution Sandbox → canary → registry.  
Si poda **merma** capability → capa D de reemplazo **o** BLOCK (EVO.08).

---

## 2. Cinco modos

### Modo 1 — Agente → capability determinista
Extrae tools/pipelines. LLM solo en nodos de generación de código; resto determinista.

### Modo 2 — Descapitar + micro TEAM
Corta planner/loop libre; instala entrypoint ControlBus/TEAM.  
Ej.: Hermes sin planner LLM; OpenClaw sin agent-loop libre. Conserva tools/workers/UI.

### Modo 3 — Skill → código ejecutable
Skill → plantilla DSL/DAG/Sheriff → 90% D / 10% LLM.  
Code agents (Claude Code, Codex, Mimo, OpenCode, OpenHands) escriben el módulo; no mandan el kernel.

### Modo 4 — Software OS → extension KER
Graphiti, n8n, Grapify…: source pinneado → package extensions/… sin app externa obligatoria.

### Modo 5 — Dataset / acoplador → knowledge o work pack
Versionado; no prompts sueltos.

---

## 3. Ya en agents/ (no re-clonar base)

| Path | Rol |
|------|-----|
| OpenClaw | Host UI (podar loop) |
| OpenClaw-headless | Variante |
| Hermes | Workers/cola (podar planner) |
| Claude-Code | Code runtime |
| Codex | Code runtime |
| Mimo-Code | Code runtime |
| Kimi | Code/research |

---

## 4. A pinnear / descargar (determinista)

### Code (cadenas confirmadas)
- OpenCode, OpenHands, Cline (faltan en repo)  
- Ya hay: Codex, Claude Code, Mimo, Kimi  

### Nav / tipo Perplexity
- browser.navigate / click / type (Playwright u OS browser agent)  
- browser.screenshot → artifact  
- web.search (API detrás de broker)  
- web.cite / extract  
- github.search_repos  

Grupo: groups/nav.yaml — runtimes reales, no roles de prompt.

### Mobile
- device.adb / ssh / ui_dump  
- mobile.screenshot  
Grupo: groups/mobile.yaml · secrets solo broker.

### Memoria / OCR vía Evolution
- Graphiti source → memory_graph  
- OCR OS o API broker → ocr.extract_text  

### Modelos GGUF
Seed-Coder, Nemotron, Nanbeige, Gemma → storage HF/bucket, **no** monorepo git.  
MODELS_MANIFEST.yaml con SHA.

---

## 5. Layout objetivo

```text
agentes/
  agents/              # una copia canónica por agente
  agents/sources/      # OpenHands, OpenCode, Cline, graphiti…
  groups/
    backend.yaml
    frontend.yaml
    fromted.yaml
    nav.yaml
    mobile.yaml
  manifests/
    AGENTS_SOURCE_MANIFEST.yaml
    MODELS_MANIFEST.yaml
  control-layer/
  extensions/
    evolution/
    memory_graph/
    ocr/
    osquestador_memory/   # diferido
```

Duplicar grupos = **instancias + isolation**, no 5 forks de OpenClaw.

---

## 6. Pull determinista

```yaml
- id: openhands
  repo: https://github.com/...
  ref: vX.Y.Z
  sha256: "..."
  path: agents/sources/OpenHands
  method: git-archive | release-asset
```

1. Clone depth 1 o curl asset  
2. Verificar sha256  
3. SOURCE_RECEIPT.json  
4. Prohibido main flotante sin pin  

---

## 7. Tareas EVO pendientes (código)

- EVO.01 este doc como base de recetas  
- EVO.02–06 implementaciones de modos  
- EVO.07 templates  
- EVO.08 gap→D/BLOCK  
- EVO.09 sandbox→canary  
- EVO.10 Source Reuse Contract  
