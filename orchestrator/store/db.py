# -*- coding: utf-8 -*-
"""SQLite: única fuente de estado estructurado (WAL). Journal = replay."""
import sqlite3, json
from ..base.resilience import now, new_id

SCHEMA = """
CREATE TABLE IF NOT EXISTS inventory(
  hash TEXT PRIMARY KEY, proyecto TEXT, nombre TEXT, vault TEXT,
  estado TEXT, parents TEXT DEFAULT '', ts TEXT);
CREATE INDEX IF NOT EXISTS ix_inv ON inventory(proyecto, estado);
CREATE TABLE IF NOT EXISTS conflictos(
  id TEXT PRIMARY KEY, proyecto TEXT, doc_a TEXT, doc_b TEXT,
  similitud REAL, estado TEXT, ts TEXT);
CREATE INDEX IF NOT EXISTS ix_conf ON conflictos(proyecto, estado);
CREATE TABLE IF NOT EXISTS tareas(
  id TEXT PRIMARY KEY, proyecto TEXT, titulo TEXT, etiqueta TEXT,
  estado TEXT, remoto_id TEXT, ts TEXT, UNIQUE(proyecto, titulo));
CREATE TABLE IF NOT EXISTS journal(
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, wf TEXT, step TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT);
"""

class DB:
    def __init__(self, path):
        self.c = sqlite3.connect(path, check_same_thread=False)
        self.c.execute("PRAGMA journal_mode=WAL")
        self.c.executescript(SCHEMA); self.c.commit()
    def _x(self, q, a=()):
        cur = self.c.execute(q, a); self.c.commit(); return cur
    def inv_add(self, h, proyecto, nombre, vault):
        self._x("INSERT OR IGNORE INTO inventory VALUES(?,?,?,?,?,?,?)",
                (h, proyecto, nombre, vault, "ingresado", "", now()))
    def inv_get(self, h):
        r = self._x("SELECT * FROM inventory WHERE hash=?", (h,)).fetchone()
        return r and dict(zip(["hash","proyecto","nombre","vault","estado","parents","ts"], r))
    def inv_estado(self, h, estado, parents=None):
        if parents is not None:
            self._x("UPDATE inventory SET estado=?, parents=? WHERE hash=?",
                    (estado, parents, h))
        else:
            self._x("UPDATE inventory SET estado=? WHERE hash=?", (estado, h))
    def inv_por(self, proyecto=None, estado=None):
        q, a = "SELECT * FROM inventory WHERE 1=1", []
        if proyecto: q += " AND proyecto=?"; a.append(proyecto)
        if estado: q += " AND estado=?"; a.append(estado)
        return [dict(zip(["hash","proyecto","nombre","vault","estado","parents","ts"], r))
                for r in self._x(q, a)]
    def conf_add(self, proyecto, a, b, sim):
        cid = new_id()
        self._x("INSERT INTO conflictos VALUES(?,?,?,?,?,?,?)",
                (cid, proyecto, a, b, sim, "abierto", now()))
        return cid
    def conf_abiertos(self, proyecto=None):
        q, a = "SELECT * FROM conflictos WHERE estado='abierto'", []
        if proyecto: q += " AND proyecto=?"; a.append(proyecto)
        return [dict(zip(["id","proyecto","doc_a","doc_b","similitud","estado","ts"], r))
                for r in self._x(q, a)]
    def conf_resolver(self, cid, estado):
        self._x("UPDATE conflictos SET estado=? WHERE id=?", (estado, cid))
        r = self._x("SELECT * FROM conflictos WHERE id=?", (cid,)).fetchone()
        return r and dict(zip(["id","proyecto","doc_a","doc_b","similitud","estado","ts"], r))
    def tarea_add(self, proyecto, titulo, etiqueta, remoto_id=""):
        self._x("INSERT OR IGNORE INTO tareas VALUES(?,?,?,?,?,?,?)",
                (new_id(), proyecto, titulo, etiqueta, "pendiente", remoto_id, now()))
    def tareas(self, proyecto):
        return [dict(zip(["id","proyecto","titulo","etiqueta","estado","remoto_id","ts"], r))
                for r in self._x("SELECT * FROM tareas WHERE proyecto=?", (proyecto,))]
    def j(self, wf, step, payload):
        self._x("INSERT INTO journal(ts,wf,step,payload) VALUES(?,?,?,?)",
                (now(), wf, step, json.dumps(payload, ensure_ascii=False)))
    def kv_get(self, k, d=""):
        r = self._x("SELECT v FROM kv WHERE k=?", (k,)).fetchone()
        return r[0] if r else d
    def kv_set(self, k, v):
        self._x("INSERT INTO kv VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=?",
                (k, str(v), str(v)))
