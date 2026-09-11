# NESTED IGNORE BLAST RADIUS — 2026-09-11

Estado: `VERIFIED_READ_ONLY / NO_PHYSICAL_REPAIR / FAIL_CLOSED`.

## Objetivo
Extender M27 sin repetir M21/M22/M23 y resolver el residuo de `51/130` missing mediante reglas `.gitignore` ya presentes en el propio árbol publicado de Sharck Input V2.

## Fuentes de verdad
- `PARTIALS-XRAY-11-2026-09-11.md` — run `34567075204`, agregado `130 missing + 7 changed + 0 extra`.
- `ROOT-IGNORE-BLAST-RADIUS-2026-09-11.md` — mínimo previo `79/130` explicado por reglas root.
- `.gitignore` raíz del repo destino.
- `.gitignore` publicados dentro de los partials; no se consultó memoria suelta para clasificar los paths.
- Job read-only exacto de kythe `103161283044` para enumerar sus 14 missing.

## Resultado agregado
Los **130/130 missing** de M22 quedan cubiertos por una regla ignore concreta del repo destino o por una regla ignore importada/anidada dentro del snapshot upstream publicado.

Esto NO significa que los archivos sean prescindibles. Significa que la causa de desaparición durante re-vendoring/staging queda explicada sin atribuirla a descarga/extracción incompleta.

### 1. heritrix3 — 57/57
- Missing: todos bajo `dist/`.
- Regla causal: `.gitignore` raíz → `dist/`.

### 2. sqry — 21/21
- Missing: todos bajo `sqry-core/src/graph/unified/build/`.
- Regla causal: `.gitignore` raíz → `build/`.

### 3. scira — 12/12
- Missing: `create_indexes.sql`, `reindex_tables.sql` y migraciones SQL.
- Regla causal en `scira/code/.gitignore` → `*.sql`.

### 4. nutch — 3/3
- `conf/log4j2.xml` → `conf/*.xml`.
- `ivy/dependency-check-ant/dependency-check-suppressions.xml` → `ivy/dependency-check-ant/*`.
- `ivy/dependency-check-ant/lib/.gitignore` → el mismo subtree ignorado `ivy/dependency-check-ant/*`.

### 5. yacy_search_server — 5/5
- `.env` → `.gitignore` raíz `.env`.
- `.classpath` → YaCy `.gitignore` `.classpath`.
- `.project` → YaCy `.gitignore` `.project`.
- `lib/.gitignore` → YaCy `.gitignore` `/lib`.
- `source/net/yacy/peers/operation/yacyBuildProperties.java` → `.gitignore` anidado en ese directorio contiene literalmente `yacyBuildProperties.java`.

### 6. pyserini — 3/3
- `collections/.gitkeep` → `collections/*`.
- `indexes/.gitkeep` → `indexes/*`.
- `logs/.gitkeep` → `logs/`.

### 7. OpenSearch — 4/4 missing
- Los cuatro paths faltantes están bajo `.idea/`.
- `OpenSearch/code/.gitignore` ignora `.idea/` y contiene negaciones para esos archivos. Al re-vendorizar como archivos nuevos, el parent ignorado sigue siendo una colisión de staging y los tracked-upstream históricos no se preservan automáticamente.
- Los **7 changed** permanecen fuera de este conteo; M24 ya los probó como `CRLF → LF` por attributes.

### 8. datasketch — 5/5
- Los cinco PNG faltantes están bajo `benchmark/.../plots/`.
- Regla causal: `benchmark/**/*.png`.

### 9. smolagents — 1/1
- Missing: `tests/data/000000039769.png`.
- Regla causal: `data` / `data/` en `smolagents/code/.gitignore` cubre el directorio `tests/data`.

### 10. kythe — 14/14
Job exacto: `103161283044`.
- 6 paths contienen directorio `build/`:
  - `kythe/go/util/build/BUILD`
  - `kythe/go/util/build/build.go`
  - cuatro paths `third_party/bazel/.../build/lib/...`
  - Regla causal: `.gitignore` raíz → `build/`.
- 3 `*.class` → regla kythe `*.class`.
- 3 `.vscode/{launch,settings,tasks}.json` → regla kythe `.vscode`.
- 2 `third_party/libmemcached/{BUILD,COPYING}` → regla kythe `third_party/libmemcached`.

### 11. continue — 5/5
- Cuatro IntelliJ `*.iml` → regla `*.iml` en `continue/code/.gitignore`.
- `extensions/intellij/src/main/resources/webview/index.html` → `.gitignore` anidado de `extensions/intellij` ignora `src/main/resources/webview`; aunque existe negación para `index.html`, el parent directory ignorado crea la misma clase de colisión al re-agregar tracked-upstream como vendor nuevo.

## Cuantificación final
- Missing M22: **130**.
- Missing con regla ignore exacta identificada: **130/130 = 100%**.
- Changed M22: **7/7**, tratados separadamente por M24 como `CRLF → LF` inducido por attributes.
- Extra: **0**.

Por tanto, para los 11 partials de M22, la evidencia disponible ya explica **137/137 anomalías de path/contenido** como efectos de staging Git (`ignore rules` + `attributes`), no como fallo demostrado de descarga/extracción.

## Implicación para M06/M07/M08
- M06/ASTRA: validar que una StrategyDelta preserve fail-closed y no convierta ignores/special-files en bypass global.
- M07/CLAUDE: el repair/staging propuesto debe preservar el tracked set upstream y bytes/modes sin depender de `git add` semántico sobre ignores/attributes.
- M08/GROK: este hallazgo no resuelve los 9 source-special ni los symlink gaps B04; package/subtree/API alternatives siguen revisión separada.

## Gate
`NO_PHYSICAL_REPAIR / NO_SOURCE_REF_REDESIGN / STEP3_BLOCKED` hasta M06+M07+M08 + gate director.

No se modificaron componentes, motores, source refs ni destinos parciales en M28.