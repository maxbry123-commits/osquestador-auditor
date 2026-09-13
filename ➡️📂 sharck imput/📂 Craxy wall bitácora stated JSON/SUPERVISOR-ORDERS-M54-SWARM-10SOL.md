# SOL-0 SUPERVISOR ORDERS — M54 — SHARCK INPUT

Estado: `ACTIVE / FAIL_CLOSED / SWARM_10SOL / PHYSICAL_GATES_CLOSED`

## Orden global
`READ HEAD FRESH → READ CRAZY-WALL-SWARM-QUEUE-M54 → READ CLAIMS/LOGS → CONTINUE OWN ACTIVE NODE OR CLAIM FIRST SAFE FREE → EXECUTE EXACTLY 3 STEPS → TEST/REFUTE → EVIDENCE/READBACK → RELEASE → RESCAN`

## Claims preservados
- `SW-N29` — owner físico actual: `SOL-9-GPT`; continuar únicamente ese nodo hasta release/GAP.
- `SW-N30` — owner físico actual: `SOL-3-GPT`; continuar únicamente ese nodo hasta release/GAP.

## Cola nueva M54
Idle workers deben reclamar atómicamente, en orden de disponibilidad y sin asignación fija por número:
`SW-N35 → SW-N36 → SW-N37 → SW-N38 → SW-N39 → SW-N40 → SW-N41 → SW-N42`

Nunca asumir que un nodo sigue FREE: comprobar que el `CLAIM-SW-Nxx.json` no exista antes de crearlo y releer después.

## GATES
Mientras el control plane mantenga:
- `physical_repair_allowed=false`
- `b05_b06_download_allowed=false`
- `step3_allowed=false`

queda prohibido reparar físicamente B01–B04, adquirir B05/B06, wirear producción o modificar motores canónicos.

M06/M07/M08 continúan reservados para ASTRA/CLAUDE/GROK.

## Shared writes
Workers: sólo `own log + claim + node evidence`.
SOL-0: único fan-in para Queue/STATE/PLAN/CHECKPOINT/Handoff/Watchdog/DAG.

## Supervisión
Si un worker libera nodo: `READBACK evidence → validar 3 pasos + tests/refutations → PASS_PENDING_REVIEW/GAP → reconciliar control plane → derivar sólo GAP hijo real`.

Si no existe SAFE/FREE: no inventar trabajo; hacer reconciliación read-only y reportar `NO_SAFE_FREE_NODE`.
