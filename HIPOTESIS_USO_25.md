# 25 HIPÓTESIS DE USO — Interface Osquestador (per Max, paso previo al prototipo)

**Fecha**: 2026-07-19 18:30
**Modo SHERIFF v8.2**: input-block-reader literal · NO improvisar
**Trigger**: Max "bienes haciendo antes de crear el prototipo de la INtERFACE en htlm haces 25 hipótesis de uso luego haces 25 simulaciónes de uso"

---

## Definición de hipótesis de uso

Una **hipótesis de uso** es un escenario de usuario (persona + acción + contexto + resultado esperado) que el sistema DEBE soportar si la hipótesis se valida. Se diferencia de un requisito funcional porque:
- Una hipótesis PUEDE ser falsa → se valida con simulaciones
- Una hipótesis está escrita en lenguaje natural (no en código)
- Una hipótesis tiene un "test de aceptación" (¿cómo sé que el sistema la soporta?)

---

## Las 25 hipótesis (lectura del spec + de los 9 puntos de Max)

### Grupo A — Onboarding y navegación (5 hipótesis)

**H01**: Como Max, cuando abro el panel por primera vez, veo el proyecto "osquestador-auditor" como activo en el sidebar izquierdo (240px) y el árbol de conocimiento del proyecto en el panel central. **Aceptación**: en <500ms renderiza el árbol completo con los 9 tipos de nodos (objetivos, decisiones, componentes, repos, recursos, método, tareas, evidencias, conflictos).

**H02**: Como Max, cuando hago click en otro proyecto del sidebar (ej. "agentes"), el panel central cambia al árbol de ese proyecto y la URL cambia a `/p/agentes`. **Aceptación**: la navegación usa History API (no hash) y el back button del browser funciona.

**H03**: Como Max, cuando hay 3+ proyectos, puedo filtrar el sidebar por "todos / activos / archivados" y el filtro persiste en localStorage. **Aceptación**: refrescar la página mantiene el filtro elegido.

**H04**: Como Max, cuando abro un proyecto, veo un breadcrumb "Inicio / osquestador-auditor / Documentos" arriba del árbol. **Aceptación**: el breadcrumb es clickeable y cada nivel navega al nivel padre.

**H05**: Como Max, cuando trabajo en mobile (360px), el sidebar se oculta por default y aparece como drawer con scrim oscuro al tocar el ícono ☰ del header. **Aceptación**: patrón iOS 26 con translateX(-100%) → 0 en <300ms + botón cerrar en el drawer.

### Grupo B — Bandeja Anthropic (3 hipótesis)

**H06**: Como Max, cuando presiono "+ Nuevo proyecto", aparece una ventana tipo bandeja Anthropic con tabs (Conocimiento / Nuevo proyecto / Configuración). **Aceptación**: modal centrado con backdrop blur, animación fade-in 200ms, click fuera cierra.

**H07**: Como Max, en el tab "Nuevo proyecto" de la bandeja, puedo escribir el nombre del proyecto, elegir entre los 10 SDKs (Haystack, Graphiti, Kanboard, Plandex, Hermes, Obsidian, LiteLLM, MCP SDK, PaddleOCR, Telegram) y dar "Crear". **Aceptación**: el botón Crear está deshabilitado hasta que haya nombre + 1 SDK elegido. Al crear, aparece en el sidebar en <1s.

**H08**: Como Max, en el tab "Configuración", veo 4 grupos (Modelo LLM, Memoria, MCP, Apariencia) con toggle iOS azul #0A84FF estilo iOS Settings. **Aceptación**: el cambio se persiste en localStorage inmediatamente (sin botón "guardar").

### Grupo C — Chat y agentes (5 hipótesis)

**H09**: Como Max, cuando escribo en el chat central y presiono Enter, el mensaje se envía al backend vía WebSocket y la respuesta del asistente aparece token a token. **Aceptación**: streaming en vivo con cursor parpadeante, latencia <100ms al primer token.

**H10**: Como Max, puedo usar slash commands (`/memory`, `/search`, `/projects`, `/audit`) y el sistema responde con el contexto correspondiente. **Aceptación**: autocomplete muestra los 4 slash commands al escribir `/`.

**H11**: Como Max, cuando un agente termina una tarea, aparece en el panel derecho "Agentes activos" con el estado (corriendo / ok / error) y el tiempo de ejecución. **Aceptación**: el estado se actualiza en vivo vía WebSocket.

