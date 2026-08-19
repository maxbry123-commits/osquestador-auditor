Sí. Aquí hay que ser muy estricto, porque si Grok está trabajando sobre repositorios y código, “copiar” y “reescribir” no pueden significar lo mismo.

La regla que yo pondría es:

> Si el código ya existe y se ha decidido reutilizarlo, Grok NO debe regenerarlo. Debe trasladarlo mediante operaciones de Git que preserven el contenido y después verificar que el resultado es equivalente.



Y distinguir claramente COPY-FIRST, MOVE-FIRST, REUSE, ADAPT y GENERATE.

Te dejo el parche adicional:

PATCH-GIT-01

PROTOCOLO DE COPIA, MOVIMIENTO Y REUTILIZACIÓN DE CÓDIGO

Este parche complementa el método de trabajo.

Su finalidad es impedir que un agente reescriba código existente cuando la estrategia exige reutilizarlo.

---

1. REGLA SUPREMA

Cuando exista código funcional o reutilizable, está PROHIBIDO regenerarlo desde cero si la decisión es:

REUSE
COPY_FIRST
MOVE_FIRST
ADAPT_EXISTING

El agente debe trabajar sobre el código existente.

No debe:

- volver a escribirlo manualmente;
- reconstruirlo desde memoria;
- generar una "versión equivalente";
- cambiar nombres innecesariamente;
- reformatearlo masivamente;
- traducirlo a otro lenguaje;
- simplificarlo sin autorización;
- crear una implementación paralela.

Primero:

LOCATE
↓
READ
↓
COPY/MOVE
↓
VERIFY
↓
TEST
↓
ADAPT ONLY IF AUTHORIZED

---

2. MODOS DE REUTILIZACIÓN

Existen cinco modos.

COPY_FIRST

Copiar primero sin modificar el contenido.

SOURCE
↓
COPY
↓
VERIFY
↓
TEST
↓
ADAPT LATER IF NEEDED

Es el modo predeterminado cuando el código puede reutilizarse.

---

MOVE_FIRST

Mover el archivo o directorio conservando su contenido.

SOURCE
↓
MOVE
↓
VERIFY
↓
TEST

El objetivo es cambiar su ubicación, no reescribirlo.

---

REUSE

Utilizar el código existente tal como está.

No modificar salvo que exista una tarea específica.

---

ADAPT_EXISTING

Modificar código existente porque existe una incompatibilidad concreta.

Antes de modificar:

IDENTIFY
↓
DOCUMENT GAP
↓
CREATE TASK
↓
MODIFY
↓
TEST

---

GENERATE_LAST

Generar código nuevo solamente cuando:

1. no existe código reutilizable;
2. se verificó que no existe;
3. ADAPT_EXISTING no resuelve el problema;
4. existe autorización para generar una implementación nueva.

---

3. JERARQUÍA OBLIGATORIA

Siempre intentar en este orden:

REUSE
↓
COPY_FIRST
↓
MOVE_FIRST
↓
ADAPT_EXISTING
↓
GENERATE_LAST

No saltar directamente a GENERATE.

---

4. COPIAR UN ARCHIVO CON GIT

Para copiar un archivo dentro del mismo repositorio:

cp path/origen.py path/destino.py
git add path/origen.py path/destino.py
git diff --cached -- path/origen.py path/destino.py

Después verificar que ambos archivos son iguales:

cmp path/origen.py path/destino.py

o:

sha256sum path/origen.py path/destino.py

Los hashes deben coincidir antes de cualquier modificación.

---

5. COPIAR UN DIRECTORIO

Para COPY-FIRST:

cp -a path/origen/ path/destino/

Después:

diff -qr path/origen/ path/destino/

Si no existen diferencias:

COPY_VERIFY: PASS

Si existen diferencias:

COPY_VERIFY: FAIL

No continuar silenciosamente.

---

6. COPIAR ENTRE REPOSITORIOS

Nunca asumir que un "cp" entre carpetas locales significa que el repositorio remoto quedó actualizado.

Proceso:

SOURCE_REPO
↓
FETCH
↓
COPY
↓
DESTINATION_REPO
↓
VERIFY
↓
COMMIT
↓
PUSH
↓
VERIFY_REMOTE

Ejemplo:

git clone <SOURCE_REPO>
git clone <DESTINATION_REPO>
cp -a source/orchestrator destination/

Después:

diff -qr source/orchestrator destination/orchestrator

Antes de publicar.

---

7. MOVER UN ARCHIVO

Para mover dentro del mismo repositorio usar preferentemente:

git mv path/origen.py path/destino.py

Después:

git status
git diff --cached --summary
git diff --cached

Git debe reconocer el cambio como movimiento/renombrado cuando corresponda.

Importante:

"git mv" no significa que el contenido deba cambiar.

Primero mover.

Después verificar.

---

8. MOVER DIRECTORIOS

Ejemplo:

git mv orchestrator/ destino/orchestrator/

Después:

git status
git diff --cached --summary

Y comprobar el contenido.

No modificar simultáneamente decenas de archivos durante el movimiento salvo que exista una tarea específica.

---

9. COPIAR NO ES MOVER

COPY:

SOURCE permanece
DESTINATION aparece

MOVE:

SOURCE desaparece
DESTINATION aparece

Nunca ejecutar "git mv" cuando el objetivo es conservar el original.

Nunca ejecutar "cp" cuando el objetivo es eliminar el origen.

---

10. PROHIBICIÓN DE REESCRITURA

Cuando exista:

COPY_FIRST

está prohibido hacer:

GENERATE_NEW_VERSION
REIMPLEMENT
REWRITE_FROM_SCRATCH

Aunque el agente considere que puede hacerlo "mejor".

Primero debe preservar la implementación existente.

---

11. PROHIBICIÓN DE "MEJORAS AUTOMÁTICAS"

Durante COPY-FIRST o MOVE-FIRST NO realizar automáticamente:

- refactor;
- renombrado;
- limpieza;
- optimización;
- cambio de arquitectura;
- cambio de estilo;
- cambio de imports;
- actualización de APIs;
- cambio de dependencias;
- reorganización de módulos.

Si detecta una mejora:

IMPROVEMENT_FOUND
↓
CREATE_GAP_OR_PROPOSAL
↓
WAIT_FOR_DECISION

No ejecutarla dentro de la copia.

