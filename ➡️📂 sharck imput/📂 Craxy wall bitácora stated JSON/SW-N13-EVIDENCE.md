# SW-N13 — spaCy special-source provenance audit

- agent: SOL-5-GPT
- mode: READ_ONLY_FORENSIC
- base claim commit: 82b445e725970bfcbca0f9a8f6d11dd99b7b94d5e
- gate snapshot: physical_repair_allowed=false; b05_b06_download_allowed=false; step3_allowed=false
- target: spaCy canonical source `explosion/spaCy@26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`
- anomaly under audit: `spacy/matcher/polyleven.c` previously reported `symlink_dereferenced` in B04.

## STEP 1 — SYNC / VERIFY / CLAIM
Claim `CLAIM-SW-N13.json` was created on fresh main and read back before evidence work. M48 authorizes SW-N13 as READ_ONLY_FORENSIC and forbids product/download/shared-control mutation.

GOALS12_INPUT: literal requirement preserved; fresh HEAD/queue/DAG/claims read; owner free; gates false respected; write scope isolated; prior SW-N03 evidence and B04 anomaly record read.

Classification: SOURCE_PROVENANCE_FAILURE / EVIDENCE_FAILURE candidate.

## STEP 2 — EXECUTE / VERIFY
Fresh immutable upstream inspection found `spacy/matcher/polyleven.c` as a regular Git blob in the spaCy commit tree (mode 100644), not a symlink entry. The file itself embeds provenance to upstream Polyleven source `fujimotos/polyleven@c3f95a080626c5652f0151a2e449963288ccae84` and carries the MIT permission text. Recursive immutable tree scan returned no mode `120000` entry for this path and no `120000` match in the scanned tree response.

Causal conclusion: the historical B04 `symlink_dereferenced` label is not supported by the immutable spaCy source tree for this path. Treat it as provenance/evidence drift until canonical destination bytes can be compared under a future physical gate. This node does NOT assert destination repair or VERIFIED_CLOSED.

No canonical component, downloader, adapter, STATE, PLAN, CHECKPOINT, HANDOFF, Recovery, or DAG was mutated.

## STEP 3 — TEST / REFUTE / REPORT
Tests:
1. immutable commit resolves and tree contains `spacy/matcher/polyleven.c`: PASS.
2. exact file fetch at immutable commit: PASS; regular source content returned.
3. special-file surface check for this path: PASS as regular blob; no symlink mode observed.
4. embedded provenance/license header readback: PASS.

3 simulations:
- S1: if a GitHub ZIP dereferences a symlink, immutable Git tree should still expose mode 120000 at source; it does not for this path.
- S2: if the path were absent at the pinned commit, exact fetch would fail; it succeeds.
- S3: if embedded third-party provenance were missing, source attribution would remain unresolved; the file names the Polyleven source commit and MIT terms.

3 refutations:
- R1: refute 'folder/file presence means component verified': accepted; this report does not promote component state.
- R2: refute 'historical symlink_dereferenced proves current upstream symlink': successful; immutable upstream metadata contradicts that label for this path.
- R3: refute 'upstream regular blob proves destination integrity': successful; destination byte/hash comparison is still required when physical gate permits.

GOALS12_OUTPUT: G01-G10 satisfied for read-only scope; G11 evidence persisted with claim/readback chain; G12 release required next. No production PASS claimed.

Verdict: PASS_PENDING_REVIEW for SW-N13 evidence scope only.
Remaining gap: canonical destination provenance/full-byte comparison remains gated; historical anomaly classification should be reconciled by SOL-0/reviewer, not this worker.
