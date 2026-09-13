# SW-N03 EVIDENCE — 139 ANOMALIES / 12 PARTIAL COMPONENTS

- schema: `sharck-input.swarm-node-evidence.v1`
- agent_name: `SOL-1-GPT`
- chat_id: `chat-sol1-20260912T2305-0500`
- node_id: `SW-N03`
- parent_node: `M47_8SOL_SWARM_CONTROL_PLANE`
- mode: `READ_ONLY_FORENSIC`
- claim_commit: `8be890dce641d42d4b1fb447f838b4e143b86667`
- claim_blob: `d68a35b9f623354b353266104ed1c3cdabb5d558`
- base_sha: `1943a81ededc219ef2423e8d17d4cffe6e88d074`
- fresh_head_before_evidence_write: `de5f22df1e3c34fc33ebd3d2560f9dfd489890b2`
- stale-head revalidation: `PASS`; intervening SW-N04 claim has distinct write scope.
- primary_classification: `EVIDENCE_FAILURE + CONTROLLED_CAUSAL_CLASSIFICATION`
- physical_repair: `false`

## STEP 1 — SYNC / VERIFY / CLAIM

Atomic claim read-back verified at `swarm-claims/CLAIM-SW-N03.json`.

Primary evidence:
- `PARTIALS-XRAY-11-2026-09-11.md` blob `c0ceb058475522689b116c321c4993dc3bc4c030`, run `34567075204`.
- `NESTED-IGNORE-BLAST-RADIUS-2026-09-11.md` blob `5d01e883fae780203e3f1529c0a8fd5d2dc5c6b0`.
- `B04-XRAY-2026-09-11.md` blob `385d73c909d6d6d9fa17a44a397b51f8dc5b57e9`, spaCy readback run `34566821665`, diff run `34566985338`.
- `STRATEGYDELTA-COVERAGE-AUDIT-2026-09-11.md` blob `6fb85d20acee101264ea00a78eed0d613d412253`.

Global physical gates remain closed: no repair, no B05/B06 download, no Step3; canonical motors immutable.

### GOALS12_INPUT
- G01 literal requirement preserved: PASS.
- G02 fresh HEAD: PASS.
- G03 control plane + evidence artifacts: PASS.
- G04 owner/atomic claim: PASS.
- G05 gate valid for read-only forensic: PASS.
- G06 write scope unique: PASS.
- G07 existing X-Ray evidence reused before new inference: PASS.
- G08 delta minimal/evidence-only: PASS.
- G09 exact 139 accounting test defined: PASS.
- G10 3 simulations + 3 refutations required: PASS.
- G11 SHA/readback: claim PASS; evidence/log post-write readback required.
- G12 supervisor fan-in required: PASS.

## STEP 2 — EXECUTE / VERIFY

### A. Universe

The exact partial universe is:
- B01-B03: `11 components`, `130 missing + 7 changed + 0 extra = 137 anomalies`.
- B04 spaCy: `2 missing + 0 changed + 0 extra = 2 anomalies`.
- Total: `12 components / 139 exact anomalies`.

### B. Causal classification — 12/12 components

