# -*- coding: utf-8 -*-
import os, json, time, uuid, signal, random, hashlib, threading
from datetime import datetime, timezone

def now(): return datetime.now(timezone.utc).isoformat()
def new_id(): return uuid.uuid4().hex[:12]

def atomic_write_json(path, data):
    tmp = f"{path}.{uuid.uuid4().hex}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)

def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except Exception: return default

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""): h.update(c)
    return h.hexdigest()

def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

_LOG_PATH = None
def init_log(path):
    global _LOG_PATH; _LOG_PATH = path
def jlog(**kw):
    kw.setdefault("ts", now())
    line = json.dumps(kw, ensure_ascii=False)
    print(line, flush=True)
    if _LOG_PATH:
        with open(_LOG_PATH, "a", encoding="utf-8") as f: f.write(line + "\n")

_shutdown = threading.Event()
def _sig(*_): _shutdown.set()
def install_signals():
    signal.signal(signal.SIGTERM, _sig); signal.signal(signal.SIGINT, _sig)
def shutting_down(): return _shutdown.is_set()
def wait(sec): _shutdown.wait(sec)

class CircuitBreaker:
    def __init__(self, name, threshold=5, cooldown=60, enabled=True):
        self.name, self.t, self.cd, self.enabled = name, threshold, cooldown, enabled
        self.fails, self.opened = 0, None
    def allow(self):
        if not self.enabled: return True
        if self.opened and time.time() - self.opened > self.cd:
            self.opened, self.fails = None, 0
        return self.opened is None
    def ok(self): self.fails = 0
    def fail(self):
        self.fails += 1
        if self.fails >= self.t: self.opened = time.time()

def backoff(i, base=0.5, cap=10.0):
    d = min(cap, base * 2 ** i); return d + d * 0.1 * random.random()
