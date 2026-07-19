# 10 REFUTACIONES — SEGUNDA PASADA post-V11 (BUCLE 7/200)

**Fecha**: 2026-07-19 19:05
**Trigger**: Max repite "10 refutaciónes de defectos y de mejoras y faltantes" (segunda pasada)

---

## REF-11 (v11): El sidebar mobile NO tiene backdrop oscuro real
**Tipo**: DEFECTO
**Ataco**: En mobile drawer, el scrim es sólido rgba(0,0,0,0.4) pero el contenido detrás NO se desenfoca. iOS usa UIVisualEffectView con blur 30px sobre el contenido.
**Defensa imposible**: iOS HIG section "Modality" — el contenido debe quedar visualmente "atrás", no solo cubierto.
**Acción**: Cambiar scrim a `backdrop-filter: blur(20px) saturate(180%)`.

## REF-12 (v11): El modal bandeja NO tiene shortcut de teclado
**Tipo**: FALTANTE
**Ataco**: Cmd+N (o Ctrl+N) debería abrir la bandeja, Esc debería cerrarla. Ningún atajo funciona.
**Defensa imposible**: Power users de iOS/macOS esperan Cmd+ shortcuts.
**Acción**: Agregar listener de keydown para Cmd+N / Esc.

## REF-13 (v11): El composer NO tiene contador de tokens
**Tipo**: FALTANTE
**Ataco**: Max escribe mucho, llega al límite de Anthropic (200K) sin aviso. La status bar muestra tokens consumidos HOY pero no del mensaje actual.
**Defensa imposible**: Claude.ai muestra "X / 200K tokens" en el composer.
**Acción**: Agregar contador live "Xs / 200K" debajo del textarea.

## REF-14 (v11): El 9 agentes en sidebar NO son links reales
**Tipo**: DEFECTO
**Ataco**: Los 9 botones "researcher, coder, writer, auditor, orchestr, router, memory, watchdog, translator" son `<button>` sin onclick. Click no hace nada.
**Defensa imposible**: console.log muestra 0 listeners.
**Acción**: Agregar `onclick="openAgent('researcher')"` que muestre un detalle o inicie un chat con ese agente.

## REF-15 (v11): El breadcrumb NO es clickeable
**Tipo**: DEFECTO
**Ataco**: "Inicio > osquestador-auditor" se ve pero al hacer click no navega. El anchor no tiene `href` real.
**Defensa imposible**: href="#" en ambos, no previene default.
**Acción**: href="/" y href="/p/osquestador-auditor" + preventDefault + dispatch router event.

## REF-16 (v11): El filtro "Todos / Activos / Archivados" NO funciona
**Tipo**: DEFECTO
**Ataco**: Click en "Activos" no filtra la lista. Solo cambia la clase `.is-active`.
**Defensa imposible**: No hay handler onclick ni filter logic.
**Acción**: Agregar `onclick="filterProjects('active')"` + data-attribute `data-status="active|archived"` + display:none condicional.

## REF-17 (v11): El botón "+ Nuevo proyecto" abre el modal pero NO crea nada
**Tipo**: DEFECTO + FALTANTE
**Ataco**: Click en "Crear proyecto" del modal cierra el modal pero NO agrega un proyecto a la lista.
**Defensa imposible**: El botón solo llama `closeBandeja()`.
**Acción**: Implementar `createProject(name, sdks)` que persiste en localStorage y agrega a la lista.

## REF-18 (v11): El switch de tema NO sincroniza entre tabs
**Tipo**: DEFECTO
**Ataco**: Si Max abre 2 tabs y cambia tema en una, la otra no se entera.
**Defensa imposible**: localStorage no dispara evento entre tabs.
**Acción**: Listener de `storage` event para sync cross-tab.

## REF-19 (v11): El header search NO hace nada al escribir
**Tipo**: DEFECTO
**Ataco**: El input search acepta texto pero Enter no busca. Falta lógica de búsqueda.
**Defensa imposible**: El input no tiene form ni handler.
**Acción**: `<form onsubmit="search(event)">` + dispatch a la vista actual con query.

## REF-20 (v11): El dashboard "Hola, Max" tiene hora hardcodeada, no real
**Tipo**: DEFECTO
**Ataco**: El saludo es siempre "Hola, Max" — no cambia según hora (buenos días/tardes/noches).
**Defensa imposible**: String literal en HTML.
**Acción**: `new Date().getHours()` → "Buenos días" (5-12) / "Buenas tardes" (12-19) / "Buenas noches" (19-5).

---

## Resumen de las 10 refutaciones v11

| # | Tipo | Síntoma | Acción correctiva |
|---|------|---------|-------------------|
| 11 | DEFECTO | Drawer scrim sin blur real | backdrop-filter blur(20px) |
| 12 | FALTANTE | Sin shortcuts teclado | Cmd+N, Esc listeners |
| 13 | FALTANTE | Sin contador tokens | "Xs / 200K" live |
| 14 | DEFECTO | 9 agentes botones sin onclick | openAgent() por tipo |
| 15 | DEFECTO | Breadcrumb no clickeable | href + router event |
| 16 | DEFECTO | Filtros no filtran | data-status + display none |
| 17 | DEFECTO | "+ Nuevo" no crea | createProject() persiste |
| 18 | DEFECTO | Tema no sync entre tabs | storage event listener |
| 19 | DEFECTO | Search no busca | form submit + dispatch |
| 20 | DEFECTO | Saludo no cambia por hora | Date.getHours() dinámico |

**Próximo paso**: BUCLE 8 — REDISEÑO v12 aplicando las 10 correcciones.
