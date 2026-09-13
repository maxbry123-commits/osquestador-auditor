# SW-N33 EVIDENCE — HTML/ARTICLE EXTRACTION BENCHMARK CONTRACT

- schema: `sharck-input.swarm-node-evidence.v1`
- node_id: `SW-N33`
- parent_node: `M53_ADD_GAP_DERIVED_PREINTEGRATION_NODES`
- agent_name: `SOL-10-GPT`
- chat_id: `sol10-0284245c-e710-416b-9488-4d2cd6fd7a50`
- mode: `READ_ONLY_DESIGN`
- claim_commit: `bd96de3ea98a7d401310fad8446f60467536e74c`
- claim_blob: `d896f9205204b1e5af319d12b799861fc7f4f0bf`
- canonical_mutation: `NO`
- downloads_installs_wiring: `0`

## Assertion

N21 defers Newspaper4k and selectolax until a fixed multilingual/malformed-HTML benchmark proves net-new value against existing extraction capability. N07 confirms acquisition-verified Trafilatura is the existing `extract` baseline (`T-EXT-01`).

## STEP 1 — SYNC / VERIFY / CLAIM

Fresh M53 was read. N31 and N32 were already claimed; N33 had no physical claim and was atomically claimed/read back by SOL-10. Gates remain `physical_repair=false / b05_b06_download=false / step3=false / motors=IMMUTABLE`.

### GOALS12_INPUT
G01 literal requirement PASS; G02 HEAD fresh PASS; G03 M53/N21/N07 read PASS; G04 owner lock PASS; G05 gates PASS; G06 isolated write scope PASS; G07 baseline/candidates deduped PASS; G08 evidence-only delta PASS; G09 deterministic scorer required PASS; G10 3 simulations+3 refutations required PASS; G11 readback POST_WRITE; G12 release POST_WRITE.

## STEP 2 — EXECUTE / VERIFY

### Fixed corpus contract

Future benchmark MUST materialize exactly 24 immutable local HTML fixtures: four language/script lanes × six failure classes.

Languages/scripts: `en`, `es`, `ar` (RTL), `zh-Hans`.

Classes per language:
1. `clean-semantic`: article/title/byline/date/canonical metadata.
2. `boilerplate`: nav/ads/footer/comments/related-story sentinels around article.
3. `malformed`: unclosed/misnested tags, entities, duplicated attributes.
4. `multi-article`: main story + related/article-like competing blocks.
5. `unicode`: combining marks, RTL, CJK, emoji/non-BMP and HTML entities.
6. `metadata-conflict`: HTML title vs OpenGraph vs JSON-LD author/date/title conflicts with explicit gold precedence.

Each fixture manifest MUST contain: `fixture_id, language, class, html_sha256, gold_sha256, gold_title, gold_body, gold_authors[], gold_published_at, gold_canonical_url, selector_assertions[], forbidden_sentinels[]`. Any corpus/hash drift invalidates comparison.

### Execution pin envelope

Every run MUST persist exact: `baseline_component, baseline_source_commit, candidate_name, candidate_source_commit, adapter_commit, scorer_commit, corpus_manifest_sha256, runtime, OS/container digest, locale, timezone=UTC, seed, run_count=5`. Missing pin => `EVAL_INVALID`, never PASS.

Baseline: acquisition-verified **Trafilatura** at the exact canonical manifest source commit read at execution time. Do not substitute modern HEAD for a missing canonical pin.

Candidate pins preserved from N21:
- Newspaper4k: `b53a81fc01ff54601faaeae68d6b4a6d2f18efcb` (DEFER pending benchmark).
- selectolax: `54c4818d34a9e899aef64cd48bab325fac6c1b90` (KEEP_FOR_REVIEW pending benchmark).

### Canonical output envelope

Every adapter returns canonical JSON: `title, body, authors[], published_at, canonical_url, selector_results{}, typed_errors[]`. Normalize text with Unicode NFC + deterministic whitespace collapse for similarity, while separately checking exact Unicode sentinel preservation.

### Metrics

