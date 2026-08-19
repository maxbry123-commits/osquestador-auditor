#!/usr/bin/env python3
"""python3 tools/scaffold.py input notion → inputs/notion/ listo."""
import os, sys, json
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIPOS = {"input": ("inputs", "InputAdapter", "input.v1"),
         "output": ("outputs", "OutputConnector", "output.v1"),
         "agent": ("agents", "AgentAdapter", "agent.v1")}

def main():
    if len(sys.argv) < 3:
        print("uso: python3 tools/scaffold.py <tipo> <nombre>")
        print("tipos:", list(TIPOS.keys()))
        sys.exit(1)
    tipo, nombre = sys.argv[1], sys.argv[2]
    carpeta, clase, iface = TIPOS[tipo]
    d = os.path.join(BASE, carpeta, nombre); os.makedirs(d, exist_ok=True)
    m = {"type": tipo, "name": nombre, "version": "0.1", "iface": iface, "status": "active"}
    if tipo == "agent": m["capabilities"] = ["TODO"]
    if tipo == "output": m["capability"] = "TODO"
    json.dump(m, open(os.path.join(d, "manifest.json"), "w"), indent=2)
    open(os.path.join(d, "adapter.py"), "w").write(
        f"from ...base.contracts import {clase}\n\n"
        f"class {nombre.capitalize()}Plugin({clase}):\n"
        f"    name = \"{nombre}\"\n"
        f"    # TODO: implementar contrato {iface}\n"
    )
    open(os.path.join(d, "README.md"), "w").write(
        f"# {nombre}\n\nTODO: propósito, config, ejemplos.\n")
    print(f"✓ {carpeta}/{nombre}/ creado — implementar adapter.py")

if __name__ == "__main__": main()
