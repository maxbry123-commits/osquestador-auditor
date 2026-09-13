import asyncio
import json
import tempfile
import time
from pathlib import Path

from sharck_v3_runtime import (
    ParallelRouter,
    QueueDownloadEngine,
    RunLedger,
    SharckV3Runtime,
    StaticCatalogProvider,
    StaticSearchProvider,
)


def build_runtime(tmp: str, delay: float = 0.03):
    evidence = [
        {"title": f"Evidence {i}", "url": f"https://e/{i}", "description": "construye sdk api evidencia oficial comunidad skills datasets adaptadores research skill dataset adapter tool evidence guide", "trust": 0.9}
        for i in range(30)
    ]
    catalog = [
        {"id": f"x-{i}", "name": f"sdk-research-{i}", "description": "sdk api skill dataset adapter tool research", "url": f"https://c/{i}", "trust": 0.8}
        for i in range(30)
    ]
    official = [dict(x) for x in evidence]
    community = [{**x, "url": x["url"].replace("https://e/", "https://community.example/e/")} for x in evidence]
    sp = [StaticSearchProvider("official", official, delay), StaticSearchProvider("community", community, delay)]
    def cp(name):
        rows = [{**x, "id": f"{name}-{x['id']}", "url": f"https://{name}.invalid/{i}"} for i, x in enumerate(catalog)]
        return StaticCatalogProvider(name, rows, delay)
    return SharckV3Runtime(
        search_router=ParallelRouter(sp, min_fanout=10, max_fanout=100, concurrency=32),
        skill_libraries=[cp("huggingface"), cp("openai"), cp("anthropic")],
        dataset_providers=[cp("huggingface-datasets"), cp("zenodo"), cp("datagov")],
        adapter_providers=[cp("mcp-registry"), cp("github"), cp("local")],
        tool_providers=[cp("mcp-registry"), cp("openai-plugins"), cp("local")],
        ledger=RunLedger(tmp),
        continuous_rounds=2,
    )


def test_contracts_and_outputs():
    with tempfile.TemporaryDirectory() as tmp:
        rt = build_runtime(tmp, 0.001)
        pkg = asyncio.run(rt.run("Construye un SDK API con evidencia oficial y comunidad, skills, datasets y adaptadores."))
        assert pkg.verdict == "CONTEXT_READY", pkg.gaps
        assert len(pkg.active_skills) == 3
        assert len(pkg.datasets) == 3
        assert len(pkg.adapters) == 3
        assert len(pkg.tools) == 3
        run = Path(tmp) / pkg.run_id
        for name in ["INPUT_RAW.txt", "profile.json", "memory.md", "HANDOFF.md", "handoff-index.json", "CONTEXT_PACKAGE.json", "evidence-ledger.jsonl", "lane-results.json"]:
            assert (run / name).exists(), name
        profile = json.loads((run / "profile.json").read_text())
        assert profile["input_sha256"] == pkg.input_sha256
        assert len(profile["lane_status"]) == 12


def test_parallel_start_is_not_serial():
    with tempfile.TemporaryDirectory() as tmp:
        rt = build_runtime(tmp, 0.03)
        start = time.perf_counter()
        pkg = asyncio.run(rt.run("SDK API evidence community dataset skill adapter tool"))
        elapsed = time.perf_counter() - start
        assert pkg.verdict == "CONTEXT_READY"
        assert elapsed < 1.4, elapsed


def test_skill_gate_requires_three_libraries_and_twenty_items():
    with tempfile.TemporaryDirectory() as tmp:
        rt = build_runtime(tmp, 0.0)
        rt.skill_libraries = rt.skill_libraries[:2]
        pkg = asyncio.run(rt.run("SDK API skill dataset adapter tool evidence"))
        assert pkg.verdict == "CONTEXT_GAP_LOOP"
        assert any("skill" in g for g in pkg.gaps)


def test_queue_download_engine_writes_fail_closed_request():
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "run"
        run_dir.mkdir(parents=True)
        engine = QueueDownloadEngine()
        pinned = {
            "name": "mcp-builder",
            "source_repo": "anthropics/skills",
            "source_ref": "34040c9c568585f6929bedeaad110ad08f079624",
            "url": "https://github.com/anthropics/skills/tree/main/skills/mcp-builder",
            "license": "Apache-2.0",
        }
        staged = asyncio.run(engine.stage(lane="skills", item=pinned, run_dir=run_dir))
        assert staged["status"] == "READY_FOR_CANONICAL_MOTOR"
        req = json.loads((run_dir / staged["request"]).read_text())
        assert req["publish"] is False
        assert req["source_ref"] == pinned["source_ref"]
        assert req["dest_root"].startswith("RUN_SANDBOX/")
        assert "READBACK_OK" in req["required_gates"]

        unpinned = {"name": "unknown", "url": "https://example.invalid/unknown"}
        blocked = asyncio.run(engine.stage(lane="datasets", item=unpinned, run_dir=run_dir))
        assert blocked["status"] == "NEEDS_GATE_METADATA"


def test_literal_alignment_gate_blocks_unrelated_context():
    with tempfile.TemporaryDirectory() as tmp:
        rt = build_runtime(tmp, 0.0)
        unrelated = [{"title": f"Weather {i}", "url": f"https://w/{i}", "description": "rain temperature forecast climate", "trust": 0.9} for i in range(30)]
        rt.search = ParallelRouter([StaticSearchProvider("official", unrelated), StaticSearchProvider("community", unrelated)], min_fanout=10, max_fanout=100, concurrency=32)
        pkg = asyncio.run(rt.run("Construye un SDK API con evidencia oficial y comunidad, skills, datasets y adaptadores."))
        assert pkg.verdict == "CONTEXT_GAP_LOOP"
        assert "literal_input_alignment_gap" in pkg.gaps
        assert any(x.get("status") == "GAP" for x in pkg.anti_hallucination_checklist)


if __name__ == "__main__":
    test_contracts_and_outputs()
    test_parallel_start_is_not_serial()
    test_skill_gate_requires_three_libraries_and_twenty_items()
    test_queue_download_engine_writes_fail_closed_request()
    test_literal_alignment_gate_blocks_unrelated_context()
    print("5 tests PASS")
