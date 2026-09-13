# SW-N23 EVIDENCE — spaCy `website/.vscode/extensions.json` MISSING FORENSIC

- schema: `sharck-input.swarm-node-evidence.v1`
- agent: `SOL-8-GPT`
- chat_id: `chat-sol8-20260912T2313-0500`
- node: `SW-N23`
- parent: `M50_ADD_TWO_GAP_DERIVED_SAFE_NODES`
- mode: `READ_ONLY_FORENSIC`
- claim_commit: `5cce3a6b6e11b026c9939d72b807f59d50c7fdd1`
- claim_blob: `f45dd493c66f266ee97663a0a66a63b9ac9c1abc`
- base_sha: `f6a88c7b7844ce1abe0fdb78372f050818b779a1`
- fresh_head_before_evidence_write: `a3babe83e0c42c53f886688d8a23a9dbf71626ba`
- physical_mutation: `false`
- downloads: `0`
- canonical_motor_mutation: `false`

## STEP 1 — SYNC / VERIFY / CLAIM

N23 was added by M50 from a real unresolved GAP: SW-N03 had proven two spaCy missing files but classified their cause as unproven; SW-N13 resolved only `spacy/matcher/polyleven.c`. Atomic N23 claim was created and read back before forensic work.

Authoritative evidence reused:
- `SW-N03-EVIDENCE.md`: spaCy `2/139` exact anomalies remained `CAUSE_UNPROVEN`.
- `SW-N13-EVIDENCE.md`: pinned spaCy source commit `26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`; N13 scope was polyleven only.
- `B04-XRAY-2026-09-11.md`: `website/.vscode/extensions.json` missing, 165 bytes, SHA256 `515b1ef75f9d7e9b2e63f7009ffe9b9cf4a809b27d7a96265f72f48127767fdf`.
- spaCy `DOWNLOAD_EXTRACT_MANIFEST.json`: exact pinned commit above, source tree `1776 files / 20636010 bytes / cad7a1cd...`.

## STEP 2 — EXECUTE / VERIFY

### F1 — The path is physically present and tracked in the immutable upstream source

At `explosion/spaCy@26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`, exact fetch of `website/.vscode/extensions.json` succeeds with Git blob SHA `4b533827a909bc135ca82fcb122587645508b302`.

Exact content readback is 165 bytes. Its SHA256 is:

`515b1ef75f9d7e9b2e63f7009ffe9b9cf4a809b27d7a96265f72f48127767fdf`

This matches the B04 X-Ray expected missing-file hash byte-for-byte. Therefore the anomaly is not source absence and not path drift at the pinned commit.

### F2 — The same immutable source contains an ignore rule that matches the path

The pinned upstream root `.gitignore` contains:

`# Vim / VSCode / editors`
`...`
`.vscode`

A pattern without a slash matches a `.vscode` directory at nested levels, including `website/.vscode/`.

The canonical published spaCy partial still contains the same imported `code/.gitignore` blob `af75a4d47c7abdfc7588f1b4883bcb15debe693f`, proving the ignore file itself was copied into the destination.

### F3 — Canonical publication mechanism re-applies imported ignore semantics

Canonical `hf_download_extract_engine.py` blob `91e6e4486692eab314be5c7130d8310d3c855397` copies the extracted source tree into the destination and then runs:

`git add --sparse -- <destination>`

It does not use `git add -f` and does not stage from an upstream tracked-file manifest. Consequently, copied upstream files matching an imported `.gitignore` can be present in the working tree yet omitted from the published Git commit.

### F4 — Causal microtest

A clean temporary Git repository was created with:
- `target/code/.gitignore` containing `.vscode`;
- `target/code/website/.vscode/extensions.json`;
- one normal file.

Results:
1. `git check-ignore -v target/code/website/.vscode/extensions.json` identified `.gitignore:1:.vscode`.
2. `git add --sparse -- target` staged `.gitignore` and the normal file.
3. `git ls-files --stage` did **not** contain `website/.vscode/extensions.json`.

This independently reproduces the exact staging mechanism without touching Sharck canonical destinations.

### F5 — Canonical destination confirms the consequence

Current canonical destination fetch for:

`.../spaCy/code/website/.vscode/extensions.json`

