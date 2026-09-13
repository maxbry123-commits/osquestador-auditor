# M57 — TRIPLE AUDIT PACKET / SHARCK INPUT V2.1

Mode: `INDEPENDENT_CROSSCHECK / FAIL_CLOSED / NO_OVERENGINEERING`
Owners: `M06 ASTRA`, `M07 CLAUDE`, `M08 GROK`.

## COMMON OBJECTIVE
Auditar Sharck Input V2.1 como sistema PRE-LLM completo y determinar qué falta realmente para mejorar la calidad del `CONTEXT_PACKAGE` y llegar a un cierre demostrable, sin inflar arquitectura, sin duplicar componentes y sin confundir catálogo con integración.

La auditoría debe verificar la idea completa contra la realidad física del repo, no sólo contra documentación.

### Mandatory reading / inventory
1. inventariar raíz completa del repo y clasificar cada item: `SHARCK_RELEVANT | SHARED_PLATFORM | UNRELATED | UNKNOWN`.
2. leer `AGENTS.md`.
3. leer `PIPELINE/00_METODO_TRABAJO_Y_ARQUITECTURA.md`.
4. leer `PIPELINE/FORENSIC_CODE_AUDIT.md`.
5. leer `➡️📂 sharck imput/00-START-HERE-SHARCK-INPUT.md`.
6. leer `README-METODO-TRABAJO-MULTIAGENTE.md`.
7. leer `📁 readme arquitectura sharck imput V2.1.md`.
8. leer Handoff actual y current STATE/PLAN/CHECKPOINT/queue/watchdog/claims/logs/evidence relevantes.
9. inspeccionar código principal, manifests, component inventory y ports/adapters por pointers; no cargar 117 componentes completos sin necesidad.
10. contrastar los documentos con GitHub physical tree, hashes, runs y readback.

## 12 GOALS — INPUT AUDIT
G-IN-01 preservar objetivo PRE-LLM literal y separar Sharck de otros proyectos del repo.
G-IN-02 reconstruir arquitectura real `input→context package→main LLM` y sus feedback loops.
G-IN-03 verificar qué módulos/microkernels existen físicamente vs sólo documentados.
G-IN-04 mapear 117 catálogo → acquired → verified → wired → tested → promoted.
G-IN-05 reconstruir los 23 FAILED, 12 partial, 139 anomalies y causalidad sin heredar PASS.
G-IN-06 verificar source provenance, immutable refs, special files, licenses y supply-chain gates.
G-IN-07 revisar retrieval/index/rerank/evidence/contradiction/coverage/context compression como cadena de calidad.
G-IN-08 revisar ownership, queue, locks, checkpoints, watchdog y recuperación ante concurrencia/stale claims.
G-IN-09 revisar conflictos entre método raíz y método Sharck; proponer una sola precedencia ejecutable.
G-IN-10 revisar COPY-FIRST y si existe duplicación/monolito/abstracción innecesaria.
G-IN-11 comprobar qué evidencia falta para M06/M07/M08, repair, acquisition y Step3.
G-IN-12 definir baseline cuantificable para calidad, cobertura, latencia, contexto/tokens, reproducibilidad y operador.

