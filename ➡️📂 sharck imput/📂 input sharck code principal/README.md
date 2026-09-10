# 🦈 INPUT SHARCK CODE PRINCIPAL

Único root de código/producto V2:
`➡️📂 sharck imput/📂 input sharck code principal/`

## Reglas
- COPY-FIRST; no programar desde cero si existe componente reusable aprobado.
- Backend en contracts/adapters/plugins/registry/loader/guards/tests; no monolito.
- Todo upstream descargado vive en `📂 componentes open source/` y no se considera wired automáticamente.
- `📂 component acquisition/` contiene sólo queues/state/index/config para invocar motores canónicos externos.
- Código integrado se crea por versión/patch, manteniendo rollback pointer.
- Integración Paso 3 bloqueada hasta review gate ASTRA + CLAUDE + GROK + gate del director.
- Tool/resource connections se exponen por interfaces MCP/API/plugins según capacidad; no acoplar lógica de proveedor al Core.

## Estados físicos
`RESEARCHED → QUEUED → ACQUIRED → EXTRACTED → READBACK_VERIFIED → APPROVED_FOR_WIRE → WIRED → TESTED → PROMOTED`.

No usar `VERIFIED_CLOSED` para una integración sólo porque la descarga terminó.
