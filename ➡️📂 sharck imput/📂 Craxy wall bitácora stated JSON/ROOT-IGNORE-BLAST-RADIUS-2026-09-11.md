# ROOT IGNORE BLAST RADIUS — 2026-09-11

Estado: `VERIFIED_READ_ONLY / NO_PHYSICAL_REPAIR / FAIL_CLOSED`.

## Objetivo
Cuantificar cuánto del X-Ray M22 ya puede atribuirse **directamente** a reglas del `.gitignore` raíz del repositorio destino, sin repetir M21/M22/M23, sin editar motores y sin reparar componentes.

## Fuente de verdad
- `PARTIALS-XRAY-11-2026-09-11.md`: 11 partials, 130 missing + 7 changed + 0 extra; run `34567075204`.
- `ROOT-CAUSE-GIT-IGNORE-XRAY-2026-09-11.md`: causa raíz confirmada; `git add --sparse` reinterpreta ignores y attributes en staging.
- `.gitignore` de `maxbry123-commits/osquestador-auditor/main` contiene explícitamente: `.env`, `dist/`, `build/`.
- Logs read-only exactos del run `34567075204`.

## Evidencia exacta adicional
### heritrix3 — job `103161283085`
- missing_count = **57**.
- Los **57/57 paths** están bajo `dist/`.
- Regla causal del repo destino: root `.gitignore` → `dist/`.
- Conclusión: los 57 missing de heritrix3 quedan dentro del blast-radius directo de una regla root del repo destino.

### sqry — job `103161282985`
- missing_count = **21**.
- Los **21/21 paths** están bajo `sqry-core/src/graph/unified/build/`.
- Regla causal del repo destino: root `.gitignore` → `build/`.
- Conclusión: los 21 missing de sqry quedan dentro del blast-radius directo de una regla root del repo destino.

### yacy_search_server — job `103161282836`
- missing_count = **5**.
- Uno de los paths es `.env`.
- Regla causal del repo destino: root `.gitignore` → `.env`.
- Los otros cuatro paths conservan su evidencia M24 separada; este documento no los reclasifica por inferencia.

## Cuantificación mínima demostrada
- Missing M22 totales: **130**.
- Missing explicados directamente por root `.gitignore` con path exacto + regla exacta en esta ampliación: **79**.
  - heritrix3 `dist/`: 57.
  - sqry `build/`: 21.
  - yacy `.env`: 1.
- Cobertura mínima directa root-ignore: **79/130 = 60.77%**.
- Esto es un **mínimo probado**, no el total: M24 ya confirmó reglas importadas/anidadas adicionales para scira, nutch, pyserini, OpenSearch, datasketch, smolagents, kythe, continue y spaCy.

## Mutación de contenido separada
M24 ya probó que los **7/7 changed** de OpenSearch son exclusivamente normalización `CRLF → LF` inducida por attributes durante staging. No se mezclan con el conteo 79/130 de missing.

## Implicación para review — no autorización
La evidencia fortalece que el problema principal de los partials no es descarga/extracción sino la conversión de un source tree verificado a un vendor tree Git nuevo. La StrategyDelta debe evaluar el staging como una capa separada y preservar simultáneamente:
- `tracked_upstream_set == staged_set == published_set`;
- bytes y modos Git;
- NO_LFS / special-file gates;
- no-force / no silent overwrite;
- canonical read-back/hash fail-closed.

Este resultado **NO** autoriza `git add -f`, reparación física, cambio de source/ref ni Step3. M06/M07/M08 + gate director siguen obligatorios.
