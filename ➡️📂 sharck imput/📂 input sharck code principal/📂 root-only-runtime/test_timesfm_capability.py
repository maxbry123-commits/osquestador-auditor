#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("timesfm_capability.py")
spec = importlib.util.spec_from_file_location("timesfm_capability", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

req = {"series": [1,2,3,4,5,6,7,8,9,10], "horizon": 4, "use_case": "development"}
plan = mod.build_plan(req)
assert plan["capability"] == "forecast.timeseries.timesfm3"
assert plan["horizon"] == 4
assert plan["authority"] == "PROBABILISTIC_CONTEXT_NOT_FUTURE_FACT"
assert plan["quantile_levels"] == [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

multi = {"series": [[1,2,3,4,5,6,7,8], [2,3,4,5,6,7,8,9]], "horizon": 2}
assert mod.build_plan(multi)["target_variates"] == 2

for bad in (
    {"series": [1,2,3], "horizon": 2},
    {"series": [1,2,3,4,5,6,7,8], "horizon": 0},
    {"series": [1,2,3,4,5,6,7,8], "horizon": 2, "use_case": "production"},
):
    try:
        mod.build_plan(bad)
        raise AssertionError("invalid request accepted")
    except mod.ContractError:
        pass

print("PASS: TimesFM capability contract")
