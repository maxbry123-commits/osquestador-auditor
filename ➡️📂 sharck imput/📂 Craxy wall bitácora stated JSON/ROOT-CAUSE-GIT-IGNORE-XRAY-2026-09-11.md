# ROOT CAUSE X-RAY — GITIGNORE / GITATTRIBUTES — 2026-09-11

Estado: `ROOT_CAUSE_CONFIRMED / EXCEPTIONS_CLOSED / NO_MOTOR_EDIT / NO_PHYSICAL_REPAIR`.

## Evidencia primaria
- Motor canónico: `hf_download_extract_engine.py`, blob `91e6e4486692eab314be5c7130d8310d3c855397`.
- El motor copia `extracted/` al destino y luego ejecuta `git add --sparse -- <rel>` sin `-f`.
- Después hace push + read-back y compara `tree_hash`, por lo que detecta correctamente cualquier archivo omitido o transformado.
- Root `.gitignore` del repo destino incluye `.env`, `dist/`, `build/` y otros patrones.
- FAST ignore/attr X-Ray workflow: `.github/workflows/sharck-input-ignore-attr-xray-fast.yml`.
- Workflow commit: `92a5c581433f53db8978296adb9f705f6833ef58`.
- Run: `34567757437`; job `103163258640`; conclusion=`success`.

## Reglas confirmadas por `git check-ignore -v --no-index`
1. `scira/create_indexes.sql` + migration SQL → `scira/code/.gitignore: *.sql`.
2. `nutch/conf/log4j2.xml` → `nutch/code/.gitignore: conf/*.xml`.
3. `yacy_search_server/.env` → repo destino root `.gitignore: .env`.
4. `heritrix3/dist/pom.xml` → repo destino root `.gitignore: dist/`.
5. `pyserini/collections/.gitkeep` → `pyserini/code/.gitignore: collections/*`.
6. `OpenSearch/.idea/icon.svg` → `OpenSearch/code/.gitignore: .idea/`.
7. `datasketch/.../jaccard_distances_at_k.png` → `datasketch/code/.gitignore: benchmark/**/*.png`.
8. `smolagents/tests/data/000000039769.png` → `smolagents/code/.gitignore: data/`.
9. `kythe/.../build/build.go` → repo destino root `.gitignore: build/`.
10. `sqry/.../build/entrypoint.rs` → repo destino root `.gitignore: build/`.
11. `continue/.idea/continue.iml` → `continue/code/.gitignore: *.iml`.
12. `spaCy/spacy/matcher/polyleven.c` → `spaCy/code/.gitignore: *.c`.
13. `spaCy/website/.vscode/extensions.json` → `spaCy/code/.gitignore: .vscode`.

## Excepciones iniciales — CERRADAS
Workflow: `.github/workflows/sharck-input-exception-eol-xray.yml`.
Commit: `88027e8921b68a9ebbbb15ba90751278cf6bdf82`.
Run: `34567916375`.

### YaCy `yacyBuildProperties.java`
- `git ls-files -s` confirma que está TRACKED upstream, mode `100644`, blob `0da296595a4d1ca649429ba2186e6643b13e9772`.
- `.gitignore` anidado `source/net/yacy/peers/operation/.gitignore` contiene `yacyBuildProperties.java`.
- `git check-ignore --no-index` confirma esa regla como causa.
- Veredicto: `TRACKED_UPSTREAM_BUT_REIGNORED_ON_VENDOR_PUBLISH`.

### Continue `webview/index.html`
- `git ls-files -s` confirma TRACKED upstream, mode `100644`, blob `be67d62c93cf6cab4763d2fa1a67529c1c2085fc`.
- `extensions/intellij/.gitignore` excluye `src/main/resources/webview`; aunque contiene una negación posterior para `index.html`, Git no re-incluye correctamente el archivo cuando el directorio padre ya está excluido en este contexto de nuevo vendor tree.
- `git check-ignore --no-index` devuelve la regla de exclusión del directorio.
- Veredicto: `TRACKED_UPSTREAM_BUT_REIGNORED_ON_VENDOR_PUBLISH`.

## OpenSearch — EOL CAUSALIDAD PROBADA
El mismo run `34567916375`, job `opensearch-eol`, comparó byte a byte los 7 LICENSE/NOTICE con hash distinto.

Resultado global: `all_crlf_to_lf_only=true`.
Para los 7 archivos:
- source contiene CRLF;
- published contiene 0 CRLF;
- `source.replace(CRLF, LF) == published`;
- `SHA256(normalized_source) == SHA256(published)`.

Conteos de CRLF convertidos: 200, 5, 9, 1, 202, 17 y 202 respectivamente. Esto prueba que la única mutación de contenido observada fue normalización `CRLF → LF` inducida por atributos `text=auto` + `eol=lf` durante staging/commit.

Veredicto: `GITATTRIBUTES_EOL_NORMALIZATION_CONFIRMED`.

## Conclusión técnica
Los partials auditados no nacen de una descarga incompleta del source: el motor verificó `source_tree == extracted_tree` antes de publicar. La pérdida/mutación ocurre al convertir un árbol ya verificado en archivos nuevos dentro del repo destino:

1. `git add --sparse -- <rel>` vuelve a aplicar `.gitignore` del repo destino y de los repos importados, omitiendo archivos que sí estaban TRACKED upstream.
2. `.gitattributes` vuelve a aplicar filtros de normalización y puede cambiar bytes, como quedó demostrado en OpenSearch.
3. El read-back canónico funciona correctamente al detectar la divergencia y evita falso PASS.

## Restricciones
- NO editar motor canónico.
- NO usar `git add -f` dentro del motor sin autorización explícita + review.
- NO reparar partials a ciegas.
- NO debilitar special-file/LFS/blob gates.
- StrategyDelta debe preservar source SHA, historial, no-overwrite y read-back.

## StrategyDelta para M06/M07/M08
- ASTRA/M06: revisar una capa/adaptador de publicación versionada que preserve exactamente el conjunto TRACKED upstream sin debilitar gates.
- CLAUDE/M07: diseñar test `tracked_upstream_set == published_set` + `upstream_bytes == published_bytes`, y una vía de staging que no vuelva a interpretar `.gitignore/.gitattributes` del vendor snapshot.
- GROK/M08: validar patrón Git/archive/subtree/package oficial para transportar snapshot exacto sin reactivar symlinks ni special files.
- SOL: conservar evidencia y preparar opciones usando sólo motores canónicos/bridges autorizados hasta gate.
