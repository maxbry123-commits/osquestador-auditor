# SW-N37 EVIDENCE — EVAL CROSS-VERSION COMPARABILITY CONTRACT

- schema: `sharck-input.swarm-node-evidence.v2`
- agent_name: `SOL-7-GPT`
- chat_id: `sol7-5f38c044-03f6-4c32-a681-663c0e16b94f`
- node_id: `SW-N37`
- parent_node: `M54_POST_M53_EVIDENCE_CONTINUATION`
- task: `EVAL_CROSS_VERSION_COMPARABILITY_CONTRACT`
- mode: `READ_ONLY_DESIGN`
- claim_commit: `d22faa5c4b7292a2d5e69120a6f99816a645c4b7`
- source_contract: `SW-N31-EVIDENCE.md`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- downloads: `0`
- installations: `0`
- canonical_mutations: `0`

## STEP 1 — immutable replay dimensions extracted from N31

Exact replay identity requires equality of all applicable dimensions:

1. runner source commit/package version;
2. benchmark source commit + benchmark/task-set version;
3. dataset immutable revision + materialized content SHA256;
4. grader version/commit/config SHA256;
5. seed or explicit unsupported marker;
6. environment image digest, OS/arch, runtime, browser, locale, timezone;
7. provider/model/version or explicit snapshot guarantee classification;
8. sampling-config SHA256;
9. prompt/config SHA256;
10. tool-manifest SHA256;
11. input-set SHA256;
12. score-schema version.

Any change means the two runs are not the same exact replay lineage.

## STEP 2 — cross-version migration classes

### `sharck.eval.comparability.v1`

Every old→new comparison MUST classify itself before score comparison.

| class | allowed drift | direct aggregate comparison | required evidence |
|---|---|---|---|
| `EXACT_REPLAY` | none in required replay dimensions | YES | exact manifest equality + artifact readback |
| `MODEL_ONLY_EXPERIMENT` | evaluated model/version and declared sampling treatment only; eval function fixed | YES, as an experiment comparison, not replay identity | all evaluator-side dimensions equal; changed model field explicit |
| `INFRA_EQUIVALENT_MIGRATION` | runner/runtime/browser/container implementation change only | CONDITIONAL | paired anchor replay on identical inputs; score/output invariance within declared tolerance; no benchmark/data/grader/score drift |
| `EVAL_SEMANTICS_MIGRATION` | benchmark/task-set/dataset/grader/score-schema changes | NO globally; CONDITIONAL only on explicitly frozen intersection or calibrated dual-evaluation | item-level old/new mapping, content hashes, dual-grader/dual-version results, migration report |
| `NONCOMPARABLE` | unbounded, unknown, missing provenance, multiple uncontrolled changes, mutable latest refs | NO | must fail closed |

### Fail-closed comparison rules

`C01` Exact replay label requires equality of every required N31 replay field.

`C02` If only model identity changes while evaluator-side contract remains byte/version identical, runs may be compared as a controlled model experiment; they remain different run lineages.

`C03` Infrastructure migration may not claim score comparability until a frozen anchor set is executed under both old and new infrastructure and demonstrates evaluator invariance. Any item-level mismatch outside the declared tolerance blocks comparison.

`C04` Dataset/task-set version changes prohibit whole-score comparison. Only the exact intersection whose item content hashes are identical may be compared, and that intersection score must be labeled separately.

`C05` Grader/rubric/config changes prohibit direct score comparison. A migration requires grading the same frozen outputs with both graders and publishing a calibration/mapping report. Without that evidence, scores are noncomparable.

`C06` Score-schema changes require an explicit deterministic mapping. If the mapping is many-to-one, lossy, or ambiguous, old/new aggregate scores remain separate.

`C07` Benchmark implementation change plus dataset/grader change is `EVAL_SEMANTICS_MIGRATION`, never `INFRA_EQUIVALENT_MIGRATION`.

`C08` Missing provider snapshot/build identity must be explicit. Unknown identity can never be silently treated as equal across runs.

`C09` Prompt/tool-manifest/input-set changes create a treatment/config migration; direct model-quality attribution is prohibited unless those are the declared independent variable and all other dimensions are fixed.

`C10` A migration report must preserve both original manifests and never rewrite historical provenance.

### Migration report minimum schema

```json
{
  "schema":"sharck.eval.comparability.v1",
  "comparison_id":"immutable-id",
  "old_run_id":"...",
  "new_run_id":"...",
  "class":"EXACT_REPLAY|MODEL_ONLY_EXPERIMENT|INFRA_EQUIVALENT_MIGRATION|EVAL_SEMANTICS_MIGRATION|NONCOMPARABLE",
  "changed_dimensions":[],
  "unchanged_dimensions":[],
  "old_manifest_sha256":"...",
  "new_manifest_sha256":"...",
  "anchor_or_intersection_manifest_sha256":null,
  "mapping_or_calibration_sha256":null,
  "comparison_scope":"full|intersection|paired-anchor|none",
  "verdict":"COMPARABLE|CONDITIONALLY_COMPARABLE|NONCOMPARABLE",
  "reason_codes":[]
}
```

