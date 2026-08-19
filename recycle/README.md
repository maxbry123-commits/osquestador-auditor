# recycle/ — COPY-FIRST, no rewrite

Subset needed for osquestador-auditor + memoria.
Source repos stay intact. Do not copy the entire `agentes` tree here.

See `SOURCE_MAP.yaml` for SHA provenance.

## SALIDA-2 layout

```
recycle/
  audit_forensic/          # engine P0-P3 + EvidencePacket (from agentes)
  wordflow/                # abi + reuse_12 + memory_port + copy_first
  wordflow_kernel/         # bootstrap / ficha / llm_control / memory_slot
  memoria/                 # MEMORIA-FRONT + DOC_UPLOAD_SCHEMA
```

Canonical work repo: `maxbry123-commits/osquestador-auditor`
Cuenta 2 `abc1tienda-web`: UNREACHABLE from this GitHub token.
