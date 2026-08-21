# Método de trabajo

## Regla canónica de copia entre repositorios

Cualquier instancia debe leer y seguir:

1. `PIPELINE/00_METODO_TRABAJO_Y_ARQUITECTURA.md` — si existe en este repo.
2. `PIPELINE/56_METODO_COPY_MOVE_REUSE_INDEX.md`.
3. `PIPELINE/59_PATCH_GIT_01.md`.
4. `PIPELINE/58_CROSS_REPOSITORY_TRANSFER.md`.
5. `PIPELINE/57_MARKDOWN_TO_CODE_EXTRACTION.md`.
6. `PIPELINE/60_REUSE_FIRST.md`.

### Procedimiento exacto para copiar un archivo entre repositorios

1. Auditar primero el repositorio origen y el destino.
2. Identificar el archivo exacto por ruta y comprobar si ya existe en destino.
3. Si ya existe en destino: **NO borrar y NO reescribir**.
4. Si no existe: obtener del origen el blob/objeto Git original y su SHA.
5. Crear en destino la entrada del archivo en el árbol (`tree`) usando el blob correspondiente, manteniendo la ruta indicada.
6. Usar el árbol actual del destino como `base_tree`; no reemplazar el resto del repositorio.
7. Crear un commit con el nuevo árbol.
8. Actualizar la referencia de la rama destino al commit nuevo (push).
9. Verificar que el archivo existe en destino y comparar SHA/contenido con el origen.
10. Registrar el resultado en la bitácora antes de pasar al siguiente archivo.

### Reglas de seguridad

- **COPY-FIRST.**
- **Origen intacto.**
- **EXTRACT_LITERAL.** No resumir, reconstruir, corregir ni reescribir el contenido copiado.
- **LLM ≠ PASS.** La tarea solo se considera terminada después de la verificación en GitHub.
- **GitHub = verdad.**
- No usar Actions, issues ni workflows como mecanismo de copia cuando la operación puede hacerse directamente mediante Git blobs/trees.
- Para lotes, se pueden incluir varios archivos nuevos en un mismo `tree` y un mismo commit, siempre que ninguno existente sea sobrescrito.

Este procedimiento se basa en el modelo Git de GitHub: los archivos se almacenan como blobs; los trees relacionan rutas con blobs; después se crea un commit y se actualiza la referencia de la rama. 
