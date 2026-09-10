# 🦈 RECOVERY PATCH — MULTI-ENV — SHARCK INPUT V2

Schema: `sharck.recovery.multi-env.v1`  
Mode: `OWNER_LOCK_FAIL_CLOSED`

## Fuente de verdad
- Repo: `maxbry123-commits/osquestador-auditor`
- Branch: `main`
- Root única del proyecto: `➡️📂 sharck imput/`
- Handoff: `➡️📂 sharck imput/➡️📂 handoff Readme shark imput.md`

Handoff URL visible:
https://github.com/maxbry123-commits/osquestador-auditor/blob/main/%E2%9E%A1%EF%B8%8F%F0%9F%93%82%20sharck%20imput/%E2%9E%A1%EF%B8%8F%F0%9F%93%82%20handoff%20Readme%20shark%20imput.md

## Boot sequence obligatorio
`HANDOFF → PLAN.json → STATE.json → CHECKPOINT.json → LOG PROPIO → GAPS → REVIEW-GATE → owner check → claim → execute → evidence → checkpoint.after`.

## Ownership
### SOL
`GAP_WATCHDOG + state_control + consolidation + motor_watch`.
No duplicar M06/M07/M08.

### ASTRA
Owner: `M06_INDEPENDENT_AUDIT`.
Scope exclusivo: `XRAY_ARQUITECTURA`, `EVALUACION_PREVIA`, `MEJORA_VERSIONADA`, `COMPONENT_GAP_RESEARCH`, `INDEPENDENT_VERIFY`.

### CLAUDE
Owner: `M07_CODE_PORTS_TEST_REVIEW`.
Scope: code, contracts, ports, adapters, typing, unit/integration/failure tests y diagnóstico técnico de GAPs.

### GROK
Owner: `M08_OSS_REFUTATION`.
Scope: OSS, comunidad, Hugging Face, labs, alternativas, licencias, mantenimiento y contradicciones.

### OTRO ENTORNO
Arranca con `owner=NONE`. Sólo puede tomar una tarea `PENDING/FREE` sin owner o una asignación explícita. Nunca apropiarse de M06/M07/M08/GAP_WATCHDOG.

## Protocolo anti-pisado
1. READ latest STATE.
2. READ latest CHECKPOINT.
3. Verificar owner/lock.
4. Escribir claim/RUNNING solamente en log propio.
5. Releer STATE antes de tocar archivo compartido.
6. Ejecutar exclusivamente scope propio.
7. Adjuntar evidencia: ruta + SHA/diff + test/log + URL/read-back según aplique.
8. Persistir resultado sin borrar entradas ajenas.
9. Crear/actualizar checkpoint.after.
10. Releer `main` antes de declarar cierre.

## Regla de conflicto
Si dos agentes reclaman el mismo nodo, conserva ownership el primer claim verificable. El segundo no escribe en ese nodo y elige otra tarea `parallel_safe`; si no existe, queda WAIT/REVIEW sin inventar progreso.

## Shared-write rule
PLAN/STATE/CHECKPOINT/Handoff/Recovery = writers secuenciales. Logs = uno por agente. Antes de update de archivo compartido siempre fetch SHA fresco; nunca usar SHA viejo.

## Locks
- INPUT_RAW = IMMUTABLE
- MOTOR_CODE = CANONICAL_IMMUTABLE_COPY_ONLY
- V1 = READ_ONLY_REFERENCE
- NO_LFS
- NO_FORCE
- NO_SILENT_OVERWRITE
- READBACK obligatorio
- Step3 = BLOCKED hasta reviews y gate director

## Estado base al crear este parche
- Current node: `M06_M07_M08_REVIEW_AND_GAP_STRATEGY`.
- V2 acquisition: 10 VERIFIED_CLOSED / 20 FAILED / 0 pending.
- X-Ray exacto: 6 DESTINATION_EXISTS + 5 READBACK_TREE_HASH_GAP + 9 SOURCE_SPECIAL_FILE_GAP.
- SOL inició StrategyDelta read-only sobre los 6 DESTINATION_EXISTS: workflow `sharck-input-v2-readback-recover.yml`, run `34535896880`.
- ASTRA=M06 READY; CLAUDE=M07 READY; GROK=M08 READY.
- External engineering review = NOT_PERFORMED/NO_EVIDENCE.
- Paso 3 sigue bloqueado.

## Contrato por cambio
`INPUT literal → objetivo único → owner → dependencia → execute → verify/refute → evidence → PASS|GAP → checkpoint → next safe node`.
