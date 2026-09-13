# M59 — SHARCK INPUT V3 PARALLEL 11-LANE DESIGN / CANDIDATE

## Verdict
`CANDIDATE_CODE_TESTED / PRODUCTION_NOT_PROMOTED / EXISTING_PHYSICAL_GATES_UNCHANGED`

## User flow normalized
`A INPUT_RAW → B INPUT_LOCK + ambiguity/decomposition → C literal lexical/entity/goal/question spec → D 11 SHARCK lanes start together → E continuous research/context deltas → FINAL SHERIFF/FAN-IN → CONTEXT_PACKAGE → LLM/AGENT`

The duplicated user label “Paso 8” is preserved semantically as two lanes: `error_lens` (8) and `solution_guides` (9). No requested function is dropped.

## Concurrency contract
- One immutable InputSpec per job.
- 11 independent LaneKernel tasks start in the same event-loop fan-out.
- Continuous research is a supporting concurrent task.
- 10–100 search jobs means query/provider fan-out, **not** 100 mandatory external vendors.
- A semaphore imposes backpressure; DedupAsync shares identical in-flight searches.
- API secrets are environment-only.

## Context quality contract
- Evidence pointers before factual context.
- Evidence validator requires >=2 independent sources.
- Community/error search is intentionally adversarial.
- 10 alternative routes are ranked by: zero user friction → minimum time → avoid overengineering → evidence strength.
- Multi-Shark challenges the primary route with newer, older and simpler alternatives.
- LiteralAlignmentJudge runs after fan-in and blocks release if a literal input goal lacks traceable evidence overlap.

## Skills contract
- Read at least 20 metadata records from at least 3 libraries.
- Use progressive disclosure; do not dump 20 full SKILL.md bodies into model context.
- Fully activate at most 3 chosen skills for the job.
- M59 selected acquisition candidates are pinned and license-clean: HF `hf-cli`, Anthropic `mcp-builder`, Microsoft `skill-creator`.
- OpenAI `agents-sdk` was full-read as useful reference but is not acquisition-selected because no root repository LICENSE was observed; fail closed.

## Dataset/adapters/tools contract
- Datasets: Hugging Face + Zenodo + Data.gov, 3 active + 5 standby.
- Adapters/tools: Official MCP Registry + configured catalogs/local registry, 3 active + 5 standby.
- Selected items become acquisition requests only; no download claim until canonical motor readback.

## Runtime outputs
Each job writes memory, profile, evidence ledger, handoff, executable handoff index inputs, context package and lane results. Handoff reuse avoids redundant search unless freshness/version requires a new query.

## Existing gates preserved
M59 candidate creation does **not** change `physical_repair_allowed=false`, `b05_b06_download_allowed=false`, `step3_allowed=false`, and does not mutate canonical motors.

## Test evidence
Local test command:
```bash
python test_sharck_v3_runtime.py
python test_provider_adapters.py
```
Observed: `5 tests PASS` + `3 provider tests PASS`. Live-provider smoke from the current sandbox: `URLError` for all five public providers because DNS/network is unavailable there; this remains an infra GAP.
