Sí. Pero aquí hay que distinguir dos situaciones, porque si el Markdown contiene código, no se debe simplemente renombrar .md → .py.

Caso 1 — El .md contiene código Python

Por ejemplo:

# Kernel

```python
def run():
    return True

El proceso correcto es:

```text
.md
 ↓
LEER
 ↓
IDENTIFICAR BLOQUES PYTHON
 ↓
EXTRAER CÓDIGO
 ↓
CREAR archivo .py
 ↓
VERIFICAR
 ↓
TEST
 ↓
COPY-FIRST hacia B

Es decir, se extrae el código del documento y se crea un .py nuevo a partir del código encontrado.

Eso no es reescribir el código, siempre que Grok copie literalmente los bloques de código y no los modifique.

---

Caso 2 — El Markdown contiene una implementación completa

Si tienes SALIDA_2_v2_A_nucleo.md y dentro hay varios archivos, Grok debe reconstruir el árbol extrayendo literalmente cada bloque.

MARKDOWN_TO_CODE EXTRACTION PROTOCOL

1. NO reescribir el código.
2. NO reinterpretar el código.
3. NO mejorarlo.
4. NO corregirlo automáticamente.
5. NO generar una implementación equivalente.

READ .md → IDENTIFY code blocks → IDENTIFY language → IDENTIFY path → EXTRACT literal → CREATE .py → VERIFY → TEST → COPY_FIRST → VERIFY destination → COMMIT → PUSH

CONTENT_POLICY: EXTRACT_LITERAL=REQUIRED REWRITE=DENY AUTO_FIX=DENY REFACTOR=DENY

Si no se puede determinar el archivo: STATUS=BLOCKED REQUIRED_ACTION=REQUEST_MAPPING

El .md original se conserva como provenance.

Canónico completo: https://github.com/maxbry123-commits/agentes/blob/main/PIPELINE/57_MARKDOWN_TO_CODE_EXTRACTION.md
