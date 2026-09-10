# 🦈 SHARCK INPUT V2 — MÉTODO DE TRABAJO MULTIAGENTE

Estado: `ACTIVE_LOOP / FAIL_CLOSED / COPY_FIRST / VERSIONED`

## 0. Raíz canónica V2

- Repo: `maxbry123-commits/osquestador-auditor`
- Branch: `main`
- Raíz activa V2: `➡️📂 sharck imput/`
- Código principal: `➡️📂 sharck imput/📂 input sharck code principal/`
- La raíz histórica `➡️📂 Shack imput/` queda preservada como V1/read-only de referencia. No se borra ni se reescribe.
- Excepción operativa: GitHub Actions debe vivir técnicamente en `.github/workflows/`; puede invocar únicamente código/colas V2 y los motores canónicos inmutables. No se considera código fuente del producto.

## 1. Contrato único de 3 pasos

1. `ANOTAR + ARQUITECTURA + INVENTARIO`: INPUT literal, hash, goals, tareas, fuentes físicas, GAPs, owners y checkpoints antes de tocar código.
2. `ADQUIRIR`: descargar/extraer/copiar/mover únicamente con los motores canónicos; grupos de máximo 10; destino explícito; no LFS; no force; read-back.
3. `CABLEAR + PODA MÍNIMA + CODE FALTANTE + TEST`: COPY-FIRST, adapters/plugins/ports, no monolito, no modificar upstream sin necesidad demostrada.

## 2. Flujo por cada INPUT

`INPUT_RAW → INPUT_LOCK → CONTRACT_JOB → GOALS → TASK_GRAPH → ROLE_ROUTER → CLAIM → FAN_OUT → WORKER_CHECKPOINTS → EVIDENCE_GRAPH → FAN_IN → CROSS_REVIEW → VERDICT → CHECKPOINT_GLOBAL → NEXT_NODE`

### Estados
`PENDING → CLAIMED → RUNNING → READY_FOR_REVIEW → VERIFIED_CLOSED`

Estados alternos: `GAP`, `FLAG`, `BLOCKED_CONTINUE_SAFE_TASK`, `REPAIR_REQUIRED`, `CLOSED_UNVERIFIED`.

Presencia física nunca equivale a integración. `DISCOVERED → ACQUIRED → EXTRACTED → READBACK_VERIFIED → WIRED → TESTED → PROMOTED`.

## 3. Contrato de nodo/checkpoint

Cada tarea debe persistir como mínimo:

```json
{
  "task_id": "Txxx",
  "input_sha256": "...",
  "version": "vN",
  "owner": "SOL|ASTRA|GROK|CLAUDE",
  "status": "PENDING|CLAIMED|RUNNING|GAP|READY_FOR_REVIEW|VERIFIED_CLOSED",
  "dependencies": [],
  "parallel_safe": true,
  "source_refs": [],
  "outputs": [],
  "evidence": [],
  "gaps": [],
  "next_node": "...",
  "resume_from": "..."
}
```

Un agente que entra nuevo lee `README → PLAN → STATE → CHECKPOINT → su log → Handoff` y continúa desde `resume_from`; no repite un nodo cerrado.

## 4. Reparto general de agentes

### SOL / ChatGPT — integrador y consolidator
- mantener INPUT literal y contrato;
- compilar DAG/tareas y owners;
- implementar núcleo determinista/ports/adapters cuando sea su nodo;
- consolidar fan-in sin borrar evidencia contradictoria;
- vigilar motores, estados y read-back;
- nunca declarar PASS sólo por respuesta de una LLM.

### CLAUDE — ingeniería de código
- code intelligence y Code Pointer RAG;
- implementar adapters/plugins/ports pequeños;
- revisar interfaces, typing, tests, failure paths e invariantes;
- COPY-FIRST desde componentes auditados;
- producir patches versionados, no sobrescritura silenciosa.

### GROK — investigación OSS y contradicción
- buscar alternativas OSS, repos, issues, benchmarks y comunidad dev;
- revisar Hugging Face, labs, documentación y limitaciones;
- proponer componentes sin instalarlos automáticamente;
- aportar contra-evidencia y StrategyDelta cuando exista GAP.

### ASTRA — rol separado de auditor/mejora
ASTRA NO duplica implementación rutinaria de SOL/CLAUDE. Sus cinco frentes son:
1. `XRAY_ARQUITECTURA`: revisar frontend/backend/contratos y detectar fricción, acoplamientos y monolitos.
2. `EVALUACION_PREVIA`: auditar lo hecho por SOL/GROK/CLAUDE, refutar evidencias y señalar falsos PASS.
3. `MEJORA_VERSIONADA`: proponer/copiar una versión `+` sin destruir la anterior; comparar antes/después.
4. `COMPONENT_GAP_RESEARCH`: investigar OSS reutilizable antes de autorizar código desde cero; registrar URL/ref/licencia/mantenimiento.
5. `INDEPENDENT_VERIFY`: ejecutar/revisar tests, read-back, invariantes y compatibilidad; emitir `REVIEW_PASS|REPAIR_REQUIRED`, no PASS global.

