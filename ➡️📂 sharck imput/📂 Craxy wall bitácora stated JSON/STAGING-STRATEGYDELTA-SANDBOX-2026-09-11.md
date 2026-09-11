# STAGING StrategyDelta — SANDBOX — 2026-09-11

Estado: `SANDBOX_PASS / REVIEW_REQUIRED / NO_PHYSICAL_REPAIR`.

## Objetivo
Probar una vía de publicación que preserve exactamente archivos TRACKED upstream sin editar motores canónicos y sin repetir los fallos demostrados de `.gitignore` / `.gitattributes`.

## Evidencia
Workflow: `.github/workflows/sharck-input-staging-strategydelta-lite.yml`  
Commit: `2499be177fd359825051a9dba4bc09c5cfad7b02`  
Run: `34568249222`  
Job: `103164691377`  
Conclusion: `success`.

Motor usado: `motor_3_copy_batches.py` blob canónico `3689924361ce4a1a9fde4ae2b6f6009c37a6042d`.

Fuentes reales/pinneadas:
- spaCy `26b4d1dc04a812f426e4bef3e8a1b6f159d6f048`.
- OpenSearch `0249cde03ef66b56ac61e8929c3ba7e10b062523`.
- sqry `631710ce145b6ef6adb527dda13ac60e20be16cf`.

## Reproducción del método actual
Después de Motor 3, `git add -- vendor` produjo:
- `vendor/spaCy/spacy/matcher/polyleven.c` → `indexed=False`.
- `vendor/spaCy/website/.vscode/extensions.json` → `indexed=False`.
- `vendor/sqry/sqry-core/src/graph/unified/build/entrypoint.rs` → `indexed=False`.
- `vendor/OpenSearch/.../commons-collections4-LICENSE.txt` → `indexed=True` pero `byte_equal=False`.

Esto reproduce las dos clases raíz ya demostradas: ignored tracked files + EOL normalization.

## Candidate staging probado
Sin editar Motor 3:
1. Motor 3 copia y verifica source→sandbox destino.
2. Se aparta temporalmente `.gitattributes` del snapshot OpenSearch sólo durante staging.
3. `git add -f -- vendor` indexa los archivos que eran TRACKED upstream aunque sus `.gitignore` los marquen ignorados al ser re-vendorized.
4. Se restaura `.gitattributes` exacto.
5. Se indexa `.gitattributes` restaurado.
6. Se compara blob de index contra bytes fuente antes de commit.

## Resultado byte-a-byte
- spaCy `polyleven.c`: `byte_equal=True`, mode=`100644`, SHA256 `8d6cc95a1e44c334c3a5c1ffe3011f7e8d7a0afea27345d769a7db7d16abce0a`.
- spaCy `website/.vscode/extensions.json`: `byte_equal=True`, mode=`100644`, SHA256 `515b1ef75f9d7e9b2e63f7009ffe9b9cf4a809b27d7a96265f72f48127767fdf`.
- sqry `entrypoint.rs`: `byte_equal=True`, mode=`100644`, SHA256 `88737e89669fb45c385b09e86d6095a9ed049d887c8714572b2bbf3922c294d2`.
- OpenSearch LICENSE: `byte_equal=True`, mode=`100644`, SHA256 `3abbdb7c0bd9762290440313110a225d312493a9b060d195123bc2d0c22bfb1c`.

Final: `CANDIDATE_VERDICT=SANDBOX_PASS`.

## Lo que este PASS NO significa
- No repara ningún componente físico.
- No autoriza editar el motor.
- No autoriza `git add -f` en producción por sí solo.
- No demuestra todavía el árbol completo de 11 partials; prueba representativa con causas reales.
- Special-file/symlink gaps siguen separados y nunca se fuerzan con esta estrategia.

## Revisión requerida
### CLAUDE / M07
- validar que el wrapper indexe exclusivamente el conjunto TRACKED upstream validado contra source commit;
- validar mode 100644/100755 y no sólo bytes;
- añadir test completo `source tracked set == staged set == published set`;
- decidir si es preferible Git plumbing (`hash-object --no-filters` + index/tree) frente a neutralización temporal de attributes.

### ASTRA / M06
- verificar que el wrapper no debilite NO_LFS, blob limits, special-file gate, no-force, no-overwrite y read-back;
- preferir destino/versionado recuperable y fail-closed.

### GROK / M08
- contrastar patrón con prácticas de vendoring/snapshot Git y alternativas package/subtree oficiales.

## Gate de producción
`SANDBOX_PASS → M06 + M07 + M08 REVIEW → DIRECTOR GATE → physical repair 1×1 → canonical full read-back → VERIFIED_CLOSED`.
