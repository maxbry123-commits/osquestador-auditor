#!/usr/bin/env python3
"""Root-only TimesFM 3 capability adapter for SHARCK Input.

TimesFM forecasts are probabilistic context/evidence for YAIWES; they are not
authoritative future facts or autonomous decisions.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

CAPABILITY_ID = "forecast.timeseries.timesfm3"
MODEL_ID = "google/timesfm-3.0-pytorch"
SCHEMA = "yaiwes.timesfm-capability.v1"
QUANTILE_LEVELS = [round(i / 10, 1) for i in range(1, 10)]
ALLOWED_USE_CASES = {"research", "development", "noncommercial"}


class ContractError(ValueError):
    pass


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _shape(series: Any) -> str:
    if not isinstance(series, list) or not series:
        raise ContractError("series must be a non-empty list")
    if all(_is_number(x) for x in series):
        if len(series) < 8:
            raise ContractError("univariate series requires at least 8 historical points")
        return "univariate"
    if all(isinstance(row, list) and row for row in series):
        widths = {len(row) for row in series}
        if len(widths) != 1:
            raise ContractError("all multivariate rows must have the same context length")
        if next(iter(widths)) < 8:
            raise ContractError("multivariate series requires at least 8 historical points")
        if not all(_is_number(x) for row in series for x in row):
            raise ContractError("series contains non-numeric values")
        return "multivariate"
    raise ContractError("series must be numeric 1D or numeric 2D")


def validate_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ContractError("request must be a JSON object")
    shape = _shape(request.get("series"))
    horizon = request.get("horizon")
    if not isinstance(horizon, int) or isinstance(horizon, bool) or horizon < 1 or horizon > 1000:
        raise ContractError("horizon must be an integer between 1 and 1000")
    use_case = str(request.get("use_case", "noncommercial")).lower()
    if use_case not in ALLOWED_USE_CASES:
        raise ContractError(
            "TimesFM 3.0 checkpoint is configured only for research/development/noncommercial use; "
            "commercial or production use must route to a separately licensed backend."
        )
    return {
        **request,
        "use_case": use_case,
        "shape": shape,
        "return_quantiles": bool(request.get("return_quantiles", True)),
        "device": str(request.get("device", os.getenv("TIMESFM_DEVICE", "cpu"))),
        "per_core_batch_size": int(request.get("per_core_batch_size", 16)),
    }


def build_plan(request: dict[str, Any]) -> dict[str, Any]:
    req = validate_request(request)
    return {
        "schema": SCHEMA,
        "capability": CAPABILITY_ID,
        "model": MODEL_ID,
        "mode": "PLAN_ONLY",
        "input_shape": req["shape"],
        "context_length": len(req["series"]) if req["shape"] == "univariate" else len(req["series"][0]),
        "target_variates": 1 if req["shape"] == "univariate" else len(req["series"]),
        "horizon": req["horizon"],
        "return_quantiles": req["return_quantiles"],
        "quantile_levels": QUANTILE_LEVELS if req["return_quantiles"] else [],
        "device": req["device"],
        "route": [
            "YAIWES_AGENT", "KERNEL", "CAPABILITY_DECISION", "TIMESFM_SKILL_TOOL",
            "ROUTER_INTELIGENTE_UNIVERSAL", "AI_STAFF", "TIMESFM_3_0",
            "FORECAST_QUANTILES", "KERNEL", "AGENT_DECISION",
        ],
        "authority": "PROBABILISTIC_CONTEXT_NOT_FUTURE_FACT",
        "license_gate": "TIMESFM_3_LICENSE_ACCEPTED=1 required for local execution",
    }


def execute(request: dict[str, Any]) -> dict[str, Any]:
    req = validate_request(request)
    if os.getenv("TIMESFM_3_LICENSE_ACCEPTED") != "1":
        raise ContractError("execution blocked: set TIMESFM_3_LICENSE_ACCEPTED=1 only after accepting the TimesFM 3.0 checkpoint license")

    try:
        import numpy as np
        from timesfm3 import ModelConfig, TimesFM3Evaluator
    except Exception as exc:
        raise ContractError(f"TimesFM 3 runtime unavailable: {exc}") from exc

    config = ModelConfig(
        checkpoint_path=MODEL_ID,
        per_core_batch_size=req["per_core_batch_size"],
        device=req["device"],
    )
    forecaster = TimesFM3Evaluator(config)
    context = np.asarray(req["series"], dtype=np.float32)

    kwargs: dict[str, Any] = {
        "contexts": [context],
        "horizon": req["horizon"],
        "return_quantiles": req["return_quantiles"],
        "use_symmetric_averaging": bool(req.get("use_symmetric_averaging", False)),
    }
    if req.get("past_only_covariates") is not None:
        kwargs["past_only_covariates"] = [np.asarray(req["past_only_covariates"], dtype=np.float32)]
    if req.get("past_future_covariates") is not None:
        kwargs["past_future_covariates"] = [np.asarray(req["past_future_covariates"], dtype=np.float32)]

    output = list(forecaster.predict_batch(**kwargs))[0]
    quantiles = getattr(output, "quantiles", None)
    return {
        "schema": SCHEMA,
        "capability": CAPABILITY_ID,
        "model": MODEL_ID,
        "mode": "EXECUTED",
        "forecast": output.forecast.tolist(),
        "quantiles": quantiles.tolist() if quantiles is not None else None,
        "quantile_levels": QUANTILE_LEVELS if quantiles is not None else [],
        "horizon": req["horizon"],
        "authority": "PROBABILISTIC_CONTEXT_NOT_FUTURE_FACT",
    }


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    parser = argparse.ArgumentParser(description="SHARCK root-only TimesFM 3 capability")
    parser.add_argument("--input", required=True, help="JSON request file")
    parser.add_argument("--execute", action="store_true", help="Run TimesFM. Default is PLAN_ONLY.")
    args = parser.parse_args()
    try:
        request = load_json(Path(args.input))
        result = execute(request) if args.execute else build_plan(request)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(json.dumps({"schema": SCHEMA, "verdict": "GAP", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
