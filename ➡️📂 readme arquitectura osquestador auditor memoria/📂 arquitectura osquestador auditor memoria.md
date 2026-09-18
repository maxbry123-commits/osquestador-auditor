# Arquitectura — Osquestador Auditor Memoria

> Auditoría forense X-Ray de la raíz `main`.
> Fecha: 2026-09-17
> Repo: `maxbry123-commits/osquestador-auditor`

## Hallazgo crítico — TencentDB Agent Memory

**CORRECCIÓN DE HIPÓTESIS:** se pensaba que TencentDB Agent Memory podía no existir, pero la lectura fresh de `main` confirma que **SÍ EXISTE físicamente** en:

`TencentDB-Agent-Memory/`

El README interno identifica el upstream como `https://github.com/Tencent/TencentDB-Agent-Memory.git` y describe un Memory Hub/Proxy compartido para agentes.

Top-level materializado (27 entradas):
- `TencentDB-Agent-Memory/.github`
- `TencentDB-Agent-Memory/.gitignore`
- `TencentDB-Agent-Memory/CHANGELOG.md`
- `TencentDB-Agent-Memory/CONTRIBUTING.md`
- `TencentDB-Agent-Memory/CONTRIBUTING_CN.md`
- `TencentDB-Agent-Memory/INSTALL.md`
- `TencentDB-Agent-Memory/INSTALL_CN.md`
- `TencentDB-Agent-Memory/LICENSE`
- `TencentDB-Agent-Memory/MemoryCore`
- `TencentDB-Agent-Memory/MemoryKnowledge`
- `TencentDB-Agent-Memory/MemoryPanel`
- `TencentDB-Agent-Memory/MemoryProxy`
- `TencentDB-Agent-Memory/README.deployment.md`
- `TencentDB-Agent-Memory/README.docker.md`
- `TencentDB-Agent-Memory/README.md`
- `TencentDB-Agent-Memory/README_CN.md`
- `TencentDB-Agent-Memory/ROADMAP.md`
- `TencentDB-Agent-Memory/ROADMAP_CN.md`
- `TencentDB-Agent-Memory/TencentDB-Agent-Memory_0001.zip`
- `TencentDB-Agent-Memory/TencentDB-Agent-Memory_0002.zip`
- `TencentDB-Agent-Memory/TencentDB-Agent-Memory_0003.zip`
- `TencentDB-Agent-Memory/TencentDB-Agent-Memory_0004.zip`
- `TencentDB-Agent-Memory/agents`
- `TencentDB-Agent-Memory/assets`
- `TencentDB-Agent-Memory/deploy`
- `TencentDB-Agent-Memory/docs`
- `TencentDB-Agent-Memory/sdk`

**GAP:** presencia física confirmada; esta auditoría NO declara integración funcional global ni despliegue PASS.

## X-Ray de componentes

Raíz inspeccionada: `main`.
Entradas totales de primer nivel: **194**.
Directorios de primer nivel: **158**.
Archivos de primer nivel: **36**.

### Inventario completo de directorios / componentes y subsistemas de primer nivel

> Para evitar falsos positivos, esta lista se denomina “directorios/componentes/subsistemas”: algunos son componentes OSS y otros son infraestructura, documentación o control del proyecto.

