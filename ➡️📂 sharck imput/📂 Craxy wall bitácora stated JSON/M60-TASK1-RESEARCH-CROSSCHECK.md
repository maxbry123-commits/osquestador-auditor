# M60 — TASK 1 — RESEARCH CROSS-CHECK FOR CONCURRENT SHARCK AGENCY

**Status:** `ARCHITECTURE_EVIDENCE / NOT_A_PRODUCTION_BENCHMARK`  
**Date:** 2026-09-13  
**Rule:** the user's numbered steps are capability references, not a serial workflow. Research below maps each capability to implementation signals and constraints. “100x” remains a target that Task 2 must measure; no theoretical multiplier is accepted as proof.

## Primary external research signals

1. OpenAI — Agents/Responses: tools, handoffs, guardrails, tracing/observability, web/file/computer tools, remote MCP; current agent harnesses support controlled sandbox/tool execution.  
   - https://openai.com/index/new-tools-for-building-agents/  
   - https://openai.com/index/the-next-evolution-of-the-agents-sdk/  
   - https://platform.openai.com/docs/quickstart/make-your-first-api-request
2. Anthropic — multi-agent research: orchestrator-worker, parallel independent search, iterative research, citation/evidence agents, external memory/artifacts; 3–5 subagents and 3+ parallel tools improved research latency in their reported system, but multi-agent can use far more tokens and is weaker for tightly interdependent tasks.  
   - https://www.anthropic.com/engineering/multi-agent-research-system  
   - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents  
   - https://www.anthropic.com/engineering/building-effective-agents
3. MiniMax — production-agent lessons: move from one-off calls toward context-rich agents with memory/triggers; Agent Teams run multiple roles in parallel for long-running work; M2.7 emphasizes agent teams, complex skills and dynamic tool search.  
   - https://www.minimax.io/news/minimax-agent-what-we-learned-while-building-in-2025  
   - https://www.minimax.io/blog/minimax-agent-team-long-running-1779893953  
   - https://www.minimax.io/news/minimax-m27-en
4. Kimi — swarm/background/persistence: Agent Swarm demonstrates large dynamic fan-out; Kimi Code exposes swarm mode, background tasks/questions, goals, sub-skill discovery, rate-limit-aware retries and provider management.  
   - https://www.kimi.com/en/help/agent/agent-swarm  
   - https://www.kimi.com/en/blog/kimi-k2-5  
   - https://www.kimi.com/code/docs/en/kimi-code/whats-new.html  
   - https://www.kimi.com/code/docs/en/kimi-code-cli/reference/tools.html
5. Hugging Face — discoverable data/tools: dataset cards expose license/language/size/task metadata, datasets can be streamed before full download, Hub tools must be inspected before trusted remote code is executed, and MCP/tool collections provide a universal adapter surface.  
   - https://huggingface.co/docs/hub/datasets-cards  
   - https://huggingface.co/docs/datasets/stream  
   - https://huggingface.co/docs/hub/agents-overview  
   - https://huggingface.co/docs/smolagents/reference/tools
6. GitHub skill libraries already pinned by M59: `huggingface/skills`, `anthropics/skills`, `microsoft/skills`; `openai/plugins` remains reference-only until its license gate is resolved. See `V3-SOURCE-MANIFEST.json`.
7. Developer-community contra-evidence: reports of runaway subagents, duplicated context and very high token usage reinforce hard spawn caps, recursion-off-by-default, per-agent telemetry, shared artifact pointers and adaptive parallelism instead of “always spawn 100”. Community evidence is advisory/contra-evidence, never sufficient alone for PASS.

## Process-by-process research mapping

