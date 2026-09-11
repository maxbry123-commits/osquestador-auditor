# STRATEGYDELTA COVERAGE AUDIT — 2026-09-11

Estado: `VERIFIED_READ_ONLY / COVERAGE_GAP_IDENTIFIED / NO_PHYSICAL_REPAIR / FAIL_CLOSED`.

## Objetivo
Cuantificar cuánto de los GAPs partial ya diagnosticados queda realmente ejercitado por M25, sin repetir M21/M22/M23 y sin ejecutar producción.

## Fuentes internas
- `PARTIALS-XRAY-11-2026-09-11.md`: 11 partials B01–B03, `130 missing + 7 changed + 0 extra`.
- `B04-XRAY-2026-09-11.md`: spaCy añade 2 missing exactos.
- `NESTED-IGNORE-BLAST-RADIUS-2026-09-11.md`: 130/130 missing M22 asociados a reglas ignore; 7/7 changed OpenSearch ya explicados por attributes.
- `STAGING-STRATEGYDELTA-SANDBOX-2026-09-11.md`: M25 sandbox sobre spaCy, sqry y OpenSearch.

## Cuantificación
Universo partial actualmente diagnosticado y potencialmente reparable por una StrategyDelta de staging:
- 11 componentes partial B01–B03 + spaCy B04 = **12 componentes**.
- Anomalías path/contenido exactas: M22 `137` + spaCy `2` = **139**.

M25 ejercitó directamente:
- spaCy: 2/2 paths missing.
- sqry: 1/21 paths missing (`entrypoint.rs`).
- OpenSearch: 1/7 paths changed (un LICENSE sample); no ejercitó sus 4 missing `.idea/*`.

Cobertura observable del sandbox actual:
- componentes partial tocados: **3/12 = 25%**;
- paths/anomalías directamente muestreados: **4/139 = 2.88%**.

## Lo que sigue no probado por M25
- Árbol completo de `sqry` (20 missing adicionales).
- Los 57 missing de `heritrix3`.
- `yacy_search_server`, `nutch`, `kythe`, `scira`, `continue`, `datasketch`, `smolagents`, `pyserini`.
- Los 4 missing `.idea/*` de OpenSearch y los otros 6 changed LICENSE/NOTICE.
- Modes 100755 donde existan ejecutables/scripts en los árboles partials.
- Invariante completa `tracked_upstream_set == staged_set == published_set` por componente.
- Los 9 source-special B01–B03 y los symlink gaps B04 quedan fuera por diseño y no deben forzarse con esta StrategyDelta.

## GAP nuevo/refinado
`G-V2-STRATEGYDELTA-COVERAGE-12` = el sandbox M25 prueba causalidad y viabilidad representativa, pero su cobertura actual es insuficiente para convertir el wrapper candidato en autorización de producción.

## Requisito de review
### ASTRA / M06
Confirmar que ampliar el sandbox a árboles completos no debilita special-file, NO_LFS, no-overwrite, rollback/versionado ni fail-closed.

### CLAUDE / M07
Exigir antes de producción una validación sandbox por componente/árbol que demuestre:
`tracked_upstream_set == staged_set == published_set`, bytes exactos y Git modes relevantes (100644/100755), con read-back completo.

### GROK / M08
Mantener package/subtree/API alternatives separadas para source-special/symlink; no extrapolar el PASS de staging a esas clases.

## Gate
`NO_PHYSICAL_REPAIR / NO_SOURCE_REF_REDESIGN / STEP3_BLOCKED` hasta M06+M07+M08 + gate director.

No se modificaron motores, componentes, source refs ni destinos parciales.