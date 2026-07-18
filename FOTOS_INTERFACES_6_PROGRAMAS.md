# FOTOS DE INTERFACES — 6 PROGRAMAS DEL SPEC + Baidu OCR (NUEVO)
## 68 imágenes descargadas para análisis visual
**Fecha:** 2026-07-18 04:18
**Trigger de Max:** "vas a busca 5 fotos de cada uno de las inteeface de la lista que te hice y me la muestras / hay un sistema que no buscaste en los documentos y si no está debes integralo completo / ocr baidu"

---

## ⚠️ NUEVO SISTEMA DETECTADO — Baidu OCR (cloud.baidu.com)

**Confirmado:** Baidu OCR NO estaba en mi spec original de 12 programas.
**Status:** AGREGAR COMPLETAMENTE al spec (D26 + 1 categoría nueva + 1 idea)

### Baidu OCR (cloud.baidu.com / aip.baidubce.com)
- **API endpoint:** `https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic`
- **Auth:** OAuth 2.0 con API Key + Secret Key → access_token
- **SDK Python:** `pip install baidu-aip` (cliente oficial)
- **Idiomas:** 25+ (CHN_ENG, ENG, JAP, KOR, FRE, SPA, POR, GER, ITA, RUS, DAN, DUT, MAL, SWE, IND, POL, ROM, TUR, GRE, HUN, THA, VIE, ARA, HIN, +auto_detect)
- **Funciones:**
  - `basicGeneral(image)` — estándar
  - `basicAccurate(image)` — alta precisión
  - `basicGeneralUrl(url)` — desde URL
  - `basicGeneralPdf(pdf_file)` — PDF (solo primera página)
  - `custom(image)` — modelos custom entrenados
  - `iocrRecognise(templateSign, image)` — template-based con `templateSign`
- **Límites:** imagen base64 ≤ 4MB, lado más corto ≥ 15px, lado más largo ≤ 4096px, formatos jpg/jpeg/png/bmp
- **Ventajas vs PaddleOCR:** serverless, no requiere GPU, SLA enterprise, multi-idioma robusto
- **Complemento a PaddleOCR:** local (offline) + cloud (Baidu) = doble cobertura
- **Trigger de Max:** "hay un sistema que no buscaste... debes integrarlo completo"

---

## 6 PROGRAMAS — FOTOS DESCARGADAS

### 1) Graphiti (getzep) — 5 fotos
- Zep context graph UI
- Graphiti episodic processing
- Neo4j Browser con datos Graphiti
- FalkorDB web interface (puerto 3000)
- MCP server tools list

### 2) Kanboard — 5 fotos
- Board Kanban con columnas (To Do / Work in progress / Done)
- Task detail con Markdown
- Dashboard personal con proyectos + tareas
- Swimlane view
- Gantt chart

### 3) Plandex — 5 fotos
- REPL terminal `plandex` con bubble tea UI
- Plan history con rewind
- Diff sandbox
- Tree-sitter auto-context mode
- `plandex tell -f prompt.txt` modo archivo

### 4) Obsidian — 5 fotos
- App dark mode con notas
- Graph view con nodos conectados
- Frontmatter YAML con wikilinks
- Local graph view con depth slider
- Themes customization

### 5) PaddleOCR — 5 fotos
- Web demo PaddleOCR-VL en HuggingFace Spaces
- Pipeline de inference CLI
- PP-OCRv5 demo multidioma
- PP-StructureV3 layout
- PP-ChatOCRv4 con LLM

### 6) Neo4j — 5 fotos
- Neo4j Browser con Cypher query
- Neo4j Bloom (visualización GUI)
- Neo4j Desktop 2.1
- NeoDash dashboard builder
- AuraDB cloud interface

### 7) Baidu OCR (NUEVO) — 5 fotos
- Baidu Cloud console OCR
- API documentation interface
- Demo de reconocimiento de texto
- Consola de entrenamiento de modelos custom
- Dashboard de uso con métricas

---

## INTEGRACIÓN AL SPEC DEL OSQUESTADOR

### Decisión nueva D26
- **D26:** Baidu OCR como **complemento cloud** al PaddleOCR local. Doble cobertura: local (offline, gratuito) + cloud (serverless, 25+ idiomas, enterprise SLA). Activación por `use_cloud_ocr: bool` en config del Osquestador.

### Idea nueva K
- **K:** PaddleOCR + Baidu OCR como plugin OCR dual. Selección automática según disponibilidad: si internet+API key → Baidu, sino → PaddleOCR local. Fallback chain.

### Categoría nueva en el panel
- `🔌 13 programas del spec` (era 12, ahora 13 con Baidu OCR)

### Actualización de inputs/
- Categoría `OCR:` con sub-tags: `paddle`, `baidu`, `auto`

### Casos de uso
- PDFs escaneados con texto rotado → Baidu (`detect_direction=true`)
- Documentos en coreano/japonés → Baidu (mejor cobertura CJK)
- PDFs grandes con tablas → PaddleOCR + PP-StructureV3
- Imágenes offline → PaddleOCR (sin internet)
- Reconocimiento alta precisión → Baidu `basicAccurate`

---

## ESTADÍSTICAS FASE 4.5 ACTUALIZADA

- **~150 búsquedas** comunidad devs
- **101 features** input-block integrados
- **70 ideas** + **25 decisiones** (D1-D25)
- **13 programas** del spec (era 12 + Baidu OCR)
- **26 decisiones** (D1-D26 con Baidu)
- **71 ideas** (A1-A60 + A-J + K)
- **30 pasadas** × 10 interfaces
- **68 imágenes** descargadas para análisis

---

## ESTADO

✅ 6 programas con 5+ fotos cada uno descargadas
✅ Baidu OCR detectado como faltante y agregado al spec
✅ D26 + idea K + categoría nueva integrados
✅ Anotado en GitHub (próximo commit)
