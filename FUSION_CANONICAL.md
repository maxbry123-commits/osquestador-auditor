# FUSIÓN CANÓNICA — AUDITOR

**Fecha:** 2026-08-19
**Política:** COPY-FIRST · 90/10 · no PAT crudo · workflow en A · software en B

## Verdad

| Rol | Repo | Cuenta |
|-----|------|--------|
| Workflow / contrato / reception / forense | `maxbry123-commits/osquestador-auditor` | A |
| Kernel Wordflow / ficha / token_ref | `maxbry123-commits/agentes` | A |
| Software store + memoria (código runtime) | `abc1tienda-web/osquestador-auditor-y-memoria-1` | B |
| Fase 0 a reciclar (NO verdad) | `maxbry123-commits/orchestrator-auditor` | A |
| Stub vacío NCT | `maxbry123-commits/Auditoria` | A |
| Memoria NCT (no auditor) | `maxbry123-commits/MEMORIA` | A |

## Qué se fusiona y qué no

- **Canónico auditor (A):** solo `osquestador-auditor`.
- **`orchestrator-auditor`:** se conserva como archivo de recambio. Kernel/plugins en `orchestrator/{kernel,agents,inputs,outputs,mcp,workflows}` se copian a B cuando haya primer enchufe, no se reescriben aquí.
- **`Auditoria`:** stub; no hay código. Queda señalizado como no-canónico.
- **No se borra ningún repo** en este corte (evidencia forense).
- **No se mete software nuevo en `agentes`** (evitar saturación).

## Recycle (COPY-FIRST)

Desde `orchestrator-auditor`:

- `orchestrator/kernel/` → runtime B
- `orchestrator/mcp/` → connector MCP
- `orchestrator/workflows/` → jobs deterministas
- `reception/` → alinear con `osquestador-auditor/reception/DOC_UPLOAD_SCHEMA.yaml`

Desde `agentes`:

- `extensions/wordflow_kernel/` → kernel
- `extensions/wordflow/ficha.v2.json` + reception convert
- `extensions/wordflow/connectors/github_external.py` + `credential_ref`

Desde `osquestador-auditor`:

- `reception/DOC_UPLOAD_SCHEMA.yaml`
- enchufe universal (plugin bus + ficha_contract) ya en raíz
- fusion resumen en `reception/`

## UI

Solo ventana de carga de documentos (schema reception). Nada de canales extra.

## Estado B

Workflow `agentes/.github/workflows/create-cuenta-b-repo.yml` run 2 (2026-08-19) = **success** con `EXTERNAL_GH_B_TOKEN`.
Esta sesión (A) no puede listar el repo privado de B. URL esperada:

https://github.com/abc1tienda-web/osquestador-auditor-y-memoria-1
