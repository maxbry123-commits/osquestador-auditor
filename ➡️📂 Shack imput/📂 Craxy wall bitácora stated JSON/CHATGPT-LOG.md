# SOL / ChatGPT — Craxy Wall Log

## 2026-09-10 — Bootstrap

`NODE=BOOTSTRAP_ARCHITECTURE`

- Leído `AGENTS.md` y `PIPELINE/00_METODO_TRABAJO_Y_ARQUITECTURA.md`.
- Leído skill canónico de descarga/extracción/copia/move.
- Verificados los seis blobs canónicos de motores.
- Creada raíz `➡️📂 Shack imput/`.
- Publicados arquitectura, handoff, parche de recuperación, índice de componentes, runtime README, INPUT LOCK, Role Router, Research Dispatcher, tests, Community Registry, Component Registry y memoria de búsqueda.
- Catálogo inicial: 77 componentes.
- Comunidades de programación preestablecidas: 63.
- Test local del Core: 4/4 PASS después de corregir detección de React y limpiar trailing whitespace.
- Motores canónicos: NO modificados.

## 2026-09-10 — Adquisición

`NODE=T04_ACQUISITION_MONITOR`

- Publicadas 6 colas; suma total = 77 componentes.
- Publicado `.github/workflows/shack-input-components.yml`.
- Run inicial `34470498878`: seis lanes arrancaron, pero quedaron en checkout del repo completo.
- GitHub reportó repo size `9516442 KB` (~9.1 GB), por lo que el checkout completo fue identificado como cuello físico previo al motor.
- Se corrigió únicamente el cable del workflow: partial clone `--filter=blob:none` + sparse paths para motores/colas/Craxy Wall. Ningún motor fue editado.
- Run optimizado `34470821525` creado; se conserva `NO_COMPONENT_PASS_YET` hasta recibir verdicts físicos.
- Watchdog ChatGPT horario activado, timezone America/Bogota.
- Arquitectura, índice y STATE tuvieron read-back desde `main`.

## 2026-09-10 — Watchdog T04 / balance real

`NODE=T04_ACQUISITION_GAP_RECOVERY`

- Releídos handoff, parche y `STATE.json` antes de actuar.
- Run optimizado `34470821525`: 6/6 jobs `completed/success`.
- En los 6 jobs pasaron: partial sparse checkout NO LFS, verificación de los seis blob SHA canónicos, ejecución del motor y persistencia de state/index.
- Los índices generados por Motor 2 confirman balance físico: search 3/13 VERIFIED_CLOSED; code 2/12; rag 8/13; skills 5/15; media-input-router 10/18; orchestration 0/6.
- Balance global: `28 VERIFIED_CLOSED + published read-back verified`, `49 FAILED`, `0 PENDING`.
- Se observaron al menos tres clases de fallo diferentes: `SOURCE_SPECIAL_FILE_GAP`, `READBACK_TREE_HASH_GAP`, `DESTINATION_EXISTS`.
- Ejemplo auditado: `search/gpt-researcher/DOWNLOAD_EXTRACT_MANIFEST.json` existe en `main`, contiene `extraction_verified=true`, fuente fijada a commit `6f998577d547b1e54ec662dac63583aa11e3b84b` y árbol esperado; sin embargo la cola terminó FAILED por `DESTINATION_EXISTS` tras reintentos, por lo que NO se reclasifica automáticamente como VERIFIED_CLOSED.
- Reparación segura aplicada: actualizado `STATE.json` a revision 5 con balance real y `GAPS_PENDING_NO_BLIND_RETRY`; T05 queda bloqueado por T04 para evitar cablear sobre componentes no verificados.
- No se editó ningún motor canónico. No LFS. No force push. No sobrescritura silenciosa.

`NEXT=CLASIFICAR_49_FAILURES → RECUPERAR_DESTINATION_EXISTS_CON_READBACK → ESTRATEGIA_SEPARADA_SOURCE_SPECIAL_FILE_GAP → ESTRATEGIA_SEPARADA_READBACK_TREE_HASH_GAP → SOLO_DESPUES_T05_WIRE_TEST`

## 2026-09-10 — Watchdog T04 / auditoría de GAPs y reparación aditiva

`NODE=T04_ACQUISITION_GAP_RECOVERY`

