"""Agent: Obsidian adapter — guarda docs en vault/<proyecto>/."""
from pathlib import Path
import logging, shutil
log = logging.getLogger("obsidian")

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"

def save_to_vault(doc, ctx):
    """Copia el doc al vault con su contenido procesado."""
    proyecto = doc.get("proyecto", "desconocido")
    target_dir = VAULT / proyecto
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / doc["name"]
    if doc["path"].suffix.lower() in (".md", ".txt"):
        shutil.copy2(doc["path"], target)
    else:
        # Para binarios, guardar junto a un .md con metadata
        shutil.copy2(doc["path"], target)
        meta = target_dir / (doc["name"] + ".md")
        meta.write_text(f"# {doc['name']}\n\nTipo: binario\nOrigen: {doc['path']}\n", encoding="utf-8")
    log.info("saved to vault: %s", target)
    return str(target)
