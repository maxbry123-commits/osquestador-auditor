# NODE_001_DISCOVERY_V2 — Re-discovery con 4 fotos de Max

**Fecha**: 2026-07-18 21:57
**Modo SHERIFF v8.2**: DISCOVERY revisitado
**Source**: INPUT_BLOCK_004 (9 instrucciones) + INPUT_BLOCK_006 (4 fotos)

## ESPEC DESCUBIERTO (consolidado v1 + v2)

### De v1 (preservado)
- 13 programas del spec
- 9 instrucciones de Max
- 10 UI patterns community
- 7 funciones window.osquestador
- 3 ventanas tipo Anthropic
- 5 patrones iOS
- 37 decisiones D1-D37

### De v2 (NUEVO — de las 4 fotos)
- **FOTO-01** (06_kanban_dragdrop.html):
  - Layout: 4 columnas OK en mobile
  - Tipografía: las cards se ven bien
  - Problema: el botón "Mover a..." se ve fuera de la card (alineación rota)
  - GAP: el `.card-move` necesita `position: relative` o reorden DOM

- **FOTO-02** (00_main_dashboard.html):
  - Header overlapping breadcrumb "Inicio /" con "osquestador-v3"
  - "0 finding abiertos" se corta (overflow)
  - Chat cards layout weird — el "0" badge flota sobre la primera card
  - Status bar: "Tokens: 12,847" visible, pero cortado el "SQLite: 42[MB]"
  - Input "Pregúntale al Osquestado[r]" cortado
  - GAP CRÍTICO: el header no es sticky bien, el chat-area no escala mobile

- **FOTO-03** (02_nuevo_proyecto.html):
  - Modal "Nuevo proyecto" se ve bien
  - 8 iconos: building, code, monitor, circle, folder, star, chat, graph
  - Templates: Research/Notes · Webapp
  - **PROBLEMA**: el modal no tiene scroll en mobile, los campos inferiores (color picker, agente default) están cortados
  - GAP: modal necesita `max-height: 90vh; overflow-y: auto`

- **FOTO-04** (07_panel_final.html — Max lo ve así):
  - "Panel de control" + "Estado en vivo" tipografía serif bien
  - KPI cards: "5 Proyectos activos", "37 Decisiones" se ven bien
  - **PROBLEMA**: en mobile el title se ve muy grande — necesita `clamp(1.5rem, 5vw, 2rem)`
  - GAP: tipografía responsiva con clamp()

## 4 GAPS VISUALES MOBILE IDENTIFICADOS

| # | HTML | Gap | Severidad |
|---|------|-----|-----------|
| G-V2-01 | 00 | Header overlapping breadcrumb, chat cards layout | HIGH |
| G-V2-02 | 00 | "0" badge flota sobre cards, sin position | HIGH |
| G-V2-03 | 06 | Botón "Mover a..." se sale de la card | MED |
| G-V2-04 | 02 | Modal sin scroll en mobile | MED |
| G-V2-05 | 07 | Tipografía title muy grande en mobile | MED |
| G-V2-06 | 00 | Input chat cortado "Pregúntale al Osquestado..." | MED |
| G-V2-07 | 00 | Status bar cortado "SQLite: 42" | LOW |
| G-V2-08 | (general) | No hay media query < 480px en 7/8 HTMLs | HIGH |

## DECISIONES D38-D45 (nuevas para v2)

- **D38**: Mobile-first breakpoints explícitos: 360px / 414px / 768px / 1024px
- **D39**: Tipografía con `clamp()` para títulos
- **D40**: Modales con `max-height: 90vh; overflow-y: auto`
- **D41**: Botones in-card con `align-self: flex-end` o reorden DOM
- **D42**: Header sticky con z-index correcto para no overlap breadcrumb
- **D43**: Badges de status con position absolute controlado
- **D44**: Validación visual obligatoria con Playwright (NODE_011)
- **D45**: Certificación requiere 4/4 fotos mobile + 1 desktop = 5/5 visual PASS

## ANTI-INVENT CHECK

- No inventé frameworks mobile nuevos
- No inventé patterns iOS nuevos (uso los 5 ya investigados)
- No inventé breakpoints (uso 360/414/768/1024 estándar)
- No inventé herramientas (uso Playwright ya disponible)

## PRÓXIMO

NODE_002-009_REVISED + NODE_010_MOBILE_FIRST + NODE_011_VISUAL_VALIDATION
