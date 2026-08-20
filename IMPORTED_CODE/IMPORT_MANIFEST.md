# COPY-FIRST IMPORT MANIFEST

Fecha: 2026-08-20

## Regla
Se importó únicamente código fuente detectado en:
- `maxbry123-commits/MEMORIA`
- `maxbry123-commits/router-universal`

No se copiaron README, documentación, imágenes ni archivos de configuración solo por existir.

## MEMORIA

| Fuente | SHA fuente | Destino |
|---|---|---|
| `app.js` | `03186e6a096e3b33a2099e2d94ef911c767e3f57` | `IMPORTED_CODE/MEMORIA/app.js` |
| `archivos documentos Open claw/sync_to_github.sh` | `348a731a85ffc7dc42953fe9173a562e29cfe9f4` | `IMPORTED_CODE/MEMORIA/archivos documentos Open claw/sync_to_github.sh` |

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

## Excluded from this code-only import
`router-universal/src/index.html`, `router-universal/src/index-local.html` y `router-universal/src/css/styles.css` son frontend assets/source de presentación. Se dejaron fuera de esta primera importación para mantener la operación estrictamente orientada a código de lógica/ejecución. Se pueden importar en una pasada separada si se solicita.

## Nota
El árbol de `MEMORIA` también contiene Markdown/YAML/documentación y archivos de conocimiento; no se copiaron porque esta operación fue solicitada como **code-only**.
