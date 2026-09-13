# SW-N39 EVIDENCE — HTML EXTRACTION SCORER REFERENCE VECTORS

- schema: `sharck-input.swarm-node-evidence.v1`
- node_id: `SW-N39`
- parent_node: `M54_POST_M53_EVIDENCE_CONTINUATION`
- agent_name: `SOL-1-GPT`
- mode: `SANDBOX_ONLY`
- claim_commit: `d05c62a70a6e04ec9c9601dfce46f651a1106b2e`
- claim_blob: `1b0a70fbe4298026ce8dbd98a74ce9b2e56f9b3e`
- source_contract: `SW-N33-EVIDENCE.md` blob `d0e468828ac9303a988102352c1bcebe8d8e5d44`
- canonical_mutation: `NO`
- downloads_installs_wiring: `0`

## STEP 1 — DERIVE REFERENCE VECTORS

N33 defines ArticleScore = `.55*body_f1 + .15*title_f1 + .20*metadata_f1 + .05*unicode_integrity + .05*malformed_success` plus fail-closed hard gates.

Independent deterministic metric vectors executed in sandbox:
- `3GRAM_IDENTICAL`: gold=`abcd`, pred=`abcd` -> `body/title_f1=1.0`.
- `3GRAM_HALF`: gold=`abcd`, pred=`abce` -> shared trigram `abc`, precision=recall=0.5 -> `F1=0.5`.
- `3GRAM_DISJOINT`: gold=`abcd`, pred=`wxyz` -> `F1=0.0`.
- `METADATA_3_OF_3`: authors/date/canonical all exact -> micro-F1 `1.0`.
- `METADATA_2_OF_3`: 2 exact fields + 1 mismatch -> TP=2 FP=1 FN=1 -> micro-F1 `0.6666666667`.
- Unicode normalization contract preserved as NFC + deterministic whitespace collapse for similarity, while sentinel preservation remains an exact independent hard gate.

## STEP 2 — DECISION SIMULATIONS

Synthetic baseline used only to test logic:
`body=.88 title=.80 metadata=.70 unicode=1 malformed=1 boilerplate=.05 repeatability=1 exceptions=0` -> baseline ArticleScore=`0.8440000000`.

Article vectors:
1. `ARTICLE_BOUNDARY_PASS`: body=`.875` (=baseline-.005), title=`.912`, metadata=`.73` (=baseline+.03), unicode=`1`, malformed=`1`, boilerplate=`.05` (=baseline), repeatability=`1`, exceptions=`0` -> candidate score `0.8640500000` >= baseline+`.02`; expected `PROMOTION_REVIEW=true`; observed PASS.
2. `ARTICLE_SCORE_FAIL`: same but title=`.911` -> score `0.8639000000` < `.864`; expected `ARTICLE_SCORE_UPLIFT`; observed blocked.
3. `ARTICLE_METADATA_FAIL`: metadata=`.729999` -> expected `METADATA_UPLIFT`; observed blocked.
4. `ARTICLE_BODY_FAIL`: body=`.874999` -> expected `BODY_NONREGRESSION`; observed blocked.
5. `ARTICLE_REPEAT_FAIL`: repeatability=`.8` with otherwise promotion-capable score -> expected `REPEATABILITY`; observed blocked.
6. `ARTICLE_UNICODE_FAIL`: unicode=`0` -> expected `UNICODE` (and score deficit); observed blocked.
7. `ARTICLE_BOILER_FAIL`: leak=`.050001` > baseline -> expected `BOILERPLATE`; observed blocked.
8. `ARTICLE_EXCEPTION_FAIL`: exceptions=`1` -> expected `UNCAUGHT_EXCEPTION`; observed blocked.

Parser vectors:
1. `PARSER_BOUNDARY_PASS`: selector=`.995`, unicode=`1`, malformed=`.95`, repeatability=`1`, exceptions=`0` -> REVIEW PASS.
2. selector=`.994999` -> blocked `SELECTOR`.
3. malformed=`.949999` -> blocked `MALFORMED`.
4. repeatability=`.8` -> blocked `REPEATABILITY`.
5. exceptions=`1` -> blocked `UNCAUGHT_EXCEPTION`.

Mismatch/failure classes for independent scorer validation:
`SCORE_MISMATCH_BODY_3GRAM`, `SCORE_MISMATCH_TITLE_3GRAM`, `SCORE_MISMATCH_METADATA_MICROF1`, `HARD_GATE_REPEATABILITY`, `HARD_GATE_UNICODE`, `HARD_GATE_UNCAUGHT_EXCEPTION`, `HARD_GATE_BOILERPLATE`, `HARD_GATE_BODY_NONREGRESSION`, `HARD_GATE_ARTICLE_SCORE_UPLIFT`, `HARD_GATE_METADATA_UPLIFT`, `PARSER_SELECTOR_THRESHOLD`, `PARSER_MALFORMED_THRESHOLD`, `PORT_BOUNDARY_VIOLATION`.

## STEP 3 — TEST / REFUTE / REPORT

### Three executed simulations
1. Metric reference pack: 5/5 expected metric values PASS.
2. Article promotion matrix: 8/8 expected decisions PASS.
3. Parser gate matrix: 5/5 expected decisions PASS.

### Three refutations
1. `REFUTE_AGGREGATE_SCORE_SUFFICIENT`: false. Repeatability, boilerplate, body regression, Unicode or exception hard gates block promotion even with sufficient aggregate score.
2. `REFUTE_THRESHOLDS_ARE_STRICT_GT`: false. The exact N33 operators are inclusive where written (`>=` / `<=`); boundary vectors `.875`, `.73`, `.995`, `.95`, equal boilerplate and +.02 score all pass when every other gate passes.
3. `REFUTE_PARSER_REVIEW_IMPLIES_ARTICLE_PROMOTION`: false. Parser REVIEW is confined to `extract.html_parser`; article promotion remains independently gated by ArticleScore/body/metadata/boilerplate/repeatability/Unicode/exceptions.

## Verification

- Schema step 1 complete: reference vectors derived for body/title 3-gram F1, metadata micro-F1 and independent hard gates.
- Schema step 2 complete: promotion/nonpromotion/boundary simulations executed deterministically.
- Schema step 3 complete: expected vectors + 3 refutations + mismatch classes published.
- Canonical writes/downloads/installs/wiring: none.
- Gates: unchanged and false; canonical motors immutable.

## Producer verdict

`PASS_PENDING_SUPERVISOR_FANIN` — SW-N39 worker scope complete. This validates scorer decision behavior only; it does not promote, download, install or wire Newspaper4k/selectolax and does not claim project-level VERIFIED_CLOSED.
