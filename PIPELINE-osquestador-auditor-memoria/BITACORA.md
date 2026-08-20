# BITÁCORA — osquestador auditor + memoria

## 2026-08-20 — CORRECCIÓN: COPIAR reciclaje, no escribir
- TASK_ID: S5-COPY-56-60
- Error previo: se escribió un documento nuevo de reciclaje. Operador: COPIAR el original.
- Original = `agentes/PIPELINE/56–60` (texto del operador 2026-08-19). No reescrito.
- COPY_FIRST:
  - agentes → `osquestador-auditor/PIPELINE/57–60` (reemplaza stubs/recortes)
  - mismos blobs → `PIPELINE-osquestador-auditor-memoria/56–60`
  - mismos blobs → `MEMORIA/PIPELINE/` y `orchestrator-auditor/PIPELINE/` (este lote)
- INTEGRITY PIPELINE/57–60 vs agentes: SHA blob idéntico
  - 56: 633db146900074721d9a3320b83258cf350e18d7 (ya coincidía)
  - 57: fe7d74ec237f5f84e440f402ddeb3b87998bbb8f
  - 58: bdc491a966ecdcc7466e0bd48a694a90541e84c0
  - 59: f8a38ff498d8608726d386aca8ec8080bbb9e8d9
  - 60: e35795f6ab550ac6a924d46bbfff6fbc2e2b390f
- Commit copy PIPELINE: `cb21d3e65906dd0058bafa7ffda4de17ab6d2907`
- Cuenta 2 abc1tienda-web: UNREACHABLE (sigue)
- No se tocó origen agentes.
- Sandbox: NO

## 2026-08-19 — SALIDA-2 (cerrada)
- Recycle forensic engine + wordflow reuse/memory/copy_first → `recycle/`
- Cuenta 2 `abc1tienda-web`: UNREACHABLE
- Commits: `37d9e213` … `27850e26`

## 2026-08-19 — SALIDA-5 intake + recycle scan
- TASK_ID: S5-USB-SCAN
- OBJECTIVE: 4 pasadas Wordflow + repos; anotar archivo USB/plugin; crear esta memoria PIPELINE
- Sandbox usado: NO
- Hallazgo: Wordflow YA tiene Resource Runtime + CapabilityBrain + EnchufeGate. No generar bus nuevo.
- Recycle: ver `recycle/SOURCE_MAP.yaml` bloque `salida_5`.
