#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import tempfile
import urllib.request

ROOT = pathlib.Path("➡️📂 Shack imput")
CODE_ROOT = ROOT / "➡️📂 shart imput code Run"
WALL = ROOT / "📂 Craxy wall bitácora stated JSON"
COMPONENTS = ROOT / "📂 Componentes para integración sharck imput"
AUDIT = WALL / "ACQUISITION-GAP-AUDIT.json"
RESULT = WALL / "IGNORED-PUBLICATION-REPAIR.json"
MOTOR_ROOT = pathlib.Path("➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor")
MOTOR1 = MOTOR_ROOT / "➡️📂 Motor de extracción zip" / "motor_1_extract_only.py"
MOTOR3 = MOTOR_ROOT / "➡️📂motor de copiar archivos" / "motor_3_copy_batches.py"
TOKEN = os.getenv("GITHUB_TOKEN", "")


def run(argv: list[str], *, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(argv, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and p.returncode:
        raise RuntimeError(f"COMMAND_FAILED:{argv}:{p.stdout[-3000:]}")
    return p


def run_bytes(argv: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and p.returncode:
        tail = p.stdout[-3000:].decode("utf-8", errors="replace")
        raise RuntimeError(f"COMMAND_FAILED:{argv}:{tail}")
    return p


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def api_json(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "wanted-shark-ignore-repair"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
        return json.load(r)


def source_blobs(repo: str, commit: str) -> dict[str, str]:
    obj = api_json(f"https://api.github.com/repos/{repo}/git/commits/{commit}")
    tree_sha = obj["tree"]["sha"]
    tree = api_json(f"https://api.github.com/repos/{repo}/git/trees/{tree_sha}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("SOURCE_TREE_TRUNCATED")
    return {
        row["path"]: row["sha"]
        for row in tree.get("tree", [])
        if row.get("type") == "blob" and row.get("mode") in {"100644", "100755"}
    }


def json_from_last_line(text: str) -> dict:
    for line in reversed([x.strip() for x in text.splitlines() if x.strip()]):
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    raise RuntimeError("NO_JSON_VERDICT")


def extend_sparse(targets: list[pathlib.Path]) -> None:
    info = pathlib.Path(".git/info/sparse-checkout")
    existing = info.read_text() if info.exists() else ""
    with info.open("a") as fh:
        for target in targets:
            pattern = f"/{target.as_posix()}/\n"
            if pattern not in existing:
                fh.write(pattern)
    run(["git", "read-tree", "-mu", "HEAD"])


def verify_archive_parts(target: pathlib.Path, manifest: dict) -> None:
    archive_dir = target / "_archives"
    for row in manifest.get("parts", []):
        part = archive_dir / row["name"]
        if not part.is_file():
            raise RuntimeError(f"ARCHIVE_PART_MISSING:{part}")
        actual = sha256_file(part)
        if actual != row["sha256"]:
            raise RuntimeError(f"ARCHIVE_PART_HASH_MISMATCH:{part.name}")


def rollback_target(target: pathlib.Path) -> None:
    run(["git", "reset", "HEAD", "--", target.as_posix()], check=False)
    run(["git", "checkout", "--", target.as_posix()], check=False)
    run(["git", "clean", "-fdx", "--", (target / "code").as_posix()], check=False)


def staged_paths(target: pathlib.Path, diff_filter: str) -> list[str]:
    raw = run_bytes([
        "git", "diff", "--cached", "--name-only", "-z", f"--diff-filter={diff_filter}", "--", target.as_posix()
    ]).stdout
    return [item.decode("utf-8", errors="strict") for item in raw.split(b"\0") if item]


def repair_one(row: dict) -> dict:
    lane = row["lane"]
    slug = row["slug"]
    target = COMPONENTS / lane / slug
    manifest_path = target / "DOWNLOAD_EXTRACT_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    source_repo = str(manifest["source_repo"]).removeprefix("https://github.com/")
    source_commit = manifest["source_commit"]
    expected_blobs = source_blobs(source_repo, source_commit)
    verify_archive_parts(target, manifest)

    with tempfile.TemporaryDirectory(prefix=f"shark-repair-{slug}-") as td:
        temp = pathlib.Path(td)
        extracted = temp / "extracted"
        env1 = dict(os.environ)
        env1.update({
            "ARCHIVE_INPUT": str(target / "_archives"),
            "DEST_DIR": str(extracted),
            "STATE_FILE": str(temp / "extract-state.json"),
            "BATCH_SIZE": "100",
        })
        p1 = run(["python3", str(MOTOR1)], env=env1, check=False)
        v1 = json_from_last_line(p1.stdout)
        if p1.returncode or v1.get("verdict") != "VERIFIED_CLOSED":
            raise RuntimeError("MOTOR1_NOT_CLOSED:" + json.dumps(v1, ensure_ascii=False))

        env3 = dict(os.environ)
        env3.update({
            "SOURCE_DIR": str(extracted),
            "DEST_DIR": str(target / "code"),
            "STATE_FILE": str(temp / "copy-state.json"),
            "BATCH_SIZE": "100",
            "COLLISION_POLICY": "fail",
        })
        p3 = run(["python3", str(MOTOR3)], env=env3, check=False)
        v3 = json_from_last_line(p3.stdout)
        if p3.returncode or v3.get("verdict") != "VERIFIED_CLOSED":
            raise RuntimeError("MOTOR3_NOT_CLOSED:" + json.dumps(v3, ensure_ascii=False))

    run(["git", "add", "-f", "--", (target / "code").as_posix()])
    non_additive = staged_paths(target / "code", "DMRTUXB")
    if non_additive:
        raise RuntimeError("NON_ADDITIVE_CHANGE:" + json.dumps(non_additive, ensure_ascii=False))

    added_paths = staged_paths(target / "code", "A")
    added: list[str] = []
    prefix = (target / "code").as_posix().rstrip("/") + "/"
    for path in added_paths:
        rel = path[len(prefix):] if path.startswith(prefix) else path
        added.append(rel)
        actual_blob = run(["git", "hash-object", "--", path]).stdout.strip()
        if expected_blobs.get(rel) != actual_blob:
            raise RuntimeError(f"STAGED_SOURCE_BLOB_MISMATCH:{rel}")

    if len(added) != int(row.get("missing_count", -1)):
        raise RuntimeError(f"MISSING_COUNT_MISMATCH:expected={row.get('missing_count')} staged={len(added)}")
    return {
        "lane": lane,
        "slug": slug,
        "source_repo": source_repo,
        "source_commit": source_commit,
        "restored_files": len(added),
        "restored_paths": added,
        "motor_1": "VERIFIED_CLOSED",
        "motor_3": "VERIFIED_CLOSED",
        "verdict": "READY_FOR_PUBLISH",
    }


def main() -> None:
    audit = json.loads(AUDIT.read_text())
    candidates = [
        row for row in audit.get("rows", [])
        if row.get("audit_verdict") == "SOURCE_DEST_MISMATCH"
        and int(row.get("missing_count", 0)) > 0
        and int(row.get("changed_count", 0)) == 0
        and int(row.get("extra_count", 0)) == 0
        and not row.get("source_special")
        and not row.get("destination_special")
        and row.get("manifest_exists") is True
    ]
    targets = [COMPONENTS / row["lane"] / row["slug"] for row in candidates]
    extend_sparse(targets)

    results = []
    for row in candidates:
        target = COMPONENTS / row["lane"] / row["slug"]
        try:
            results.append(repair_one(row))
        except Exception as exc:
            rollback_target(target)
            results.append({
                "lane": row.get("lane"),
                "slug": row.get("slug"),
                "verdict": "REPAIR_FAILED_CLOSED",
                "error": str(exc),
            })

    payload = {
        "schema": "wanted-shark.ignored-publication-repair.v2",
        "audit_schema": audit.get("schema"),
        "candidates": len(candidates),
        "ready_for_publish": sum(1 for x in results if x.get("verdict") == "READY_FOR_PUBLISH"),
        "failed_closed": sum(1 for x in results if x.get("verdict") == "REPAIR_FAILED_CLOSED"),
        "results": results,
    }
    RESULT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    run(["git", "add", "--", RESULT.as_posix()])
    print(json.dumps({k: payload[k] for k in ("candidates", "ready_for_publish", "failed_closed")}, sort_keys=True))


if __name__ == "__main__":
    main()
