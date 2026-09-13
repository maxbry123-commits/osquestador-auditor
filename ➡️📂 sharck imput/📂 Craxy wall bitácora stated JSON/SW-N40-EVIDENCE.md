# SW-N40 EVIDENCE — BROWSERTRIX / WARCIO RUNTIME + LICENSE PREFLIGHT

- schema: `sharck-input.swarm-node-evidence.v2`
- agent_name: `SOL-7-GPT`
- chat_id: `sol7-5f38c044-03f6-4c32-a681-663c0e16b94f`
- node_id: `SW-N40`
- parent_node: `M54_POST_M53_EVIDENCE_CONTINUATION`
- task: `BROWSERTRIX_WARCIO_RUNTIME_LICENSE_PREFLIGHT`
- mode: `READ_ONLY_RESEARCH`
- claim_commit: `f9f7da54a6f2ce20318480fa00ca020e421804c0`
- downloads: `0`
- installations: `0`
- canonical_mutations: `0`
- gates: `physical_repair_allowed=false; b05_b06_download_allowed=false; step3_allowed=false; canonical_motors=IMMUTABLE`

## STEP 1 — official sources / pins / maintenance / licenses

### Browsertrix Crawler
- official repo: `webrecorder/browsertrix-crawler`
- observed source pin: `6657757ecdd71f283d46d81a34b8fce38a9d708f`
- observed source date: 2026-09-11
- repo state: public, not archived
- package version at pin: `1.15.0-beta.0`
- repo/package license: `AGPL-3.0-or-later`
- role: containerized high-fidelity browser capture producer

### warcio
- official repo: `webrecorder/warcio`
- observed source pin: `2a797aa8c6d67e70966ce9d1a690208ab250fbe7`
- observed source date: 2026-04-06
- repo state: public, not archived
- Python package version at pin: `1.8.1`
- license: `Apache-2.0`
- role: WARC/ARC streaming reader/writer and readback/normalization library

Mirrors/forks are not accepted as provenance substitutes for these official sources.

## STEP 2 — acquisition/runtime pin envelope

### Browsertrix future acquisition prerequisites

Source pin alone is insufficient for a reproducible runtime. Any future authorized acquisition MUST persist:

1. official source repo + exact commit;
2. image registry/repository identity;
3. immutable OCI image digest (`sha256:...`), not only `latest` or a mutable tag;
4. declared Browsertrix package/version label;
5. browser base image digest;
6. effective `BROWSER_VERSION` and resolved browser binary version;
7. target platform/architecture;
8. exact crawl config/tool manifest hash;
9. exact output WARC/WACZ artifact hashes and readback result;
10. LICENSE/source-offer/compliance metadata required by the selected deployment/distribution model.

Observed Browsertrix source at the pinned commit uses:
- `BROWSER_VERSION=1.93.138`;
- base image reference `webrecorder/browsertrix-browser-base:brave-${BROWSER_VERSION}` (tag, not digest);
- documentation/compose examples using `webrecorder/browsertrix-crawler` and `:latest`;
- a build-time fetch from `StevenBlack/hosts/master/hosts`;
- replaywebpage assets pinned to version `2.4.7` but fetched remotely during image build.

Therefore a rebuild from source is NOT bit-reproducible unless every remote build input is frozen or content-hashed. Preferred future path: acquire an approved upstream image by immutable digest and record its source relation/SBOM if available; otherwise freeze all build inputs and verify final image digest.

### warcio future acquisition prerequisites

Any future authorized warcio acquisition MUST persist:

1. official repo + exact commit;
2. package version;
3. exact wheel/sdist SHA256 when installing a package artifact, or source-tree digest if built from source;
4. Python version/platform;
5. resolved dependency lock/hash set;
6. LICENSE + NOTICE retention metadata;
7. fixed WARC fixture and expected record/readback digest contract;
8. installed artifact/version readback before use as system evidence.

A semantic version alone is not sufficient when exact replay is required.

### License boundary

- Browsertrix Crawler is AGPL-3.0-or-later. Future use must preserve the license and satisfy applicable source-availability obligations for the actual modified/network/deployment model. This preflight does not make a legal determination; any production distribution or modified network service requires project compliance review before acquisition/wiring.
- warcio is Apache-2.0. Future redistribution must preserve applicable license/notice requirements.
- warcio's Apache license does not neutralize or replace Browsertrix's AGPL obligations; each component keeps its own license boundary.

