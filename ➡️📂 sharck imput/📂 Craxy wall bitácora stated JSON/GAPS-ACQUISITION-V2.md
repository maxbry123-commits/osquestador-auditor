# 🦈 GAPS — ADQUISICIÓN V2

Estado: `ACTIVE_LOOP / FAIL_CLOSED`.

## Balance comprobado parcial
- B01: 3 VERIFIED_CLOSED / 7 FAILED / 0 pending en su motor.
- B02: 5 VERIFIED_CLOSED / 5 FAILED / 0 pending en su motor.
- B03: motor todavía IN_PROGRESS al crear este ledger.
- Total comprobado de B01+B02: 8 VERIFIED_CLOSED + 12 FAILED.

## Clases de GAP observadas
### G1 DESTINATION_EXISTS
El retry encuentra un destino ya creado por un intento anterior. No borrar ni reemplazar automáticamente. Primero inventariar/read-back y decidir si es una publicación parcial, completa-no-reconciliada o colisión real.

### G2 READBACK_TREE_HASH_GAP
La publicación llegó a crear contenido/commit, pero el árbol releído no coincide con el tree hash esperado. Nunca promover como VERIFIED_CLOSED. Inspeccionar manifest, commit fuente, árbol remoto y concurrencia antes de decidir.

### G3 SOURCE_SPECIAL_FILE_GAP
El source contiene symlink u otro special file rechazado por el motor canónico. Es un rechazo de seguridad válido; no parchear el motor para aceptarlo.

## StrategyDelta — hasta 20 vías, ordenadas por menor riesgo
1. Releer destino existente y su `DOWNLOAD_EXTRACT_MANIFEST.json` antes de cualquier retry.
2. Comparar source commit del intento con el commit/material publicado y clasificar partial vs complete.
3. Si existe copia idéntica verificada en otra raíz del repo, reutilizarla con motor canónico de copia en vez de descargar otra vez.
4. Buscar el mismo componente ya presente/VERIFIED_CLOSED en V1 antes de nueva adquisición.
5. Pinnear `source_ref` a SHA/tag exacto en vez de `HEAD` para reproducibilidad.
6. Reintentar 1×1, no en matrix concurrente, cuando el fallo pueda relacionarse con concurrencia de pushes/read-back.
7. Crear destino versionado nuevo sólo después de preservar/documentar el destino fallido; no sobrescribir silenciosamente.
8. Separar cada componente conflictivo en job propio con state/checkpoint propio.
9. Para `READBACK_TREE_HASH_GAP`, comparar manifest remoto y conteo de archivos antes de repetir adquisición.
10. Revisar si el componente genera/modifica archivos durante checkout/build; el motor sólo debe copiar source estático.
11. Revisar `.gitattributes`/filtros que puedan alterar bytes y documentar el efecto; no desactivar controles a ciegas.
12. Revisar tamaño/blob limits y partes ZIP aunque el error final sea distinto, para descartar corrupción previa.
13. Para special files, probar un `source_ref` estable/tag donde el árbol sea compatible, si existe y mantiene la funcionalidad requerida.
14. Buscar una distribución/source snapshot oficial equivalente que ya exista físicamente en una fuente autorizada y pueda pasar por los motores existentes; no inventar downloader.
15. Si el repo completo es incompatible por symlinks, buscar un subproyecto/repositorio oficial equivalente que contenga sólo la capacidad necesaria.
16. Sustituir componente por alternativa OSS funcionalmente equivalente que pase los gates, preservando el candidato fallido en el índice como `REJECTED_BY_ACQUISITION_GATE`.
17. Priorizar componentes pequeños/maduros para construir el primer vertical slice y aplazar gigantes que no sean indispensables.
18. Para herramientas que sólo se necesitan por API/MCP, evaluar si basta referencia/adapter sin importar todo el source al runtime; requiere review arquitectónica.
19. Para bibliotecas que ya pueden consumirse como dependencia versionada, evaluar pointer/lockfile en vez de vendorizar todo el repo; requiere review y no sustituye evidencia de origen.
20. Si ninguna vía compatible con el skill resuelve el componente, mantener GAP abierto y escalar sólo la decisión arquitectónica al review gate; nunca alterar el motor para forzar PASS.

## Reglas de ejecución
- Estrategias 1–12 pueden investigarse sin modificar motores; cualquier escritura sigue usando motores canónicos.
- Estrategias 13–19 cambian fuente/ref/diseño y deben ser revisadas por ASTRA/CLAUDE/GROK antes de promoción.
- Estrategia 20 mantiene el GAP visible.
- Ninguna StrategyDelta autoriza borrar evidencia, force push, LFS o editar motores.

## Review solicitado
ASTRA: validar que estas StrategyDelta no degraden arquitectura/seguridad.
CLAUDE: validar causas técnicas de hash/collisions/special files y proponer verifier/adapter sólo si hace falta.
GROK: buscar alternativas OSS/source refs oficiales para componentes incompatibles.