| component | missing | changed | exact anomalies | causal class | evidence verdict | required repair/test prerequisite |
|---|---:|---:|---:|---|---|---|
| scira | 12 | 0 | 12 | `IGNORE_RULE_RESTAGING` | `*.sql` ignored in imported `.gitignore`; tracked upstream files lost during re-vendoring | preserve exact upstream tracked set; bytes/modes; full-tree readback |
| nutch | 3 | 0 | 3 | `IGNORE_RULE_RESTAGING` | `conf/*.xml` and dependency-check subtree rules cover all 3 | exact source-commit tracked set + runtime config readback |
| yacy_search_server | 5 | 0 | 5 | `IGNORE_RULE_RESTAGING` | root/imported/nested rules cover all 5, including source Java path | preserve source/build files; compile/static check after authorized repair + full-tree readback |
| heritrix3 | 57 | 0 | 57 | `ROOT_IGNORE_RESTAGING` | root `dist/` rule covers 57/57 | preserve distribution tree, executable modes/scripts, byte/hash/full-tree equality |
| pyserini | 3 | 0 | 3 | `IGNORE_RULE_RESTAGING` | collections/indexes/logs rules cover `.gitkeep` sentinels | tracked-set equality + tree hash; no functional-pass shortcut |
| OpenSearch | 4 | 7 | 11 | `IGNORE_RULE_RESTAGING + ATTRIBUTES_EOL_MUTATION` | 4 `.idea/*` missing explained by ignore-parent collision; 7 LICENSE/NOTICE changed are CRLF→LF | preserve tracked set and exact bytes; prove no attributes mutation; full-tree/hash comparison |
| datasketch | 5 | 0 | 5 | `IGNORE_RULE_RESTAGING` | benchmark PNG rule covers 5/5 | tracked-set/byte equality; benchmark artifacts restored only through authorized staging |
| smolagents | 1 | 0 | 1 | `IGNORE_RULE_RESTAGING` | `tests/data` ignored; exact PNG missing | exact fixture byte/hash and full-tree readback |
| kythe | 14 | 0 | 14 | `IGNORE_RULE_RESTAGING` | build/, *.class, .vscode and libmemcached rules cover 14/14 | preserve code/build/proto/test assets and relevant Git modes; full-tree equality |
| sqry | 21 | 0 | 21 | `ROOT_IGNORE_RESTAGING` | root `build/` pattern covers all 21 core Rust files | CRITICAL: exact source tree, byte/mode equality, syntax/build test only after gate, full-tree readback |
| continue | 5 | 0 | 5 | `IGNORE_RULE_RESTAGING` | `*.iml` plus nested webview parent ignore cover all 5 | preserve webview runtime resource + tracked-set equality; targeted integration check after gate |
| spaCy | 2 | 0 | 2 | `CAUSE_UNPROVEN_EXACT_PARTIAL` | exact missing paths/hashes are proven, but current cited evidence does NOT prove why those two disappeared | restore only from exact source commit/versioned clean path after review; expected manifest 1776 files/20636010 bytes/tree hash + full canonical readback |

### C. Arithmetic reconciliation

B01-B03 missing:
`12 + 3 + 5 + 57 + 3 + 4 + 5 + 1 + 14 + 21 + 5 = 130`.

B01-B03 changed:
`OpenSearch 7 = 7`.

B04 spaCy:
`2 missing = 2`.

Global:
`130 ignore-associated missing + 7 attributes/EOL changed + 2 spaCy cause-unproven missing = 139/139`.

### D. Cause confidence

- `130/139` = exact paths with concrete ignore-rule causal coverage.
- `7/139` = exact OpenSearch files with concrete `.gitattributes`/CRLF→LF content-mutation evidence.
- `2/139` = exact spaCy paths/hashes known, but causal mechanism is **not proven by the cited evidence**.

Therefore the correct fail-closed statement is `139/139 ACCOUNTED`, but only `137/139 CAUSALLY EXPLAINED`; the remaining `2/139` are `CAUSE_UNPROVEN`, not guessed into the ignore class.

### E. Repair/test contract by causal class

1. `IGNORE_RULE_RESTAGING` / `ROOT_IGNORE_RESTAGING`:
   - repair strategy must preserve the exact upstream tracked file set independent of destination/imported `.gitignore` semantics;
   - must not weaken special-file gates;
   - verify `tracked_upstream_set == staged_set == published_set`;
   - verify bytes and relevant Git modes (100644/100755);
   - canonical full-tree/hash readback required.

2. `ATTRIBUTES_EOL_MUTATION`:
   - copy/stage must preserve upstream bytes and avoid CRLF→LF mutation;
   - compare exact blob/byte hashes for all 7 changed files;
   - canonical full-tree readback required.

3. `CAUSE_UNPROVEN_EXACT_PARTIAL` (spaCy):
   - no causal repair assumption;
   - use exact source commit `26b4d1dc04a812f426e4bef3e8a1b6f159d6f048` and two proven missing paths only after gate/reviewer decision;
   - verify both path SHA256 values from B04-XRAY plus expected manifest/tree totals;
   - if causal reproduction cannot be established, keep GAP explicit.

