# SW-N35 EVIDENCE — FULL BYTE REPLAY EXECUTOR PREFLIGHT

- schema: `sharck-input.swarm-node-evidence.v1`
- node_id: `SW-N35`
- parent_node: `M54_POST_M53_EVIDENCE_CONTINUATION`
- agent_name: `SOL-6-GPT`
- chat_id: `chat-sol6-20260912T2329-0500`
- mode: `READ_ONLY_PLUS_SANDBOX_DESIGN`
- task: `FULL_BYTE_REPLAY_EXECUTOR_PREFLIGHT`
- claim_commit: `074e275820204cadef04d364b39b4e9955ee5b54`
- claim_blob: `411760aca04861f6d4a0b6a0228b029950b021ae`
- claim_base_sha: `31e9abc282b7b6dc7f1e9db0dd14d97a6a0b689f`
- evidence_prewrite_head: `aee736d8ca60ac8236ddc03b56ff024a3b90bca0`
- canonical_mutation: `NO`
- workflow_created_or_modified: `NO`
- physical_repair: `NO`
- B05_B06_download: `NO`
- step3_production: `NO`
- Git_LFS: `FORBIDDEN / NOT USED`
- gates: `physical_repair_allowed=false / b05_b06_download_allowed=false / step3_allowed=false / canonical_motors=IMMUTABLE`

## Assertion under test

A safe executor path for the N26 full pinned tracked-tree byte replay can be identified without canonical mutation or production wiring.

## STEP 1 — EXECUTION PATH INVENTORY

Origin `SW-N26-EVIDENCE.md` was read fresh. N26 pinned `rapidfuzz/RapidFuzz@db6e504539a9c895180b266a06b36a32cb6029ee`, verified recursive source tree `80b6ab641d0000bd5e6ed1706f6a8ba2c9478e0c`, observed root `.gitignore/.gitattributes/.gitmodules`, two `160000` gitlinks and four `100755` paths, but failed actual byte materialization because its local execution container could not resolve GitHub hosts.

Available paths and classification:

1. **Local execution container** — `BLOCK`: N26 demonstrated DNS failure for `github.com` and `api.github.com`; cannot materialize pinned bytes.
2. **GitHub connector** — `METADATA/READBACK_ONLY`: can verify commits/trees/files but does not expose a generic checkout/archive execution primitive for building a candidate filesystem.
3. **Existing `gha-copy-files.yml`** — `BLOCK`: it has `contents: write`, commits and pushes to `main`; incompatible with N35 read-only/noncanonical scope.
4. **Existing StrategyDelta sandbox runner** — `CAPABILITY_PROOF_ONLY`: `sharck-input-staging-strategydelta-lite.yml` demonstrates `ubuntu-24.04`, external pinned Git fetch, temporary filesystem, `contents: read`, Motor 3 invocation, and no canonical push, but it is hard-coded to spaCy/OpenSearch/sqry and verifies only selected paths.
5. **Selected executor path** — `GHA_EPHEMERAL_GIT_PLUMBING_REPLAY_V1`: GitHub-hosted ephemeral runner, read-only repository permission, exact pinned source commit, full Git tree enumeration, byte materialization/readback in `/tmp`, no repository push and no canonical destination write.

## STEP 2 — SELECTED NONCANONICAL EXECUTOR CONTRACT

### Runtime envelope

- runner: GitHub-hosted ephemeral Linux runner;
- repository permission: `contents: read` only;
- network: source allowlist limited to exact official GitHub repository needed for the pinned replay;
- source ref: immutable commit SHA only; branch/tag/HEAD is forbidden;
- destination: runner-local temp directory only;
- output: logs + optional workflow artifact only; no `git push`, no canonical write;
- LFS: forbidden; fail if LFS is required/detected;
- control motor: canonical motors remain immutable and are not modified.

### Full tracked-tree source ledger

Enumerate the exact source tree from the pinned commit using Git plumbing, not the filtered working tree.

For every path record:

`path | exact git mode | object type | source object id | content identity`

