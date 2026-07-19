# TASK_019 — LOOP CONTROLLER

**Fecha**: 2026-07-18 21:20
**Modo SHERIFF v8.2**: LOOP_CONTROLLER (orquesta reparación + research + execution)

## OBJETIVO

Definir el controlador que decide QUÉ loop correr, CUÁNDO parar, y CÓMO recuperarse.

## TIPOS DE LOOPS

| Loop | Trigger | Max iter | Stop condition |
|------|---------|----------|----------------|
| EXECUTION_LOOP | pending_tasks > 0 | ∞ | all tasks CERTIFIED |
| REPAIR_LOOP | task.status = FAIL | 3 | task.status = PASS |
| RESEARCH_LOOP | task.has_gap = true | 20 (o más si Max pide) | gap resuelto |
| MEMORY_LOOP | new state.json checkpoint | 1 | written to disk |
| GITHUB_STATE_LOOP | new commit | 1 | pushed to remote |

## STATE MACHINE

```
START
  ↓
LOAD state.json
  ↓
pending = filter(state.tasks, status = pending)
  ↓
while pending not empty:
  task = next task (priority order)
  status = EXECUTE(task)
  ↓
  if status = PASS:
    mark complete
    write state.json
    commit to GitHub
    continue
  ↓
  if status = FAIL:
    for attempt in 1..3:
      status = REPAIR(task, attempt)
      if status = PASS: break
    if still FAIL:
      escalate to research loop (20 pasadas)
    if still FAIL:
      mark BLOCKED, continue with next task
  ↓
  if status = NEEDS_RESEARCH:
    research_result = RESEARCH_LOOP(task.gap, max=20)
    status = EXECUTE(task)  # retry
```

## REPAIR STRATEGIES (3 attempts)

### Attempt 1: SIMPLE_FIX
- Relee spec literal
- Aplica fix mínimo (1-2 líneas)
- Re-ejecuta

### Attempt 2: REDESIGN
- Si SIMPLE no funcionó
- Aplica redesign engine (clasifica + rediseña)
- Re-ejecuta

### Attempt 3: ROLLBACK + FORK
- Si rediseño no funcionó
- Rollback a estado anterior
- Fork del approach (alternativa)
- Re-ejecuta

### After 3 attempts: RESEARCH_LOOP (20 pasadas)
- Búsqueda paralela en 5 repos
- Búsqueda paralela en 5 community sources
- 5 docs oficiales
- 5 source code audits
- Si nada funciona → escala a Max con evidencia completa

## CURRENT STATE (inicio TASK_019)

```json
{
  "pipeline": "DSL_DAG_SHERIFF_v8.2",
  "node_id": "TASK_019",
  "completed": ["PIPELINE_BOOT", "NODE_001-009", "TASK_001-018"],
  "pending": ["TASK_020", "TASK_021", "TASK_022", "TASK_023", "TASK_024", "HARDENING"],
  "tasks_total": 24,
  "tasks_done": 18,
  "findings_open": 0,
  "htmls_v5": 8,
  "size_total_kb": 138
}
```

## NEXT TASK (TASK_020_STATE_SYNC)

Actualizar state.json con el estado actual y commit.

## CIERRE TASK_019

Loop Controller definido. Strategies documentadas. Procede TASK_020.
