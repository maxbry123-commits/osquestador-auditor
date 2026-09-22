# 🦈 HANDOFF M65 — TIMESFM 3 CAPABILITY

Fecha: 2026-09-22
Estado: `WIRED_STATIC_TEST_PASS / RUNTIME_MODEL_TEST_PENDING`
Repo: `maxbry123-commits/osquestador-auditor@main`
Raíz única: `➡️📂 sharck imput/`

## Cambio
Se añadió TimesFM 3 como capacidad especializada de forecasting, sin alterar la arquitectura M64 ni reducir paralelismo.

Ruta:
`YAIWES AGENT → KERNEL → CAPABILITY_DECISION → TIMESFM TOOL/SKILL → ROUTER INTELIGENTE UNIVERSAL → AI STAFF → TIMESFM 3.0 → FORECAST + QUANTILES → KERNEL → AGENT_DECISION`.

## Código
- `📂 input sharck code principal/📂 root-only-runtime/timesfm_capability.py`
- `📂 input sharck code principal/📂 root-only-runtime/TIMESFM-SKILL.md`
- `📂 input sharck code principal/📂 root-only-runtime/test_timesfm_capability.py`
- `📂 input sharck code principal/📂 root-only-runtime/timesfm_request.example.json`
- `sharck_root_runner.py` cableado con comandos `timesfm` y `test-timesfm`.

## Reglas
- PLAN_ONLY por defecto.
- Ejecución real exige `--execute` + runtime TimesFM + aceptación explícita de licencia.
- `commercial/production` se bloquea para el checkpoint TimesFM 3.0 configurado.
- forecast/cuantiles son evidencia probabilística, no hechos futuros.
- Router Universal/AI STAFF quedan como frontera externa referenciada; este nodo no escribe fuera de SHARCK.

## Validación
Contrato probado localmente: univariado, multivariado, horizonte, cuantiles y fallos de contrato.
No se declara runtime model PASS hasta ejecutar inferencia real con pesos/dependencias en el entorno de cómputo autorizado.
