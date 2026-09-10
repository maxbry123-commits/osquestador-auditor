#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import urllib.request

ROOT = pathlib.Path("➡️📂 Shack imput")
CODE_ROOT = ROOT / "➡️📂 shart imput code Run"
WALL = ROOT / "📂 Craxy wall bitácora stated JSON"
DEST_ROOT = ROOT / "📂 Componentes para integración sharck imput"
REPORT = WALL / "ACQUISITION-GAP-AUDIT.json"
RECOVERY_QUEUE = CODE_ROOT / "queues" / "07-existing-destination-recovery.json"
TOKEN = os.getenv("GITHUB_TOKEN", "")
LANES = ["search", "code", "rag", "skills", "media-input-router", "orchestration"]


def run(argv: list[str], check: bool = True) -> str:
    p = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and p.returncode:
        raise RuntimeError(f"COMMAND_FAILED:{argv}:{p.stdout[-2000:]}")
    return p.stdout.strip()


def git_object_exists(path: pathlib.Path) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{path.as_posix()}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def git_read_json(path: pathlib.Path) -> dict:
    return json.loads(run(["git", "show", f"HEAD:{path.as_posix()}"]))


def api_json(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "wanted-shark-gap-audit"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def source_tree(repo: str, commit: str) -> tuple[dict[str, str], list[str]]:
    commit_obj = api_json(f"https://api.github.com/repos/{repo}/git/commits/{commit}")
    tree_sha = commit_obj["tree"]["sha"]
    tree = api_json(f"https://api.github.com/repos/{repo}/git/trees/{tree_sha}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("SOURCE_TREE_TRUNCATED")
    blobs: dict[str, str] = {}
    special: list[str] = []
    for row in tree.get("tree", []):
        kind = row.get("type")
        mode = row.get("mode")
        path = row.get("path", "")
        if kind == "blob" and mode in {"100644", "100755"}:
            blobs[path] = row["sha"]
        elif kind == "blob":
            special.append(path)
    return blobs, special


def destination_tree(prefix: pathlib.Path) -> dict[str, str]:
    prefix_s = prefix.as_posix().rstrip("/") + "/"
    text = run(["git", "ls-tree", "-r", "HEAD", "--", prefix.as_posix()])
    out: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        meta, fullpath = line.split("\t", 1)
        _mode, kind, sha = meta.split()
        if kind == "blob" and fullpath.startswith(prefix_s):
            out[fullpath[len(prefix_s):]] = sha
    return out


def classify_error(error: str) -> str:
    for code in ("DESTINATION_EXISTS", "READBACK_TREE_HASH_GAP", "SOURCE_SPECIAL_FILE_GAP"):
        if code in error:
            return code
    return "OTHER"


def main() -> None:
    audit_rows = []
    recovery = []
    class_counts: dict[str, int] = {}

    for lane in LANES:
        state_path = WALL / f"download-{lane}-state.json"
        if not state_path.exists():
            audit_rows.append({"lane": lane, "status": "STATE_MISSING"})
            continue
        state = json.loads(state_path.read_text())
        for item_id, row in sorted(state.get("items", {}).items()):
            if row.get("status") != "FAILED":
                continue
            error = row.get("error", "")
            error_class = classify_error(error)
            class_counts[error_class] = class_counts.get(error_class, 0) + 1
            slug = row.get("slug", item_id)
            dest = DEST_ROOT / lane / slug
            manifest_path = dest / "DOWNLOAD_EXTRACT_MANIFEST.json"
            manifest_exists = git_object_exists(manifest_path)
            destination_exists = bool(destination_tree(dest))
            result = {
                "lane": lane,
                "item_id": item_id,
                "slug": slug,
                "source_repo": row.get("source_repo"),
                "error_class": error_class,
                "destination_exists": destination_exists,
                "manifest_exists": manifest_exists,
                "audit_verdict": "NOT_AUDITED_FOR_EXISTING_DESTINATION",
            }

            if error_class not in {"DESTINATION_EXISTS", "READBACK_TREE_HASH_GAP"}:
                audit_rows.append(result)
                continue
            if not manifest_exists:
                result["audit_verdict"] = "EXISTING_DESTINATION_MANIFEST_MISSING"
                audit_rows.append(result)
                continue

            manifest = git_read_json(manifest_path)
            source_repo = manifest.get("source_repo") or row.get("source_repo")
            source_commit = manifest.get("source_commit")
            if not source_repo or not source_commit:
                result["audit_verdict"] = "SOURCE_TRACEABILITY_MISSING"
                audit_rows.append(result)
                continue

            try:
                src, special = source_tree(source_repo.removeprefix("https://github.com/"), source_commit)
                dst = destination_tree(dest / "code")
                missing = sorted(set(src) - set(dst))
                extra = sorted(set(dst) - set(src))
                changed = sorted(p for p in set(src) & set(dst) if src[p] != dst[p])
                result.update({
                    "source_commit": source_commit,
                    "source_files_git": len(src),
                    "destination_files_git": len(dst),
                    "source_special": special[:30],
                    "missing_count": len(missing),
                    "extra_count": len(extra),
                    "changed_count": len(changed),
                    "missing_sample": missing[:30],
                    "extra_sample": extra[:30],
                    "changed_sample": changed[:30],
                })
                if not special and not missing and not extra and not changed:
                    result["audit_verdict"] = "SOURCE_DEST_GIT_BLOBS_IDENTICAL"
                    recovery.append({
                        "id": f"recover-{lane}-{item_id}",
                        "source_repo": source_repo,
                        "source_ref": source_commit,
                        "slug": slug,
                        "publish": False,
                        "recovery_of": item_id,
                        "lane": lane,
                    })
                else:
                    result["audit_verdict"] = "SOURCE_DEST_MISMATCH"
            except Exception as exc:
                result["audit_verdict"] = "AUDIT_ERROR"
                result["audit_error"] = str(exc)
            audit_rows.append(result)

    payload = {
        "schema": "wanted-shark.acquisition-gap-audit.v1",
        "failed_total_seen": sum(class_counts.values()),
        "failure_classes": class_counts,
        "exact_existing_destinations": len(recovery),
        "recovery_queue": RECOVERY_QUEUE.as_posix(),
        "rows": audit_rows,
    }
    REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    RECOVERY_QUEUE.write_text(json.dumps({"queue": recovery}, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({
        "verdict": "AUDIT_COMPLETE",
        "failed_total_seen": payload["failed_total_seen"],
        "failure_classes": class_counts,
        "exact_existing_destinations": len(recovery),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
