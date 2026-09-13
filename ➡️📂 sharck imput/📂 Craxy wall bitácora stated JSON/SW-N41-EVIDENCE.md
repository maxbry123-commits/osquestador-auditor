# SW-N41 EVIDENCE — WARC RECORD TYPE NORMALIZATION POLICY

- schema: `sharck-input.swarm-node-evidence.v1`
- node_id: `SW-N41`
- parent_node: `M54_POST_M53_EVIDENCE_CONTINUATION`
- agent_name: `SOL-6-GPT`
- chat_id: `chat-sol6-20260912T2329-0500`
- mode: `READ_ONLY_DESIGN`
- task: `WARC_RECORD_TYPE_NORMALIZATION_POLICY`
- claim_commit: `18ebab93beccc005a08adfcb84fac57ad31753e3`
- claim_blob: `ed2ae6ede5fa533368014a53a7a8af4517786aac`
- claim_base_sha: `1294a9e1844827550130ed9199f5d37761fb8fff`
- evidence_prewrite_head: `fefbce833ad0968213d83725f6b38b7f06f3a231`
- source_contract: `SW-N34-EVIDENCE.md`
- warcio_source_pin: `2a797aa8c6d67e70966ce9d1a690208ab250fbe7`
- canonical_mutation: `NO`
- downloads: `0`
- installs: `0`
- gates: `physical_repair_allowed=false / b05_b06_download_allowed=false / step3_allowed=false / canonical_motors=IMMUTABLE`

## STEP 1 — RECORD TYPES + STABLE/VOLATILE FIELD AUDIT

N34 already separates raw WARC artifact integrity from a normalized semantic ledger and explicitly leaves `revisit/resource` normalization open. The pinned warcio test corpus confirms concrete examples for `response`, `request`, `revisit`, `resource`, `metadata`, and `warcinfo` records.

Cross-run semantic normalization MUST NOT key on volatile transport identity fields such as:

- `WARC-Record-ID`;
- `WARC-Date`;
- `WARC-Refers-To` UUID;
- `WARC-Refers-To-Date` capture timestamp;
- gzip/compression timestamp or archive byte offsets.

These may be retained as diagnostic/provenance fields, but they are excluded from the semantic-ledger digest.

Supported semantic types for this policy:

1. `response`
2. `resource`
3. `metadata`
4. `revisit`

`request` and `warcinfo` remain in the raw type/count profile but are not required semantic replay targets by N34. `conversion`, `continuation` or any unknown/unhandled record type fail closed into `UNSUPPORTED_RECORD_TYPE` until a dedicated policy exists; they are never silently dropped.

## STEP 2 — NORMALIZATION / DIGEST / REPLAY / DUPLICATE RULES

### response

Canonical semantic row:

`type=response | target_uri | http_status | normalized_content_type | payload_sha256(recomputed) | payload_length`

Declared WARC payload/block digests are retained as diagnostics and must agree when present, but the canonical content identity is recomputed from payload bytes.

Replay requirement: exact target, status and body hash; content type must satisfy the expected normalized value when the fixture declares one.

### resource

Canonical semantic row:

`type=resource | target_uri | normalized_content_type | payload_sha256(recomputed) | payload_length`

Replay/readback requirement: exact target/body hash and content type where replayable. Non-HTTP resources remain archive-readback assertions even when no browser-facing replay endpoint exists.

### metadata

Canonical semantic row:

`type=metadata | target_uri-or-empty | normalized_content_type | semantic_payload_sha256`

For `application/json`, parse and canonicalize JSON using UTF-8, sorted keys, compact separators and unchanged values before hashing. This avoids false drift from key order or insignificant whitespace. Invalid JSON under a JSON content type is `METADATA_NORMALIZATION_FAILURE`. For non-JSON metadata, hash exact payload bytes.

Metadata records are archive-readback semantic assertions, not mandatory HTTP replay targets.

### revisit

A revisit record MUST NOT be treated as an empty response merely because its payload block is empty.

Canonical semantic row:

`type=revisit | target_uri | normalized_profile | refers_to_target_uri | resolved_payload_sha256 | optional_http_status | optional_content_type`

