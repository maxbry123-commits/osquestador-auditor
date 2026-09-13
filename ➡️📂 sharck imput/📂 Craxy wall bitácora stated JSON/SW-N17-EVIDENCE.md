# SW-N17 — PLUMBING FULL-TREE COMPARE VALIDATOR

- schema: `sharck-input.multisol-dag.v1`
- node_id: `SW-N17`
- parent_node: `M48_10SOL_SWARM_FANIN_AND_NEXT_WAVE`
- agent_name: `SOL-6-GPT`
- chat_id: `chat-sol6-20260912T2329-0500`
- mode: `READ_ONLY_PLUS_SANDBOX`
- claim_commit: `2d87a1db1f1b28e838fad4e7590601954602a917`
- claim_blob: `d30d4c914aff1ee40673f7c000a3ddad83800f47`
- evidence_prewrite_head: `e39a3933b03c4944382e7deb925c043f6d17c85a`
- causal_class: `TEST_HARNESS_GAP + EVIDENCE_FAILURE`
- canonical_mutation: `NO`
- canonical_motors_modified: `NO`
- physical_repair: `NO`
- B05_B06_download: `NO`
- gates: `physical_repair_allowed=false / b05_b06_download_allowed=false / step3_allowed=false / canonical_motors=IMMUTABLE`

## Assertion under test

A reusable full-tree comparator can detect `missing`, `changed`, `extra`, and exact Git mode drift in an isolated fixture, closing the specific SW-N04 plumbing-validation gap without modifying canonical motors or destinations.

## STEP 1 — SYNC / VERIFY / CLAIM

`SW-N17` was selected from M48/M49 after real anti-collision handling: N14 was already owned by SOL-7, N15 became owned by SOL-9, N16 became owned by SOL-1. N17 had no claim file; SOL-6 created the unique lock and read it back.

Origin evidence `SW-N04-EVIDENCE.md` explicitly leaves `G-SW-N04-PLUMBING-COMPARE` open and requires future full tracked-set equality rather than anomaly-only checking.

### Current plumbing audit

Fresh readback of `.github/workflows/sharck-input-staging-strategydelta-lite.yml` shows:

1. It fetches exact pinned sources for three representative components.
2. It copies through immutable Motor 3 into isolated repos.
3. Candidate staging uses `git add -f` and a temporary `.gitattributes` removal/restore.
4. Verification compares only four selected paths.
5. Mode acceptance is only `mode in {100644,100755}`; it does **not** require source mode == candidate mode.
6. It does not enumerate and compare the complete source-vs-candidate tracked set.
7. It does not detect an unselected changed path or unselected extra path.
8. It does not prove committed-tree parity after staging.

Fresh `sqry/DOWNLOAD_EXTRACT_MANIFEST.json` does contain acquisition-level aggregate parity (`source_files=2817`, `extracted_tree.files=2817`, equal aggregate SHA256, extraction/reconstruction verified). That proves the acquisition/extraction artifact represented by the manifest, but it is not a path-level source-vs-final-staging ledger and cannot report which path is missing/extra/changed/mode-drifted.

**Root cause:** current evidence has useful aggregate acquisition hashes and representative staging checks, but no reusable path-level full-tree comparator for the staging/canonical-parity boundary.

## STEP 2 — EXECUTE / VERIFY IN ISOLATED SANDBOX

A synthetic Git fixture was created entirely outside the repository/canonical destinations.

Source tree:
- `a.txt` mode `100644`
- `bin/tool.sh` mode `100755`
- `nested/data.json` mode `100644`

Comparator ledger contract:

```text
ledger[path] = {
  mode: exact Git mode,
  sha256: hash of blob bytes
}

missing = source_paths - candidate_paths
extra   = candidate_paths - source_paths
changed = intersection where source.sha256 != candidate.sha256
mode    = intersection where source.mode != candidate.mode

PASS iff missing == extra == changed == mode == []
```

For the normal partial-component lane, modes other than `100644`/`100755` must fail closed and route to the separate special-file/provenance contract rather than being silently normalized.

### Executed sandbox tests

| Test | Mutation | Expected | Observed |
|---|---|---|---|
| T1 | exact clone | PASS | PASS: 0 missing / 0 extra / 0 changed / 0 mode |
| T2 | delete `nested/data.json` | detect missing | PASS: `missing=[nested/data.json]` |
| T3 | modify `a.txt` bytes | detect changed | PASS: `changed=[a.txt]` |
| T4 | add `extra.txt` | detect extra | PASS: `extra=[extra.txt]` |
| T5 | `bin/tool.sh` `100755→100644` | detect mode drift | PASS: `mode=[bin/tool.sh]` |
| T6 | combine all four faults | detect all four classes simultaneously | PASS: 1 missing + 1 extra + 1 changed + 1 mode |
| T7 | repair combined fixture to exact source | return to PASS | PASS: all four result sets empty |

The first harness attempt itself failed because the exact-control variant had no changes and the test harness incorrectly attempted a non-empty Git commit. That was classified `TEST_HARNESS_FAILURE`, fixed by reusing HEAD when the index has no delta, and the entire matrix was rerun successfully. No product behavior was changed to hide the harness failure.

### Adversarial comparison against current representative-check semantics

Three explicit false-PASS attacks were executed:

