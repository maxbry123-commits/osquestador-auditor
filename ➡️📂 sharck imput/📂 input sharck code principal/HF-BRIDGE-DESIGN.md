# Hugging Face Bridge — Sharck Input V2

Scope: INPUT/context only. This is not a general workflow engine.

## Goal
Expose Hugging Face models/datasets/Spaces/skills/papers to Sharck Input as **searchable context sources**, without flooding the LLM context or executing untrusted repository code by default.

## Ports
- `HFHubPort` → `huggingface_hub` / HF API.
- `HFDatasetPort` → `datasets` metadata + streaming/load adapters.
- `HFMCPPort` → official `huggingface/hf-mcp-server` when MCP is available.
- `HFSkillPointerPort` → metadata/pointer for `huggingface/skills`; load SKILL.md only on relevance.

## Mini pipeline
`INPUT_SLOT → HF_QUERY → metadata shortlist → policy/license/card gate → pointer snapshot → optional dataset/sample retrieval → evidence ledger → context compiler`.

## Context rules
1. Always keep repo/model/dataset id + revision + URL + card/license metadata.
2. Prefer metadata first; retrieve full README/card/files only when needed.
3. Dataset access defaults to metadata/streaming/sample; never ingest an entire large dataset into LLM context.
4. `trust_remote_code=false` by default.
5. Secrets/tokens are runtime environment inputs only; never copy them into project files/logs/context packages.
6. No automatic execution of model/dataset repo code.
7. Every result gets `FACT | INFERENCE | UNKNOWN` plus provenance.
8. Cache pointers/hashes, not secrets or opaque generated summaries without source refs.

## Progressive disclosure
- L0: id, type, description, tags, license, revision, URL.
- L1: card/README relevant excerpt.
- L2: selected files/schema/features/sample rows.
- L3: only if explicitly required, heavier download/inference via isolated adapter.

## Failure policy
Unavailable HF connector/tool does not become fake PASS. Record `HF_CONNECTOR_GAP` and fall back only to official GitHub/HF HTTP metadata that is available through an authorized tool.

## Current evidence
Official active repositories verified for acquisition candidate B04:
- https://github.com/huggingface/huggingface_hub — Apache-2.0.
- https://github.com/huggingface/datasets — Apache-2.0.
- https://github.com/huggingface/hf-mcp-server — MIT.

The Hugging Face dataset search connector in the current chat returned disabled-by-server-configuration; therefore no dataset-specific installation was claimed in this checkpoint.

## Integration gate
Design may be documented now. Physical wiring into Step 3 remains blocked by the existing M06/M07/M08 review gate and director approval.
