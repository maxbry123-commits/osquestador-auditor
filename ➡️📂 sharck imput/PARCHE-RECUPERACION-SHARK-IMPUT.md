# 🦈 PARCHE DE RECUPERACIÓN — SHARCK INPUT V2

## Objetivo
Recuperar el proyecto sin depender del chat, sin repetir nodos cerrados y sin declarar PASS sin evidencia.

## 1. Fuente de verdad
- Repo: `maxbry123-commits/osquestador-auditor`
- Branch: `main`
- Raíz activa V2: `➡️📂 sharck imput/`
- Código: `➡️📂 sharck imput/📂 input sharck code principal/`
- V1: `➡️📂 Shack imput/` preservada; 47/77 VERIFIED_CLOSED y 30 GAP en el último STATE leído.

## 2. Lectura obligatoria para SOL / ASTRA / GROK / CLAUDE
1. `README-METODO-TRABAJO-MULTIAGENTE.md`
2. `📁 readme arquitectura sharck imput.md`
3. `➡️📂 readme indice de componentes sharck imput.md`
4. `📂 Craxy wall bitácora stated JSON/PLAN.json`
5. `📂 Craxy wall bitácora stated JSON/STATE.json`
6. `📂 Craxy wall bitácora stated JSON/CHECKPOINT.json`
7. log del agente que ejecuta
8. `➡️📂 handoff Readme shark imput.md`

## 3. Regla de reanudación
Tomar `resume_from` de CHECKPOINT y comprobar STATE antes de reclamar una tarea. Si el nodo ya está `VERIFIED_CLOSED`, no repetirlo. Si está CLAIMED/RUNNING por otro owner, tomar otra tarea `parallel_safe`.

## 4. Arquitectura de trabajo
`INPUT_RAW → INPUT_LOCK → CONTRACT → GOALS → TASK_GRAPH → ROLE_ROUTER → OWNER_LOCK → FAN_OUT → CHECKPOINTS → EVIDENCE → FAN_IN → CROSS_REVIEW → VERDICT → NEXT_NODE`.

Tres pasos globales:
1. ANOTAR/ARQUITECTURA/INVENTARIO.
2. ADQUIRIR con motor canónico, lotes máximo 10.
3. WIRE/PRUNE mínimo/CODE faltante/TEST tras review gate.

## 5. Estado al crear este parche
- Método V2: publicado.
- Arquitectura V2: publicada.
- Índice: 107 componentes = 77 heredados + 30 nuevos.
- PLAN/STATE/CHECKPOINT y logs de cuatro agentes: publicados.
- B01/B02/B03: colas creadas, 10 componentes cada una.
- Workflow V2: `.github/workflows/sharck-input-v2-components.yml`.
- Run: `34514168678`.
- Última observación: `QUEUED`, sin conclusión. No contar nuevos componentes como descargados/verificados hasta leer state/index físico posterior.

## 6. Motores — fail closed
Sólo usar la raíz canónica externa de motores. Validar blobs antes de ejecutar:
`a52d5dc0...`, `84d566e2...`, `91e6e448...`, `36899243...`, `8281211d...`, `9a21facf...` según Handoff completo.
No LFS, no force, no editar motores, no destination defaults implícitos.

## 7. Owners
- SOL: estado, integración, consolidación, motor watch.
- CLAUDE: code/ports/adapters/typing/tests.
- GROK: OSS/community/HF/labs/alternatives/contradiction.
- ASTRA: XRAY_ARQUITECTURA, EVALUACION_PREVIA, MEJORA_VERSIONADA, COMPONENT_GAP_RESEARCH, INDEPENDENT_VERIFY.

## 8. Review gate
Antes de integrar los componentes nuevos, registrar en Craxy Wall resultados independientes de ASTRA, CLAUDE y GROK. Una revisión externa adicional sólo puede registrarse cuando exista evidencia real (commit, comentario, informe o referencia verificable). No afirmar revisión/supervisión externa por intención.

## 9. GAP handling
`GAP → preservar evidencia → hasta 20 vías cuando lo amerite → StrategyDelta materialmente distinto → retry acotado → checkpoint`.
Si un GAP bloquea un nodo pero existe otro independiente, continuar ese otro nodo. Nunca spin infinito.

## 10. Cierre
`VERIFIED_CLOSED` exige evidencia apropiada al tipo de artefacto: URL/source ref + ruta + commit/SHA/diff + test/log + read-back. Presencia física sola nunca basta.

## Nodo de reanudación recomendado
`MONITOR_V2_RUN_34514168678 → UPDATE_STATE → M06/M07/M08_INDEPENDENT_REVIEWS → DIRECTOR_GATE → STEP3`.
