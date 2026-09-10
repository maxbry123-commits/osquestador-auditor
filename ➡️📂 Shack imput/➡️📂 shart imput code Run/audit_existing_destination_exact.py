#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, sys

ROOT = pathlib.Path("➡️📂 Shack imput/📂 Componentes para integración sharck imput")
TARGETS = [
    ("search", "firecrawl"),
    ("code", "tree-sitter"),
]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def tree_hash(root: pathlib.Path) -> dict:
    h = hashlib.sha256(); files = 0; total = 0
    for p in sorted((x for x in root.rglob("*") if x.is_file()), key=lambda x: x.relative_to(root).as_posix()):
        rel = p.relative_to(root).as_posix(); digest = sha256_file(p); size = p.stat().st_size
        h.update(rel.encode("utf-8") + b"\0" + digest.encode("ascii") + b"\n")
        files += 1; total += size
    return {"files": files, "bytes": total, "sha256": h.hexdigest()}


def audit_one(lane: str, slug: str) -> dict:
    target = ROOT / lane / slug
    mp = target / "DOWNLOAD_EXTRACT_MANIFEST.json"
    if not mp.is_file():
        return {"lane": lane, "slug": slug, "verdict": "MANIFEST_MISSING"}
    manifest = json.loads(mp.read_text())
    code = target / "code"; archives = target / "_archives"
    if not code.is_dir() or not archives.is_dir():
        return {"lane": lane, "slug": slug, "verdict": "DESTINATION_INCOMPLETE"}
    actual_tree = tree_hash(code)
    expected_tree = manifest.get("extracted_tree", {})
    part_rows = []
    parts_ok = True
    for row in manifest.get("parts", []):
        p = archives / row["name"]
        actual = sha256_file(p) if p.is_file() else None
        ok = actual == row.get("sha256")
        parts_ok = parts_ok and ok
        part_rows.append({"name": row["name"], "expected_sha256": row.get("sha256"), "actual_sha256": actual, "ok": ok})
    tree_ok = actual_tree == expected_tree
    manifest_invariants = (
        manifest.get("source_tree") == manifest.get("extracted_tree")
        and manifest.get("extraction_verified") is True
        and manifest.get("reconstruction_verified") is True
        and manifest.get("no_lfs") is True
    )
    verdict = "EXACT_EXISTING_DESTINATION_VERIFIED" if tree_ok and parts_ok and manifest_invariants else "EXISTING_DESTINATION_MISMATCH"
    return {
        "lane": lane,
        "slug": slug,
        "source_repo": manifest.get("source_repo"),
        "source_commit": manifest.get("source_commit"),
        "expected_tree": expected_tree,
        "actual_tree": actual_tree,
        "tree_ok": tree_ok,
        "parts_ok": parts_ok,
        "manifest_invariants": manifest_invariants,
        "parts": part_rows,
        "verdict": verdict,
    }


def main() -> None:
    rows = [audit_one(*x) for x in TARGETS]
    ok = all(r["verdict"] == "EXACT_EXISTING_DESTINATION_VERIFIED" for r in rows)
    out = {"schema": "wanted-shark.existing-destination-exact-audit.v1", "targets": len(rows), "verified": sum(r["verdict"] == "EXACT_EXISTING_DESTINATION_VERIFIED" for r in rows), "rows": rows, "verdict": "VERIFIED_CLOSED" if ok else "GAPS_PENDING"}
    report = pathlib.Path("➡️📂 Shack imput/📂 Craxy wall bitácora stated JSON/EXISTING-DESTINATION-EXACT-AUDIT.json")
    report.write_text(json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if ok else 2)


if __name__ == "__main__":
    main()
