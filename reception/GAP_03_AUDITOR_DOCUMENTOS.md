# NCT — GAPS DEL ORQUESTADOR AUDITOR DE DOCUMENTOS (repo aislado)
# Fuente: CHECKPOINT_AUDITORIA_MAESTRO.md (Tanda 3, código real confirmado)

## CORRECCIÓN IMPORTANTE SOBRE LO QUE DIJE ANTES
En la ronda anterior dije que el backend del Auditor "no existe, solo
el panel visual". **Eso estaba incompleto.** La bandeja confirma que
Fable SÍ construyó código real para esto (6 archivos): especificación
completa, `contracts.py` + `resilience.py` (núcleo), plugins de
entrada/salida/agentes/flujos, un servidor MCP, y un manual de
despliegue de 10 pasos para el VPS. Esto NO es un gap — es integración
pendiente, igual que el Kernel.

## LO QUE SÍ EXISTE (código real de Fable)

| Componente | Qué hace |
|---|---|
| Especificación (SALIDA_2_orquestador_fase0) | Filosofía + 4 workflows + políticas + frontera de qué puede y no puede tocar |
| Núcleo (contracts.py + resilience.py) | Kernel agnóstico basado en plugins — no conoce nombres, los descubre por carpeta+manifiesto |
| Plugins (inputs/outputs/agents/workflows) | La lógica real de los 4 workflows |
| Servidor MCP | El Auditor expuesto como herramienta MCP |
| Manual de despliegue | 10 pasos: VPS+GitHub+Kanboard+Graphiti+Obsidian+Telegram+OCR+systemd |

**Regla de frontera confirmada:** el Auditor se detiene cuando el
inventario cubre 100% de los documentos + 0 conflictos + árbol
completo. No participa en nada después de eso. No ejecuta código de
proyectos, no hace push a repos reales.

## GAPS REALES QUE SIGUEN CONFIRMADOS

| # | Función requerida | ¿Existe? |
|---|---|---|
| A-1 | Detector de alucinaciones (valida afirmaciones contra fuentes antes de aceptarlas) | **No existe en ningún lado** — ni en mi código, ni en el de Fable, ni como ficha |
| A-2 | Verificar que los plugins de Obsidian/Graphiti/OCR Baidu/Kanboard tienen la integración REAL (no solo el contrato genérico) | **Sin confirmar** — tengo el nombre de los plugins pero no vi el contenido interno de cada uno; puede que ya esté o puede que sean plantillas vacías |
| A-3 | Traer las credenciales/configuración de estas 4 herramientas a mi `providers.yaml` o similar | **No hecho** — mi configuración actual no las contempla |

## MICRO-DIAGRAMA DEL FLUJO REAL (según la especificación de Fable)

```
documento entra → [1.1] Input Adapter (normaliza + congela FROZEN v1.0)
   → [1.2] Hash Engine (¿ya existe en inventory.json?)
   → si es nuevo: Ingesta → Auditoría → Árbol del proyecto → Índice
   → escribe SOLO a: Obsidian / Graphiti / Kanboard / su propio estado
   → se detiene ahí (nunca toca repos de proyectos)
```

## RESUMEN: 1 gap real confirmado sin ambigüedad (detector de
alucinaciones) + 2 puntos que requieren que abras/verifiques el
contenido real de los archivos "plugins" antes de saber si son gap o no
(no puedo confirmarlo sin ver el contenido interno de esos plugins).
