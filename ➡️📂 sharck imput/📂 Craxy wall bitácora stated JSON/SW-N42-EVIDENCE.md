# SW-N42 — SPACY PRE-REPAIR DRIFT AND STAGING PREFLIGHT

- schema: `sharck-input.multisol-dag.v1`
- node_id: `SW-N42`
- parent_node: `M54_POST_M53_EVIDENCE_CONTINUATION`
- agent: `SOL-8-GPT`
- mode: `READ_ONLY_PLUS_SANDBOX`
- claim_commit: `97a6db912baa8ef0bea9cd3d283d9f787b663233`
- claim_blob: `d0cbe4c40fc9767e73884f0c391e393b21c28596`
- gates: `physical_repair_allowed=false / b05_b06_download_allowed=false / step3_allowed=false / canonical_motors=IMMUTABLE`
- physical repair/download/canonical mutation: `NO / 0 / NO`

## STEP 1 — source identities + pre-repair drift guard

Pinned source remains `explosion/spaCy@26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`.

Exact N32 identities revalidated from upstream:

| path | bytes | SHA256 | mode | Git blob |
|---|---:|---|---|---|
| `spacy/matcher/polyleven.c` | 9571 | `8d6cc95a1e44c334c3a5c1ffe3011f7e8d7a0afea27345d769a7db7d16abce0a` | `100644` | `2f2b8826c50754f496e0ef09c9367173679f41de` |
| `website/.vscode/extensions.json` | 165 | `515b1ef75f9d7e9b2e63f7009ffe9b9cf4a809b27d7a96265f72f48127767fdf` | `100644` | `4b533827a909bc135ca82fcb122587645508b302` |

A future repair MUST abort before mutation unless fresh canonical readback is exactly:
- files `1774`
- bytes `20626274`
- missing set = exactly the two paths above
- changed `0`
- extra `0`
- each missing descriptor still matches N32 bytes/SHA256/mode/source blob.

Synthetic guard results — `5/5 PASS`:
1. exact state => `PRE_REPAIR_READY`
2. unexpected extra => `ABORT_PRE_REPAIR / EXTRA_PATH_DRIFT`
3. changed path => `ABORT_PRE_REPAIR / CHANGED_PATH_DRIFT`
4. third missing path => `ABORT_PRE_REPAIR / MISSING_SET_DRIFT`
5. mode drift `100644→120000` => `ABORT_PRE_REPAIR / IDENTITY_DRIFT`

## STEP 2 — tracked-set-preserving staging strategy

N23 proved imported `.gitignore` matches `.vscode`; canonical-like `git add --sparse -- target` omits `website/.vscode/extensions.json`.

Synthetic Git fixture reproduced that omission, then tested a narrow reviewed allowlist strategy:

1. stage `spacy/matcher/polyleven.c` normally;
2. stage ONLY exact authoritative ignored path `website/.vscode/extensions.json` with path-scoped force-add;
3. never use blanket `git add -f -- <destination>`;
4. require `git diff --cached --name-only` to equal exactly the two-path allowlist;
5. require `git ls-files --stage` mode `100644` for both;
6. recompute bytes/SHA256 and compare with N32/source identities;
7. reject any ignored decoy or third staged path.

Synthetic result: baseline restaging omitted `.vscode/extensions.json`; exact allowlisted staging included both required files and excluded an ignored `.vscode/decoy.tmp`. Staged set equality and modes passed.

This is a staging preflight only. No canonical path was repaired or staged by this node.

## STEP 3 — abort conditions + refutations + repair-ready packet

### Abort conditions
Return `ABORT_PRE_REPAIR` before physical mutation if ANY occurs:
- source commit differs from `26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`;
- canonical pre-diff is not exactly `2 missing / 0 changed / 0 extra`;
- missing set differs from the exact two paths;
- bytes/SHA256/blob/mode differ;
- physical/reviewer gate is not explicitly open;
- staged path set is not exactly two paths;
- broad force-add or unrelated ignored content appears;
- special-file gate detects non-regular representation;
- post-publish full-tree readback differs from target.

### 3 refutations

**REF-1 — blanket `git add -f -- destination` is a safe fix.** REFUTED. It can stage unrelated ignored content. Only the exact reviewed ignored path may use path-scoped force-add, followed by staged-set equality.

**REF-2 — if the two filenames are staged, repair is ready.** REFUTED. Exact bytes, hashes, Git blobs, modes, staged-set equality, full-tree totals/hash and canonical readback are mandatory.

**REF-3 — because upstream blobs still match, current canonical drift may differ from N32.** REFUTED. Any pre-repair drift outside the exact `2/0/0` state invalidates the repair packet and requires a new full-tree forensic diff.

### Director/reviewer repair-ready packet

A future authorized executor may proceed only when ALL gates are explicit:

A. `physical_repair_allowed=true` plus reviewer/director authorization; source pin unchanged.  
B. Fresh pre-mutation canonical state exactly `1774 files / 20626274 bytes / 2 missing / 0 changed / 0 extra`.  
C. Source identities equal the table above.  
D. Write only exact source bytes for the two approved paths.  
E. Stage only the exact two-path allowlist; use force only on `website/.vscode/extensions.json`; no destination-wide force.  
F. Pre-commit cached diff exactly two paths; both mode `100644`; bytes/SHA256/source identities exact.  
G. Post-publish canonical readback must equal `1776 files / 20636010 bytes / tree SHA256 cad7a1cdfae8046e24df6735336a9dace6ceebc917fc18eb9b1d187c4d875c1e`, with changed `0` and extra `0`.  
H. Any mismatch => abort/rollback/no `VERIFIED_CLOSED`; canonical motors and unrelated gates remain untouched.

## Verification

- exact 3 M54 steps: PASS
- source identity revalidation: `2/2 PASS`
- drift guard: `5/5 PASS`
- staging synthetic fixture: PASS
- ignored-decoy exclusion: PASS
- 3 refutations: PASS
- canonical mutation/download: `0/0`

Producer verdict: `PASS_PENDING_REVIEW`.
