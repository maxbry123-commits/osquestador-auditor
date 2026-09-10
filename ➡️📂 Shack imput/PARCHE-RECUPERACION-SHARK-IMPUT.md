# 🦈 PARCHE DE RECUPERACIÓN — SOL / ASTRA / GROK

## Identidad
Proyecto: **Wanted Shark Web / Shack imput**.
Objetivo: construir una capa pre-LLM que preserve el INPUT literal, lo descomponga, enfoque la investigación, ejecute búsqueda amplia y especializada, encuentre code/skills/tools, verifique evidencia y entregue un Context Package a la LLM principal.

## Recuperación obligatoria
1. Abrir `➡️📂 handoff Readme shark imput.md`.
2. Abrir `📁 readme arquitectura Shack imput.md`.
3. Abrir `📂 Craxy wall bitácora stated JSON/STATE.json`.
4. Abrir el log propio y `memoria búsqueda.md`.
5. No asumir que ninguna tarea está terminada: verificar GitHub y outputs físicos.
6. Mantener los 3 pasos; no crear fases nuevas.

## Reglas inmutables
- INPUT_BLOCK literal: conservar `raw` y SHA-256; análisis siempre sidecar.
- Motor de descarga/extracción/copia/move: usar el canónico; jamás editarlo.
- COPY-FIRST: antes de generar código, buscar componente/función/skill existente.
- GitHub = fuente persistente de verdad.
- PASS sólo con evidencia/read-back/test.
- Las LLM de Focus A/B proponen enfoque; no son VerdictAuthority.

## Coordinación
SOL: integración/ejecución.
ASTRA: auditoría/refutación/gaps de arquitectura.
GROK: investigación OSS/comunidades/code-skill-tool alternatives.
Si el nodo ya está RUNNING por otro agente, escoger otro pendiente.

## Qué existe ya
- Registry de 63 comunidades dev.
- Registry de 77 componentes.
- 5 colas de descarga.
- `shark_input_lock.py` para raw+hash.
- `role_router.py` multi-role determinista inicial.
- `research_dispatch.py` para plan de investigación.
- tests unitarios iniciales.
- arquitectura, índice, handoff, memoria y Craxy Wall.

## Qué falta verificar/continuar
- publicación/read-back del bootstrap;
- ejecución real de las colas y balance por lane;
- inventario de componentes VERIFIED_CLOSED vs FAILED;
- adapters de búsqueda, Code Pointer RAG, Skill Pointer y Tool Finder;
- Evidence Ledger y Gap Loop;
- Focus AI A/B y Clarifier 3–12;
- Context Compiler;
- integración final + tests end-to-end.

## Salida esperada de cada agente
`NODE | INPUTS | ACTION | FILES_TOUCHED | EVIDENCE | TESTS | GAPS | NEXT`.
