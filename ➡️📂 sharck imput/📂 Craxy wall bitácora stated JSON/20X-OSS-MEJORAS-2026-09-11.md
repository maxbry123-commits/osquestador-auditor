# 🦈 SHARCK INPUT V2 — 20X MEJORAS OSS / PLAN DE ADQUISICIÓN

Fecha: 2026-09-11
Estado: `RESEARCHED_CANDIDATE_NO_DOWNLOAD / REVIEW_GATE_REQUIRED`
Base de control: `STATE rev25`, `PLAN rev13`, `CHECKPOINT CP-V2-CONTROL-PLANE-RECONCILED-023`.
Catálogo canónico existente: **117** componentes. Este documento **NO** incrementa el catálogo canónico todavía: `117 + 20 candidatos`, porque `CATALOGADO/INVESTIGADO != DESCARGADO != VERIFIED_CLOSED != WIRED`.

## Reglas de entrada
- Se cruzó la lista contra `➡️📂 readme indice de componentes sharck imput.md`; ninguno de estos 20 aparece entre los 117 actuales.
- Los 20 repos fueron verificados mediante metadata GitHub como públicos y `archived=false` en 2026-09-11.
- Antes de descargar: verificar `license + default/ref exacto + commit pin + special-file/symlink surface + tamaño + destino explícito + overlap`.
- No usar HEAD mutable como evidencia final; la queue física debe recibir SHA/tag pinneado.
- Todo componente pasa `RESEARCHED_CANDIDATE → REVIEW_APPROVED → QUEUED → VERIFIED_CLOSED → WIRED → TESTED`.
- Motores canónicos permanecen inmutables; no LFS, no force, no silent overwrite, read-back obligatorio.

## 20 mejoras candidatas

| # | Componente / repo oficial | Mejora concreta para Sharck Input | Estado / gate |
|---|---|---|---|
| 118 | `webrecorder/browsertrix-crawler` | Crawl reproducible de navegador + captura WARC; fortalece `kernel.capture` y evidencia web dinámica. | `PUBLIC_NOT_ARCHIVED / LICENSE+PIN_GATE` |
| 119 | `webrecorder/warcio` | Lectura/escritura/inspección WARC; permite hashes y replay de evidencia capturada. | `PUBLIC_NOT_ARCHIVED / LICENSE+PIN_GATE` |
| 120 | `ArchiveBox/ArchiveBox` | Snapshot durable multi-formato de páginas; mejora reproducibilidad y recuperación de fuentes. | `PUBLIC_NOT_ARCHIVED / LICENSE+PIN_GATE` |
| 121 | `OpenLineage/OpenLineage` | Modelo estándar de lineage para source→retrieval→claim→context package. | `PUBLIC_NOT_ARCHIVED / LICENSE+PIN_GATE` |
| 122 | `MarquezProject/marquez` | Backend/referencia para consultar lineage OpenLineage; opcional, no obligatorio si basta ledger local. | `PUBLIC_NOT_ARCHIVED / OVERLAP_GATE` |
| 123 | `open-telemetry/opentelemetry-collector` | Traces/metrics/logs neutrales para research DAG, tools, latencia y errores. | `PUBLIC_NOT_ARCHIVED / LICENSE+PIN_GATE` |
| 124 | `open-policy-agent/opa` | Policy-as-code determinista para gates de tool/source/tenant/capability. | `PUBLIC_NOT_ARCHIVED / POLICY_POC_GATE` |
| 125 | `cedar-policy/cedar` | Política/autorización tipada fina; candidato alternativo a OPA, no instalar ambos sin comparación. | `PUBLIC_NOT_ARCHIVED / OPA_VS_CEDAR_GATE` |
| 126 | `anchore/syft` | SBOM de cada componente OSS adquirido; supply-chain provenance. | `PUBLIC_NOT_ARCHIVED / SECURITY_GATE` |
| 127 | `anchore/grype` | CVE scanning sobre SBOM/filesystem; complementa Syft. | `PUBLIC_NOT_ARCHIVED / SYFT_TRIVY_OVERLAP_GATE` |
| 128 | `aquasecurity/trivy` | Vulnerabilidades, misconfig, secrets/licensing/SBOM; posible consolidación de scanners. | `PUBLIC_NOT_ARCHIVED / OVERLAP_GATE` |
| 129 | `google/osv-scanner` | Evidencia CVE centrada en dependencias/lockfiles vía OSV. | `PUBLIC_NOT_ARCHIVED / SECURITY_GATE` |
| 130 | `gitleaks/gitleaks` | Detección de secretos antes de promover código/skills/tools. | `PUBLIC_NOT_ARCHIVED / SECURITY_GATE` |
| 131 | `567-labs/instructor` | Extracción estructurada/typed outputs; refuerza schemas en Focus/Questions/Evidence. | `PUBLIC_NOT_ARCHIVED / CONTRACT_POC_GATE` |
| 132 | `stanfordnlp/dspy` | Firmas + evaluación/optimización reproducible de módulos LLM; sólo advisory/eval, sin autoridad PASS. | `PUBLIC_NOT_ARCHIVED / EVAL_GATE` |
| 133 | `eth-sri/lmql` | Constrained LLM programs/queries; candidato para outputs con restricciones. | `PUBLIC_NOT_ARCHIVED / OVERLAP_GATE` |
| 134 | `guardrails-ai/guardrails` | Validadores y structured output; solapa Pydantic/JSON Schema/Instructor y requiere comparación. | `PUBLIC_NOT_ARCHIVED / OVERLAP_GATE` |
| 135 | `duckdb/duckdb` | Query analítica local de Evidence Ledger/snapshots/Parquet sin servicio externo. | `PUBLIC_NOT_ARCHIVED / STORAGE_POC_GATE` |
| 136 | `pola-rs/polars` | Normalización/dedup/estadísticas de evidencia con procesamiento columnar rápido. | `PUBLIC_NOT_ARCHIVED / DUCKDB_OVERLAP_GATE` |
| 137 | `souffle-lang/souffle` | Reglas Datalog deterministas para relaciones, contradicción, dependencia y coverage. | `PUBLIC_NOT_ARCHIVED / RULE_ENGINE_POC_GATE` |

