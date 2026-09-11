# HANDOFF DELTA — EXACT GAPS — 2026-09-11

Fuente de verdad: `maxbry123-commits/osquestador-auditor` → `main` → `➡️📂 sharck imput/`.

Este delta NO sustituye el Handoff maestro. Resume evidencia M21–M36 para que ASTRA/CLAUDE/GROK continúen sin pisarse.

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
Evidence primaria: `📂 Craxy wall bitácora stated JSON/SPECIAL-FILES-XRAY-9-2026-09-11.md`.
- B01: stormcrawler, tika, docling.
- B02: vespa, networkx.
- B03: cocoindex, pydantic-ai, litellm, fastmcp.
- El detalle de paths de `docling` en M23 queda corregido por M30; no usar ese detalle aislado para diseñar StrategyDelta.
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

## M26 — canonical motor integrity watch
Estado: `VERIFIED_READ_ONLY_NO_DRIFT`.
Referencia de hashes: `.github/workflows/sharck-input-v2-components.yml`.
Read-back directo de los seis motores canónicos en `main`:
- `motor_1_extract_only.py` = `a52d5dc0e6ff26f75d753b848dcc1a40c5dd4500`.
- `motor_2_queue_download_extract.py` = `84d566e2ee4e98e42eb3a864026d067d48caabd9`.
- `hf_download_extract_engine.py` = `91e6e4486692eab314be5c7130d8310d3c855397`.
- `motor_3_copy_batches.py` = `3689924361ce4a1a9fde4ae2b6f6009c37a6042d`.
- `motor_copy_root_to_repo.py` = `8281211da76db3080fe1f1ea38b3eb0c45d655cb`.
- `motor_4_move_batches.py` = `9a21facfe11327cf60a2afca8f415ad52f0ecbe5`.
Los seis coinciden exactamente con el lock canónico. No hubo edición, adquisición ni reparación física. Esta evidencia elimina `MOTOR_DRIFT` como causa nueva para el estado actual, pero no desbloquea producción ni Step3.

## M27 — root ignore blast radius cuantificado
Evidence: `📂 Craxy wall bitácora stated JSON/ROOT-IGNORE-BLAST-RADIUS-2026-09-11.md`.
Relectura read-only del run M22 `34567075204` + `.gitignore` raíz del repo destino:
- heritrix3: 57/57 missing bajo `dist/` → regla raíz `dist/`.
- sqry: 21/21 missing bajo `sqry-core/src/graph/unified/build/` → regla raíz `build/`.
- yacy_search_server: `.env` → regla raíz `.env`.
- mínimo directo probado por reglas root: **79/130 missing = 60.77%**.
- los 7/7 changed de OpenSearch permanecen separados y ya están probados como `CRLF → LF` por attributes.
Esto cuantifica el blast-radius del problema de staging; NO autoriza reparación física ni debilitar gates.

## M28 — root + imported/nested ignore blast radius completo
Evidence: `📂 Craxy wall bitácora stated JSON/NESTED-IGNORE-BLAST-RADIUS-2026-09-11.md`.
Read-only, sin repetir M21/M22/M23.
- **130/130 missing** de M22 quedan asociados a una regla `.gitignore` concreta del destino raíz o del snapshot upstream publicado.
- Breakdown exacto: heritrix3=57, sqry=21, scira=12, nutch=3, yacy_search_server=5, pyserini=3, OpenSearch=4, datasketch=5, smolagents=1, kythe=14, continue=5.
- Casos de cierre causal adicionales: scira `*.sql`; nutch `conf/*.xml` + `ivy/dependency-check-ant/*`; pyserini `collections/*`, `indexes/*`, `logs/`; datasketch `benchmark/**/*.png`; smolagents `data/`; kythe `build/`, `*.class`, `.vscode`, `third_party/libmemcached`; yacy `.classpath`, `.project`, `/lib` y `.gitignore` anidado que nombra literalmente `yacyBuildProperties.java`; continue `*.iml` y parent `src/main/resources/webview` ignorado en `.gitignore` anidado.
- OpenSearch: los 4 missing están bajo `.idea/`; el ignore parent y sus negaciones muestran la colisión de re-staging de tracked-upstream. Los 7 changed siguen separados y M24 ya los explicó como attributes `CRLF → LF`.
- Con M24+M28, **137/137 anomalías M22 = 130 missing + 7 changed** tienen causa de staging Git identificada (`ignore rules + attributes`).
- Esto NO reclasifica los 11 partials, NO prueba que los archivos sean prescindibles y NO autoriza reparación física.

