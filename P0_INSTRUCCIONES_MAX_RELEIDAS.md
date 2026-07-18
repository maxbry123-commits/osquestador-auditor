# P0: 9 INSTRUCCIONES DE MAX — Re-leídas del repo

**Fecha**: 2026-07-18
**Modo**: loops anotando antes de empezar

## LAS 9 INSTRUCCIONES DE MAX (de INVESTIGACION_9_PUNTOS_INTERFACE.md)

### 1. Código fuente de las 8 interfaces del spec
- 10 SDKs investigados: Haystack, Graphiti, Kanboard, Plandex, Hermes, Obsidian, LiteLLM, MCP SDK, PaddleOCR, python-telegram-bot
- Métodos reales extraídos (write_documents, add_episode, jsonrpc, etc)
- **Aplicación**: cada UI component usa los métodos reales de cada SDK

### 2. Capturas de cómo funciona cada interface
- 7 fotos analizadas (Claude.ai iOS: Conocimiento proyecto, Artefactos, Menú lateral, Nuevo chat, Habilidades, Configuración, Anthropic Console)
- Patrones iOS: DocumentPicker, File manager, long-press selection

### 3. Fusionar todos los paneles en uno
**10 UI patterns para AI agents 2026 (community)**:
1. Chat+ (Co-Creator Workspace)
2. Generative UI (static/declarative/open-ended)
3. Hybrid Input (texto + GUI)
4. Proactive UI (sugiere antes de pedir)
5. Agent Progress Canvas (visualizar pasos)
6. Multi-Agent Tabs
7. Supervisor pattern
8. Transparency (confidence + reasoning + sources)
9. Context Preservation
10. Intervention controls (pause/modify/undo)

### 4. Incorporar ventanas tipo "bandeja Anthropic"
**3 ventanas tipo Anthropic**:
- 4.1 Conocimiento del proyecto (grid cards + slider capacidad + agregar)
- 4.2 Nuevo proyecto (form nombre + descripción + icono + crear)
- 4.3 Configuración (tabs: Capacidades/Conectores/Permisos/Habilidades)

### 5. Ventanas de archivos tipo iOS Apple
**3 patrones iOS**:
- 5.1 iOS DocumentPicker (file row + thumb + nombre + tipo + download)
- 5.2 Obsidian mobile file manager (sidebar vaults + folders + long-press)
- 5.3 JotDrop Google Keep-style (card grid colores + long-press multi-select)

### 6. Documentos seleccionables individual/grupo/folder
**3 patrones + source code**:
- 6.1 Individual: tap → toggle
- 6.2 Grupo: long-press → selection mode
- 6.3 Folder: tap → expandir / select all
- Code: `Set<id>` + visual border + checkmark + 3 acciones bulk (Routing, Download, Delete)

### 7. Routing a agentes y chat
**Patrones community**:
- 7.1 Claude Code Agent View (may 2026) - supervisor architecture
- 7.2 Multi-Agent Tabs (Vibe Kanban, parallel agents)
- 7.3 Implementación Osquestador:
  - Routing individual: botón → en file → menu agentes
  - Routing bulk: selección múltiple → bottom bar "Routing a..."
  - Routing por tag: automático
  - Routing por proyecto: default al agente del proyecto
  - Visual: badge del agente en file

### 8. Clasificar 70 ideas + 25 decisiones en UI vs Backend
**11 UI + 14 Backend** (ya anotado en docs)
**Frontend abierto**: cada botón = función MCP invocable por otros agentes

### 9. Binario/auto-run + funciones abiertas
- `pip install osquestador` → todo funciona
- `window.osquestador` con 7 funciones:
  - `search(query)`
  - `routing(fileIds, agentId)`
  - `openModal(modalName)`
  - `selectFiles(fileIds)`
  - `sendMessage(text)`
  - `getState()`
  - `+ IPC MCP completo`

## ESTÉTICA APROBADA (de CORRECCIONES_ESTETICA_MAX.md)
- Dark mode puro (#000 base, #0a0a0a cards)
- Sin emojis a color → iconos SVG monocromáticos outline stroke 1.5
- Sin beige/anaranjados (#d4a574, #c96442 PROHIBIDOS)
- Paleta: #000, #0a0a0a, #141414, #1a1a1a, #2e2e2e + #ffffff, #b0aea5, #9ca3af, #6b7280 + accent #3b82f6 (solo focus/ON)
- Tipografía SERIF Charter para títulos, sans-serif para body
- 5 zonas fijas: Sidebar + Header + Chat + Panel derecho + Status bar

## 13 PROGRAMAS DEL SPEC (ya anotado en TABLA_DECISIONES_ARQUITECTONICAS.md)
1. Haystack 2.31.0
2. Graphiti jul 2026
3. Kanboard v1.2.52
4. Plandex v2
5. Hermes v0.10.0
6. Obsidian v1.10+
7. LiteLLM v1.94.x
8. MCP Python SDK v3.2.4
9. PaddleOCR v3.7
10. python-telegram-bot v22.8
11. SQLite WAL 3.51
12. Neo4j 5.26+
13. Baidu OCR (NUEVO D26)

## 70 IDEAS + 37 DECISIONES (consolidadas D1-D37)

## FUNCIONES INVESTIGADAS QUE DEBEN ESTAR EN LA UI
- input-block-reader (120 puntos verificación)
- graphiti-recall (top-5 entities)
- kanboard-sync (JSON-RPC tasks)
- mcp-bridge (3 transports)
- orchestrator-kernel (5 hooks nativos)
- watchdog-loop (heartbeat + auto-restart)
- memory-distill (HOT/WARM/COLD)
- vault-search (BM25+vector)
- paddleocr-extract + baidu-ocr-cloud
- pdf-parse
- Skills auto-creadas (threshold 5/3d)
- 9 modelos LLM
- 52 skills / 100 max
- 9 tipos de agentes
- 12 tags
- Wikilinks Obsidian `[[D37]]`
- Frontmatter YAML
- Graph view
- 4-col Kanban
- Multi-select
- Routing a agentes
- Modales tipo Anthropic
- File picker iOS
- Search unificada 4 fuentes
- Slash commands
- Auto-save
- Health check watchdog
- Backups automáticos
- Export panel

## AHORA SÍ — INICIO P2: 25 HIPÓTESIS
