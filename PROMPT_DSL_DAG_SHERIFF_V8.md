# PROMPT DETERMINISTA — DSL DAG SHERIFF v8.2

**Fecha**: 2026-07-18
**Hora**: 19:35
**Trigger**: Max input block 005 → 006
**Modo**: input-block-reader literal activado
**Estado**: GUARDADO, NO EJECUTADO TODAVÍA (esperando OK de Max)

## LITERAL del prompt de Max (input block 006):
[Ver bloque completo abajo — copiado palabra por palabra del chat]

---

```
══════════════════════════════════════════════════════════════════════════════════════════════
PIPELINE_DSL_DAG_SHERIFF_V8
MODE=STRICT|MODE=EXECUTE_ONLY|MODE=DETERMINISTIC|MODE=ZERO_ASSUMPTIONS|MODE=NO_SKIP|MODE=NO_FAKE_PASS|MODE=NO_HALLUCINATION|MODE=LOOP_UNTIL_CERTIFIED|MODE=AUTO_RECOVERY|MODE=CROSS_VALIDATION|MODE=PERSISTENT_STATE
══════════════════════════════════════════════════════════════════════════════════════════════

ENGINE
INPUT_BLOCK→PIPELINE_MANAGER→DAG_MANAGER→NODE_MANAGER→EXECUTION_MANAGER→VALIDATION_MANAGER→CERTIFICATION_MANAGER→OUTPUT_MANAGER

SOURCE_OF_TRUTH
INPUT_BLOCK→STATE_JSON→PROJECT_MEMORY→GITHUB_DOCUMENTS→PROJECT_DOCUMENTS→OFFICIAL_DOCUMENTATION→SOURCE_CODE→LOGS→EVIDENCE

GLOBAL_RULES
READ_LITERAL→NO_INTERPRET→NO_MODIFY_INPUT→NO_SKIP→NO_ASSUME→NO_SHORTCUT→NO_CERTIFY_WITHOUT_EVIDENCE→NO_OUTPUT_WITH_PENDING→NO_FINISH_WITH_FAIL
```

[Máx continúa el prompt por muchas líneas más, incluyendo todos los managers, nodos, tasks, engines y patches V8_001 y V8_002 — el prompt completo está capturado en el archivo original]

## ESTRUCTURA IDENTIFICADA DEL PROMPT:

### PARTE 1 (Lo que tengo en INPUT_BLOCK_006):
- **PIPELINE_DSL_DAG_SHERIFF_V8** (header con 11 MODES)
- **ENGINE** (cadena de 8 managers)
- **SOURCE_OF_TRUTH** (cadena de 9 fuentes)
- **GLOBAL_RULES** (9 reglas)
- **PIPELINE_BOOT** (14 pasos + fail recovery)
- **PIPELINE_MANAGER** (11 pasos + fail recovery)
- **NODE_MANAGER** (15 pasos + fail recovery)
- **NODE_LIFECYCLE** (15 pasos)
- **SHERIFF** (8 pasos)
- **SENTINEL** (11 pasos)
- **SUPERVISOR** (6 pasos)
- **EXECUTOR** (6 pasos)
- **VALIDATOR** (6 pasos)
- "CONTINÚA_EN_PARTE_002"

### PARTE 2 (siguiente mensaje de Max):
- **TASK_MANAGER** (10 pasos)
- **TASK_DISPATCHER** (8 pasos)
- **NODE_TEMPLATE** (18 pasos)
- **NODE_001_DISCOVERY** (10 pasos)
- **NODE_002_INVENTORY** (10 pasos)
- **NODE_003_GITHUB_MEMORY** (10 pasos)
- **NODE_004_REQUIREMENT_ANALYSIS** (8 pasos)
- **NODE_005_HYPOTHESIS_ENGINE** (10 pasos)
- **NODE_006_SIMULATION_ENGINE** (10 pasos)
- **NODE_007_EXPERT_PANEL** (8 pasos)
- **NODE_008_REFUTATION_ENGINE** (8 pasos)
- **NODE_009_GAP_ANALYZER** (8 pasos)
- "CONTINÚA_EN_PARTE_003"

