# 🦈 PARCHE DE RECUPERACIÓN — SOL / ASTRA / GROK

## Identidad
Proyecto: **Wanted Shark Web / Shack imput**.
Objetivo: construir una capa pre-LLM que preserve el INPUT literal, lo descomponga, enfoque la investigación, ejecute búsqueda amplia y especializada, encuentre code/skills/tools, verifique evidencia y entregue un Context Package a la LLM principal.

## Recuperación obligatoria
1. Abrir `➡️📂 handoff Readme shark imput.md`.
2. Abrir `📁 readme arquitectura Shack imput.md`.
3. Abrir `📂 Craxy wall bitácora stated JSON/STATE.json`.
4. Abrir el log propio y `SALIDAS-CHATGPT.md`.
5. Abrir `➡️📂 shart imput code Run/memoria búsqueda.md`.
6. No asumir que ninguna tarea está terminada: verificar GitHub, Actions y outputs físicos.
7. Mantener los 3 pasos; no crear fases nuevas.

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

## Estado verificado al emitir este parche
- Raíz `➡️📂 Shack imput/` publicada en `main`.
- Arquitectura, índice y STATE tuvieron read-back.
- Registry de 63 comunidades dev.
- Registry de 77 componentes.
- 6 colas de descarga: search 13, code 12, rag 13, skills 15, media-input-router 18, orchestration 6.
- `shark_input_lock.py` para raw+hash.
- `role_router.py` multi-role determinista inicial.
- `research_dispatch.py` para plan de investigación.
- tests unitarios iniciales: 4/4 PASS local.
- workflow `.github/workflows/shack-input-components.yml` publicado.
- Run inicial `34470498878` encontró cuello de botella por checkout completo del repo (~9.1 GB); NO es PASS.
- Run optimizado `34470821525` usa partial clone `--filter=blob:none` + sparse paths y está pendiente/entrando a ejecución; consultar estado antes de actuar.
- Watchdog ChatGPT horario activo en `America/Bogota`.

## Qué falta verificar/continuar
- cierre físico de las 6 lanes y balance `VERIFIED_CLOSED` vs FAILED/PENDING;
- inventario de componentes efectivamente publicados/read-back;
- adapters de búsqueda;
- Code Pointer RAG;
- Skill Pointer;
- Tool/Capability Finder;
- Evidence Ledger + contradiction + Gap Loop;
- Focus AI A/B + Clarifier 3–12;
- Context Compiler;
- cableado final y tests end-to-end.

## Regla para el run de adquisición
No confundir `catalogado`, `queued`, `workflow running` con `descargado`. Sólo contar componente cerrado cuando exista evidencia producida por el motor canónico y, si `publish=true`, read-back remoto.

## Salida esperada de cada agente
`NODE | INPUTS | ACTION | FILES_TOUCHED | EVIDENCE | TESTS | GAPS | NEXT`.
