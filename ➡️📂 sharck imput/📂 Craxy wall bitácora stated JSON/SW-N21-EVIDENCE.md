# SW-N21 — WEB_CAPTURE_EXTRACTION_I09_PREFLIGHT

- schema: `sharck-input.swarm-node-evidence.v2`
- agent: `SOL-5-GPT`
- node: `SW-N21`
- claim_commit: `e39a3933b03c4944382e7deb925c043f6d17c85a`
- claim_blob: `597d78230453fa416d8ae73ed020719c949c6bf7`
- mode: `READ_ONLY_RESEARCH`
- gates: `physical_repair=false / download=false / step3=false / motors=IMMUTABLE`
- downloads_or_wiring: `0`

## STEP 1 — SYNC_VERIFY_CLAIM
Read M49 STATE/CHECKPOINT/PLAN/Handoff, M48 queue/DAG, claims and M40 I09. N14-N20 were occupied; N21 was first FREE and was atomically claimed/read back.

## STEP 2 — EXECUTE_VERIFY

| candidate | pin | license | current status | decision |
|---|---|---|---|---|
| Browsertrix | `6657757ecdd71f283d46d81a34b8fce38a9d708f` | AGPL-3.0 | active; EXISTING_20X #118 | KEEP_EXISTING; license+sandbox gate |
| warcio | `2a797aa8c6d67e70966ce9d1a690208ab250fbe7` | Apache-2.0 | active; EXISTING_20X #119 | KEEP_EXISTING; WARC codec complement |
| ArchiveBox | `da9b867dafc7777d114b93f6f951074a1a05497a` | MIT | active; default `dev`; EXISTING_20X #120 | DEFER; broad overlap, pin exact release later |
| Newspaper4k | `b53a81fc01ff54601faaeae68d6b4a6d2f18efcb` | MIT | active | DEFER; compare against existing article extractor first |
| selectolax | `54c4818d34a9e899aef64cd48bab325fac6c1b90` | MIT | active | KEEP_FOR_REVIEW; narrow HTML parser, benchmark first |
| Browserless | `41948d67785a62e74b454f46916bd65c79cf63c7` | SSPL-1.0 OR commercial license | active | DEFER_LICENSE_AND_OVERLAP |
| Goose3 | `87b6003d740e1be591ede6a2c328e02ed7c1d84c` | Apache-2.0 | active | DEFER_DUPLICATE_EXTRACTOR |
| curl_cffi | `571560b562fe2d379a5fd9bcb3cdf032383d1e3f` | MIT | active | REFERENCE/DEFER_POLICY_GATE |

### Port/test recommendation
- `capture.warc`: Browsertrix producer + warcio reader; test fixed local dynamic fixture, record count, digest and replay/readback.
- `capture.snapshot`: ArchiveBox optional only if a durable multi-format snapshot GAP remains; hash each expected artifact.
- `extract.article`: Newspaper4k/Goose3 only after fixed multilingual corpus comparison against existing extraction baseline.
- `extract.html_parser`: selectolax candidate for deterministic DOM/CSS parsing; test malformed HTML, Unicode, selector parity and repeatability.
- `capture.browser_service`: Browserless remains default-deny until license/use authority is explicit.
- policy-sensitive HTTP transports remain non-default and require explicit policy approval.

### Acquisition order if a future gate opens
1. Reuse warcio #119; no duplicate.
2. Reuse Browsertrix #118 subject to AGPL acceptance.
3. Benchmark selectolax for narrow parser value.
4. Benchmark Newspaper4k only for net-new article metadata quality.
5. ArchiveBox only for a proven snapshot GAP.
6. Defer Browserless, Goose3 and policy-sensitive HTTP transport unless their exact GAP survives review.

## STEP 3 — TEST_REFUTE_REPORT_RELEASE
Tests: upstream `8/8 PASS`; license `8/8 PASS`; immutable pin `8/8 PASS`; archived check `8/8 PASS`; existing-20X dedup `3/3 PASS`; no download/wiring `PASS`; physical gates unchanged `PASS`.

### Simulations
1. Local dynamic site -> Browsertrix -> warcio readback. Partial capture/digest failure => GAP, never PASS.
2. Fixed multilingual article corpus -> existing baseline vs Newspaper4k/selectolax. Candidate promotion requires measured net-new value.
3. Browserless requested without resolved license authority -> DEFER/default-deny, no silent promotion.

### Refutations
1. Public GitHub source does not imply unrestricted Browserless commercial use: canonical LICENSE has SSPL/commercial terms. REFUTED.
2. More ArchiveBox output formats do not automatically justify acquisition because capability overlap and runtime surface increase. REFUTED.
3. Active permissive OSS status alone does not justify adding Newspaper4k/selectolax/Goose3; capability and benchmark evidence are still required. REFUTED.

## Verdict
`PASS_PENDING_SUPERVISOR_FANIN`

Scope complete; zero downloads, installs, canonical mutations, shared-control writes or self-promotion to VERIFIED_CLOSED.
