from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Resolve prior SHARCK evidence pointers without re-search")
    p.add_argument("run_dir")
    p.add_argument("query")
    args = p.parse_args()
    path = Path(args.run_dir) / "handoff-index.json"
    if not path.exists():
        print(json.dumps({"error": "handoff-index.json not found"}))
        return 2
    rows = json.loads(path.read_text(encoding="utf-8"))
    terms = [t.lower() for t in args.query.split() if len(t) > 2]
    scored = []
    for row in rows:
        hay = f"{row.get('title','')} {row.get('source','')} {row.get('lane','')} {row.get('pointer','')}".lower()
        score = sum(t in hay for t in terms)
        if score:
            scored.append((score, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    print(json.dumps([r for _, r in scored[:20]], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