- Clasificación forense de los 49 FAILED confirmada por workflow: `DESTINATION_EXISTS=17`, `READBACK_TREE_HASH_GAP=5`, `SOURCE_SPECIAL_FILE_GAP=19`, `OTHER=8`.
- Se creó `acquisition_gap_audit.py` como sidecar de auditoría; no sustituye ni modifica motores.
- Se corrigieron dos fallos del sidecar/workflow antes de aceptar evidencia: persistencia que borraba outputs durante rebase y resolución de árbol destino mediante ref de rama en Git Data API.
- Run de auditoría válido `34483405056`: checkout parcial sin LFS PASS, seis blob SHA canónicos PASS, auditoría por Git blob identity PASS, persistencia PASS y read-back de `ACQUISITION-GAP-AUDIT.json` realizado.
- Hallazgo físico: los destinos parciales no están vacíos. Ejemplos: Vane `235/238`, MindSearch `116/117`, DeerFlow `2650/2653`, Pyright `7561/7584` archivos Git frente a sus fuentes fijadas.
- Los faltantes coinciden con reglas ignore: Vane perdió `searxng/limiter.toml`, `searxng/settings.yml`, `searxng/uwsgi.ini`; MindSearch perdió `.DS_Store`; DeerFlow perdió `.vscode/*`; Pyright perdió rutas `build/*`. Esto confirma un GAP de publicación de archivos tracked ignorados después de una descarga/extracción correcta.
- No se consideran idénticos los destinos con `changed_count>0`; quedan fuera de la reparación aditiva inicial.
- Se creó `repair_ignored_publication.py`: usa `motor_1_extract_only.py` sobre `_archives` existentes con hashes de partes verificados y `motor_3_copy_batches.py` con `COLLISION_POLICY=fail`; sólo después hace `git add -f` de los archivos tracked faltantes. Cualquier colisión o cambio no aditivo falla cerrado y revierte el target.
- Se creó workflow `.github/workflows/shack-input-ignored-repair.yml`; run `34483843389` activo. Ya pasó checkout NO LFS y lock de motores; está ejecutando restauración canónica y luego hará publicación sin force + auditoría remota por blob SHA.
- `STATE.json` actualizado a revision 6. El balance oficial sigue `28 VERIFIED_CLOSED / 49 FAILED` hasta que el run de reparación cierre y el read-back posterior confirme una mejora; T05 continúa bloqueado.
- ASTRA y GROK no fueron reclamados ni modificados. SOL mantiene ownership exclusivo de `T04_ACQUISITION_GAP_RECOVERY`.

`NEXT=ESPERAR_VEREDICTO_RUN_34483843389 → READBACK_REAUDIT → ACTUALIZAR_BALANCE_SI_Y_SOLO_SI_VERIFICADO → DESPUES_TRATAR_CHANGED_COUNT_Y_SOURCE_SPECIAL_FILE_GAP`

## 2026-09-10 — Watchdog T04 / corrección NUL-safe del helper

`NODE=T04_ACQUISITION_GAP_RECOVERY`

- Releídos handoff, parche y `STATE.json` antes de actuar; ASTRA y GROK continúan sin nodos reclamados.
- Run `34483843389` terminó `completed/success`, pero su evidencia física fue `candidates=19`, `ready_for_publish=0`, `failed_closed=19`; por tanto NO reparó componentes y NO se contabilizó mejora.
- Causa verificada en `IGNORED-PUBLICATION-REPAIR.json`: el helper interpretaba rutas emitidas por `git diff --name-status` como strings citados/escapados (`\342...`) y las entregaba literalmente a `git hash-object`, produciendo `No such file or directory`.
- Reparación aplicada exclusivamente a `repair_ignored_publication.py`: parser de rutas staged cambiado a `git diff --cached --name-only -z` con separación NUL y chequeo separado de cambios no aditivos. Se añadió `git hash-object -- <path>` para proteger rutas que empiezan con guion. Ningún motor canónico fue editado.
- Commit del helper: `3f03ec86e231673f7ceae293217a9e5850c12bc1`.
- El push disparó run `34484946622`; ya pasó `Partial sparse checkout — no LFS` y `Verify canonical motors unchanged`; actualmente ejecuta `Restore only missing tracked files through canonical motors`.
- `STATE.json` actualizado a revision 7. Balance oficial permanece `28 VERIFIED_CLOSED / 49 FAILED / 0 PENDING` hasta read-back posterior.
- No LFS. No force push. No sobrescritura silenciosa. T05 continúa bloqueado por T04.

`NEXT=RUN_34484946622_VERDICT → REMOTE_REAUDIT → ACTUALIZAR_BALANCE_SOLO_CON_EVIDENCIA → CLASIFICAR_RESTANTES`