## STEP 3 — KEEP / DEFER / BLOCK + tests/refutations

### Decision matrix

| component | verdict | reason |
|---|---|---|
| Browsertrix Crawler | `KEEP_CONDITIONAL` | technically aligned with WARC producer role; active upstream; must pin image digest/browser/build inputs and clear AGPL deployment compliance |
| warcio | `KEEP` | aligned with deterministic WARC reader/readback role; Apache-2.0; package/source pin and artifact hash still mandatory |
| Browsertrix `latest` / mutable image tag | `BLOCK` | not immutable provenance |
| Browsertrix source rebuild with unpinned remote build inputs | `BLOCK` | build result may drift despite fixed Git commit |
| warcio version-only install without wheel/sdist hash | `DEFER/BLOCK_FOR_REPLAY` | version name alone is insufficient for exact artifact identity |

### Acceptance checks

- `P01_OFFICIAL_SOURCE_IDENTITY` -> PASS
- `P02_IMMUTABLE_SOURCE_PIN` -> PASS
- `P03_LICENSE_IDENTIFIED` -> PASS
- `P04_MAINTENANCE_NOT_ARCHIVED` -> PASS
- `P05_IMAGE_DIGEST_REQUIRED` -> PASS contract
- `P06_BROWSER_RUNTIME_PIN_REQUIRED` -> PASS contract
- `P07_REMOTE_BUILD_INPUTS_MUST_BE_FROZEN` -> PASS contract
- `P08_PACKAGE_ARTIFACT_HASH_REQUIRED` -> PASS contract
- `P09_LICENSE_BOUNDARIES_NOT_COLLAPSED` -> PASS contract
- `P10_NO_ACQUISITION_AUTHORIZATION_IMPLIED` -> PASS
- `P11_NO_CANONICAL_MUTATION` -> PASS
- `P12_WARC_READBACK_REQUIRED_BEFORE_EVIDENCE_USE` -> PASS contract

Any failed required check => `WARC_RUNTIME_PREFLIGHT_BLOCKED`.

### Synthetic preflight cases

1. Browsertrix source pin + image `latest`, no digest -> `BLOCK` -> PASS.
2. Browsertrix immutable image digest + exact browser/runtime/config ids + compliance review -> `KEEP_CONDITIONAL / ACQUISITION_GATE_STILL_REQUIRED` -> PASS.
3. Source rebuild uses pinned Git commit but mutable `hosts/master` -> `BLOCK_REPRODUCIBILITY` -> PASS.
4. warcio `1.8.1` + official commit + exact package artifact hash + Python lock -> `KEEP` -> PASS.
5. warcio `1.8.1` without artifact hash/lock -> `DEFER_FOR_REPLAY` -> PASS.
6. Either component requested while project download gate=false -> `NO_ACQUISITION` -> PASS.

Synthetic cases: `6/6 PASS`.

### Three refutations

**REF-1 — “A pinned Browsertrix Git commit guarantees the container runtime is identical.”**
REFUTED. Image/base-image identity and remote build inputs can drift independently of source commit.

**REF-2 — “Using a versioned Docker tag is equivalent to an immutable image digest.”**
REFUTED. Tags can be repointed; exact runtime evidence requires content digest/readback.

**REF-3 — “Because warcio is Apache-2.0, the combined Browsertrix+warcio evaluation path has no AGPL boundary.”**
REFUTED. Each component retains its own license terms; Browsertrix remains AGPL-3.0-or-later.

Additional refutation: **“Active upstream + known license means acquisition is already approved.”** REFUTED. M54 gates remain closed and research does not authorize download/wiring.

## Worker verdict

`PASS_PENDING_FINAL_READBACK_THEN_SUPERVISOR_FANIN`

- schema steps: `3/3 PASS`
- components: `2/2 official sources verified`
- source pins: `2/2 exact`
- acceptance checks: `12/12 contract-defined`
- synthetic cases: `6/6 PASS`
- required refutations: `3/3 PASS` (+1 additional)
- downloads/installations/canonical mutations: `0/0/0`
- acquisition authorization: `NONE`
