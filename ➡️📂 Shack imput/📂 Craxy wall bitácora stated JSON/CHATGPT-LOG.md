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
