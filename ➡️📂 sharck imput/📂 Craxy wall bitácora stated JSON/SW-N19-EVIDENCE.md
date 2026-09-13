# SW-N19 — RUNTIME CANDIDATE SPECIAL-SURFACE PREFLIGHT

- schema: `sharck-input.swarm-evidence.v2`
- agent_name: `SOL-4-GPT`
- chat_id: `chat-sol4-20260912T2308-0500`
- node_id: `SW-N19`
- parent_node: `M48_10SOL_SWARM_FANIN_AND_NEXT_WAVE`
- mode: `READ_ONLY_RESEARCH`
- claim_commit: `ffdfe3ef233aaa137327485aa98500511cdf3a8c`
- claim_blob_at_execution: `d12a84784bbe586a2d315bdef7f097e291c2f1dd`
- claim_base_sha: `ac038d8c4d9763ac579c6ba6a9c9001f9169e955`
- latest_control_revalidation: `M50_ACTIVE / SW-N19 still owned by SOL-4-GPT`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- acquisition_performed: `NO`
- canonical/product mutation: `NO`

## Assertion

Take only the `KEEP` / `REFERENCE` set produced by SW-N06 and verify current official upstream topology, license, immutable commit, and special-file/submodule/LFS acquisition risk without downloading or promoting any candidate.

## STEP 1 — TAKE N06 KEEP/REFERENCE SET

Deduplicated set from `SW-N06-EVIDENCE.md`:

1. OpenHands Software Agent SDK — `KEEP`
2. mini-SWE-agent — `KEEP`
3. Continue — `KEEP_EXISTING_117 / NO_NEW_ACQUISITION`
4. OpenClaw — `REFERENCE`
5. Agent Skills — `REFERENCE`
6. OpenAI Agents SDK — `REFERENCE`

Hermes, Cline, goose and OpenCode are `DEFER`; Roo Code is `REJECT`; they are outside this node's literal set and were not promoted into this scan.

## STEP 2 — OFFICIAL UPSTREAM / LICENSE / REF / SPECIAL SURFACE

### Matrix

