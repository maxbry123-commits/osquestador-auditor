# SW-N36 — MODEL SNAPSHOT PROVENANCE MATRIX

- schema: `sharck-input.multisol-dag.v1`
- node_id: `SW-N36`
- parent_node: `M54_POST_M53_EVIDENCE_CONTINUATION`
- agent: `SOL-8-GPT`
- mode: `READ_ONLY_RESEARCH`
- claim_commit: `2f88c4c89fcecb27236cd6f2fff38eb18c35194b`
- claim_blob: `3359bca3b8cbfa5a87986c112751fda1b7e018d0`
- gates: `physical_repair_allowed=false / b05_b06_download_allowed=false / step3_allowed=false / canonical_motors=IMMUTABLE`
- downloads/install/canonical mutation: `0 / 0 / NO`

## Assertion
Eval provenance can fail closed when provider-side immutable model build IDs are unavailable by classifying snapshot guarantees, recording observable fallback provenance, and blocking exact replay unless model identity is STRONG.

## STEP 1 — N31 identity inventory
N31 requires provider, exact model_id, version/snapshot when available, `sampling_config_sha256`, immutable environment/runtime identity, and full replay hashes. Unavailable build/snapshot fields must be explicit, never invented.

Additional N36 fields:
`provider`, requested/returned model id, snapshot/version, endpoint/provider slug, region/variant, fallback policy, API version, source repo, resolved source revision, model/source manifest SHA256, runtime image digest/profile id, provider metadata SHA256, sampling SHA256, timestamp, unknown fields, snapshot class.

Official evidence checked:
- Hugging Face Hub can resolve a revision once to a full commit and pin all downloads to that commit.
- OpenAI official API docs expose dated snapshot identifiers for supported models.
- Groq exposes model IDs and documents deprecation/replacement; automatic upgrades may apply to some models.
- OpenRouter defaults may load-balance/fallback across providers; an exact provider endpoint can be targeted and fallbacks disabled.
- NVIDIA NIM exposes exact profile IDs described as deterministic/version-safe selectors.
- Cerebras exposes public model IDs; dedicated deployment supports explicit model-version paths using integer version IDs or aliases.

Sources:
- https://huggingface.co/docs/huggingface_hub/guides/manage-cache
- https://platform.openai.com/docs/models/default-usage-policies-by-endpoint
- https://console.groq.com/docs/models
- https://console.groq.com/docs/deprecations
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://docs.nvidia.com/nim/large-language-models/latest/profiles.html
- https://inference-docs.cerebras.ai/api-reference/models/public-models
- https://inference-docs.cerebras.ai/api-reference/customer_management_api/deploy-model-to-endpoint

## STEP 2 — classes + fallback contract

### SNAPSHOT_STRONG
Requires immutable model/source identifier, exact artifact/manifest hash, immutable runtime/container identity, fixed endpoint/runtime variant, no silent fallback, sampling hash, and explicit unknowns. Examples: HF full commit + model hashes + pinned runtime; self-hosted NIM with immutable image digest + exact profile ID + source/artifact pin.

### SNAPSHOT_PARTIAL
Versioned identity exists but replay-critical build/weights/runtime remains opaque. Examples: dated OpenAI snapshot; Groq exact model ID; Cerebras public/integer version ID without artifact/build digest; OpenRouter exact model + exact provider variant + fallbacks disabled but opaque provider build; NIM profile ID without complete image/model digests.

### SNAPSHOT_NONE
Mutable alias (`latest`, `main`), unversioned family only, router/provider not fixed, fallbacks may substitute execution, no resolvable snapshot/version/source revision, or conflicting unresolved returned identity.

Matrix:
| surface | class | rule |
|---|---|---|
| HF commit + artifact hashes + runtime digest | STRONG | exact replay possible only if all other N31 fields match |
| HF commit but runtime opaque | PARTIAL | exact replay blocked |
| OpenAI dated snapshot | PARTIAL | provider build digest not client-verifiable |
| floating provider alias | NONE | comparison blocked |
| Groq exact model ID | PARTIAL | opaque provider build |
| Cerebras explicit model/version ID | PARTIAL | needs artifact/build/runtime digests for STRONG |
| OpenRouter exact endpoint + no fallback | PARTIAL | underlying provider build still needed |
| OpenRouter default routing/fallback | NONE | backend is not fixed |
| NIM immutable image + exact profile + source pin | STRONG | N31 full manifest still required |

Fallback metadata for PARTIAL/NONE: provider/API version, requested+returned model IDs, snapshot/version, endpoint slug/region/variant, fallback policy/resolved provider, canonical SHA256 of model metadata, sampling SHA256, timestamp/request id, source repo+commit, materialized manifest SHA256, runtime digest/profile id, and `unknown_fields[]`.

Comparability:
- STRONG + all N31 fields equal => `MODEL_IDENTITY_EXACT_REPLAY_READY`.
- PARTIAL => `MODEL_IDENTITY_OPAQUE_PARTIAL`; exact replay blocked, observational lineage only.
- NONE => `MODEL_IDENTITY_NONCOMPARABLE`; cross-run score comparison blocked.
- Any class change starts a new lineage; same numeric score never upgrades comparability.

## STEP 3 — synthetic tests + refutations
A deterministic fail-closed classifier was run locally with no downloads, installs, model calls, or canonical writes.

9/9 PASS:
1. HF exact source+hash+pinned runtime => STRONG
2. HF `main` only => NONE
3. OpenAI dated snapshot => PARTIAL
4. OpenAI floating alias => NONE
5. OpenRouter exact provider/no fallback/backend opaque => PARTIAL
6. OpenRouter default routing => NONE
7. NIM runtime digest+profile+source pin => STRONG
8. Groq model ID only => PARTIAL
9. Cerebras version ID/runtime opaque => PARTIAL

Refutations:
- REF-1: dated model ID alone proves immutable weights/build — REFUTED; remains PARTIAL without client-verifiable build/artifact identity.
- REF-2: same model family across providers is directly comparable — REFUTED; provider runtime/quantization/tokenizer/hidden revision may differ.
- REF-3: same OpenRouter model slug proves same backend — REFUTED; default routing/fallback can change provider; fixed endpoint/no fallback only reaches PARTIAL unless build is pinned.

Acceptance for STRONG requires: provider explicit; requested+returned IDs recorded; immutable version/source resolved; artifact/manifest hashed; runtime image/build pinned; endpoint variant fixed; fallback disabled/not applicable; sampling+metadata hashed; unknowns explicit; full N31 replay manifest equal.

## Results
- exact M54/N36 requirement: PASS
- atomic claim/readback: PASS
- N31 identity extraction: PASS
- official evidence review: PASS
- STRONG/PARTIAL/NONE contract: PASS
- fallback metadata: PASS
- fail-closed comparability: PASS
- synthetic matrix: PASS 9/9
- 3 refutations: PASS
- downloads/install/canonical mutation: 0/0/NO

Remaining GAP: provider-side opaque weight/build IDs remain opaque by definition; they must not be inferred. PARTIAL/NONE intentionally block exact replay.

Producer verdict: `PASS_PENDING_REVIEW`.
