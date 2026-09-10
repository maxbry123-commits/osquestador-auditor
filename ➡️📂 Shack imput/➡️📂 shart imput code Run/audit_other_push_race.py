#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

from acquisition_gap_audit import (
    DEST_REF,
    DEST_REPO,
    DEST_ROOT,
    ROOT,
    WALL,
    git_object_exists,
    git_read_json,
    repo_subtree,
    source_tree,
)

RESIDUAL = WALL / "RESIDUAL-GAP-AUDIT.json"
REPORT = WALL / "OTHER-PUSH-RACE-AUDIT.json"
RECOVERY_QUEUE = ROOT / "➡️📂 shart imput code Run" / "queues" / "08-other-push-race-recovery.json"


def is_push_race(error: str) -> bool:
    needles = (
        "fetch first",
        "cannot lock ref 'refs/heads/main'",
        "failed to push some refs",
    )
    return "COMMAND_FAILED:git:1" in error and any(x in error for x in needles)


def audit_row(row: dict) -> dict:
    lane = row["lane"]
    slug = row["slug"]
    item_id = row["item_id"]
    result = {
        "item_id": item_id,
        "lane": lane,
        "slug": slug,
        "source_repo": row.get("source_repo"),
        "failure_kind": "PUSH_RACE" if is_push_race(row.get("error", "")) else "OTHER_NON_PUSH_RACE",
        "verdict": "NOT_RECOVERABLE_BY_READBACK",
    }
    if result["failure_kind"] != "PUSH_RACE":
        return result

    dest = DEST_ROOT / lane / slug
    manifest_path = dest / "DOWNLOAD_EXTRACT_MANIFEST.json"
    if not git_object_exists(manifest_path):
        result["verdict"] = "MANIFEST_MISSING_RETRY_REQUIRED"
        return result

    manifest = git_read_json(manifest_path)
    source_repo = (manifest.get("source_repo") or row.get("source_repo") or "").removeprefix("https://github.com/")
    source_commit = manifest.get("source_commit")
    result["source_commit"] = source_commit
    if not source_repo or not source_commit:
        result["verdict"] = "SOURCE_TRACEABILITY_MISSING"
        return result

    src, source_special = source_tree(source_repo, source_commit)
    dst, dest_special = repo_subtree(DEST_REPO, DEST_REF, pathlib.PurePosixPath((dest / "code").as_posix()))
    missing = sorted(set(src) - set(dst))
    extra = sorted(set(dst) - set(src))
    changed = sorted(p for p in set(src) & set(dst) if src[p] != dst[p])
    result.update({
        "source_files_git": len(src),
        "destination_files_git": len(dst),
        "source_special_count": len(source_special),
        "destination_special_count": len(dest_special),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "changed_count": len(changed),
        "missing_sample": missing[:20],
        "extra_sample": extra[:20],
        "changed_sample": changed[:20],
    })
    if not source_special and not dest_special and not missing and not extra and not changed:
        result["verdict"] = "EXACT_REMOTE_READBACK_VERIFIED"
    else:
        result["verdict"] = "REMOTE_DESTINATION_MISMATCH"
    return result


def main() -> None:
    residual = json.loads(RESIDUAL.read_text())
    candidates = [r for r in residual.get("rows", []) if r.get("error_class") == "OTHER"]
    rows = []
    recover = []
    for row in candidates:
        try:
            out = audit_row(row)
        except Exception as exc:
            out = {
                "item_id": row.get("item_id"),
                "lane": row.get("lane"),
                "slug": row.get("slug"),
                "source_repo": row.get("source_repo"),
                "failure_kind": "PUSH_RACE" if is_push_race(row.get("error", "")) else "OTHER_NON_PUSH_RACE",
                "verdict": "AUDIT_ERROR",
                "error": str(exc),
            }
        rows.append(out)
        if out.get("verdict") == "EXACT_REMOTE_READBACK_VERIFIED":
            recover.append({
                "id": f"recover-{out['item_id']}",
                "lane": out["lane"],
                "slug": out["slug"],
                "source_repo": out["source_repo"],
                "source_ref": out.get("source_commit"),
                "publish": False,
                "recovery_of": out["item_id"],
            })

    payload = {
        "schema": "wanted-shark.other-push-race-audit.v1",
        "destination_ref": DEST_REF,
        "other_candidates": len(candidates),
        "push_race_candidates": sum(r.get("failure_kind") == "PUSH_RACE" for r in rows),
        "exact_remote_readback_verified": len(recover),
        "rows": rows,
        "verdict": "AUDIT_COMPLETE",
    }
    REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    RECOVERY_QUEUE.write_text(json.dumps({"queue": recover}, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({k: payload[k] for k in ("verdict", "other_candidates", "push_race_candidates", "exact_remote_readback_verified")}, sort_keys=True))


if __name__ == "__main__":
    main()
