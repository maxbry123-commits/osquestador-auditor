#!/usr/bin/env python3
from __future__ import annotations

import functools
import json
import os
import pathlib
import subprocess
import urllib.parse
import urllib.request

ROOT = pathlib.Path("➡️📂 Shack imput")
CODE_ROOT = ROOT / "➡️📂 shart imput code Run"
WALL = ROOT / "📂 Craxy wall bitácora stated JSON"
DEST_ROOT = ROOT / "📂 Componentes para integración sharck imput"
REPORT = WALL / "ACQUISITION-GAP-AUDIT.json"
RECOVERY_QUEUE = CODE_ROOT / "queues" / "07-existing-destination-recovery.json"
TOKEN = os.getenv("GITHUB_TOKEN", "")
DEST_REPO = os.getenv("GITHUB_REPOSITORY", "maxbry123-commits/osquestador-auditor")
DEST_REF = os.getenv("DEST_REF") or os.getenv("GITHUB_SHA") or run(["git", "rev-parse", "HEAD"])
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


@functools.lru_cache(maxsize=1024)
def api_tree(repo: str, tree_sha: str, recursive: bool = False) -> dict:
    suffix = "?recursive=1" if recursive else ""
    return api_json(f"https://api.github.com/repos/{repo}/git/trees/{tree_sha}{suffix}")


def commit_tree_sha(repo: str, ref: str) -> str:
    obj = api_json(f"https://api.github.com/repos/{repo}/git/commits/{urllib.parse.quote(ref, safe='')}")
    return obj["tree"]["sha"]


def subtree_sha(repo: str, ref: str, path: pathlib.PurePosixPath) -> str | None:
    current = commit_tree_sha(repo, ref)
    for part in path.parts:
        tree = api_tree(repo, current, False)
        match = next((x for x in tree.get("tree", []) if x.get("path") == part and x.get("type") == "tree"), None)
        if not match:
            return None
        current = match["sha"]
    return current


def repo_subtree(repo: str, ref: str, path: pathlib.PurePosixPath) -> tuple[dict[str, str], list[str]]:
    sha = subtree_sha(repo, ref, path)
    if not sha:
        return {}, []
    tree = api_tree(repo, sha, True)
    if tree.get("truncated"):
        raise RuntimeError("DESTINATION_TREE_TRUNCATED")
    blobs: dict[str, str] = {}
    special: list[str] = []
    for row in tree.get("tree", []):
        kind = row.get("type")
        mode = row.get("mode")
        rel = row.get("path", "")
        if kind == "blob" and mode in {"100644", "100755"}:
            blobs[rel] = row["sha"]
        elif kind == "blob":
            special.append(rel)
    return blobs, special


def source_tree(repo: str, commit: str) -> tuple[dict[str, str], list[str]]:
    root_sha = commit_tree_sha(repo, commit)
    tree = api_tree(repo, root_sha, True)
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
            result = {
                "lane": lane,
                "item_id": item_id,
                "slug": slug,
                "source_repo": row.get("source_repo"),
                "error_class": error_class,
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
            source_repo = (manifest.get("source_repo") or row.get("source_repo") or "").removeprefix("https://github.com/")
            source_commit = manifest.get("source_commit")
            if not source_repo or not source_commit:
                result["audit_verdict"] = "SOURCE_TRACEABILITY_MISSING"
                audit_rows.append(result)
                continue

            try:
                src, source_special = source_tree(source_repo, source_commit)
                dst, dest_special = repo_subtree(DEST_REPO, DEST_REF, pathlib.PurePosixPath((dest / "code").as_posix()))
                missing = sorted(set(src) - set(dst))
                extra = sorted(set(dst) - set(src))
                changed = sorted(p for p in set(src) & set(dst) if src[p] != dst[p])
                result.update({
                    "source_commit": source_commit,
                    "source_files_git": len(src),
                    "destination_files_git": len(dst),
                    "source_special": source_special[:30],
                    "destination_special": dest_special[:30],
                    "missing_count": len(missing),
                    "extra_count": len(extra),
                    "changed_count": len(changed),
                    "missing_sample": missing[:30],
                    "extra_sample": extra[:30],
                    "changed_sample": changed[:30],
                })
                if not source_special and not dest_special and not missing and not extra and not changed:
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
        "schema": "wanted-shark.acquisition-gap-audit.v3",
        "destination_ref": DEST_REF,
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
        "destination_ref": DEST_REF,
        "failed_total_seen": payload["failed_total_seen"],
        "failure_classes": class_counts,
        "exact_existing_destinations": len(recovery),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
