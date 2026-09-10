from __future__ import annotations
import json
from pathlib import Path
from shark_input_lock import lock_input, assert_literal_integrity
from role_router import route_roles

ROOT = Path(__file__).resolve().parent

def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def build_plan(raw: str) -> dict:
    env = lock_input(raw)
    assert_literal_integrity(raw, env)
    roles = route_roles(raw)
    boosters = sorted({b for r in roles for b in r["boosters"]})
    communities = load_json("community_registry.json")
    components = load_json("component_registry.json")
    selected_sources = [s for s in communities["sources"] if any(tag in boosters for tag in s.get("tags", []))]
    if not selected_sources:
        selected_sources = communities["sources"][:12]
    return {
        "schema":"wanted-shark.prellm.plan.v1",
        "input": json.loads(env.to_json()),
        "roles": roles,
        "boosters": boosters,
        "community_sources": selected_sources,
        "component_catalog_size": len(components["components"]),
        "llm_policy": {
            "focus_ai_allowed": True,
            "focus_ai_can_propose_queries": True,
            "focus_ai_cannot_mutate_input_raw": True,
            "focus_ai_cannot_declare_pass": True
        }
    }
