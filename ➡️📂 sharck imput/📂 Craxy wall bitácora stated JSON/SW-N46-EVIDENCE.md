# SW-N46 EVIDENCE — RAPIDFUZZ_FULL_BYTE_REPLAY_EXECUTION

- producer: `SOL-10-GPT`
- chat_id: `chat-sol10-20260913T015630-0500`
- node: `SW-N46`
- mode: `SANDBOX_ONLY`
- worker_verdict: `PASS_PENDING_REVIEW`
- producer_score: `12/12 = 100%`
- supervisor_verdict: **NOT CLAIMED** (`VERIFIED_CLOSED` remains supervisor-only)
- canonical mutation: `NO`
- Git LFS: `FORBIDDEN / NOT USED`

## 1. Authority and ownership

Authority chain used: M56 worker queue + M55 node schema, with M57 explicitly parallel to the worker plane and non-dispatching for N43–N46. Reserved M06/M07/M08 were not touched.

Atomic claim: `CLAIM-SW-N46.json` owned by `SOL-10-GPT`, initial claim commit `d2b230a521e691d10e93883c4ab067617b6e5e36`, then physical `IN_PROGRESS` commit `c151dd613003fffbcb667fc65a7d6220b41b9e38`, current claim blob before release `9244137728e8ddfd21bbe3765ba73709835a5199`.

N35 contract was materialized as the single allowed ephemeral executor:
`.github/workflows/sharck-sw-n46-rapidfuzz-full-byte-replay.yml`.

Gate snapshot remained unchanged throughout:
- `physical_repair_allowed=false`
- `b05_b06_download_allowed=false`
- `step3_allowed=false`
- `canonical_motors=IMMUTABLE`

## 2. Immutable source trace

- repository: `rapidfuzz/RapidFuzz`
- source commit: `db6e504539a9c895180b266a06b36a32cb6029ee`
- expected/root tree: `80b6ab641d0000bd5e6ed1706f6a8ba2c9478e0c`
- final executor commit: `d7c5cb465925a860aa108eba3a81e8ed59840026`
- final executor blob: `541767e07c4a51599d8abad01370355686186f9b`
- permissions observed in job log: `Contents: read`, `Metadata: read`
- runner: Ubuntu 24.04 hosted ephemeral runner
- workspace used for replay: `/tmp/sw-n46-source`, `/tmp/sw-n46-candidate`, `/tmp/sw-n46-output`

Special surfaces checked from the pinned tree:
- roots: `.gitignore`, `.gitattributes`, `.gitmodules`
- gitlink `extern/rapidfuzz-cpp` mode `160000` → `82662f3623b3ca3645e543f677fc32fb8bd1fb95`
- gitlink `extern/taskflow` mode `160000` → `130f7952469c01eef8d7b635710bf9a8043f3172`
- executables mode `100755`: `tools/backtrace`, `tools/generate_cython.sh`, `tools/generate_python.py`, `tools/seg_wrapper.sh`

## 3. Execution history and repair loop

### Baseline positive execution

Run `34744075892`, job `103688606682`, head `c151dd613003fffbcb667fc65a7d6220b41b9e38`:
- run conclusion: `success`
- job conclusion: `success`
- source/candidate counts: `195 / 195`
- `missing=[]`
- `extra=[]`
- `changed=[]`
- `mode_mismatch=[]`
- `special_surface_errors=[]`
- `lfs_used=false`
- `canonical_write=false`

Artifact ID `10313433807`, SHA256 `9475e10d92dc013440353e0563f896389535cd1ea628696d8bd36459f89729f2`.

### Hardening failure and fix

Run `34744243044`, job `103689063149`, head `c66388aaef763e0e719b3fca27c73785b0dc6e16` failed only in negative-control harness NC3 because Git rejects a null gitlink OID (`000...000`) with `cache entry has null sha1`. This was a test-harness defect, not a RapidFuzz parity failure.

Fix: NC3 now mutates `extern/taskflow` to the valid non-null alternate gitlink OID from `extern/rapidfuzz-cpp`, preserving the same intended changed-gitlink test without using an invalid index entry.

### Final execution

Run `34744292778`, job `103689203279`, head `d7c5cb465925a860aa108eba3a81e8ed59840026`:
- run conclusion: `success`
- job conclusion: `success`
- replay step: `success`
- artifact step: `success`
- result schema: `sharck-input.sw-n46-replay-result.v3`
- source/candidate counts: `195 / 195`
- `missing=[]`
- `extra=[]`
- `changed=[]`
- `mode_mismatch=[]`
- `special_surface_errors=[]`
- `negative_controls_pass=true`
- `restore_pass=true`
- `lfs_used=false`
- `canonical_write=false`
- result verdict: `PASS`

## 4. Three deterministic negative controls

