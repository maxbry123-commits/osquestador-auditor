# MÉTODO — réplica agentes/PIPELINE 00 + V4

**Fuente:** `maxbry123-commits/agentes/PIPELINE/00_METODO_TRABAJO_Y_ARQUITECTURA.md`
**Append:** `PIPELINE/00_METODO_V4_DOS_PASOS.md` (prevalece para ejecución nueva)
**Copia local previa:** `osquestador-auditor/PIPELINE/00_METODO_TRABAJO_Y_ARQUITECTURA.md`

## Cadena obligatoria
CONTEXT/HANDOFF → COPY-FIRST SCAN → IMPLEMENT(COPY|ADAPT|GENERATE) → WIRE → FORENSIC VERIFY → VERDICT AUTHORITY → CLOSED | FIX LOOP

## COPY-FIRST / REUSE-FIRST (56–60)
REUSE → COPY_FIRST → MOVE_FIRST → ADAPT_EXISTING → GENERATE_LAST
Entre repos: COPY, origen intacto. No `git mv` A→B.
REWRITE = DENY si existe implementación reusable.

## V4 vigente (2 pasos)
TASK_INTAKE → PASO 1 SANDBOX_BUILD → LOCAL_VERIFY → PASO 2 GITHUB_PUBLISH → REMOTE_VERIFY
Forense por tarea: DESACTIVADO. Una sola auditoría al cierre del bloque de code.

## CONTROL DE TRABAJO
1 TOTAL · 2 TERMINADAS · 3 PENDIENTES · 4 SIGUIENTE · 5 PLAN · 6 MÉTODO · 7 GitHub=verdad

## Autoridad
- Método = reglas operativas
- GitHub = fuente persistente
- Sandbox = temporal (confirmar si se usó)
- Usuario = aprueba cierre
- Forense = evidencia, no afirmación LLM
