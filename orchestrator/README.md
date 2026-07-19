# Osquestador — Orquestador Fase 0

**Versión**: v1.0 MVP · **Fecha**: 2026-07-19 · **Modo SHERIFF v8.2 STRICT**

## Estructura

```
orchestrator/
├── kernel/main.py            # Loop principal (200 LOC, atomic_write_json)
├── agents/                   # 5 adapters (ocr, classifier, obsidian, graphiti, kanboard)
├── workflows/                # JSON declarativos
│   └── ingesta.workflow.json # 6 steps: hash → ocr → classify → vault → graphiti → kanboard
├── state/                    # inventory.json, health.json, dead_letter.json, graph.json, tasks.json
├── policies/                 # knowledge.policy.md (anti-síntesis)
├── registries/               # agents.json (capability → provider)
├── inbox/                    # entrada de documentos
├── vault/                    # salida de documentos
└── __init__.py
```

## Cómo arrancar

```bash
cd /root/osquestador
python3 -m orchestrator.kernel.main
# Logs: orchestrator state
# Health: cat orchestrator/state/health.json
# Inventory: cat orchestrator/state/inventory.json
```

## End-to-end verificado

1. Poner un `.md` o `.txt` en `inbox/<proyecto>/`
2. El kernel lo detecta cada 2s (poll)
3. Calcula SHA256
4. Si NO está en inventory → ejecuta workflow
5. OCR (solo si es pdf/img, NO md/txt)
6. Clasifica (proyecto = nombre carpeta inbox)
7. Guarda en `vault/<proyecto>/`
8. Crea entity en Graphiti (in-process JSON)
9. Crea task en Kanboard (in-process JSON, o JSON-RPC si KANBOARD_URL set)
10. Marca como "ingestado" en inventory.json
11. Repite con SIGTERM → graceful shutdown

## Smoke test

```bash
mkdir -p orchestrator/inbox/test
echo "# Test objetivo: validar Fase 0 decision: SQLite WAL" > orchestrator/inbox/test/SMOKE.md
timeout 5 python3 -m orchestrator.kernel.main
# Esperado: inventory.json con 1 item, vault/test/SMOKE.md, graph.json con 1 entity
```

## Contrato del orquestador (per 01_ESPECIFICACION_v1.0.md)

- `atomic_write_json` en TODO state (SIGKILL-safe) ✓
- `graceful shutdown` con SIGTERM/SIGINT ✓
- `idempotencia` por SHA256 ✓
- `dead_letter.json` si un step falla ✓
- `health.json` refrescado en cada paso ✓
- `state/atomic_write_json` ✓
- Loop infinito mientras `_running` ✓
- NO inspecciona código de agentes (solo su contrato) ✓
- NO conoce Telegram/Drive (eso son inputs/) ✓
- NO contiene prompts (viven en skills/) ✓

## Pendiente para v1.1+

- 4 workflows reales (solo ingesta está implementado)
- 12 SDKs reales importados (ahora son adapters in-process)
- Neo4j real (ahora JSON)
- Kanboard JSON-RPC real (ahora local JSON)
- MCP server en :8765 con 4 tools
- systemd service `osquestador.service`
- `pip install osquestador` con entry point
- TUI interface (per 01_ESPECIFICACION)

REGLA #0: OpenClaw INTACTO (este orquestador vive en `/root/osquestador/`, NO en `/opt/nct/`).
