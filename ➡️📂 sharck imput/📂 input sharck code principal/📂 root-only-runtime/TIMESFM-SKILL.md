# YAIWES TimesFM 3 — Agent Skill / Tool Contract

Estado: `M65 / ROOT_ONLY / ADDITIVE_ONLY`

## Objetivo
Usar TimesFM 3 como capacidad especializada de forecasting de series temporales. No es un agente autónomo ni una fuente de verdad futura.

## Ruta canónica
`YAIWES AGENT → KERNEL → CAPABILITY_DECISION → TIMESFM TOOL/SKILL → ROUTER INTELIGENTE UNIVERSAL → AI STAFF → TIMESFM 3.0 → FORECAST + QUANTILES → KERNEL → DECISIÓN DEL AGENTE`

Dentro de SHARCK Input esta integración sólo emite/ejecuta la capacidad y devuelve contexto probabilístico. No mueve ni modifica código de otros repos.

## Cuándo activar
Activar únicamente cuando el contrato de entrada declare `forecast.timeseries.timesfm3` o aporte una serie temporal histórica válida + horizonte. No activar para preguntas generales sin datos temporales.

## Contrato mínimo
```json
{
  "series": [1,2,3,4,5,6,7,8],
  "horizon": 4,
  "use_case": "development",
  "return_quantiles": true
}
```

También acepta matrices `(num_variates, context_length)` y covariables opcionales `past_only_covariates` / `past_future_covariates`.

## Salida
- forecast;
- cuantiles 0.1…0.9 cuando estén habilitados;
- horizonte;
- identificador del modelo;
- marca obligatoria `PROBABILISTIC_CONTEXT_NOT_FUTURE_FACT`.

## Gates
1. PLAN_ONLY por defecto.
2. `--execute` requiere runtime TimesFM 3 y `TIMESFM_3_LICENSE_ACCEPTED=1`.
3. La configuración incluida bloquea `commercial` y `production` para el checkpoint 3.0.
4. Errores de runtime/licencia/dependencia → `GAP`; nunca convertir a PASS textual.
5. Forecast y cuantiles vuelven al kernel como evidencia probabilística; el agente conserva la decisión.

## Fuentes oficiales verificadas
- https://github.com/google-research/timesfm
- https://huggingface.co/google/timesfm-3.0-pytorch
- https://www.research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/
