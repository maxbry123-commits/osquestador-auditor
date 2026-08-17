# osquestador-auditor

Orquestador auditor del ecosistema YAIWES / NCT.

## Método de trabajo — multi-cuenta (obligatorio)

```
CUENTA A (sistema vivo)
  maxbry123-commits/agentes          ← Wordflow / kernel
  maxbry123-commits/maxbry-router    ← Router
  maxbry123-commits/osquestador-auditor  ← este repo
  maxbry123-commits/MEMORIA
        │
        │ credential_ref (nunca token en git/chat)
        ▼
CUENTA B (almacén software, NO ejecuta)
  ej. abc1tienda-web / repos de software, forks, tools
        │
        │ download/clone/API
        ▼
RUNTIME (VPS / sandbox / HF Space)  ← aquí se ejecuta
HF ← datasets / models / skills grandes
```

| Qué vive aquí (Cuenta A) | Qué NO saturar aquí |
|--------------------------|---------------------|
| Orquestación, auditoría, plugins del auditor | Software externo completo, datasets grandes |

### Conexión a Cuenta B

El conector canónico está en el repo sistema:

- https://github.com/maxbry123-commits/agentes/blob/main/extensions/wordflow/connectors/github_external.py
- Método: https://github.com/maxbry123-commits/agentes/blob/main/PIPELINE/53_MULTI_ACCOUNT_STORAGE_METHOD.md

Este repo **usa el mismo contrato**: `account_id` + `credential_ref` + `owner/repo/branch`.  
Tokens solo en secret store / variables de entorno del runtime.

### Contenido histórico del repo

Material de limpieza 2026-07 y docs fuente en `docs/`. El método multi-cuenta aplica a todo trabajo nuevo.
