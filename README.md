# `osquestador-auditor`

**Osquestador Auditor — sistema operativo de ejecución con kernel pequeño + plugins, MCP, VPS, memoria avanzada.**

**Owner:** maxbry123-commits · **Agente:** Mavis (M3) · **Fecha:** 2026-07-17 · **Modo:** SHERIFF v8.2 STRICT

---

## 🎯 Objetivo

Construir el `osquestador-auditor` con:
- Panel de control conectado a **MCP + VPS + Memoria Avanzada**
- Estética visual tipo **Claude.ai / Anthropic** (NO funciones de router — solo modelo visual)
- Orquestador Fase 0 con kernel pequeño y plugins intercambiables
- OpenClaw completamente **aislado e intacto**

---

## 📚 Documentos del repo

| Doc | Qué contiene |
|-----|--------------|
| [`README.md`](./README.md) | Este archivo (visión, quickstart, índice) |
| [`TASKS.md`](./TASKS.md) | Lista cascada de tareas en 9 fases |
| [`BITACORA.md`](./BITACORA.md) | Bitácora cronológica de cada acción ejecutada |
| [`HISTORIAL_TAREAS.md`](./HISTORIAL_TAREAS.md) | Historial completo de tareas (qué se hizo, cuándo, hash, evidencia) |
| [`INSTRUCCIONES.md`](./INSTRUCCIONES.md) | Pendiente FASE 2 |
| [`INVESTIGACION.md`](./INVESTIGACION.md) | Pendiente FASE 0-1 (100+ fuentes) |
| [`CHECKPOINTS.md`](./CHECKPOINTS.md) | Pendiente FASE 2 |
| [`state.json`](./state.json) | Pendiente FASE 2 |

---

## 🧰 Repos upstream verificados (descargados a `/workspace/agentes/`)

| Agente (del spec) | Repo GitHub | Hash local | Estado |
|-------------------|-------------|------------|--------|
| Haystack (similitud) | `deepset-ai/haystack` | `007c66b` | ✅ clonado |
| Plandex (planificar) | `plandex-ai/plandex` | `e2d7720` | ✅ clonado |
| SWE-agent (frontera) | `SWE-agent/SWE-agent` | `3ea751c` | ✅ clonado |
| Repomix (empaquetar) | `yamadashy/repomix` | `a5577d5` | ✅ clonado |
| Kanboard (task index) | `kanboard/kanboard` | `564cc30` | ✅ clonado |
| Graphiti (grafo) | `getzep/graphiti` | `0b4bcf1` | ✅ clonado |
| LiteLLM (providers) | `BerriAI/litellm` | `dbb5b81` | ✅ clonado |
| Tesseract (OCR) | `tesseract-ocr/tesseract` | `4b70b7d` | ✅ clonado |
| PaddleOCR (OCR alt) | `PaddlePaddle/PaddleOCR` | `211989f` | ✅ clonado |

**Pendientes (ESCALAR — no son OSS descargable o no tienen upstream en GitHub):**
- OpenClaw → npm package `openclaw` (no es repo GitHub)
- Hermes → modelo de HuggingFace, no es código
- Obsidian → app de pago, no es OSS
- Anthropic Console → producto cerrado
- Telegram → API + libs cliente (no es repo único)

---

## 🚫 Reglas duras

- **OpenClaw = INTACTO.** Prohibido modificar, instalar encima, alterar config, usar como workspace.
- **Todo el trabajo ocurre en `osquestador-auditor`.**
- **No se construye sin investigación previa documentada.**
- **No se certifica sin evidencia completa (TASK_ID, NODE_ID, CHECKPOINT_ID, STATE_VERSION, HASH, LOGS, REPOSITORIO_ACTUALIZADO, CHAT_BACKUP).**
- **No se borra bitácora, historial, checkpoints ni state.**

---

## 📍 Fases

Ver [`TASKS.md`](./TASKS.md) para la lista cascada completa.

```
FASE 0 → Investigación pura (100+ fuentes/programa)
FASE 1 → Consolidación + 5 SKILL.md
FASE 2 → DOC-GATE (6 docs obligatorios)
FASE 3 → Repositorio (crear/subir docs)
FASE 4 → Diseño del panel (estética Claude)
FASE 5 → Panel HTML + MCP + VPS + Memoria
FASE 6 → Deploy Cloudflare Pages
FASE 7 → Deploy VPS (sin tocar OpenClaw)
FASE 8 → End-to-End
FASE 9 → Certificación
```

---

## 🔗 Links

- **Repo:** https://github.com/maxbry123-commits/osquestador-auditor
- **TASKS:** [`TASKS.md`](./TASKS.md)
- **Bitácora:** [`BITACORA.md`](./BITACORA.md)
- **Historial:** [`HISTORIAL_TAREAS.md`](./HISTORIAL_TAREAS.md)