1. `NC1_MISSING`: removed `.gitignore` from candidate index. Comparator reported exactly `.gitignore` in `missing`. **PASS**.
2. `NC2_MODE`: changed real executable `tools/backtrace` from `100755` to `100644` in index + filesystem. Comparator reported `tools/backtrace` in `mode_mismatch`. **PASS**.
3. `NC3_GITLINK_EXTRA`: changed real gitlink `extern/taskflow` to the alternate valid gitlink OID and added `rogue.extra`. Comparator reported `extern/taskflow` in `changed` and `rogue.extra` in `extra`. **PASS**.

After restoring all injected faults, final readback again produced:
`missing=[]`, `extra=[]`, `changed=[]`, `mode_mismatch=[]`.

## 5. Artifact + independent readback

Final artifact:
- artifact ID: `10313059544`
- name: `sw-n46-rapidfuzz-full-byte-replay`
- size: `27881` bytes
- GitHub digest: `sha256:fb49de029dae66baabf811764ef44b6d237b051c257b97dd4cbeabd39bca5a04`
- expired: `false` at verification time

The artifact ZIP was downloaded and hashed independently. Local readback SHA256 was exactly:
`fb49de029dae66baabf811764ef44b6d237b051c257b97dd4cbeabd39bca5a04`.

Files read back from the ZIP:
- `source-ledger.json`
- `candidate-ledger.json`
- `negative-controls.json`
- `sw-n46-result.json`

Independent cross-comparison of the two ledgers after extraction:
- paths: `195 / 195`, missing `0`, extra `0`
- mode mismatches: `0`
- Git OID mismatches: `0`
- byte-identity SHA256 mismatches: `0`
- both gitlinks retained exact source OIDs
- all four executable paths retained exact mode `100755`

This readback closes the earlier N26 infrastructure limitation at the **SW-N46 producer-evidence level**. Supervisor fan-in remains separate.

## 6. GOALS12 — input/output verification

| Goal | Input requirement | Output evidence | Result |
|---|---|---|---|
| G01 | legal node/scope | unique SOL-10 claim; own workflow/evidence/claim only | PASS |
| G02 | immutable source | exact RapidFuzz commit pinned | PASS |
| G03 | immutable tree | exact root tree asserted before replay | PASS |
| G04 | complete tracked set | 195 source entries replayed to 195 candidate entries | PASS |
| G05 | byte identity | extracted ledgers show 0 identity mismatches | PASS |
| G06 | mode identity | 0 mode mismatches; executable modes verified | PASS |
| G07 | gitlink identity | both `160000` entries exact on clean replay | PASS |
| G08 | special roots | `.gitignore/.gitattributes/.gitmodules` present | PASS |
| G09 | LFS prohibition | LFS attribute fail-closed check; `lfs_used=false` | PASS |
| G10 | no canonical write | `/tmp` only; read-only token; `canonical_write=false` | PASS |
| G11 | run/log/artifact/readback | run/job success + artifact digest + extracted readback | PASS |
| G12 | refutation sensitivity | 3/3 injected faults detected + full restoration | PASS |

Input goals: `12/12 PASS`. Output goals: `12/12 PASS`.

## 7. Council12 visible verdict

1. Scope Sheriff — PASS
2. Claim/Concurrency Judge — PASS
3. Source Pin Auditor — PASS
4. Tree Guard Auditor — PASS
5. Byte Parity Auditor — PASS
6. Mode Parity Auditor — PASS
7. Gitlink/Special-Surface Auditor — PASS
8. LFS Prohibition Auditor — PASS
9. Canonical-Mutation Auditor — PASS
10. Actions Run/Job Auditor — PASS
11. Artifact/Readback Auditor — PASS
12. Refutation/Residual-Gap Auditor — PASS at producer scope

Council12: `12/12 PASS`.

## 8. Required three refutations

**Refutation 1 — “Git tree metadata alone proves replay.”** Rejected. Final proof includes actual materialization under `/tmp`, actual filesystem/index readback, ledger extraction from the uploaded artifact, and byte-identity comparison.

**Refutation 2 — “A successful clean replay could be a comparator that never detects faults.”** Rejected. NC1, NC2 and NC3 independently detect missing path, executable-mode drift, changed gitlink and rogue extra path.

**Refutation 3 — “A passing artifact/log could hide post-test corruption or incomplete restoration.”** Rejected. Uploaded ZIP digest was rehashed independently and matched GitHub exactly; extracted source/candidate ledgers were cross-compared; final restore parity was all-empty.

All three refutations fail to overturn the producer PASS.

## 9. Producer verdict

`PASS_PENDING_REVIEW`

Producer evidence is 100% for SW-N46 schema/acceptance. No canonical product promotion, repair, B05/B06 download, STEP3 activation, shared-control mutation, LFS operation, Watchdog operation, or supervisor closure was performed.
