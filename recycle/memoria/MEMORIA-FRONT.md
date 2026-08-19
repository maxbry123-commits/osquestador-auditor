# MEMORIA-FRONT · Documentación del Frontend NCT

Donde vive cada parte del frontend y como iteramos.

## Repositorio

| Campo | Valor |
|---|---|
| Repo | `maxbry123-commits/frontend` |
| Branch | `main` |
| Hosting destino | Cloudflare Pages |
| URL publica objetivo | `frontend.pages.dev` |
| Stack | HTML + CSS + JS vanilla |

## Versionado

Cada bloque iterativo se pushea con tag de version en el commit message. Ej:

```
FRONT v0.1.0 · MOCK_V0.1 shell JARVIS-like 3 columnas + DSL loops
```

## Sistema de loops (`.loops/`)

| Archivo | Funcion |
|---|---|
| `PLANTILLAS.md` | DSL versionado + 10 bloques planeados |
| `BITACORA.md` | Notas de parche por cada iteracion |

## Bloques planeados

| Version | ID | Descripcion | Estado |
|---|---|---|---|
| v0.0.1 | (init) | Sistema loops creado | DONE |
| v0.1.0 | MOCK_V0.1 | Shell 3 columnas JARVIS-like (sidebar/centro/debate) | DONE |
| v0.2.0 | MOCK_V0.2 | Chat pill Qwen-style | PENDING |
| v0.3.0 | MOCK_V0.3 | Lista proyectos con thumbnails | PENDING |
| v0.4.0 | MOCK_V0.4 | Dashboard Crazy Wall con KPIs | PENDING |
| v0.5.0 | MOCK_V0.5 | Modal selector de modelo | PENDING |
| v0.6.0 | MOCK_V0.6 | Modal agregar al chat | PENDING |
| v0.7.0 | MOCK_V0.7 | Sidebar proyectos (crear/eliminar) | PENDING |
| v0.8.0 | MOCK_V0.8 | Knowledge base + docs | PENDING |
| v0.9.0 | MOCK_V0.9 | Panel API Health (router multi-key) | PENDING |
| v1.0.0 | (deploy) | Dark mode + responsive + deploy CF | PENDING |

## Vista previa local

```
/workspace/loop_v0/
├── README.md
├── HISTORIAL.md
└── src/
    ├── index.html         <- shell completo
    ├── css/styles.css      <- tema dual dark/light
    ├── js/app.js           <- agentes mock + clock
    └── assets/avatar.svg
```

Para ver el mockup Max puede:

1. Abrir `/workspace/loop_v0/src/index.html` en un navegador
2. O pedirle a Mavis que lo sirva con `python3 -m http.server`
3. O revisarlo en GitHub: https://github.com/maxbry123-commits/frontend/blob/main/src/index.html

## Decisiones de diseno

- **Tema dual dark/light**: por defecto dark (como JARVIS) con toggle via `<html data-theme="light">`
- **Responsive**: en pantallas <1100px se reducen anchos, <900px se ocultan sidebars
- **Sin frameworks**: HTML+CSS+JS vanilla para deploy rapido en Cloudflare Pages
- **Mocks por ahora**: agentes, debate, feed son datos hardcoded en `app.js` hasta que haya backend
- **Estilo replicado del JARVIS Command Center**: paleta cyan/teal/purple, dot-greens, badges con porcentaje
