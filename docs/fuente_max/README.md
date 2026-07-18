# docs/fuente_max/ — Documentos fuente de Max (NCT Neuronas Code Turbo)

**Fuente de la verdad para programar el código del Osquestador.**

Estos 6 archivos fueron provistos directamente por Max en el turno del 2026-07-18 01:35 y constituyen la **especificación base** sobre la cual se programa el Osquestador. NO son исследоваción — son la constitución del proyecto que el Osquestador debe implementar.

---

## Índice de archivos

| # | Archivo | Tipo | Tamaño | Propósito |
|---|---------|------|--------|-----------|
| 01 | `01_RAIZ_MAESTRA_ORQUESTADOR_ESTRUCTURA_COMPLETA.md` | Markdown | 130 KB | **Raíz Maestra 00** — 14+ Checkpoints que definen la constitución, arquitectura documental, mapa mental, Crazy Wall, state.json, registro maestro, configuración global, perfil del proyecto, inicialización del orquestador, captura universal de input, input block, persistencia universal. **Es el documento MAESTRO de Max.** |
| 02 | `02_BIBLIOTECA_UNIVERSAL_CONOCIMIENTO_SKILLS.md` | Markdown | 77 KB | **Biblioteca Universal de Conocimiento** — Sistema inteligente de capacidades organizado por FASES del proyecto (FASE 03 Arquitectura → Clean Architecture/Microservicios; FASE 05 Desarrollo → Python/TypeScript/React; FASE 07 Seguridad). Cada elemento debe ser encontrado, comprendido, validado, ejecutado, combinado, actualizado, auditado. |
| 03 | `03_biblioteca-conocimiento.html` | HTML | 101 KB | Render visual de la biblioteca — incluye diagrama de flujo, ejemplos, estructura visual. |
| 04 | `04_ENGINE_DESTILACION_CONOCIMIENTO.md` | Markdown | 7 KB | **Knowledge Distillation Engine** (Engine 2) — Convierte conocimiento bruto (de investigaciones, conversaciones, repos) en activos profesionales documentados (skills + docs Markdown). Pipeline: recepción → análisis → destilación → creación. Regla: "Nunca crear un activo sin revisar primero la biblioteca." |
| 05 | `05_ENGINE_ADQUISICION_CONOCIMIENTO.md` | Markdown | 6 KB | **Knowledge Acquisition Engine** (Engine 1) — Investiga, busca fuentes, descarga información, analiza calidad, compara, clasifica. **NO puede** crear skills finales ni modificar biblioteca final. Regla: "Antes de investigar debe comprobar si el conocimiento ya existe." |
| 06 | `06_orquestador-estructura.html` | HTML | 181 KB | Render visual completo de la Raíz Maestra 00 — incluye todos los checkpoints, diagramas, artefactos. |

**Total:** 501 KB · 6 documentos

---

## Cómo se usan estos documentos en la programación del Osquestador

### Mapeo documento → módulo del Osquestador

| Documento | Módulo Python | Función |
|-----------|---------------|---------|
| 01 (Raíz Maestra 00) | `osquestador/checkpoints/` | Implementa los 14 Checkpoints como state machine determinístico |
| 02 (Biblioteca Universal) | `osquestador/biblioteca/` | Catálogo + REGISTRY.yaml + búsqueda |
| 03 (HTML biblioteca) | `osquestador/biblioteca/visual/` | UI render del catálogo (opcional) |
| 04 (Distillation Engine) | `osquestador/distillation/engine.py` | Convierte bruto en SKILL.md + scripts/ |
| 05 (Acquisition Engine) | `osquestador/acquisition/engine.py` | Investiga + descarga + clasifica |
| 06 (HTML orquestador) | `osquestador/docs/visual/` | Referencia visual |

### Relación con la regla 90% código / 10% LLM

- **90% código:** estos documentos se traducen en if/else + state machines + JSON Schemas + SQLite + Git. NO se interpretan con LLM en runtime.
- **10% LLM:** la sección "Constitución", "Misión", "Principios" del Checkpoint 00.01 se generan una vez (compile-time) con LLM, luego quedan como texto literal en el código.
- **Validación:** jsonschema contra los YAML definidos en estos documentos.

---

## Estado de implementación

- [ ] Checkpoint 00.01 Constitución → `osquestador/checkpoints/cp_001_constitucion.py`
- [ ] Checkpoint 00.02 Arquitectura Documental → `osquestador/checkpoints/cp_002_arquitectura_doc.py`
- [ ] Checkpoint 00.03 Mapa Mental Maestro → `osquestador/checkpoints/cp_003_mapa_mental.py`
- [ ] Checkpoint 00.04 Pizarra Global (Crazy Wall) → `osquestador/checkpoints/cp_004_crazy_wall.py`
- [ ] Checkpoint 00.05 Sistema de Estados → `osquestador/state/` (state.json)
- [ ] Checkpoint 00.06 Registro Maestro → `osquestador/registry/`
- [ ] Checkpoint 00.07 Configuración Global → `osquestador/config/`
- [ ] Checkpoint 00.08 Perfil del Proyecto → `osquestador/profile/`
- [ ] Checkpoint 00.09 Inicialización del Orquestador → `osquestador/bootstrap.py`
- [ ] Checkpoint 00.10 Artefactos Generados → `osquestador/artifacts/`
- [ ] Checkpoint 00.11 Captura Universal de Input → `osquestador/input/capture.py`
- [ ] Checkpoint 00.12 Input Block → `osquestador/input/block.py`
- [ ] Checkpoint 00.13 Perfil del Proyecto → `osquestador/profile/dynamic.py`
- [ ] Checkpoint 00.14 Registro Maestro de Checkpoints → `osquestador/checkpoints/registry.py`
- [ ] Ley Universal de Persistencia → `osquestador/persistence/` (SQLite WAL + Git auto-commit)
- [ ] Knowledge Acquisition Engine → `osquestador/acquisition/engine.py`
- [ ] Knowledge Distillation Engine → `osquestador/distillation/engine.py`
- [ ] Biblioteca Universal de Conocimiento → `osquestador/biblioteca/` (catalogador)

**Total a implementar:** 17+ módulos Python · ~2-3k líneas de código · 90% determinístico

---

## Regla de versionado

Estos documentos son **INMUTABLES** una vez commiteados al repo. Si Max envía una nueva versión, se commitea como `NN_nombre_v2.md` y se actualiza este README. El código del Osquestador siempre se programa contra la última versión aprobada.

---

**Aprobado por:** Max (turno 2026-07-18 01:35)
**Subido al repo:** commit `f7a9877+1` (siguiente)
**Propósito:** Fuente de la verdad para programar el Osquestador con la visión completa de Max.