**H12**: Como Max, puedo routing a un agente específico tipeando `@agente` antes del mensaje. **Aceptación**: el agente recibe el mensaje y su respuesta llega con el ícono del agente.

**H13**: Como Max, los 9 tipos de agentes (researcher, coder, writer, auditor, orchestrator, router, memory, watchdog, translator) están disponibles en el panel derecho. **Aceptación**: click en un agente abre su chat dedicado en el panel central.

### Grupo D — Documentos y archivos (4 hipótesis)

**H14**: Como Max, cuando selecciono un documento en el panel central, puedo elegir entre "selección individual", "selección de grupo" o "selección de folder" via 3 botones. **Aceptación**: cada modo cambia el highlight visual (border azul, background azul, checkbox).

**H15**: Como Max, puedo hacer drag&drop de un PDF al panel central y el sistema lo ingiere via PaddleOCR, lo guarda en el vault, y crea un nodo en Graphiti. **Aceptación**: progreso visible en la status bar (%), nodo aparece en <2s.

**H16**: Como Max, veo los documentos del vault Obsidian en formato file row estilo iOS (icono + nombre + tipo + fecha + tamaño). **Aceptación**: tap abre preview, long-press activa selección múltiple.

**H17**: Como Max, cuando hay un documento nuevo, aparece un toast "Documento ingestado" con botones "Ver" / "Archivar". **Aceptación**: el toast desaparece en 5s o al hacer click fuera.

### Grupo E — Memoria y grafo (3 hipótesis)

**H18**: Como Max, en el panel derecho tab "Memoria", veo el grafo de Graphiti con los nodos (entidades) y edges (relaciones) del proyecto activo. **Aceptación**: click en un nodo abre sus detalles en el panel central.

**H19**: Como Max, cuando busco "graphiti" en el panel de búsqueda, aparecen resultados de los 3 motores (local hybrid BM25+FAISS, web Tavily, git memoria histórica). **Aceptación**: los resultados se agrupan por fuente con tabs.

**H20**: Como Max, puedo filtrar la memoria por tier (HOT <500 tokens, WARM 1-3K facts, COLD repo summaries). **Aceptación**: la barra de progreso muestra el % de cada tier.

### Grupo F — Configuración y funciones abiertas (3 hipótesis)

**H21**: Como Max, en Configuración, puedo elegir el modelo LLM entre 5 providers (Anthropic Claude, OpenAI GPT, Groq, Cerebras, NVidia) via LiteLLM. **Aceptación**: el cambio se aplica sin reiniciar el backend (model router en runtime).

**H22**: Como Max, hay 7 funciones `window.osquestador` expuestas a la IA/otros agentes: `osquestador.search()`, `osquestador.commit()`, `osquestador.log()`, `osquestador.diff()`, `osquestador.blame()`, `osquestador.checkout()`, `osquestador.branch()`. **Aceptación**: las funciones están documentadas en una tab "API para agentes" y responden con JSON estándar.

**H23**: Como Max, puedo instalar el sistema via `pip install osquestador` (binario) o correr `osquestador serve` para arrancar el panel. **Aceptación**: el binario está en PyPI o GitHub Releases y arranca el server + el panel en 1 comando.

### Grupo G — Status bar y observabilidad (2 hipótesis)

**H24**: Como Max, la status bar inferior muestra tokens consumidos hoy, latencia del último LLM call, memoria usada por SQLite WAL, próximo backup restic, watchdog status. **Aceptación**: actualiza cada 5s via WebSocket, números formateados con separadores de miles.

**H25**: Como Max, cuando OpenClaw o el kernel se caen, veo una alerta roja en la status bar "KERNEL DOWN" con botón "Reiniciar". **Aceptación**: el watchdog reintenta en <30s, la alerta desaparece cuando vuelve.

---

## Resumen

25 hipótesis distribuidas en 7 grupos:
- A: 5 (onboarding/navegación)
- B: 3 (bandeja Anthropic)
- C: 5 (chat/agentes)
- D: 4 (documentos/archivos)
- E: 3 (memoria/grafo)
- F: 3 (config/API)
- G: 2 (status)

**Próximo paso del spec de Max**: 25 simulaciones de uso de cada hipótesis.
