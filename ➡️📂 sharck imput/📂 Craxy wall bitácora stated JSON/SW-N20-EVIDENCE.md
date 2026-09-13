# SW-N20 EVIDENCE — M40 PRIORITY PREFLIGHT LICENSE / REF / PIN / SIZE

- schema: `sharck-input.swarm-node-evidence.v2`
- agent_name: `SOL-3-GPT`
- chat_id: `chat-sol3-20260912T2330-0500`
- node_id: `SW-N20`
- task: `M40_PRIORITY_PREFLIGHT_LICENSE_REF_PIN_SIZE`
- mode: `READ_ONLY_RESEARCH`
- claim_commit: `7fcad59c37cf5a4981b613da3f3a6156e6257cc0`
- claim_base_sha: `c462ef0891f4e0e734a6bf3bc407e98caed1fd62`
- fresh_head_before_evidence_write: `593f42bccb95e7ccacc1d71c40aedfe2b9edaaae`
- stale_head_scope_check: `PASS — intervening commits are distinct SW-Nxx worker scopes; no SW-N20 evidence/log collision observed`
- physical_mutation: `false`
- download_count: `0`
- shared_control_write: `false`

## STEP 1 — DEDUP

Authoritative inputs:
- `RESEARCH-SHORTLIST-M40-6TRACK-2026-09-11.md`
- `➡️📂 readme indice de componentes sharck imput.md` = canonical 117
- `20X-OSS-MEJORAS-2026-09-11.md` = 20 researched candidates #118-#137

M40 high-priority universe contains 22 entries:
`Inspect AI, Promptfoo, BrowserGym, AgentLab, MCPMark, TEI, LibCST, Difftastic, tree-sitter-graph, Joern, ts-morph, Hermes Agent, OpenClaw, Agent Skills spec, OpenHands Software Agent SDK, Cline, mini-SWE-agent, Newspaper4k, selectolax, curl_cffi, Browserless, OpenAI Agents SDK`.

Exact repo/name dedup result: `22/22 NONDUPLICATE` against canonical 117 and 20X. Functional overlap is handled separately below and is NOT treated as exact duplication.

## STEP 2 — OFFICIAL METADATA / LICENSE / REF / PIN / SIZE PREFLIGHT

`size_kb` is the GitHub repository metadata value observed during this audit. `pin` is an immutable commit SHA observed for the repo. A pin is evidence, not acquisition authorization.