- `100644/100755`: content identity = SHA256 of `git cat-file blob` bytes.
- `120000`: content identity = SHA256 of symlink target bytes stored by Git; mode must remain `120000`.
- `160000`: identity = exact gitlink commit OID; it is not flattened into regular files.
- any unsupported/special mode: fail closed.

### Candidate materialization

Build a fresh temp Git repository. For each regular/executable/symlink entry, materialize from source Git object bytes, hash the candidate bytes again and stage with the exact source mode. For `160000`, stage the exact gitlink OID and `160000` mode. Do not reuse the source index as the candidate proof.

Motor 3 by itself is **not** a full-tree executor for this source: its manifest is based on filesystem `is_file()`, records bytes/SHA256 but not Git modes, follows file semantics that do not preserve Git special-entry identity, and omits gitlink entries. Motor 3 may remain a separate regular-file copy primitive in other lanes, but N35 full-tree acceptance cannot depend on Motor-3-only output.

### Required readback comparator

Reuse N17 semantics over the complete source and candidate ledgers:

- `missing = source_paths - candidate_paths`
- `extra = candidate_paths - source_paths`
- `changed = same path / different content or gitlink identity`
- `mode_mismatch = same path / different exact Git mode`

PASS iff all four sets are empty. Emit source/candidate counts and deterministic ledger digests. No sampled-path substitute is accepted.

## STEP 3 — SYNTHETIC TEST / REFUTE

Synthetic source ledger included four identity classes:

- `README.md` `100644`
- `bin/tool.sh` `100755`
- `link` `120000`
- `extern/sub` `160000`

### Comparator matrix — 8/8 PASS

1. exact candidate -> PASS, all four drift sets empty.
2. regular-file byte drift -> detected in `changed`.
3. executable `100755→100644` -> detected in `mode_mismatch`.
4. symlink `120000→100644` with same target bytes -> detected in `mode_mismatch`.
5. gitlink commit OID drift -> detected in `changed`.
6. missing path -> detected in `missing`.
7. rogue path -> detected in `extra`.
8. mixed missing + extra + byte drift + mode loss -> all four classes detected simultaneously.

### Executor eligibility matrix — 8/8 PASS

Only `github_actions_ephemeral + pinned source + canonical_write=false + LFS=false + full tracked enumeration + exact modes + byte readback + special-mode lane + bounded network` returned READY.

The following each returned BLOCK with the expected reason:

- local DNS-blocked runtime;
- canonical/main push enabled;
- sampled-only validation;
- unpinned HEAD;
- LFS enabled/required;
- no special-mode handling;
- no candidate byte readback.

### Three refutations

1. `REFUTE-MOTOR3-ALONE-IS-FULLTREE`: PASS — refuted by absence of exact Git-mode and gitlink/symlink identity contract in Motor 3.
2. `REFUTE-CHECKOUT-ALONE-IS-REPLAY`: PASS — a source checkout without an independently materialized candidate/readback does not prove copy parity.
3. `REFUTE-SAMPLED-PARITY-IS-FULLTREE`: PASS — N17 already demonstrates unselected byte/extra/mode faults can false-PASS sampled workflows.

## Readiness / limits

`READY_EXECUTOR`: **YES, as an executor contract/preflight path.**

This node does not claim that the real RapidFuzz replay has run. Materializing a new generic full-tree workflow is outside SW-N35 write scope. A later authorized execution node may instantiate this exact contract on a GitHub-hosted ephemeral runner and then close or reclassify `G-SW-N26-FULL-BYTE-REPLAY` from real bytes/readback.

## Three final refutations requested by node loop

1. Did SW-N35 complete all three schema steps? `YES` — path inventory, selected exact executor contract, synthetic decision/refutation tests.
2. Does any real GAP remain? `YES, but outside N35 scope` — the executor contract is not yet materialized/executed against full RapidFuzz bytes; N26 replay gap remains until a later authorized execution.
3. Does evidence support producer-side PASS for this preflight? `YES` — path selection and contract validation pass; no claim of `VERIFIED_CLOSED` for N26 or project.

## Producer verdict

`PASS_PENDING_REVIEW / READY_EXECUTOR`
