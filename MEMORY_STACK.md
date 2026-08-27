# MEMORY / STORAGE ROOT CONTRACT

Canonical owner: osquestador-auditor
Purpose: memory, persistence, audit state, storage contracts and retrieval interfaces.

## Canonical boundary
- All memory/storage state is owned here.
- Other repositories consume this service through the router contract.
- No credentials are stored in Git.
- No provider-specific token is hard-coded.

## Logical stack
1. Persistent state / metadata
2. Document and artifact storage
3. Vector retrieval
4. Graph retrieval
5. Lexical retrieval (BM25)
6. HNSW/vector index layer
7. Audit/event history

## Integration endpoints
- MEMORY_API_BASE: runtime-configured endpoint
- MEMORY_WRITE_PATH: /v1/memory/write
- MEMORY_READ_PATH: /v1/memory/read
- MEMORY_SEARCH_PATH: /v1/memory/search
- MEMORY_AUDIT_PATH: /v1/audit/events

## External compute boundary
Hugging Face is a compute/execution boundary only. Persistent memory remains canonical here.

## Status
Repository contract installed. Runtime/provider implementation and live HF verification remain separate gates and must not be inferred from this file.