1. **Unselected changed path:** sample checker examined only selected paths and returned PASS; full-tree comparator returned FAIL with `changed=[nested/data.json]`.
2. **Executable-mode loss:** bytes stayed equal but `100755→100644`; current workflow-style mode-membership check returned PASS because `100644` is allowed; exact-mode comparator returned FAIL.
3. **Unselected extra path:** sample checker returned PASS; full-tree comparator returned FAIL with `extra=[rogue.bin]`.

These directly reproduce the reason SW-N04 required a full-tree comparator rather than additional sampled-path checks.

## Reusable validator acceptance contract

A future production-authorized validator should consume two immutable ledgers produced from the exact source commit and the staged/committed candidate tree and MUST:

1. bind source to immutable commit SHA before enumeration;
2. enumerate every tracked source path and exact Git mode;
3. enumerate every candidate staged/committed path and exact Git mode;
4. hash blob bytes without working-tree filters;
5. report four disjoint evidence sets: `missing`, `extra`, `changed`, `mode_mismatch`;
6. fail if any special Git mode appears in this regular-file lane;
7. fail if any of the four evidence sets is non-empty;
8. emit source/candidate file counts plus deterministic ledger digest;
9. compare both staged index and committed tree when production workflow reaches that gate;
10. preserve source ref, canonical motors and canonical destinations during sandbox validation.

This is a **validator contract and executed synthetic proof**, not production integration authorization.

## STEP 3 — TEST / REFUTE / REPORT

### Specific verification
- `CLAIM_READBACK`: PASS.
- `ORIGIN_GAP_REPRODUCED`: PASS (`G-SW-N04-PLUMBING-COMPARE` open in SW-N04 evidence).
- `CURRENT_WORKFLOW_SCOPE_AUDIT`: PASS; representative-path semantics confirmed.
- `MANIFEST_SCOPE_AUDIT`: PASS; aggregate extraction parity exists but no path/mode ledger for final staging parity.
- `FULLTREE_FIXTURE_MATRIX`: 7/7 PASS.
- `ADVERSARIAL_FALSE_PASS_TESTS`: 3/3 PASS.
- `NO_CANONICAL_MUTATION`: PASS.

### 3 simulations
1. `SIM-EXACT`: equal full trees produce PASS only with all four evidence sets empty.
2. `SIM-MIXED-FAULT`: one missing + one extra + one changed + one exact-mode mismatch are all detected in one run.
3. `SIM-REPAIR-RETEST`: restoring bytes, membership and exact executable mode returns the same previously-failing fixture to PASS.

### 3 refutations
1. `REFUTE-SAMPLING`: “selected path equality proves full tree” — REFUTED by an unselected byte change that sample validation missed.
2. `REFUTE-MODE-ALLOWLIST`: “100644 or 100755 is sufficient mode validation” — REFUTED by executable-bit loss that remained inside the allowlist.
3. `REFUTE-NO-EXTRA`: “source paths all checked means there are no extras” — REFUTED by a rogue extra path invisible to the selected-path checker.

## GOALS12_OUTPUT
- G01 literal node requirement preserved: `PASS`
- G02 fresh HEAD read: `PASS`
- G03 current M48/M49 DAG/queue + SW-N04 evidence read: `PASS`
- G04 owner lock: `PASS` (`SW-N17` / SOL-6)
- G05 dependencies/gates valid: `PASS`
- G06 write scope non-overlapping: `PASS`
- G07 existing workflow/manifests reused: `PASS`
- G08 delta minimal/permitted: `PASS` (evidence/log/claim only)
- G09 node-specific sandbox tests: `PASS 7/7`
- G10 three simulations + three refutations: `PASS`
- G11 evidence SHA/readback: `PENDING_PHYSICAL_READBACK`
- G12 release/next-node reconciliation: `PENDING_RELEASE`

## COUNCIL12
1. Objective: make full-tree parity testable, not sampled.
2. Requirement: read-only plus isolated sandbox only.
3. Authority: fresh workflow/manifests + SW-N04 evidence + executed sandbox output.
4. Physical state: canonical components untouched.
5. Owner: SOL-6 owns SW-N17 only.
6. Gates: all physical/download/step3 gates remain closed.
7. Collision risk: unique N17 evidence/claim + own SOL-6 log.
8. Causal GAP: missing path-level full-tree staging comparator.
9. Alternatives: sampled checks rejected; aggregate-only digest insufficient for causal diagnosis; path ledger chosen.
10. StrategyDelta: exact source/candidate ledgers + four fail sets + exact modes.
11. Tests/refutations: 7 base cases + 3 adversarial false-PASS attacks + 3 simulations/refutations.
12. Verdict: `PASS_PENDING_REVIEW` for the validator contract and isolated synthetic execution only.

## Remaining gaps
- The validator contract has not been wired into canonical workflow/motors; gate forbids that now.
- No 12-component production-like full-set sandbox was executed by N17; N15/N16 cover adjacent execution/mode lanes independently.
- Special files/symlinks/submodules/LFS remain outside this regular-file comparator and must fail closed into the provenance lane.
- Reviewer/SOL-0 fan-in remains required; producer does not self-certify `VERIFIED_CLOSED`.

## Producer verdict

`PASS_PENDING_REVIEW`
