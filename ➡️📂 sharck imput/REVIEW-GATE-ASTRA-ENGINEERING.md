# 🦈 REVIEW GATE — ASTRA + ENGINEERING REVIEW

Estado: `READY_FOR_REVIEW / STEP3_BLOCKED`.

Este documento prepara una revisión independiente. No significa que ASTRA ni ningún equipo externo haya revisado o aprobado todavía.

## Paquete mínimo a leer
1. `README-METODO-TRABAJO-MULTIAGENTE.md`
2. `📁 readme arquitectura sharck imput.md`
3. `➡️📂 readme indice de componentes sharck imput.md`
4. `📂 Craxy wall bitácora stated JSON/PLAN.json`
5. `STATE.json`
6. `CHECKPOINT.json`
7. `➡️📂 handoff Readme shark imput.md`
8. `PARCHE-RECUPERACION-SHARK-IMPUT.md`
9. `.github/workflows/sharck-input-v2-components.yml`
10. queues B01/B02/B03 y sus state/index cuando los motores terminen.

## ASTRA — cinco verificaciones obligatorias
- A1 XRAY_ARQUITECTURA: ¿el backend sigue modular contracts/adapters/plugins/registry/loader/guards/tests?
- A2 EVALUACION_PREVIA: ¿hay estados que afirman más que la evidencia?
- A3 MEJORA_VERSIONADA: ¿cada mejora preserva la versión previa y rollback?
- A4 COMPONENT_GAP_RESEARCH: ¿se escribió código desde cero existiendo OSS reutilizable mejor?
- A5 INDEPENDENT_VERIFY: ¿hashes, read-back, tests e invariantes sostienen el siguiente gate?

Salida ASTRA permitida: `REVIEW_PASS` o `REPAIR_REQUIRED`, con lista de evidencia. No PASS global.

## CLAUDE — revisión de ingeniería
- contratos/ports/adapters coherentes;
- typing/error model;
- Code Pointer RAG y source refs;
- unit/integration/failure tests propuestos;
- no acoplamiento directo a providers;
- no monolito;
- no cambios a motores canónicos.

## GROK — revisión OSS/contradicción
- alternativas y solapamientos del catálogo;
- repos archivados/deprecados;
- mantenimiento/licencia cuando sea relevante;
- issues/benchmarks/comunidad/HF/labs;
- contra-evidencia y componentes que conviene excluir.

## Revisión externa indicada por el director
Comprobar de forma independiente:
- trazabilidad de commits y paths;
- seguridad de adquisición y archivos especiales;
- separación LLM/control determinista;
- reproducibilidad D0/D1;
- gates de tool discovery;
- límites de loops/retries;
- riesgo de supply chain de componentes OSS;
- criterio de integración 1×1.

## Gate para autorizar Paso 3
No promover a `STEP3_READY` hasta registrar:
- resultado ASTRA;
- resultado CLAUDE;
- resultado GROK;
- estados reales de batches y GAPs;
- decisión del director sobre qué componentes integrar;
- cualquier review externa que el director exija, con evidencia real.
