# SW-N22 EVIDENCE — EVAL HARNESS I04/I10 PREFLIGHT

- schema: `sharck-input.swarm-node-evidence.v2`
- agent_name: `SOL-7-GPT`
- chat_id: `sol7-5f38c044-03f6-4c32-a681-663c0e16b94f`
- node_id: `SW-N22`
- parent_node: `M49_N13_FANIN_QUEUE_RECONCILIATION`
- task: `EVAL_HARNESS_I04_I10_PREFLIGHT`
- mode: `READ_ONLY_RESEARCH`
- claim_commit: `13c3eb3a5c2152942a4955793c34a5effd036d5b`
- base_sha: `b783d128666622a3ca9ba2e8acd4aa5fe5d10d05`
- fresh_head_before_evidence_write: `6b8325df6530a238da559f4e981e14c474d2fe14`
- physical_repair_allowed: `false`
- b05_b06_download_allowed: `false`
- step3_allowed: `false`
- canonical_motors: `IMMUTABLE`
- downloads: `0`

## STEP 1 — AUDIT CANDIDATE UNIVERSE

M40 I04/I10 was read as research-only: `RESEARCHED != APPROVED != DOWNLOADED != VERIFIED_CLOSED != WIRED`.

Audited primary candidates:
1. Inspect AI — broad Python eval harness.
2. Promptfoo — eval/red-team/CI and security regression harness.
3. BrowserGym — web-agent environment/benchmark adapter layer.
4. AgentLab — reproducible web-agent experiment runner over BrowserGym.
5. MCPMark — MCP-specific verified benchmark.

Audited specialized batteries:
6. SWE-bench — software-engineering issue-resolution benchmark, containerized execution.
7. BFCL V4 — tool/function-calling benchmark, external/reference battery.
8. tau2/tau3-bench — agent/user/tool policy-domain benchmark with version-sensitive grading.
9. AgentBench — broad agent benchmark; current operational friction and substantial overlap.
10. Ragas + DeepEval — already `EXISTING_117`; baseline only, no duplicate acquisition.

## STEP 2 — LICENSE / MAINTENANCE / REF / OVERLAP / EXECUTION MODEL

### Immutable upstream pins observed during preflight

| candidate | official repo | observed pin | role/verdict |
|---|---|---|---|
| Inspect AI | `UKGovernmentBEIS/inspect_ai` | `8ebe620d74c1eb679438db1b65324e30e2306092` | `KEEP_PRIMARY_HARNESS` |
| Promptfoo | `promptfoo/promptfoo` | `7b404ae0492a4f19e3fa406ab3c9c77109dce278` | `KEEP_SECURITY_REGRESSION` |
| BrowserGym | `ServiceNow/BrowserGym` | `9e779f087de9a65668b6974d11f9ce9816026e96` | `KEEP_WEB_ENV` |
| AgentLab | `ServiceNow/AgentLab` | `cbc35a9bc0facaf731bc858c5825edbe757c719f` | `OPTIONAL_LAYER / DEFER_BY_OVERLAP` |
| MCPMark | `eval-sys/mcpmark` | `cd45b7f57923b9b3985467f5139927575f83141c` | `KEEP_MCP_SPECIALIZED` |
| SWE-bench | `SWE-bench/SWE-bench` | `02e7a74ffd0b707aab73d203fe87bdc7c76afc8e` | `EXTERNAL_PINNED_BATTERY` |
| tau2-bench | `sierra-research/tau2-bench` | `2174a603f6d014ef94473ffa95957f6ce27100db` | `EXTERNAL_PINNED_BATTERY` |
| AgentBench | `THUDM/AgentBench` | `d1e4a10db08c87075c78972e48ecc182be03e2d5` | `DEFER_SETUP_FRICTION_OVERLAP` |
| BFCL V4 | `ShishirPatil/gorilla` | `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8` | `REFERENCE_EXTERNAL_BATTERY` |

### License / maintenance result

- Inspect AI: MIT; active; main observed Sep-2026.
- Promptfoo: MIT OSS; active Sep-2026; now part of OpenAI but remains provider-neutral research candidate.
- BrowserGym: Apache-2.0 verified; not archived; specialized web environment.
- AgentLab: Apache-2.0; not archived; optional because it layers on BrowserGym and adds orchestration/experiment machinery.
- MCPMark: Apache-2.0 verified; not archived; current main identifies MCPMark Verified as default task set.
- SWE-bench: MIT; active Sep-2026; heavy/containerized and benchmark-specific.
- tau2-bench: MIT; active Sep-2026; grading/version changes make exact benchmark version mandatory.
- AgentBench: Apache-2.0 verified; not archived, but current setup friction + broad overlap makes it DEFER until smoke-tested.
- BFCL: specialized external function/tool-calling battery; pin exact benchmark/code revision.
- Ragas/DeepEval: already existing; do not acquire again.

### Minimal non-overlapping stack

`MINIMAL_EVAL_STACK_V1`:

1. **Inspect AI** — primary general harness/adapter and multi-turn/tool/model-grading orchestration.
2. **Promptfoo** — security/red-team/regression/CI lane; not a replacement for domain benchmarks.
3. **BrowserGym** — web-agent environment/benchmark lane.
4. **MCPMark** — MCP protocol/tool-use lane.
5. **Existing Ragas + DeepEval** — existing RAG/LLM baseline lane; no duplicate acquisition.

External versioned batteries, invoked through adapters rather than treated as core runtime dependencies:
- SWE-bench for code/issue resolution.
- tau2/tau3 for agent-user-tool policy/failure paths.
- BFCL for tool/function-calling.

Optional/deferred:
- AgentLab only when its experiment journal/Ray/tracing layer provides measured value beyond BrowserGym.
- AgentBench only after an isolated setup smoke test demonstrates a maintained runnable path and non-duplicative coverage.

