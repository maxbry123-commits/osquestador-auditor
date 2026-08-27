# ROUTER / HF / MEMORY WIRING

Canonical memory/storage owner: osquestador-auditor.

Inbound:
frontend / agentes / Orquestador-Maxbry- -> universal router -> memory/storage

Compute boundary:
osquestador-auditor -> universal router -> Hugging Face

Persistent state remains in this repository. Hugging Face is compute only.

Runtime references:
- ROUTER_BASE_URL
- HF_EXECUTION_BASE_URL
- MEMORY_AUTH_REF
- ROUTER_AUTH_REF
- HF_AUTH_REF

Secrets are deployment-time only.