Article lane:
- `body_f1`: deterministic character-3-gram F1 against gold.
- `title_f1`: same normalization/scorer.
- `metadata_f1`: exact field micro-F1 over author/date/canonical URL.
- `unicode_integrity`: exact gold Unicode sentinels preserved.
- `malformed_success`: malformed fixtures yielding typed result without uncaught exception.
- `boilerplate_leak`: forbidden sentinel hit rate.
- `repeatability`: canonical output SHA256 identical across 5 runs.

`ArticleScore = .55*body_f1 + .15*title_f1 + .20*metadata_f1 + .05*unicode_integrity + .05*malformed_success`.

Parser lane (selectolax):
- `selector_accuracy`: exact selector text/attribute assertions.
- `unicode_integrity`, `malformed_success`, `repeatability`, `uncaught_exceptions`.

### Promotion / overlap gates

Newspaper4k may enter `extract.article` REVIEW only when all hard gates pass: `repeatability=1.0`, `unicode_integrity=1.0`, `uncaught_exceptions=0`, `boilerplate_leak <= baseline`, `body_f1 >= baseline_body_f1-0.005`; AND `ArticleScore >= baseline+0.02`; AND `metadata_f1 >= baseline_metadata_f1+0.03`. Otherwise `DEFER/REJECT_OVERLAP` and keep Trafilatura baseline.

selectolax may enter `extract.html_parser` REVIEW only when `selector_accuracy>=0.995`, `unicode_integrity=1.0`, `malformed_success>=0.95`, `repeatability=1.0`, `uncaught_exceptions=0`. Parser success does **not** authorize replacing Trafilatura at `extract.article`; article promotion requires the full article contract independently.

No candidate is promoted merely for speed, popularity, permissive license, or one aggregate score.

## STEP 3 — TEST / REFUTE / REPORT

### Executed deterministic scoring simulations

Synthetic numbers test the decision logic only; they are not candidate benchmark claims.

1. `SIM-NEWSPAPER-NET-NEW`: baseline ArticleScore `0.8875`; candidate `0.9228`, body non-regression + metadata uplift + hard gates => `PROMOTION_REVIEW=true`.
2. `SIM-METADATA-HIDES-BODY-REGRESSION`: metadata `0.95` but body `0.92→0.88`; weighted candidate score remains high (`0.9185`) yet hard body gate => `REJECT`. This proves aggregate score cannot hide extraction regression.
3. `SIM-SELECTOLAX-PORT-BOUNDARY`: selector `0.998`, Unicode `1.0`, malformed `0.97`, repeatability `1.0` => parser REVIEW; identical perfect parser with repeatability `0.8` => REJECT. Neither result implies article-port promotion.

### Three refutations

1. `REFUTE-HIGH-SCORE-ENOUGH`: REFUTED by SIM2; hard body/unicode/repeatability gates override aggregate score.
2. `REFUTE-PARSER-EQUALS-ARTICLE`: REFUTED; selectolax can satisfy parser capability while lacking article title/body/metadata contract.
3. `REFUTE-ONE-RUN-ENOUGH`: REFUTED; five identical canonical output digests are mandatory; nondeterministic output is fail-closed.

### GOALS12_OUTPUT
G01 PASS; G02 PASS; G03 PASS; G04 PASS; G05 PASS; G06 PASS; G07 PASS; G08 PASS evidence-only; G09 scorer/threshold simulation PASS; G10 3/3 simulations + 3/3 refutations PASS; G11 pending physical readback; G12 release/fan-in pending.

## COUNCIL12
1 objective benchmark before candidate promotion; 2 literal requirement preserved; 3 authority M53+N21+N07; 4 no product mutation; 5 SOL-10 owns N33; 6 physical gates false; 7 unique scope; 8 causal gap was missing benchmark contract; 9 alternatives popularity/speed-only rejected; 10 StrategyDelta fixed corpus+pins+hard gates; 11 simulations/refutations pass; 12 verdict `PASS_PENDING_REVIEW`.

## Producer verdict

`PASS_PENDING_REVIEW` — node design contract is complete and runnable later without installing Newspaper4k/selectolax now. No candidate has been promoted, downloaded, wired, or declared VERIFIED_CLOSED.