---

12. REGLA DE INTEGRIDAD

Después de COPY-FIRST:

SOURCE_HASH
=
DESTINATION_HASH

para cada archivo que deba permanecer idéntico.

Si no coincide:

COPY_INTEGRITY: FAIL

y detener el proceso.

---

13. CUANDO EL HASH NO PUEDE COMPARARSE

Si existen archivos donde el hash completo no puede coincidir por razones legítimas:

INTEGRITY_MODE: STRUCTURAL

comparar:

- nombres;
- cantidad de archivos;
- tamaños;
- estructura;
- contenido relevante;
- permisos cuando corresponda.

La excepción debe quedar registrada.

Nunca asumir que "seguramente es igual".

---

14. VERIFICACIÓN DE GIT

Antes de copiar:

git status --short

Registrar estado inicial.

Después:

git status --short
git diff --stat
git diff

El agente debe poder explicar exactamente qué cambió.

---

15. REGLA DE DIFF

Después de una operación de reutilización:

EXPECTED_CHANGE
vs
ACTUAL_CHANGE

Si el usuario pidió mover un archivo y aparecen modificaciones internas:

UNEXPECTED_CONTENT_CHANGE

Estado:

BLOCKED

No continuar hasta determinar el origen.

---

16. COMMIT

Un commit de COPY-FIRST debe representar la operación de reutilización.

Ejemplo:

git add .
git commit -m "chore: copy orchestrator components to destination"

No mezclar en ese commit:

- refactor;
- features nuevas;
- correcciones no relacionadas;
- cambios de arquitectura.

Una operación = una intención.

---

17. PUSH

Después del commit:

git push

Después verificar el remoto:

git status
git log -1 --oneline

Y comprobar que el commit remoto corresponde al esperado.

No declarar publicación exitosa solamente porque "git push" terminó sin error.

---

18. PROTOCOLO ENTRE DOS REPOSITORIOS

Cuando el código pase de:

REPOSITORY_A

a:

REPOSITORY_B

registrar:

TRANSFER_ID: X-001

SOURCE_REPOSITORY:
A

SOURCE_PATH:
orchestrator/

DESTINATION_REPOSITORY:
B

DESTINATION_PATH:
orchestrator/

METHOD:
COPY_FIRST

CONTENT_POLICY:
PRESERVE

SOURCE_COMMIT:
<sha>

DESTINATION_COMMIT:
<sha>

INTEGRITY_CHECK:
PASS/FAIL

TEST_RESULT:
PASS/FAIL

---

19. REGLA COPY-FIRST PARA EL PROYECTO

Cuando se detecte código existente en otro repositorio:

DISCOVER
↓
COMPARE
↓
SELECT
↓
COPY_FIRST
↓
VERIFY
↓
TEST
↓
PROMOTE

No:

DISCOVER
↓
ASK_LLM_TO_REWRITE

---

20. SI HAY CONFLICTO

Si el código existente no encaja exactamente:

NO reescribir inmediatamente.

Crear:

GAP

Ejemplo:

GAP-007

SOURCE:
orchestrator/kernel.py

TARGET:
wordflow/kernel.py

CONFLICT:
API_INCOMPATIBLE

CURRENT:
interface_v1

TARGET:
interface_v2

ACTION:
ADAPT_EXISTING

STATUS:
REQUIRES_DECISION

Después decidir si:

ADAPT

o:

GENERATE_LAST

---

21. REGLA DE PRESERVACIÓN

El archivo original es evidencia.

Durante una transferencia:

SOURCE = IMMUTABLE_REFERENCE

No modificar el origen mientras se está verificando la copia.

Si posteriormente se decide modificarlo, debe existir otra tarea.

---

22. REGLA PARA ARCHIVOS DE CONFIGURACIÓN

No copiar secretos.

Nunca copiar:

.env
tokens
PAT
private keys
credentials
secrets

salvo mediante el mecanismo de credenciales autorizado.

Los valores sensibles deben mantenerse mediante:

credential_ref
environment_secret
secret_manager

El código puede copiarse.

El secreto no.

---

23. REGLA PARA MEMORIA

La memoria tampoco debe duplicarse indiscriminadamente.

Antes de copiar:

CLASSIFY:
SOURCE_CODE
CONFIG
MEMORY
ARTIFACT
CACHE
SECRET

Después aplicar la política correspondiente.

---

24. MATRIZ OPERACIONAL

Situación| Acción
Código idéntico y reutilizable| REUSE
Código debe aparecer en otro lugar| COPY_FIRST
Código debe cambiar de ubicación| MOVE_FIRST
Código existe pero tiene incompatibilidad| ADAPT_EXISTING
No existe implementación| GENERATE_LAST
Hay duda| BLOCK / REQUEST_DECISION
Hay conflicto| GAP + DECISION_GATE
Hay secreto| NO COPY

---

25. PROHIBICIONES ABSOLUTAS

El agente tiene PROHIBIDO:

1. Reescribir código existente durante COPY_FIRST.
2. Regenerar código que ya existe sin justificarlo.
3. Hacer refactor durante una transferencia.
4. Cambiar arquitectura durante un movimiento.
5. Modificar el origen para facilitar una copia.
6. Mezclar features nuevas con una operación de traslado.
7. Ocultar diferencias de contenido.
8. Declarar una copia correcta sin validarla.
9. Declarar DONE sin evidencia.
10. Copiar secretos.
11. Hacer "force push" para resolver conflictos de transferencia.
12. Eliminar el origen cuando la operación era COPY.
13. Conservar el origen cuando la operación era MOVE.
14. Resolver automáticamente un conflicto de código reescribiendo.
15. Sustituir código existente por una implementación generada por LLM solamente porque parece mejor.

---

26. ORDEN OBLIGATORIO PARA CÓDIGO EXISTENTE

Siempre:

FIND
↓
READ
↓
UNDERSTAND
↓
COMPARE
↓
SELECT
↓
REUSE/COPY/MOVE
↓
VERIFY
↓
TEST
↓
ADAPT IF REQUIRED
↓
GENERATE ONLY IF NECESSARY

---

27. COMANDO OPERACIONAL DEL AGENTE

Cuando la estrategia sea COPY-FIRST, el agente debe declarar:

MODE: COPY_FIRST
CONTENT_POLICY: PRESERVE
REWRITE: DENY
REFACTOR: DENY
AUTO_IMPROVEMENT: DENY
SOURCE_MUTATION: DENY
VERIFY_AFTER_COPY: REQUIRED
TEST_AFTER_COPY: REQUIRED

Cuando sea MOVE-FIRST:

MODE: MOVE_FIRST
CONTENT_POLICY: PRESERVE
REWRITE: DENY
REFACTOR: DENY
SOURCE_DELETE: EXPECTED
VERIFY_AFTER_MOVE: REQUIRED

---

28. PRINCIPIO FINAL

El agente no debe demostrar que sabe programar escribiendo código nuevo.

Debe demostrar que sabe programar eligiendo correctamente entre reutilizar, copiar, mover, adaptar o generar.

La regla general es:

EXISTING CODE
      ↓
CAN REUSE?
   YES → REUSE
   NO
      ↓
CAN COPY?
   YES → COPY_FIRST
   NO
      ↓
CAN MOVE?
   YES → MOVE_FIRST
   NO
      ↓
CAN ADAPT?
   YES → ADAPT_EXISTING
   NO
      ↓
GENERATE_LAST

La generación desde cero es el último recurso, no el comportamiento predeterminado.

Sí, pero hay que corregir una parte importante de esa frase.

Veredicto

> “GitHub no hace git mv entre repos. Entre remotes eso es COPY + dejar el origen.”



Correcto si estás hablando de git mv como comando de Git. git mv opera sobre el árbol de trabajo/index de un repositorio local; no acepta “repo A → repo B” como una operación atómica. GitHub documenta el movimiento de archivos dentro de un repositorio, y git mv igualmente describe mover/renombrar dentro del repositorio. 

Pero:

NO es correcto decir que entre repositorios solo existe COPY.

Puedes hacer una migración/movimiento entre repositorios, incluso preservando historial, mediante otras operaciones Git. Eso es distinto de git mv. 

Para vuestro método, yo lo definiría así

MISMO REPOSITORIO
    ↓
git mv
    ↓
MOVE

Mientras que:

REPOSITORIO A
    ↓
REPOSITORIO B

no tiene un:

git mv A → B

atómico.

Para vuestro caso de COPY-FIRST, la política correcta es:

SOURCE REPO A
      │
      ├── código original
      │
      ▼
COPY / IMPORT
      │
      ▼
DESTINATION REPO B
      │
      ▼
VERIFY
      │
      ▼
COMMIT
      │
      ▼
PUSH

Y A permanece intacto.

Si después de verificar B se decide que A debe dejar de contener ese código, eso es otra operación explícita:

COPY
  ↓
VERIFY
  ↓
AUTHORIZE DELETE FROM A
  ↓
DELETE FROM A
  ↓
COMMIT A

No debe llamarse git mv A→B, porque técnicamente son operaciones sobre dos repositorios distintos.

Y esto es especialmente importante para Grok

Añadiría esta regla al parche:

CROSS_REPOSITORY_MOVE = NOT_ATOMIC_GIT_MV

IF SOURCE_REPOSITORY != DESTINATION_REPOSITORY:

    METHOD = CROSS_REPOSITORY_TRANSFER

    DEFAULT:
        COPY_FIRST
        PRESERVE_SOURCE = TRUE
        VERIFY_DESTINATION = REQUIRED

    NEVER:
        pretend_git_mv
        rewrite_existing_code
        delete_source_automatically

Y una distinción más:

COPY_FIRST
A → B
A permanece

vs.

TRANSFER/MOVE SEMÁNTICO
A → B
copiar/verificar
+
eliminar A posteriormente

Así Grok no confundirá el concepto lógico de “mover” con el comando técnico git mv.

Y si se necesita conservar el historial de los archivos al pasar de A a B, hay que usar un procedimiento específico de migración de historial; una simple copia hace que los archivos aparezcan como nuevos en B. 

Por tanto, para vuestro proyecto, la regla más segura es:

> **Entre repositorios: COPY-FIRST por defecto. Nunca borrar el origen automáticamente. Si se requiere un “MOVE” semántico, primero COPY → VERIFY → AUTHORIZATION → DELETE SOURCE. Nunca reescribir el código para realizar la transferencia.**

Sí. Te lo explico sin lenguaje técnico innecesario.

La solución

El problema es esta idea:

> git mv sirve para mover archivos dentro del mismo repositorio.



Si tienes:

REPO A
agentes/
  archivo.py

y quieres llevarlo a:

REPO B
osquestador-auditor-y-memoria-1/
  archivo.py

no existe un comando git mv que haga A → B.

La forma correcta para vuestro método es:

REPO A
  │
  │  1. LEER
  ▼
archivo original
  │
  │  2. COPIAR
  ▼
REPO B
  │
  │  3. COMPARAR
  ▼
¿es idéntico?
  │
  ├── NO → BLOQUEAR
  │
  └── SÍ
       │
       ▼
  4. PROBAR
       │
       ▼
  5. COMMIT + PUSH
       │
       ▼
  6. VERIFICAR B
       │
       ▼
  7. SOLO SI SE AUTORIZA
     eliminar de A

En otras palabras

Primero COPIA. Después comprueba. Después, si realmente quieres que desaparezca de A, lo borras.

No intentes hacer un supuesto git mv entre repositorios.


---

Instrucciones exactas para Grok

Dale estas instrucciones:

PROTOCOLO CROSS-REPOSITORY TRANSFER

OBJETIVO:
Transferir código desde REPO A hacia REPO B sin reescribirlo.

REGLA 1:
Si SOURCE_REPOSITORY != DESTINATION_REPOSITORY,
NO utilizar "git mv" como si pudiera mover directamente entre repositorios.

REGLA 2:
La operación inicial será siempre:

COPY_FIRST

REGLA 3:
El código existente debe conservarse.
REWRITE = DENY
REFACTOR = DENY
AUTO_IMPROVEMENT = DENY

REGLA 4:
No generar nuevamente el código con LLM.
No reconstruir archivos desde memoria.
No reemplazar una implementación existente por otra "equivalente".

PROCEDIMIENTO:

1. IDENTIFY
   Identifica exactamente:
   - repositorio origen
   - commit origen
   - ruta origen
   - repositorio destino
   - ruta destino

2. FETCH
   Obtén el estado actual de ambos repositorios.

