#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path("➡️📂 Shack imput")
CODE = ROOT / "➡️📂 shart imput code Run"
WALL = ROOT / "📂 Craxy wall bitácora stated JSON"
RECOVERY = CODE / "queues" / "07-existing-destination-recovery.json"
REPORT = WALL / "RESIDUAL-GAP-AUDIT.json"
LANES = ["search", "code", "rag", "skills", "media-input-router", "orchestration"]


def classify(error: str) -> str:
    for code in ("DESTINATION_EXISTS", "READBACK_TREE_HASH_GAP", "SOURCE_SPECIAL_FILE_GAP"):
        if code in error:
            return code
    return "OTHER"


def main() -> None:
    recovered = {
        row["recovery_of"]
        for row in json.loads(RECOVERY.read_text()).get("queue", [])
        if row.get("recovery_of")
    }
    rows = []
    counts: dict[str, int] = {}
    lane_counts: dict[str, dict[str, int]] = {}
    failed_seen = 0

    for lane in LANES:
        state_path = WALL / f"download-{lane}-state.json"
        state = json.loads(state_path.read_text())
        lane_counts[lane] = {"baseline_failed": 0, "recovered": 0, "remaining": 0}
        for item_id, row in sorted(state.get("items", {}).items()):
            if row.get("status") != "FAILED":
                continue
            failed_seen += 1
            lane_counts[lane]["baseline_failed"] += 1
            if item_id in recovered:
                lane_counts[lane]["recovered"] += 1
                continue
            lane_counts[lane]["remaining"] += 1
            error = row.get("error", "")
            error_class = classify(error)
            counts[error_class] = counts.get(error_class, 0) + 1
            rows.append({
                "lane": lane,
                "item_id": item_id,
                "slug": row.get("slug", item_id),
                "source_repo": row.get("source_repo"),
                "error_class": error_class,
                "error": error[-3000:],
            })

    payload = {
        "schema": "wanted-shark.residual-gap-audit.v1",
        "baseline_failed": failed_seen,
        "verified_recoveries": len(recovered),
        "remaining_failed": len(rows),
        "remaining_failure_classes": counts,
        "lane_counts": lane_counts,
        "recovered_item_ids": sorted(recovered),
        "rows": rows,
        "verdict": "RESIDUAL_AUDIT_COMPLETE" if failed_seen - len(recovered) == len(rows) else "RECONCILIATION_MISMATCH",
    }
    REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({
        "verdict": payload["verdict"],
        "baseline_failed": failed_seen,
        "verified_recoveries": len(recovered),
        "remaining_failed": len(rows),
        "remaining_failure_classes": counts,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
