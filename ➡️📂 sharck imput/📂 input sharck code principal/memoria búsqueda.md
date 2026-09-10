# 🦈 MEMORIA DE BÚSQUEDA — SHARCK INPUT V2

Tipo: memoria de investigación/provenance. No sustituye STATE ni CHECKPOINT.

## 2026-09-10 — bootstrap V2

### Estado heredado
- V1 catalogó 77 componentes.
- Último STATE V1 leído: 47 VERIFIED_CLOSED, 30 GAP.
- V1 se preserva sin reescritura.

### Criterios de investigación aplicados
1. COPY-FIRST: buscar componente/repo antes de diseñar código nuevo.
2. Separar `RESEARCHED`, `QUEUED`, `VERIFIED_CLOSED`, `WIRED`, `TESTED`.
3. Revisar existencia/mantenimiento cuando sea posible antes de poner un candidato en cola.
4. Excluir repos archivados como base principal cuando haya alternativa activa.
5. Mantener experimental separado de base madura.

### 30 componentes añadidos
- B01: Scira, YaCy, Nutch, Heritrix3, StormCrawler, Scrapy, Trafilatura, Tika, Docling, MinerU.
- B02: Lucene, Pyserini, PyTerrier, OpenSearch, Vespa, Tantivy, NetworkX, RDFLib, RapidFuzz, datasketch.
- B03: CocoIndex, Kythe, sqry, open-codebase-index, Sourcebot, Continue, PydanticAI, smolagents, LiteLLM, FastMCP.

### Decisiones y descartes
- `smallcloudai/refact`: detectado archivado durante revisión; no se puso en batch. Sustitución: Continue.
- `sqry` y `open-codebase-index`: conservar como `EXPERIMENTAL` hasta tests propios.
- SearXNG se mantiene como federador importante, no como única fuente: arquitectura exige múltiples engines y scoring de evidencia.
- Code RAG debe preferir símbolos/call graph/pointers sobre chunks arbitrarios cuando la estructura esté disponible.

### Principios de source/code/skill/tool
- KNOWLEDGE, CODE, SKILLS y TOOLS son índices separados conectados por Capability Graph.
- Repo encontrado no implica código confiable/ejecutable.
- Tool encontrada no se auto-instala: discover → verify source/version/permissions → sandbox/test → register → expose.
- Code Pointer conserva repo/ref/path/symbol/hash; contenido completo se recupera bajo demanda.

### Adquisición
- 3 colas de 10 creadas bajo `📂 component acquisition/queues/`.
- Workflow: `.github/workflows/sharck-input-v2-components.yml`.
- Run inicial: `34514168678`.
- Última evidencia al escribir: B01/B02/B03 en ejecución; checkout NO LFS y motor blob gate PASS 3/3; descarga/extracción todavía en progreso.

## Regla append-only
Añadir nuevas investigaciones por fecha. Si cambia una conclusión, escribir `SUPERSEDES: <entrada>` y conservar la anterior; no borrar historia para aparentar consistencia.
