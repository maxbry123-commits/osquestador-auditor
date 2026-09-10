# 🦈 READBACK X-RAY — 2026-09-10

Mode: `READ_ONLY / FAIL_CLOSED`  
Owner: `SOL / GAP_WATCHDOG`  
Canonical helper source: `hf_download_extract_engine.py` blob `91e6e4486692eab314be5c7130d8310d3c855397`.

## Purpose
Quantify the 6 initial `DESTINATION_EXISTS` failures and the 5 initial `READBACK_TREE_HASH_GAP` failures without deleting, moving, redownloading, or editing any component or canonical motor.

Workflow: `.github/workflows/sharck-input-v2-readback-recover.yml`  
Workflow commits: `15ad8f0e5d128d3095c6de537ef4537571ff2372`, extended by `33fb8f2d63fe91abd6d6c57d357bb8b8512fb850`.  
Runs: `34535896880` and `34536177351`.

## Result
**0/11 recovered.** All 11 destinations contain manifests/code but the current `code/` tree differs from the manifest expected tree. No item is reclassified as VERIFIED_CLOSED.

| Batch | Component | Initial class | Expected files | Actual files | Expected bytes | Actual bytes | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| B01 | scira | DESTINATION_EXISTS | 451 | 439 | 29089180 | 29066182 | GAPS_PENDING |
| B01 | nutch | DESTINATION_EXISTS | 1126 | 1123 | 6723302 | 6719852 | GAPS_PENDING |
| B01 | yacy_search_server | READBACK_TREE_HASH_GAP | 2283 | 2278 | 68987641 | 68980000 | GAPS_PENDING |
| B01 | heritrix3 | READBACK_TREE_HASH_GAP | 1007 | 950 | 7510189 | 7234963 | GAPS_PENDING |
| B02 | pyserini | DESTINATION_EXISTS | 761 | 758 | 11972540 | 11972259 | GAPS_PENDING |
| B02 | OpenSearch | DESTINATION_EXISTS | 19225 | 19221 | 158910234 | 158906443 | GAPS_PENDING |
| B02 | datasketch | DESTINATION_EXISTS | 129 | 124 | 2886392 | 2714863 | GAPS_PENDING |
| B03 | smolagents | DESTINATION_EXISTS | 185 | 184 | 2694061 | 1999563 | GAPS_PENDING |
| B03 | kythe | READBACK_TREE_HASH_GAP | 2407 | 2393 | 14203196 | 14148654 | GAPS_PENDING |
| B03 | sqry | READBACK_TREE_HASH_GAP | 2817 | 2796 | 125961734 | 124570719 | GAPS_PENDING |
| B03 | continue | READBACK_TREE_HASH_GAP | 3058 | 3053 | 283463694 | 283461802 | GAPS_PENDING |

Each row also failed SHA-256 tree equality; archive fragments were checked before tree comparison by the workflow using the canonical engine `sha256()` helper.

## X-Ray conclusion
Initial causal provenance must be preserved, but the 11 destinations are now independently confirmed as **partial/incomplete remote code trees**, not safe reusable copies. A blind retry would hit `DESTINATION_EXISTS`; treating folder presence as success would be a false PASS.

## Remaining 9 source-side failures
`SOURCE_SPECIAL_FILE_GAP` remains for:
- B01: stormcrawler, tika, docling
- B02: vespa, networkx
- B03: cocoindex, pydantic-ai, litellm, fastmcp

These are source-tree compatibility/safety-gate cases and must not be solved by weakening the canonical engine. Source/ref/subproject/alternative decisions remain review-gated.

## Next StrategyDelta candidates — NOT YET EXECUTED
1. For the 11 partial destinations: preserve them, then review a versioned quarantine/move strategy using canonical Motor4 before any 1×1 reacquisition.
2. For the 9 special-file sources: review pinned SHA/tag, official subproject/release artifact, dependency/reference mode, or OSS alternative.
3. CLAUDE diagnoses mutation-safe recovery and test plan; ASTRA audits architecture/safety; GROK validates source/alternative/license/maintenance.

No physical repair is authorized by this X-Ray alone. Step 3 remains blocked.
