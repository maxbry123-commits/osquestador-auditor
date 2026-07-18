# /docs/fuente/ — Documentos originales del Orquestador Fase 0

Estos son los **7 documentos originales** que Max entregó como especificación del Orquestador.
Son la **fuente de verdad técnica** del proyecto. NO se modifican.

| Archivo | Descripción |
|---------|-------------|
| `01_ESPECIFICACION_v1.0.md` | Especificación completa del Orquestador Fase 0 (filosofía, estructura, workflows, políticas, robustez) |
| `02_PARTE_A_NUCLEO.md` | Código Python: contratos, resiliencia, db, kernel, motor, comandos |
| `02b_PARTE_A_NUCLEO_v2.md` | Código Parte A v2 (variante con el mismo contenido) |
| `03_PARTE_B_PLUGINS.md` | Código Python: inputs (inbox, telegram), outputs (obsidian, kanboard, graphiti, telegram_notify, handoff), agentes (ocr, haystack, persistir, auditor, arbolista, plandex, hermes, swe), workflows (4 JSON declarativos) |
| `04_PARTE_C_MCP_TOOLS.md` | Código: MCP server (4 tools), MCP client (HTTP+stdio), tools (check_kernel_isolation, scaffold), despliegue, fix v2.0 |
| `05_INSTRUCCIONES_CLAUDE_CODE.md` | 10 pasos de despliegue en VPS + GitHub |
| `06_MODELO_HTML_REFERENCIA_ESTETICA.html` | HTML de referencia VISUAL (paleta, tipografía, layout). NO replicar funciones de router |

**Hash de los originales:** ver `HASHES.sha256`
