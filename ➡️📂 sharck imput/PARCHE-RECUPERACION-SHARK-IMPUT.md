# 🦈 PARCHE DE RECUPERACIÓN — SHARCK INPUT V2

## Objetivo
Recuperar el proyecto sin depender del chat, sin repetir nodos cerrados y sin declarar PASS sin evidencia.

## 1. Fuente de verdad
- Repo: `maxbry123-commits/osquestador-auditor`
- Branch: `main`
- Raíz activa V2: `➡️📂 sharck imput/`
- Código: `➡️📂 sharck imput/📂 input sharck code principal/`
- V1: `➡️📂 Shack imput/` preservada; último estado leído: 47/77 VERIFIED_CLOSED y 30 GAP.

## 2. Lectura obligatoria SOL / ASTRA / GROK / CLAUDE
1. `README-METODO-TRABAJO-MULTIAGENTE.md`
2. `📁 readme arquitectura sharck imput.md`
3. `➡️📂 readme indice de componentes sharck imput.md`
4. `📂 Craxy wall bitácora stated JSON/PLAN.json`
5. `📂 Craxy wall bitácora stated JSON/STATE.json`
6. `📂 Craxy wall bitácora stated JSON/CHECKPOINT.json`
7. log propio
8. `➡️📂 handoff Readme shark imput.md`
9. `REVIEW-GATE-ASTRA-ENGINEERING.md`

## 3. Reanudación
Tomar `resume_from` de CHECKPOINT y volver a comprobar STATE antes de reclamar una tarea. Nodo `VERIFIED_CLOSED` no se repite. Nodo CLAIMED/RUNNING por otro owner no se pisa; se toma otra tarea `parallel_safe`.

## 4. Flujo
`INPUT_RAW → INPUT_LOCK → CONTRACT → GOALS → TASK_GRAPH → ROLE_ROUTER → OWNER_LOCK → FAN_OUT → CHECKPOINTS → EVIDENCE → FAN_IN → CROSS_REVIEW → VERDICT → NEXT_NODE`.

Tres pasos globales:
1. ANOTAR/ARQUITECTURA/INVENTARIO.
2. ADQUIRIR con motor canónico, lotes máximo 10.
3. WIRE/PRUNE mínimo/CODE faltante/TEST tras review gate.

## 5. Estado comprobado al actualizar este parche
- Método, arquitectura, índice, PLAN/STATE/CHECKPOINT y logs: publicados.
- Catálogo: 107 = 77 V1 + 30 nuevos.
- B01/B02/B03: 10 componentes cada uno.
- Workflow V2: `.github/workflows/sharck-input-v2-components.yml`.
- Commit workflow: `c276f51a56f5c0bc433d2991240c72f14142d464`.
- Run `34514168678`: `IN_PROGRESS`, conclusión `null`.
- Jobs B01/B02/B03: `IN_PROGRESS`.
- `Partial sparse checkout — NO LFS`: PASS 3/3.
- `Verify canonical motor blob SHAs`: PASS 3/3.
- motor de descarga+extracción: ejecutándose 3/3.
- Componentes V2 contables como `VERIFIED_CLOSED` en este checkpoint: 0/30 hasta obtener state/index/read-back individuales.
- Watchdog ChatGPT/SOL: actualizado a V2 y habilitado cada hora.

## 6. Motores fail-closed
Sólo usar la raíz canónica externa de motores. Blobs exactos completos están en Handoff. No LFS, no force, no editar motores, no destination defaults implícitos.

## 7. Owners
- SOL: estado, integración, consolidación, motor watch.
- CLAUDE: code/ports/adapters/typing/tests.
- GROK: OSS/community/HF/labs/alternatives/contradiction.
- ASTRA: XRAY_ARQUITECTURA, EVALUACION_PREVIA, MEJORA_VERSIONADA, COMPONENT_GAP_RESEARCH, INDEPENDENT_VERIFY.

## 8. Review gate
Antes de integrar los componentes nuevos, registrar revisiones independientes de ASTRA, CLAUDE y GROK en Craxy Wall, más el gate del director. `REVIEW-GATE-ASTRA-ENGINEERING.md` define las pruebas.
Una revisión externa adicional sólo se registra cuando exista evidencia real. Actualmente `NOT_PERFORMED_NO_EVIDENCE`.

## 9. GAP handling
`GAP → preservar evidencia → investigar hasta 20 vías cuando lo amerite → StrategyDelta distinto → retry acotado → checkpoint`.
Si el GAP bloquea un nodo pero existe otro independiente, continuar ese nodo. Nunca spin infinito.

## 10. Cierre
`VERIFIED_CLOSED` exige evidencia apropiada: URL/source ref + ruta + commit/SHA/diff + test/log + read-back. Presencia física sola nunca basta.

## Nodo de reanudación
`MONITOR_V2_RUN_34514168678 → READ_BATCH_STATE/INDEX → UPDATE_STATE/CHECKPOINT → M06/M07/M08_REVIEWS → DIRECTOR_GATE → STEP3`.