### F. Coverage implication

Current M25 sandbox exercised only `3/12 components` and `4/139 anomalies = 2.88%`. It does not validate the entire causal universe. Specifically, full sqry, heritrix3, yacy, nutch, kythe, scira, continue, datasketch, smolagents, pyserini, OpenSearch missing paths and six additional changed files remain unexercised; source-special/symlink failures are outside this node entirely.

## STEP 3 — TEST / REFUTE / REPORT

### Three simulations
1. `sqry`: a tracked upstream Rust path under `build/` disappears on vendor re-add → classification remains `ROOT_IGNORE_RESTAGING`; valid future test requires all 21/21 exact tracked paths plus modes/bytes, not one sample.
2. `OpenSearch`: 4 missing and 7 changed coexist → they must remain two causal sub-classes; repairing ignore behavior alone cannot prove the 7 byte mutations fixed.
3. `spaCy`: exact two missing paths are known but cause is not → system must abstain from assigning ignore/EOL cause and require exact-source readback after authorized repair.

### Three refutations
1. Refute `all partials are failed downloads`: FALSE. 130 missing are associated with Git ignore staging semantics and 7 changes with attributes; source acquisition itself is not demonstrated incomplete by this evidence.
2. Refute `all 139 anomalies are caused by ignore rules`: FALSE. 7 are attributes/EOL changes and 2 spaCy causes remain unproven.
3. Refute `M25 sandbox PASS authorizes production`: FALSE. Coverage is only 3/12 components and 4/139 anomalies; production gate remains false.

### Test results
- component accounting: `12/12` mapped — PASS.
- anomaly accounting: `139/139` accounted — PASS.
- causal proof: `137/139` explained, `2/139 explicit unknown` — PASS fail-closed.
- physical repair: `0` — PASS scope invariant.
- source-special/symlink scope pollution: `0` — PASS; those remain separate N02/M08 concerns.
- canonical motor mutation: `0` — PASS.

### COUNCIL12
1. Objective: classify exact partial anomaly universe.
2. Requirement: no physical repair; preserve exact evidence and unknowns.
3. Authority: exact diff/readback runs and physical artifacts > control summaries > inference.
4. State: 12 partial components / 139 anomalies remain FAILED, not VERIFIED_CLOSED.
5. Owner: SOL-1-GPT exclusively owns SW-N03 after atomic claim.
6. Gates: physical repair/download/Step3 false.
7. Collision: SW-N04 claimed independently; no path overlap.
8. Causal GAP: re-staging ignore/attributes explains B01-B03; spaCy cause remains unresolved.
9. Alternatives rejected: blind retry, global ignore bypass, normalization of unknown spaCy cause.
10. StrategyDelta: causal-class-specific staging/readback requirements; no production execution.
11. Tests/refutations: exact arithmetic + 3 simulations + 3 refutations.
12. Verdict: `PASS_PENDING_SUPERVISOR_FANIN` with `2/139 CAUSE_UNPROVEN` preserved.

### GOALS12_OUTPUT
- G01 literal preserved: PASS.
- G02 fresh HEAD revalidated: PASS.
- G03 control/evidence read: PASS.
- G04 claim/owner: PASS.
- G05 gate: PASS.
- G06 scope isolation: PASS.
- G07 reuse/dedup: PASS.
- G08 minimal delta: PASS.
- G09 exact test: PASS.
- G10 simulations/refutations: PASS.
- G11 evidence/log readback: pending immediate post-write readback.
- G12 supervisor fan-in required: PASS.

## WORKER VERDICT
`PASS_PENDING_SUPERVISOR_FANIN`

Remaining GAPs:
- `2/139` spaCy paths have exact evidence but unresolved causal mechanism;
- M25 coverage is insufficient for production;
- repair remains gated by M06/M07/M08 + director + explicit physical_repair_allowed;
- this node does not touch the 11 source-special/symlink failures.
