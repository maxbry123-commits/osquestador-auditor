# 🦈 RECOVERY PATCH — GROK — SHARCK INPUT V2.1

Schema: `sharck.recovery.grok.v2`
Mode: `RESUME_WITHOUT_COLLISION / FAIL_CLOSED`

## Fuente de verdad
- Repo: `maxbry123-commits/osquestador-auditor`
- Branch: `main`
- Root: `➡️📂 sharck imput/`
- Handoff vigente: `➡️📂 sharck imput/HANDOFF-MULTIENV-3STEP-20X-2026-09-11.md`
- State base: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/STATE.json`
- Último state delta al reconciliar: `STATE-DELTA-033-M44-RECOVERY-RECONCILIATION.json`
- Checkpoint base: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/CHECKPOINT.json`
- Último checkpoint delta al reconciliar: `CHECKPOINT-DELTA-031-M44-RECOVERY-RECONCILIATION.json`
- Plan base: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/PLAN.json`
- Último plan delta al reconciliar: `PLAN-DELTA-015-M44-RECOVERY-RECONCILIATION.json`
- Log propio GROK: `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/GROK-LOG.md`

## Orden obligatorio de arranque
1. Leer Handoff vigente y luego STATE/CHECKPOINT/PLAN más sus deltas posteriores desde `main`.
2. Leer `GROK-LOG.md`, `20X-OSS-MEJORAS-2026-09-11.md`, `XRAY-ADN-CROSSCHECK-2026-09-11.md` y evidencia de gaps relevante.
3. Confirmar ownership y SHA fresco antes de escribir.
4. Reclamar únicamente `M08_OSS_REFUTATION` en `GROK-LOG.md`; el claim sólo es válido si lo escribe GROK como propietario.
5. Evaluar B05/B06 con `KEEP / DEFER / REJECT` y verificar por candidato `license + source/ref/commit + special-scan + maintenance + contradiction`.
6. Registrar evidencia y verdict en `GROK-LOG.md`; no borrar evidencia previa ni instalar por descubrimiento.

## Owner exclusivo GROK
`M08_OSS_REFUTATION`

Scope: OSS/package/subtree/API alternatives, comunidad de desarrolladores, Hugging Face/labs, issues/benchmarks, mantenimiento/licencias, contradicciones, source refs oficiales y refutación del catálogo/StrategyDelta.

## Estado verificado de recuperación
- Catálogo canónico: `117`.
- B01–B04: `17 VERIFIED_CLOSED / 23 FAILED / 0 pending`.
- 23 FAILED preservados: `12 partial + 11 source-special/symlink`.
- Partial universe: `12 components / 139 exact anomalies`.
- M25 sandbox coverage: `3/12 components` y `4/139 anomalies`; no autoriza producción.
- B05/B06: `20 RESEARCHED_CANDIDATE_NO_DOWNLOAD / 0 downloaded`.
- M06 ASTRA: `OPEN_UNCLAIMED` al último read-back.
- M07 CLAUDE: `OPEN_UNCLAIMED` al último read-back.
- M08 GROK: `OPEN_UNCLAIMED` al último read-back.
- `physical_repair_allowed=false`.
- `b05_b06_download_allowed=false`.
- `step3_allowed=false`.

## Contrato global 3 pasos
1. `INVENTARIO / XRAY / ARQUITECTURA`.
2. `RESEARCH/PREFLIGHT + ADQUISICIÓN/StrategyDelta + READBACK`; cualquier adquisición física sigue bloqueada por los reviews/gate definidos.
3. `WIRE / PRUNE / MIN-CODE / TEST` sólo después de `M06 + M07 + M08 + director gate`.

## Prohibido
- tocar o reclamar `M06` ASTRA;
- tocar o reclamar `M07` CLAUDE;
- duplicar control/state/motor-watch de SOL;
- iniciar Paso 3;
- reparar físicamente los 23 FAILED antes del gate;
- descargar B05/B06 antes del fan-in y decisión del director;
- editar motores canónicos;
- LFS/force/silent overwrite;
- declarar PASS por presencia o discovery;
- borrar evidencia contradictoria previa.

## Anti-colisión
`READ latest Handoff/STATE/CHECKPOINT/PLAN → FETCH GROK-LOG SHA → verify M08 free → CLAIM in GROK-LOG → execute read-only review → evidence/verdict → fan-in`.

Si otro owner ya reclama M08: `NO WRITE` sobre ese nodo. No sustituir el claim del propietario ni usar un log ajeno.

## Salida de GROK esperada
Por candidato/hallazgo: `component | URL/ref | source SHA/tag/commit | función | licencia | mantenimiento | special-scan | contradicción | alternativa | KEEP/DEFER/REJECT | evidencia`.

## Recovery rule
Este parche no autoriza descarga, repair ni integración. Si al reanudar existe un checkpoint/delta posterior, prevalece el posterior tras read-back. Toda promoción física exige los gates del Handoff vigente.
