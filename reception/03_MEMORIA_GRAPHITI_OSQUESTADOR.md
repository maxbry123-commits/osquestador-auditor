# Memoria · Graphiti, Grapify, OCR Baidu, Osquestador auditor
**Base en repo:** control-layer/memory/ (parcial)  
**Regla de producto:** memoria **nativa**. No obligar Obsidian / Graphiti / n8n / Baidu UI como sistemas independientes.

---

## 1. Qué ya existe (no reescribir)

```text
control-layer/memory/
  router.py, guard.py, policy.py, classifier.py
  session_store.py, doc_registry.py, versioning.py
  providers/local_provider.py
  providers/tencent/          # adapter oculto
  MEMORY.md                   # tiers 0–3 parciales
```

Arquitectura acordada:

```text
Wordflow / ControlBus
        ↓
Memory Control Plane (qué guardar, dónde, cuándo, cuánto)
        ↓
Router + Guard + Policy + Classifier
        ↓
LocalProvider (primero) → TencentAdapter (opcional, oculto)
        ↓
Tier 0 RAW · 1 SESSION · 2 STRATEGIC · 3 PROJECT
```

KG lateral (diseño): aristas version_de / contradice / refina / depende_de / cita_a / autoridad_sobre.  
Conflicto → C60 CONFLICT (no auto-elige ganador; escala salvo autoridad_sobre).

---

## 2. Graphiti → capability nativa

| Paso | Acción |
|------|--------|
| 1 | Pin source OS en manifest (repo + ref + sha256) |
| 2 | Pull determinista → agents/sources/graphiti/ o vendor/ |
| 3 | Evolution modo 4: destilar motor grafo |
| 4 | Package extensions/memory_graph/ |
| 5 | Capabilities: memory.graph.upsert, memory.graph.query |
| 6 | Wire a MemoryRouter (tiers 2/3 + aristas) |

**Grapify:** mismo patrón si aporta grafo/visual; capability opcional memory.graph.visualize (export). No GUI externa obligatoria.

---

## 3. OCR Baidu → capability nativa

| Opción | Uso |
|--------|-----|
| A API Baidu | Solo CredentialBroker; nunca key en prompt/event/log |
| B OCR OS (Paddle/Tesseract/…) | Preferible: pin source → Evolution → extensions/ocr/ |

Capability: `ocr.extract_text` (artifact imagen/pdf → texto + bbox opcional).  
Salida a Tier 0/1 o Artifact Store.

---

## 4. Osquestador auditor de memoria

**Qué es:** kernel/microservicios de memoria + auditoría de integridad (docs usuario).  

**Estado:** diferido hasta docs completos del osquestador.  

**Slot:**

```text
extensions/osquestador_memory/
  auditor.py       # integridad tiers, scopes, no-regresión
  kernel_hooks.py  # API hacia MemoryRouter
  tests/
```

**Auditor debe chequear:**
- chain tips tier0/1/3 coherentes  
- isolation proyecto A ⟂ B  
- no secrets en records  
- no-regresión post-Evolution (canary memoria)  

Binario temporal: manifest SHA + carpeta dedicada; no mezclar con core hasta OK.

---

## 5. Orden cuando se implemente memoria

1. Namespaces G0.11 (Mission/Task/Job)  
2. Artifact refs en eventos (no blobs en bus)  
3. Graph nativo (Graphiti destilado o KG mínimo)  
4. OCR capability  
5. Dream / Distill loops  
6. Osquestador + auditor (docs usuario)  

**Prohibido:** exigir Graphiti/Baidu instalados como dependencia de usuario final.
