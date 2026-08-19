# SALIDA 5 — archivo operador (USB / plugin / resource bus)

**Ingest:** 2026-08-19
**Repo:** osquestador-auditor/reception
**Anotación de trabajo:** `PIPELINE-osquestador-auditor-memoria/SALIDA_5_USB_RESOURCE_BUS.md`
**No reescrito.** El md es provenance.

---

Sí, te entiendo perfectamente. Lo que estás describiendo sí es una arquitectura real: no quieres “meter” el código de n8n, Graphiti, un OCR, etc. dentro del agente. Quieres que el agente los trate como recursos externos enchufables, igual que conectar un USB: el agente descubre el recurso, conoce su interfaz y lo utiliza, pero no modifica su código fuente.

La forma técnica de pensarlo es:

AGENTE / WORDFLOW
                       │
                 RESOURCE BUS
                       │
              ┌───────┴───────┐
              │                 │
         PLUGIN ADAPTER     PLUGIN ADAPTER
              │                 │
          Graphiti             OCR
              │                 │
        servicio externo   servicio externo

## 1. La idea fundamental

El agente no necesita conocer la implementación interna.
Solo necesita conocer un contrato:

CAPABILITY: name: ocr
INPUT: image
OUTPUT: extracted_text
EXECUTE: ocr(image) → text

Por debajo puede haber Baidu OCR, Tesseract, PaddleOCR, Google OCR u otro servicio.
El agente no debería importar ni modificar el código de esos proyectos.

## 2. El USB de código

El agente conecta el recurso y llama:

agent.execute(capability="ocr", input=image)

No necesita saber cómo funciona internamente OCR.

## 3. Cuatro capas

WORDflow (decisión / tareas)
→ RESOURCE BRAIN (discover / register / select)
→ PLUGIN ADAPTER (contrato uniforme)
→ EXTERNAL RESOURCE (Graphiti / n8n / OCR / etc.)

PLUGIN ADAPTER no modifica el software externo.

## 4. Qué hace el plugin

Adaptador/traductor. Wordflow habla search_memory(query); el adapter habla la API nativa.

## 5. Código externo intacto

plugins/<name>/{manifest.yaml, adapter.py, contract.yaml}
PLUGIN ≠ SOFTWARE EXTERNO.

## 6. Manifest

name, version, type: external_resource, transport, capabilities, input/output, healthcheck, credential_ref.

## 7. Ciclo Resource Brain

DISCOVER → REGISTER → MAP → VERIFY → SELECT → PREPARE → LOAD → EXECUTE

## 8–9. n8n y OCR

Mismo patrón. Capability = OCR, no BaiduOCRInternals.

## 10–11. Transports

LOCAL PROCESS, HTTP, MCP, CLI, DOCKER, PYTHON PACKAGE, REMOTE API.
Open source sin tocar el repo original. Graphiti v1→v2 mantiene memory_search.

## 12. Capacidades, no programas

NEED: memory_search. SELECT por health, version PINNED, latency.

## 13. No reescribir

NEED CAPABILITY → SEARCH EXISTING → CONNECT → USE
GENERATE solo si no hay resource, adapter ni API.

## 14. Contrato pequeño

class Resource: discover, health, capabilities, execute(capability, payload)

## 15. Resultado

RESOURCE BUS con n8n, Graphiti, OCR, GitHub, HF, MCP, Browser, Docker, SSH, DB.
Wordflow no contiene ese software. Contiene RESOURCE, PLUGIN, MANIFEST, ADAPTER, CONTRACT, CREDENTIAL_REF, HEALTHCHECK.

Frase: Un recurso externo debe poder conectarse al Wordflow mediante un Plugin Adapter sin modificar ni reescribir su código fuente. Wordflow consume capacidades, no implementaciones.
