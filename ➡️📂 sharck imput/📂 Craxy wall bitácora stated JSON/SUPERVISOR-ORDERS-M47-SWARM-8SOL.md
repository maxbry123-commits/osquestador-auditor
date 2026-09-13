# SUPERVISOR ORDERS — M47 — SOL GPT 1–8

## Current command
`READ FRESH → CLAIM FIRST SAFE FREE READY NODE → EXECUTE EXACT 3 STEPS → TEST/REFUTE → OWN LOG + UNIQUE EVIDENCE → RELEASE → NEXT`

## Ready queue
1. `SW-N01` — M40/20X/canonical-117 dedup + decision matrix.
2. `SW-N02` — 11 source-special/symlink provenance forensic audit.
3. `SW-N03` — 139 anomaly exact classification across 12 partial components.
4. `SW-N04` — StrategyDelta sandbox coverage expansion design/test, no canonical mutation.
5. `SW-N05` — Hugging Face bridge ports/adapters/failure-contract audit.
6. `SW-N06` — runtime/agent candidate maintenance/upstream/license/overlap audit.
7. `SW-N07` — component→capability→port→adapter→test matrix.
8. `SW-N08` — STATE/PLAN/CHECKPOINT/Handoff/Recovery/DAG contradiction watch.

## Atomic claim
A worker must create `swarm-claims/CLAIM-<NODE_ID>.json` on fresh `main` and read it back. Existing claim file means occupied; do not overwrite or wait: re-read queue and claim another READY node.

## Worker write boundaries
Each worker writes only:
- its `SOL-SWARM-0N-LOG.md`;
- its claimed `SW-Nxx-EVIDENCE.md`;
- the unique atomic claim file for that node.

Workers do NOT write shared STATE/PLAN/CHECKPOINT/Handoff/Watchdog/DAG/queue.

## Supervisor fan-in
`SOL-0` alone reads worker evidence, refutes it, reconciles claims/status and performs sequential fresh-SHA shared writes.

## Blocked until gates change
- `SW-N09` physical repair of 23 FAILED.
- `SW-N10` new B05/B06/M40 acquisition.
- `SW-N11` production wire/prune/min-code.
- `SW-N12` final system test/fan-in.

## Reserved owners
- `M06 ASTRA` — ASTRA only.
- `M07 CLAUDE` — CLAUDE only.
- `M08 GROK` — GROK only.

## Fail-closed
No worker result is `VERIFIED_CLOSED` by self-report. Worker emits `PASS_PENDING_SUPERVISOR_FANIN | GAP | BLOCKED | INCONCLUSIVE`. Physical gates remain false until explicit later evidence changes them.
