# 25 SIMULACIONES DE DISEÑO (BUCLE 4/200)

**Fecha**: 2026-07-19 18:50
**Modo SHERIFF v8.2**: input-block-reader literal
**Trigger**: Max "luego haces 25 simulaciónes de diseño luego aplicas un diseño prototipo y luego lo auditas contras los documentos"

**Relación**: Cada simulación es un walkthrough visual del diseño del panel aplicando los 40 findings de los 10 paneles expertos.

---

## Metodología de simulación de diseño

A diferencia de las simulaciones de uso (que validaban funcionalidad), las simulaciones de diseño **validan la estética y la arquitectura visual** del panel.

Cada una incluye:
- **Momento**: en qué segundo/estado de la interacción
- **Estado actual**: qué muestra mi UI
- **Estado objetivo**: qué debería mostrar según los hallazgos
- **Cambio concreto**: qué CSS/componente aplicar
- **Veredicto**: ✓ OK / ✗ CAMBIAR / ⚠ ITERAR

---

## SIM-D01: Color de fondo del panel
**Momento**: Carga inicial
**Actual**: `#202124` (gris Chrome dark, decisión D65)
**Objetivo**: `#0D0D0F` (negro Anthropic) o `#FAF9F5` (cream Anthropic light) — el spec dice "crema/beige #D4A574 estilo Anthropic"
**Cambio**: Cambiar `body` background a `#FAF9F5` para light mode (default) y `#0D0D0F` para dark mode toggle.
**Veredicto**: ✗ CAMBIAR

## SIM-D02: Color de acento
**Momento**: Botones primarios, CTAs
**Actual**: `#FF6B6B` (coral, decisión D66)
**Objetivo**: `#D4A574` (beige Anthropic) o `#cc785c` (oficial Anthropic)
**Cambio**: Cambiar `--accent` a `#cc785c` y mantener coral como accent-2.
**Veredicto**: ✗ CAMBIAR

## SIM-D03: Tipografía headings
**Momento**: "Osquestador", títulos de proyecto, h1/h2
**Actual**: `system-ui, -apple-system, sans-serif`
**Objetivo**: `Fraunces, Georgia, serif` (decisión diseño)
**Cambio**: Importar Fraunces de Google Fonts y aplicar a `h1, h2, h3, .title`.
**Veredicto**: ✗ CAMBIAR

## SIM-D04: Tipografía body
**Momento**: Texto de párrafos, mensajes de chat
**Actual**: `system-ui`
**Objetivo**: `Inter, -apple-system, sans-serif`
**Cambio**: Importar Inter y aplicar a `body, p, .message`.
**Veredicto**: ✗ CAMBIAR

## SIM-D05: Radio de cards
**Momento**: Cards de proyectos, plugins, artefactos
**Actual**: `border-radius: 12px`
**Objetivo**: `18px` (Anthropic style)
**Cambio**: Cambiar `--radius-card: 18px`.
**Veredicto**: ✗ CAMBIAR

## SIM-D06: Sombras de cards
**Momento**: Cards de proyectos
**Actual**: `border: 1px solid rgba(255,255,255,0.08)` (dark mode)
**Objetivo**: `box-shadow: 0 1px 2px rgba(0,0,0,0.05)` + `border: 0`
**Cambio**: Aplicar shadow sutil estilo iOS.
**Veredicto**: ✗ CAMBIAR

## SIM-D07: Botón toggle (Configuración)
**Momento**: "Cerrar sesión", switches de Config
**Actual**: Checkbox plano
**Objetivo**: Switch iOS animado (40x24, thumb 20x20, slide 200ms)
**Cambio**: Componente `<Toggle>` con `transform: translateX(16px)` cuando activo.
**Veredicto**: ✗ CAMBIAR

## SIM-D08: Iconos
**Momento**: Sidebar, header, settings
**Actual**: Emoji (🎨, 📁, ⚙️) + algunos SVG inline
**Objetivo**: SF Symbols SVG (consistencia iOS)
**Cambio**: Crear `icons/sf-symbols.svg` con 30+ iconos (house, folder, gear, person, magnifier, etc).
**Veredicto**: ✗ CAMBIAR

## SIM-D09: Sidebar drawer mobile
**Momento**: Tap en ☰
**Actual**: `translateX(-100%) → 0` con `transition: 300ms` (verificado ✓)
**Objetivo**: Mantener + agregar scrim con `backdrop-filter: blur(8px)` y botón cerrar ✕
**Cambio**: Agregar `<div class="scrim">` con click-to-close.
**Veredicto**: ⚠ ITERAR

## SIM-D10: Sidebar desktop
**Momento**: 1200px viewport
**Actual**: Sidebar 240px fijo, sin sombra
**Objetivo**: Sidebar 280px + `box-shadow: 1px 0 0 rgba(0,0,0,0.05)` divisor
**Cambio**: Aumentar ancho + divider sutil.
**Veredicto**: ✗ CAMBIAR

## SIM-D11: Header
**Momento**: Top de la página
**Actual**: 56px con logo + título
**Objetivo**: 60px con logo pequeño + breadcrumb + acciones derecha (search, settings, avatar)
**Cambio**: Agregar breadcrumb + search box centrado.
**Veredicto**: ✗ CAMBIAR

