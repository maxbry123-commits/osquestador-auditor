# SW-N14 EVIDENCE — SPECIAL FILE SCAN PROVENANCE CONTRACT

- schema: `sharck-input.swarm-node-evidence.v2`
- agent_name: `SOL-7-GPT`
- chat_id: `sol7-5f38c044-03f6-4c32-a681-663c0e16b94f`
- node_id: `SW-N14`
- parent_node: `M48_10SOL_SWARM_FANIN_AND_NEXT_WAVE`
- task: `SPECIAL_FILE_SCAN_PROVENANCE_CONTRACT`
- mode: `READ_ONLY_DESIGN`
- claim_commit: `8b3e2f5668b571fa68d19ec68e9d3f3183b86faa`
- base_sha: `062173a7b40daa5841d86a71ab0c89874d810049`
- fresh_head_before_evidence_write: `ac038d8c4d9763ac579c6ba6a9c9001f9169e955`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- source_evidence: `SW-N02-EVIDENCE.md`

## Assertion under test

A future acquisition/replay can remain fail-closed on special files while preserving exact, replayable provenance if and only if immutable source identity is durably persisted before scanning and every non-regular/special object is classified from the pinned Git tree without guessing.

## STEP 1 — SYNC / VERIFY CLAIM

- M48 queue and DAG read fresh.
- `SW-N13` was already consumed/released; `SW-N14` was the first READY node with no claim file.
- unique claim `CLAIM-SW-N14.json` created and read back with owner `SOL-7-GPT`, state `CLAIMED`, and isolated write scope.
- no queue/STATE/PLAN/CHECKPOINT/HANDOFF/WATCHDOG/DAG mutation is authorized to this worker.
- no canonical component, acquisition motor, download, repair, or production wiring mutation is authorized.

## STEP 2 — EXECUTE / VERIFY

### A. Immutable source provenance contract

Contract id: `sharck-input.source-special-provenance-contract.v1`.

A replay/acquisition record MUST persist the following **before** any tree/special-file scan can throw:

```json
{
  "source_repo": "official owner/repo",
  "requested_ref": "branch|tag|HEAD|commit",
  "resolved_commit": "40-hex immutable dependency commit",
  "source_tree_sha": "tree object bound to resolved_commit",
  "provenance_persisted_before_scan": true,
  "scan_policy": "FAIL_CLOSED_SPECIAL_SURFACE_V1",
  "lfs_policy": "PROHIBITED_NO_GIT_LFS",
  "special_entries": [],
  "scan_complete": false
}
```

Required invariants:

1. `resolved_commit` is the third-party dependency commit, never the orchestration repository/workflow SHA.
2. `source_tree_sha` must be obtained from that immutable commit and bound to the same official repository.
3. provenance persistence occurs before traversal or content materialization.
4. scan walks the complete pinned Git tree and records exact path/mode/type/object SHA for every non-regular entry.
5. mode `120000` is classified as `SYMLINK` and its link-target blob is preserved as evidence; the target is not followed into an implicit copy.
6. mode `160000` is classified as `GITLINK_SUBMODULE`; the gitlink commit is recorded; recursive acquisition is forbidden unless separately authorized.
7. a regular blob that is an LFS pointer is classified as `LFS_POINTER`; Git LFS installation/pull/smudge is forbidden; replay fails closed under the project no-LFS rule.
8. any mode/object combination not in the allowlisted classifier is `UNKNOWN_SPECIAL` and fails closed.
9. ordinary regular files remain byte-addressable by pinned blob SHA; executable mode is preserved rather than normalized.
10. `scan_complete=true` may be persisted only after counts and entries reconcile to the full pinned tree.
11. no repair/copy/wiring follows from a PASS of this provenance contract; separate gates remain mandatory.

### B. Special-surface classifier

| Git surface | Required classification | Durable evidence | Action |
|---|---|---|---|
| regular `100644` | REGULAR | path + blob SHA | continue |
| executable `100755` | REGULAR_EXECUTABLE | path + blob SHA + mode | continue preserving mode |
| symlink `120000` | SYMLINK | path + blob SHA + exact target text | fail closed / strategy required |
| gitlink `160000` | GITLINK_SUBMODULE | path + referenced commit SHA | fail closed / no recursion by default |
| LFS pointer in regular blob | LFS_POINTER | path + pointer blob SHA + oid/size text only | fail closed; **no Git LFS** |
| unknown/non-allowlisted mode | UNKNOWN_SPECIAL | exact mode/type/object SHA | fail closed |

Directories/tree objects are traversal structure, not copied as file payloads.

### C. Acceptance schema

A replay is `PROVENANCE_ACCEPTED_FOR_REVIEW` only when all checks pass:

- `A01_OFFICIAL_SOURCE`: source repository identity is explicit and official/approved.
- `A02_IMMUTABLE_PIN`: exact dependency `resolved_commit` is persisted.
- `A03_PIN_BEFORE_SCAN`: durable provenance write precedes any scanner exception point.
- `A04_TREE_BINDING`: `source_tree_sha` resolves from the pinned commit.
- `A05_FULL_TREE_SCAN`: every tracked path is accounted for.
- `A06_MODE_EXACT`: special entries have exact Git modes; `special` is not silently renamed to `symlink`.
- `A07_SYMLINK_TARGET`: every `120000` entry preserves target evidence.
- `A08_GITLINK_EXPLICIT`: every `160000` entry records referenced commit and remains non-recursive by default.
- `A09_LFS_FAIL_CLOSED`: LFS pointer detection never invokes Git LFS and blocks replay pending an explicitly non-LFS strategy.
- `A10_UNKNOWN_FAIL_CLOSED`: unknown object/mode cannot pass.
- `A11_COUNTS_RECONCILE`: file/special/path counts reconcile to the pinned tree.
- `A12_NO_GATE_BYPASS`: acceptance does not authorize repair/download/Step3/canonical mutation.

