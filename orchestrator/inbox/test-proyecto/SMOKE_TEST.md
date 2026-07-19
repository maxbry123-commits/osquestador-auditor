# Test Smoke del Orquestador Fase 0

Este es un documento de prueba para validar que el kernel del osquestador
funciona end-to-end:

1. Detecta el doc en inbox
2. Calcula SHA256
3. Verifica inventario (idempotencia)
4. Ejecuta workflow de ingesta
5. Crea nodo en Graphiti (in-process)
6. Crea tarea en Kanboard (in-process)
7. Guarda en vault

objetivo: validar Fase 0 end-to-end
decision: usar SQLite WAL
proyecto: test-proyecto
