#!/usr/bin/env python3
"""SHARCK case engine for canonical Motor 2.

This wrapper does NOT modify the immutable canonical engine. It adds only:
1) safe in-root symlink materialization before canonical scan/package;
2) executable-bit restoration after canonical ZIP extraction;
3) repair publication for an existing destination using git add -f so ignored
   source files are not silently omitted.

Acquisition is still performed by the canonical engine's acquire() implementation.
No GitHub Actions and no Hugging Face Jobs are used by this wrapper.
"""
from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import shutil
import stat
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve()
SHARCK_ROOT = HERE.parents[1]
ENGINE = pathlib.Path(
    os.getenv(
        "CANONICAL_ENGINE_PATH",
        str(SHARCK_ROOT / "📂 motores canónicos copiados" / "hf_download_extract_engine.py"),
    )
)
REPAIR_EXISTING = os.getenv("REPAIR_EXISTING", "1").lower() in {"1", "true", "yes"}


def _inside(child: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        child.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def _symlinks(root: pathlib.Path) -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for current, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        cur = pathlib.Path(current)
        for name in list(dirnames) + list(filenames):
            p = cur / name
            if p.is_symlink():
                found.append(p)
    return sorted(found, key=lambda p: (len(p.parts), p.as_posix()), reverse=True)


def deref_in_root(root: pathlib.Path) -> int:
    """Materialize only symlinks whose resolved target remains inside root."""
    root = root.resolve()
    links = _symlinks(root)
    for p in links:
        try:
            target = p.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise RuntimeError("SYMLINK_UNRESOLVED:" + p.relative_to(root).as_posix()) from exc
        if not _inside(target, root):
            raise RuntimeError("SYMLINK_ESCAPES_TREE:" + p.relative_to(root).as_posix())
        try:
            p.relative_to(target)
            raise RuntimeError("SYMLINK_CYCLE_GAP:" + p.relative_to(root).as_posix())
        except ValueError:
            pass

    done = 0
    for p in links:
        if not p.is_symlink():
            continue
        target = p.resolve(strict=True)
        mode = stat.S_IMODE(target.stat().st_mode)
        if target.is_dir():
            p.unlink()
            shutil.copytree(target, p, symlinks=False)
        elif target.is_file():
            data = target.read_bytes()
            p.unlink()
            p.write_bytes(data)
            p.chmod(mode)
        else:
            raise RuntimeError("SYMLINK_SPECIAL_TARGET:" + p.relative_to(root).as_posix())
        done += 1
    return done


def load_engine():
    if not ENGINE.is_file():
        raise RuntimeError("CANONICAL_ENGINE_MISSING:" + str(ENGINE))
    spec = importlib.util.spec_from_file_location("yaiwes_canonical_engine", ENGINE)
    eng = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(eng)
    return eng


def install_overrides(eng):
    original_acquire = eng.acquire

    def acquire_case(work):
        src, commit = original_acquire(work)
        count = deref_in_root(src)
        os.environ["YAIWES_DEREF_COUNT"] = str(count)
        return src, commit

    def safe_extract_case(bundle, dst):
        dst.mkdir()
        with zipfile.ZipFile(bundle) as z:
            for info in z.infolist():
                name = info.filename.replace("\\", "/")
                q = pathlib.PurePosixPath(name)
                if q.is_absolute() or ".." in q.parts:
                    raise RuntimeError("UNSAFE_ZIP_PATH:" + name)
                ftype = (info.external_attr >> 16) & 0o170000
                if ftype in {stat.S_IFLNK, stat.S_IFCHR, stat.S_IFBLK, stat.S_IFIFO, stat.S_IFSOCK}:
                    raise RuntimeError("UNSAFE_ZIP_SPECIAL:" + name)
                out = dst / pathlib.Path(*q.parts)
                if info.is_dir():
                    out.mkdir(parents=True, exist_ok=True)
                    continue
                out.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as r, out.open("wb") as w:
                    shutil.copyfileobj(r, w, 1024 * 1024)
                mode = (info.external_attr >> 16) & 0o777
                out.chmod(mode or 0o644)
        eng.scan_tree(dst, enforce_blob_limit=True)

    def publish_case(work, parts_dir, extracted, manifest_path, slug):
        if not eng.TOKEN:
            return {"verdict": "WRITE_AUTH_GAP", "detail": "GITHUB_TOKEN is not available"}
        env = eng.auth_env()
        rel = (pathlib.Path(eng.DEST_ROOT) / slug).as_posix()
        dst = work / "destination"
        eng.sparse_checkout(dst, eng.DEST_REPO, eng.DEST_BRANCH, rel, env)
        eng.run(["git", "config", "user.name", "yaiwes-case-repair-engine"], dst)
        eng.run(["git", "config", "user.email", "yaiwes-case-repair-engine@users.noreply.github.com"], dst)
        target = dst / rel

        if target.exists():
            if not REPAIR_EXISTING:
                raise RuntimeError("DESTINATION_EXISTS:" + rel)
            shutil.rmtree(target)

        target.mkdir(parents=True)
        shutil.copytree(extracted, target / "code", dirs_exist_ok=False, copy_function=shutil.copy2)
        archives = target / "_archives"
        archives.mkdir()
        for p in sorted(parts_dir.iterdir()):
            if p.is_file() and not p.name.startswith("_") and p.name != "DOWNLOAD_EXTRACT_MANIFEST.json":
                shutil.copy2(p, archives / p.name)
        shutil.copy2(manifest_path, target / "DOWNLOAD_EXTRACT_MANIFEST.json")
        eng.scan_tree(target, enforce_blob_limit=True)

        # -f is essential here: source repositories can intentionally track files
        # matching their own .gitignore. Without -f, those files vanished in the
        # historical partial publications.
        eng.run(["git", "add", "-f", "--sparse", "-A", "--", rel], dst)
        staged = eng.run(["git", "diff", "--cached", "--name-only", "--", rel], dst)
        if not staged.strip():
            raise RuntimeError("REPAIR_NO_STAGED_CHANGE:" + rel)

        eng.run(["git", "commit", "-m", f"build(case-repair): publish {slug} complete extracted tree"], dst)
        eng.run(["git", "fetch", "origin", eng.DEST_BRANCH], dst, env=env)
        reb = eng.run(["git", "rebase", f"origin/{eng.DEST_BRANCH}"], dst, env=env, check=False)
        if "CONFLICT" in reb:
            eng.run(["git", "rebase", "--abort"], dst, check=False)
            raise RuntimeError("NON_FAST_FORWARD_CONFLICT")
        eng.run(["git", "push", "origin", f"HEAD:{eng.DEST_BRANCH}"], dst, env=env)
        commit = eng.run(["git", "rev-parse", "HEAD"], dst)

        rb = work / "readback"
        eng.sparse_checkout(rb, eng.DEST_REPO, eng.DEST_BRANCH, rel, env)
        rt = rb / rel
        remote = json.loads((rt / "DOWNLOAD_EXTRACT_MANIFEST.json").read_text())
        for row in remote["parts"]:
            p = rt / "_archives" / row["name"]
            if not p.exists() or eng.sha256(p) != row["sha256"]:
                raise RuntimeError("READBACK_ARCHIVE_HASH_GAP:" + row["name"])
        actual = eng.tree_hash(rt / "code")
        expected = remote["extracted_tree"]
        if actual["sha256"] != expected["sha256"] or actual["files"] != expected["files"] or actual["bytes"] != expected["bytes"]:
            raise RuntimeError("READBACK_TREE_HASH_GAP")
        return {
            "verdict": "PUBLISHED_AND_EXTRACTED_READBACK_VERIFIED",
            "commit": commit,
            "repair_existing": REPAIR_EXISTING,
            "deref_count": int(os.getenv("YAIWES_DEREF_COUNT", "0")),
        }

    eng.acquire = acquire_case
    eng.safe_extract = safe_extract_case
    eng.publish = publish_case
    return eng


def main() -> None:
    eng = install_overrides(load_engine())
    eng.main()


if __name__ == "__main__":
    main()
