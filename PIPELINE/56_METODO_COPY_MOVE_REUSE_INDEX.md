# Método — COPY / MOVE / REUSE / EXTRACT

Fuente: input del operador 2026-08-19. Los archivos 57–60 son el texto original. No reescritos.

Leer en este orden:

1. `PIPELINE/59_PATCH_GIT_01.md`
2. `PIPELINE/58_CROSS_REPOSITORY_TRANSFER.md`
3. `PIPELINE/57_MARKDOWN_TO_CODE_EXTRACTION.md`
4. `PIPELINE/60_REUSE_FIRST.md`

Reglas cortas:

- REUSE → COPY_FIRST → MOVE_FIRST → ADAPT_EXISTING → GENERATE_LAST
- Entre repos: COPY_FIRST. Origen intacto. No `git mv` A→B.
- MOVE semántico = COPY → VERIFY → AUTHORIZE DELETE → DELETE origen.
- Si el código está en un `.md`: EXTRACT_LITERAL. No reimplementar.
- El `.md` no se borra. Es provenance.
- SOURCE_HASH = DESTINATION_HASH o COPY_INTEGRITY FAIL.
- Secretos: no copiar.

## Procedimiento operativo detallado — copia entre repositorios

1. Auditar origen y destino antes de cualquier escritura.
2. Identificar la ruta exacta y comprobar si ya existe en destino.
3. Si existe: no borrar y no sobrescribir.
4. Si no existe: obtener el blob original del origen y conservar su SHA.
5. En destino, usar el árbol actual como `base_tree`.
6. Añadir al `tree` únicamente las rutas nuevas, apuntando al blob correspondiente.
7. Crear el commit con ese tree.
8. Actualizar la referencia de la rama destino (push).
9. Hacer read-back desde GitHub y comparar SHA/contenido origen ↔ destino.
10. Registrar evidencia y continuar con el siguiente archivo.

Para lotes, varias rutas nuevas pueden entrar en un mismo tree y un solo commit. Nunca incluir una ruta existente si la regla es no reescribir.

## Reglas de integridad

- COPY-FIRST.
- Origen intacto.
- Copia literal; no resumir, reconstruir, traducir ni corregir.
- GitHub = fuente de verdad.
- La tarea no es DONE hasta SOURCE_HASH = DESTINATION_HASH para cada copia verificable.
- No usar Actions/issues/workflows como mecanismo de copia cuando la transferencia directa Git blob/tree es suficiente.

Hashes de los protocolos (origen local de esta publicación):

- 57: ecd9e8b21ed3ade18a9e8f3b2bdca1cfabecec7de4dd14dec20488c892974a82
- 58: 77eab1ea666849ca1f9f01b23f9128e7626bfbbe2ed157bfac0f56f389c9419f
- 59: 628727306165a74106f6f7532a089574ef4220d2c33b5d7be60244e0f387b5d0
- 60: 6087f799cec98bbf9619c6f069f61d2c660e6ebb52921677af413e1d80ca3879
