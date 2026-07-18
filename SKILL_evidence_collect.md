# SKILL: Captura de Evidencia Reproducible (Sheriff SHERIFF)

## Objetivo
Garantizar que **cada nodo del pipeline** del Osquestador genere evidencia objetiva, verificable y trazable. Sin evidencia → NO_PASS. La evidencia se guarda en `state.json`, `BITACORA.md`, `CHECKPOINTS.md` Y en el repo GitHub (doble copia).

## Contexto
Investigación consolidada en `INVESTIGACION.md` (reglas del spec del Orquestador) + DSL/DAG SHERIFF v8.2 de Max.
El SHERIFF exige 6 tipos de evidencia por nodo + bitácora + state + checkpoint.

## Entradas
- TASK_ID · SESSION_ID · NODE_ID
- Acción ejecutada (build, test, deploy, sync)
- Output del comando (stdout + stderr)
- Hashes SHA256 de archivos modificados
- Métricas (CPU, RAM, latency, throughput)
- Timestamps UTC

## Procedimiento

### 1. Antes de ejecutar el nodo
```python
# CHECKPOINT START
{
  "checkpoint_id": "ckpt-2026-07-17-225530-P0.5",
  "node_id": "0.5",
  "task_id": "verificar-OpenClaw",
  "ts_start": "2026-07-17T22:55:30Z",
  "objetivo": "Confirmar que OpenClaw sigue intacto antes de tocar el VPS",
  "evidencia_pre": [
    {"tipo": "ss_tlnp", "comando": "ss -tlnp | grep 18789", "esperado": "node 18789"}
  ]
}
```

### 2. Ejecutar el nodo
```bash
# Capturar TODO: stdout, stderr, exit code, duración
{
  cmd="ss -tlnp | grep 18789"
  start=$(date +%s)
  output=$(eval "$cmd" 2>&1)
  exit_code=$?
  end=$(date +%s)
  duration=$((end - start))
}
```

### 3. Después de ejecutar (CHECKPOINT END)
```python
{
  "checkpoint_id": "ckpt-2026-07-17-225530-P0.5",
  "ts_end": "2026-07-17T22:55:35Z",
  "duration_s": 5,
  "comando": "ss -tlnp | grep 18789",
  "exit_code": 0,
  "stdout": "LISTEN 0 511 0.0.0.0:18789 0.0.0.0:* users:((\"node\",pid=78726,fd=27))",
  "stderr": "",
  "resultado": "PASS",
  "evidencia_post": [
    {"tipo": "openclaw_intacto", "pid": 78726, "puerto": 18789}
  ],
  "hash_archivos_cambiados": [],
  "metricas": {"cpu": 12, "ram_mb": 4500}
}
```

### 4. Persistir
- `state.json` — estado operativo (machine-readable).
- `BITACORA.md` — log humano-legible con timestamp + acción + resultado.
- `CHECKPOINTS.md` — tabla de checkpoints con ID + nodo + resultado.
- **Repo GitHub** — commit automático del state.json + delta de BITACORA + CHECKPOINTS.

### 5. Validar (VALIDATOR + VERIFIER + JUDGE)
- VALIDATOR: schema, integridad, dependencias, trazabilidad.
- VERIFIER: confirmación externa (otro agente o humano).
- JUDGE: PASS / FAIL / WARNING / DEGRADED / BLOCKED.

## Reglas
- ✅ CADA nodo genera al menos 1 checkpoint.
- ✅ Evidencia es **reproducible** (otro agente puede verificar).
- ✅ Evidencia es **objetiva** (no "parece que funciona" → "response 200 en 45ms").
- ✅ Evidencia es **trazable** (linked al TASK_ID + NODE_ID).
- ✅ Hash SHA256 de todo archivo modificado.
- ❌ NUNCA claim PASS sin evidencia medible.
- ❌ NUNCA borrar checkpoints previos.
- ❌ NUNCA saltar CHECKPOINT_END (siempre cerrar el ciclo).

## Restricciones
- Mínimo 1 checkpoint por nodo (recomendado: pre + post = 2).
- Latencia de la captura: < 1s (no entorpecer el pipeline).
- Storage: 1 KB por checkpoint promedio.
- Retención: indefinida (los checkpoints son historia).

## Ejemplos

### state.json (fragmento)
```json
{
  "pipeline_id": "osquestador-auditor-v1",
  "session_id": "418434919792827",
  "current_phase": "FASE_0",
  "current_node": "0.5",
  "current_task": "verificar-OpenClaw",
  "ts": "2026-07-17T22:55:35Z",
  "node_status": "PASS",
  "health": {"cpu": 12, "ram_mb": 4500, "disk_free_gb": 156},
  "openclaw_intacto": true,
  "evidencias_count": 1
}
```

### BITACORA.md (entrada)
```markdown
### [2026-07-17 22:55:30] ACCIÓN: Verificar OpenClaw intacto
- TASK: 0.5 de TASKS.md
- COMANDO: `ss -tlnp | grep 18789`
- RESULTADO: ✅ OpenClaw escuchando en 18789 (pid 78726)
- HASH: n/a (no se modificó nada)
- EVIDENCIA: stdout capturado en checkpoint `ckpt-2026-07-17-225530-P0.5`
```

### CHECKPOINTS.md (entrada)
| checkpoint_id | node | ts | resultado | duración |
|---------------|------|----|-----------|----------|
| ckpt-2026-07-17-225530-P0.5 | 0.5 | 2026-07-17T22:55:35Z | PASS | 5s |

## Fuentes
- DSL/DAG SHERIFF v8.2 de Max (sección EVIDENCIA_OBLIGATORIA).
- Spec Orquestador `docs/fuente/01-05` (state persistente, journal, recovery).
- ISO 27001 — auditoría y trazabilidad.
- GitOps best practices — declarative state + drift detection.

## Dependencias
- Python 3.10+ (datetime, json, hashlib stdlib)
- `state/` folder en el repo
- `journal` table en SQLite
- `health.json` actualizado en cada paso

## Cuándo utilizar
- **SIEMPRE** — en cada nodo del pipeline.
- Cuando se necesita auditar quién hizo qué cuándo.
- Cuando hay que demostrar que el sistema cumple criterios (certificación).
- Cuando un usuario externo (Max, ingeniero) necesita reproducir el resultado.

## Cuándo NO utilizar
- Scripts de 1 solo uso efímeros.
- Operaciones que no modifican estado (consultas puras, no necesario CHECKPOINT_START).
- Debugging interactivo (capturar manualmente con `tee` + timestamp).

## Relación con otros Skills
- `SKILL_orquestador_kernel.md` — el kernel emite eventos a la bitácora.
- `SKILL_mcp_integration.md` — la bitácora es consultable vía MCP.
- `SKILL_memoria_avanzada.md` — la bitácora alimenta la memoria episódica.
- `SKILL_panel_ui.md` — el panel muestra la bitácora en una vista.

## Versión
v1.0 — 2026-07-17 · Mavis.

## Historial
- v1.0 — extracción de las reglas SHERIFF v8.2 + spec Orquestador atomic_write_json + journal.