## SIM-D12: Chat composer
**Momento**: Bottom del chat
**Actual**: Textarea + botón enviar coral
**Objetivo**: Textarea con auto-grow (max 200px) + botón enviar con SF Symbol `paperplane.fill` + adjuntar archivo (clip icon)
**Cambio**: Auto-grow JS + clip icon.
**Veredicto**: ✗ CAMBIAR

## SIM-D13: Burbujas de chat
**Momento**: Mensajes en el chat
**Actual**: Burbujas planas con bg gris
**Objetivo**: User = accent color, assistant = surface color, max-width 70%, padding 12px 16px
**Cambio**: Aplicar colores asimétricos.
**Veredicto**: ✗ CAMBIAR

## SIM-D14: Modal bandeja Anthropic
**Momento**: Click "+ Nuevo proyecto"
**Actual**: No existe modal
**Objetivo**: Modal centrado 480px, 3 tabs (Conocimiento / Nuevo / Config), backdrop blur 12px, fade-in 200ms
**Cambio**: Crear componente `<BandejaAnthropic>` con tabs accesibles.
**Veredicto**: ✗ CAMBIAR

## SIM-D15: Toast notifications
**Momento**: Documento ingestado, agente terminó
**Actual**: No existe
**Objetivo**: Bottom-right, 360px, slide-in 300ms, auto-dismiss 5s, con acciones
**Cambio**: Crear `<Toast>` con state global.
**Veredicto**: ✗ CAMBIAR

## SIM-D16: Status bar inferior
**Momento**: Bottom fixed
**Actual**: No existe
**Objetivo**: 32px, 5 columnas (Tokens / Latencia / SQLite / Backup / Watchdog), monospace font, update c/5s
**Cambio**: Crear `<StatusBar>` con WebSocket de health.
**Veredicto**: ✗ CAMBIAR

## SIM-D17: Panel derecho plegable
**Momento**: Click en icono de la derecha
**Actual**: No existe
**Objetivo**: 320px, 4 tabs (Memoria / Documentos / Tareas / Logs), slide-in 250ms
**Cambio**: Crear `<RightPanel>` con tabs.
**Veredicto**: ✗ CAMBIAR

## SIM-D18: File rows estilo iOS
**Momento**: Lista de artefactos
**Actual**: Cards con chip + título + descarga
**Objetivo**: Filas con icono 28x28 + nombre + metadata (fecha · tamaño) + chevron `>`
**Cambio**: Restilizar `<Artefactos>`.
**Veredicto**: ✗ CAMBIAR

## SIM-D19: Multi-select mode
**Momento**: Long-press en file row
**Actual**: No existe
**Actual**: Checkboxes aparecen a la izquierda, "Selección: 3" en header
**Cambio**: State machine (NONE/INDIVIDUAL/GROUP/FOLDER) con CSS condicional.
**Veredicto**: ✗ CAMBIAR

## SIM-D20: Kanban 4 columnas
**Momento**: Vista Tareas
**Actual**: 4 columnas con cards
**Objetivo**: MANTENER + agregar drag&drop visual (border dashed al arrastrar)
**Cambio**: Agregar visual feedback al drag.
**Veredicto**: ⚠ ITERAR

## SIM-D21: Dashboard greeting
**Momento**: Top del dashboard
**Actual**: "Hola, *Max*" con coral + 4 cards de proyecto
**Objetivo**: MANTENER + agregar CTA "+ Nuevo proyecto" prominente
**Cambio**: Botón primario arriba a la derecha.
**Veredicto**: ⚠ ITERAR

## SIM-D22: Sidebar project items
**Momento**: Lista de proyectos
**Actual**: Texto blanco + dot color
**Objetivo**: SF Symbol `folder.fill` + nombre + count (52) badge + active state con bg accent/10
**Cambio**: Iconos + badge.
**Veredicto**: ✗ CAMBIAR

## SIM-D23: Plugin tiles
**Momento**: Vista Plugins
**Actual**: Grid 2 columnas con letter icon + nombre + descripción
**Objetivo**: Grid 3 columnas desktop / 2 mobile + SF Symbol + nombre + estado (active/disabled)
**Cambio**: Cambiar a 3 columnas + SF Symbols.
**Veredicto**: ✗ CAMBIAR

## SIM-D24: Memory triple stats
**Momento**: Vista Memoria
**Actual**: 3 cards HOT/WARM/COLD con % de uso
**Objetivo**: MANTENER + agregar barra de progreso fina + filtro por tier
**Cambio**: Progress bar + filter.
**Veredicto**: ⚠ ITERAR

## SIM-D25: Empty states
**Momento**: Cuando no hay datos (0 proyectos, 0 docs)
**Actual**: Texto "No hay datos"
**Objetivo**: Ilustración SVG + texto + CTA "Crear primer proyecto"
**Cambio**: Diseñar 5 empty states (proyectos, docs, tareas, memoria, plugins).
**Veredicto**: ✗ CAMBIAR

---

## Resumen ejecutivo de las 25 simulaciones de diseño

| Veredicto | Cantidad | % |
|---|---|---|
| ✓ OK (mantener) | 0 | 0% |
| ⚠ ITERAR (mejorar) | 4 | 16% |
| ✗ CAMBIAR (refactor) | 21 | 84% |

**Diagnóstico**: 21 de 25 elementos visuales necesitan cambio. El diseño actual es un esqueleto funcional, no el diseño final Anthropic/iOS que pide el spec.

**Próximo paso del spec de Max**: aplicar el diseño prototipo (con los cambios identificados) y auditarlo contra los documentos.
