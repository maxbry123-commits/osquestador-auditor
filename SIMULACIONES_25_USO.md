# 25 Simulaciones de uso

**Fecha**: 2026-07-18
**Paso**: 3/10

## S1: Comparar 3 modelos
**Acción**: Max selecciona Claude/GPT-OSS/Gemma + pregunta "¿cuál es mejor framework agent?".
**Esperado**: 3 columnas streaming paralelo, latencia por columna, tokens contados, botón "save comparison".

## S2: Retomar proyecto 2 semanas después
**Acción**: Max abre proyecto `osquestador-v3`.
**Esperado**: Header muestra "Last session: 14 days ago, 47 messages". Auto-recall de Graphiti inyecta top-5 entities relevantes en input-block.

## S3: Drag-drop 5 archivos
**Acción**: Max arrastra 3 PDFs + 1 PNG + 1 .md.
**Esperado**: Pinned bar muestra 5 miniaturas, hash SHA-256 cada uno, botón "send all" + "preview".

## S4: Búsqueda "D26"
**Acción**: Max escribe "D26" en search bar.
**Esperado**: 4 tabs: Decisión | Commit | Conversación | Skill. Click cada tab abre resultado.

## S5: Skill auto-creación
**Acción**: Max usa 3 veces `/weather Madrid`.
**Esperado**: Popup "¿Crear skill `weather-check`? Mostrando diff proposed". Botones: Create / Edit / Dismiss.

## S6: Watchdog loop
**Acción**: Max activa watchdog en `maxbry123-commits/osquestador-auditor`.
**Esperado**: Status bar: "🟢 12s ago, next in 48s, 5 cycles, 0 errors". Log live actualiza cada segundo.

## S7: Crear nota con wikilink
**Acción**: Max escribe `ver [[D26]] y [[input-block-reader]]`.
**Esperado**: Auto-complete dropdown, después de Enter links se colorean y se subrayan.

## S8: Drag-drop tarea Kanban
**Acción**: Max arrastra card de "Doing" a "Done".
**Esperado**: Animación suave, Graphiti actualiza `Task.status = done`, chat confirma "✅ Task moved".

## S9: OCR foto pizarra
**Acción**: Max sube `pizarra.jpg` con "/ocr" prefix.
**Esperado**: Progress 4-stage: Upload → PaddleOCR → BaiduOCR (valida) → Graphiti index. Output markdown con entidades linkeadas.

## S10: Conectar 3 MCPs
**Acción**: Max click "+ Add MCP" en header.
**Esperado**: Modal con templates (Graphiti/Kanboard/Filesystem). Llenar form → test connection → save.

## S11: Cambiar entre 5 proyectos
**Acción**: Max click proyecto `m3-vps-chat` en sidebar.
**Esperado**: Vault/tareas/memory/secretos cambian sin reload. Header muestra nuevo nombre. Status bar parpadea "context switched".

## S12: Slash command no disponible
**Acción**: Max escribe `/deploy` en proyecto tipo `research-note`.
**Esperado**: Aparece tachado con tooltip "Only available in: webapp, api, service". Sugiere `/export`.

## S13: Editar config
**Acción**: Max modifica `AGENTS.md` sección "tone".
**Esperado**: Diff side-by-side automático. Botones Apply/Cancel. Version history con timestamp.

## S14: Crear template
**Acción**: Max click "New template".
**Esperado**: Editor con frontmatter required badges. Live preview. Save en `templates/`.

## S15: Click nodo graph
**Acción**: Max click nodo "D26" en mini-graph.
**Esperado**: Archivo se abre en panel central, nodo se ilumina, edges se animan.

## S16: Telegram bridge
**Acción**: Max manda "hola" al bot desde móvil.
**Esperado**: Panel recibe mensaje con badge `📱 Telegram`. Respuesta del agente se envía de vuelta al móvil.

## S17: Guardar API key
**Acción**: Max click "Secrets" → "Add" → nombre "OPENAI_KEY" + valor.
**Esperado**: Campo password enmascarado, botón "Test connection" antes de save. Storage en `~/.osquestador/secrets/` con permisos verificados.

## S18: Health check falla
**Acción**: Graphiti se cae.
**Esperado**: Status bar cambia a `❌ Graphiti: connection refused (3 retries)`. Botón "Restart" + log link.

## S19: Backup programado
**Acción**: Reloj llega a las 03:00.
**Esperado**: Status bar muestra "🟡 Backup in progress 30%". Al terminar: "✅ Backup saved 124MB → /backups/20260718-0300.tar.gz".

## S20: Seleccionar modelo
**Acción**: Max click dropdown modelos en header.
**Esperado**: 9 modelos con metadata: provider, max_tokens, $/M, status. Filtros por provider. Último usado marcado.

## S21: Slash command menu
**Acción**: Max escribe `/` en chat input.
**Esperado**: Menu flotante 50+ comandos agrupados. Fuzzy search filtra en tiempo real. Arrow keys navega.

## S22: Activar agente
**Acción**: Max click "Investigador" en sidebar agentes.
**Esperado**: Agente se activa, header muestra "🤖 Investigador activo", chat cambia color sutil. System prompt se inyecta.

## S23: Diff en config
**Acción**: Max modifica `temperature: 0.7` a `0.3` en `~/.osquestador/config.yaml`.
**Esperado**: Diff aparece automáticamente en panel. "Apply" persiste, "Cancel" revierte.

## S24: Toggle light/dark
**Acción**: (hipotético) Max busca toggle light.
**Esperado**: No existe. Solo dark. Tooltip explica decisión arquitectónica.

## S25: Export completo
**Acción**: Max `Cmd/Ctrl+Shift+E`.
**Esperado**: Browser descarga `osquestador-export-20260718.tar.gz` con index.html, assets, state.json. Auto-guarda en `~/Downloads/`.
