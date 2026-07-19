# TASK_018 — RESEARCH LOOP: 5 búsquedas + 1 gap cerrado

**Fecha**: 2026-07-18 21:18
**Modo SHERIFF v8.2**: RESEARCH_LOOP · no-gap → 5 búsquedas + 1 pasada
**Source**: web (Anthropic docs, CloudZero, Tembo, Apple HIG, W3C, OpenAI)

## 5 BÚSQUEDAS EJECUTADAS

### B1: Anthropic design tokens + dark mode CSS
- **URL**: claude.com/docs/connectors/building/mcp-apps/transparent-theming
- **Hallazgo**: MCP Apps usan `var(--color-background-primary)` y `light-dark()`. CSS variables con `<meta name="color-scheme" content="light dark" />`
- **Aplicación prototipo v5**: ✓ ya usa CSS variables. NO gap.

### B2: Claude Code Agent View (may 2026)
- **URL**: code.claude.com/docs/en/agent-view + cloudzero.com/blog/claude-code-agents
- **Hallazgo**: Agent view es research preview, requiere Claude Code v2.1.139+. Subagents = .claude/agents/ YAML. Agent teams = orchestrator dispatches workers.
- **Aplicación prototipo v5**: ✓ flow diagram Supervisor→Worker está en 05_routing_agentes.html. NO gap.

### B3: iOS 17/18 file manager multi-select
- **URL**: lifetips.alibaba.com (UXPA benchmark n=47)
- **Hallazgo**: drag-to-select gesture, no long-press model. UXPA 2023: Select All wastes 14.6s.
- **Aplicación prototipo v5**: ✓ tap-toggle implementado en 04. NO gap.

### B4: WCAG 2.5.7 Dragging Movements ⚠️ GAP ENCONTRADO
- **URL**: allaccessible.org/blog/wcag-257-dragging-movements-implementation-guide + W3C
- **Hallazgo**: **CRÍTICO** — Kanban drag-drop REQUIERE alternativa single-pointer (botón, keyboard, tap)
- **Gap**: 06_kanban_dragdrop.html solo tenía drag-drop
- **Severidad**: HIGH (legal: ADA, Section 508, EAA)
- **Fix aplicado**: botón "Mover a…" por cada card + menú dropdown con 3 columnas destino

### B5: OpenAI Agents SDK + guardrails
- **URL**: openai.github.io/openai-agents-python/guardrails
- **Hallazgo**: Tool guardrails (input/output), Input/Output guardrails, handoffs pipeline
- **Aplicación prototipo v5**: documentado en D28 ya. NO gap en HTML.

## GAP CERRADO

### F-018-01 (HIGH): WCAG 2.5.7 — alternativa single-pointer a drag-drop
- **Antes**: 06_kanban_dragdrop.html solo drag-drop (ilegal bajo EAA 2025+)
- **Después**: 13 cards con botón "Mover a…" + menú dropdown con 3 columnas destino
- **Verificación**: `grep -c "card-move\|data-move" → 20` (13 buttons + CSS + JS)
- **Status**: CLOSED

## HALLAZGOS INFORMATIVOS (no gaps)

- Anthropic design system usa `light-dark()` + CSS variables (prototipo ya compatible)
- Claude Agent View v2.1.139+ es research preview (no production) — usar con disclaimer
- iOS 18 drag-to-select es preferible a long-press+check (UXPA bench)
- OpenAI Agents SDK: `agent.asTool()` para handoff vs helper pattern

## ESTADO PIPELINE

- 24 nodos completados (TASK_015 → TASK_018)
- 8 HTMLs v5 + 4 docs nuevos
- 1 gap crítico cerrado (WCAG 2.5.7)
- 0 findings abiertos

## CONTEO

- Búsquedas: 5 (no-gap path mínimo)
- Pasadas extra: 0 (no necesarias)
- Gap crítico: 1 (cerrado)
- Gaps menores: 0

Procede TASK_019_LOOP_CONTROLLER.
