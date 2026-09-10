# 🦈 RECOVERY PATCH — GROK — SHARCK INPUT V2

Schema: `sharck.recovery.grok.v1`  
Mode: `RESUME_WITHOUT_COLLISION / FAIL_CLOSED`

## Fuente de verdad
- Repo: `maxbry123-commits/osquestador-auditor`
- Branch: `main`
- Root: `➡️📂 sharck imput/`
- Handoff: `➡️📂 sharck imput/➡️📂 handoff Readme shark imput.md`
- State: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/STATE.json`
- Checkpoint: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/CHECKPOINT.json`
- Log propio: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/GROK-LOG.md`

Handoff URL visible:
https://github.com/maxbry123-commits/osquestador-auditor/blob/main/%E2%9E%A1%EF%B8%8F%F0%9F%93%82%20sharck%20imput/%E2%9E%A1%EF%B8%8F%F0%9F%93%82%20handoff%20Readme%20shark%20imput.md

## Orden obligatorio de arranque
1. Leer Handoff fresco desde `main`.
2. Leer PLAN + STATE + CHECKPOINT.
3. Leer `GROK-LOG.md` y `GAPS-ACQUISITION-V2.md`.
4. Confirmar ownership antes de escribir.
5. Reclamar únicamente `M08_OSS_REFUTATION` o una subtarea `parallel_safe` explícitamente libre.
6. Registrar evidencia y resultado en `GROK-LOG.md`; no borrar evidencia previa.

## Owner exclusivo GROK
`M08_OSS_REFUTATION`

Scope: OSS, comunidad de desarrolladores, Hugging Face, AI labs, alternativas, issues, benchmarks, mantenimiento, licencias, contradicciones, source refs oficiales y refutación del catálogo/StrategyDelta.

## Prohibido
- tocar `M06` ASTRA;
- tocar `M07` CLAUDE;
- tomar `GAP_WATCHDOG` de SOL;
- iniciar Paso 3;
- integrar automáticamente;
- editar motores canónicos;
- instalar por descubrimiento solamente;
- force/LFS/silent overwrite;
- declarar PASS sin evidencia/read-back.

## Anti-colisión
`READ latest STATE → verify owner → CLAIM/RUNNING en log propio → execute → evidence → result → checkpoint.`

Si otro owner ya reclama el nodo: `NO WRITE`; elegir otra subtarea `parallel_safe` registrada o esperar.

## Estado base verificado al crear este parche
- catálogo V2: 107;
- adquisición inicial: 10 VERIFIED_CLOSED / 20 FAILED;
- clases X-Ray exactas del FAILED: 6 DESTINATION_EXISTS + 5 READBACK_TREE_HASH_GAP + 9 SOURCE_SPECIAL_FILE_GAP;
- recovery read-back SOL para los 6 DESTINATION_EXISTS: workflow `sharck-input-v2-readback-recover.yml`, run inicial `34535896880`, en ejecución al emitir este parche;
- V1 histórica: 47/77 VERIFIED_CLOSED + 30 GAP;
- Paso 3: BLOCKED por review gate.

## Salida de GROK esperada
Por hallazgo: `component | URL/ref | source SHA/tag | función | licencia | mantenimiento | evidencia | contradicción | alternativa | verdict`.
