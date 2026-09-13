# M59 STRICT ENTRYPOINT

**Authoritative candidate entrypoint:** `StrictSharckV3Runtime` from `sharck_v3_strict.py`.

Do not promote the base `SharckV3Runtime` directly. The strict layer adds the literal user gates that the base intentionally kept generic:

- 11 independently scheduled `LaneKernel` tasks + continuous research task.
- Skills: at least 3 distinct libraries with results.
- Skills: exactly the first 20 distinct candidates are fully read (`SKILL.md` body), SHA256 hashed and cached under `RUN/artifacts/skills-read/`.
- Only 3 skills are selected/activated; selection must span 3 distinct libraries and each selected item must have repository pin + license.
- 5 additional skills remain standby.
- `skill_library_provider.default_skill_libraries()` pins:
  - `huggingface/skills@f3186efbbc322121eb5d0f31e8a1d669ee961159`, preferred `hf-cli`, Apache-2.0.
  - `anthropics/skills@34040c9c568585f6929bedeaad110ad08f079624`, preferred/licensed `mcp-builder`, Apache-2.0.
  - `microsoft/skills@903dc62b1e4c833235b54db918a9a51cb6d3cc8f`, preferred `skill-creator`, MIT.
- Full bodies stay external to the LLM context. The context receives hashes/pointers and only selected skills are activated, preserving progressive disclosure.
- Acquisition remains a request only (`publish=false`) until the immutable canonical Motor 2 and readback gates execute.

## Minimal construction

```python
from sharck_v3_runtime import ParallelRouter, QueueDownloadEngine, RunLedger
from sharck_v3_strict import StrictSharckV3Runtime
from skill_library_provider import default_skill_libraries

runtime = StrictSharckV3Runtime(
    search_router=ParallelRouter(search_providers, min_fanout=10, max_fanout=100),
    skill_libraries=default_skill_libraries(),
    dataset_providers=dataset_providers,
    adapter_providers=adapter_providers,
    tool_providers=tool_providers,
    ledger=RunLedger(run_root),
    download_engine=QueueDownloadEngine(),
)
package = await runtime.run(INPUT_RAW)
```

## Promotion gate

This remains `SANDBOX_CANDIDATE / NOT_PRODUCTION_WIRED`. Promotion requires remote CI PASS, live provider/network smoke, source/license/readback for acquisitions, and an explicit supervisor gate. Existing `physical_repair_allowed=false`, `b05_b06_download_allowed=false`, and `step3_allowed=false` remain unchanged.