1. `.github/`
2. `AFFiNE/`
3. `Acontext/`
4. `Agente motores nct/`
5. `Agente motores osquestador auditor memoria/`
6. `AppFlowy/`
7. `BLAKE3/`
8. `BrowserUse/`
9. `DOCUMENTOS-MAXBRY/`
10. `Desplegar nct/`
11. `Desplegar osquestador auditor memoria/`
12. `Documentos proyectos nct/`
13. `Documentos proyectos osquestador auditor memoria/`
14. `Download code NCT/`
15. `Download code osquestador auditor memoria/`
16. `FalkorDB/`
17. `GPTCache/`
18. `GraphRAG/`
19. `Graphify/`
20. `HyperMem/`
21. `IMPORTED_CODE/`
22. `LangChain/`
23. `LibreTranslate/`
24. `MegaMem/`
25. `MemOS/`
26. `Memora/`
27. `Memoria/`
28. `Milvus/`
29. `Método de trabajo nct/`
30. `Método de trabajo osquestador auditor memoria/`
31. `Método de trabajo/`
32. `NCT neuronas code turbo/`
33. `Notas de trabajo grock gpt osquestador auditor memoria/`
34. `PIPELINE nct/`
35. `PIPELINE osquestador auditor memoria/`
36. `PIPELINE-osquestador-auditor-memoria/`
37. `PIPELINE/`
38. `PaddleOCR/`
39. `Perplexica/`
40. `RapidFuzz/`
41. `Refactoria nct/`
42. `Refactoria osquestador auditor memoria/`
43. `SWE-agent/`
44. `Skills de trabajos osquestador auditor memoria/`
45. `Speech/`
46. `TencentDB-Agent-Memory/`
47. `Weaviate/`
48. `_work/`
49. `agent-memory/`
50. `agentic-memory/`
51. `agentmemory/`
52. `agents-deep-research/`
53. `airflow/`
54. `anytype-ts/`
55. `argo-workflows/`
56. `argos-translate/`
57. `ast-grep/`
58. `automerge/`
59. `cachelib/`
60. `cass_memory_system/`
61. `chroma/`
62. `cloudflared/`
63. `code-session-memory/`
64. `componentes open soure osquestador auditor memoria/`
65. `conectividad con Router inteligente universal/`
66. `crawl4ai/`
67. `cryptography/`
68. `dagster/`
69. `dbos-transact-ts/`
70. `deep-research/`
71. `docker-py/`
72. `docs/`
73. `dolphinscheduler/`
74. `duckdb/`
75. `engram-memory/`
76. `excalidraw/`
77. `faiss/`
78. `fastapi/`
79. `forensics/`
80. `git/`
81. `graphiti/`
82. `graphology/`
83. `guardrails/`
84. `haystack/`
85. `hermes-agent/`
86. `inngest/`
87. `joplin/`
88. `kanboard/`
89. `khoj/`
90. `kuzu/`
91. `la coneccion de todos los repos con el almacenamiento de huggueface/`
92. `ladybug/`
93. `lancedb/`
94. `litestream/`
95. `llama_index/`
96. `logseq/`
97. `memos/`
98. `memvid/`
99. `mnemon/`
100. `moby/`
101. `n8n/`
102. `nats-server/`
103. `neo4j/`
104. `obsidian-releases/`
105. `ollama/`
106. `opentelemetry-specification/`
107. `orchestrator/`
108. `parakeet.cpp/`
109. `pgvector/`
110. `phoenix/`
111. `plandex/`
112. `playwright/`
113. `plex/`
114. `prefect/`
115. `pydantic-ai/`
116. `pydantic-settings/`
117. `pydantic/`
118. `python-diskcache/`
119. `python-sdk/`
120. `pyyaml/`
121. `react/`
122. `reception/`
123. `recycle/`
124. `redis-py/`
125. `repomix/`
126. `restate/`
127. `restic/`
128. `rqlite/`
129. `scripts/`
130. `searxng/`
131. `semgrep/`
132. `sentence-transformers/`
133. `servers/`
134. `sessions/`
135. `siyuan/`
136. `skills agente nct/`
137. `skills agente osquestador auditor memoria/`
138. `sqlite-vec/`
139. `sqlite/`
140. `systemd/`
141. `tailwindcss/`
142. `terminusdb/`
143. `tesseract/`
144. `tika/`
145. `tree-sitter/`
146. `trigger.dev/`
147. `ultralytics/`
148. `unstructured/`
149. `valkey/`
150. `vllm/`
151. `watchdog/`
152. `whisper/`
153. `whisperX/`
154. `xxl-job/`
155. `yt-dlp/`
156. `➡️📂 Shack imput/`
157. `➡️📂 sharck imput/`
158. `➡️📂motores de descarga extracción copiado movimiento archivos osquestador-auditor/`

## Biblioteca explícita de componentes open source

Ruta: `componentes open soure osquestador auditor memoria/`

- `Cognee`
- `LangGraph`
- `Mem0`
- `Neo4j-Agent-Memory`
- `RDC_ADDITIONAL_COMPONENTS_EVIDENCE.json`
- `archives`

## Evidencia y conclusiones X-Ray

- `TencentDB-Agent-Memory/`: **PRESENTE**.
- `componentes open soure osquestador auditor memoria/`: **PRESENTE**.
- Se detectaron **158 directorios** en la raíz `main`; se inventariaron todos arriba, sin omitir directorios por asumir que eran componentes.
- Esta auditoría es de **presencia/estructura**. No convierte presencia en “integrado”, “desplegado” o “PASS”.
- TencentDB Agent Memory contiene módulos `MemoryCore`, `MemoryKnowledge`, `MemoryPanel`, `MemoryProxy`, `agents`, `deploy`, `docs` y `sdk`, además de archivos de instalación/documentación y archivos ZIP materializados.
- Próximo GAP técnico: verificar cableado real de TencentDB Agent Memory con el orquestador y ejecutar pruebas de integración antes de marcarlo integrado.

## Estado

`X_RAY_ROOT_INVENTORY=PASS`
`TENCENTDB_AGENT_MEMORY_PRESENT=TRUE`
`TENCENTDB_AGENT_MEMORY_INTEGRATION=UNVERIFIED`
