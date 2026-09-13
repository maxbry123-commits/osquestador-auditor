# SW-N31 — EVAL REPRODUCIBILITY PIN CONTRACT

- schema: `sharck-input.multisol-dag.v1`
- node_id: `SW-N31`
- parent_node: `M53_ADD_GAP_DERIVED_PREINTEGRATION_NODES`
- agent_name: `SOL-6-GPT`
- chat_id: `chat-sol6-20260912T2329-0500`
- mode: `READ_ONLY_DESIGN`
- claim_commit: `584e56f28e64cc8eefbd3e35d83a41551c24b083`
- claim_blob: `d6d3b42a8b34658fb8099c4aba619a242fbdb0ee`
- evidence_prewrite_head: `a8576c3c40662958f0e121e182108c88676d8706`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- downloads: `0`
- installs: `0`
- canonical_mutation: `NO`

## Assertion under test

The minimal eval stack selected by SW-N22 can be made reproducible only when runner, benchmark, dataset/task-set, grader, seed, environment, model identity and relevant config/input hashes are all immutable and replay comparisons fail closed on drift.

## STEP 1 — EXTRACT N22 STACK + DEPENDENCIES

SW-N22 recommends `MINIMAL_EVAL_STACK_V1`:

1. **Inspect AI** — primary general eval harness/orchestration.
2. **Promptfoo** — security/red-team/regression/CI lane.
3. **BrowserGym** — web-agent environment lane.
4. **MCPMark** — MCP-specific verified benchmark lane.
5. **Ragas + DeepEval** — existing baseline lane; no duplicate acquisition.

External batteries through adapters:
- SWE-bench — code/issue-resolution.
- tau2/tau3 — agent/user/tool policy and failure paths.
- BFCL — tool/function-calling.

Optional/deferred:
- AgentLab only when experiment-runner value beyond BrowserGym is measured.
- AgentBench only after isolated runnable-path/non-overlap validation.

### Immutable pins observed by N22

| component | observed immutable source pin | role |
|---|---|---|
| Inspect AI | `8ebe620d74c1eb679438db1b65324e30e2306092` | primary harness |
| Promptfoo | `7b404ae0492a4f19e3fa406ab3c9c77109dce278` | security/regression |
| BrowserGym | `9e779f087de9a65668b6974d11f9ce9816026e96` | web environment |
| AgentLab | `cbc35a9bc0facaf731bc858c5825edbe757c719f` | optional/defer |
| MCPMark | `cd45b7f57923b9b3985467f5139927575f83141c` | MCP benchmark |
| SWE-bench | `02e7a74ffd0b707aab73d203fe87bdc7c76afc8e` | external battery |
| tau2-bench | `2174a603f6d014ef94473ffa95957f6ce27100db` | external battery |
| AgentBench | `d1e4a10db08c87075c78972e48ecc182be03e2d5` | deferred |
| BFCL/gorilla | `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8` | external/reference battery |

These are evidence pins observed by N22; they do **not** authorize downloads and must not silently float to newer HEADs in a replay.

## STEP 2 — IMMUTABLE REPLAY SCHEMA

### `sharck.eval.reproducibility.v1`

A replayable eval run MUST persist the following contract before execution:

```json
{
  "schema":"sharck.eval.reproducibility.v1",
  "run_id":"immutable unique id",
  "runner":{
    "id":"inspect-ai|promptfoo|...",
    "repo":"official source",
    "commit":"40-hex immutable commit",
    "package_version":"optional but pinned when used"
  },
  "benchmark":{
    "id":"benchmark/task suite id",
    "repo":"official source/reference",
    "commit":"immutable commit",
    "version":"explicit benchmark/task-set version"
  },
  "dataset":{
    "id":"dataset/task set",
    "source":"repo/dataset pointer",
    "commit":"immutable revision when source supports it",
    "content_sha256":"exact materialized input-set digest"
  },
  "grader":{
    "id":"grader/evaluator id",
    "version":"explicit grader schema/version",
    "commit":"immutable grader code pin when applicable",
    "config_sha256":"grader prompt/rubric/config digest"
  },
  "seed":1337,
  "environment":{
    "image_digest":"sha256:<immutable container/sandbox digest>",
    "os":"platform/arch",
    "runtime_versions":{},
    "browser_version":null,
    "locale":"explicit locale",
    "timezone":"explicit timezone"
  },
  "model":{
    "provider":"provider id",
    "model_id":"exact model id",
    "version":"snapshot/version if available",
    "sampling_config_sha256":"temperature/top_p/etc digest"
  },
  "prompt_config_sha256":"...",
  "tool_manifest_sha256":"...",
  "input_set_sha256":"...",
  "score_schema":"versioned score schema",
  "expected_artifacts":["results","stdout","stderr","trace"],
  "secret_policy":"REDACT_VALUES_STORE_SECRET_REFS_ONLY"
}
```

### Mandatory immutable comparison fields

A result may be compared as an exact replay only when these are equal:

- runner commit/version;
- benchmark commit + benchmark/task-set version;
- dataset immutable revision + materialized content hash;
- grader version/commit/config hash;
- random seed when supported;
- environment image digest/runtime/browser/locale/timezone as applicable;
- provider/model/version plus sampling-config hash;
- prompt/config hash;
- tool manifest hash;
- input-set hash;
- score schema version.

If a field is intentionally changed, the result becomes a **new experiment lineage**, not an exact replay.

### Result/readback contract

After execution, persist:

- input contract digest;
- stdout/stderr/result/trace SHA256 values;
- score payload + score schema version;
- elapsed/resource metadata;
- exit code and failure class;
- resolved runtime/container/browser identities;
- secret-redaction verification;
- immutable links back to runner/benchmark/dataset/grader pins.