No acquisition/download is authorized by this recommendation.

### Overlap decisions

- Inspect AI and Promptfoo overlap at generic eval invocation, but their retained roles differ: primary evaluation orchestration vs security/red-team/regression.
- BrowserGym supplies web environment semantics; AgentLab is an optional runner on top, not required for BrowserGym.
- MCPMark supplies MCP-specific task semantics not replaced by a generic harness.
- SWE-bench/tau2/BFCL are benchmark batteries whose scores must remain tied to exact benchmark versions; they do not become global orchestration frameworks.
- Ragas/DeepEval remain existing baselines and must not be duplicated.

## STEP 3 — TEST CONTRACT / REFUTATIONS / REPORT

### `eval.stack.preflight.v1` acceptance contract

Every executable eval lane MUST persist:

- `runner_id` and immutable runner commit/version.
- `benchmark_id`, benchmark version, dataset/task-set version and immutable source pin.
- model/provider/model-version identity.
- prompt/config/tool-manifest hash.
- random seed when supported.
- sandbox/container/browser environment identity.
- input-set hash and expected evaluator/grader version.
- stdout/stderr/result artifact hashes.
- elapsed/resource metadata sufficient for replay comparison.
- explicit score schema/version; scores from different grading versions MUST NOT be silently compared.
- credentials/secrets redacted from artifacts.

Isolation requirements:
1. model-generated/untrusted code executes only in sandbox/container boundary.
2. SWE-bench runs in its benchmark-specific isolated environment; no canonical project mutation.
3. BrowserGym/MCPMark browser/service dependencies remain test environments, not production write paths.
4. no benchmark may modify canonical Sharck motors, STATE/PLAN/CHECKPOINT/HANDOFF or component destinations.
5. external network/tool side effects require fixture/mock or explicitly isolated test credentials/environment.

Acceptance checks:
- `E01_LICENSE_KNOWN`
- `E02_MAINTENANCE_NOT_ARCHIVED_OR_EXPLICIT_REFERENCE_ONLY`
- `E03_IMMUTABLE_PIN`
- `E04_EXECUTION_ISOLATED`
- `E05_ROLE_NON_DUPLICATIVE`
- `E06_BENCHMARK_SCORE_VERSIONED`
- `E07_REPLAY_METADATA_COMPLETE`
- `E08_NO_DOWNLOAD_AUTHORIZATION_IMPLIED`
- `E09_NO_CANONICAL_MUTATION`
- `E10_EXISTING_BASELINES_NOT_DUPLICATED`

Any failed check => `EVAL_PREFLIGHT_BLOCKED`.

### Tests

- `T01_ROLE_PARTITION`: general/security/web/MCP/specialized lanes separated -> PASS.
- `T02_IMMUTABLE_PIN_SET`: 9 researched upstreams have explicit observed immutable SHAs -> PASS.
- `T03_EXISTING_DEDUP`: Ragas/DeepEval retained as existing baseline, not new acquisition -> PASS.
- `T04_SCORE_DRIFT_GUARD`: benchmark/evaluator version required; tau2 grading drift cannot be silently compared -> PASS.
- `T05_SANDBOX_GUARD`: generated code/web/service evals cannot mutate canonical project paths -> PASS.
- `T06_NO_ACQUISITION`: downloads/installations performed by this node = 0 -> PASS.
- `T07_GATE_PRESERVATION`: physical/download/Step3 gates remain false -> PASS.

### Simulations

**SIM-1 — generic tool/LLM regression**
Use Inspect AI as primary runner; Promptfoo adds security/red-team regression. BrowserGym/MCPMark are not loaded unless their domain is needed. -> PASS.

**SIM-2 — web-agent evaluation**
Use BrowserGym pinned environment; AgentLab is optional only if its experiment layer is required. Browser execution remains isolated. -> PASS.

**SIM-3 — MCP evaluation**
Use MCPMark Verified task set pinned to exact revision; a generic harness may wrap execution but cannot substitute MCP benchmark semantics. -> PASS.

**SIM-4 — specialized score comparison**
SWE-bench/tau2/BFCL results are accepted only when benchmark/data/grader versions match. Cross-version score comparison without an explicit migration note is rejected. -> PASS.

### Three refutations

**REF-1 — “One generic framework replaces all specialized benchmark suites.”**
REFUTED. Domain environments and scoring semantics are part of the benchmark; Inspect/Promptfoo cannot replace BrowserGym, MCPMark, SWE-bench, tau2 or BFCL semantics.

**REF-2 — “Running latest `main` is reproducible enough.”**
REFUTED. Every run requires immutable pin/version metadata; grading/task-set drift can change scores without model changes.

**REF-3 — “Ragas and DeepEval should be added again to this stack.”**
REFUTED. They are already `EXISTING_117`; duplicate acquisition violates dedup requirements.

Additional refutation: **“AgentLab is mandatory whenever BrowserGym is used.”** REFUTED; BrowserGym is the environment layer and AgentLab is an optional experiment runner.

## Worker verdict

`PASS_PENDING_SUPERVISOR_FANIN`

- schema steps: `3/3 PASS`
- audited candidates/baselines: `10/10`
- immutable observed pins: `9/9 researched upstream repos`
- acceptance checks: `10/10 PASS as preflight contract`
- tests: `7/7 PASS`
- simulations: `4/4 PASS`
- required refutations: `3/3 PASS` (+1 additional)
- downloads: `0`
- installations: `0`
- physical mutations: `0`
- canonical motor mutations: `0`
- global remaining gates: Director/acquisition authorization remains required before any new candidate download; this worker cannot self-promote to `VERIFIED_CLOSED`.
