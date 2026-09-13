# SW-N43 EVIDENCE — M40 KEEP DESTINATION/PORT MAP RECOVERY

- schema: `sharck-input.swarm-node-evidence.v1`
- node_id: `SW-N43`
- agent_name: `SOL-5-GPT`
- mode: `READ_ONLY_ARCHITECTURE`
- canonical_mutation: `NO`
- downloads_wiring: `0`
- physical_destination_gate: `UNASSIGNED_GATE`

## STEP 1 — source truth
N20 classifies exactly 11 KEEP: Inspect AI, Promptfoo, BrowserGym, MCPMark, TEI, LibCST, Joern, ts-morph, Agent Skills spec, mini-SWE-agent, selectolax. N20 explicitly forbids inventing a new acquisition batch/destination while the destination gate is unassigned. V2.1 uses logical adapters/ports; existing examples include `capture.warc`, `provenance.lineage`, `observability.otel`, `policy.engine`, `structured_output`, `evidence.compute`, `evidence.rules`, `llm_policy_eval`. N33 fixes selectolax boundary as `extract.html_parser`, not `extract.article`.

## STEP 2 — proposed logical map
Physical acquisition destination remains `UNASSIGNED_GATE` for all rows.

| KEEP | logical destination / owner | capability port | conflict disposition |
|---|---|---|---|
| Inspect AI | `labs` | `eval.agent` | distinct agent-eval lane |
| Promptfoo | `labs` | `eval.redteam` | distinct from advisory `llm_policy_eval` |
| BrowserGym | `labs` | `eval.browser_env` | benchmark env; not `capture.warc` |
| MCPMark | `tool_finder` | `eval.mcp_tooling` | benchmark; not MCP registry/discovery |
| TEI | `huggingface` | `hf.embedding_server` | distinct from dataset/Space ports |
| LibCST | `code_pointer` | `code.python_cst` | lossless Python CST lane |
| Joern | `code_pointer` | `code.cpg_dataflow` | CPG/dataflow lane; no Kythe/sqry replacement implied |
| ts-morph | `code_pointer` | `code.ts_ast` | TS/JS transform lane |
| Agent Skills spec | `skill_pointer` | `skill.contract` | contract/spec; not registry retrieval |
| mini-SWE-agent | `labs` | `eval.code_agent_harness` | sandbox baseline; not production agent runtime |
| selectolax | `extract` | `extract.html_parser` | parser only; Trafilatura article baseline preserved |

## Conflict matrix / guards
- unique proposed port IDs: `11/11 PASS`.
- exact collision against named V2.1 ports: `0/11`.
- acquisition destination assigned: `0/11`; all remain fail-closed until supervisor/director assigns a legal batch/destination.
- canonical catalog change: `0`; download/install/wiring: `0`.
- functional overlap is handled by port boundary, not treated as approval: Joern remains CPG/dataflow-only; Promptfoo red-team-only; BrowserGym eval-environment-only; mini-SWE-agent eval-harness-only; selectolax parser-only.

## STEP 3 — tests + exactly 3 refutations
Tests:
1. `KEEP_COUNT=11/11 PASS`.
2. `MAP_COMPLETE=11/11 PASS`.
3. `PORT_UNIQUENESS=11/11 PASS`.
4. `EXACT_EXISTING_PORT_COLLISIONS=0 PASS`.
5. `UNASSIGNED_PHYSICAL_DESTINATION=11/11 PASS`.
6. `NO_DOWNLOAD_NO_WIRING_NO_CANONICAL_WRITE=PASS`.

Refutations:
1. `KEEP => approved/downloadable` — REFUTED: destination and global gates remain closed.
2. `eval adapter => production runtime replacement` — REFUTED: eval/browser/harness ports are advisory/test-only boundaries.
3. `selectolax parser success => article extractor replacement` — REFUTED: `extract.html_parser` is separate from `extract.article`; Trafilatura baseline remains authoritative.

## Verdict
`PASS_PENDING_SUPERVISOR_FANIN` — 11/11 KEEP mapped to non-overlapping logical destinations/capabilities/ports/owners, with zero acquisition or wiring. No physical destination or new batch was invented.
