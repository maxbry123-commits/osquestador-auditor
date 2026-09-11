# HANDOFF DELTA — EXACT GAPS — 2026-09-11

Fuente de verdad: `maxbry123-commits/osquestador-auditor` → `main` → `➡️📂 sharck imput/`.

Este delta NO sustituye el Handoff maestro. Resume únicamente la evidencia nueva M21/M22/M23 para que ASTRA/CLAUDE/GROK continúen sin pisarse.

## Estado base
- Método único: 3 pasos.
- Paso 1 inventario/arquitectura: documentado.
- Paso 2 adquisición: activo con GAPs.
- Paso 3 integración: `BLOCKED` hasta M06+M07+M08 + gate director.
- Catálogo: 117 total = 77 legacy + 40 nuevos.
- Nuevos B01–B04: 17 VERIFIED_CLOSED / 23 FAILED / 0 pending.
- Watchdog: `Sharck Input V2 Watchdog`, hourly, enabled.

## M21 — B04 exact X-Ray
Evidence: `📂 Craxy wall bitácora stated JSON/B04-XRAY-2026-09-11.md`.
- `spaCy`: partial exacto; faltan sólo `spacy/matcher/polyleven.c` y `website/.vscode/extensions.json`; 0 changed/0 extra. Runs 34566821665 + 34566985338.
- `huggingface_hub`: `CLAUDE.md` special; Git mode 120000 confirmado.
- `unstructured`: special paths concentrados en performance fixtures; symlink evidence confirmada.

## M22 — 11 partials B01–B03 exact diff
Evidence: `📂 Craxy wall bitácora stated JSON/PARTIALS-XRAY-11-2026-09-11.md`.
Run: `34567075204`, jobs 11/11 diagnostic success.
Agregado: 130 missing + 7 changed + 0 extra.
Prioridad:
1. sqry — 21 missing core `graph/unified/build`.
2. OpenSearch — 4 missing + 7 changed license/notice files.
3. heritrix3 — 57 missing under `dist/`.
4. yacy_search_server — 5 missing incl. Java source.
5. nutch — 3 missing incl. `conf/log4j2.xml`.
6. kythe — 14 missing build/source/proto/test artifacts.
7. scira — 12 missing SQL/migrations.
8. continue — 5 missing incl. runtime webview resource.
9. datasketch — 5 benchmark PNGs.
10. smolagents — 1 test PNG.
11. pyserini — 3 `.gitkeep`.

## M23 — 9 source-special B01–B03 mapped
Evidence: `📂 Craxy wall bitácora stated JSON/SPECIAL-FILES-XRAY-9-2026-09-11.md`.
- B01: stormcrawler, tika, docling.
- B02: vespa, networkx.
- B03: cocoindex, pydantic-ai, litellm, fastmcp.
No motor changes. StrategyDelta must prefer official package/subtree/reference where appropriate rather than weakening special-file safety.

## Owner entry points
### ASTRA / M06
Read the three evidence files above. Audit whether each StrategyDelta preserves PRE-LLM scope, fail-closed gates, modular adapters/plugins and versioned rollback. Output `REVIEW_PASS` or `REPAIR_REQUIRED`; no global PASS.

### CLAUDE / M07
Classify each partial as runtime-critical / build-critical / test-only / docs-only / metadata-only. Propose minimal canonical repair or clean versioned reacquisition; define tests/read-back. Pay special attention to sqry, OpenSearch, Nutch, YaCy, Kythe, spaCy.

### GROK / M08
For the 9 special-source components plus huggingface_hub/unstructured B04, verify official package/subtree/API alternatives, maintenance/license/source refs and contradictions. Do not auto-install.

### SOL
Maintain STATE/CHECKPOINT/Handoff, monitor owners, keep evidence/read-only diagnostics moving; no physical repair before reviews/gate.

## Current checkpoint
`CP-V2-EXACT-GAP-XRAY-011`
Resume: `M06_M07_M08_REVIEW_AND_GAP_STRATEGY_WITH_EXACT_XRAY_EVIDENCE`.

## Anti-collision
`FETCH STATE → verify owner → claim own log → execute own scope → evidence → checkpoint`.
Shared files are sequential writes with fresh SHA. Logs remain per-agent.
