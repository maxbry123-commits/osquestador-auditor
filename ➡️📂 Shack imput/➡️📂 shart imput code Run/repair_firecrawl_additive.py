#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import shutil
import tempfile

BASE = pathlib.Path("➡️📂 Shack imput/➡️📂 shart imput code Run")
HELPER = BASE / "repair_ignored_publication.py"
REPORT = pathlib.Path("➡️📂 Shack imput/📂 Craxy wall bitácora stated JSON/FIRECRAWL-ADDITIVE-REPAIR.json")

spec = importlib.util.spec_from_file_location("repair_ignored_publication", HELPER)
if spec is None or spec.loader is None:
    raise SystemExit("HELPER_IMPORT_GAP")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

LANE = "search"
SLUG = "firecrawl"
EXPECTED_MISSING = 2
TARGET = mod.COMPONENTS / LANE / SLUG


def git_blob(path: pathlib.Path) -> str:
    return mod.run(["git", "hash-object", "--", path.as_posix()]).stdout.strip()


def main() -> int:
    manifest_path = TARGET / "DOWNLOAD_EXTRACT_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    source_repo = str(manifest["source_repo"]).removeprefix("https://github.com/")
    source_commit = str(manifest["source_commit"])
    expected_blobs = mod.source_blobs(source_repo, source_commit)
    mod.verify_archive_parts(TARGET, manifest)

    existing = {
        p.relative_to(TARGET / "code").as_posix()
        for p in (TARGET / "code").rglob("*")
        if p.is_file()
    }
    missing = sorted(set(expected_blobs) - existing)
    if len(missing) != EXPECTED_MISSING:
        raise RuntimeError(f"MISSING_COUNT_MISMATCH:expected={EXPECTED_MISSING} actual={len(missing)}")

    with tempfile.TemporaryDirectory(prefix="shark-firecrawl-additive-") as td:
        temp = pathlib.Path(td)
        extracted = temp / "extracted"
        missing_source = temp / "missing-source"

        env1 = dict(os.environ)
        env1.update({
            "ARCHIVE_INPUT": str(TARGET / "_archives"),
            "DEST_DIR": str(extracted),
            "STATE_FILE": str(temp / "extract-state.json"),
            "BATCH_SIZE": "100",
        })
        p1 = mod.run(["python3", str(mod.MOTOR1)], env=env1, check=False)
        v1 = mod.json_from_last_line(p1.stdout)
        if p1.returncode or v1.get("verdict") != "VERIFIED_CLOSED":
            raise RuntimeError("MOTOR1_NOT_CLOSED:" + json.dumps(v1, ensure_ascii=False))

        for rel in missing:
            src = extracted / pathlib.PurePosixPath(rel)
            if not src.is_file():
                raise RuntimeError(f"EXTRACTED_MISSING:{rel}")
            actual_blob = git_blob(src)
            if actual_blob != expected_blobs[rel]:
                raise RuntimeError(f"EXTRACTED_SOURCE_BLOB_MISMATCH:{rel}")
            dst = missing_source / pathlib.PurePosixPath(rel)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

        env3 = dict(os.environ)
        env3.update({
            "SOURCE_DIR": str(missing_source),
            "DEST_DIR": str(TARGET / "code"),
            "STATE_FILE": str(temp / "copy-state.json"),
            "BATCH_SIZE": "100",
            "COLLISION_POLICY": "fail",
        })
        p3 = mod.run(["python3", str(mod.MOTOR3)], env=env3, check=False)
        v3 = mod.json_from_last_line(p3.stdout)
        if p3.returncode or v3.get("verdict") != "VERIFIED_CLOSED":
            raise RuntimeError("MOTOR3_NOT_CLOSED:" + json.dumps(v3, ensure_ascii=False))

    mod.run(["git", "add", "-f", "--", (TARGET / "code").as_posix()])
    non_additive = mod.staged_paths(TARGET / "code", "DMRTUXB")
    if non_additive:
        raise RuntimeError("NON_ADDITIVE_CHANGE:" + json.dumps(non_additive, ensure_ascii=False))

    added_paths = mod.staged_paths(TARGET / "code", "A")
    prefix = (TARGET / "code").as_posix().rstrip("/") + "/"
    added = [p[len(prefix):] if p.startswith(prefix) else p for p in added_paths]
    if sorted(added) != missing:
        raise RuntimeError("STAGED_PATH_SET_MISMATCH:" + json.dumps({"expected": missing, "actual": sorted(added)}, ensure_ascii=False))
    for rel, staged in zip(sorted(added), sorted(added_paths)):
        if git_blob(pathlib.Path(staged)) != expected_blobs[rel]:
            raise RuntimeError(f"STAGED_SOURCE_BLOB_MISMATCH:{rel}")

    payload = {
        "schema": "wanted-shark.firecrawl-additive-repair.v2",
        "lane": LANE,
        "slug": SLUG,
        "source_repo": source_repo,
        "source_commit": source_commit,
        "missing_before": missing,
        "restored_files": len(added),
        "restored_paths": sorted(added),
        "motor_1": "VERIFIED_CLOSED",
        "motor_3": "VERIFIED_CLOSED",
        "policy": "ADDITIVE_ONLY + SOURCE_BLOB_MATCH + COLLISION_FAIL + NO_FORCE",
        "verdict": "READY_FOR_PUBLISH",
    }
    REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    mod.run(["git", "add", "--", REPORT.as_posix()])
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        mod.rollback_target(TARGET)
        payload = {
            "schema": "wanted-shark.firecrawl-additive-repair.v2",
            "error": str(exc),
            "verdict": "REPAIR_FAILED_CLOSED",
        }
        REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
        mod.run(["git", "add", "--", REPORT.as_posix()])
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        raise SystemExit(2)
