# AGENTS.md — maxbry123-commits/osquestador-auditor

## Authority
- Work method: `PIPELINE/00_METODO_TRABAJO_Y_ARQUITECTURA.md`
- Forensic audit: `PIPELINE/FORENSIC_CODE_AUDIT.md`
- Canonical sibling (mismo método): `maxbry123-commits/agentes`
- Engineering standard: `agentes/PIPELINE/ADVANCED_ENGINEERING_STANDARD_V3.md`

## Hard rules
- Handoff ≠ full traceability; missing context/handoff → BLOCK
- COPY-FIRST before GENERATE
- LLM cannot declare PASS; VerdictAuthority only
- GitHub is source of truth; no sandbox storage claims

## Programming pipeline
`CONTEXT → COPY-FIRST → IMPLEMENT → WIRE → FORENSIC 4-PASS → VERDICT → CLOSED|FIX`

Code (vive en agentes): `extensions/wordflow/engine/programming_pipeline.py`  
Gates: `extensions/wordflow/standards/executor_gates.py`