| Candidate | Official repo | License verified | Default ref | pin | size_kb | Maintenance | Overlap / gate | Verdict |
|---|---|---|---|---|---:|---|---|---|
| Inspect AI | UKGovernmentBEIS/inspect_ai | MIT | main | `8ebe620d74c1eb679438db1b65324e30e2306092` | 434095 | ACTIVE_2026 | distinct eval framework; size moderate/high | KEEP |
| Promptfoo | promptfoo/promptfoo | MIT | main | `7b404ae0492a4f19e3fa406ab3c9c77109dce278` | 744661 | ACTIVE_2026 | overlaps Ragas/DeepEval partly; adds red-team/CI | KEEP |
| BrowserGym | ServiceNow/BrowserGym | Apache-2.0 via LICENSE readback | main | `9e779f087de9a65668b6974d11f9ce9816026e96` | 1787 | ACTIVE_2026 | overlaps browser tooling but adds benchmark env | KEEP |
| AgentLab | ServiceNow/AgentLab | Apache-2.0 via LICENSE readback | main | `cbc35a9bc0facaf731bc858c5825edbe757c719f` | 4949 | ACTIVE_2026 | strong dependency/overlap with BrowserGym agent-eval layer | DEFER |
| MCPMark | eval-sys/mcpmark | Apache-2.0 | main | `cd45b7f57923b9b3985467f5139927575f83141c` | 17732 | ACTIVE_2026 | complements MCP Registry/ToolBench as benchmark | KEEP |
| TEI | huggingface/text-embeddings-inference | Apache-2.0 | main | `e2e051afda1dbc8993979feae5f061eba80900d3` | 3172 | ACTIVE_2026 | serving layer distinct from embedding libraries | KEEP |
| LibCST | Instagram/LibCST | MIT; documented PSF/Apache-derived files | main | `d9a255843b5cdbecc6834684d233bce1f2987f9d` | 4564 | ACTIVE_2026 | overlaps AST tooling but preserves Python syntax losslessly | KEEP |
| Difftastic | Wilfred/difftastic | MIT | master | `1708c69b5ef89d346615a481b5a098d05221df23` | 1706103 | ACTIVE_2026 | structural diff useful, repository size very high | DEFER |
| tree-sitter-graph | tree-sitter/tree-sitter-graph | Apache-2.0 | main | `b930fb59c2177a90b3a6a68e1feeca6918ceb58b` | 626 | LAST_DEFAULT_COMMIT_2024 | overlaps Tree-sitter/Kythe/sqry graph lane; maintenance weak | DEFER |
| Joern | joernio/joern | Apache-2.0 | master | `4bb889d96ce972e2ded50d0d5765c514c1a032cf` | 170525 | ACTIVE_2026 | overlaps code graph tools but adds CPG/dataflow | KEEP |
| ts-morph | dsherret/ts-morph | MIT | latest | `f288183ddb496adc6f4c5b6929830b5b73437185` | 28303 | ACTIVE_2026 | TS-specific transformation capability | KEEP |
| Hermes Agent | NousResearch/hermes-agent | MIT | main | `d5774ad8807b0bf838f011c6194848ce8bc5ef38` | 948081 | ACTIVE_2026 | heavy runtime overlap with existing agent frameworks | DEFER |
| OpenClaw | openclaw/openclaw | MIT via LICENSE readback | main | `9ef7fb4ccc8f9f09dd2bd6c5331b7c0918e48da9` | 4588596 | ACTIVE_2026 | very high size + heavy runtime/control overlap | DEFER |
| Agent Skills spec | agentskills/agentskills | Apache-2.0 | main | `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | 782 | ACTIVE_2026 | standard/spec; overlaps skill repos but useful as contract reference | KEEP |
| OpenHands Software Agent SDK | OpenHands/software-agent-sdk | MIT | main | `c37007429be8b4465a83487dc1fd0914df0ea734` | 37232 | ACTIVE_2026 | overlaps PydanticAI/smolagents/agent runtimes | DEFER |
| Cline | cline/cline | Apache-2.0 | main | `cfe9cadab99617d5013bf89f07b079d105057791` | 579713 | ACTIVE_2026 | large coding-agent runtime overlap with Continue/Aider/etc. | DEFER |
| mini-SWE-agent | SWE-agent/mini-swe-agent | MIT | main | `04d809ceab9df28f9adaed044884180159172930` | 20171 | ACTIVE_2026 | minimal baseline/harness distinct enough for eval/reference | KEEP |
| Newspaper4k | AndyTheFactory/newspaper4k | MIT | master | `b53a81fc01ff54601faaeae68d6b4a6d2f18efcb` | 26174 | ACTIVE_2026 | strong extraction overlap with Trafilatura/Unstructured | DEFER |
| selectolax | rushter/selectolax | MIT | master | `54c4818d34a9e899aef64cd48bab325fac6c1b90` | 602 | ACTIVE_2026 | small deterministic HTML parser primitive | KEEP |
| curl_cffi | lexiforest/curl_cffi | MIT | main | `571560b562fe2d379a5fd9bcb3cdf032383d1e3f` | 2633 | ACTIVE_2026 | TLS/fingerprint impersonation creates policy gate | DEFER |
| Browserless | browserless/browserless | `SSPL-1.0 OR Browserless Commercial License` via LICENSE readback | main | `41948d67785a62e74b454f46916bd65c79cf63c7` | 104787 | ACTIVE_2026 | browser infrastructure overlap + non-permissive/commercial gate | REJECT |
| OpenAI Agents SDK | openai/openai-agents-python | MIT | main | `fbd2dbcaaf74a2c447c6d3fa9d5645d83fd7e292` | 47037 | ACTIVE_2026 | useful reference but overlaps existing agent orchestration/runtimes | DEFER |

### Destination gate

The current M40 architecture does not assign an authorized acquisition batch/destination for these 22 candidates. Therefore:
- `destination_status = UNASSIGNED_GATE` for all 22;
- `QUEUEABLE = 0/22` in this worker result;
- no worker may invent B07 or a new canonical destination;
- SOL-0/director/review fan-in must assign an explicit destination before any future acquisition queue.

### Classification counts
- KEEP: `11`
- DEFER: `10`
- REJECT: `1`
- TOTAL: `22`
- DOWNLOADS: `0`
- QUEUEABLE NOW: `0`

## STEP 3 — TEST / SIMULATE / REFUTE

### Tests
1. `22 = 11 KEEP + 10 DEFER + 1 REJECT` — PASS.
2. Exact dedup against 117 + 20X — `22/22` accounted, PASS.
3. Official repository metadata reviewed — `22/22`, PASS.
4. Immutable SHA observed — `22/22`, PASS.
5. NOASSERTION metadata resolved by LICENSE readback where required: BrowserGym, AgentLab, LibCST, OpenClaw, Browserless — PASS.
6. No download / canonical destination mutation / shared-control mutation — PASS.
7. Global physical/download/Step3 gates remain false — PASS.

### Three simulations
1. `selectolax`: small, active, MIT, distinct parser primitive, immutable SHA present → KEEP, but destination gate still blocks acquisition. PASS.
2. `OpenClaw`: active and MIT but multi-GB metadata size + strong runtime overlap → DEFER despite popularity/activity. PASS.
3. `Browserless`: active with immutable SHA but SSPL/commercial license + browser overlap → REJECT acquisition under normal OSS preflight. PASS.

### Three refutations
1. Refute `not an exact duplicate => KEEP`: FALSE. AgentLab/Newspaper4k/runtime candidates show functional overlap can still require DEFER.
2. Refute `active + permissive license + SHA => queueable`: FALSE. Explicit destination is still missing and acquisition gate is false.
3. Refute `immutable pin => approved/downloaded/verified`: FALSE. Pin is only provenance evidence; review/director/gates remain authoritative.

## GOALS12 OUTPUT
- G01 requirement preserved: PASS.
- G02 fresh HEAD before writes: PASS.
- G03 M48/M49 queue/DAG/control read: PASS.
- G04 atomic owner claim + readback: PASS.
- G05 dependencies/gates valid: PASS.
- G06 write scope isolated: PASS.
- G07 117+20X dedup complete: PASS.
- G08 minimum delta/read-only only: PASS.
- G09 node-specific preflight tests: PASS.
- G10 3 simulations + 3 refutations: PASS.
- G11 evidence SHA/readback: pending immediate post-write readback.
- G12 release/next-node reconciliation: pending immediate post-write readback.

## WORKER VERDICT

`PASS_PENDING_SUPERVISOR_FANIN`

This result does NOT approve acquisition, does NOT open gates, does NOT create a destination, and does NOT self-certify any candidate as VERIFIED_CLOSED.
