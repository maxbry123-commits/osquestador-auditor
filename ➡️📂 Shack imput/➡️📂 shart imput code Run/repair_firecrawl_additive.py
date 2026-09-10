#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, pathlib

BASE = pathlib.Path("➡️📂 Shack imput/➡️📂 shart imput code Run")
HELPER = BASE / "repair_ignored_publication.py"
REPORT = pathlib.Path("➡️📂 Shack imput/📂 Craxy wall bitácora stated JSON/FIRECRAWL-ADDITIVE-REPAIR.json")

spec = importlib.util.spec_from_file_location("repair_ignored_publication", HELPER)
if spec is None or spec.loader is None:
    raise SystemExit("HELPER_IMPORT_GAP")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

row = {"lane": "search", "slug": "firecrawl", "missing_count": 2}
try:
    result = mod.repair_one(row)
    payload = {"schema": "wanted-shark.firecrawl-additive-repair.v1", "result": result, "verdict": "READY_FOR_PUBLISH"}
except Exception as exc:
    mod.rollback_target(mod.COMPONENTS / "search" / "firecrawl")
    payload = {"schema": "wanted-shark.firecrawl-additive-repair.v1", "error": str(exc), "verdict": "REPAIR_FAILED_CLOSED"}
REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
mod.run(["git", "add", "--", REPORT.as_posix()])
print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if payload["verdict"] == "READY_FOR_PUBLISH" else 2)
