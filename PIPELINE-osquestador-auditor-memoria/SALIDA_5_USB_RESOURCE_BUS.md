# SALIDA 5 — USB / PLUGIN ADAPTER / RESOURCE BUS

**Origen:** input operador 2026-08-19 (Pasted Text — arquitectura USB de recursos).
**Tipo:** ANOTACIÓN. No reescribe el texto. Provenance intacta.
**Método:** V4 · COPY-FIRST · capabilities no vendors.

## Veredicto de recycle (antes de programar)

EXISTING_IMPLEMENTATION_FOUND → DO NOT GENERATE el bus.

El archivo describe 4 capas (Wordflow → Resource Brain → Plugin Adapter → External Resource).
En `agentes/extensions/wordflow` eso ya está parcialmente code:

| idea del documento | code existente |
|---|---|
| RESOURCE BRAIN discover…execute | `capability_brain.py` + `resource_runtime.py` |
| contrato Capability | `capability_intent.py` + `capability_passport.py` |
| catalog / register | `resource_catalog.py` |
| prepare / load | `resource_broker.py` + `resource_gate.py` |
| enchufe / ficha | `enchufe_gate.py` + `ficha.v2.json` |
| PLUGIN ≠ SOFTWARE EXTERNO | **GAP:** falta carpeta `plugins/<recurso>/` |
| Graphiti / n8n / OCR adapters | **GAP:** no hay adapter.py por vendor |
| healthcheck + credential_ref | **GAP** (hay `credential_store.py` POINTER) |
| transports HTTP/MCP/CLI/Docker | parcial: `docker_transport.py` POINTER |

## Regla de salida 5

NEED: memory_search | ocr | execute_workflow
SEARCH: catalog + runtime + connect_catalog
CONNECT: plugin adapter (nuevo, delgado)
USE: execute(capability, payload)
NO: copiar Graphiti/n8n/Tesseract al repo.
NO: 2000 líneas LLM.
GENERATE solo adapter+manifest+contract si no existen.

## Frase canónica (del input)

> Un recurso externo debe poder conectarse al Wordflow mediante un Plugin Adapter sin modificar ni reescribir su código fuente. El recurso se registra como una Capability Provider y se ejecuta mediante su interfaz nativa. Wordflow consume capacidades, no implementaciones.

## Texto original (sin reescribir)

---

Sí, te entiendo perfectamente. Lo que estás describiendo sí es una arquitectura real: no quieres “meter” el código de n8n, Graphiti, un OCR, etc. dentro del agente. Quieres que el agente los trate como recursos externos enchufables, igual que conectar un USB: el agente descubre el recurso, conoce su interfaz y lo utiliza, pero no modifica su código fuente.

AGENTE / WORDFLOW → RESOURCE BUS → PLUGIN ADAPTER → Graphiti | OCR (servicio externo).

El agente solo conoce un contrato: CAPABILITY / INPUT / OUTPUT / EXECUTE.
Por debajo puede haber Baidu OCR, Tesseract, PaddleOCR, Google OCR. El agente no importa ni modifica esos proyectos.

Cuatro capas: WORDflow (decisión) → RESOURCE BRAIN (discover/register/select) → PLUGIN ADAPTER (contrato uniforme) → EXTERNAL RESOURCE.

PLUGIN ≠ SOFTWARE EXTERNO. El repo solo tiene `plugins/<name>/{manifest.yaml, adapter.py, contract.yaml}`.

Ciclo: DISCOVER → REGISTER → MAP → VERIFY → SELECT → PREPARE → LOAD → EXECUTE.

n8n / OCR / Graphiti = HTTP u otro transporte. Capability estable si cambia la versión del vendor.

Transports: LOCAL PROCESS | HTTP | MCP | CLI | DOCKER | PYTHON PACKAGE | REMOTE API.

NEED CAPABILITY → SEARCH EXISTING → CONNECT → USE. GENERATE solo si no hay resource, ni adapter, ni API.

Contrato mínimo: discover / health / capabilities / execute(capability, payload).

SOURCE CODE → NO REWRITE / NO MODIFY → EXTERNAL RESOURCE → PLUGIN ADAPTER → CAPABILITY → WORDFLOW.

Texto íntegro también en `reception/SALIDA_5_USB_PLUGIN_ADAPTER.md`.
