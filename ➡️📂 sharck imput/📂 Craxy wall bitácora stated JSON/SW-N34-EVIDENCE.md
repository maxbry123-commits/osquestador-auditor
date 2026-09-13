# SW-N34 — WARC CAPTURE FAILURE / READBACK CONTRACT

- schema: `sharck-input.multisol-dag.v1`
- node_id: `SW-N34`
- parent_node: `M53_ADD_GAP_DERIVED_PREINTEGRATION_NODES`
- agent_name: `SOL-6-GPT`
- chat_id: `chat-sol6-20260912T2329-0500`
- mode: `READ_ONLY_DESIGN`
- claim_commit: `28c8ddaa131bbb3d8de1ac47120f0352c859b192`
- claim_blob: `2df042456ed5787ed44a390ffdc45b11f0da7758`
- evidence_prewrite_head: `28c8ddaa131bbb3d8de1ac47120f0352c859b192`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- browser_run: `NO`
- downloads: `0`
- installs: `0`
- canonical_mutation: `NO`

## Assertion under test

The N21 recommendation `Browsertrix producer + warcio reader` can be converted into a deterministic future capture contract that distinguishes within-run artifact integrity from cross-run semantic capture equality and fails closed on missing/extra/corrupt/unreplayable records.

## STEP 1 — LOCAL DYNAMIC FIXTURE + IMMUTABLE INPUTS

SW-N21 provenance used without downloading:

- Browsertrix `EXISTING_20X #118`, observed pin `6657757ecdd71f283d46d81a34b8fce38a9d708f`, AGPL-3.0, future producer role subject to license acceptance.
- warcio `EXISTING_20X #119`, observed pin `2a797aa8c6d67e70966ce9d1a690208ab250fbe7`, Apache-2.0, future WARC reader/verification role.

No physical vendored Browsertrix/warcio manifest was found by N34; therefore `EXISTING_20X` is treated as catalog/provenance evidence, **not** as `SOURCE_PRESENT`, `WIRED`, `RUNTIME_ACTIVE` or `VERIFIED_CLOSED`.

### Fixture `warc-local-dynamic-v1`

A future test creates only a loopback/local HTTP fixture with no external side effects:

| route | deterministic behavior | expected payload SHA256 |
|---|---|---|
| `/index.html` | HTML loads `/app.js` | `138cb8b76ecccf687a62f3362afee5be9a78e61763ffc7e85da7a964db1e6272` |
| `/app.js` | fetches `/api/item?seed=42` and writes result into DOM | `1baa4a19520e0b4c430fa7ac263a3570cc5d0c00d39402272dc54f3d2f8a2107` |
| `/api/item?seed=42` | returns fixed JSON `{"value":"alpha-42"}` | `8dd135035c12c944494b2478527fa3fdf0af3b07a3813108a74fc54f22152ac8` |
| `/asset.txt` | fixed text asset | `454cdb59f2ea60f8843ce2c24d2741c5b00530f9c0a4ca78ca6a8206aa595a70` |

Pinned crawl inputs:

```json
{
  "fixture_id":"warc-local-dynamic-v1",
  "start_url":"http://fixture.local/index.html",
  "scope":"prefix:http://fixture.local/",
  "max_pages":1,
  "wait_until":"networkidle",
  "seed":42,
  "external_network":"DENY",
  "fixture_manifest_sha256":"e4768a44e5a71c8d86a980549a0899e129fff79f7256eadabbd9989ce29b165f"
}
```

The future capture environment must additionally pin Browsertrix commit/image digest, browser build, warcio commit/package version, OS/runtime and crawler config hash.

## STEP 2 — RECORD COUNT / DIGEST / REPLAY / READBACK ASSERTIONS

### Two different digests are required

1. **Raw WARC artifact SHA256** — integrity of the exact bytes written in one run. Compute immediately after write and recompute after artifact readback/download. A mismatch is corruption.
2. **Normalized semantic-ledger SHA256** — cross-run reproducibility digest built from stable record fields; volatile `WARC-Date`, record IDs, compression timestamps and equivalent transport metadata are excluded.