## STEP 3 — synthetic old→new migration matrix

| case | old→new drift | expected verdict | observed contract decision |
|---|---|---|---|
| M01 | no drift | `EXACT_REPLAY / COMPARABLE` | PASS |
| M02 | model id only, evaluator contract identical | `MODEL_ONLY_EXPERIMENT / COMPARABLE` | PASS |
| M03 | container digest only, paired anchors identical | `INFRA_EQUIVALENT_MIGRATION / CONDITIONALLY_COMPARABLE` | PASS |
| M04 | container digest only, anchor score differs | `NONCOMPARABLE` until root cause resolved | PASS |
| M05 | dataset v1→v2 with 80% identical item hashes | global `NONCOMPARABLE`; frozen 80% intersection may be compared separately | PASS |
| M06 | grader v1→v2, no dual-grading calibration | `NONCOMPARABLE` | PASS |
| M07 | grader v1→v2 with dual-grade mapping but residual ambiguity | `NONCOMPARABLE` for aggregate claims | PASS |
| M08 | score schema v1→v2 with exact reversible mapping | `EVAL_SEMANTICS_MIGRATION / CONDITIONALLY_COMPARABLE` only under mapped scope | PASS |
| M09 | runner commit + benchmark + dataset all drift | `NONCOMPARABLE` | PASS |
| M10 | mutable `main`/latest references with no immutable identities | `NONCOMPARABLE` | PASS |
| M11 | prompt changes while model constant | new treatment lineage; not model-quality comparison | PASS |
| M12 | model provider returns same alias but immutable snapshot unknown | `NONCOMPARABLE` for exact replay claim | PASS |

Synthetic decision matrix: `12/12 PASS`.

### Three required refutations

**REF-1 — “Same benchmark name means scores across benchmark versions are comparable.”**
REFUTED. Task-set, dataset, grader and score semantics can change while the public benchmark name remains unchanged.

**REF-2 — “If aggregate score differs only slightly after an environment upgrade, comparison is safe.”**
REFUTED. Magnitude alone does not prove semantic equivalence; paired anchor invariance is required.

**REF-3 — “A new grader can be compared to an old grader if both output the same scale.”**
REFUTED. Equal numeric range does not establish equal scoring function; dual-grading/calibration evidence is required.

Additional refutation: **“Cross-version normalization can replace the original run provenance.”** REFUTED; historical manifests remain immutable and the migration is a separate evidence object.

## Acceptance contract

A cross-version comparison is accepted only when all applicable checks pass:

- `X01_OLD_MANIFEST_COMPLETE`
- `X02_NEW_MANIFEST_COMPLETE`
- `X03_CHANGED_DIMENSIONS_EXPLICIT`
- `X04_MIGRATION_CLASS_VALID`
- `X05_NO_MUTABLE_REF_AS_IDENTITY`
- `X06_ITEM_HASH_INTERSECTION_EXPLICIT_IF_DATA_DRIFT`
- `X07_DUAL_EVALUATION_REQUIRED_IF_GRADER_DRIFT`
- `X08_PAIRED_ANCHOR_REQUIRED_IF_INFRA_DRIFT`
- `X09_SCORE_SCHEMA_MAPPING_EXPLICIT_IF_CHANGED`
- `X10_UNKNOWN_MODEL_SNAPSHOT_FAILS_EXACT_REPLAY`
- `X11_HISTORICAL_MANIFESTS_UNCHANGED`
- `X12_COMPARISON_SCOPE_LABELED`

Any failed required check => `EVAL_CROSS_VERSION_COMPARISON_BLOCKED`.

## Verification

- schema steps: `3/3 PASS`
- replay dimensions from N31 covered: `12/12`
- migration classes: `5/5 defined`
- fail-closed rules: `10/10`
- synthetic migration cases: `12/12 PASS`
- acceptance checks: `12/12 contract-defined`
- required refutations: `3/3 PASS` (+1 additional)
- downloads/installations/canonical mutations: `0/0/0`

## Worker verdict

`PASS_PENDING_FINAL_READBACK_THEN_SUPERVISOR_FANIN`

Remaining boundaries:
- this node does not authorize any eval acquisition or execution;
- comparability evidence cannot manufacture immutable model snapshot ids unavailable from a provider;
- actual future migrations must execute the required anchor/intersection/dual-grading procedure before scores are merged or compared.
