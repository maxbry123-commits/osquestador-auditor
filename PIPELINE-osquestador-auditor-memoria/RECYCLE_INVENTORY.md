# RECYCLE INVENTORY — 4 pasadas Wordflow + repos

**Fecha:** 2026-08-19
**Política:** COPY-FIRST · 90-10 · no saturar A · no reescribir orígenes

## PASADA 1 — estructura Wordflow (`extensions/wordflow/`)

Árbol: engine, connectors, contracts, standards, schemas, motors, planner, reception, accounts, catalogs.

**Reciclable ya en canónico (SALIDA-2):**
- `ficha.v2.json`, `abi.py`, `validator_v2.py`, ENCHUFE schema
- `reuse_12.py`, `memory_port.py`, `cognitive_registers.py`, `copy_first.py`
- kernel: bootstrap_multi, ficha_loader, memory, llm_control, memory_slot

**No copiar:** engine completo (~130+ py), tests, codegen.

## PASADA 2 — resource bus (USB / capability)

YA EXISTE. No generar Resource Brain.

| archivo | rol | acción |
|---|---|---|
| `engine/capability_brain.py` | discover→register→map→verify→select→prepare→load | COPY |
| `engine/capability_intent.py` | NEED → capabilities | COPY |
| `engine/capability_passport.py` | authorize cap | COPY |
| `engine/resource_catalog.py` | registry entries | COPY |
| `engine/resource_broker.py` | prepare/load | COPY |
| `engine/resource_runtime.py` | 8 estados DISCOVERED…AVAILABLE | COPY |
| `engine/resource_gate.py` | deny remote fetch | COPY |
| `engine/enchufe_gate.py` | ficha.v2 before load | COPY |
| `connect_catalog.json` | mapa WIRED/STUB/GAP | COPY |
| `engine/resource_trace.py` | traza | POINTER |
| `engine/docker_transport.py` | transporte docker | POINTER |
| `engine/extension_registry.py` | registry pkgs | POINTER |
| `engine/credential_store.py` | creds | POINTER |

## PASADA 3 — connectors / ports

- `connectors/github_external.py` — POINTER (GitHub ya vía API)
- `engine/ports/memory_port.py` — ya copiado
- `engine/ports/planning_port.py` — POINTER
- **GAP:** no hay `plugins/graphiti|n8n|ocr/` con adapter+manifest+contract

## PASADA 4 — dependencias del bus

capability_brain importa: capability_intent, environment_scan, extension_registry, hf_index, resource_broker, resource_catalog.
resource_runtime importa: catalog + gate.

**COPY ahora:** los 8 archivos de pasada 2 (autosuficientes o con imports relativos documentados).
**POINTER:** environment_scan, hf_index, extension_registry — no saturar.

## Otros repos (1 pasada cada uno)

| repo | hallazgo | reciclar |
|---|---|---|
| `agentes` | wordflow + audit_forensic | sí, subset |
| `orchestrator-auditor` | kernel+plugins ya en `orchestrator/` | no re-copiar |
| `MEMORIA` | app.js, reception schema | schema ya; app.js POINTER |
| `Auditoria` | repo casi vacío | — |
| `nct-core` | sin hits plugin/adapter | — |
| `router-universal` / `maxbry-router` | router, no USB bus | POINTER |
| `comand-Center` | UI Claude | POINTER panel |
| `abc1tienda-web` | UNREACHABLE | usuario crea |

## Documentos del operador (ya en este repo)

`reception/` + `INPUT_BLOCK_*.md` + `PIPELINE/` corto. No mover. Indexados aquí.
El archivo USB de esta conversación → `SALIDA_5_USB_RESOURCE_BUS.md` + `reception/SALIDA_5_USB_PLUGIN_ADAPTER.md`.
