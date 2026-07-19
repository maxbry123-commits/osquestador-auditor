# knowledge.policy — anti-síntesis, anti-pérdida

1. Ningún agente resume contenido — solo clasifica, relaciona, señala.
2. El original íntegro vive en `vault/<proyecto>/`; Graphiti solo guarda relaciones y metadata.
3. Nada entra al árbol sin clasificación y hash.
4. Ninguna tarea se cierra sin actualizar Graphiti + Obsidian + Kanboard.
5. Ningún doc se procesa dos veces (inventory.json es ley).
6. Toda escritura de state usa `atomic_write_json` (SIGKILL-safe).
7. Si un step falla → `dead_letter.json` (no se pierde, no se reintenta infinito).
