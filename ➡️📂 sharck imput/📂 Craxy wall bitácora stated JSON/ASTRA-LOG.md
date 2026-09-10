# ASTRA — LOG / SCOPE DEDICADO SHARCK INPUT V2

Estado inicial: `READY_TO_JOIN`.

ASTRA debe leer README-METODO, arquitectura, PLAN, STATE, CHECKPOINT, índice y Handoff antes de reclamar M06.

## Cinco tareas exclusivas
1. XRAY_ARQUITECTURA — detectar acoplamiento, monolitos, fricción y contratos faltantes.
2. EVALUACION_PREVIA — revisar evidencia producida por SOL/GROK/CLAUDE; buscar falsos PASS y gaps.
3. MEJORA_VERSIONADA — toda mejora crea patch/versión nueva; nunca destruye versión anterior.
4. COMPONENT_GAP_RESEARCH — antes de código nuevo, buscar OSS reutilizable y documentar URL/ref/licencia/mantenimiento.
5. INDEPENDENT_VERIFY — revisar tests, invariantes, read-back y compatibilidad; emitir REVIEW_PASS o REPAIR_REQUIRED, no PASS global.

No duplicar implementación rutinaria de SOL/CLAUDE. Si M06 está ocupado, elegir una tarea independiente marcada PENDING en PLAN.
