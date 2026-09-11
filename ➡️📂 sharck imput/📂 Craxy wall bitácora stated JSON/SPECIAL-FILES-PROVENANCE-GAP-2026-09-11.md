# Sharck Input V2 — M32 Special-file provenance GAP

Fecha: 2026-09-11
Owner: SOL
Modo: parallel_safe / read-only evidence
Alcance: PRE-LLM; no integración, no reparación física, no source/ref redesign.

## Objetivo

Resolver la incógnita explícita de M30 sobre por qué no puede certificarse retrospectivamente el Git mode exacto del snapshot de adquisición de los 9 `SOURCE_SPECIAL_FILE_GAP` B01–B03 usando únicamente el estado canónico del proyecto.

## Evidencia canónica leída

- `state/B01-state.json`
- `state/B02-state.json`
- `state/B03-state.json`
- `SPECIAL-FILES-STATE-LEDGER-AUDIT-2026-09-11.md`
- `CHECKPOINT.json` CP-V2-CONTROL-PLANE-RECONCILED-018

## Hallazgos

### FACT — orden de ejecución del motor

En los fallos special, el traceback canónico muestra esta secuencia:

`src,commit=acquire(work); rows,src_bytes=scan_tree(src); src_tree=tree_hash(src)`

`scan_tree()` eleva `RuntimeError('SOURCE_SPECIAL_FILE_GAP:...')` antes de que el flujo llegue a construir/persistir el bloque final `result`.

### FACT — pérdida de provenance en state al fallar temprano

Los items FAILED por `SOURCE_SPECIAL_FILE_GAP` conservan `slug`, `source_repo`, `status` y traceback, pero no persisten `source_commit`/snapshot identity dentro de un `result`. En contraste, los items `VERIFIED_CLOSED` sí persisten `source_commit`, `source_ref`, hashes y árboles.

Esto afecta el ledger de 9 componentes special ya establecido por M30: stormcrawler, tika, docling, vespa, networkx, cocoindex, pydantic-ai, litellm y fastmcp.

### FACT — exact Git mode del intento histórico no es demostrable desde el state actual

El commit de adquisición existió en memoria (`commit=acquire(work)`), pero no quedó registrado en los state items que abortaron durante `scan_tree()`. Por lo tanto, consultar el HEAD actual del upstream no equivale a verificar el snapshot exacto usado por el intento histórico.

### INFERENCE — causa del UNKNOWN de M30

El `UNKNOWN_NOT_INFERRED` de M30 no es sólo falta de inspección de los paths: existe un GAP de provenance del motor para early-failure states. Sin `source_commit` exacto no puede certificarse de forma reproducible el Git mode histórico de cada path únicamente desde los artefactos canónicos actuales.

### UNKNOWN

- Git mode exacto de cada path special en el snapshot histórico de cada intento B01–B03.
- Si el HEAD actual de cada upstream conserva exactamente la misma topología/mode que el snapshot histórico.
- El commit exacto de adquisición de cada uno de los 9 fallos, salvo que exista evidencia adicional fuera de estos state files que lo registre explícitamente.

## GAP nuevo

`G-V2-SPECIAL-PROVENANCE-9`

Definición: los 9 early failures `SOURCE_SPECIAL_FILE_GAP` no persisten `source_commit` antes de abortar, impidiendo reproducir/certificar retrospectivamente el Git mode del snapshot exacto desde los state files actuales.

## StrategyDelta candidata — REVIEW REQUIRED, NO IMPLEMENTADA

Para M07/M06: evaluar persistir un registro fail-closed de provenance inmediatamente después de `acquire(work)` y antes de `scan_tree(src)`, como mínimo `source_repo`, `source_ref`, `source_commit` y evidencia de Git modes/special entries. Esta propuesta no modifica el motor canónico en M32 y no autoriza reparación física.

## Gate

- ASTRA/M06: PENDING
- CLAUDE/M07: PENDING
- GROK/M08: PENDING
- Director gate: CLOSED
- `step3_allowed=false`
- `physical_repair_allowed=false`

## Veredicto M32

`SPECIAL_SNAPSHOT_PROVENANCE_GAP_VERIFIED_READ_ONLY`

No se declara PASS por presencia. No se consultó HEAD actual como sustituto del snapshot histórico. No hubo mutación de componentes, motores, source/ref ni destinos.
