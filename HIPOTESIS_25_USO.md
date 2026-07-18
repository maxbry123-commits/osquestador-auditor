# 25 Hipótesis de uso del Osquestador-Auditor

**Fecha**: 2026-07-18
**Paso**: 2/10

## H1: Chat multi-modelo simultáneo
Max quiere comparar respuestas de 3 LLMs en paralelo (Claude, GPT-OSS, Gemma) sobre la misma pregunta. La interface debe permitir split-view 3-way con streaming sincronizado.

## H2: Memoria persistente cross-session
Max retoma proyecto después de 2 semanas. El panel debe mostrar el contexto completo de la conversación anterior sin que Max tenga que repetir nada. Auto-recall via Graphiti.

## H3: Input multimodal (texto + archivos)
Max arrastra 3 PDFs + 1 imagen + texto. El input-block-reader debe parsear todo, hashear, indexar y mostrar miniaturas antes de enviar.

## H4: Búsqueda unificada
Max busca "D26" en el panel. Debe encontrar el doc donde se decidió, el commit donde se anotó, la conversación donde se discutió y la skill que la implementa. 1 query → 4 fuentes.

## H5: Skills auto-creadas
El agente detecta patrón repetido (3+ veces "consultar weather") y propone auto-crear skill `weather-check`. Panel muestra propuesta con diff antes de aceptar.

## H6: Modo loops watchdog
Max configura `watchdog: every 60s check repo X`. Panel muestra latencia del último check, próxima ejecución, log live, botón pause/resume.

## H7: Vault estilo Obsidian
Panel central es un vault markdown con wikilinks `[[proyecto]]`, frontmatter YAML, daily notes, graph view lateral.

## H8: Kanban integrado
Sidebar derecho tiene 3 columnas (Backlog/Doing/Done) con drag-drop. Tareas se crean via slash-command `/task crear feature X`.

## H9: OCR automático
Max sube foto de pizarra. PaddleOCR extrae texto → Baidu OCR valida → Graphiti indexa entidades → aparece en chat "detecté 3 personas, 2 fechas, 1 lugar".

## H10: MCP bridge
Panel conecta a 3 MCP servers simultáneos (Graphiti, Kanboard, Filesystem). Status indicators en header, tools list en sidebar.

## H11: Multi-proyecto
Max tiene 5 proyectos activos. Sidebar los lista, click cambia contexto completo (vault, tasks, memory, secrets).

## H12: Slash commands contextuales
`/memory add "..."` solo funciona en chat de proyecto activo. `/deploy` solo en proyecto tipo webapp. UI muestra disponibles según contexto.

## H13: Auto-save + version history
Cada cambio en vault o settings se guarda automáticamente. Version history accesible con diff side-by-side y botón rollback.

## H14: Templates
Max define template `bug-report.md` con frontmatter obligatorio (severity, area, repro). Comando `/new bug-report` pre-llena.

## H15: Graph view interactivo
Sidebar muestra mini-graph (nodos = archivos, edges = links). Click en nodo abre archivo. Zoom/pan idéntico Obsidian Canvas.

## H16: Telegram bridge
Max envía mensaje a su bot Telegram desde el móvil. Aparece en panel como nuevo mensaje de user "Max-via-Telegram" con badge.

## H17: Secretos seguros
Max guarda `OPENAI_API_KEY` en panel. Se almacena en `~/.osquestador/secrets/` con chmod 600, EXCLUIDO de backup y git.

## H18: Health check watchdog
Cada 30s, watchdog verifica: SQLite WAL integrity, Graphiti connection, disk space, memoria processes. Status bar muestra ✅/⚠️/❌.

## H19: Backups automáticos
Cada 6h, snapshot de `vault/` + `db/` → `/backups/osquestador-YYYYMMDD-HH.tar.gz`. Botón restore desde panel.

## H20: 9 modelos LLM
Header tiene dropdown con 9 modelos. Cada modelo tiene: provider, max tokens, $/M tokens, status (configured/error), benchmark score.

## H21: Slash commands UI
`/` abre menu flotante con 50+ comandos agrupados (Memoria/Tareas/Vault/Skills/Deploy). Fuzzy search + keyboard nav.

## H22: Agentes especializados
52/100 agentes categorizados en 9 tipos. Sidebar muestra árbol colapsable: Investigador/Escritor/Code/DevOps/etc. Click activa.

## H23: Diff visual para cambios
Max modifica config. Panel muestra diff verde/rojo antes de aplicar. Botón "Apply" + "Cancel" + "Open full file".

## H24: Dark mode puro
Panel solo dark mode (estética Anthropic). Toggle light/dark removido. Accent azul solo en estados ON/focus.

## H25: Export panel completo
Max hace `Cmd/Ctrl+Shift+E` y se exporta panel completo (HTML+CSS+JS+state.json) en 1 ZIP portable. Para backup, sharing, migración.
