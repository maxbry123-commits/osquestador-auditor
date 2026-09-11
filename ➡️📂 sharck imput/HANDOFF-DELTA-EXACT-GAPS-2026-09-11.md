# HANDOFF DELTA — EXACT GAPS — 2026-09-11

Fuente de verdad: `maxbry123-commits/osquestador-auditor` → `main` → `➡️📂 sharck imput/`.

Este delta NO sustituye el Handoff maestro. Resume evidencia M21–M25 para que ASTRA/CLAUDE/GROK continúen sin pisarse.

## Estado base
- Método único: 3 pasos.
- Paso 1 inventario/arquitectura: documentado.
- Paso 2 adquisición: activo con GAPs.
- Paso 3 integración: `BLOCKED` hasta M06+M07+M08 + gate director.
- Catálogo: 117 total = 77 legacy + 40 nuevos.
- Nuevos B01–B04: 17 VERIFIED_CLOSED / 23 FAILED / 0 pending.

## M21 — B04 exact X-Ray
Evidence: `📂 Craxy wall bitácora stated JSON/B04-XRAY-2026-09-11.md`.
- `spaCy`: partial exacto; faltan sólo `spacy/matcher/polyleven.c` y `website/.vscode/extensions.json`; 0 changed/0 extra. Runs 34566821665 + 34566985338.
- `huggingface_hub`: `CLAUDE.md` special; Git mode 120000 confirmado.
- `unstructured`: special paths concentrados en performance fixtures; symlink evidence confirmada.

## M22 — 11 partials B01–B03 exact diff
Evidence: `📂 Craxy wall bitácora stated JSON/PARTIALS-XRAY-11-2026-09-11.md`.
Run: `34567075204`, jobs 11/11 diagnostic success.
Agregado: 130 missing + 7 changed + 0 extra.
Prioridad: sqry, OpenSearch, heritrix3, yacy_search_server, nutch, kythe, scira, continue, datasketch, smolagents, pyserini.

## M23 — 9 source-special B01–B03 mapped
Evidence: `📂 Craxy wall bitácora stated JSON/SPECIAL-FILES-XRAY-9-2026-09-11.md`.
- B01: stormcrawler, tika, docling.
- B02: vespa, networkx.
- B03: cocoindex, pydantic-ai, litellm, fastmcp.
No motor changes. StrategyDelta debe preferir package/subtree/reference oficial cuando corresponda, sin debilitar special-file safety.

## M24 — causa raíz de los partials
Evidence: `📂 Craxy wall bitácora stated JSON/ROOT-CAUSE-GIT-IGNORE-XRAY-2026-09-11.md`.
Runs: `34567757437` + `34567916375`.
- Los source trees ya estaban completos antes de publicar; el GAP aparece durante staging del snapshot vendor.
- `git add --sparse -- <rel>` vuelve a interpretar `.gitignore` root/anidados y omite archivos que eran TRACKED upstream.
- YaCy `yacyBuildProperties.java` y Continue `webview/index.html` quedaron confirmados como TRACKED upstream pero re-ignorados al re-vendorizar.
- Los 7 LICENSE/NOTICE cambiados de OpenSearch son exclusivamente `CRLF → LF` por filtros/attributes; no se detectó otra mutación.
- Canonical read-back funciona correctamente y mantiene fail-closed.
- No editar motor; no usar `git add -f` en producción sin review/gate.

## M25 — StrategyDelta de staging en sandbox
Evidence: `📂 Craxy wall bitácora stated JSON/STAGING-STRATEGYDELTA-SANDBOX-2026-09-11.md`.
Run: `34568249222`, conclusion=`success`.
Motor usado sin editar: `motor_3_copy_batches.py`, blob `3689924361ce4a1a9fde4ae2b6f6009c37a6042d`.
Prueba representativa con fuentes pinneadas spaCy/OpenSearch/sqry:
- spaCy `polyleven.c` → byte_equal true, mode 100644.
- spaCy `website/.vscode/extensions.json` → byte_equal true, mode 100644.
- sqry `entrypoint.rs` → byte_equal true, mode 100644.
- OpenSearch LICENSE sample → byte_equal true, mode 100644.
Veredicto: `SANDBOX_PASS / REVIEW_REQUIRED / NO_PHYSICAL_REPAIR`.
Esto NO autoriza producción, NO repara los 11 partials completos y NO aplica a source-special/symlink gaps.

## Owner entry points actualizados
### ASTRA / M06
Auditar M24/M25: PRE-LLM scope, fail-closed, NO_LFS, blob/special-file gates, no-force, no-overwrite, rollback/versionado y read-back. Emitir `REVIEW_PASS` o `REPAIR_REQUIRED`; no PASS global.

### CLAUDE / M07
Validar `tracked_upstream_set == staged_set == published_set`, modos 100644/100755 y bytes completos; decidir entre Git plumbing (`hash-object --no-filters`/index-tree) y neutralización temporal controlada de attributes. Definir tests/read-back antes de repair.

### GROK / M08
Contrastar el patrón con vendoring/snapshot Git y alternativas package/subtree oficiales, especialmente para los 9 special-source + huggingface_hub/unstructured. Verificar licencia/mantenimiento/source refs; no auto-instalar.

### SOL
Mantener STATE/CHECKPOINT/Handoff y monitor de owners. Sólo nueva evidencia read-only; no physical repair ni Step3 antes de reviews + gate director.

## Current checkpoint
`CP-V2-STAGING-STRATEGYDELTA-012`
Resume: `M06_M07_M08_REVIEW_OF_ROOT_CAUSE_AND_STAGING_STRATEGYDELTA`.
Balance permanece: **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.
`step3_allowed=false`; `physical_repair_allowed=false`.

## Anti-collision
`FETCH STATE → verify owner → claim own scope → execute only owned/parallel_safe node → evidence → checkpoint`.
Shared files: fresh SHA + sequential write + read-back. Logs separados por agente.