Any failed item -> `REPLAY_BLOCKED_PROVENANCE_GAP`.

### D. Validation against the exact 11 historical source-special failures

Historical identity is deliberately **not reconstructed**. SW-N02 established all 11 used mutable `HEAD` and the failed canonical state did not durably preserve the acquired dependency `source_commit` before the early special-file failure.

| component | observed historical special surface | contract result | reason |
|---|---:|---|---|
| stormcrawler | 2 special paths | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | historical commit absent; future pin+mode ledger closes provenance gap |
| tika | >=30 special paths | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | cannot infer every special item is a symlink; exact modes required |
| docling | 6 special paths | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | future full-tree exact mode/object scan required |
| vespa | 3 special paths | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | immutable pin must precede scan |
| networkx | 1 special path | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | one special object still requires exact mode/type evidence |
| cocoindex | 7 special paths | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | exact mode/target ledger tied to pinned commit required |
| pydantic-ai | 15 special paths | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | exact mode/target ledger tied to pinned commit required |
| litellm | 1 special path | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | historical mutable HEAD cannot be replay identity |
| fastmcp | 2 special paths | `BLOCK_OLD_RUN / CONTRACT_APPLICABLE` | future immutable pin + full tree reconciliation required |
| huggingface_hub | current `CLAUDE.md` corroborated as mode `120000` | `BLOCK_OLD_RUN / SYMLINK_RULE_VALIDATED` | current topology corroborates classifier but cannot backfill historical commit |
| unstructured | 20-path special/symlink fixture surface corroborated | `BLOCK_OLD_RUN / SYMLINK_RULE_VALIDATED` | current evidence validates special handling but not historical snapshot identity |

Validation score: `11/11 CONTRACT_APPLICABLE`; `0/11 historical commits fabricated`; `0/11 repairs authorized`.

### E. Fail-closed replay prerequisites

Before any future gated replay of these historical failures:

1. choose an explicitly approved official source and exact immutable commit; do not use floating `HEAD` as replay identity.
2. persist `{source_repo, requested_ref, resolved_commit, source_tree_sha}` before special-file scanning.
3. enumerate the entire pinned tree and build the exact special-surface ledger.
4. classify `120000`, `160000`, LFS pointers, executable modes, and unknown modes without normalization.
5. do not follow symlinks, initialize submodules, or invoke Git LFS merely to make the scan pass.
6. reconcile path counts and blob/object SHAs against the pinned tree.
7. if the desired historical commit remains unknown, label the old run `HISTORICAL_REF_NONRECOVERABLE`; do not claim byte-identical historical replay.
8. only after this provenance layer passes may a separately authorized StrategyDelta decide how a specific special entry is represented.
9. physical repair/download/Step3/canonical-motor gates remain authoritative and closed in this node.

## STEP 3 — TEST / REFUTE / REPORT

### Tests

- `T01_PRE_SCAN_PIN`: contract rejects mutable-only `HEAD` with absent resolved dependency commit -> PASS.
- `T02_MODE_CLASSIFIER`: `120000`, `160000`, executable, LFS pointer, and unknown modes have distinct fail-closed handling -> PASS.
- `T03_NO_LFS`: no Git LFS install/pull/smudge is part of the contract -> PASS.
- `T04_11_CASE_MATRIX`: all 11 SW-N02 cases map to a deterministic contract verdict -> PASS (11/11).
- `T05_HISTORICAL_NONFABRICATION`: modern upstream evidence cannot overwrite unknown historical identity -> PASS.
- `T06_GATE_PRESERVATION`: contract completion opens no repair/download/Step3 gate -> PASS.

### Three simulations

**SIM-1 — mutable HEAD + scanner throws before provenance write**
Expected: `REPLAY_BLOCKED_PROVENANCE_GAP` because dependency identity is not durable. PASS.

**SIM-2 — pinned commit contains symlink + gitlink + LFS pointer**
Expected: exact entries are recorded; symlink not followed, submodule not recursively initialized, LFS not fetched; run remains fail-closed pending reviewed strategy. PASS.

**SIM-3 — current upstream resembles historical special topology**
Expected: current evidence may corroborate classifier behavior but cannot fill the historical `resolved_commit`; old run remains `HISTORICAL_REF_NONRECOVERABLE`. PASS.

### Three refutations

**REF-1 — “Current HEAD can stand in for the failed historical source.”**
REFUTED. Current HEAD may prove present topology, not the immutable dependency snapshot used by the old run.

**REF-2 — “Every prior `special` path can be treated as a symlink.”**
REFUTED. Without exact Git mode/object evidence, the contract preserves `UNKNOWN_SPECIAL` and fails closed.

**REF-3 — “Using Git LFS or initializing submodules is acceptable to make replay succeed.”**
REFUTED. Project policy forbids Git LFS; implicit submodule recursion also changes acquisition scope. Both require explicit separate authorization/strategy and are not part of this contract.

### Worker verdict

`PASS_PENDING_SUPERVISOR_FANIN`

- schema steps complete: `3/3`
- contract checks: `12/12`
- historical cases validated: `11/11`
- tests: `6/6`
- simulations: `3/3`
- refutations: `3/3`
- physical mutations: `0`
- downloads: `0`
- Git LFS operations: `0`
- canonical motor mutations: `0`
- remaining global gap: historical source commits for the old failed runs remain nonrecoverable from persisted canonical evidence; future repair still requires independent gates and supervisor/director review.
- worker cannot self-promote node to global `VERIFIED_CLOSED`; SOL-0 fan-in required.
