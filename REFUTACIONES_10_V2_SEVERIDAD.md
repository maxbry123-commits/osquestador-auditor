# 10 Refutaciones (V2) — con severidad y métrica de impacto

**Fecha**: 2026-07-18
**Paso**: 4/10 v2

## R1: 3 columnas split-view sin espacio
**Severidad**: ALTA
**Impacto UX**: Con 3 modelos en split-view a 1280px, cada columna = 426px. Texto chat apretado, código cortado.
**Métrica**: Si viewport <1440px, mostrar warning "Use 2 models or wider viewport".
**Fix**: Default 1 modelo. Botón "Compare" para split. 2 modelos = 50/50. 3 modelos = 33/33/33 con modo compact (reduce padding 8px→4px).

## R2: Memory auto-recall puede inyectar info obsoleta
**Severidad**: MEDIA
**Impacto**: Graphiti retorna top-5 de hace 14 días. Pueden no aplicar hoy → confusión.
**Métrica**: Relevance threshold >0.7, max 5 entities, timestamp visible.
**Fix**: Botón "X" en cada entity. Graphiti aprende negative feedback. Top 3 siempre, con option "Show 5 more".

## R3: Drag-drop no funciona en mobile
**Severidad**: ALTA
**Impacto**: HTML5 drag-drop es desktop-only. 40% del tráfico web es mobile.
**Métrica**: Lighthouse mobile score <90 = fail.
**Fix**: Botón `+` en input-block → file picker nativo. Multi-select thumbnails. Long-press para reorder en mobile.

## R4: Búsqueda unificada lenta con 4 fuentes
**Severidad**: MEDIA
**Impacto**: 4 queries (FTS5 + GitHub + Chroma + Graphiti) = 2-3s latencia.
**Métrica**: SLA <500ms post-cache-warm.
**Fix**: Pre-cache indices al login (background). Update incremental cada 5min. Single-flight request para evitar duplicados. Web Worker para no bloquear UI.

## R5: Skill auto-creación puede spammear
**Severidad**: BAJA
**Impacto**: 50 comandos usados = 50 propuestas en 1 día.
**Métrica**: Max 1 propuesta por día por usuario.
**Fix**: Threshold 5 usos / 3 días rolling. Cooldown 7 días entre propuestas. Setting para disable global. Snooze 24h.

## R6: Watchdog log puede llenar disco
**Severidad**: MEDIA
**Impacto**: 5KB/log × 1440min/día = 7MB/día = 2.5GB/año.
**Métrica**: Max 500MB log storage.
**Fix**: Log rotation daily. Gzip >7 días. Delete >30 días. UI muestra "X MB used" + botón clean.

## R7: Wikilinks no se actualizan al renombrar
**Severidad**: ALTA
**Impacto**: Renombrar `nota1.md` → `intro.md` rompe `[[nota1]]` en 5+ archivos.
**Métrica**: 0 wikilinks rotos después de rename.
**Fix**: Hook PreToolUse detecta rename → update all wikilinks → commit. Index lookup en SQLite FTS5. Atomic transaction.

## R8: Kanban sin optimistic UI
**Severidad**: MEDIA
**Impacto**: Graphiti lento = drop se siente laggy 2-3s. Usuario piensa que falló.
**Métrica**: Visual feedback <16ms.
**Fix**: Optimistic UI: card se mueve inmediato, status "syncing". Sync background. Rollback si falla >5s. Toast confirmation.

## R9: OCR solo extrae texto, no estructura
**Severidad**: ALTA
**Impacto**: Foto de tabla → texto plano. Pierde info crítica (filas/columnas).
**Métrica**: 95% estructura preservada.
**Fix**: PaddleOCR tiene `table` mode. Baidu OCR `table recognize` (form-aware). Detección automática: si ve grids, aplicar table mode. Output markdown con `<table>`.

## R10: Export sin state.json
**Severidad**: ALTA
**Impacto**: HTML+CSS+JS sin state pierde conversaciones, settings, projects. Export inútil.
**Métrica**: 100% state restoration.
**Fix**: Incluir `state.json` con TODO el state serializado (conversations, projects, skills, settings, tokens, decisions). Import wizard detecta + restaura. Versioning semántico para migrations. Sanitización: NO secrets en export.
