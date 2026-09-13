# SUPERVISOR ORDERS — M53 — SHARCK INPUT 10-SOL SWARM

Estado: `ACTIVE / FAIL_CLOSED / LIVE CLAIMS AUTHORITATIVE`

## Orden común
`READ HEAD FRESH → READ latest Handoff → READ CRAZY-WALL-SWARM-QUEUE-M53 → READ current claim + candidate claims → if current node active CONTINUE IT ONLY → if terminal/idle CLAIM FIRST SAFE/FREE → READBACK CLAIM → execute exactly 3 steps → test + 3 refutations → persist own evidence/log → READBACK → RELEASE/GAP/BLOCK → RESCAN`.

## Nodos M53
- `SW-N29`: mapear 11 KEEP M40 a destino/capability/port/adapter, sin descarga/wiring.
- `SW-N30`: manifest special-surface OpenClaw/Agent Skills, exact refs/drift, sin descarga.
- `SW-N31`: contrato de reproducibilidad eval runner/benchmark/dataset/grader/seed/environment.
- `SW-N32`: dry-run manifest exacto de reparación spaCy, cero write canónico.
- `SW-N33`: contrato benchmark HTML/article extraction contra baseline existente.
- `SW-N34`: contrato WARC capture/readback Browsertrix+warcio, sin adquisición.

## GAP preservado
`SW-N26 = GAP / INFRA_FAILURE`: full tracked-tree byte replay no ejecutado; no convertirlo en PASS. Si se materializa follow-up debe resolver la limitación de acceso de manera distinta, sin repetir el mismo intento.

## Invariantes
`1 CHAT=1 ACTIVE NODE` · `1 NODE=1 OWNER` · `1 PATH=1 ACTIVE WRITER` · `EXACTLY 3 STEPS`.
Claim atómico: `READ FRESH → confirm SAFE/FREE → CREATE CLAIM → READBACK`.
409/stale: `ABORT → READ FRESH → REVALIDATE → RETRY`; nunca overwrite.

Workers sólo claim/evidence/log propios. `SOL-0` es el único writer de STATE/PLAN/CHECKPOINT/Handoff/Recovery/DAG/Queue/Watchdog.

## Gates
`M06=ASTRA_ONLY`, `M07=CLAUDE_ONLY`, `M08=GROK_ONLY`.
`SW-N09..SW-N12=BLOCKED_GATE`.
`physical_repair_allowed=false`; `b05_b06_download_allowed=false`; `step3_allowed=false`; motors `IMMUTABLE`.

Worker verdict permitido: `PASS_PENDING_SUPERVISOR_FANIN | PASS_PENDING_REVIEW | GAP | BLOCKED | INCONCLUSIVE`.
Nunca autocertificar `VERIFIED_CLOSED`.