## M29 — control-plane PLAN reconciliation
Estado: `VERIFIED_DOCUMENT_ONLY / NO_PHYSICAL_MUTATION`.
- `CHECKPOINT 015` marcaba explícitamente `PLAN rev9` como `STALE_TASK_LEDGER_BEYOND_M20` mientras STATE/Handoff ya registraban M21–M28.
- SOL reconcilió el ledger: `PLAN rev10` contiene M21–M29 y mantiene los mismos ownership locks y gates.
- `STATE rev18` registra M29 sin alterar adquisición, fuentes, motores ni destinos.
- Balance físico permanece **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.
- M06/M07/M08 siguen sin claim/review/verdict verificable en sus logs; no se infiere revisión externa.
- Este nodo corrige coherencia documental; NO autoriza StrategyDelta de producción, repair físico ni Step3.

## M30 — source-special state ledger contradiction audit
Evidence: `📂 Craxy wall bitácora stated JSON/SPECIAL-FILES-STATE-LEDGER-AUDIT-2026-09-11.md`.
Estado: `VERIFIED_READ_ONLY_LEDGER_CORRECTION / NO_PHYSICAL_MUTATION`.
- Se releyeron los errores persistidos en `B01-state.json`, `B02-state.json` y `B03-state.json`; no se usó evidencia externa ni se ejecutó adquisición.
- El detalle M23 de `docling` estaba mal atribuido: M23 le asignó 7 paths tipo cocoindex, pero el estado B01 registra 6 paths de skills bajo `.claude`, `.codex` y `.opencode`.
- Los 7 paths tipo cocoindex sí aparecen exactamente bajo `cocoindex` en B03.
- Blast-radius mínimo observado por `scan_tree()`: **>=67 special entries** en los 9 componentes: stormcrawler=2, tika>=30, docling=6, vespa=3, networkx=1, cocoindex=7, pydantic-ai=15, litellm=1, fastmcp=2.
- Tika permanece `>=30`, no `=30`, porque el motor persiste sólo `special[:30]` en el error.
- `special` NO se promueve automáticamente a `symlink`: Git mode exacto de cada path continúa UNKNOWN salvo donde ya exista evidencia individual.
- Los 9 componentes siguen FAILED; ningún gate cambia.

## M31 — control-plane reconciliation de M30
Estado: `VERIFIED_DOCUMENT_ONLY / NO_PHYSICAL_MUTATION`.
- El checkpoint 017 declaraba explícitamente `PLAN rev10` sincronizado sólo hasta M29 y M30 pendiente del próximo ledger reconciliation.
- SOL releyó los logs de ASTRA/CLAUDE/GROK: los tres continúan `READY_TO_JOIN`, sin claim ni verdict verificable.
- `PLAN rev11` incorpora M30 con su corrección docling/cocoindex y registra M31 sin alterar adquisición ni ownership.
- `STATE rev20` registra `M31_CONTROL_PLANE_PLAN_RECONCILED_M30`.
- Checkpoint de cierre M31: `CP-V2-CONTROL-PLANE-RECONCILED-018`.
- Balance físico permanece **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.
- Cero physical repair, source/ref redesign, motor mutation o integración Step3.

