# SOL-SWARM-05 LOG — SHARCK INPUT

- agent_name: `SOL-5-GPT`
- state: `READY_NO_ACTIVE_CLAIM`
- active_node: `null`
- rule: claim only one `READY_TO_CLAIM` node from `SWARM-DAG-8SOL-M47-v1.json` after fresh read; write only this log + node-unique evidence; never write shared STATE/PLAN/CHECKPOINT/Handoff/Watchdog/DAG.
- reserved nodes forbidden: `M06_ASTRA`, `M07_CLAUDE`, `M08_GROK`.
- physical mutation: forbidden while latest gates remain false.
