CROSS_REPOSITORY_MOVE = NOT_ATOMIC_GIT_MV

IF SOURCE_REPOSITORY != DESTINATION_REPOSITORY:
    METHOD = CROSS_REPOSITORY_TRANSFER
    DEFAULT:
        COPY_FIRST
        PRESERVE_SOURCE = TRUE
        VERIFY_DESTINATION = REQUIRED
    NEVER:
        pretend_git_mv
        rewrite_existing_code
        delete_source_automatically

COPY_FIRST: A → B, A permanece.
TRANSFER/MOVE SEMÁNTICO: COPY → VERIFY → AUTHORIZE DELETE FROM A → DELETE FROM A → COMMIT A

Entre repositorios: COPY-FIRST por defecto. Nunca borrar el origen automáticamente.

Canónico completo: https://github.com/maxbry123-commits/agentes/blob/main/PIPELINE/58_CROSS_REPOSITORY_TRANSFER.md
