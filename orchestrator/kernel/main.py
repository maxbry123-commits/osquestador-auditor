"""
orchestrator/kernel/main.py — KERNEL DEL OSQUESTADOR (200 LOC max)
================================================================
Loop principal del orquestador Fase 0.
- Lee inbox/ cada poll_seconds
- Detecta nuevos docs
- Hashea SHA256, registra en inventory.json (idempotencia)
- Despacha evento → router → workflow → agent
- Atomic write state + dead_letter
- Graceful shutdown SIGTERM
"""
import os, sys, time, json, signal, hashlib, logging, traceback
from pathlib import Path
from datetime import datetime, timezone

# Constantes
ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
VAULT = ROOT / "vault"
STATE = ROOT / "state"
WORKFLOWS = ROOT / "workflows"
AGENTS = ROOT / "agents"
INVENTORY = STATE / "inventory.json"
HEALTH = STATE / "health.json"
DEAD_LETTER = STATE / "dead_letter.json"
WORKFLOW_STATE = STATE / "workflow_state.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("kernel")

_running = True

def atomic_write_json(path: Path, data: dict):
    """Write JSON atomically: tmp file + rename. SIGKILL-safe."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log.warning("load_json %s: %s", path, e)
        return default

def save_inventory(inv):
    atomic_write_json(INVENTORY, inv)

def save_health(status, step, **meta):
    atomic_write_json(HEALTH, {"ts": datetime.now(timezone.utc).isoformat(), "status": status, "step": step, "pid": os.getpid(), **meta})

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def discover_inbox():
    """Devuelve lista de archivos en inbox/<proyecto>/<archivo>."""
    files = []
    if not INBOX.exists():
        return files
    for proyecto_dir in INBOX.iterdir():
        if not proyecto_dir.is_dir() or proyecto_dir.name.startswith("_"):
            continue
        for f in proyecto_dir.iterdir():
            if f.is_file() and not f.name.startswith("."):
                files.append({"path": f, "proyecto": proyecto_dir.name, "name": f.name})
    return files

def is_processed(inv, sha):
    return any(item.get("sha") == sha for item in inv.get("items", []))

def add_to_inventory(inv, sha, proyecto, name):
    inv.setdefault("items", []).append({
        "sha": sha,
        "proyecto": proyecto,
        "name": name,
        "ts": datetime.now(timezone.utc).isoformat(),
        "estado": "ingestado",
    })

def route_event(doc):
    """Router: decide qué workflow aplicar al doc."""
    # Por ahora, todos los docs van al workflow de ingesta
    wf_path = WORKFLOWS / "ingesta.workflow.json"
    return wf_path

def execute_workflow(wf_path, doc, inv):
    """Ejecuta un workflow sobre un doc."""
    wf = load_json(wf_path, {"steps": []})
    log.info("workflow %s on %s", wf_path.name, doc["name"])
    ctx = {"doc": doc, "inv": inv, "results": {}}
    for step in wf.get("steps", []):
        try:
            log.info("  step: %s", step.get("name", "?"))
            if step.get("type") == "ocr":
                from orchestrator.agents.ocr import run_ocr
                ctx["results"]["ocr_text"] = run_ocr(doc["path"])
            elif step.get("type") == "classify":
                from orchestrator.agents.classifier import classify
                ctx["results"]["proyecto"] = classify(doc, ctx)
            elif step.get("type") == "save_vault":
                from orchestrator.agents.obsidian_adapter import save_to_vault
                save_to_vault(doc, ctx)
            elif step.get("type") == "graphiti_node":
                from orchestrator.agents.graphiti_adapter import add_node
                ctx["results"]["graphiti_node"] = add_node(doc, ctx)
            elif step.get("type") == "kanboard_task":
                from orchestrator.agents.kanboard_adapter import create_task
                ctx["results"]["kanboard_task"] = create_task(doc, ctx)
            elif step.get("type") == "done":
                log.info("  workflow DONE")
                return True
        except Exception as e:
            log.error("step %s failed: %s", step.get("name"), e)
            traceback.print_exc()
            dead_letter = load_json(DEAD_LETTER, [])
            dead_letter.append({"doc": doc["name"], "step": step.get("name"), "error": str(e), "ts": datetime.now(timezone.utc).isoformat()})
            atomic_write_json(DEAD_LETTER, dead_letter)
            return False
    return True

def shutdown(signum, frame):
    global _running
    log.info("signal %s received, shutting down gracefully", signum)
    _running = False

def main():
    global _running
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    log.info("Osquestador kernel starting (pid %d)", os.getpid())
    VAULT.mkdir(parents=True, exist_ok=True)
    STATE.mkdir(parents=True, exist_ok=True)
    INVENTORY.touch(exist_ok=True)
    HEALTH.touch(exist_ok=True)
    inv = load_json(INVENTORY, {"items": []})
    save_health("alive", "boot")
    while _running:
        try:
            files = discover_inbox()
            save_health("alive", "polling", inbox_count=len(files))
            for doc in files:
                sha = sha256_file(doc["path"])
                if is_processed(inv, sha):
                    log.debug("skip already-processed: %s", doc["name"])
                    continue
                log.info("NEW: %s/%s sha=%s", doc["proyecto"], doc["name"], sha[:12])
                wf = route_event(doc)
                ok = execute_workflow(wf, doc, inv)
                if ok:
                    add_to_inventory(inv, sha, doc["proyecto"], doc["name"])
                    save_inventory(inv)
            time.sleep(2)
        except Exception as e:
            log.error("loop error: %s", e)
            traceback.print_exc()
            save_health("error", "loop", error=str(e))
            time.sleep(5)
    save_health("shutdown", "stopped")
    log.info("kernel stopped")

if __name__ == "__main__":
    main()
