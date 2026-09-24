from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
CODE_ROOT = HERE.parent.parent
PREPASS_ROOT = CODE_ROOT / "📂 root-only-runtime" / "📂 research-prepass-native"
if str(PREPASS_ROOT) not in sys.path:
    sys.path.insert(0, str(PREPASS_ROOT))

import research_prepass as rp  # noqa: E402
from sharck_v3_runtime import Evidence, LaneResult, _sha  # noqa: E402
from sharck_v3_strict import LaneKernel, StrictSharckV3Runtime  # noqa: E402


def _run_prepass_sync(spec, run_dir: Path) -> dict:
    output_root = run_dir / "artifacts" / "research-prepass"
    registry = PREPASS_ROOT / "source_registry_no_hf.json"
    if not registry.is_file():
        raise RuntimeError("NO_HF_REGISTRY_MISSING")
    return rp.run(
        input_text=spec.raw,
        input_origin="SHARCK_INPUT_RAW",
        plan_text="",
        plan_origin="",
        registry_path=registry,
        output_root=output_root,
        limit=max(1, min(int(os.getenv("SHARCK_PRESEARCH_LIMIT", "4")), 10)),
        budget_tokens=max(1, int(os.getenv("SHARCK_PRESEARCH_BUDGET_TOKENS", "5000"))),
        max_per_source=max(1, int(os.getenv("SHARCK_PRESEARCH_MAX_PER_SOURCE", "3"))),
        cache_ttl=max(0, int(os.getenv("SHARCK_PRESEARCH_CACHE_TTL_SECONDS", "21600"))),
        force=os.getenv("SHARCK_PRESEARCH_FORCE", "0").lower() in {"1", "true", "yes"},
    )


async def native_presearch_lane(spec, run_dir: Path) -> LaneResult:
    try:
        packet = await asyncio.to_thread(_run_prepass_sync, spec, run_dir)
    except Exception as exc:
        return LaneResult(
            "presearch",
            "GAP",
            f"native research prepass exception: {type(exc).__name__}",
            gaps=[f"presearch_exception:{type(exc).__name__}"],
        )

    evidence = []
    for row in packet.get("records", []):
        pointer = str(row.get("url") or "")
        claim = str(row.get("snippet") or row.get("title") or "")[:1200]
        evidence.append(
            Evidence(
                lane="presearch",
                source=str(row.get("source_id") or row.get("provider") or "research-prepass"),
                title=str(row.get("title") or pointer or "untitled"),
                pointer=pointer,
                claim=claim,
                confidence=min(1.0, max(0.0, float(row.get("source_weight", 0.5)))),
                source_type=str(row.get("source_kind") or "research"),
                sha256=_sha(pointer + claim),
                metadata={
                    "provider": row.get("provider"),
                    "score": row.get("score"),
                    "estimated_tokens": row.get("estimated_tokens"),
                    "prepass_run_id": packet.get("run_id"),
                },
            )
        )

    ok = bool(evidence) and packet.get("input", {}).get("verbatim_preserved") is True
    gaps = [] if ok else ["presearch_no_new_evidence"]
    source_gaps = [
        f"presearch_source_gap:{sid}"
        for sid, state in (packet.get("source_status") or {}).items()
        if (state or {}).get("state") == "GAP"
    ]
    gaps.extend(source_gaps)
    return LaneResult(
        "presearch",
        "PASS" if ok else "GAP",
        f"{len(evidence)} evidence / {len(packet.get('sources_requested', []))} sources / no_hf=true",
        evidence=evidence,
        gaps=gaps,
        metrics={
            "packet": packet.get("context_packet"),
            "context_md": packet.get("context_md"),
            "cache_state": packet.get("cache_state"),
            "estimated_context_tokens": packet.get("estimated_context_tokens"),
            "llm_used": packet.get("llm_used"),
            "no_hf": True,
        },
    )


class PresearchStrictSharckV3Runtime(StrictSharckV3Runtime):
    """Strict M59 runtime plus one native deterministic PRESEARCH support lane.

    PRESEARCH starts concurrently with the 11 mandatory LaneKernels and
    continuous research. It never serializes or reduces Director parallelism.
    Its evidence is merged into the same ContextPackage and it is a fail-closed
    supporting gate.
    """

    async def run(self, raw_input):
        s = self.decompose(raw_input)
        await self.ledger.initialize(s)
        await self.ledger.append(s.run_id, {"event": "INPUT_LOCK", "sha256": s.raw_sha256})

        funcs = [
            lambda: self._search_lane("research", s, ["official docs", "community implementation", "current best practice"], 20, 2),
            lambda: self._skills(s),
            lambda: self._catalog("datasets", self.dataset_providers, s, 3, 5),
            lambda: self._catalog("adapters", self.adapter_providers, s, 3, 5),
            lambda: self._tools(s),
            lambda: self._persistence(s),
            lambda: self._validator(s),
            lambda: self._search_lane("error_lens", s, ["bug", "failed", "negative review", "pitfall", "breaking change", "regression"], 20, 1),
            lambda: self._search_lane("solution_guides", s, ["official manual", "install guide", "runbook", "developer tutorial", "troubleshooting"], 20, 1),
            lambda: self._multi(s),
            lambda: self._anti(s),
        ]
        kernels = [LaneKernel(n, f) for n, f in zip(self.LANE_NAMES, funcs)]

        tasks = [asyncio.create_task(k.run(), name=f"sharck:{k.name}") for k in kernels]
        continuous_task = asyncio.create_task(self._continuous(s), name="sharck:continuous")
        presearch_task = asyncio.create_task(
            native_presearch_lane(s, self.ledger.run_dir(s.run_id)),
            name="sharck:presearch",
        )

        results = await asyncio.gather(*tasks)
        continuous, presearch = await asyncio.gather(continuous_task, presearch_task)
        supporting = [*continuous, presearch]

        for r in results + supporting:
            await self.ledger.append(
                s.run_id,
                {"event": "LANE_RESULT", "lane": r.lane, "status": r.status, "gaps": r.gaps},
            )

        pkg = self._compile(s, results, supporting)
        if presearch.status != "PASS":
            if "presearch_required_gap" not in pkg.gaps:
                pkg.gaps.append("presearch_required_gap")
            pkg.verdict = "CONTEXT_GAP_LOOP"

        await self._persist(s, results, supporting, pkg)
        return pkg