| User capability / bureau | Research signal | SHARCK architecture decision |
|---|---|---|
| Literal INPUT decomposition + ambiguity questions | Kimi background structured questions; Anthropic stresses explicit objective/boundaries for subagents; OpenAI guardrails/tool schemas | Two deterministic bootstrap operations only: lock + literal decomposition. Ambiguity generates structured questions while unrelated research may continue if safe. |
| Advanced research/context | Anthropic parallel research and dynamic path-dependent search; Kimi Agent Swarm; MiniMax search/tool agents | Breadth-first fan-out by independent source/query class; adaptive specialists; incremental fan-in; no fixed serial DAG for research. |
| Skills >=20, select 3, >=3 libraries | Kimi Sub-Skill discovery; HF Hub skills/tools; M59 pinned HF/Anthropic/Microsoft libraries | Full-read/hash 20 skill bodies outside model context; select 3 across 3 libraries; 5 standby; progressive disclosure and license/source pin before acquisition. |
| Datasets >=3 + 5 standby | HF Dataset Cards + streaming | Search at least 3 appropriate datasets, retain 5 standby; inspect card/license/freshness/schema/sample/fit; stream/sample first; do not inject entire datasets into LLM context. |
| Adapters/couplers | OpenAI remote MCP; HF MCPClient/ToolCollection; Anthropic MCP ecosystem | Capability-driven adapter discovery; >=3 active-compatible candidates + 5 standby when relevant; schema/auth/version/read-only smoke before mutation. |
| Tools/plugins universal socket | OpenAI Responses supports built-in tools/custom functions/remote MCP; HF tools can come from MCP/Hub | Use MCP/API as preferred universal port; give agent capability, schema, auth requirement and usage pointer; remote code requires inspect/trust gate. |
| Persistence/context loop | MiniMax persistent context-rich agents/triggers; Kimi goals/background tasks; uploaded Mavis guide: persistent pools/queues/cache/batching | Durable job abstraction, continuous context-delta producer, 12 goals in/out + Council12 + 3 refutations + 4 simulations; persist artifacts outside LLM window. |
| SHARCK evidence sheriff | OpenAI guardrails/tracing/evals; Anthropic citation/evidence synthesis; MiniMax production benchmark focuses on instruction adherence | Separate deterministic validator from generator; official evidence first, independent community contra-evidence second; rank 10 routes by user friction, time, simplicity, evidence. |
| Error Lens / negative evidence | Anthropic stresses evals/observability and failure analysis; developer communities expose runaway/quality failures | Dedicated adversarial searchers for regressions, complaints, breaking changes and known failure paths before tactical execution. |
| Solution/manual bureau | OpenAI/Anthropic/HF official docs plus community implementation evidence | Official manual/runbook path first; community confirms friction/failure reality; result is an exact executable route with prerequisites/fallback. |
| Multi-SHARCK debate/refutation | Anthropic parallelization “sectioning/voting”; multi-agent research independent contexts | Spawn independent counter-route cells, not copies of the same prompt; compare newer/older/simpler route; use structured debate + evidence, then deterministic fan-in. |
| Anti-hallucination literal gate | OpenAI guardrails/output validation; MiniMax benchmark notes user dissatisfaction when agents violate explicit specs | Final `LiteralAlignmentJudge`/schema sheriff maps every literal requirement to evidence/context/output or blocks release as GAP. |
| News Reporter | General research principle: dynamic/fresh sources; user requires local→international + social traces | Event-triggered bureau only when freshness/news is material; geographic source ladder, social/source thread graph, timestamp/QDF, refresh watchdog. |
| Continuous work while YAIWES executes | MiniMax Agent Teams/long-running operation; Kimi background tasks | Context research continues asynchronously and publishes small deltas to a queue; tactical agent need not stop for unrelated searches. |
| Academic/study research | HF dataset cards can link papers; Hub provides datasets/papers/models; source graph principle | Separate academic specialists for papers, datasets, benchmark/method cross-links and citation lineage when domain requires it. |
| Watchdogs | Kimi goals/background tasks and MiniMax triggers show non-blocking long-running supervision | Per-bureau watcher or global watcher; time/condition based; may refresh/research, but cannot open physical mutation gates autonomously. |
| Always-on persistence | Kimi goal/background operation + MiniMax long-running teams; uploaded MAX system proposes durable state/checkpoint layers | Persistent Job Runtime with checkpoint/resume/idempotency; process lifetime is not tied to chat turn. External ChatGPT automation remains a supervisor, not the runtime itself. |
| 10–100+ parallel processes | Kimi reports large swarm fan-out; Anthropic reports big latency benefit but much higher token cost | Dynamic 1..128 target ceiling initially; parallelize only independent critical-path work; recursion off by default; token/request/time budgets; dedup/backpressure. |
| Memory/profile/Handoff | Anthropic external memory/artifact pointers; Kimi compaction/goals; M59 executable handoff | Every job persists `memory.md`, `profile.json`, evidence ledger, context deltas, `HANDOFF.md`, executable index and source graph; LLM receives compact pointers. |
| Download/extraction traceability | HF warns that loading a Hub tool downloads/executes code and should be inspected; existing SHARCK Motor 2 has source/license/readback gates | Research lane emits acquisition request only; canonical immutable motor remains physical authority; source pin + license + readback mandatory. |
| Simulation / 3 hypotheses | Anthropic recommends multiple perspectives/voting when confidence benefits | Simulation cells run three genuinely different hypotheses/routes when risk/ambiguity warrants it; outputs feed evidence/debate, not automatic truth. |

## Architecture consequence: agency, not pipeline

The correct target is an **event-driven intelligence fabric**:

`INPUT LOCK/DECOMPOSE → publish InputSpec → [many independent bureaus/subagents RUN concurrently] ↔ evidence ledger/context-delta bus ↔ [validators can REACTIVATE searches] → incremental fan-in → literal/evidence sheriff → CONTEXT_PACKAGE/HANDOFF → YAIWES tactical execution`

Parallel bureaus can continue after the first tactical handoff when freshness/long-running work requires it. New evidence arrives as context patches, not as a full prompt rebuild.

## Anti-overengineering conclusions from research

- Do **not** deploy 100 agents for a lookup that needs 1 request.
- Do **not** add another orchestration platform merely because it exists; current Python `asyncio` candidate is sufficient until durability/scale benchmarks prove a GAP.
- Do **not** let subagents recursively spawn by default.
- Do **not** copy every source into the main LLM context; persist artifacts and pass pointers/digests.
- Do **not** treat “parallel = faster” as proof. Measure wall-clock critical path, coverage, cost/tokens, duplicate rate, failure rate and evidence quality.
- Do use batching/cache/dedup/priority/backpressure from the supplied `MAVIS-PARALLEL-100X` reference before adding distributed infrastructure.
- Durable queue/orchestrator is justified only if restart/resume tests show the in-process runtime cannot meet the continuous-work requirement.

## Task 1 research verdict

`SUPPORTED_DIRECTION`: dynamic multi-agent research, background persistence, tools/MCP, external memory/artifacts and deterministic guardrails are consistent with current OpenAI/Anthropic/MiniMax/Kimi/Hugging Face patterns.

`CRITICAL_MODIFICATION`: user-requested “10/100/100+ simultaneous” must be **adaptive and budget-governed**, otherwise community and vendor evidence show token/cost/coordination blow-ups.

`CURRENT_CODE_STATUS`: M59 is a useful tested sandbox candidate but remains partial relative to the complete agency target. M60 records the missing bureaus/services without falsely marking them implemented.