# SKILLS.md — Índice de Skills del Osquestador

**5 skills de información generadas tras la FASE 0 investigación.**
**Cada skill contiene:** Objetivo · Contexto · Entradas · Procedimiento · Reglas · Restricciones · Ejemplos · Fuentes · Dependencias · Cuándo usar/no usar · Relación con otros skills · Versión · Historial.

---

## Índice

| # | Skill | Propósito |
|---|-------|-----------|
| 1 | [`SKILL_orquestador_kernel.md`](./SKILL_orquestador_kernel.md) | Patrón kernel pequeño + plugins intercambiables (validado por JSON-Agents/PAM, agent-registry, MOYA). |
| 2 | [`SKILL_mcp_integration.md`](./SKILL_mcp_integration.md) | Exponer el orquestador como MCP server + consumirlo desde panel/IDE. |
| 3 | [`SKILL_memoria_avanzada.md`](./SKILL_memoria_avanzada.md) | Carpeta `~/.osquestador/memoria/{episodica,semantica,procedimiento}/` con RAG local. |
| 4 | [`SKILL_panel_ui.md`](./SKILL_panel_ui.md) | UI de control con estética Claude/Anthropic (paleta, tipografía, layout). NO funciones de router. |
| 5 | [`SKILL_evidence_collect.md`](./SKILL_evidence_collect.md) | Captura reproducible de evidencia por cada nodo (state.json + BITACORA + CHECKPOINTS). |

---

## Cómo se relacionan

```
┌─────────────────────────────────────────────┐
│  SKILL_panel_ui (HTML/CSS/JS)               │
│  └─ consume via fetch JSON-RPC 2.0          │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│  SKILL_mcp_integration (HTTP server)        │
│  └─ expone 4 tools: search/get/list/queue  │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│  SKILL_orquestador_kernel (Python)          │
│  └─ carga plugins, ejecuta workflows        │
│     ├─ inputs/                              │
│     ├─ agents/                              │
│     └─ outputs/                             │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│  SKILL_memoria_avanzada (carpeta VPS)       │
│  └─ ~/.osquestador/memoria/                 │
│     ├─ episodica/                           │
│     ├─ semantica/                           │
│     └─ procedimiento/                       │
└─────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│  SKILL_evidence_collect (state + git)       │
│  └─ state.json + BITACORA + CHECKPOINTS     │
│     + commits en GitHub                     │
└─────────────────────────────────────────────┘
```

## Reglas globales aplicadas a todas las skills

- ✅ OpenClaw = INTACTO (nunca tocar).
- ✅ Evidencia reproducible antes de claim PASS.
- ✅ Hot-reload por mtime en el orquestador.
- ✅ Idempotencia en todos los conectores.
- ✅ Circuit breaker en cada output connector.
- ✅ MCP discovery en `/.well-known/mcp.json`.
- ❌ NO inventar dependencias (escaladas, no fake).
- ❌ NO copiar funciones de UI ajena.
- ❌ NO claim PASS sin evidencia medible.

## Cómo añadir una nueva skill

1. Crear `SKILL_<nombre>.md` siguiendo la plantilla (ver cualquier skill existente).
2. Actualizar este índice con la nueva fila.
3. Commit + push a GitHub.
4. Mencionar la skill en el README principal.
5. Si la skill contradice el spec del Orquestador, **gana el spec** (es la fuente de verdad).

## Versión
v1.0 — 2026-07-17 · Mavis.
