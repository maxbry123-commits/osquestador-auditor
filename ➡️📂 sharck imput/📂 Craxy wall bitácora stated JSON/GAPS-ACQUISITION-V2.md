# 🦈 GAPS — ADQUISICIÓN V2

Estado: `ACTIVE_LOOP / FAIL_CLOSED / REVIEW_REQUIRED`.

## Balance comprobado final del run inicial 34514168678
- B01: 3 VERIFIED_CLOSED / 7 FAILED / 0 pending.
- B02: 5 VERIFIED_CLOSED / 5 FAILED / 0 pending.
- B03: 2 VERIFIED_CLOSED / 8 FAILED / 0 pending.
- TOTAL: **10 VERIFIED_CLOSED / 20 FAILED / 0 pending**.

Los tres jobs del run inicial aparecieron `success` en GitHub porque Motor 2 imprime `GAPS_PENDING` pero no sale con código no-cero. Eso se clasifica como `WORKFLOW_FALSE_GREEN_GAP`; no se interpreta como 30/30.

## G4 WORKFLOW_FALSE_GREEN_GAP — CORREGIDO PARA FUTUROS RUNS
Workflow actualizado en commit `1bb43ca45bd548278cb2074cb563bd2ece0cab43` con un guard posterior que lee `STATE_FILE` y falla el job si no están todos los items en `VERIFIED_CLOSED`. Los motores canónicos no fueron editados. También se quitó el auto-trigger por editar el workflow para evitar retries destructivos/no deliberados.

## X-Ray exacto de los 20 FAILED
- 6 `DESTINATION_EXISTS`: scira, nutch, pyserini, OpenSearch, datasketch, smolagents.
- 5 `READBACK_TREE_HASH_GAP`: yacy_search_server, heritrix3, kythe, sqry, continue.
- 9 `SOURCE_SPECIAL_FILE_GAP`: stormcrawler, tika, docling, vespa, networkx, cocoindex, pydantic-ai, litellm, fastmcp.

### StrategyDelta read-only ejecutada
Se creó `.github/workflows/sharck-input-v2-readback-recover.yml` sin modificar motores ni componentes. Importa por referencia las funciones `sha256()` y `tree_hash()` del HF engine canónico blob `91e6e4486692eab314be5c7130d8310d3c855397`.

Runs de evidencia: `34535896880` y `34536177351`.

Se auditaron los 6 `DESTINATION_EXISTS` y los 5 `READBACK_TREE_HASH_GAP`: **0/11 recuperados**. Los 11 destinos existentes tienen manifiesto/code pero el árbol actual no coincide con `extracted_tree` por hash/conteo/bytes. Por tanto siguen FAILED; presencia física no equivale a PASS.

Detalle reproducible: `📂 Craxy wall bitácora stated JSON/READBACK-XRAY-2026-09-10.md`.

A partir de esta evidencia, conservar la causa inicial para provenance pero clasificar operacionalmente esos 11 como `PARTIAL_DESTINATION_READBACK_GAP` hasta reparación versionada.

## Clases de GAP observadas
### G1 DESTINATION_EXISTS → PARTIAL_DESTINATION_READBACK_GAP confirmado
Un retry encuentra destino creado por intento anterior. Read-back independiente demostró que los seis destinos iniciales de esta clase no son copias completas. No borrar/reemplazar automáticamente.

### G2 READBACK_TREE_HASH_GAP → PARTIAL_DESTINATION_READBACK_GAP confirmado
La publicación creó contenido/commit pero el árbol releído no coincide con el tree hash esperado. Los cinco fueron re-auditados y siguen incompletos.

### G3 SOURCE_SPECIAL_FILE_GAP
El source contiene symlink/archivo especial rechazado por el motor. El rechazo es un gate de seguridad válido; no parchear motor.

### G4 WORKFLOW_FALSE_GREEN_GAP
GitHub job-success no equivalía a batch-success. Corregido en wrapper para futuras ejecuciones; run inicial conserva su historia sin reescritura.

## StrategyDelta — 20 vías
1. Releer destino existente y `DOWNLOAD_EXTRACT_MANIFEST.json` antes de retry. **EJECUTADA para 11 destinos; 0/11 recuperados.**
2. Comparar source commit con material publicado; clasificar partial/complete/collision. **PARCIAL: 11 confirmados partial por manifest/tree.**
3. Reutilizar copia idéntica verificada existente mediante motor canónico de copia.
4. Buscar componente VERIFIED_CLOSED en V1 antes de nueva adquisición.
5. Pinnear `source_ref` a SHA/tag exacto.
6. Retry 1×1 cuando concurrencia pueda afectar push/read-back.
7. Crear destino versionado nuevo sólo preservando/documentando destino fallido.
8. Separar cada conflictivo en job/state/checkpoint propio.
9. Para hash gap, comparar manifest remoto + conteo + tree hash antes de retry. **EJECUTADA para 11; FAIL-CLOSED.**
10. Revisar si checkout/source cambia bytes durante adquisición.
11. Revisar `.gitattributes`/filtros; no desactivar controles a ciegas.
12. Descartar límites/blob/ZIP corruption con hashes y CRC existentes.
13. Probar tag/ref estable compatible con el gate de special files.
14. Usar snapshot/distribución oficial equivalente sólo si ya es fuente autorizada y puede entrar por motores canónicos.
15. Buscar subproyecto/repo oficial de la capacidad si el monorepo completo es incompatible.
16. Sustituir por alternativa OSS equivalente, dejando candidato fallido trazado.
17. Priorizar vertical slice con componentes ya verificados; aplazar gigantes no indispensables.
18. Si sólo se necesita API/MCP, evaluar adapter/reference en vez de vendorizar todo source, sujeto a review.
19. Si es biblioteca consumible por dependencia versionada, evaluar pointer/lockfile, sujeto a review.
20. Si no hay vía compatible, mantener GAP abierto; nunca modificar motor para forzar PASS.

## Próxima frontera segura
- Los 11 partial requieren decisión de reparación física: preservar/quarantine versionado + Motor4 + reacquisition 1×1 es candidato, no ejecutado todavía.
- Los 9 special-file requieren source/ref/subproject/dependency/alternative review.
- M06 ASTRA + M07 CLAUDE + M08 GROK deben revisar estas ramas antes de promoción o cambio de source/ref/diseño.

## Reglas
- No borrar evidencia, no force, no LFS, no editar motores.
- StrategyDelta que cambie source/ref/diseño requiere ASTRA/CLAUDE/GROK review antes de promoción.
- El watchdog puede investigar/registrar y ejecutar únicamente acciones ya permitidas por los contratos y gates.

## Review solicitado
ASTRA: seguridad/arquitectura/falsos PASS/StrategyDelta.
CLAUDE: diagnóstico técnico de collisions/hash/special files y contracts/adapters/tests.
GROK: alternativas OSS/source refs oficiales/licencias/mantenimiento/contradicciones.