Do **not** incorrectly demand identical raw WARC bytes across captures when legitimate volatile WARC headers differ. Exact artifact integrity and semantic replay equality are separate assertions.

### Required response ledger

For every expected fixture target, warcio readback must emit a normalized record:

```json
{
  "warc_type":"response",
  "target_uri":"http://fixture.local/...",
  "http_status":200,
  "content_type":"...",
  "payload_sha256":"recomputed from payload bytes",
  "payload_length":0,
  "declared_payload_digest":"parsed WARC-Payload-Digest when present"
}
```

Golden fixture response-set size: `4`.
Golden normalized semantic-ledger digest for the synthetic contract instance: `ef14bcfb8b0ca65c0a214f83deed0efe1af0693daba5b09d5d572c14a601c293`.

The first real Browsertrix baseline must additionally persist **total raw WARC record count by WARC type** (`warcinfo/request/response/resource/revisit/metadata/...`). Future runs using the same exact producer/browser/config may compare this raw count profile; the mandatory semantic contract is the expected target/response ledger above.

### Capture acceptance assertions

- `W01_FIXTURE_MANIFEST_MATCH`
- `W02_PRODUCER_PIN_AND_IMAGE_DIGEST`
- `W03_READER_PIN`
- `W04_RAW_ARTIFACT_WRITE_SHA_READBACK_MATCH`
- `W05_WARC_PARSE_NO_TRUNCATION`
- `W06_EXPECTED_TARGET_SET_EXACT`
- `W07_RESPONSE_COUNT_EXACT`
- `W08_PAYLOAD_DIGEST_RECOMPUTED`
- `W09_HTTP_STATUS_EXPECTED`
- `W10_NORMALIZED_LEDGER_DIGEST_MATCH`
- `W11_REPLAY_TARGET_SET_EXACT`
- `W12_REPLAY_STATUS_AND_BODY_HASH_MATCH`

Any failure => `WARC_CAPTURE_GAP`; never promote a partial capture to PASS.

### Executed synthetic capture matrix — 8/8 PASS

The contract validator was executed in-memory over the deterministic fixture ledger:

| case | expected | observed |
|---|---|---|
| exact capture | PASS | PASS |
| missing response record | FAIL | count + target-set + semantic digest mismatch detected |
| extra response record | FAIL | count + target-set + semantic digest mismatch detected |
| payload bytes corrupt vs declared digest | FAIL | payload digest + semantic digest mismatch detected |
| payload changes and declared digest changes too | FAIL | semantic-ledger digest mismatch detected |
| HTTP status drift | FAIL | semantic-ledger digest mismatch detected |
| raw artifact readback corruption | FAIL | raw readback digest mismatch detected |
| duplicate target replacing another target | FAIL | target-set + semantic digest mismatch detected |

### Executed replay matrix — 5/5 PASS

| replay case | expected | observed |
|---|---|---|
| exact target/status/body set | PASS | PASS |
| missing replay target | FAIL | missing target detected |
| altered replay body | FAIL | payload hash mismatch detected |
| altered replay status | FAIL | status mismatch detected |
| unexpected replay target | FAIL | extra target detected |

## STEP 3 — FAILURE CONTRACT + ACQUISITION PREREQUISITES + REFUTATIONS

### Failure classes

- `CAPTURE_PRODUCER_FAILURE`: crawler/browser exits nonzero, timeout, unresolved local target.
- `WARC_PARSE_FAILURE`: warcio cannot parse complete artifact or truncation detected.
- `ARTIFACT_INTEGRITY_FAILURE`: raw artifact write-time SHA != readback SHA.
- `RECORD_SET_FAILURE`: expected target/response missing, duplicated or extra.
- `PAYLOAD_INTEGRITY_FAILURE`: recomputed payload hash disagrees with declared/readback bytes.
- `SEMANTIC_CAPTURE_DRIFT`: stable normalized ledger digest differs.
- `REPLAY_FAILURE`: replay target/status/body differs from fixture manifest.
- `PROVENANCE_FAILURE`: producer/reader/browser/config/fixture immutable identities incomplete.
- `LICENSE_GATE_FAILURE`: Browsertrix AGPL acceptance/usage authority unresolved.

