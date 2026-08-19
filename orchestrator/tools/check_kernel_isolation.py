#!/usr/bin/env python3
"""Linter: falla si kernel/ nombra plugins o proveedores específicos."""
import os, re, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROHIBIDO = re.compile(
    r"(telegram|kanboard|obsidian|graphiti|haystack|plandex|hermes|notion|"
    r"slack|cerebras|groq|swe\b|repomix)", re.I)
errores = []
for fn in os.listdir(os.path.join(BASE, "kernel")):
    if not fn.endswith(".py"): continue
    for i, linea in enumerate(open(os.path.join(BASE, "kernel", fn), encoding="utf-8"), 1):
        if PROHIBIDO.search(linea):
            errores.append(f"kernel/{fn}:{i}: {linea.strip()}")
if errores:
    print("VIOLACIONES DE AISLAMIENTO:"); print("\n".join(errores))
    sys.exit(1)
print("kernel limpio ✓")