## 12 GOALS — OUTPUT AUDIT
G-OUT-01 entregar `REAL_ARCHITECTURE_MAP`: componentes y flujos realmente respaldados por paths/evidencia.
G-OUT-02 entregar `DOC_VS_PHYSICAL_DRIFT`: todo lo documentado que ya no coincide con main.
G-OUT-03 entregar `MISSING_CRITICAL_CAPABILITIES`: sólo gaps que afecten el objetivo PRE-LLM.
G-OUT-04 entregar `OVERENGINEERING_PRUNE`: piezas/candidatos que deben podarse, fusionarse o mantenerse deferred.
G-OUT-05 entregar `TOP_10_FIXES`: máximo 10, priorizados por impacto/riesgo/esfuerzo.
G-OUT-06 entregar `PATH_TO_100_PASS`: gates y pruebas secuenciales mínimas, sin tareas decorativas.
G-OUT-07 entregar `TEST_MATRIX`: unit/contract/integration/e2e/replay/readback/negative paths requeridos.
G-OUT-08 entregar `QUALITY_SCORECARD`: métricas baseline→target y método de medición.
G-OUT-09 entregar `10X_CANDIDATES`: sólo mejoras cuyo beneficio 10x sea medible o falsable; si no se puede probar, marcar `NOT_VALIDATED_10X`.
G-OUT-10 entregar `RISKS_AND_ROLLBACKS`: failure modes y rollback mínimo por recomendación.
G-OUT-11 entregar `WHAT_NOT_TO_DO`: explícito, para evitar nuevos servicios/componentes sin necesidad.
G-OUT-12 emitir `REVIEW_PASS | REPAIR_REQUIRED | BLOCKED` con evidence pointers; nunca `VERIFIED_CLOSED` global por opinión.

## ASK COUNCIL — 12 DECISION STEPS
C01 ¿El objetivo real de Sharck está reflejado por el código actual o sólo por documentos?
C02 ¿Cuál es el hot path mínimo que produce mejor `CONTEXT_PACKAGE` hoy?
C03 ¿Qué piezas del pipeline son imprescindibles y cuáles son opcionales/deferred?
C04 ¿Dónde se pierde calidad: intent/entity/research/retrieval/rerank/evidence/compression/hand-off?
C05 ¿Qué gaps son físicos y cuáles son sólo falta de evidencia/control-plane?
C06 ¿Qué 23 failures deben repararse, reemplazarse, aceptar como nonrecoverable o sacar del camino crítico?
C07 ¿Qué candidatos B05/B06 agregan capacidad neta y cuáles duplican lo existente?
C08 ¿Qué contrato mínimo de ports/adapters evita acoplamiento sin crear framework extra?
C09 ¿Qué pruebas demuestran que el contexto mejora el resultado del LLM principal frente a baseline sin Sharck?
C10 ¿Qué métricas pueden demostrar 10x y cuáles no deben llamarse 10x?
C11 ¿Cuál es la secuencia mínima de gates para habilitar repair→acquisition→Step3 sin mezclar fases?
C12 ¿Qué evidencia faltante impide hoy un veredicto final y cuál es el siguiente nodo exacto?

## 3 REFUTATIONS — MANDATORY
R1 `Más componentes = mejor Sharck.` Debe intentar refutarlo con overlap, coste, failure surface y marginal utility.
R2 `17 VERIFIED_CLOSED y muchos contratos implican que el proyecto está casi terminado.` Debe refutar o demostrar usando wiring/tests/e2e, no conteo documental.
R3 `El control plane/watchdog puede compensar gaps del producto.` Debe refutar: control/evidence no sustituyen código, datos, adquisición, integración ni pruebas reales.

## DEBATE — MANDATORY
Cada auditor debe incluir dos columnas:
- `ARGUMENT_FOR`: mejor caso a favor de sus 5 recomendaciones principales.
- `ARGUMENT_AGAINST`: mejor caso en contra, incluyendo coste/duplicación/latencia/maintenance/risk.
Luego emitir `KEEP | MODIFY | REJECT` por recomendación.

SOL-0 realizará fan-in sólo después de recibir los 3 informes y resolver contradicciones; ninguna recomendación gana por mayoría sin evidencia.

## 4 SIMULATIONS — MANDATORY
S1 `INPUT CLARO`: input bien definido; Sharck debe evitar investigación/routers innecesarios y producir contexto mínimo.
S2 `INPUT VAGO/CONTRADICTORIO`: preguntas 0–12 + presearch independiente + contradiction slots; medir si evita alucinación/deriva.
S3 `PROGRAMMING/RESEARCH HEAVY`: GitHub/docs/community/code pointers; medir precision@k, provenance, token/context compression y reproducibilidad.
S4 `FAILURE/STALE SOURCE`: fuente desaparecida/symlink/gitignore/commit no recuperable; validar fail-closed, StrategyDelta, recovery y ausencia de falso PASS.

