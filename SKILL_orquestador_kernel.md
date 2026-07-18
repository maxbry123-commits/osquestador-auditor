# SKILL: Orquestador con kernel pequeño + plugins

## Objetivo
Construir o entender un sistema de orquestación cuya pieza central (kernel) sea **pequeña, estable y agnóstica de los plugins concretos**, y donde toda la inteligencia viva en **carpetas intercambiables** (inputs, outputs, agents, skills, workflows).

## Contexto
Investigación consolidada en `INVESTIGACION.md` secciones 2-8, 12, 13, 14, 28.
Patrón validado por JSON-Agents/PAM, agent-registry, MOYA, Haystack 2.0, y el spec del Orquestador que Max entregó en `docs/fuente/`.

## Entradas
- Lista de capabilities deseadas (ej: `ocr`, `similitud`, `auditoria`, `arbol`, `planificar`, `documentar`, `frontera`).
- Lista de conectores externos (Telegram, Kanboard, Obsidian, Graphiti, Discord, etc.).
- Lista de inputs (inbox, telegram, drive, webhooks, polling, etc.).
- Workflows deseados (ingesta, auditoría, árbol, task index, etc.).

## Procedimiento
1. **Diseñar el kernel** como capa delgada: `boot()` carga config + DB, `pump()` itera inputs + ejecuta workflows, `shutdown()` persiste + exit.
2. **Definir contratos universales** (interfaces): `InputAdapter.discover()/ack()`, `OutputConnector.call()/health()`, `AgentAdapter.execute()/capabilities()/health()`.
3. **Implementar Registry** que escanea carpetas y carga plugins por `importlib` (sin importar por nombre desde el kernel).
4. **Implementar AgentManager** con **fallback_chain** (orden por priority, break por circuit breaker).
5. **Implementar OutputManager** que despacha por `capability` (el kernel NO nombra "kanboard" o "telegram").
6. **Motor de workflows declarativo**: lee `workflows/*.json` o `*.yaml` y los ejecuta como secuencia de steps.
7. **Comandos de usuario** operan SOLO sobre DB + OutputManager (`/estado`, `/conflictos`, `/resolver`, `/frontera`, `/handoff`).
8. **Hot-reload** por mtime de los `manifest.json` (sin restart).
9. **Linter de aislamiento** (`check_kernel_isolation.py`) que prohíbe nombres concretos en `kernel/`.

## Reglas
- ❌ NUNCA el kernel importa un plugin por nombre.
- ❌ NUNCA el kernel conoce un proveedor (Telegram, Kanboard, Slack, etc.).
- ❌ NUNCA agentes resumen contenido (solo clasifican, relacionan, señalan).
- ✅ TODO cambio es agregar/quitar una carpeta + manifest, sin tocar kernel.
- ✅ Toda capacidad tiene una cadena de agentes con priority + circuit breaker.
- ✅ Toda escritura externa es idempotente (reintento safe) y tiene fallback local.

## Restricciones
- Tamaño kernel: ≤ 200 líneas (regla del spec).
- Idempotencia en todos los `execute()`.
- Hot-reload no debe romper instancias en uso.
- Circuit breakers: threshold=5 fails, cooldown=60s, semi-open después.

## Ejemplos

### Contrato AgentAdapter
```python
class AgentAdapter:
    def capabilities(self) -> list: return []
    def execute(self, capability, payload, ctx) -> dict: raise NotImplementedError
    def health(self) -> Health: return Health()
```

### Hot-reload por mtime
```python
def _dirty(self, root):
    t = max(os.path.getmtime(os.path.join(root, d, "manifest.json"))
            for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "manifest.json")))
    return self._mtimes.get(root) != t  # recarga si cambió
```

### Workflow declarativo
```json
{
  "trigger": "document.new",
  "steps": [
    {"id": "ocr", "capability": "ocr"},
    {"id": "persistir", "capability": "persistir"},
    {"id": "auditar", "capability": "auditoria"}
  ]
}
```

## Fuentes
- Spec Orquestador Fase 0 v2.0 (`docs/fuente/01-05`)
- JSON-Agents / PAM — https://jsonagents.org
- agent-registry — https://github.com/agentoperations/agent-registry
- MOYA — https://github.com/montycloud/moya
- Haystack 2.0 — https://docs.haystack.deepset.ai/docs/creating-pipelines

## Dependencias
- Python 3.10+
- SQLite 3.7+ (con WAL)
- `importlib` (stdlib)
- `requests` (opcional, para conectores HTTP)
- `pyyaml` (opcional, para workflows YAML)

## Cuándo utilizar
- Sistemas con > 1 capacidad heterogénea (OCR + RAG + tareas + notificaciones).
- Cuando los proveedores van a cambiar (swap Telegram por Discord sin tocar el core).
- Cuando se necesita auditabilidad y trazabilidad de cada nodo.
- Cuando el equipo es > 3 personas y cada una mantiene su agente.

## Cuándo NO utilizar
- Scripts de 1 solo uso (overkill).
- Sistemas con 1 sola capacidad (kernel = overhead).
- Cuando la latencia importa y la indirección suma ms (no es nuestro caso).
- Cuando NO hay garantía de hot-reload seguro (preferir restart limpio).

## Relación con otros Skills
- `SKILL_mcp_integration.md` — cómo exponer el orquestador como MCP server.
- `SKILL_memoria_avanzada.md` — cómo conectar memoria episódica/semántica/procedimiento al AgentManager.
- `SKILL_panel_ui.md` — cómo construir el panel de control que consume el MCP server.
- `SKILL_evidence_collect.md` — cómo capturar evidencia reproducible de cada nodo.

## Versión
v1.0 — 2026-07-17 · Mavis · basado en spec v2.0 de Max.

## Historial
- v1.0 — extracción inicial del spec del Orquestador + validación con JSON-Agents/PAM + agent-registry + MOYA.
