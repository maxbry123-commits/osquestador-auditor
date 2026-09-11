# SOURCE SPECIAL X-RAY 9 — 2026-09-11

Estado: `CANONICAL_SCAN_EVIDENCE / NO_GATE_WEAKENING / NO_PHYSICAL_REPAIR`.

Fuente: `B01-state.json`, `B02-state.json`, `B03-state.json` generados por Motor 2 + HF engine canónico. `scan_tree()` falla cerrado ante symlink o filesystem entry no regular/directorio. Este documento no asume que todos sean symlink hasta inspección Git-mode individual; registra exactamente los paths que el motor clasificó como special.

## B01

### stormcrawler
- Repo: https://github.com/apache/stormcrawler
- Paths special:
  - `external/opensearch/dashboards`
  - `external/solr/archetype/src/main/resources/archetype-resources/configsets`
- StrategyDelta a revisar: subproyecto/core oficial necesario para crawling sin vendorizar enlaces externos completos.

### tika
- Repo: https://github.com/apache/tika
- El motor reportó múltiples paths bajo `docs/modules/ROOT/examples/`, incluyendo ejemplos `claude-vlm-*`, `gemini-vlm-*`, `openai-vlm-*`, parser/pipes configs y otros JSON.
- StrategyDelta a revisar: adquirir/usar módulos runtime/parser requeridos, no la documentación enlazada si no es necesaria para Sharck Input.

### docling
- Repo: https://github.com/docling-project/docling
- Paths special bajo skills enlazadas:
  - `.agents/skills/cocoindex`
  - `.agents/skills/cocoindex-diagrams`
  - `.agents/skills/target-connector`
  - `.agents/skills/upgrade-examples`
  - `.claude/skills/cocoindex-diagrams`
  - `.claude/skills/target-connector`
  - `.claude/skills/upgrade-examples`
- StrategyDelta a revisar: core Docling/document parser separado de skills auxiliares enlazadas.

## B02

### vespa
- Repo: https://github.com/vespa-engine/vespa
- Paths special:
  - `fileacquirer/src/vespa/fileacquirer/filedistributorrpc.def`
  - `jrt_test/src/binref/progctl.sh`
  - `messagebus_test/src/binref/progctl.sh`
- StrategyDelta a revisar: SDK/client/query integration o subtree oficial necesario para retrieval, no vendorizar monorepo si no es imprescindible.

### networkx
- Repo: https://github.com/networkx/networkx
- Path special: `benchmarks/pyproject.toml`
- StrategyDelta a revisar: package/runtime NetworkX sin benchmark fixture especial; alto candidato a consumo por dependencia versionada.

## B03

### cocoindex
- Repo: https://github.com/cocoindex-io/cocoindex
- Paths special bajo `.agents/skills/` y `.claude/skills/`, incluyendo `cocoindex`, `cocoindex-diagrams`, `target-connector`, `upgrade-examples`.
- StrategyDelta a revisar: core/indexer separado de skills enlazadas.

### pydantic-ai
- Repo: https://github.com/pydantic/pydantic-ai
- Paths special reportados en `.claude/skills/...`, `.github/workflows/CLAUDE.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `docs/**/CLAUDE.md`, `pydantic_ai_slim/**/CLAUDE.md`, `tests/CLAUDE.md`.
- StrategyDelta a revisar: package `pydantic-ai`/`pydantic_ai_slim` consumido por dependencia o subtree oficial, sin material auxiliar enlazado.

### litellm
- Repo: https://github.com/BerriAI/litellm
- Path special: `litellm/proxy/enterprise`.
- StrategyDelta a revisar: core OSS/router sin enterprise-linked subtree.

### fastmcp
- Repo: https://github.com/PrefectHQ/fastmcp
- Paths special:
  - `.github/copilot-instructions.md`
  - `AGENTS.md`
- StrategyDelta a revisar: package/runtime FastMCP sin instrucciones enlazadas de desarrollo.

## Balance
- Componentes special B01-B03: **9**.
- B01=3, B02=2, B03=4.
- No se modifica motor ni se fuerza PASS.
- Ninguna StrategyDelta física se ejecuta antes de M06/M07/M08 + gate director.

## Ownership para revisión
- ASTRA/M06: verificar que subtrees/packages no debiliten seguridad/arquitectura ni cambien objetivo PRE-LLM.
- CLAUDE/M07: determinar package/subtree mínimo, interfaces/adapters y pruebas necesarias.
- GROK/M08: validar fuente oficial, mantenimiento, licencia, alternativas y si package/subtree es soportado oficialmente.
- SOL: conservar estado, evidence ledger y ejecutar sólo acciones aprobadas con motores/bridge permitidos.
