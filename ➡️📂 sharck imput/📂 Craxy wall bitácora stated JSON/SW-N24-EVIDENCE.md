# SW-N24 EVIDENCE — HISTORICAL SOURCE COMMIT RECOVERY FEASIBILITY

- agent: `SOL-9-GPT`
- node: `SW-N24`
- mode: `READ_ONLY_FORENSIC`
- fresh_head_before_write: `c52d80291ba30d4a82d338354fe4c84d069b40b5`
- verdict: `PASS_PENDING_SUPERVISOR_FANIN`
- physical_mutation: `false`

## 11/11 recovery matrix
Recovery target is the immutable upstream commit used by the failed acquisition attempt. Repo/path/error metadata alone is not a recovered source commit.

| batch | component | source_commit recovery |
|---|---|---|
| B01 | stormcrawler | NONRECOVERABLE |
| B01 | tika | NONRECOVERABLE |
| B01 | docling | NONRECOVERABLE |
| B02 | vespa | NONRECOVERABLE |
| B02 | networkx | NONRECOVERABLE |
| B03 | cocoindex | NONRECOVERABLE |
| B03 | pydantic-ai | NONRECOVERABLE |
| B03 | litellm | NONRECOVERABLE |
| B03 | fastmcp | NONRECOVERABLE |
| B04 | huggingface_hub | NONRECOVERABLE |
| B04 | unstructured | NONRECOVERABLE |

## Evidence
- `SPECIAL-FILES-PROVENANCE-GAP-2026-09-11.md`: `scan_tree()` can abort after acquire but before failed-row `result/source_commit` persistence.
- `SPECIAL-FILES-STATE-LEDGER-AUDIT-2026-09-11.md`: exact nine B01-B03 special-failure components and observed special surfaces.
- B01-B03 run `34514168678`, jobs `102995352354`, `102995352236`, `102995352003`: raw stdout contains motor balance but no per-failure upstream source commit; artifacts = `0`.
- B04 run `34551490992`, job `103115160403`: raw stdout contains motor balance and destination-repo persistence SHA but no upstream pin for failed items; artifacts = `0`.
- `B04-INDEX.md` has empty source-commit cells for `huggingface_hub` and `unstructured`, while successful items contain immutable commits.

## 3 simulations
1. B01: state + raw log + artifacts checked for stormcrawler/tika/docling; no immutable source pin recovered.
2. B02/B03: state + raw logs + artifacts checked for six failures; no immutable source pin recovered.
3. B04: state/index + raw log + artifacts checked for huggingface_hub/unstructured; no immutable source pin recovered.

## 3 refutations
1. Runner and destination-repository SHAs visible in logs are not dependency `source_commit`; rejected.
2. Modern upstream HEAD cannot substitute the historical attempt because the acquisition ref was mutable and capture-time SHA was not persisted; rejected.
3. Workflow timestamp or destination persistence SHA cannot deterministically identify an upstream commit without a recorded mapping; rejected.

## Future persistence contract
Before `scan_tree(src)`, durably persist `slug`, `source_repo`, requested ref, resolved immutable `source_commit`, attempt id and acquisition timestamp. Any later FAILED result must retain that record. Persist special-entry path/type/mode/link-target evidence keyed to that commit. Tests must inject `scan_tree` failure and prove the pin survives, then advance upstream HEAD and prove replay uses stored commit.

## Boundary
No fabricated SHA. No modern-HEAD substitution. No canonical destination/motor/shared-control mutation. Physical repair/download/Step3 gates remain closed. Worker verdict is `PASS_PENDING_SUPERVISOR_FANIN`, not `VERIFIED_CLOSED`.
