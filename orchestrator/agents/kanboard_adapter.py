"""Agent: Kanboard adapter — crea tareas vía JSON-RPC (o mock si no hay Kanboard)."""
import json, logging, os
from pathlib import Path
log = logging.getLogger("kanboard")
STATE = Path(__file__).resolve().parent.parent / "state"
TASKS = STATE / "tasks.json"

def _load():
    if not TASKS.exists(): return {"tasks": []}
    return json.loads(TASKS.read_text(encoding="utf-8"))

def _save(t):
    tmp = TASKS.with_suffix(".tmp")
    tmp.write_text(json.dumps(t, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, TASKS)

def create_task(doc, ctx):
    """Crea tarea local. Si KANBOARD_URL está set, intenta JSON-RPC."""
    kb_url = os.environ.get("KANBOARD_URL", "")
    if kb_url:
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{kb_url}/jsonrpc.php",
                data=json.dumps({"jsonrpc": "2.0", "method": "createTask", "params": {"title": f"Procesar {doc['name']}", "project_id": int(os.environ.get("KANBOARD_PROJECT_ID", "1"))}, "id": 1}).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                log.info("kanboard rpc ok: %s", r.read()[:80])
        except Exception as e:
            log.warning("kanboard rpc failed: %s, fallback local", e)
    t = _load()
    tid = len(t["tasks"]) + 1
    task = {
        "id": tid,
        "title": f"Procesar {doc['name']}",
        "proyecto": doc.get("proyecto"),
        "column": "backlog",
        "priority": "medium",
        "agente_recomendado": "auditor",
        "ts": ctx.get("ts", ""),
    }
    t["tasks"].append(task)
    _save(t)
    log.info("kanboard task created local: %s", tid)
    return tid
