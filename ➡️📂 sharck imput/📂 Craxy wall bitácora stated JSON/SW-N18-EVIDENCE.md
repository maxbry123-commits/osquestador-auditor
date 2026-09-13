# SW-N18 EVIDENCE — HF HUB SPECIAL PROVENANCE FORENSIC

- schema: `sharck-input.swarm-node-evidence.v1`
- agent_name: `SOL-8-GPT`
- chat_id: `chat-sol8-20260912T2313-0500`
- node_id: `SW-N18`
- parent_node: `M49_N13_FANIN_QUEUE_RECONCILIATION`
- task: `HF_HUB_SPECIAL_PROVENANCE_FORENSIC`
- mode: `READ_ONLY_FORENSIC`
- claim_commit: `ac038d86593163e729ac8457d26ea89cc6b7c40e`
- claim_blob: `50b3853958901283c8916b54998423638173b480`
- claim_base_sha: `2d87a1db1f1b28e838fad4e7590601954602a917`
- fresh_head_before_evidence_write: `b783d128666622a3ca9ba2e8acd4aa5fe5d10d05`
- physical_mutation: `false`
- canonical_motor_mutation: `false`
- download: `false`
- shared_control_write: `false`

## Assertion

`#108 huggingface_hub can be given an explicit provenance/special-file repair preflight using current official upstream evidence without claiming historical false equivalence.`

## STEP 1 — SYNC / VERIFY / CLAIM

Atomic claim was created and read back before material work. M49 remained active, physical repair/download/Step3 gates remained false, canonical motors remained immutable, and SOL-8 write scope was limited to this evidence, its own log and its N18 claim file.

Primary evidence read:

1. `SW-N05-EVIDENCE.md` — #108 remains canonical B04 FAILED / `SOURCE_SYMLINK_GAP_CONFIRMED`; no duplicate HF acquisition is justified.
2. `📂 input sharck code principal/📂 component acquisition/state/B04-state.json` — B04-01 `huggingface_hub` failed 3 attempts with `SOURCE_SPECIAL_FILE_GAP:CLAUDE.md` and has no persisted successful result/source_commit.
3. `📂 input sharck code principal/📂 component acquisition/queues/B04-context-engineering.json` — B04-01 source is official `huggingface/huggingface_hub` with historical requested `source_ref=HEAD`.
4. Canonical `hf_download_extract_engine.py` blob `91e6e4486692eab314be5c7130d8310d3c855397`.

### GOALS12_INPUT

G01 literal requirement preserved: PASS.  
G02 fresh HEAD read: PASS.  
G03 M49/M48 control surfaces and N18 dependencies read: PASS.  
G04 owner lock: PASS via atomic claim + readback.  
G05 dependency/gate valid: PASS, read-only only.  
G06 write scope isolated: PASS.  
G07 existing HF evidence deduplicated: PASS.  
G08 delta minimum: evidence only.  
G09 specific causal tests defined: PASS.  
G10 three simulations + three refutations required: PASS.  
G11 evidence SHA/readback required: pending publication readback.  
G12 release/fan-in required: pending Step 3.

## STEP 2 — EXECUTE / VERIFY

### F1 — Historical B04-01 failure is exact but source commit is not persisted

Canonical B04 state records:

- component: `#108 huggingface_hub`
- official source: `huggingface/huggingface_hub`
- attempts: `3`
- status: `FAILED`
- error: `SOURCE_SPECIAL_FILE_GAP:CLAUDE.md`

The historical queue records requested ref `HEAD`, not an immutable commit.

The canonical engine resolves the checkout commit in `acquire()` using `git rev-parse HEAD`, then `main()` immediately calls `scan_tree(src)`. `scan_tree()` raises on a symlink/non-regular special entry. The manifest containing `source_ref` and `source_commit` is constructed only after `scan_tree()` succeeds. Therefore B04-01 can resolve a commit transiently during execution yet fail before that exact resolved commit is persisted in the canonical result.

**Historical provenance verdict:** `EXACT_SOURCE_COMMIT_UNKNOWN_NOT_RECOVERABLE_FROM_CURRENT_CANONICAL_PERSISTENCE`.

No current upstream ref may be substituted for that missing historical identity.

### F2 — Current official upstream topology independently reproduces the special-file class

Official upstream `huggingface/huggingface_hub` current `main` was read as:

- current commit: `129bbb5cf1a7ca2128636eca1695c9960bddd5ca`
- current root tree: `e8df036ec87e4c2b165cd8d66f66ad357fdcd77c`
- `CLAUDE.md`: Git mode `120000`, blob `47dc3e3d863cfb5727b87d785d09abf9743c0a72`, size `9`
- raw blob content: `AGENTS.md`
- `AGENTS.md`: regular Git blob/mode `100644` in the same current tree

Thus the current upstream `CLAUDE.md` is a symlink whose target text is `AGENTS.md`. This is authoritative Git-tree topology. A high-level contents fetch may dereference the symlink and show the target document body; that does not change its Git mode `120000`.

**Current topology verdict:** `SPECIAL_FILE_CLASS_REPRODUCED_AT_CURRENT_OFFICIAL_HEAD`.

This proves the present class/path, not the historical B04 checkout commit.

### F3 — Deterministic current preflight against the immutable canonical engine

Canonical `scan_tree()` appends any `stat.S_ISLNK()` path to `special` and raises `SOURCE_SPECIAL_FILE_GAP` before manifest generation. Given current official `CLAUDE.md` mode `120000`, an unchanged canonical engine must remain fail-closed on the current tree rather than silently flattening/dereferencing the symlink.

This is a deterministic code+tree preflight, not a production retry and not an authorization to repair.

### F4 — Repair preflight contract / evidence boundary