## M32 — special snapshot provenance GAP
Evidence: `📂 Craxy wall bitácora stated JSON/SPECIAL-FILES-PROVENANCE-GAP-2026-09-11.md`.
Estado: `SPECIAL_SNAPSHOT_PROVENANCE_GAP_VERIFIED_READ_ONLY / NO_PHYSICAL_MUTATION`.
- Los tracebacks canónicos de `SOURCE_SPECIAL_FILE_GAP` muestran que el motor ejecuta `src,commit=acquire(work)` y después entra en `scan_tree(src)`.
- `scan_tree()` eleva el error special antes de construir/persistir el bloque final `result`.
- Los state items FAILED conservan repo/slug/error/status, pero no `source_commit`; los VERIFIED_CLOSED sí conservan `source_commit`, `source_ref`, hashes y tree evidence.
- Consecuencia: el Git mode exacto del snapshot histórico de los 9 special-source no puede certificarse retrospectivamente desde B01/B02/B03 state files. HEAD actual no se usa como sustituto del snapshot histórico.
- GAP nuevo: `G-V2-SPECIAL-PROVENANCE-9`.
- StrategyDelta candidata para review M06/M07, no implementada: persistir provenance fail-closed inmediatamente después de `acquire(work)` y antes de `scan_tree(src)`, incluyendo al menos repo/ref/commit y evidencia de modes/special entries.
- No se editó el motor canónico, no se cambió source/ref y no se ejecutó reparación física.

## M33 — special provenance recoverability audit
Evidence: `📂 Craxy wall bitácora stated JSON/SPECIAL-PROVENANCE-RECOVERABILITY-AUDIT-2026-09-11.md`.
Estado: `VERIFIED_READ_ONLY / NO_PHYSICAL_MUTATION / FAIL_CLOSED`.
- Se inspeccionaron workflow canónico, Motor 2, HF engine, queues B01/B02/B03 y metadata del run inicial `34514168678`.
- El engine obtiene el commit antes de `scan_tree()`, pero no lo emite ni persiste antes del `SOURCE_SPECIAL_FILE_GAP`.
- Motor 2 sólo asigna `result` después de `VERIFIED_CLOSED`; ante fallo conserva texto de excepción, no el commit.
- El workflow hace `tee Bxx-motor-output.jsonl`, pero persiste únicamente STATE e INDEX; no existe upload-artifact/commit del output temporal.
- Los 9 special-source tienen `source_ref:"HEAD"`; queue no contiene SHA/tag inmutable para reconstrucción histórica.
- Resultado: `G-V2-SPECIAL-PROVENANCE-9 = CONFIRMED_NONRECOVERABLE_FROM_CURRENT_CANONICAL_PERSISTENCE`.
- No se usa HEAD actual como sustituto del snapshot histórico y no se modifica motor/source/ref.

## M34 — control-plane PLAN reconciliation de M32/M33
Estado: `VERIFIED_DOCUMENT_ONLY / NO_PHYSICAL_MUTATION`.
- `CHECKPOINT 020` declaraba explícitamente `PLAN rev11` sincronizado sólo hasta M31 mientras STATE/Handoff ya contenían M32/M33.
- Los logs ASTRA/CLAUDE/GROK fueron releídos y continúan `READY_TO_JOIN`, sin claim/review/verdict verificable.
- `PLAN rev12` incorpora M32, M33 y M34 sin alterar adquisición, source/ref, motores, ownership locks ni gates.
- `STATE rev23` registra `M34_CONTROL_PLANE_PLAN_RECONCILED_M32_M33`.
- Checkpoint de cierre: `CP-V2-CONTROL-PLANE-RECONCILED-021`.
- Balance físico permanece **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.
- Cero physical repair, source/ref redesign, motor mutation o integración Step3.

