# COPY-FIRST IMPORT MANIFEST

Fecha: 2026-08-20

## Regla
Se auditó el contenido de código de:
- `maxbry123-commits/MEMORIA`
- `maxbry123-commits/router-universal`

Se copiaron al `osquestador-auditor` los artefactos de código que no estaban presentes por el mismo contenido SHA. Se usaron rutas con namespace `IMPORTED_CODE/` para no pisar componentes existentes.

## MEMORIA

| Fuente | SHA fuente | Destino |
|---|---|---|
| `app.js` | `03186e6a096e3b33a2099e2d94ef911c767e3f57` | `IMPORTED_CODE/MEMORIA/app.js` |
| `archivos documentos Open claw/sync_to_github.sh` | `348a731a85ffc7dc42953fe9173a562e29cfe9f4` | `IMPORTED_CODE/MEMORIA/archivos documentos Open claw/sync_to_github.sh` |

El resto del árbol de MEMORIA contiene principalmente Markdown, YAML, índices, knowledge placeholders y documentación; no se importó en esta operación code-only.

## ROUTER-UNIVERSAL

| Fuente | SHA fuente | Destino |
|---|---|---|
| `examples/ejemplo_basico.py` | `a4272874c0c3725495be1ed0ad2c64fcf6512108` | `IMPORTED_CODE/ROUTER_UNIVERSAL/examples/ejemplo_basico.py` |
| `red/connectors.py` | `e1a708a4cd7e531f6dcf3ccd16f0fb71554d99bd` | `IMPORTED_CODE/ROUTER_UNIVERSAL/red/connectors.py` |
| `red/enchufe_gate.py` | `8a0b4965d3066faf9e42a8cbc56012c84d753280` | `IMPORTED_CODE/ROUTER_UNIVERSAL/red/enchufe_gate.py` |
| `red/router.py` | `c3aaf0d50fc2de5f92a787aa841a810dc98be579` | `IMPORTED_CODE/ROUTER_UNIVERSAL/red/router.py` |
| `src/js/app.js` | `a7484ba4c5ad48bce3d0951ef640ebc6a1ef5f15` | `IMPORTED_CODE/ROUTER_UNIVERSAL/src/js/app.js` |
| `src/js/inspector.js` | `6d5aef91a23fe4bf6f3abbef2fd142dec2e127e3` | `IMPORTED_CODE/ROUTER_UNIVERSAL/src/js/inspector.js` |
| `src/js/router.js` | `9d82222aaa7a1427a7bf93243ee0d175eca525de` | `IMPORTED_CODE/ROUTER_UNIVERSAL/src/js/router.js` |
| `src/css/styles.css` | `96d4e810d3aab2d08bb2026147135ba17bb88465` | `IMPORTED_CODE/ROUTER_UNIVERSAL/src/css/styles.css` |
| `src/index.html` | `74c977c774e165c6b4b0dff3d829b884749b5f8e` | `IMPORTED_CODE/ROUTER_UNIVERSAL/src/index.html` |

`src/index-local.html` tiene el mismo SHA que `src/index.html`, por lo que no se creó una segunda copia: `74c977c774e165c6b4b0dff3d829b884749b5f8e`.

## No importado
README, docs Markdown, PNG y otros documentos no se copiaron porque la instrucción fue importar **code**. Los archivos JSON/YAML de contrato/configuración no se trataron como código ejecutable en esta pasada.

## Nota de integridad
`IMPORTED_CODE/ROUTER_UNIVERSAL/src/js/router.js` fue re-leído después de la escritura y su `content_sha` coincide exactamente con el SHA fuente `9d82222aaa7a1427a7bf93243ee0d175eca525de`.
