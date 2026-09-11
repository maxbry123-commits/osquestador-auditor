# SPECIAL FILES STATE LEDGER AUDIT — 2026-09-11

Estado: `VERIFIED_READ_ONLY_LEDGER_CORRECTION / NO_PHYSICAL_REPAIR / FAIL_CLOSED`.

## Objetivo
Cerrar una incertidumbre documental de M23 usando exclusivamente los estados canónicos del proyecto `B01-state.json`, `B02-state.json` y `B03-state.json`. No se inspeccionaron repos externos, no se modificaron motores, source refs ni destinos.

## Hecho nuevo
`SPECIAL-FILES-XRAY-9-2026-09-11.md` mantiene correctamente 9 componentes con `SOURCE_SPECIAL_FILE_GAP`, pero su detalle de `docling` no coincide con el error canónico persistido en `B01-state.json`.

- M23 documentó para `docling` paths tipo `.agents/skills/cocoindex...` / `.claude/skills/...`.
- `B01-state.json` registra para `docling` exactamente 6 paths observados por `scan_tree()`:
  1. `.claude/skills/building-pydantic-ai-agents`
  2. `.claude/skills/dignified-python`
  3. `.codex/skills/building-pydantic-ai-agents`
  4. `.codex/skills/dignified-python`
  5. `.opencode/skills/building-pydantic-ai-agents`
  6. `.opencode/skills/dignified-python`
- Los 7 paths tipo cocoindex que M23 atribuyó a docling sí aparecen exactamente en `B03-state.json` bajo `cocoindex`:
  `.agents/skills/cocoindex`, `.agents/skills/cocoindex-diagrams`, `.agents/skills/target-connector`, `.agents/skills/upgrade-examples`, `.claude/skills/cocoindex-diagrams`, `.claude/skills/target-connector`, `.claude/skills/upgrade-examples`.

Conclusión: existe una **misatribución documental M23 docling↔cocoindex**. El estado operativo de ambos componentes permanece FAILED y no cambia por esta corrección.

## Ledger exacto observado desde estados canónicos
El motor lanza `SOURCE_SPECIAL_FILE_GAP:` con `','.join(special[:30])`; por ello una lista de 30 paths es un **mínimo observado**, no prueba de que sólo existan 30.

### B01
- `stormcrawler`: 2 paths observados.
  - `external/opensearch/dashboards`
  - `external/solr/archetype/src/main/resources/archetype-resources/configsets`
- `tika`: **>=30 paths observados**; el error persistido contiene exactamente los primeros 30 por el límite `special[:30]`.
- `docling`: 6 paths observados, listados arriba.

### B02
- `vespa`: 3 paths observados.
  - `fileacquirer/src/vespa/fileacquirer/filedistributorrpc.def`
  - `jrt_test/src/binref/progctl.sh`
  - `messagebus_test/src/binref/progctl.sh`
- `networkx`: 1 path observado.
  - `benchmarks/pyproject.toml`

### B03
- `cocoindex`: 7 paths observados.
- `pydantic-ai`: 15 paths observados.
- `litellm`: 1 path observado: `litellm/proxy/enterprise`.
- `fastmcp`: 2 paths observados: `.github/copilot-instructions.md`, `AGENTS.md`.

## Blast radius mínimo comprobado
- stormcrawler 2
- tika >=30
- docling 6
- vespa 3
- networkx 1
- cocoindex 7
- pydantic-ai 15
- litellm 1
- fastmcp 2

**Total mínimo observado: >=67 special entries en los 9 componentes.**

Esto NO equivale a 67 symlinks: el estado canónico sólo prueba que `scan_tree()` los clasificó como special. Determinar mode Git exacto de cada path sigue pendiente de evidencia específica y no se infiere aquí.

## Impacto sobre gates
- Componentes afectados: siguen 9 `SOURCE_SPECIAL_FILE_GAP` FAILED.
- No se reclasifica ningún componente.
- No se debilita `scan_tree()` ni el fail-closed especial.
- No se autoriza package/subtree/source-ref redesign.
- No se autoriza reparación física ni Step3.
- M06/M07/M08 mantienen ownership de review/implementación/alternativas.

## Clasificación
- FACT: los estados canónicos contienen los paths y conteos observados arriba.
- FACT: `scan_tree()` limita el error a `special[:30]`; por eso Tika es `>=30`, no `=30` demostrado.
- FACT: M23 contiene una misatribución documental de paths entre docling y cocoindex.
- INFERENCE: la corrección reduce riesgo de que M06/M07/M08 revisen una StrategyDelta contra el componente equivocado.
- UNKNOWN: Git mode/tipo exacto de cada special path que aún no tenga evidencia individual dentro del proyecto.

## Veredicto
`M30_SPECIAL_LEDGER_CONTRADICTION_VERIFIED_READ_ONLY`

No physical mutation. No PASS por presencia. Balance de adquisición permanece `17 VERIFIED_CLOSED / 23 FAILED / 0 pending`.