## M35 — StrategyDelta coverage audit
Evidence: `📂 Craxy wall bitácora stated JSON/STRATEGYDELTA-COVERAGE-AUDIT-2026-09-11.md`.
Estado: `VERIFIED_READ_ONLY / COVERAGE_GAP_IDENTIFIED / NO_PHYSICAL_MUTATION`.
- Universo partial diagnosticado: 11 partials B01–B03 + spaCy B04 = **12 componentes** y **139 anomalías exactas** (`137` M22 + `2` spaCy).
- M25 ejercitó directamente spaCy 2/2, sqry 1/21 y 1/7 changed de OpenSearch.
- Cobertura observable M25: **3/12 componentes = 25%** y **4/139 anomalías = 2.88%**.
- No se ejercitaron en M25 los árboles completos de heritrix3/yacy/nutch/kythe/scira/continue/datasketch/smolagents/pyserini, los 4 missing `.idea/*` de OpenSearch, los otros 6 changed LICENSE/NOTICE ni modes 100755 donde correspondan.
- GAP: `G-V2-STRATEGYDELTA-COVERAGE-12`.
- Conclusión: M25 conserva su valor como PASS representativo, pero NO es cobertura suficiente para autorización de producción. Source-special/symlink permanece fuera por diseño.

## M36 — control-plane PLAN reconciliation de M35
Estado: `VERIFIED_DOCUMENT_ONLY / NO_PHYSICAL_MUTATION`.
- `CHECKPOINT 022` declaraba `PLAN rev12` sincronizado sólo hasta M34 mientras M35 ya estaba en STATE/Handoff.
- Los logs ASTRA/CLAUDE/GROK fueron releídos: continúan `READY_TO_JOIN`, sin claim/review/verdict verificable.
- `PLAN rev13` incorpora M35 y M36 sin alterar adquisición, source/ref, motores, ownership locks ni gates.
- `STATE rev25` registra `M36_CONTROL_PLANE_PLAN_RECONCILED_M35`.
- Checkpoint de cierre: `CP-V2-CONTROL-PLANE-RECONCILED-023`.
- Balance físico permanece **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.
- Cero physical repair, source/ref redesign, motor mutation o integración Step3.

## Owner entry points actualizados
### ASTRA / M06
Auditar M24/M25/M27/M28/M35 y usar M30+M32+M33 para el ledger source-special: PRE-LLM scope, fail-closed, NO_LFS, blob/special-file gates, no-force, no-overwrite, rollback/versionado y read-back. Revisar si ampliar la StrategyDelta sandbox a árboles completos mantiene el fail-closed y si persistir provenance pre-scan mantiene special-files como bloqueo. Emitir `REVIEW_PASS` o `REPAIR_REQUIRED`; no PASS global.

### CLAUDE / M07
Validar `tracked_upstream_set == staged_set == published_set`, modos 100644/100755 y bytes completos por árbol/componente, no sólo por muestras M25. Para source-special, usar M30/M32/M33: el exact historical mode sigue UNKNOWN y M33 confirma que el source commit histórico no es recuperable desde la persistencia actual. Evaluar mejora versionada para provenance pre-scan y staging que preserve set/bytes/modes sin depender de `git add` semántico sujeto a ignores/filtros; tests/read-back completos obligatorios antes de repair.

### GROK / M08
Contrastar el patrón con vendoring/snapshot Git y alternativas package/subtree oficiales, especialmente para los 9 special-source + huggingface_hub/unstructured. Usar M30 como mapping corregido, M32/M33 como limitación de reproducibilidad histórica y M35 para impedir extrapolar el PASS M25 a clases no cubiertas. Verificar licencia/mantenimiento/source refs; no auto-instalar.

### SOL
Mantener STATE/CHECKPOINT/Handoff y monitor de owners/motores. Sólo nueva evidencia read-only o reconciliación de control plane; no physical repair ni Step3 antes de reviews + gate director. PLAN rev13 está sincronizado hasta M36; no redocumentar el mismo estado sin evidencia nueva.

## Current checkpoint
`CP-V2-CONTROL-PLANE-RECONCILED-023`
Resume: `M06_M07_M08_REVIEW_OF_ROOT_CAUSE_STAGING_COVERAGE_CORRECTED_SPECIAL_LEDGER_PROVENANCE_GAP_AND_M33_NONRECOVERABILITY`.
Balance permanece: **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.
`step3_allowed=false`; `physical_repair_allowed=false`.

## Anti-collision
`FETCH STATE → verify owner → claim own scope → execute only owned/parallel_safe node → evidence → checkpoint`.
Shared files: fresh SHA + sequential write + read-back. Logs separados por agente.