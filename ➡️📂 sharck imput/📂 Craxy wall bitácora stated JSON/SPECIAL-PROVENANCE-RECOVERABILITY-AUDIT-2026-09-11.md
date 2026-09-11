# SPECIAL PROVENANCE RECOVERABILITY AUDIT — 2026-09-11

Estado: `VERIFIED_READ_ONLY / NO_PHYSICAL_MUTATION / FAIL_CLOSED`.

Nodo: `M33_SPECIAL_PROVENANCE_RECOVERABILITY_AUDIT`.

## Objetivo
Convertir el UNKNOWN abierto por M32 (`G-V2-SPECIAL-PROVENANCE-9`) en evidencia concreta sin repetir M21/M22/M23 y sin ejecutar adquisición/reparación física.

## Evidencia canónica inspeccionada
- `.github/workflows/sharck-input-v2-components.yml`
- `➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/📂Motor descarga de componentes y extracción de zip/motor_2_queue_download_extract.py`
- `➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/📂Motor descarga de componentes y extracción de zip/hf_download_extract_engine.py`
- queues B01/B02/B03
- run inicial `34514168678`, jobs B01/B02/B03

## FACT
1. El engine obtiene `src,commit=acquire(work)` antes de `scan_tree(src)`.
2. `scan_tree()` eleva `SOURCE_SPECIAL_FILE_GAP` antes de construir el manifest/result final.
3. El engine no imprime ni persiste `source_commit` entre `acquire()` y `scan_tree()`.
4. Motor 2 ejecuta el engine con stdout capturado; ante excepción guarda sólo el texto de error en el state row. El `result` sólo se asigna después de un `VERIFIED_CLOSED`.
5. El workflow ejecuta Motor 2 con `tee Bxx-motor-output.jsonl`, pero la fase `Persist state and index` sólo añade `STATE_FILE` e `INDEX_PATH`; no existe paso de upload-artifact ni commit del `*-motor-output.jsonl`.
6. Los tres jobs del run `34514168678` existen y cerraron `success` históricamente, pero su metadata sólo identifica el workflow head SHA, no los source commits de cada componente.
7. Los 9 componentes `SOURCE_SPECIAL_FILE_GAP` usan `source_ref:"HEAD"` en las queues B01/B02/B03: stormcrawler, tika, docling, vespa, networkx, cocoindex, pydantic-ai, litellm y fastmcp.
8. Por ser `HEAD`, el queue no contiene un SHA/tag inmutable desde el cual reconstruir con certeza el snapshot usado en el intento histórico.

## INFERENCE
- El `source_commit` histórico exacto de los 9 fallos special **no es recuperable de forma verificable desde el state/index/queue/workflow metadata persistidos actualmente**.
- Consultar HEAD actual del repo fuente sólo produciría un snapshot actual, no evidencia del snapshot histórico; no debe usarse para rellenar provenance retroactivamente.
- Una mejora futura de M07 puede persistir provenance inmediatamente después de `acquire()` y antes del scan fail-closed, pero eso requiere review M06/M07 y no se implementa aquí.

## UNKNOWN
- GitHub Actions logs crudos del paso de ejecución no están disponibles mediante la superficie de lectura utilizada en esta auditoría. Aun así, el código canónico no emite el commit antes del fallo y el workflow no persiste el archivo tee, por lo que no existe evidencia canónica actual que permita promover el commit histórico a FACT.

## Veredicto
`G-V2-SPECIAL-PROVENANCE-9 = CONFIRMED_NONRECOVERABLE_FROM_CURRENT_CANONICAL_PERSISTENCE`.

Esto NO cierra `G-V2-SPECIAL-9`, NO reclasifica los 9 componentes, NO autoriza source/ref redesign, NO modifica motores y NO desbloquea Step3.

Balance físico preservado: **17 VERIFIED_CLOSED / 23 FAILED / 0 pending**.