All are fail-closed. Retrying may produce new evidence but does not erase prior failure evidence.

### Acquisition/runtime prerequisites before any future execution

1. director explicitly enables acquisition gate;
2. Browsertrix AGPL use/distribution boundary accepted for intended deployment;
3. exact official repo + immutable commit + image digest verified;
4. warcio exact source/package pin verified;
5. special-file/submodule/LFS surface scanned before acquisition as required by common acquisition contract;
6. sandbox/browser environment isolated from canonical project paths;
7. local fixture has external network denied;
8. raw + semantic readback artifact paths are non-canonical test evidence locations;
9. no new capture component is added if existing #118/#119 can be reused;
10. only after acquisition verification may an execution node run this contract.

### 3 simulations

1. `SIM-PARTIAL-CAPTURE`: Browsertrix output parses but `/asset.txt` is absent. `W06/W07/W10/W11` fail; verdict GAP.
2. `SIM-ARTIFACT-CORRUPTION`: semantic records were originally valid but stored WARC bytes change after write. `W04` fails independently of semantic equality; verdict GAP.
3. `SIM-REPLAY-DRIFT`: artifact parses and target set exists, but replayed API response status/body differs. `W12` fails; verdict GAP.

### 3 refutations

**REF-1 — “A parseable WARC means capture succeeded.”**
REFUTED. A parseable archive may still omit targets, contain wrong payloads/statuses or fail replay.

**REF-2 — “Matching raw WARC SHA across different runs is the only valid reproducibility check.”**
REFUTED. Volatile WARC metadata can legitimately change raw bytes; within-run raw readback hash proves artifact integrity, while normalized semantic ledger + replay assertions prove content reproducibility.

**REF-3 — “Browsertrix and warcio being EXISTING_20X means they are ready to run now.”**
REFUTED. N21 supplies catalog/provenance pins; current global download/physical/Step3 gates remain false and N34 found no physical vendored runtime manifest proving SOURCE_PRESENT/WIRED/RUNTIME_ACTIVE.

## GOALS12_OUTPUT

- G01 literal N34 requirement preserved: `PASS`
- G02 fresh HEAD read: `PASS`
- G03 M53 + N21 #118/#119 provenance read: `PASS`
- G04 atomic owner/readback: `PASS`
- G05 dependencies/gates valid: `PASS`
- G06 write scope non-overlap: `PASS`
- G07 existing provenance reused/deduped: `PASS`
- G08 minimal permitted delta only: `PASS`
- G09 capture/replay contract tests: `PASS 8/8 + 5/5`
- G10 three simulations + three refutations: `PASS`
- G11 evidence SHA/readback: `PENDING_WRITE_READBACK`
- G12 release/rescan: `PENDING_RELEASE`

## COUNCIL12

1. Objective: make WARC producer→reader→replay evidence deterministic.
2. Requirement: design only; no browser run/download.
3. Authority: N21 #118/#119 pins + M53 N34 contract.
4. Physical state: catalog provenance exists; runtime/source-presence is not assumed.
5. Owner: SOL-6 owns SW-N34 only.
6. Gates: download/physical/Step3 false; motors immutable.
7. Collision risk: unique N34 evidence/claim and own log only.
8. Causal GAP: N21 recommended record count/digest/replay but did not formalize integrity vs semantic readback failure semantics.
9. Alternatives: parse-only PASS rejected; raw-hash-only cross-run equality rejected; new duplicate capture stack rejected.
10. StrategyDelta: immutable local fixture + raw readback hash + normalized semantic ledger + replay hash/status checks.
11. Tests/refutations: 8 capture cases + 5 replay cases + 3 simulations + 3 refutations.
12. Verdict: `PASS_PENDING_REVIEW`; runnable future contract complete without gate bypass.

## Remaining gaps

- Browsertrix/warcio acquisition/runtime verification has not occurred under N34.
- First real baseline must record the raw WARC type/count profile produced by the exact pinned Browsertrix/browser configuration.
- WARC revisit/resource records require the same stable-ledger normalization policy when present; this design centers mandatory expected `response` semantics.
- License approval and execution sandbox remain future gate prerequisites.

## Producer verdict

`PASS_PENDING_REVIEW`
