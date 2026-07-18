# 10 Refutaciones: defectos, mejoras, faltantes

**Fecha**: 2026-07-18
**Paso**: 4/10

## R1: 3 columnas split-view necesita más espacio
**Defecto**: Con 3 modelos en split-view, cada columna tiene ~33% del ancho. En viewport 1280px son 426px cada una → texto chat apretado.
**Mejora**: Default 1 modelo + botón "compare" para split. 2 modelos = 50/50. 3 modelos = 33/33/33 pero con modo "compact" reduce padding.

## R2: Memory auto-recall puede inyectar info obsoleta
**Defecto**: Graphiti retorna top-5 entities de hace 14 días. Pueden ser irrelevantes hoy.
**Mejora**: Botón "X" en cada entity inyectada para descartarla. Graphiti aprende de los descartes (negative feedback loop).

## R3: Drag-drop no funciona en mobile
**Defecto**: HTML5 drag-drop es desktop-only. Mobile no tiene equivalente nativo.
**Mejora**: Botón `+` en input-block que abre file picker nativo. Multi-select con thumbnails. Mantiene UX cross-platform.

## R4: Búsqueda unificada es lenta con 4 fuentes
**Defecto**: Buscar "D26" ejecuta 4 queries (FTS5 + GitHub API + Chroma + Graphiti). 2-3s latencia.
**Mejora**: Pre-cache indices al login. Update incremental. SLA <200ms post-cache-warm.

## R5: Skill auto-creación puede spammear
**Defecto**: Si Max usa muchos comandos parecidos, panel propone 20 skills en 1 día.
**Mejora**: Threshold mínimo 5 usos + 3 días. Cooldown 7 días entre propuestas. Setting para disable.

## R6: Watchdog log puede llenar disco
**Defecto**: Cada check genera 5KB log. 1 check/min = 7MB/día = 2.5GB/año.
**Mejora**: Log rotation daily, gzip >7 días, delete >30 días. UI muestra "X MB used".

## R7: Wikilinks no se actualizan al renombrar archivos
**Defecto**: Si Max renombra `nota1.md` a `intro.md`, los `[[nota1]]` quedan rotos.
**Mejora**: Hook PreToolUse detecta rename → update all wikilinks → commit. Como Obsidian 1.11 desktop hace.

## R8: Kanban drag-drop sin optimistic UI
**Defecto**: Si Graphiti está lento, el drop se siente laggy 2-3s.
**Mejora**: Optimistic UI: card se mueve inmediato, rollback si falla. Status indicator "syncing/synced/failed".

## R9: OCR solo extrae texto, no estructura
**Defecto**: Foto de tabla → texto plano, pierde filas/columnas.
**Mejora**: PaddleOCR tiene modo `table` + Baidu OCR `table recognize` (form-aware). Detectar automáticamente y aplicar.

## R10: Export no incluye state.json
**Defecto**: HTML+CSS+JS sin state pierde conversaciones, settings, projects.
**Mejora**: Incluir `state.json` con todo el state serializado. Import wizard restaura. Versioning semántico.