For a future **authorized** repair/acquisition attempt, the minimum evidence prerequisites are:

1. Resolve requested source ref to an immutable commit and persist `{source_repo, requested_ref, resolved_commit}` **before** special-tree scanning.
2. Inspect special entries without silently dereferencing them; record at minimum `{path, git/lstat mode, object type, blob/object SHA, symlink target when applicable}`.
3. Preserve fail-closed behavior for unknown special types, submodules, unsupported symlinks and LFS pointers.
4. Define the explicit allowed representation/adapter for each special type before canonical publication; absence of an approved representation remains a GAP.
5. Run source-vs-staged-vs-readback comparison including paths, bytes and executable/special modes.
6. Never label a future/current immutable commit as the missing historical B04 source commit.
7. Keep canonical motors unchanged unless a later gate explicitly authorizes a versioned motor change.

This N18 artifact does **not** choose the global special-file repair implementation; it establishes #108-specific provenance facts and repair evidence requirements, avoiding overlap with the broader N14 special-source contract node.

## STEP 3 — TEST / REFUTE / REPORT

### Causal tests

| Test | Expected | Result |
|---|---|---|
| T1 atomic N18 claim readback | owner SOL-8 / N18 | PASS |
| T2 B04 state ↔ queue identity | #108 official repo + requested `HEAD` + special failure | PASS |
| T3 engine causal ordering | resolved commit occurs before scan; persisted manifest occurs after scan | PASS |
| T4 current official immutable pin | commit `129bbb5...` + tree `e8df036...` | PASS |
| T5 current special topology | `CLAUDE.md` mode 120000, blob target `AGENTS.md` | PASS |
| T6 historical-equivalence negative test | current HEAD must NOT become historical source_commit | PASS |
| T7 mutation/gate test | 0 downloads / 0 canonical mutation / gates unchanged | PASS |

### 3 simulations

**SIM-1 — Historical replay from persisted project evidence only.** Input has B04 queue `HEAD` and FAILED state without `source_commit`. Expected behavior is abstention on exact historical SHA. Result: PASS — historical commit remains UNKNOWN.

**SIM-2 — Current official preflight.** Pin current official commit `129bbb5...`; inspect its Git tree. `CLAUDE.md` is mode `120000` -> target `AGENTS.md`. Expected unchanged canonical scanner outcome is fail-closed `SOURCE_SPECIAL_FILE_GAP:CLAUDE.md`. Result: PASS as deterministic preflight.

**SIM-3 — False-equivalence injection.** Proposal: assign current `129bbb5...` as the historical B04 source commit because the queue used `HEAD`. Expected: reject. Result: PASS — moving HEAD cannot retroactively identify the missing historical checkout.

### 3 refutations

**REFUTE-1:** “Historical `source_ref=HEAD` proves historical commit equals current HEAD.”  
REFUTED. `HEAD` is movable and B04-01 did not persist its resolved SHA.

**REFUTE-2:** “A contents API showing the Agent Guide body proves `CLAUDE.md` is a regular file.”  
REFUTED. Git tree mode `120000` plus raw blob `AGENTS.md` is authoritative evidence of a symlink.

**REFUTE-3:** “Current upstream symlink evidence means #108 can now be physically repaired.”  
REFUTED. Current evidence is repair preflight only; `physical_repair_allowed=false`, acquisition/download gates remain false, canonical motors are immutable.

## COUNCIL12

1. Objective — establish #108 provenance boundary and current special topology: PASS.  
2. Requirement — read-only forensic, no historical false equivalence: PASS.  
3. Authority — canonical state/queue/engine + official upstream Git objects: PASS.  
4. Physical state — #108 remains FAILED; no status promotion: PASS.  
5. Owner — N18 atomically owned by SOL-8: PASS.  
6. Gates — physical/download/Step3 remain closed: PASS.  
7. Collision — unique N18 evidence/log/claim scope: PASS.  
8. Causal GAP — manifest persistence occurs after special scan failure: CONFIRMED.  
9. Alternatives — silent dereference rejected; explicit special representation requires later approved design: PASS.  
10. StrategyDelta — provenance-before-scan + special metadata capture proposed as prerequisite only: PASS.  
11. Tests/refutations — 7 tests + 3 simulations + 3 refutations: PASS.  
12. Verdict — worker scope complete, independent supervisor fan-in still required: `PASS_PENDING_SUPERVISOR_FANIN`.

## GOALS12_OUTPUT

- G01 PASS — literal N18 assertion preserved.
- G02 PASS — fresh HEAD read before publication.
- G03 PASS — required control/evidence surfaces read.
- G04 PASS — atomic owner lock/readback.
- G05 PASS — read-only gate valid.
- G06 PASS — non-overlapping write scope.
- G07 PASS — existing #108/N05 evidence reused and deduplicated.
- G08 PASS — evidence-only permitted delta; zero product mutation.
- G09 PASS — causal/current-topology/negative tests completed.
- G10 PASS — 3 simulations + 3 refutations completed.
- G11 PENDING_READBACK — evidence publication SHA/blob/readback follows this write.
- G12 PENDING_RELEASE — claim/log release follows evidence readback.

## Verdict before publication readback

`PASS_PENDING_EVIDENCE_READBACK_THEN_SUPERVISOR_FANIN`

Remaining project-level gaps are intentionally not hidden:

- exact historical B04-01 source commit remains `UNKNOWN_NOT_RECOVERABLE_FROM_CURRENT_CANONICAL_PERSISTENCE`;
- future current pin must be read fresh because upstream `main` can move;
- #108 physical repair remains gate-blocked;
- broader special-file representation/repair contract requires N14/supervisor/reviewer/director fan-in;
- worker cannot self-certify `VERIFIED_CLOSED`.