`resolved_payload_sha256` is obtained from the declared payload digest when trustworthy and independently resolved/verified against the referenced capture where available. If no deterministic payload identity can be resolved, fail `REVISIT_UNRESOLVED_PAYLOAD`.

`WARC-Refers-To` record UUID and `WARC-Refers-To-Date` are excluded from the cross-run semantic digest because legitimate recapture creates different record IDs/times. They remain diagnostic linking evidence.

Replay requirement: dereference the revisit to the original semantic payload and require the replayed body hash (and status when present) to equal the resolved revisit identity.

### Ordering and duplicates

The semantic ledger is an **order-independent multiset**, not a `target_uri -> single record` map:

1. canonicalize each semantic row to deterministic JSON;
2. sort rows lexicographically;
3. preserve multiplicity;
4. hash the newline-delimited canonical rows.

Therefore:

- archive record order may change without false semantic drift;
- an extra duplicate record changes multiplicity and therefore changes the digest;
- response + revisit for the same target is legal only when the golden baseline expects that exact multiset and the revisit resolves to the expected payload identity;
- same target with different normalized content is retained as distinct rows and must not overwrite another row;
- missing or unexpected multiplicity fails closed.

Raw WARC SHA256 from N34 remains the within-run artifact-integrity assertion; normalized multiset digest is the cross-run semantic assertion.

## STEP 3 — SYNTHETIC RECORD-LEDGER DRIFT MATRIX

Synthetic ledger contained:

- one `response`;
- one `resource`;
- one JSON `metadata` record;
- one `revisit` linked semantically to the response payload.

Executed matrix — `9/9 PASS`:

1. change only WARC UUIDs/dates/refers-to UUID/date -> semantic digest unchanged: PASS.
2. JSON metadata key order + whitespace only -> canonical semantic digest unchanged: PASS.
3. response payload drift -> detected: PASS.
4. resource payload drift -> detected: PASS.
5. metadata value drift -> detected: PASS.
6. revisit resolved payload digest drift -> detected: PASS.
7. revisit profile drift -> detected: PASS.
8. add duplicate semantic record -> multiplicity drift detected: PASS.
9. revisit with no resolvable payload identity -> fail closed `REVISIT_UNRESOLVED_PAYLOAD`: PASS.

### Three simulations

1. `SIM-VOLATILE-HEADER-CHANGE`: new `WARC-Record-ID/WARC-Date` only => semantic PASS, raw artifact may differ.
2. `SIM-REVISIT-DEDUPE`: zero-byte revisit with correct reference/payload identity => semantic PASS and replay must resolve original body, never empty body.
3. `SIM-DUPLICATE-INJECTION`: add one otherwise-identical resource => multiset count/digest changes => FAIL.

### Three refutations

1. `REFUTE-NONRESPONSE-CAN-BE-DROPPED`: REFUTED — resource/metadata/revisit alter semantic archive meaning and baseline counts.
2. `REFUTE-REVISIT-ZERO-BYTES-MEANS-EMPTY-BODY`: REFUTED — revisit semantic identity is reference/profile/resolved payload, not local block length alone.
3. `REFUTE-RECORD-ID-DATE-BELONG-IN-CROSSRUN-DIGEST`: REFUTED — changing only legitimate UUID/time fields must not produce semantic drift.

## Acceptance contract

A future N34 runtime execution passes extended normalization only when:

- raw WARC write/readback hash matches within the run;
- all records parse without truncation;
- type/count profile is persisted;
- every supported semantic record normalizes without ambiguity;
- unsupported record types fail closed rather than disappear;
- revisit payload identity resolves deterministically;
- expected multiset, multiplicity and semantic digest match;
- response/resource/revisit replay assertions succeed where applicable.

## Three final node-loop refutations

1. Did N41 complete all three schema steps? `YES` — type audit, per-type normalization/digest/replay rules, synthetic drift/refutation matrix.
2. Does any real GAP remain? `YES, outside N41 design scope` — first real Browsertrix/warcio baseline has not run and may reveal additional record types/profile-specific fields.
3. Does evidence support producer-side PASS? `YES` for the normalization policy; `NO` claim of runtime/product VERIFIED_CLOSED.

## Producer verdict

`PASS_PENDING_REVIEW`
