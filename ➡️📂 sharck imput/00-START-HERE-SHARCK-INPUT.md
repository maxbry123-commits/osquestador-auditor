# 🦈 SHARCK INPUT V2.1 — START HERE

Estado operativo: `ACTIVE / FAIL_CLOSED / M56_WORK_QUEUE + M57_TRIPLE_AUDIT`

## 1. Qué es Sharck Input
Sharck Input es una capa universal PRE-LLM. Su trabajo es preservar el input literal, detectar ambigüedad y conocimiento faltante, investigar con trazabilidad, capturar/normalizar/indexar evidencia, recuperar code/skills/tools por pointers, medir contradicción/cobertura/GAP y entregar al LLM principal un `CONTEXT_PACKAGE` mínimo suficiente y verificable.

Regla raíz: `LLM propone/razona; runtime controla; retriever encuentra; auditor cuestiona; evidence ledger prueba; verdict determinista autoriza`.

Pipeline maestro:
`INPUT_RAW → INPUT_LOCK → INTENT/CONSTRAINTS → ENTITY_RESOLUTION → RESEARCH_DECISION → FOCUS_A → QUESTIONS_0_12 || PRESEARCH → DOMAIN/ROLE/GEO/LANGUAGE ROUTER → RESEARCH_DAG → FAN_OUT SOURCES → CAPTURE/SNAPSHOT → EXTRACT/NORMALIZE → INDEX → BM25/SPARSE/DENSE → RRF/RERANK → EVIDENCE GRAPH → CONTRADICTION/COVERAGE/GAP → FOCUS_B → CODE/SKILL/TOOL POINTERS → CONTEXT_COMPRESSION → CONTEXT_PACKAGE → MAIN_LLM`.

## 2. Lectura mínima vigente
1. repo root `AGENTS.md`.
2. repo root `PIPELINE/00_METODO_TRABAJO_Y_ARQUITECTURA.md`.
3. repo root `PIPELINE/FORENSIC_CODE_AUDIT.md`.
4. `➡️📂 sharck imput/README-METODO-TRABAJO-MULTIAGENTE.md`.
5. `➡️📂 sharck imput/📁 readme arquitectura sharck imput V2.1.md`.
6. `➡️📂 sharck imput/HANDOFF-MULTIENV-3STEP-20X-2026-09-11.md`.
7. M56 current control files + fresh claims/log/evidence.
8. M57 audit packet when doing independent review.

## 3. Estado físico que NO debe maquillarse
- catálogo canónico: `117 = 77 legacy + 40 V2`.
- adquisición B01–B04: `17 VERIFIED_CLOSED / 23 FAILED / 0 pending`.
- failed: `12 partial destinations + 11 source-special/symlink`.
- partial exacto: `12 components / 139 anomalies`.
- B05/B06: `20 researched / 0 downloaded / 0 wired / 0 tested`.
- gates: `physical_repair_allowed=false`, `b05_b06_download_allowed=false`, `step3_allowed=false`.
- canonical motors: `IMMUTABLE`.

## 4. Trabajo vivo
Plano SOL: M56. `SW-N43` live claim; `SW-N44..SW-N46` son la continuación segura mientras permanezcan físicamente free.
Plano auditor: M57. `M06→ASTRA`, `M07→CLAUDE`, `M08→GROK` son auditorías independientes; no sustituyen ni reclaman nodos SOL.

## 5. Qué es histórico y no debe confundir al enjambre
Los deltas, recoveries, queues y watchdogs M47–M55 permanecen como evidencia histórica y trazabilidad. No son la puerta de entrada operativa si existe una versión posterior. No borrar: sólo dejar de leerlos primero.

Raíz histórica `➡️📂 Shack imput/`: referencia V1/read-only. No escribir allí.

## 6. Regla anti-sobreingeniería
Antes de añadir componente, servicio, cola, capa o abstracción nueva, demostrar:
1. GAP real no cubierto por lo existente;
2. COPY/ADAPT no resuelve;
3. beneficio medible;
4. coste operativo menor que el valor;
5. un rollback simple;
6. no duplicación de capability/port;
7. prueba mínima reproducible.

Si no se cumplen los siete puntos: `REJECT_OVERENGINEERING`.

## 7. Política ante conflicto de instrucciones
`GitHub physical truth + root AGENTS/PIPELINE + Sharck method + latest versioned control` prevalecen sobre snapshots viejos o chat. El watchdog puede continuar tareas ya autorizadas por la cola vigente; no puede crear trabajo físico nuevo, abrir gates ni sustituir aprobación del director para promoción/repair/acquisition/Step3.

## 8. Cierre global
Sharck NO llega a 100% porque un worker termine un nodo. 100% requiere: gates de review M06/M07/M08 resueltos, 23 fallos físicos re-clasificados o reparados con evidencia, adquisiciones necesarias cerradas, wiring mínimo, pruebas integrales/replay/readback, contradicciones resueltas o explícitamente aceptadas y VerdictAuthority final.

---

## 9. DIRECTOR OVERRIDE M62 — ROOT-ONLY

Para todo trabajo nuevo de SHARCK INPUT, la única raíz operativa autorizada es `➡️📂 sharck imput/` dentro de `maxbry123-commits/osquestador-auditor@main`.

Lectura operativa efectiva para esta Tarea 1:
1. `➡️📂 sharck imput/00-START-HERE-SHARCK-INPUT.md`
2. `➡️📂 sharck imput/📁 readme arquitectura sharck imput V2.1.md` — sección 11 contiene el INPUT BLOCK literal del Director.
3. `➡️📂 sharck imput/HANDOFF-MULTIENV-3STEP-20X-2026-09-11.md`
4. `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/M62-TASK1-ROOT-ONLY-ARCHITECTURE-WIRING.json`
5. archivos de código/componentes/estado exclusivamente bajo `➡️📂 sharck imput/`.

Las referencias históricas anteriores a archivos fuera de esta raíz se conservan sólo como historia documental; **no autorizan lectura de trabajo, escritura, integración ni mezcla fuera de `➡️📂 sharck imput/` para esta tarea y las siguientes de SHARCK INPUT**. Un motor externo únicamente puede copiarse dentro de esta raíz cuando corresponda.

---

## 10. M63 — TAREA 2 / 100X / ROOT-ONLY

Lectura prioritaria nueva:
1. `➡️📂 sharck imput/📁 readme arquitectura sharck imput V2.1.md` → secciones 11 y 12.
2. `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/M63-TASK2-100X-RESEARCH-ARCHITECTURE.md`.
3. `➡️📂 sharck imput/📂 Craxy wall bitácora stated JSON/M63-TASK2-100X-RESEARCH-ARCHITECTURE.json`.
4. `➡️📂 sharck imput/HANDOFF-MULTIENV-3STEP-20X-2026-09-11.md` → HANDOFF M63.
5. `➡️📂 sharck imput/📂 input sharck code principal/📂 root-only-runtime/sharck_root_runner.py`.
6. `➡️📂 sharck imput/📂 motores canónicos copiados/`.
7. `➡️📂 sharck imput/📂 workflows reubicados/README.md`.

Regla vigente: `100x` es target medible y sólo puede ser PASS con benchmark físico. Los 10–100+ microagentes son fan-out dinámico bajo governor, no cuota fija. Tarea 2 no abre Tarea 3/4/5 automáticamente.