## Plan físico propuesto — NO EJECUTADO

### B05 — capture / lineage / policy / supply-chain (10)
1. Browsertrix Crawler
2. warcio
3. ArchiveBox
4. OpenLineage
5. Marquez
6. OpenTelemetry Collector
7. OPA
8. Syft
9. OSV-Scanner
10. Gitleaks

Destino propuesto sólo después del gate:
`➡️📂 sharck imput/📂 input sharck code principal/📂 componentes open source/B05-capture-lineage-security/<slug>/`

### B06 — policy-alt / scanners / contracts / evidence compute (10)
1. Cedar
2. Grype
3. Trivy
4. Instructor
5. DSPy
6. LMQL
7. Guardrails
8. DuckDB
9. Polars
10. Soufflé

Destino propuesto sólo después del gate:
`➡️📂 sharck imput/📂 input sharck code principal/📂 componentes open source/B06-contracts-evidence-policy/<slug>/`

## Pruning antes de adquirir
No descargar por cantidad. GROK/M08 debe refutar solapamientos y recomendar `KEEP / DEFER / REJECT` para: `OPA↔Cedar`, `Syft+Grype↔Trivy`, `Instructor↔Guardrails↔LMQL`, `DuckDB↔Polars`, `OpenLineage↔Marquez`. ASTRA/M06 valida arquitectura/supply-chain; CLAUDE/M07 valida contratos/ports/tests. Sólo candidatos `KEEP` y con licencia/ref/commit cerrados pasan a queue.

## Criterio de aceptación B05/B06
`SOURCE_URL_OK + LICENSE_OK + PIN_IMMUTABLE + SPECIAL_SCAN_RECORDED + DESTINATION_EXPLICIT + MOTOR_BLOB_LOCK + NO_LFS + DOWNLOAD/EXTRACT + HASH_READBACK + STATE_ITEM + INDEX_ITEM`.

Veredicto actual: **20 investigados, 0 descargados, 0 wired, 0 tested**. No se suman a los 117 canónicos hasta gate y adquisición verificada.