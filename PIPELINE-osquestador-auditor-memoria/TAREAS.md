# CONTROL DE TRABAJO

## 1 TOTAL (lote actual)
S5-USB-SCAN — inventario recycle + memoria PIPELINE + anotar archivo USB

## 2 TERMINADAS
- SALIDA-2 recycle forensic (previo)
- S5-USB-SCAN docs + inventario + copia resource/capability (este commit)

## 3 PENDIENTES
- [ ] Adapter USB delgado: `plugins/<name>/{manifest,adapter,contract}` sobre ResourceRuntime existente
- [ ] Healthcheck + credential_ref (HTTP/MCP/CLI/Docker) sin embeber Graphiti/n8n/OCR
- [ ] Wire CapabilityBrain → need=memory_search|ocr|workflow, no nombres de vendor
- [ ] Cuenta 2 abc1tienda-web: el usuario crea el repo; aquí no hay acceso
- [ ] Forense de bloque (al cierre de code USB, no ahora)
- [ ] No copiar wordflow/engine completo (~250 py)

## 4 SIGUIENTE
Esperar autorización. Candidato: primer plugin adapter (graphiti o n8n) COPY-FIRST desde enchufe_gate + resource_runtime.

## 5 PLAN
NEED capability → SEARCH catalog/runtime → CONNECT adapter → USE. GENERATE solo si no hay adapter ni API.

## 6 MÉTODO
V4 + COPY-FIRST + 56–60. Ver `00_METODO.md`.

## 7 NOTAS
GitHub=verdad. No sandbox esta pasada. Orígenes A intactos.