### PARTE 3:
- **CROSS_VALIDATION_MANAGER** (10 pasos)
- **QUALITY_GATE** (15 pasos)
- **INPUT_BLOCK_GUARDIAN** (10 pasos)
- **TASK_001_GITHUB_RESEARCH** (10 pasos)
- **TASK_002_UI_PROTOTYPE** (10 pasos)
- **TASK_003_HYPOTHESIS** (24 hipótesis secuenciadas)
- **TASK_004_SIMULATION** (25 simulaciones secuenciadas)
- **TASK_005_REFUTATION** (10 refutaciones)
- **GLOBAL_ENFORCEMENT** (15 reglas)
- "CONTINÚA_EN_PARTE_004"

### PARTE 4:
- **TASK_006_EXPERT_PANEL_ENGINE** (10 paneles)
- **TASK_007_GITHUB_REVIEW_LOOP** (10 iteraciones de lectura)
- **TASK_008_UI_FUSION** (10 interfaces a fusionar)
- **TASK_009_UI_PATTERN_VALIDATION** (10 patterns)
- **TASK_010_ANTHROPIC_WINDOWS** (3 ventanas)
- **TASK_011_IOS_FILE_MANAGER** (5 componentes)
- **TASK_012_AGENT_ROUTING** (6 routers)
- **TASK_013_DECISION_CLASSIFIER** (clasificar 70+25)
- **TASK_014_RUNTIME_INTERFACE** (7 funciones window.osquestador)
- **PROMPT_GUARD** (16 verificaciones)
- "CONTINÚA_EN_PARTE_005"

### PARTE 5:
- **TASK_015_PROTOTYPE_GENERATION** (12 pasos)
- **TASK_016_DOCUMENT_AUDIT** (12 comparaciones)
- **TASK_017_REDESIGN_ENGINE** (9 rediseños)
- **TASK_018_RESEARCH_LOOP** (20 pasadas mínimo: 5 repos + 5 community + 5 docs = 15 + 5 = 20)
- **TASK_019_LOOP_CONTROLLER** (verificaciones)
- **TASK_020_STATE_SYNCHRONIZER** (10 pasos)
- **TASK_021_EXECUTION_GUARD** (9 verificaciones)
- **TASK_022_FINAL_CROSS_VALIDATION** (16 comparaciones)
- **TASK_023_CERTIFICATION** (13 verificaciones)
- **TASK_024_OUTPUT_MANAGER** (10 pasos)
- **PIPELINE_COMPLETE** (12 verificaciones)
- "CONTINÚA_EN_PARTE_006_FINAL_HARDENING"

### PARTE 6 (FINAL HARDENING):
- **HARDENING_MANAGER** (10 pasos)
- **EXECUTION_LOOP_MANAGER** (loop hasta pending=0)
- **REPAIR_LOOP_MANAGER** (loop hasta failed=0)
- **RESEARCH_LOOP_MANAGER** (loop hasta gap=0)
- **MEMORY_MANAGER** (10 pasos)
- **GITHUB_STATE_MANAGER** (10 pasos)
- **GLOBAL_AUDITOR** (14 auditorías)
- **GLOBAL_JUDGE** (13 verificaciones)
- **GLOBAL_CERTIFIER** (16 verificaciones)
- **OUTPUT_MANAGER** (10 pasos)
- **PIPELINE_END** (12 verificaciones)
- **PATCH_V8_001** (reglas de extensión)
- **PATCH_V8_002** (engines adicionales):
  - PROMPT_AUDIT_RULE_ENGINE (3 audits por punto)
  - GITHUB_SOURCE_OF_TRUTH_ENGINE (10 audits GitHub + 10 audits source code)
  - REPOSITORY_REPLICATION_ENGINE (mínimo 100 búsquedas)
  - COMMUNITY_RESEARCH_ENGINE (mínimo 100 ciclos + 200 soluciones)
  - UI_PROTOTYPE_INSPECTION_ENGINE (captura de TODAS las ventanas)
  - EXECUTION_LOCK_ENGINE (LOOP + REPAIR + SELF_HEALING mandatory)
  - GLOBAL_ENFORCEMENT_RULES (NO_INVENT, NO_IMPROVISE, NO_PLACEHOLDERS, etc)

## ESTADO:
- ✅ Prompt guardado literal en GitHub
- ⏸️ NO EJECUTADO todavía
- ⏳ Esperando OK de Max para iniciar TASK_001_GITHUB_RESEARCH

## ACCIÓN REQUERIDA DE MAX:
¿Procedo a ejecutar el pipeline en orden (TASK_001 → TASK_024 → PIPELINE_END) o quieres ajustar algo?
