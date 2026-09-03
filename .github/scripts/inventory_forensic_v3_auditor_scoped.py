import json, os, re, subprocess
from collections import Counter, defaultdict

DIRECTORY = "Download code osquestador auditor memoria"
MANIFEST = DIRECTORY + "/RESEARCH_DOWNLOAD_MANIFEST.jsonl"
repo = os.environ.get("GITHUB_REPOSITORY", "")
run_id = os.environ.get("GITHUB_RUN_ID", "")
server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")

def git(*args):
    return subprocess.check_output(["git", *args])

head = git("rev-parse", "HEAD").decode().strip()
manifest_text = git("show", "HEAD:" + MANIFEST).decode("utf-8", "replace")
raw = git("ls-tree", "-r", "-l", "-z", "HEAD", "--", DIRECTORY)

files = []
for rec in raw.split(b"\0"):
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1)
    p = meta.decode().split()
    if len(p) >= 4 and p[1] == "blob":
        files.append({"path": path.decode("utf-8", "replace"), "size": 0 if p[3] == "-" else int(p[3])})

def norm(x):
    return re.sub(r"[^a-z0-9]+", "", str(x or "").lower())

def canon(u):
    x = str(u or "").strip().lower()
    if x.endswith(".git"):
        x = x[:-4]
    return x.rstrip("/")

def source_name(u):
    x = str(u or "").rstrip("/")
    if x.lower().endswith(".git"):
        x = x[:-4]
    return x.rsplit("/", 1)[-1]

groups = defaultdict(list)
zr = re.compile(r"(?i)^(.*)_([0-9]{4})\.zip$")
for f in files:
    m = zr.match(os.path.basename(f["path"]))
    if m:
        groups[norm(m.group(1))].append({"path": f["path"], "part": int(m.group(2)), "size": f["size"]})

versions, excluded = [], []
for line_no, line in enumerate(manifest_text.splitlines(), 1):
    if not line.strip():
        continue
    d = json.loads(line)
    slug = d.get("slug") or d.get("name")
    source = d.get("source") or d.get("source_url")
    sha = d.get("source_commit") or d.get("sha")
    status = str(d.get("status") or "").upper()
    try:
        expected = int(d.get("parts"))
    except Exception:
        expected = None

    sha_ok = bool(isinstance(sha, str) and re.fullmatch(r"[0-9a-fA-F]{40}", sha))
    source_ok = bool(isinstance(source, str) and source.startswith(("https://", "http://")))
    wanted = {norm(slug), norm(source_name(source))} - {""}
    exact = []
    for w in wanted:
        ps = sorted(groups.get(w, []), key=lambda x: x["part"])
        if expected is not None and len(ps) == expected and [x["part"] for x in ps] == list(range(1, expected + 1)):
            exact = ps
            break

    if status == "SKIPPED" and not sha_ok and expected is None and not exact:
        excluded.append({"manifest_line": line_no, "slug": slug, "source": source, "reason": d.get("reason"), "classification": "EXCLUDED_NON_DOWNLOADED"})
        continue

    if not source_ok or not sha_ok:
        result_status = "INSUFFICIENT_EVIDENCE"
    elif not exact:
        result_status = "GAP"
    else:
        result_status = "COMPLETE"

    versions.append({
        "canonical_id": canon(source),
        "canonical_name": slug or source_name(source),
        "source_url": source or "INSUFFICIENT_EVIDENCE",
        "source_commit": sha if sha_ok else "INSUFFICIENT_EVIDENCE",
        "repository": repo,
        "branch": "main",
        "exact_path": DIRECTORY if exact else "INSUFFICIENT_EVIDENCE",
        "manifest_path": MANIFEST,
        "zip_parts": len(exact) if exact else "INSUFFICIENT_EVIDENCE",
        "maximum_part_size": max((x["size"] for x in exact), default=0) if exact else "INSUFFICIENT_EVIDENCE",
        "workflow_run_url": f"{server}/{repo}/actions/runs/{run_id}",
        "status": result_status,
        "locations": [{"directory": DIRECTORY, "files": [x["path"] for x in exact]}] if exact else [],
        "evidence": {
            "tree_verified": True,
            "manifest_verified": True,
            "sha_verified": sha_ok,
            "zip_verified": bool(exact),
            "destination_verified": bool(exact),
            "workflow_verified": True,
        },
    })

c = Counter(v["status"] for v in versions)
out = {
    "schema": "YAIWES-INVENTORY-INDEXES-V3-SCOPED",
    "repository": repo,
    "branch": "main",
    "main_commit": head,
    "workflow_run_url": f"{server}/{repo}/actions/runs/{run_id}",
    "versions": versions,
    "excluded_non_downloaded": excluded,
    "counts": {
        "manifest_rows": len(versions) + len(excluded),
        "unique_versions": len(versions),
        "unique_canonical": len({v["canonical_id"] for v in versions}),
        "complete": c["COMPLETE"],
        "skipped": c["SKIPPED"],
        "gaps": c["GAP"],
        "insufficient_evidence": c["INSUFFICIENT_EVIDENCE"],
        "excluded_non_downloaded": len(excluded),
    },
}
os.makedirs("audit-v3-scoped", exist_ok=True)
with open("audit-v3-scoped/inventory-scoped-v3.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
with open("audit-v3-scoped/inventory-scoped-v3.md", "w", encoding="utf-8") as f:
    f.write("# Auditoría forense V3 scoped — " + repo + "\n\n")
    for k, v in out["counts"].items():
        f.write(f"- {k}: {v}\n")
