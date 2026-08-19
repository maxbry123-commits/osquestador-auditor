# 56 — Fusión X-001 y método

Después de fusionar los repos de auditor:

1. Canónico = `osquestador-auditor`.
2. Código Fables vive en `orchestrator/` de ese repo.
3. `orchestrator-auditor` queda como archivo (no borrar).
4. COPY-FIRST / MOVE-FIRST antes de GENERATE.
5. Léxico: PATCH-LEX-01 + contrato de organización + PATCH-GIT-01.
6. 90/10: kernel y plugins deterministas; LLM solo si hay gap autorizado.
7. No saturar `agentes` con software de auditor.
8. No inventar UI: inbox de documentos.

Pipeline: CONTEXT → COPY-FIRST → WIRE → FORENSIC 4-PASS → VERDICT.
