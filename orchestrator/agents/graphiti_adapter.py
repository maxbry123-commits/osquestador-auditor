"""Agent: Graphiti adapter — crea entidades/relaciones en memoria."""
import logging
from pathlib import Path
log = logging.getLogger("graphiti")
STATE = Path(__file__).resolve().parent.parent / "state"
GRAPH = STATE / "graph.json"

def _load():
    if not GRAPH.exists(): return {"entities": [], "relations": []}
    import json
    return json.loads(GRAPH.read_text(encoding="utf-8"))

def _save(g):
    import json, os
    tmp = GRAPH.with_suffix(".tmp")
    tmp.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, GRAPH)

def add_node(doc, ctx):
    """Crea un entity con el nombre del doc y tipo 'documento'."""
    import json
    g = _load()
    eid = f"doc::{doc['name']}"
    if any(e.get("id") == eid for e in g["entities"]):
        log.info("entity already exists: %s", eid)
        return eid
    g["entities"].append({
        "id": eid,
        "type": "documento",
        "name": doc["name"],
        "proyecto": doc.get("proyecto"),
        "ts": ctx.get("ts", ""),
    })
    g["relations"].append({
        "from": eid,
        "to": f"proyecto::{doc.get('proyecto', 'desconocido')}",
        "type": "pertenece_a",
    })
    _save(g)
    log.info("graphiti node created: %s", eid)
    return eid

def search(query, project=None, limit=10):
    import json
    g = _load()
    q = query.lower()
    hits = [e for e in g["entities"] if q in e.get("name", "").lower() or q in e.get("proyecto", "").lower()]
    if project:
        hits = [e for e in hits if e.get("proyecto") == project]
    return hits[:limit]
