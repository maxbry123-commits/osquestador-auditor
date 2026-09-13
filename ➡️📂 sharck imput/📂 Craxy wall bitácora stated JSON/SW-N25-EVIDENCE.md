# SW-N25 EVIDENCE — STALE HEAD CONCURRENCY PROTOCOL

- agent: `SOL-1-GPT`
- node: `SW-N25`
- mode: `SANDBOX_ONLY`
- claim_commit: `fd11e38afc8c32a5c521b8ec8e2e5a98b84c0c96`
- claim_blob: `96207e94d09365c863aa83d17aaa1e5a16196bf8`
- canonical/shared mutation: `0`

## STEP 1 — VERIFY
Origin GAP from SW-N17: a stale HEAD was recoverable after an unrelated concurrent write, but the race protocol had not been adversarially exercised as a standalone contract. M51 acceptance requires deterministic overlap detection, safe non-overlap revalidation, and no silent overwrite.

The first local harness invocation failed because of an argument-signature error. It was classified `TEST_HARNESS_FAILURE`, discarded, corrected, and the complete matrix was rerun from clean state.

## STEP 2 — EXECUTE
Synthetic repository state modeled HEAD chronology, changed paths, unique claim creation, optimistic content versions and mandatory readback.

| case | concurrent condition | observed verdict |
|---|---|---|
| T1 | no race | `PASS`, fast-forward write + readback |
| T2 | HEAD changed on unrelated path | `STALE_HEAD -> REVALIDATE_NON_OVERLAP -> PASS` |
| T3 | HEAD changed on worker write_scope | `STALE_HEAD -> ABORT_OVERLAP -> ABORT_RESCAN` |
| T4 | another worker creates same node claim first | second worker gets `CLAIM_COLLISION`, existing owner preserved |
| T5 | two updates start from same content version | first succeeds, stale second update rejected |
| T6 | overlapping target already changed by other worker | worker aborts; other worker content remains intact, proving no silent overwrite |

Protocol contract proven in sandbox:
1. record preflight HEAD;
2. immediately before write compare current HEAD;
3. if changed, enumerate intervening changed paths;
4. overlap with write_scope => abort/rescan;
5. non-overlap => reconstruct/revalidate against fresh HEAD, never write from stale base;
6. claim path existence => collision/no overwrite;
7. updates require fresh content/blob version;
8. after write, mandatory readback;
9. force/last-write-wins forbidden.

## STEP 3 — TEST / REFUTE
Executed matrix: `6/6 PASS` after harness correction.

Three simulations:
- fresh/no-race write: PASS;
- unrelated race requiring revalidation: PASS;
- overlapping race requiring abort: PASS.

Three refutations:
1. `any HEAD change permanently blocks work` — FALSE; unrelated changes can proceed only after fresh revalidation/reconstruction.
2. `non-overlap makes stale-base writing safe` — FALSE; protocol still rebases/reconstructs on current HEAD before material write.
3. `unique node claim prevents all write races` — FALSE; claim protects ownership, while path overlap and optimistic file-version checks are still required.

Acceptance:
- stale overlap detected deterministically: PASS;
- unrelated non-overlap permitted only after revalidation: PASS;
- claim collision fail-closed: PASS;
- stale update rejected: PASS;
- no silent overwrite: PASS;
- canonical mutation/download/shared control writes: 0.

Worker verdict: `PASS_PENDING_SUPERVISOR_FANIN`. No `VERIFIED_CLOSED` or physical gate change is asserted.
