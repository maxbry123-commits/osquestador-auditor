# PARTIALS X-RAY 11 — 2026-09-11

Estado: `VERIFIED_READ_ONLY_DIAGNOSIS / NO_PHYSICAL_REPAIR / FAIL_CLOSED`.

## Evidencia
- Workflow: `.github/workflows/sharck-input-v2-partials-diff.yml`
- Workflow commit: `e782e7d87a3ef53f8edc110d781a9866ca645f15`
- Run: `34567075204`
- Jobs: 11/11 completed `success` as read-only diagnostic jobs.
- Cada job comparó el `source_commit` exacto del `DOWNLOAD_EXTRACT_MANIFEST.json` contra el árbol publicado bajo `code/`.
- No hubo write físico a componentes.

## Balance agregado
- Destinos auditados: 11.
- Missing files: **130**.
- Changed files: **7**.
- Extra files: **0**.
- Componentes recuperados automáticamente: **0**.
- Los 11 siguen `PARTIAL_DESTINATION_READBACK_GAP` hasta StrategyDelta + repair + canonical read-back.

## B01 — web/research

### scira — job `103161282968`
- Source commit: `e1692f5bdec7ec3f6482a24e0c6cf9b483d810f9`.
- source=451, published=439.
- missing=12, changed=0, extra=0.
- Missing concentrados en SQL/migrations: `create_indexes.sql`, `reindex_tables.sql`, `drizzle/migrations/0000...0009`.
- Clase: `PARTIAL_CORE_DATA_SCHEMA`.

### nutch — job `103161283102`
- Source commit: `8006e1094e7442517a01a00a9035efe74379e7fd`.
- source=1126, published=1123.
- missing=3, changed=0, extra=0.
- Missing: `conf/log4j2.xml`, `ivy/dependency-check-ant/dependency-check-suppressions.xml`, `ivy/dependency-check-ant/lib/.gitignore`.
- Clase: `PARTIAL_CONFIG_AND_METADATA`; `conf/log4j2.xml` se considera potencialmente runtime-relevante.

### yacy_search_server — job `103161282836`
- Source commit: `e171a4a0e50e08a91f8bcae0a1854d12d895a28a`.
- source=2283, published=2278.
- missing=5, changed=0, extra=0.
- Missing: `.classpath`, `.env`, `.project`, `lib/.gitignore`, `source/net/yacy/peers/operation/yacyBuildProperties.java`.
- Clase: `PARTIAL_BUILD_AND_SOURCE`; `yacyBuildProperties.java` es código fuente y no se trivializa.

### heritrix3 — job `103161283085`
- Source commit: `0d3582a136f6c04999f830bf37b1108c6de35308`.
- source=1007, published=950.
- missing=57, changed=0, extra=0.
- Missing concentrados en `dist/`: `LICENSE.txt`, `pom.xml`, assembly descriptors, scripts/bin (`heritrix`, `extractor`, `arcreader`, cmd variants), configs, pagerank extras, third-party licenses/notices y un test Java.
- Clase: `PARTIAL_DISTRIBUTION_TREE_MAJOR`.

## B02 — IR/evidence

### pyserini — job `103161283057`
- Source commit: `b0ad28270848f9b34ca822827bf5f71717255e84`.
- source=761, published=758.
- missing=3, changed=0, extra=0.
- Missing: `collections/.gitkeep`, `indexes/.gitkeep`, `logs/.gitkeep`.
- Clase: `PARTIAL_EMPTY_DIR_SENTINELS`; funcionalidad probablemente intacta, pero no se promueve sin gate/read-back.

### OpenSearch — job `103161282994`
- Source commit: `0249cde03ef66b56ac61e8929c3ba7e10b062523`.
- source=19225, published=19221.
- missing=4, changed=7, extra=0.
- Missing: `.idea/icon.svg`, `.idea/inspectionProfiles/Project_Default.xml`, `.idea/runConfigurations/Debug_OpenSearch.xml`, `.idea/vcs.xml`.
- Changed: 7 archivos `LICENSE/NOTICE` bajo `plugins/ingest-attachment`, `plugins/repository-hdfs` y `server/licenses`.
- Clase: `PARTIAL_PLUS_CONTENT_MUTATION`; requiere diagnóstico de normalización/filtros antes de cualquier repair.

### datasketch — job `103161282958`
- Source commit: `ee60290e982be00b6f0a6aea8156e2be4d6921e6`.
- source=129, published=124.
- missing=5, changed=0, extra=0.
- Missing: 5 PNG bajo `benchmark/indexes/jaccard/plots/...`.
- Clase: `PARTIAL_BENCHMARK_ARTIFACTS`.

## B03 — code/runtime

### smolagents — job `103161283066`
- Source commit: `30bb1161095dbae2271e6bc3cc4c219cc3897a57`.
- source=185, published=184.
- missing=1, changed=0, extra=0.
- Missing: `tests/data/000000039769.png` (694498 bytes).
- Clase: `PARTIAL_TEST_FIXTURE`.

### kythe — job `103161283044`
- Source commit: `26056edfc953b5d4ea0ed8e94db072caa7f7d4c7`.
- source=2407, published=2393.
- missing=14, changed=0, extra=0.
- Incluye `kythe/go/util/build/BUILD`, `kythe/go/util/build/build.go`, 3 `.class` de test, VSCode configs, Bazel BUILD/protos y third-party license/build files.
- Clase: `PARTIAL_BUILD_CODE_AND_TEST_ARTIFACTS`.

### sqry — job `103161282985`
- Source commit: `631710ce145b6ef6adb527dda13ac60e20be16cf`.
- source=2817, published=2796.
- missing=21, changed=0, extra=0.
- Los 21 faltantes están en `sqry-core/src/graph/unified/build/`, incluyendo `entrypoint.rs`, `helper.rs`, `incremental.rs`, `parallel_commit.rs`, `pass5_cross_language.rs`, `pass_go_method_set.rs`, `staging.rs`, `unification.rs` y otros módulos de build.
- Clase: `PARTIAL_CORE_CODE_CRITICAL`.

### continue — job `103161283086`
- Source commit: `5522c6f44ca0ac3528b37244818fbfa39b5af470`.
- source=3058, published=3053.
- missing=5, changed=0, extra=0.
- Missing: 4 IntelliJ `.idea/*.iml` + `extensions/intellij/src/main/resources/webview/index.html`.
- Clase: `PARTIAL_IDE_AND_RUNTIME_RESOURCE`; `webview/index.html` requiere revisión funcional.

## Prioridad StrategyDelta
1. `sqry` — CRITICAL core code missing.
2. `OpenSearch` — content mutation + missing IDE metadata; investigar filtros/newlines antes de repair.
3. `heritrix3` — major distribution subtree missing.
4. `yacy_search_server` — source file missing.
5. `nutch` — runtime config missing.
6. `kythe` — build/source/proto/test artifacts missing.
7. `scira` — schema/migrations missing.
8. `continue` — runtime webview resource + IDE metadata.
9. `spaCy` (B04) — exact 2-file partial, tracked in `B04-XRAY-2026-09-11.md`.
10. `datasketch` — benchmark images only.
11. `smolagents` — test fixture only.
12. `pyserini` — empty-dir sentinel files only.

## Gates
- No componente se reclasifica por este diagnóstico.
- No blind retry.
- No borrar partial.
- No modificar motor canónico.
- Repair físico sólo después de revisión M06/M07/M08 según ownership y gate del director.
- Todo repair debe terminar con canonical read-back/hash antes de `VERIFIED_CLOSED`.