returns `404 Not Found`, while the imported root `.gitignore` is physically present. The published manifest still identifies the source tree as the complete 1776-file pinned source, while B04 readback found only 1774 files.

## Causal verdict

`website/.vscode/extensions.json` = **`IMPORTED_GITIGNORE_RESTAGING` CONFIRMED**.

Evidence chain:

`pinned source path+hash exists` → `pinned source .gitignore matches .vscode` → `canonical publisher uses non-forced git add --sparse` → `microtest omits matching tracked-intent file` → `canonical destination lacks exact path`.

Rejected causes for this exact path:
- `SOURCE_ABSENT`: refuted by immutable exact fetch.
- `PATH_DRIFT`: refuted by exact pinned path/hash match.
- `GENERATED_ONLY`: refuted because immutable Git blob exists in source.
- `SPECIAL_FILE`: no special-file evidence; exact file fetch is normal JSON content.
- `DOWNLOAD_INCOMPLETE`: source manifest records complete extracted source tree before publication; missing occurs in published readback.

## Repair prerequisites — NOT EXECUTED

Future authorized repair must:
1. use the exact pinned/source-approved commit;
2. stage by exact upstream tracked-set semantics or another reviewed method that preserves tracked files even when imported `.gitignore` would ignore them;
3. preserve bytes and Git modes;
4. verify this exact path SHA256 `515b1ef7...` in staged + published + canonical readback;
5. run full-tree equality, not only a two-file spot fix;
6. keep special-file gates intact and avoid global unsafe ignore bypass;
7. remain blocked until physical-repair/reviewer/director gates explicitly open.

## STEP 3 — TEST / REFUTE / REPORT

### Tests
- T1 atomic claim/readback: PASS.
- T2 immutable exact source path: PASS.
- T3 source content `165 bytes` and SHA256 matches B04 X-Ray: PASS.
- T4 pinned `.gitignore` contains `.vscode`: PASS.
- T5 canonical publisher uses `git add --sparse` without force/tracked-set replay: PASS.
- T6 local causal microtest omits nested `.vscode` file: PASS.
- T7 canonical destination exact path absent: PASS.
- T8 zero canonical mutation/download/shared-control write: PASS.

### 3 simulations
1. **S1 exact pinned replay:** tracked-intent JSON exists + imported `.vscode` + non-forced restage → omitted. PASS.
2. **S2 path-drift hypothesis:** exact pinned path and exact expected SHA both match → path drift rejected. PASS.
3. **S3 forced global ignore bypass proposal:** could stage unwanted files and weaken safety; reject broad bypass and require tracked-set/full-tree contract. PASS.

### 3 refutations
1. **R1 “the file never existed upstream”** — REFUTED by immutable exact fetch and blob SHA.
2. **R2 “the file is generated/editor-local and therefore legitimately absent”** — REFUTED: it is committed in the pinned source and included in the manifest/source-vs-published expected tree.
3. **R3 “fixing this one file would prove spaCy VERIFIED_CLOSED”** — REFUTED: polyleven plus full-tree/hash/readback and independent gates remain required; folder/file presence is not component verification.

## COUNCIL12
1. objective: resolve second spaCy anomaly — PASS.
2. requirement: read-only, no repair — PASS.
3. authority: pinned source + manifest + canonical code/readback — PASS.
4. physical state: spaCy remains FAILED/partial — preserved.
5. owner: SOL-8 atomic N23 — PASS.
6. gates: unchanged false — PASS.
7. collision: unique N23 scope — PASS.
8. causal GAP: imported ignore restaging — CONFIRMED.
9. alternatives: source absence/path drift/generated/special rejected by evidence.
10. StrategyDelta prerequisite: tracked-set-preserving staged publication, not executed.
11. tests/refutations: 8 tests + 3 simulations + 3 refutations — PASS.
12. verdict: `PASS_PENDING_SUPERVISOR_FANIN` for N23 scope.

## GOALS12_OUTPUT
G01-G10: PASS.  
G11: evidence SHA/readback required immediately after this publication.  
G12: release + rescan required after readback.

## Worker verdict before readback

`PASS_PENDING_EVIDENCE_READBACK_THEN_SUPERVISOR_FANIN`

No claim of `VERIFIED_CLOSED` is made. spaCy remains physically unrepaired and gate-blocked.
