# PLATFORM INTEGRATION

Canonical memory/storage service for the platform.

Inbound application route:
frontend / agentes / Orquestador-Maxbry- -> universal router -> memory service

Outbound compute route:
osquestador-auditor -> universal router -> Hugging Face

Required deployment variables:
- ROUTER_BASE_URL
- HF_EXECUTION_BASE_URL
- MEMORY_AUTH_REF
- ROUTER_AUTH_REF
- HF_AUTH_REF

Persistent memory/storage remains here; Hugging Face is not the canonical persistence layer.
