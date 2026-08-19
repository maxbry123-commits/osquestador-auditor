# FUSIÓN CANÓNICA — AUDITOR

**Fecha:** 2026-08-19
**TRANSFER:** X-001 + SALIDA-2
**Método:** COPY-FIRST · 90/10 · no reescritura · no borrar repos

## Verdad

| Rol | Repo |
|-----|------|
| Canónico de trabajo | `maxbry123-commits/osquestador-auditor` |
| Workflow / Wordflow (no saturar) | `maxbry123-commits/agentes` |
| Fuente auditor (shell) | `maxbry123-commits/orchestrator-auditor` |
| Stub | `maxbry123-commits/Auditoria` |
| Memoria NCT (no fusionada completa) | `maxbry123-commits/MEMORIA` |
| Cuenta B software store | **NO ACCESIBLE** desde esta sesión |

## Cuenta B — acción tuya

No puedo crear ni empujar a `abc1tienda-web`.
Si quieres el store en cuenta 2, crea tú:

`abc1tienda-web/osquestador-auditor-y-memoria-1`

Luego dime la URL y cableamos `credential_ref`.

## Qué ya estaba

SOURCE: `orchestrator-auditor/orchestrator/`
DEST: `osquestador-auditor/orchestrator/`

- Árbol copiado: kernel, base, store, mcp, agents, inputs, outputs, tools, workflows.
- Repos origen no borrados.

## SALIDA-2 recycle (este commit)

Subset COPY-FIRST en `recycle/`:

- `recycle/wordflow/` — ficha.v2 + enchufe schema + abi + validator
- `recycle/wordflow_kernel/` — bootstrap_multi, ficha_loader, memory, llm_control, ficha
- `recycle/wordflow_kernel/memory_slot/` — adapter + contracts
- `recycle/audit_forensic/ficha.v2.json`
- `recycle/memoria/MEMORIA-FRONT.md`
- `recycle/SOURCE_MAP.yaml` — SHA de cada origen

**No copiado a propósito:** `agentes/extensions/wordflow/engine/**` (~250 py). Queda en A para no saturar.

## UI

Solo ventana de carga (`reception/DOC_UPLOAD_SCHEMA.yaml`).
