# INPUT BLOCK 001 — Max: "no estás anotando 1 a 1 imput block lo que te acabo de dar"

**Fecha**: 2026-07-18
**Hora**: 19:00
**Trigger**: Max observa que NO estoy anotando 1-a-1 cada input block que me da
**Modo**: input-block-reader literal activado

## LITERAL de Max:
> "no estás anotando 1 a 1 imput block lo que te acabo de dar"

## Lo que Max me pide:
1. Anotar **1 a 1** = cada input block individual debe ir a GitHub
2. **Literal** = copiar textualmente lo que Max dice, sin reinterpretar
3. Inmediatamente después de recibirlo = no esperar a juntar varios

## Estado anterior (incorrecto):
- Estaba agrupando varios mensajes en un solo commit
- Estaba re-interpretando las instrucciones antes de anotar
- NO tenía un archivo por cada input block de Max

## Corrección:
- Cada mensaje de Max = 1 archivo `INPUT_BLOCK_NNN_descripcion.md`
- Commit inmediato por cada archivo
- Sin reinterpretar: copio literal
- Sin agrupar: 1 commit = 1 input block
- Sin "mejorar" el lenguaje: dejo las palabras exactas de Max

## Estructura del archivo INPUT_BLOCK_NNN:
1. Fecha + hora
2. Trigger literal (lo que dijo Max)
3. Interpretación (lo que entendí)
4. Estado anterior (qué estaba mal)
5. Corrección (qué voy a cambiar)
6. Acción tomada (este archivo + commit)
7. Próximo paso (qué sigue)

## Próximo input block a esperar:
La respuesta de Max confirmando o corrigiendo.