Cada simulación debe declarar: input, expected path, actual path/evidence, failure injection, expected verdict, measured gaps y siguiente fix mínimo.

## 10X VALIDATION CONTRACT
No usar “10x” como adjetivo. Una propuesta es `VALIDATED_10X` sólo si demuestra al menos una métrica con baseline y target >=10x o <=10% según naturaleza, sin degradar gates críticos.

Métricas candidatas:
- reducción de contexto/tokens manteniendo recall/answer quality;
- reducción de tiempo manual de recuperación/auditoría;
- aumento de coverage de anomalías/pruebas;
- reducción de false-PASS/failure escape rate;
- mejora de throughput de investigación con misma calidad/provenance;
- reducción de duplicated components/maintenance surface.

Si el beneficio es cualitativo o <10x: etiquetar `IMPROVEMENT`, no `10X`.

## NO-OVERENGINEERING GATE
Toda recomendación nueva responde YES a:
1. ¿Gap real y prioritario?
2. ¿No existe ya capability equivalente?
3. ¿COPY/ADAPT insuficiente?
4. ¿Contrato/adapter mínimo definido?
5. ¿Test que falla antes y pasa después?
6. ¿Rollback simple?
7. ¿Menor coste total que mantener el gap?

Si alguna respuesta es NO: `DEFER_OR_REJECT`.

# OWNER-SPECIFIC AUDITS

## M06 — ASTRA / ARCHITECTURE + GATES + SIMPLICITY
Focus: topología real, coherencia README↔code↔control-plane, coupling, gates, recovery, contradictions, exceso de capas y camino mínimo a cierre.
Output: `M06-M57-ASTRA-AUDIT-EVIDENCE.md`.
Debe señalar como mínimo: policy conflicts, stale docs, hidden dependencies, unnecessary abstractions, gate order, rollback architecture y 5 mejoras máximas.

## M07 — CLAUDE / CODE + PORTS + TESTS + COVERAGE
Focus: código ejecutable, ports/adapters, typing/contracts, COPY-FIRST, wiring real, failure paths, test coverage y gap entre catálogo/adquisición/integración.
Output: `M07-M57-CLAUDE-AUDIT-EVIDENCE.md`.
Debe producir: hot-path code map, dead/unwired surfaces, missing adapters, critical tests, exact files/functions implicated y 5 fixes máximos.

## M08 — GROK / OSS + LICENSE + SECURITY + OVERLAP
Focus: 117 + 20 candidatos B05/B06, overlap funcional, license/security/maintenance, alternatives, provenance y qué NO adquirir.
Output: `M08-M57-GROK-AUDIT-EVIDENCE.md`.
Debe producir: KEEP/DEFER/REJECT matrix, maintenance/license/security risks, duplicate capability map, external evidence pointers y 5 mejoras máximas.

## FINAL REPORT FORMAT — EACH MODEL
1. `VERDICT`.
2. `TOP 5 FINDINGS` con evidence pointers.
3. `12 GOALS INPUT` PASS/GAP.
4. `12 GOALS OUTPUT` PASS/GAP.
5. `COUNCIL12` decisiones.
6. `3 REFUTATIONS`.
7. `DEBATE TABLE`.
8. `4 SIMULATIONS`.
9. `10X VALIDATION TABLE`.
10. `TOP FIXES` máximo 5 del owner.
11. `DO NOT BUILD` lista.
12. `NEXT EXACT NODE`.

No editar shared STATE/PLAN/CHECKPOINT/Handoff. Sólo escribir el evidence file propio del owner. SOL-0 hará el fan-in después.