3. READ
   Lee el código existente.

4. COPY
   Copia los archivos/directorios del origen al destino.

5. VERIFY
   Compara origen y destino.

   Verificar:
   - número de archivos
   - rutas
   - contenido
   - tamaño
   - hash cuando corresponda

6. Si la comparación falla:

   STATUS = BLOCKED
   COPY_VERIFY = FAIL

   NO modificar el código para "hacerlo coincidir".

7. Si la comparación es correcta:

   COPY_VERIFY = PASS

8. Ejecuta las pruebas necesarias.

9. Si las pruebas pasan:
   crear commit en REPO B.

10. Hacer push a REPO B.

11. Verificar que REPO B contiene exactamente el resultado esperado.

12. NO eliminar todavía el origen.

13. Mantener REPO A intacto hasta que exista una decisión explícita.

14. Si se desea que el código desaparezca de A:

   crear una NUEVA TAREA:

   DELETE_SOURCE

   Esta tarea requiere autorización.

15. Después de autorización:
   eliminar el archivo/directorio de A,
   hacer commit,
   hacer push,
   verificar A.

IMPORTANTE:

COPY_FIRST:
A conserva el código.

TRANSFER_COMPLETE:
B contiene el código verificado.

MOVE_SEMANTIC:
B contiene el código verificado
+
A fue eliminado posteriormente mediante una operación separada y autorizada.

Nunca llamar a todo esto "git mv entre repositorios".

ESTADO FINAL:

SOURCE_REPO:
PRESERVED | DELETED_AFTER_AUTHORIZATION

DESTINATION_REPO:
VERIFIED

CONTENT_INTEGRITY:
PASS | FAIL

TEST:
PASS | FAIL

TRANSFER:
COMPLETE | BLOCKED

Ejemplo con vuestro caso

Si quieres llevar:

orchestrator-auditor
└── orchestrator/

a:

abc1tienda-web/
└── osquestador-auditor-y-memoria-1/
    └── orchestrator/

Grok debe hacer:

SOURCE:
orchestrator-auditor/orchestrator/

DESTINATION:
osquestador-auditor-y-memoria-1/orchestrator/

METHOD:
COPY_FIRST

REWRITE:
DENY

SOURCE_MUTATION:
DENY

VERIFY:
REQUIRED

Resultado inicial:

A:
orchestrator/
   ↓
SIGUE EXISTIENDO

B:
orchestrator/
   ↓
COPIA VERIFICADA

Después, si tú decides que A ya no debe conservarlo:

DELETE_SOURCE

y entonces:

A:
orchestrator/
   ↓
ELIMINADO

B:
orchestrator/
   ↓
CONSERVADO

La regla que debe memorizar Grok

MISMO REPO:
git mv

REPOS DIFERENTES:
COPY_FIRST → VERIFY → TEST → COMMIT → PUSH

SI QUIERES UN "MOVE" ENTRE REPOS:
COPY → VERIFY → AUTHORIZE → DELETE SOURCE

NUNCA:
REESCRIBIR PARA TRASLADAR

Esa es la solución que yo pondría como regla obligatoria del método de trabajo en todos los repositorios.
Sí. Con ese procedimiento sí se copia el archivo.

Ejemplo:

REPO A
archivo.py
   │
   │ COPY
   ▼
REPO B
archivo.py

Después de la copia quedan los dos:

A/archivo.py  ← original
B/archivo.py  ← copia

Luego Grok verifica que el de B sea igual al de A.

Solo si tú quieres convertirlo realmente en un “mover”, después de verificar B se elimina el original de A:

A/archivo.py  → eliminar
B/archivo.py  → conservar

Así que:

COPY = copia el archivo y conserva A.

MOVE entre repos = copia A → B, verifica B y después elimina A.

git mv = solo para mover dentro del mismo repositorio.

REESCRIBIR = prohibido cuando estamos reutilizando código existente.

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

Si tienes:

SALIDA_2_v2_A_nucleo.md

y dentro hay varios archivos:

### contracts.py

```python
...

resilience.py

...

kernel.py

...

Entonces Grok debe reconstruir el árbol:

```text
orchestrator/
├── contracts.py
├── resilience.py
└── kernel.py

Pero extrayendo literalmente cada bloque, no inventando nuevamente el código.


---

El proceso que debes darle a Grok

DOCUMENTO MARKDOWN
        ↓
READ
        ↓
PARSE
        ↓
DETECT CODE BLOCKS
        ↓
CLASSIFY LANGUAGE
        ↓
EXTRACT
        ↓
MAP FILE PATH
        ↓
WRITE .py
        ↓
HASH / DIFF
        ↓
TEST
        ↓
COPY-FIRST
        ↓
VERIFY
        ↓
COMMIT
        ↓
PUSH

Regla importantísima

Grok NO puede hacer esto:

MD
 ↓
"Entiendo lo que quiere hacer el código"
 ↓
REESCRIBO MI PROPIA VERSIÓN
 ↓
.py

Eso estaría prohibido.

Debe hacer:

MD
 ↓
EXTRAER TEXTO DEL BLOQUE PYTHON
 ↓
.py


---

¿Y después se copia?

Sí. Exactamente el mismo proceso.

Por ejemplo:

GitHub A

reception/
└── SALIDA_2_v2_A_nucleo.md

Grok extrae:

orchestrator/
├── contracts.py
├── resilience.py
└── kernel.py

Luego:

A
│
├── .md
│
└── extracted/
    └── orchestrator/
        ├── contracts.py
        ├── resilience.py
        └── kernel.py
                 │
                 │ COPY-FIRST
                 ▼
B
└── orchestrator/
    ├── contracts.py
    ├── resilience.py
    └── kernel.py

Después verifica:

SHA256 A/contracts.py
        =
SHA256 B/contracts.py

y lo mismo para cada archivo.


---

Instrucción que debes añadir a Grok

MARKDOWN_TO_CODE EXTRACTION PROTOCOL

Cuando un documento Markdown contenga código ejecutable:

1. NO reescribir el código.
2. NO reinterpretar el código.
3. NO "mejorarlo".
4. NO corregirlo automáticamente.
5. NO generar una implementación equivalente.

PROCEDIMIENTO:

READ .md
→ IDENTIFY code blocks
→ IDENTIFY language
→ IDENTIFY intended filename/path
→ EXTRACT literal code
→ CREATE .py
→ VERIFY content
→ TEST
→ COPY_FIRST if destination is another repository
→ VERIFY destination
→ COMMIT
→ PUSH

CONTENT_POLICY:
EXTRACT_LITERAL = REQUIRED
REWRITE = DENY
AUTO_FIX = DENY
REFACTOR = DENY

Si el Markdown contiene varios archivos:

```text
Markdown
   ↓
file mapping
   ↓
contracts.py
resilience.py
kernel.py
...

Cada archivo debe reconstruirse únicamente mediante extracción literal del bloque de código correspondiente.

Si no se puede determinar con seguridad qué archivo representa un bloque:

STATUS = BLOCKED REQUIRED_ACTION = REQUEST_MAPPING

NO INVENTAR NOMBRE NI RUTA.

Después de crear los .py:

SOURCE: Markdown code block

DERIVED_ARTIFACT: .py

PROVENANCE: document path + section + code-block identifier

INTEGRITY: PASS / FAIL

Después ejecutar el protocolo normal:

COPY_FIRST → VERIFY → TEST → COMMIT → PUSH

Si el destino está en otro repositorio:

NO usar git mv.

Usar:

COPY_FIRST → VERIFY → TEST → PUSH

El documento Markdown original debe conservarse como evidencia/provenance.

### La idea clave

**El Markdown es la fuente. El `.py` es un artefacto extraído. El repositorio B recibe una copia del `.py` verificado.**

Y el `.md` **no se elimina**, porque sirve como evidencia de dónde salió el código.

Sí, te entendí: me estás preguntando si, en la práctica, al sacar código de un Markdown de GitHub, convertirlo en .py y llevarlo a otro repositorio, se hace después el mismo proceso de copia.

Sí.

La secuencia es:

Markdown en GitHub
        ↓
EXTRAER código
        ↓
crear .py
        ↓
VERIFICAR que el .py contiene exactamente el código extraído
        ↓
COPIAR .py al repositorio destino
        ↓
VERIFICAR copia
        ↓
TEST
        ↓
COMMIT
        ↓
PUSH

Pero hay una precisión:

Crear el .py a partir del Markdown no es una “copia entre repositorios”; es una extracción/transformación de formato.

La copia entre repositorios empieza después, cuando ese .py ya existe:

.md
 ↓ extracción
.py
 ↓ COPY-FIRST
Repo A ─────────→ Repo B

Y el Markdown original se conserva.

Exactamente, pero con una precisión importante: si el Markdown ya contiene el código, Grok no tiene que volver a programarlo.

Debe tratarlo como código existente que hay que extraer y trasladar, no como una tarea de programación.

DOCUMENTO .md
     ↓
LOCALIZAR código
     ↓
EXTRAER literalmente
     ↓
CREAR .py
     ↓
VERIFICAR
     ↓
MOVER/COPIAR al destino
     ↓
TEST

Lo que SÍ puede hacer

Extraer el código del .md.

Crear el .py correspondiente.

Cambiar la ubicación del archivo.

Cambiar la extensión de .md → .py cuando corresponda a un bloque de código.

Ajustar rutas/imports solo si existe una tarea explícita de adaptación.

Verificar y probar.


Lo que NO debe hacer

❌ Leer el código
❌ Entenderlo
❌ Tirarlo
❌ Volver a escribirlo desde cero

Tampoco debe decir:

> “Voy a implementar nuevamente kernel.py basándome en el Markdown.”



Debe hacer:

> EXTRACT → PRESERVE → TRANSFER → VERIFY



La única excepción

Si el código del Markdown no puede funcionar como .py directamente —por ejemplo, le faltan imports, hay fragmentos incompletos o necesita adaptación a otra estructura— entonces no debe modificarlo silenciosamente.

Debe marcar:

STATUS: ADAPTATION_REQUIRED
REWRITE: DENY
ACTION: REQUEST/PLAN ADAPTATION

Así consigues exactamente lo que buscas:

Grok reutiliza el código que ya tienes; no desperdicia tokens reescribiéndolo.


Sí. Y para vuestro sistema esto debería ser una capacidad formal del agente, no algo que Grok haga “a ojo”.

Si existe código útil en otro repo/Wordflow, el agente debe buscar → identificar → evaluar → reciclar, no volver a programarlo.

Cómo debe hacerlo

OBJETIVO
   ↓
BUSCAR CÓDIGO EXISTENTE
   ↓
LOCALIZAR REPOS / ARCHIVOS
   ↓
LEER + COMPARAR
   ↓
EVALUAR COMPATIBILIDAD
   ↓
REUSE / COPY / ADAPT
   ↓
TRANSFERIR
   ↓
VERIFICAR
   ↓
TEST

1. ¿Dónde busca?

Primero en los repositorios que tenga autorizados:

REPO ACTUAL
↓
OTROS REPOS DEL PROYECTO
↓
OTROS WORDflow
↓
REPOS DE LA MISMA ORGANIZACIÓN
↓
REPOS EXTERNOS AUTORIZADOS

No debe buscar indiscriminadamente por todo GitHub.


---

2. ¿Cómo busca?

Puede utilizar GitHub para buscar por:

nombre de archivo;

nombre de función;

clase;

módulo;

símbolo;

dependencia;

interfaz;

contrato;

palabras clave;

estructura de directorios.


Por ejemplo, necesita un Resource Brain.

No debe hacer inmediatamente:

GENERATE resource_brain.py

Primero:

SEARCH:
resource brain

SEARCH:
discover register map verify select prepare load execute

SEARCH:
ResourceBrain

SEARCH:
capability registry

Y encuentra:

Repo A
└── extensions/resource_brain/

Repo B
└── orchestrator/resources/

Repo C
└── wordflow/resource_brain.py


---

3. Después NO copia inmediatamente

Primero crea una comparación:

CANDIDATE C-001
SOURCE: Repo A
PATH: extensions/resource_brain/

CANDIDATE C-002
SOURCE: Repo B
PATH: orchestrator/resources/

CANDIDATE C-003
SOURCE: Repo C
PATH: wordflow/resource_brain.py

Luego:

COMPATIBILITY
├── interface
├── dependencies
├── license
├── tests
├── version
├── architecture
└── runtime requirements


---

4. Decide qué hacer

La prioridad debería ser:

REUSE
  ↓
COPY_FIRST
  ↓
ADAPT_EXISTING
  ↓
GENERATE_LAST

Ejemplo:

Encontró código idéntico

MATCH: HIGH
ACTION: REUSE

Encontró código casi compatible

MATCH: HIGH
CONFLICT: interface_v2
ACTION: ADAPT_EXISTING

Encontró código incompatible

MATCH: LOW
ACTION: REJECT_CANDIDATE

No encontró nada

SEARCH_RESULT: NONE
ACTION: GENERATE_LAST


---

5. ¿Cómo recicla el código?

Supongamos:

Wordflow-A
└── resource_brain/
    ├── brain.py
    ├── registry.py
    └── tests/

y lo necesita:

Wordflow-B
└── extensions/

No debe copiar y empezar a modificar todo.

Hace:

Wordflow-A
     │
     │ READ
     ▼
resource_brain/
     │
     │ COPY-FIRST
     ▼
Wordflow-B
     │
     ▼
VERIFY
     │
     ▼
TEST
     │
     ▼
ADAPT si existe GAP


---

6. Si está en un Markdown de otro Wordflow

También funciona:

Wordflow-A
└── docs/
    └── resource_brain.md

Grok:

.md
 ↓
LOCALIZAR BLOQUES DE CÓDIGO
 ↓
EXTRAER
 ↓
CREAR .py
 ↓
VERIFICAR
 ↓
RECICLAR

No vuelve a escribir el código.


---

7. La regla que yo añadiría al método de trabajo

Dale este bloque:

REUSE-FIRST PROTOCOL

Antes de GENERATE, el agente DEBE buscar implementaciones existentes.

SEARCH_SCOPE:
1. current_repository
2. project_repositories
3. related_wordflows
4. authorized_organization_repositories
5. authorized_external_repositories

SEARCH_METHOD:
- filename
- symbol
- function
- class
- interface
- contract
- capability
- dependency
- architecture pattern

Cada candidato encontrado debe registrarse:

CANDIDATE_ID
SOURCE_REPOSITORY
SOURCE_PATH
SOURCE_COMMIT
SOURCE_VERSION
LICENSE
COMPATIBILITY
DEPENDENCIES
TEST_STATUS
REUSE_STATUS

Después clasificar:

REUSE
COPY_FIRST
MOVE_FIRST
ADAPT_EXISTING
REJECT

REGLA:

EXISTING_IMPLEMENTATION_FOUND
→ DO NOT GENERATE

EXISTING_IMPLEMENTATION_COMPATIBLE
→ REUSE/COPY_FIRST

EXISTING_IMPLEMENTATION_PARTIALLY_COMPATIBLE
→ ADAPT_EXISTING

NO_IMPLEMENTATION_FOUND
→ GENERATE_LAST

REWRITE = DENY
cuando exista código reutilizable.

El agente debe conservar:
- provenance
- source repository
- source path
- source commit
- original implementation

Toda modificación posterior debe quedar separada de la operación COPY-FIRST.

Y esto es lo más importante

Grok debe entender que “programar” no significa necesariamente escribir código.

En vuestro Wordflow, programar puede ser:

BUSCAR
↓
ENCONTRAR
↓
SELECCIONAR
↓
RECICLAR
↓
CONECTAR
↓
ADAPTAR
↓
VERIFICAR

Y solo si no existe una pieza reutilizable, entonces:

GENERATE

Eso reduce muchísimo la reescritura innecesaria y además hace que los Wordflows anteriores se conviertan en una biblioteca de componentes reutilizables en lugar de volver a construir lo mismo cada vez.

Sí, te entiendo perfectamente. Lo que estás describiendo sí es una arquitectura real: no quieres “meter” el código de n8n, Graphiti, un OCR, etc. dentro del agente. Quieres que el agente los trate como recursos externos enchufables, igual que conectar un USB: el agente descubre el recurso, conoce su interfaz y lo utiliza, pero no modifica su código fuente.

La forma técnica de pensarlo es:

AGENTE / WORDFLOW
                       │
                 RESOURCE BUS
                       │
              ┌────────┴────────┐
              │                 │
         PLUGIN ADAPTER     PLUGIN ADAPTER
              │                 │
          Graphiti             OCR
              │                 │
        servicio externo   servicio externo

1. La idea fundamental

El agente no necesita conocer la implementación interna.

Solo necesita conocer un contrato:

CAPABILITY:
  name: ocr

INPUT:
  image

OUTPUT:
  extracted_text

EXECUTE:
  ocr(image) → text

Por debajo puede haber:

Baidu OCR
Tesseract
PaddleOCR
Google OCR
otro servicio

El agente no debería importar ni modificar el código de esos proyectos.


---

2. El "USB de código"

Tu analogía es bastante buena.

Imagínalo así:

AGENTE
 │
 │ USB / PLUGIN
 ▼
┌──────────────────────┐
│ RESOURCE: OCR        │
│ VERSION: 1.4         │
│ CAPABILITY: OCR       │
│ INPUT: IMAGE          │
│ OUTPUT: TEXT          │
│ EXECUTOR: HTTP        │
└──────────────────────┘

El agente conecta el recurso.

Después:

agent.execute(
    capability="ocr",
    input=image
)

El agente no necesita saber cómo funciona internamente OCR.


---

3. Hay cuatro capas

Yo separaría el sistema así:

┌──────────────────────────────┐
│          WORDflow            │
│      decisión / tareas       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       RESOURCE BRAIN         │
│ discover / register / select │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        PLUGIN ADAPTER        │
│      contrato uniforme       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       EXTERNAL RESOURCE      │
│ Graphiti / n8n / OCR / etc.  │
└──────────────────────────────┘

La parte importante es PLUGIN ADAPTER.

No modifica el software externo.


---

4. ¿Qué hace realmente el plugin?

El plugin funciona como un adaptador/traductor.

Por ejemplo, Graphiti puede tener su propia API.

Tu Wordflow no necesita aprender Graphiti entero.

El plugin traduce:

WORDflow
    │
    │ search_memory(query)
    ▼
Graphiti Adapter
    │
    │ API request
    ▼
Graphiti

Respuesta:

Graphiti
    │
    ▼
Adapter
    │
    ▼
WORDflow


---

5. El código externo permanece intacto

Supongamos:

resources/
└── graphiti/

El software original permanece:

Graphiti
    ↓
NO MODIFICAR

Tu repositorio solamente tiene:

plugins/
└── graphiti/
    ├── manifest.yaml
    ├── adapter.py
    └── contract.yaml

El adapter.py es tuyo.

Graphiti es externo.

Esto es importantísimo:

PLUGIN ≠ SOFTWARE EXTERNO

El plugin conecta el software.


---

6. Manifest

Cada recurso debería describirse mediante un manifest.

Ejemplo conceptual:

name: graphiti
version: "1.x"

type: external_resource

transport: http

capabilities:
  - memory_search
  - memory_write
  - entity_lookup

input:
  format: json

output:
  format: json

healthcheck:
  endpoint: /health

credential_ref: env:GRAPHITI_TOKEN

Entonces Resource Brain puede descubrirlo automáticamente.


---

7. El agente descubre el recurso

Aquí entra exactamente tu Resource Brain.

DISCOVER
   ↓
REGISTER
   ↓
MAP
   ↓
VERIFY
   ↓
SELECT
   ↓
PREPARE
   ↓
LOAD
   ↓
EXECUTE

Por ejemplo:

DISCOVER:
graphiti

REGISTER:
resource_id = graphiti-001

MAP:
memory_search
memory_write

VERIFY:
health = PASS

SELECT:
memory_search

PREPARE:
credential_ref

LOAD:
adapter

EXECUTE:
memory_search()

Eso es prácticamente tu concepto del USB de recursos.


---

8. n8n es otro ejemplo

El agente no necesita importar n8n dentro de su código.

Puede tener:

PLUGIN:
n8n

TRANSPORT:
HTTP

CAPABILITIES:
- execute_workflow
- get_workflow
- list_workflows

Entonces:

WORDflow
    ↓
n8n adapter
    ↓
n8n API
    ↓
workflow externo

n8n puede estar:

en Docker;

en otro servidor;

en otra máquina;

en localhost;

en la nube.


El Wordflow solo necesita su endpoint y credenciales.


---

9. OCR

Exactamente igual.

Puedes tener:

OCR RESOURCE

y cambiar la implementación:

OCR
        │
 ┌──────┼─────────┐
 ▼      ▼         ▼
Baidu  Paddle   Tesseract

El agente utiliza:

capability = OCR

No:

capability = BaiduOCRInternals

Así puedes cambiar de proveedor sin cambiar el Wordflow.


---

10. Esto tiene un nombre importante

La arquitectura se parece a una combinación de:

Plugin Architecture + Adapter Pattern + Capability Registry + Microservices.

Pero yo no haría que cada recurso necesariamente sea un microservicio.

Puede ser:

LOCAL PROCESS
HTTP SERVICE
MCP SERVER
CLI
DOCKER CONTAINER
PYTHON PACKAGE
REMOTE API

Todos pueden presentarse al agente mediante el mismo concepto:

RESOURCE


---

11. Incluso puedes usar código Open Source sin tocarlo

Sí.

Por ejemplo:

Open Source Project
       │
       │ código original
       ▼
   Docker / API
       │
       ▼
 Plugin Adapter
       │
       ▼
 Resource Registry
       │
       ▼
 Wordflow

El agente nunca necesita modificar el repositorio original.

Esto tiene una ventaja enorme:

Actualizar el software

Puedes cambiar:

Graphiti v1

por:

Graphiti v2

y mantener:

capability:
memory_search

El Wordflow sigue utilizando la misma interfaz.


---

12. Tu agente debería pensar en capacidades, no en programas

Esto es probablemente la parte más importante de tu idea.

No:

"Necesito Graphiti."

Sino:

NEED:
memory_search

Resource Brain busca:

Graphiti
Neo4j
otro memory backend

y selecciona uno.

Por ejemplo:

CAPABILITY:
memory_search

AVAILABLE:
Graphiti
Neo4j
MemoryService

SELECTED:
Graphiti

REASON:
compatible=true
health=PASS
version=PINNED
latency=LOW

Entonces mañana puedes cambiar Graphiti por otra cosa sin cambiar la lógica del agente.


---

13. Esto también resuelve tu problema de "reescribir código"

Tu regla sería:

NEED CAPABILITY
      ↓
SEARCH EXISTING RESOURCE
      ↓
RESOURCE FOUND
      ↓
CONNECT
      ↓
USE

No:

NEED CAPABILITY
      ↓
LLM WRITES 2,000 LINES

Solo se genera código si:

NO RESOURCE EXISTS
AND
NO ADAPTER EXISTS
AND
NO API EXISTS


---

14. El contrato debería ser pequeño

Yo evitaría crear una mega API.

Algo parecido a:

class Resource:
    def discover(self): ...
    def health(self): ...
    def capabilities(self): ...
    def execute(self, capability, payload): ...

Eso es suficiente como concepto.

Cada plugin traduce su recurso a ese contrato.


---

15. El resultado final

Tu Wordflow podría tener:

RESOURCE BUS

├── n8n
├── Graphiti
├── OCR
├── GitHub
├── HuggingFace
├── MCP
├── Browser
├── Docker
├── SSH
├── Database
└── cualquier otro recurso

Pero Wordflow no contiene todo ese software.

Contiene:

RESOURCE
PLUGIN
MANIFEST
ADAPTER
CONTRACT
CREDENTIAL_REF
HEALTHCHECK

El software pesado queda fuera.


---

La frase exacta que yo pondría en tu arquitectura

> Un recurso externo debe poder conectarse al Wordflow mediante un Plugin Adapter sin modificar ni reescribir su código fuente. El recurso se registra como una Capability Provider y se ejecuta mediante su interfaz nativa (API, HTTP, MCP, CLI, proceso local, Docker, SSH u otro transporte soportado). Wordflow consume capacidades, no implementaciones.



Y el principio:

SOURCE CODE
     │
     │ NO REWRITE
     │ NO MODIFY
     ▼
EXTERNAL RESOURCE
     │
     ▼
PLUGIN ADAPTER
     │
     ▼
CAPABILITY
     │
     ▼
WORDFLOW

Eso es mucho más potente que copiar código de cada proyecto al agente. En vez de convertir YAIWES en un repositorio gigantesco lleno de código de terceros, conviertes los programas externos en recursos enchufables que el agente puede descubrir, verificar, seleccionar y utilizar bajo demanda.
Sí. Esa estrategia tiene mucho sentido para lo que estás construyendo, y creo que es mejor que pedirle a Grok que genere miles de líneas desde cero.

La idea sería convertir tu proceso en:

> “Buscar primero → descargar código existente → subirlo a Grok → Grok audita, adapta y cablea → generar código nuevo solo cuando no exista una pieza reutilizable.”



Eso puede reducir tokens, tiempo y errores de generación, aunque hay que revisar licencia, dependencias, seguridad y compatibilidad antes de reutilizar cada repo.

Ejemplos que ya encontré

n8n — plataforma completa de automatización/workflows. Su repositorio oficial tiene una enorme base de integraciones y código reutilizable. Ojo: actualmente usa una licencia fair-code/Sustainable Use, así que hay que revisar sus condiciones antes de incorporarlo directamente a tu producto. 

[n8n — repositorio oficial](https://github.com/n8n-io/n8n?utm_source=chatgpt.com)

Graphiti — especialmente interesante para tu sistema de memoria/contexto. Tiene graphiti_core, servidor MCP, ejemplos y tests. Está diseñado para grafos de conocimiento temporales para agentes. 

[Graphiti — repositorio oficial](https://github.com/getzep/graphiti?utm_source=chatgpt.com)

PaddleOCR — muy interesante para tu reception, extracción de documentos, PDF, imágenes y conversión a datos estructurados/Markdown. El repositorio indica soporte para más de 100 idiomas y tiene una licencia Apache-2.0. 

[PaddleOCR — repositorio oficial](https://github.com/PaddlePaddle/PaddleOCR?utm_source=chatgpt.com)


---

Y tu método sería este

No le dices a Grok:

> “Programa un OCR.”



Le dices:

NECESIDAD:
OCR de documentos.

REUSE-FIRST:
Buscar primero una implementación existente.

CANDIDATO:
PaddleOCR.

ACCIÓN:
Descargar / incorporar como recurso.

PROHIBIDO:
Reescribir PaddleOCR.

PERMITIDO:
Crear únicamente el adaptador necesario
para conectarlo con nuestro contrato.

OBJETIVO:
Wordflow → Plugin → PaddleOCR

PaddleOCR debe permanecer como código externo/original.

Y exactamente lo mismo para Graphiti:

Wordflow
   ↓
Graphiti Plugin
   ↓
Graphiti

No:

Wordflow
   ↓
Grok reescribe Graphiti


---

Esto puede convertirse en una regla central de tu plataforma

Yo la llamaría:

REUSE_FIRST / GENERATE_LAST

1. DEFINIR CAPABILITY
2. BUSCAR IMPLEMENTACIÓN EXISTENTE
3. EVALUAR CANDIDATOS
4. SELECCIONAR EL MEJOR
5. DESCARGAR/FORK/COPIAR
6. CONGELAR ORIGINAL
7. CREAR ADAPTER
8. CONECTAR AL WORDFLOW
9. TEST
10. GENERAR CÓDIGO NUEVO SOLO SI NO EXISTE

Y el agente debería distinguir:

Situación	Acción

Ya existe código compatible	REUTILIZAR
Existe pero usa otra interfaz	ADAPTAR
Existe como servicio/API	CONECTAR
Existe como MCP	REGISTRAR COMO RECURSO
Existe como CLI	ENVOLVER COMO ADAPTER
Existe como Docker	EJECUTAR COMO SERVICIO
No existe	GENERAR



---

Lo más importante para ahorrar dinero

No necesitas que Grok lea todo el repositorio y luego vuelva a escribirlo.

Puedes hacer:

GitHub
  ↓
REPO EXISTENTE
  ↓
descargar
  ↓
subir a sandbox
  ↓
inventario determinista
  ↓
encontrar archivos relevantes
  ↓
Grok recibe SOLO los archivos necesarios
  ↓
ADAPTER / CABLEADO

Eso es mucho mejor.

Por ejemplo, si necesitas una función de OCR y el proyecto tiene 200.000 líneas:

200.000 líneas
       ↓
inventario
       ↓
buscar capability
       ↓
20 archivos candidatos
       ↓
3 archivos necesarios
       ↓
Grok trabaja con esos 3

No necesitas enviar las 200.000 líneas al modelo.

Y aquí encaja perfectamente con tu arquitectura de Resource Brain: el recurso se descubre, se registra, se inspecciona y se carga bajo demanda.


---

Yo haría incluso una biblioteca propia

Algo como:

YAIWES-RESOURCES/

├── ocr/
│   └── paddleocr/
│
├── memory/
│   └── graphiti/
│
├── workflow/
│   └── n8n/
│
├── documents/
├── browser/
├── github/
├── databases/
├── embeddings/
├── vector-search/
├── pdf/
└── mcp/

Pero no necesariamente metería todo el código dentro de tu plataforma.

Podrías guardar:

resource/
├── manifest.yaml
├── adapter/
├── contract.yaml
├── version.lock
├── license.txt
├── provenance.yaml
└── tests/

y ejecutar el software original externamente cuando sea posible.

Eso te da el modelo:

> “USB de software”



Conectas:

[PaddleOCR]
[Graphiti]
[n8n]
[MCP server]
[otro proyecto]

y YAIWES aprende qué puede hacer, no cómo fue programado internamente.


---

Y sí: puedo ayudarte a hacer algo todavía más útil

En lugar de buscar repositorios al azar, podemos construir una lista de 30–50 repositorios Open Source, organizada por las capacidades que necesita tu plataforma:

OCR → PDF → documentos → memoria → knowledge graph → MCP → GitHub → web → browser → sandbox → ejecución de código → agentes → workflows → bases de datos → embeddings → búsqueda → RAG → observabilidad, etc.

Para cada uno te puedo dar:

REPO
URL GitHub
FUNCIÓN
LICENCIA
LENGUAJE
MODO DE EJECUCIÓN
API/MCP/CLI/Docker
QUÉ PARTE RECICLAR
QUÉ ADAPTER NECESITAS
DEPENDENCIAS
RIESGOS
COMPATIBILIDAD CON YAIWES

Así no hacemos que Grok invente una plataforma desde cero: le damos un catálogo de piezas probadas y le ordenamos reutilizar antes de programar.