| Candidate | Decision preserved | Current immutable commit | License readback | Symlink `120000` | Submodule `160000` / `.gitmodules` | LFS / attributes preflight | Acquisition verdict |
|---|---|---|---|---|---|---|---|
| OpenHands Software Agent SDK | KEEP | `c37007429be8b4465a83487dc1fd0914df0ea734` | MIT | none observed in recursive tree scan | none observed | no `.gitattributes` observed in recursive scan | `KEEP_PREFLIGHT_LOW_SPECIAL_RISK` |
| mini-SWE-agent | KEEP | `04d809ceab9df28f9adaed044884180159172930` | MIT (`LICENSE.md`) | none observed | none observed | no `.gitattributes` observed | `KEEP_PREFLIGHT_LOW_SPECIAL_RISK` |
| Continue | KEEP_EXISTING_117 | `5522c6f44ca0ac3528b37244818fbfa39b5af470` | Apache-2.0 | none observed | none observed | no `.gitattributes` observed | `KEEP_EXISTING_NO_DUPLICATE` |
| OpenClaw | REFERENCE | `9ef7fb4ccc8f9f09dd2bd6c5331b7c0918e48da9` | MIT | **present**; current tree includes mode `120000` (for example `apps/macos/Sources/OpenClaw/MenuBar.swift`) | root `.gitmodules` absent at inspected commit | root `.gitattributes` has linguist/merge rules and no `filter=lfs`; code-search `filter=lfs` hit is a test fixture, not repository LFS policy | `REFERENCE_ONLY_SPECIAL_SURFACE` |
| Agent Skills | REFERENCE | `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | Apache-2.0 | **present**; `CLAUDE.md` mode `120000` observed | root `.gitmodules` absent | root `.gitattributes` absent; no positive LFS policy evidence found | `REFERENCE_ONLY_SPECIAL_SURFACE` |
| OpenAI Agents SDK | REFERENCE | `fbd2dbcaaf74a2c447c6d3fa9d5645d83fd7e292` | MIT | none observed | `.gitmodules` absent | `.gitattributes`: `* text=auto eol=lf`; no LFS filter. Ordinary vendoring can still normalize bytes, so reference-only remains safer | `REFERENCE_ONLY_ATTRIBUTES_RISK` |

### License readback

- OpenHands `LICENSE` at `c370074...` begins `MIT License`.
- mini-SWE `LICENSE.md` at `04d809...` begins `MIT License`.
- Continue `LICENSE` at `5522c6...` is Apache License 2.0.
- OpenClaw `LICENSE` at `9ef7fb...` is MIT.
- Agent Skills `LICENSE` at `69ef37...` is Apache License 2.0.
- OpenAI Agents SDK `LICENSE` at `fbd2db...` is MIT.

### Immutable-ref correctness

A hypothesis raised during this node that N06 may have confused commit SHAs with tree SHAs was explicitly tested and **refuted** rather than promoted as a fact.

Examples from current branch payloads:
- OpenHands commit=`c370074...`, tree=`7dccb4c...`; N06 recorded `c370074...` — correct commit.
- mini-SWE commit=`04d809c...`, tree=`05aef37...`; N06 recorded `04d809c...` — correct commit.
- Continue commit=`5522c6f...`, tree=`bbcc260...`; N06 recorded `5522c6f...` — correct commit.
- Agent Skills commit=`69ef37e...`, tree=`65e11c9...`; N06 recorded `69ef37e...` — correct commit.
- OpenAI Agents SDK commit=`fbd2dbc...`, tree=`fac4d298...`; N06 recorded `fbd2dbc...` — correct commit.

OpenClaw is the only material HEAD drift observed after N06 in this KEEP/REFERENCE set:
- N06 observed immutable commit `f369c90e95afb636531157e6fc4e8faa1bdff726`.
- fresh current `main` during SW-N19 = `9ef7fb4ccc8f9f09dd2bd6c5331b7c0918e48da9`.
- direct compare proves current is **5 commits ahead**, with N06 commit as merge base.
- This is ordinary upstream movement, not invalid historical evidence. Any future acquisition preflight must re-pin immediately before approval.

### Special-file implications

1. `OpenClaw` and `Agent Skills` are not safe for blind canonical vendoring under the current strict special-file gate because current official trees contain symlink mode `120000`.
2. This does not turn them into rejected references. Their N06 `REFERENCE` decision is strengthened: consume specification/pattern/API/pointer rather than full vendoring unless a later gate defines an explicit safe subtree/package strategy.
3. OpenAI Agents SDK does not show the same symlink/submodule surface in this scan, but its root `eol=lf` attributes are enough to require byte/readback protection if it were ever promoted from reference to vendoring.
4. `filter=lfs` code search across the six repos produced one OpenClaw test-fixture occurrence that mocks `*.bin filter=lfs`; it is not evidence that the repository itself uses LFS. No actual LFS policy was positively identified in the inspected attribute surfaces.

## STEP 3 — TEST / REFUTE / REPORT

### Specific tests

1. `SET_DEDUP`: exactly six N06 KEEP/REFERENCE candidates scanned; DEFER/REJECT candidates not silently promoted — PASS.
2. `OFFICIAL_UPSTREAM`: six canonical GitHub repositories resolved — PASS.
3. `IMMUTABLE_COMMIT`: current commit SHA recorded separately from Git tree SHA — PASS.
4. `LICENSE_READBACK`: 6/6 direct immutable-ref license evidence resolved — PASS.
5. `SPECIAL_SURFACE`: recursive Git-tree inspection performed for symlink/submodule risk; OpenClaw + Agent Skills positive symlink findings preserved — PASS.
6. `SUBMODULE_PREFLIGHT`: no positive submodule surface found in the inspected set; `.gitmodules` absent where explicitly checked — PASS as preflight, not a lifetime guarantee.
7. `LFS_PREFLIGHT`: no repository LFS policy positively identified; OpenClaw search hit classified as test fixture rather than policy — PASS with fail-closed wording.
8. `UPSTREAM_DRIFT`: OpenClaw N06 pin→current pin compare = 5 commits ahead — PASS.
9. `NO_DOWNLOAD_NO_MUTATION`: no acquisition, canonical component write, motor edit, LFS, force, Step3 or shared control write — PASS.
10. `CONTROL_REVALIDATION`: M50 fresh queue explicitly lists `SW-N19 / SOL-4-GPT`; M50 says live claim file is authoritative — PASS.
11. `CONCURRENT_WRITE_CHECK`: claim-base→pre-report HEAD had 23 concurrent commits; no other writer touched `SW-N19-EVIDENCE.md` or `SOL-SWARM-04-LOG.md`; only our own N19 claim appears in scope — PASS.

### 3 simulations

- `SIM-1 KEEP_LOW_SPECIAL_RISK`: future gated sandbox of OpenHands/mini-SWE must pin the immutable commit, rescan tree modes, verify license, and fail closed if new `120000/160000/LFS` appears. Current preflight supports KEEP, not download.
- `SIM-2 REFERENCE_SYMLINK`: blindly vendor OpenClaw/Agent Skills current tree under the canonical strict special-file policy → expected fail-closed on `120000`; therefore preserve `REFERENCE_ONLY` unless a later approved subtree/package design excludes or explicitly handles the surface.
- `SIM-3 ATTRIBUTES_NORMALIZATION`: promote OpenAI Agents SDK to vendoring using ordinary Git staging under `* text=auto eol=lf` → byte mutation is possible; future gated sandbox must compare source/staged/published bytes and modes or use no-filter plumbing.

### 3 refutations

1. `REFUTE-1 — N06 pins are tree SHAs`: **REFUTED**. Branch payloads distinguish `commit.sha` from `commit.tree.sha`, and N06 stored the commit SHA for the inspected rows.
2. `REFUTE-2 — REFERENCE means special-file scan is unnecessary`: **REFUTED**. Current OpenClaw and Agent Skills contain symlinks; an accidental later promotion to vendoring without rescan would collide with the canonical special-file gate.
3. `REFUTE-3 — filter=lfs search hit proves OpenClaw uses LFS`: **REFUTED**. The observed hit is in a test fixture mocking `.gitattributes`; root `.gitattributes` itself contains no LFS filter.

## Causal classification

- Primary: `SOURCE_PROVENANCE_RISK + RESEARCH_PREFLIGHT_GAP` resolved for this six-candidate scope.
- Confirmed product failure: `NO`.
- Confirmed acquisition failure: `NO` — no acquisition was attempted.
- Confirmed current special surface: `YES` for OpenClaw and Agent Skills symlinks.
- Control drift: `OpenClaw moving HEAD`, normal upstream drift requiring re-pin; N06 historical pin remains valid.

## Acquisition-risk recommendations

- OpenHands SDK → `KEEP_PREFLIGHT`, future sandbox only after gate.
- mini-SWE-agent → `KEEP_PREFLIGHT`, future sandbox only after gate.
- Continue → `KEEP_EXISTING_117`, no duplicate acquisition.
- OpenClaw → `REFERENCE_ONLY`; full-repo vendoring not pre-approved because symlink surface exists.
- Agent Skills → `REFERENCE_ONLY`; spec/pointer use preferred; full-repo vendoring not pre-approved because symlink surface exists.
- OpenAI Agents SDK → `REFERENCE_ONLY`; if ever promoted, enforce byte/mode readback against attributes normalization.

## GOALS12_OUTPUT

- G01 literal requirement preserved: `PASS`
- G02 fresh HEAD/control reads: `PASS`
- G03 latest queue/DAG + source evidence read: `PASS`
- G04 owner lock/readback: `PASS`
- G05 dependencies/gates valid: `PASS`
- G06 worker write scope non-overlapping: `PASS`
- G07 N06 set deduplicated: `PASS`
- G08 minimal read-only evidence delta: `PASS`
- G09 specific source/topology/license/ref tests: `PASS`
- G10 three simulations + three refutations: `PASS`
- G11 evidence SHA/readback: `PENDING_PHYSICAL_WRITE_READBACK`
- G12 release/next-free reconciliation: `PENDING_RELEASE`

## COUNCIL12

1. objective — special-surface preflight before acquisition: PASS.
2. requirement — N06 KEEP/REFERENCE set only: PASS.
3. authority — official immutable Git trees/license files/current branch metadata + Crazy Wall: PASS.
4. physical state — no component or motor touched: PASS.
5. owner — SW-N19 remains physically claimed by SOL-4 under M50 readback: PASS.
6. gates — all physical/download/Step3 gates false: preserved.
7. collision — concurrent writers do not overlap N19 evidence/log: PASS.
8. causal gap — unproven special/LFS/ref topology from N06: materially resolved for current snapshot.
9. alternatives — reference/pointer or later gated subtree/package/sandbox instead of blind vendoring.
10. StrategyDelta — re-pin immediately before any approval; rescan modes/attributes; no canonical motor patch.
11. tests/refutations — 11 checks + 3 simulations + 3 refutations.
12. verdict — `PASS_PENDING_SUPERVISOR_FANIN`; no acquisition or production authorization.

## Remaining limits

- Upstream topology can change after this snapshot; future acquisition requires a fresh immutable pin + repeat scan.
- Absence of observed LFS/submodule in a snapshot is not a permanent project invariant.
- OpenClaw/Agent Skills special-file strategy is not solved for full vendoring; current correct action is to preserve `REFERENCE_ONLY`.
- Independent supervisor fan-in remains required; producer does not self-certify `VERIFIED_CLOSED`.

## Worker verdict

`PASS_PENDING_SUPERVISOR_FANIN`
