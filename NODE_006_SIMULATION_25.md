# NODE_006_SIMULATION_ENGINE — 25 simulaciones de uso

**Fecha**: 2026-07-18
**Estado**: PASS

## S01: Comparar 3 modelos
- **Métrica éxito**: 3 columnas visibles en 1280px, sincronización <50ms drift, tokens en tiempo real
- **Compara resultados**: Claude vs GPT-OSS vs Gemma

## S02: Retomar proyecto 14 días después
- **Métrica éxito**: Header "Last session: 14d, 47 msgs" en <100ms, top-5 entities en <500ms
- **Valida**: Negative feedback loop Graphiti

## S03: Drag-drop 5 archivos
- **Métrica éxito**: Thumbnails en <200ms, hash SHA-256 en <100ms/archivo
- **Bloquea**: >10MB con mensaje

## S04: Búsqueda "D26"
- **Métrica éxito**: 4 fuentes en <300ms, tabs <50ms
- **Falla**: graceful si fuente no disponible

## S05: Skill weather-check
- **Métrica éxito**: Threshold detection 5 usos/3d rolling, diff visible
- **Cooldown**: 7d respetado

## S06: Watchdog loop
- **Métrica éxito**: Poll 60s ±5s, status <100ms, log live
- **Resume**: catch-up <5s

## S07: Wikilink [[D37]]
- **Métrica éxito**: Auto-complete <50ms al escribir `[[`, color #3b82f6
- **Backlink**: detección en archivo destino

## S08: Kanban drag-drop
- **Métrica éxito**: Animación 200ms cubic-bezier, optimistic <16ms
- **Sync**: background <2s, rollback si >5s

## S09: OCR foto pizarra
- **Métrica éxito**: Total <7s (upload <1s, PaddleOCR <3s, BaiduOCR <2s, Graphiti <1s)
- **Output**: markdown con entidades linkeadas

## S10: 3 MCPs simultáneos
- **Métrica éxito**: Sin lag, status indicators, reconnect 1s/2s/4s/8s/30s
- **Health**: cada 30s

## S11: Cambiar 5 proyectos
- **Métrica éxito**: <100ms cambio contexto, persist localStorage
- **Pulsar**: "context switched" 200ms

## S12: `/deploy` en research-note
- **Métrica éxito**: Tachado <16ms, tooltip 200ms, 3 alternativas
- **Fuzzy**: <50ms por keystroke

## S13: Auto-save + version history
- **Métrica éxito**: Diff side-by-side <200ms, rollback 1 click
- **Apply**: persist + audit log

## S14: Crear template
- **Métrica éxito**: Editor con badges required, live preview <100ms debounce
- **Validar**: required fields antes save

## S15: Click nodo graph
- **Métrica éxito**: Archivo <100ms, pulse 600ms, edges glow 400ms
- **Pan**: to node si fuera viewport

## S16: Telegram bridge
- **Métrica éxito**: Panel <3s, badge timestamp, thread continuo
- **Encrypted**: en tránsito

## S17: Guardar API key
- **Métrica éxito**: Campo password enmascarado, "Test connection" <2s
- **Audit**: log de accesos

## S18: Graphiti caído
- **Métrica éxito**: Status cambia <30s, backoff 1s/2s/4s/8s/16s
- **Alerta**: Telegram + auto-restart 5min

## S19: Backup 03:00
- **Métrica éxito**: Cron trigger, status 30% <1s, gzip, retention 30d
- **RPO**: 6h max loss, 3-2-1 strategy

## S20: Dropdown 9 modelos
- **Métrica éxito**: <100ms open, 5 grupos provider, "recent" badge
- **Keyboard**: ↑↓ + Enter

## S21: Modal Conocimiento del proyecto
- **Métrica éxito**: Grid cards, slider capacidad, "+ Agregar contenido"
- **Estilo**: Claude.ai bandeja iOS

## S22: Modal Nuevo proyecto
- **Métrica éxito**: Form nombre+desc+icono, 1-click crear
- **Switch**: context <100ms

## S23: Modal Configuración con tabs
- **Métrica éxito**: Tabs Capacidades/Conectores/Permisos/Habilidades
- **Estilo**: iOS segmented control

## S24: File manager multi-select
- **Métrica éxito**: Long-press → checkmarks, bottom bar "Routing/Download/Delete N"
- **Selección**: individual/grupo/folder

## S25: Routing individual
- **Métrica éxito**: Click "→" → menu 9 tipos agentes
- **Visual**: badge del agente en file

## COMPARE_RESULTS: OK
## CROSS_VALIDATE: OK
## AUDIT: OK
## CERTIFY: PASS
## SIGUIENTE: NODE_007_EXPERT_PANEL