A PASS score without a complete replay manifest is `EVAL_RESULT_NONREPRODUCIBLE`, never system evidence for cross-run comparison.

## Executed synthetic validator

An isolated manifest comparator was executed; no package installation or external benchmark run was required.

### Drift matrix — 7/7 PASS

| case | expected | observed |
|---|---|---|
| exact replay | no drift | PASS |
| runner commit drift | reject exact replay | PASS: `runner.commit` detected |
| benchmark commit drift | reject exact replay | PASS: `benchmark.commit` detected |
| dataset content drift | reject exact replay | PASS: `dataset.content_sha256` detected |
| grader version drift | reject exact replay | PASS: `grader.version` detected |
| environment image drift | reject exact replay | PASS: `environment.image_digest` detected |
| seed drift | reject exact replay | PASS: `seed` detected |

### Required-field fail-closed matrix — 3/3 PASS

- missing `runner.commit` -> rejected;
- missing `grader.config_sha256` -> rejected;
- missing `environment.image_digest` -> rejected.

## STEP 3 — DRIFT REFUTATIONS + ACCEPTANCE TEMPLATE

### 3 primary drift scenarios

1. **Benchmark drift**: same model/result code, benchmark source moves to a new commit/task-set. Exact-replay comparison is rejected. A migration experiment may be created only with a new lineage id and explicit old→new benchmark mapping.
2. **Dataset/grader drift**: benchmark code stays fixed but task data or grader rubric/version changes. Score comparison is rejected because the evaluated function changed.
3. **Environment/runner drift**: inputs appear equal but runner commit/container/browser/runtime changes. Exact replay is rejected; environment is part of the experiment definition.

### 3 refutations

**REF-1 — “Pinning only the benchmark repo commit makes the run reproducible.”**
REFUTED. Dataset materialization, grader, runner, environment, model sampling/config and seed can independently change outcomes.

**REF-2 — “Same numeric score means two runs are comparable.”**
REFUTED. Scores are comparable only when score schema/grader plus required immutable provenance fields match or an explicit migration analysis exists.

**REF-3 — “Latest `main` is acceptable because the tool is actively maintained.”**
REFUTED. Maintenance status is not a replay identity. A mutable branch can change code/task/grading semantics without changing the experiment label.

### Acceptance template

A future eval run is `REPLAY_READY` only when all checks pass:

- `R01_RUNNER_PINNED`
- `R02_BENCHMARK_PINNED`
- `R03_DATASET_REVISION_AND_CONTENT_HASH`
- `R04_GRADER_VERSION_CONFIG_PINNED`
- `R05_SEED_RECORDED_OR_EXPLICITLY_UNSUPPORTED`
- `R06_ENVIRONMENT_DIGESTED`
- `R07_MODEL_AND_SAMPLING_CONFIG_IDENTIFIED`
- `R08_PROMPT_TOOL_INPUT_HASHES_COMPLETE`
- `R09_SCORE_SCHEMA_VERSIONED`
- `R10_ARTIFACT_HASHES_READ_BACK`
- `R11_SECRET_VALUES_REDACTED`
- `R12_NO_CANONICAL_PROJECT_MUTATION`

Any failed required check => `EVAL_REPRODUCIBILITY_BLOCKED`.

Cross-version comparison requires a separate explicit `COMPARABILITY_REVIEW` and must never be silently merged into an exact-replay series.

## GOALS12_OUTPUT

- G01 literal N31 requirement preserved: `PASS`
- G02 fresh HEAD read: `PASS`
- G03 M53 + N22 evidence read: `PASS`
- G04 atomic owner/readback: `PASS`
- G05 dependencies/gates valid: `PASS`
- G06 write scope non-overlapping: `PASS`
- G07 existing eval research reused/deduped: `PASS`
- G08 minimal permitted delta only: `PASS`
- G09 reproducibility validator tests: `PASS 7/7 + 3/3 malformed`
- G10 three refutations: `PASS`
- G11 evidence SHA/readback: `PENDING_WRITE_READBACK`
- G12 release/rescan: `PENDING_RELEASE`

## COUNCIL12

1. Objective: turn N22 eval guidance into deterministic replay provenance.
2. Requirement: design/read-only only; no installs/downloads.
3. Authority: N22 persisted pins and role partition + M53 node contract.
4. Physical state: no eval framework acquired or executed in production.
5. Owner: SOL-6 owns SW-N31 only.
6. Gates: all acquisition/physical/step3 gates remain false.
7. Collision risk: unique N31 evidence/claim and SOL-6 log only.
8. Causal GAP: version-sensitive benchmark/data/grader/environment state was specified conceptually but lacked one exact replay schema.
9. Alternatives: pin benchmark only rejected; mutable HEAD rejected; score-only comparison rejected.
10. StrategyDelta: immutable experiment manifest + artifact readback + lineage rule.
11. Tests/refutations: 7 drift cases + 3 malformed cases + 3 refutations.
12. Verdict: `PASS_PENDING_REVIEW`; reproducibility contract is complete as design evidence, not installed runtime.

## Remaining gaps

- No eval harness/candidate acquisition is authorized by this node.
- Provider-side model snapshots may not always expose immutable weight/build ids; unavailable fields must be explicit, never invented.
- Some benchmarks materialize datasets indirectly; exact materialized `content_sha256` remains mandatory even when upstream revision is pinned.
- Cross-version migration methodology is outside N31 and requires separate evidence if future scores must be normalized.

## Producer verdict

`PASS_PENDING_REVIEW`
