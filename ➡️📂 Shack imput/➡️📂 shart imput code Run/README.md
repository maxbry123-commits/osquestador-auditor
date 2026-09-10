# shart imput code Run — runtime de Wanted Shark

Este directorio contiene únicamente código propio/glue/configuración del proyecto. Los componentes OSS descargados viven fuera, en `../📂 Componentes para integración sharck imput/`.

## Core inicial
- `shark_input_lock.py`: preserva `INPUT_RAW` literal y genera SHA-256 + sidecar de IDs/URLs/versiones.
- `role_router.py`: router determinista multi-role inicial.
- `research_dispatch.py`: compila un plan usando input lock, roles y registries.
- `community_registry.json`: 63 fuentes comunitarias preestablecidas.
- `component_registry.json`: 77 componentes trazables.
- `queues/`: lanes de adquisición con destinos explícitos.
- `memoria búsqueda.md`: bitácora humana append-only.
- `tests/test_shark_core.py`: pruebas del Core.

## Interfaces futuras
- `focus_ai`: devuelve sólo JSON estructurado de hipótesis/preguntas.
- `code_pointer`: `search_symbol`, `read_symbol`, `references`, `callers`, `callees`.
- `skill_pointer`: `search_skill`, `read_skill`, `verify_skill`.
- `tool_finder`: `find_capability`, `rank_tools`, `inspect_permissions`.
- `evidence`: claims/sources/contradictions/coverage.
- `context_compiler`: paquete final pre-LLM.

## Regla de dependencia
Preferir punteros/ref e imports a copiar bloques gigantes de código al prompt. Todo repo externo debe quedar fijable por commit/ref y con procedencia verificable.
