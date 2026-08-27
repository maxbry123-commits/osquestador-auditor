# OPEN-SOURCE RESEARCH — 2026-08-27

Destination: osquestador-auditor
No Git LFS.

## Memory/storage components

1. hnswlib
Official repository: https://github.com/nmslib/hnswlib
Role: HNSW approximate-nearest-neighbor index.
License shown by upstream repository: Apache-2.0.
Action possible here: acquire source through normal Git; pin exact release/commit; hash; read-back; verify.
Current project status: required by architecture; source acquisition not yet performed.

2. rank_bm25
Official repository: https://github.com/dorianbrown/rank_bm25
Role: BM25/BM25L/BM25+/BM25-Adpt/BM25T lexical retrieval algorithms.
Action possible here: acquire source through normal Git; pin exact release/commit; hash; read-back; verify.
Current project status: required by architecture; source acquisition not yet performed.

3. Vector/graph persistence layer
Provider must be selected before installation. Do not install an arbitrary vector/graph database merely to fill the gap.

## Agent repositories researched separately
- Hermes: https://github.com/NousResearch/hermes-agent — MIT; source is already captured in agentes according to the project manifest.
- OpenHands: https://github.com/All-Hands-AI/OpenHands — core/openhands and agent-server are MIT; not yet captured here.
- OpenCode: https://github.com/anomalyco/opencode — MIT; not yet captured here.
- mini-SWE-agent: https://github.com/SWE-agent/mini-swe-agent — MIT; not yet captured here.
- OpenClaw: https://github.com/openclaw/openclaw — separate project; project policy says not to modify its canonical source.
- Claude Code: https://github.com/anthropics/claude-code — source repository exists, but it must not be classified as an ordinary open-source dependency without checking its current license/terms.
- Mimo Code: no authoritative upstream repository was identified from the current evidence; do not fabricate one.
- SmolAgents: no authoritative upstream repository was confirmed in this pass.

## Acquisition rule
URL/reference discovery is not installation. Installation requires exact ref + acquisition + hash + destination + read-back + verification.
If normal Git cannot carry the artifact without Git LFS, stop and request the original archive from the user; do not reconstruct it.