## 5. LOOP operativo simplificado

`INPUT literal → 12 GOALS → 2 prioridades → plan → cola 1×1 por dependencia → ejecutar → verificar/refutar → GAP? investigar hasta 20 vías → elegir StrategyDelta materialmente distinto → retry o continuar tarea independiente → Council12 → 3 refutaciones → cross-check → CODA/persistencia → verify_final`.

"No stop" se implementa como persistencia + reanudación por checkpoint: un intento no puede quedar en loop CPU infinito. Cada ejecución tiene límites técnicos; el watchdog horario reabre cualquier GAP pendiente y continúa desde el checkpoint.

## 6. Cinco refutaciones del plan

1. **¿Cuatro agentes sobre la misma tarea aceleran?** No necesariamente. Solución: ownership exclusivo + fan-out sólo para tareas independientes.
2. **¿Más componentes siempre mejora Shark?** No. Solución: componente candidato ≠ integrado; gate de mantenimiento/licencia/función/solapamiento antes de wire.
3. **¿Un LOOP infinito es seguro?** No como proceso único. Solución: retries acotados por ejecución + checkpoint durable + watchdog recurrente.
4. **¿Todo debe estar físicamente dentro de la raíz?** El código/producto sí; GitHub exige workflows en `.github/workflows` y los motores canónicos ya viven fuera. Se documentan como excepciones de control, no producto.
5. **¿Una descarga correcta significa tarea cerrada?** No. Exigir motor verdict + read-back; luego wiring y tests independientes.

## 7. 12 GOALS de entrada/salida

G01 preservar `INPUT_RAW` byte-a-byte y hash estable.
G02 descomponer objetivos/tareas sin mutar el original.
G03 asignar owner único y dependencias explícitas.
G04 activar roles/domains/geo/language sólo cuando apliquen.
G05 investigar en paralelo mientras existen preguntas abiertas.
G06 reutilizar código/componentes antes de generar desde cero.
G07 mantener trazabilidad `source → ref/SHA → destino → versión`.
G08 separar conocimiento, código, skills y tools.
G09 mantener evidence/contradiction graph y GAPs visibles.
G10 recuperar desde checkpoint sin repetir nodos cerrados.
G11 cerrar sólo con test/log/hash/read-back según el tipo de tarea.
G12 entregar a la LLM principal contexto mínimo suficiente con provenance.

## 8. Ask Consil — 12 decisiones

C01 ¿El INPUT necesita aclaración? → score de ambigüedad; 0–12 preguntas.
C02 ¿Puede empezar presearch antes de respuesta? → sí, sólo ramas no dependientes de la aclaración.
C03 ¿Qué agente debe actuar? → capability router + owner lock.
C04 ¿Se necesita código nuevo? → primero inventario/COPY-FIRST.
C05 ¿Se necesita componente? → comprobar repo local, luego OSS externo.
C06 ¿Cómo evitar duplicación? → source hash + destination inventory + task claim.
C07 ¿Cómo evitar prompt enorme? → Code Pointer/Skill Pointer/Tool Card on-demand.
C08 ¿Cómo decidir calidad de fuente? → clase primaria/comunidad + autoridad/frescura/independencia.
C09 ¿Qué hacer con contradicciones? → no ocultarlas; abrir contradiction slot.
C10 ¿Qué hacer con bloqueo? → marcar flag, conservar evidencia y continuar nodo independiente.
C11 ¿Cómo mejorar sin romper? → patch/version nueva + comparación + rollback pointer.
C12 ¿Quién cierra? → Verdict/Gates basados en evidencia; ninguna LLM aislada.

## 9. Seis simulaciones

S1 INPUT claro de cocina → `CHEF` + fuentes culinarias; sin activar code lane.
S2 INPUT vago de arquitectura → Focus 3–12 preguntas mientras GitHub/docs/community presearch corre en paralelo.
S3 INPUT de programación → CODE + GITHUB + DEV_COMMUNITY + HF/LABS; Code Pointer RAG antes de cargar archivos completos.
S4 GAP en descarga por symlink/special-file → fail-closed del motor; no sobrescribir; StrategyDelta y continuar otro lote independiente.
S5 SOL y CLAUDE reclaman mismo adapter → owner lock deja uno CLAIMED y el otro recibe una tarea paralela.
S6 ASTRA encuentra regresión en V2 → V1 permanece; crea REVIEW/patch V2.1, ejecuta tests y sólo entonces puede promoverse.

## 10. Persistencia obligatoria

Cada cambio relevante actualiza, según corresponda: `STATE.json`, `CHECKPOINT.json`, `PLAN.json`, log del agente, `RECOVERY`, `README arquitectura`, índice de componentes y Handoff.

Evidencia mínima: ruta + commit/SHA o diff + test/log + URL/source ref + read-back cuando exista publicación.
