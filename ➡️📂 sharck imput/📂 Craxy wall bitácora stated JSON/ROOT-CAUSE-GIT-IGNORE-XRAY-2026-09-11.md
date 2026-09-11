# ROOT CAUSE X-RAY — GITIGNORE / GITATTRIBUTES — 2026-09-11

Estado: `ROOT_CAUSE_CONFIRMED_FOR_MAJORITY / TWO_EXCEPTIONS_OPEN / NO_MOTOR_EDIT / NO_PHYSICAL_REPAIR`.

## Evidencia primaria
- Motor canónico: `hf_download_extract_engine.py`, blob `91e6e4486692eab314be5c7130d8310d3c855397`.
- El motor copia `extracted/` al destino y luego ejecuta `git add --sparse -- <rel>` sin `-f`.
- Después hace push + read-back y compara `tree_hash`, por lo que detecta correctamente cualquier archivo omitido o transformado.
- Root `.gitignore` del repo destino incluye `.env`, `dist/`, `build/` y otros patrones.
- FAST X-Ray workflow: `.github/workflows/sharck-input-ignore-attr-xray-fast.yml`.
- Workflow commit: `92a5c581433f53db8978296adb9f705f6833ef58`.
- Run correcto: `34567757437`.
- Job: `103163258640`, conclusion=`success`.

## Reglas confirmadas por `git check-ignore -v --no-index`
1. `scira/create_indexes.sql` + migration SQL → `scira/code/.gitignore: *.sql`.
2. `nutch/conf/log4j2.xml` → `nutch/code/.gitignore: conf/*.xml`.
3. `yacy_search_server/.env` → repo destino root `.gitignore: .env`.
4. `heritrix3/dist/pom.xml` → repo destino root `.gitignore: dist/`.
5. `pyserini/collections/.gitkeep` → `pyserini/code/.gitignore: collections/*` (mismo mecanismo para indexes/logs).
6. `OpenSearch/.idea/icon.svg` → `OpenSearch/code/.gitignore: .idea/`.
7. `datasketch/.../jaccard_distances_at_k.png` → `datasketch/code/.gitignore: benchmark/**/*.png`.
8. `smolagents/tests/data/000000039769.png` → `smolagents/code/.gitignore: data/`.
9. `kythe/.../build/build.go` → repo destino root `.gitignore: build/`.
10. `sqry/.../build/entrypoint.rs` → repo destino root `.gitignore: build/`.
11. `continue/.idea/continue.iml` → `continue/code/.gitignore: *.iml`.
12. `spaCy/spacy/matcher/polyleven.c` → `spaCy/code/.gitignore: *.c`.
13. `spaCy/website/.vscode/extensions.json` → `spaCy/code/.gitignore: .vscode`.

## OpenSearch changed-content evidence
El mismo FAST X-Ray ejecutó `git check-attr -a` sobre los 7 LICENSE/NOTICE con hash distinto. Todos reciben:
- `text: auto`
- `eol: lf`
por `.gitattributes` de OpenSearch.

Esto es consistente con normalización de finales de línea durante `git add`, pero la equivalencia byte-a-byte CRLF→LF todavía se marca `TO_VERIFY`, no se declara causalidad final sin contar bytes/CRLF del source.

## Excepciones aún abiertas
El FAST X-Ray devolvió `NOT_IGNORED` para:
- `yacy_search_server/source/net/yacy/peers/operation/yacyBuildProperties.java`
- `continue/extensions/intellij/src/main/resources/webview/index.html`

No se agrupan falsamente bajo gitignore. Requieren X-Ray específico de path/index/publication.

## Conclusión técnica
La causa raíz principal de los partials no es una descarga incompleta del source: el source/extracted tree fue verificado antes de publicar. La pérdida ocurre al convertir el árbol copiado en archivos nuevos del repo destino, donde `git add` vuelve a aplicar reglas `.gitignore` del destino y de los repos importados. El read-back canónico detecta el resultado y evita falso PASS.

## Restricción
- NO editar motor canónico.
- NO usar `git add -f` dentro del motor sin autorización explícita y review; el motor permanece inmutable.
- NO reparar partials a ciegas.
- StrategyDelta debe preservar source SHA, historial, no-overwrite y read-back.

## StrategyDelta para M06/M07/M08
- ASTRA/M06: revisar una capa/adaptador de publicación versionada que preserve archivos TRACKED upstream sin debilitar special-file/LFS/blob gates.
- CLAUDE/M07: diseñar test de `tracked_upstream_set == published_set` y alternativa de staging/index que no dependa de `.gitignore` del contenido importado; revisar EOL OpenSearch.
- GROK/M08: buscar patrón oficial Git/subtree/archive/package para vendorizar snapshots tracked sin reactivar symlinks ni archivos especiales.
- SOL: sólo evidencia/control hasta gate.
