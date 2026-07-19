"""Agent: Classifier — detecta proyecto y tipo del doc."""
import re, logging
log = logging.getLogger("classifier")

def classify(doc, ctx):
    """Devuelve el nombre del proyecto. Usa la carpeta del inbox como verdad."""
    return doc.get("proyecto", "desconocido")
