# SW-N32 EVIDENCE — spaCy exact repair manifest dry-run

- schema: `sharck-input.swarm-node-evidence.v1`
- agent: `SOL-8-GPT`
- chat_id: `chat-sol8-20260912T2313-0500`
- node: `SW-N32`
- parent: `M53_ADD_GAP_DERIVED_PREINTEGRATION_NODES`
- mode: `READ_ONLY_PLUS_SANDBOX`
- claim_commit: `a8576c3c40662958f0e121e182108c88676d8706`
- claim_blob: `a0bc3c57400abc8bdf913b19707861d1c5056d16`
- base_sha: `3e14f4bde24a5c10a4aba2ade1c98d426a5ce13d`
- fresh_head_before_evidence_write: `cfe46ffae262e6949483fefdfef8e6e951c05d3e`
- physical_mutation: `false`
- downloads: `0`
- canonical_motor_mutation: `false`
- shared_control_writes: `0`

## STEP 1 — SYNC / VERIFY / CLAIM

M53 dispatches `SPACY_EXACT_REPAIR_MANIFEST_DRYRUN`. Atomic claim was created and read back. N13, N23, B04 X-Ray and the canonical spaCy `DOWNLOAD_EXTRACT_MANIFEST.json` were reused; no terminal node was reclaimed and no canonical destination was modified.

Pinned source identity:
- repo: `explosion/spaCy`
- source commit: `26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`
- root Git tree: `84b6a710fe40e594b0827c794dc8db05091785be`

## STEP 2 — EXACT TWO-PATH ACCEPTANCE MANIFEST

| path | bytes | SHA256 | Git mode | Git type | Git blob |
|---|---:|---|---|---|---|
| `spacy/matcher/polyleven.c` | 9571 | `8d6cc95a1e44c334c3a5c1ffe3011f7e8d7a0afea27345d769a7db7d16abce0a` | `100644` | `blob` | `2f2b8826c50754f496e0ef09c9367173679f41de` |
| `website/.vscode/extensions.json` | 165 | `515b1ef75f9d7e9b2e63f7009ffe9b9cf4a809b27d7a96265f72f48127767fdf` | `100644` | `blob` | `4b533827a909bc135ca82fcb122587645508b302` |

Immutable Git-tree reads prove both are regular `100644` blobs at the pinned commit. The N13 historical `symlink_dereferenced` label for `polyleven.c` is therefore not supported by the pinned Git source tree. N23 independently proved the `.vscode` path loss is `IMPORTED_GITIGNORE_RESTAGING_CONFIRMED`.

### Current partial → target arithmetic

Current canonical partial from B04 readback:
- files: `1774`
- bytes: `20626274`
- changed: `0`
- extra: `0`

Missing exact delta:
- files: `2`
- bytes: `9571 + 165 = 9736`

Target/source manifest:
- files: `1776`
- bytes: `20636010`
- tree SHA256: `cad7a1cdfae8046e24df6735336a9dace6ceebc917fc18eb9b1d187c4d875c1e`

Arithmetic guards:
- `1774 + 2 = 1776` — PASS
- `20626274 + 9736 = 20636010` — PASS

## Deterministic future acceptance contract — NOT EXECUTED PHYSICALLY

A future authorized repair is PASS only if ALL are true:
1. source commit equals exactly `26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`; modern HEAD cannot substitute it;
2. intended repair set is exactly the two paths above, unless a newly generated full-tree diff proves a different set and reviewer explicitly supersedes this manifest;
3. both files match exact bytes, SHA256, Git blob identity and mode `100644`;
4. pre-repair diff remains `2 missing / 0 changed / 0 extra`; unexpected drift aborts the repair;
5. staging preserves upstream tracked-set semantics instead of reinterpreting imported ignore rules; broad unsafe `git add -f` bypass is rejected;
6. special-file gates remain fail-closed;
7. published/canonical readback must equal `1776 files / 20636010 bytes / cad7a1cdfae8046e24df6735336a9dace6ceebc917fc18eb9b1d187c4d875c1e`;
8. folder/file presence or a successful commit is insufficient without the full-tree hash/readback;
9. any mismatch returns FAIL/GAP and must not promote spaCy to VERIFIED_CLOSED.

## STEP 3 — SANDBOX TEST / REFUTE / REPORT

### Validator results
- positive exact manifest: PASS (`0` errors)
- mutate `extensions.json` SHA256: `PATH_MANIFEST_MISMATCH` — PASS fail-closed
- mutate `polyleven.c` mode `100644 → 120000`: `PATH_MANIFEST_MISMATCH` — PASS fail-closed
- mutate target files `1776 → 1775`: `TREE_FILES_MISMATCH` — PASS fail-closed
- arithmetic guard: PASS
- zero canonical mutation/download/shared-control write: PASS

### 3 simulations
1. **Correct pinned replay:** both exact files + target full-tree totals/hash → validator accepts only when all fields match. PASS.
2. **Imported-ignore recurrence:** `.vscode` is silently omitted again → target file count/hash cannot match, therefore canonical full-tree guard fails. PASS.
3. **Special-file regression:** `polyleven.c` is represented as `120000` rather than pinned `100644` → path manifest fails before any promotion. PASS.

### 3 refutations
1. **“Restoring two filenames is enough for VERIFIED_CLOSED.”** REFUTED. Full canonical tree count/bytes/SHA256 and readback are mandatory.
2. **“Use blanket `git add -f` to solve imported ignore loss.”** REFUTED. It may stage unintended ignored content; reviewed upstream tracked-set-preserving staging is required.
3. **“Current spaCy HEAD can replace the pinned source.”** REFUTED. The acceptance manifest is bound to the immutable source commit recorded in the canonical download manifest.

## COUNCIL12
1. objective exact two-path repair dry-run — PASS
2. read-only/sandbox scope — PASS
3. authority pinned source + canonical manifest/X-Ray — PASS
4. claim/owner SOL-8 — PASS
5. gates unchanged false — PASS
6. exact 2-path identity — PASS
7. bytes/hash/modes/blobs — PASS
8. partial→target arithmetic — PASS
9. full-tree guard — PASS
10. unsafe alternatives rejected — PASS
11. simulations/refutations — PASS
12. supervisor fan-in still required; no VERIFIED_CLOSED claim — PASS

## GOALS12_OUTPUT
G01-G10: PASS.  
G11: evidence readback required immediately after publication.  
G12: release + fresh queue rescan required after readback.

## Worker verdict before evidence readback

`PASS_PENDING_EVIDENCE_READBACK_THEN_SUPERVISOR_FANIN`

spaCy remains physically unrepaired. `physical_repair_allowed=false`, `step3_allowed=false`, and canonical motors remain immutable.
