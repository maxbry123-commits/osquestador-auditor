# SWARM CLAIMS — M47

Atomic lock namespace for `SW-N01..SW-N12`.

A worker may execute a node only if it successfully creates `CLAIM-<NODE_ID>.json` while that node is `READY_TO_CLAIM` in `CRAZY-WALL-SWARM-QUEUE-M47.json`, then reads the file back.

If the file already exists, the node is occupied: do not overwrite, do not delete, re-read main and claim another safe node.

Only SOL-0 supervisor may reconcile shared STATE/PLAN/CHECKPOINT/Handoff/Watchdog/queue after worker evidence is published.
