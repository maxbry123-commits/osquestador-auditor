# SW-N26 EVIDENCE — FRESH TRACKED-TREE REPLAY SANDBOX

- schema: `sharck-input.swarm-node-evidence.v1`
- node_id: `SW-N26`
- parent_node: `M51_ADD_CONCURRENCY_AND_REPLAY_SAFE_NODES`
- agent_name: `SOL-10-GPT`
- chat_id: `sol10-0284245c-e710-416b-9488-4d2cd6fd7a50`
- mode: `SANDBOX_ONLY`
- claim_commit_sha: `593f42bccb95e7ccacc1d71c40aedfe2b9edaaae`
- claim_blob_sha: `20c0184364eac6882141fc5b9176a7fdfe5150b5`
- verdict: `GAP`
- classification: `INFRA_FAILURE`
- canonical_mutation: `NO`
- physical_repair: `NO`
- b05_b06_download: `NO`
- step3_production: `NO`
- canonical_motors_modified: `NO`

## Requirement preserved

M51 defines SW-N26 because SW-N15 passed 87/87 synthetic fixtures but left a **fresh full upstream tracked-tree replay** unresolved. Acceptance requires an exact pinned source trace plus `missing/changed/extra/mode` report in sandbox only.

## STEP 1 — SYNC / VERIFY / CLAIM

Atomic claim was created and read back at `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/swarm-claims/CLAIM-SW-N26.json`.

### GOALS12_INPUT

G01 literal requirement preserved PASS; G02 fresh HEAD PASS; G03 current DAG/deltas/control evidence read without Watchdog PASS; G04 owner/claim free PASS; G05 sandbox gate valid PASS; G06 unique write scope PASS; G07 SW-N15/SW-N17 reused PASS; G08 no canonical delta PASS; G09 replay required PASS; G10 3 simulations+3 refutations required PASS; G11 evidence readback POST_WRITE; G12 release POST_WRITE.

## STEP 2 — EXECUTE / VERIFY

### Fresh pinned upstream

Representative: official `rapidfuzz/RapidFuzz`.

- source commit: `db6e504539a9c895180b266a06b36a32cb6029ee`
- source tree: `80b6ab641d0000bd5e6ed1706f6a8ba2c9478e0c`
- recursive tree: `truncated=false`
- root special surface: `.gitignore`, `.gitattributes`, `.gitmodules`
- mode `160000`: `extern/rapidfuzz-cpp@82662f3623b3ca3645e543f677fc32fb8bd1fb95`, `extern/taskflow@130f7952469c01eef8d7b635710bf9a8043f3172`
- mode `100755`: `tools/backtrace`, `tools/generate_cython.sh`, `tools/generate_python.py`, `tools/seg_wrapper.sh`

### SW-N17 comparator contract reused

`missing = source_paths - candidate_paths`; `extra = candidate_paths - source_paths`; `changed = same path/different content identity`; `mode = same path/content/different exact Git mode`. PASS requires all four empty after an **actual candidate copy/readback**.

### Execution attempts

1. Local exact Git fetch failed: `Could not resolve host: github.com`.
2. Exact GitHub REST tarball download failed after retries: `Could not resolve host: api.github.com`.
3. `sharck-input-staging-strategydelta-lite.yml` rejected as executor: hard-coded spaCy/OpenSearch/sqry + sampled paths.
4. `sharck-input-staging-strategydelta-sim.yml` rejected as executor: hard-coded spaCy/OpenSearch + sampled paths.
5. Creating/modifying a workflow would exceed SW-N26 write scope, so it was not done.

Root cause: `INFRA_FAILURE`. The execution container cannot resolve GitHub hosts for byte materialization. The GitHub connector can verify immutable Git objects but does not provide a generic archive/checkout execution primitive.

Verified: exact commit/tree PASS; complete recursive tree PASS; ignore/attribute/special/executable surface PASS; canonical mutation NO. Not proven: actual complete candidate byte materialization, copy/readback, or full-tree `missing/changed/extra/mode` parity.

## STEP 3 — TEST / REFUTE / REPORT

### Three executed simulations

1. `SIM-EXACT-METADATA`: exact ledger copy -> `missing=[] / extra=[] / changed=[] / mode=[]` PASS.
2. `SIM-SUBMODULE-LOSS`: remove `extern/taskflow` mode 160000 -> `missing=[extern/taskflow]` detected PASS.
3. `SIM-MIXED-DRIFT`: alter `.gitignore` object identity, `tools/backtrace` mode `100755→100644`, add `rogue.extra` -> `changed=[.gitignore] / mode=[tools/backtrace] / extra=[rogue.extra]` detected PASS.

These validate the comparator against fresh source-surface entries; they do not replace full-tree replay.

### Three refutations

1. `REFUTE-TREE-METADATA-EQUALS-REPLAY`: REFUTED — Git tree metadata without candidate byte readback is insufficient.
2. `REFUTE-OLD-WORKFLOW-CLOSES-N26`: REFUTED — workflows use different sources and sampled checks.
3. `REFUTE-SYNTHETIC-CLOSES-N26`: REFUTED — synthetic/fresh-surface simulations do not satisfy M51's full upstream copy/readback requirement.

### GOALS12_OUTPUT

G01 PASS; G02 source pin PASS; G03 project/control evidence PASS; G04 claim PASS; G05 gates PASS; G06 scope PASS; G07 dedup PASS; G08 zero canonical mutation PASS; G09 `GAP` byte materialization blocked; G10 3 simulations+3 refutations PASS; G11 evidence/readback pending this write; G12 node must not be marked DONE/100 PASS PASS fail-closed.

## COUNCIL12

1 objective fresh replay; 2 requirement pinned actual copy/readback; 3 authority M51+claim+Git objects; 4 canonical state untouched; 5 owner SOL-10/N26; 6 gates closed; 7 unique scope; 8 causal gap sandbox DNS; 9 alternatives local git/REST archive/existing workflows tested; 10 StrategyDelta rerun only where GitHub network is available without product mutation; 11 tests 3 simulations+3 refutations; 12 verdict `GAP`, **not DONE / not 100 PASS / not VERIFIED_CLOSED**.

## Remaining GAP

`G-SW-N26-FULL-BYTE-REPLAY`: in a sandbox with GitHub network access, materialize this pinned commit's complete tracked tree, preserve/report special modes, build the candidate through the allowed copy path, compute actual full-tree `missing/changed/extra/mode` sets, and read back the result. If source SHA changes, revalidate from zero.
