# SHARCK — WORKFLOWS REUBICADOS DENTRO DE LA RAÍZ AUTORIZADA

Estado: `PRESERVED_BYTE_IDENTICAL / NOT_GITHUB_ACTION_ENTRYPOINT / ROOT_ONLY`

Raíz única autorizada: `➡️📂 sharck imput/`.

Los archivos `.yml` de esta carpeta fueron reubicados desde `.github/workflows/` el 2026-09-13 porque el Director estableció que TODO el código, componentes, estado y control SHARCK deben vivir exclusivamente dentro de `➡️📂 sharck imput/`.

Reglas:
1. Se preservaron byte-idénticos por blob SHA; no se reinterpretó su contenido histórico.
2. Desde esta carpeta NO son entrypoints automáticos de GitHub Actions. Son contratos/plantillas históricas para trazabilidad.
3. No usar referencias externas de motor contenidas dentro de plantillas antiguas. La autoridad de motor para SHARCK está copiada byte-idéntica en `➡️📂 sharck imput/📂 motores canónicos copiados/`.
4. Toda ejecución futura debe usar queues, state, code, artifacts y motores bajo `➡️📂 sharck imput/`.
5. Ningún workflow SHARCK debe volver a `.github/workflows/` sin autorización explícita del Director, porque esa ruta está fuera de la raíz permitida.
6. No mezclar ni copiar workflows/componentes de otros proyectos.

Motor 2 copiado: blob `84d566e2ee4e98e42eb3a864026d067d48caabd9`.
Engine copiado: blob `91e6e4486692eab314be5c7130d8310d3c855397`.

Commit de reubicación: `eec96fc8cc324c09dbae8a8d26c2c257e99026cc`.
