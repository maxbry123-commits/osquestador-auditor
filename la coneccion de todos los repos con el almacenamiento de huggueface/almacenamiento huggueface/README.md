# almacenamiento huggueface

Centro lógico de almacenamiento para los repositorios GitHub conectados.

Fuente de código/versionado: GitHub.
Almacenamiento de trabajo: Hugging Face Storage Bucket.
Bucket reutilizado inicialmente: `COMAND-CENTER-1/claude-github-mcp-backup-storage`.

Namespace por repo:
`/repos/<owner>__<repo>/`

Cada namespace puede contener `input/`, `output/`, `cache/`, `logs/`, `state/` y `artifacts/` sin duplicar el repositorio completo.

El mapa de repos verificados está en `registry.json`.
