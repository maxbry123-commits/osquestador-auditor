"""
agentmemory V4 — SQLite storage backend.

V4: valid_from/valid_until columns, media_type, raw_data_ref,
feedback_correct/feedback_incorrect for calibration.
"""

from __future__ import annotations

import asyncio
import json
import sqlite3
import struct
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from ..models import (AuditEvent, AuditOp, Edge, MemoryKind, MemoryNode,
                      Namespace, Provenance)


def _pack(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)

def _unpack(blob: bytes) -> list[float]:
    return list(struct.unpack(f"{len(blob) // 4}f", blob))


class SQLiteBackend:
    def __init__(self, path: str = ":memory:"):
        self._path = path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.execute("PRAGMA busy_timeout=5000")
        self._conn.row_factory = sqlite3.Row
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._init_schema()

    def _init_schema(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                kind TEXT NOT NULL,
                created_at REAL NOT NULL,
                event_time REAL,
                accessed_at REAL NOT NULL,
                access_count INTEGER DEFAULT 0,
                importance REAL DEFAULT 0.5,
                confidence REAL DEFAULT 1.0,
                decay_rate REAL DEFAULT 0.0,
                embedding BLOB,
                metadata TEXT DEFAULT '{}',
                prov_source TEXT DEFAULT '',
                prov_session_id TEXT DEFAULT '',
                prov_conversation_turn INTEGER,
                prov_agent_id TEXT DEFAULT '',
                prov_tool_call_id TEXT DEFAULT '',
                prov_document_id TEXT DEFAULT '',
                prov_message_role TEXT DEFAULT '',
                prov_extraction_method TEXT DEFAULT '',
                ns_org TEXT DEFAULT '',
                ns_team TEXT DEFAULT '',
                ns_agent TEXT DEFAULT '',
                ns_session TEXT DEFAULT '',
                parent_id TEXT,
                superseded_by TEXT,
                tags TEXT DEFAULT '[]',
                version INTEGER DEFAULT 1,
                valid_from REAL,
                valid_until REAL,
                media_type TEXT DEFAULT 'text',
                raw_data_ref TEXT DEFAULT '',
                feedback_correct INTEGER DEFAULT 0,
                feedback_incorrect INTEGER DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS ix_kind ON memories(kind);
            CREATE INDEX IF NOT EXISTS ix_created ON memories(created_at);
            CREATE INDEX IF NOT EXISTS ix_event_time ON memories(event_time);
            CREATE INDEX IF NOT EXISTS ix_importance ON memories(importance);
            CREATE INDEX IF NOT EXISTS ix_session ON memories(prov_session_id);
            CREATE INDEX IF NOT EXISTS ix_source ON memories(prov_source);
            CREATE INDEX IF NOT EXISTS ix_agent ON memories(prov_agent_id);
            CREATE INDEX IF NOT EXISTS ix_ns ON memories(ns_org, ns_team, ns_agent, ns_session);
            CREATE INDEX IF NOT EXISTS ix_confidence ON memories(confidence);
            CREATE INDEX IF NOT EXISTS ix_valid_until ON memories(valid_until);
            CREATE INDEX IF NOT EXISTS ix_media ON memories(media_type);

            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                id UNINDEXED, content, tokenize='porter unicode61');

            CREATE TABLE IF NOT EXISTS edges (
                source_id TEXT NOT NULL, target_id TEXT NOT NULL,
                relation TEXT NOT NULL, weight REAL DEFAULT 1.0,
                metadata TEXT DEFAULT '{}', created_at REAL NOT NULL,
                PRIMARY KEY (source_id, relation, target_id)
            );
            CREATE INDEX IF NOT EXISTS ix_edge_tgt ON edges(target_id);
            CREATE INDEX IF NOT EXISTS ix_edge_rel ON edges(relation);

            CREATE TABLE IF NOT EXISTS audit_log (
                rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL, op TEXT NOT NULL,
                timestamp REAL NOT NULL, detail TEXT DEFAULT '{}'
            );
            CREATE INDEX IF NOT EXISTS ix_audit_nid ON audit_log(node_id);
        """)
        self._conn.commit()

    def _to_node(self, r: sqlite3.Row) -> MemoryNode:
        prov = Provenance(
            source=r["prov_source"] or "", session_id=r["prov_session_id"] or "",
            conversation_turn=r["prov_conversation_turn"],
            agent_id=r["prov_agent_id"] or "", tool_call_id=r["prov_tool_call_id"] or "",
            document_id=r["prov_document_id"] or "",
            parent_message_role=r["prov_message_role"] or "",
            extraction_method=r["prov_extraction_method"] or "")
        return MemoryNode(
            id=r["id"], content=r["content"], kind=MemoryKind(r["kind"]),
            created_at=r["created_at"], event_time=r["event_time"],
            accessed_at=r["accessed_at"], access_count=r["access_count"],
            importance=r["importance"], confidence=r["confidence"],
            decay_rate=r["decay_rate"],
            embedding=_unpack(r["embedding"]) if r["embedding"] else None,
            metadata=json.loads(r["metadata"]), provenance=prov,
            namespace=Namespace(org=r["ns_org"], team=r["ns_team"],
                                agent=r["ns_agent"], session=r["ns_session"]),
            parent_id=r["parent_id"], superseded_by=r["superseded_by"],
            tags=set(json.loads(r["tags"])), version=r["version"],
            valid_from=r["valid_from"], valid_until=r["valid_until"],
            media_type=r["media_type"] or "text",
            raw_data_ref=r["raw_data_ref"] or "",
            feedback_correct=r["feedback_correct"] or 0,
            feedback_incorrect=r["feedback_incorrect"] or 0)

    _INSERT_SQL = """INSERT OR REPLACE INTO memories
        (id,content,kind,created_at,event_time,accessed_at,access_count,
         importance,confidence,decay_rate,embedding,metadata,
         prov_source,prov_session_id,prov_conversation_turn,
         prov_agent_id,prov_tool_call_id,prov_document_id,
         prov_message_role,prov_extraction_method,
         ns_org,ns_team,ns_agent,ns_session,
         parent_id,superseded_by,tags,version,
         valid_from,valid_until,media_type,raw_data_ref,
         feedback_correct,feedback_incorrect)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

    def _node_tuple(self, n: MemoryNode) -> tuple:
        return (
            n.id, n.content, n.kind.value, n.created_at, n.event_time,
            n.accessed_at, n.access_count, n.importance, n.confidence, n.decay_rate,
            _pack(n.embedding) if n.embedding else None, json.dumps(n.metadata),
            n.provenance.source, n.provenance.session_id, n.provenance.conversation_turn,
            n.provenance.agent_id, n.provenance.tool_call_id, n.provenance.document_id,
            n.provenance.parent_message_role, n.provenance.extraction_method,
            n.namespace.org, n.namespace.team, n.namespace.agent, n.namespace.session,
            n.parent_id, n.superseded_by, json.dumps(list(n.tags)), n.version,
            n.valid_from, n.valid_until, n.media_type, n.raw_data_ref,
            n.feedback_correct, n.feedback_incorrect)

    async def _run(self, fn, *args):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, fn, *args)

    # ---- Sync internals ----
    def _save_node_sync(self, node: MemoryNode):
        with self._lock:
            self._conn.execute(self._INSERT_SQL, self._node_tuple(node))
            self._conn.execute(
                "INSERT OR REPLACE INTO memories_fts(id,content) VALUES(?,?)",
                (node.id, node.content))
            self._conn.commit()

    def _save_nodes_batch_sync(self, nodes: list[MemoryNode]):
        with self._lock:
            with self._conn:
                for n in nodes:
                    self._conn.execute(self._INSERT_SQL, self._node_tuple(n))
                    self._conn.execute(
                        "INSERT OR REPLACE INTO memories_fts(id,content) VALUES(?,?)",
                        (n.id, n.content))

    def _delete_node_sync(self, nid: str):
        with self._lock:
            self._conn.execute("DELETE FROM memories WHERE id=?", (nid,))
            self._conn.execute("DELETE FROM memories_fts WHERE id=?", (nid,))
            self._conn.commit()

    def _delete_edges_for_node_sync(self, nid: str) -> int:
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(*) FROM edges WHERE source_id=? OR target_id=?", (nid, nid))
            count = cur.fetchone()[0]
            self._conn.execute("DELETE FROM edges WHERE source_id=? OR target_id=?", (nid, nid))
            self._conn.commit()
            return count

    def _save_edge_sync(self, edge: Edge):
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO edges VALUES(?,?,?,?,?,?)",
                (edge.source_id, edge.target_id, edge.relation,
                 edge.weight, json.dumps(edge.metadata), edge.created_at))
            self._conn.commit()

    def _log_audit_sync(self, event: AuditEvent):
        with self._lock:
            self._conn.execute(
                "INSERT INTO audit_log(node_id,op,timestamp,detail) VALUES(?,?,?,?)",
                (event.node_id, event.op.value, event.timestamp, json.dumps(event.detail)))
            self._conn.commit()

    def _load_node_sync(self, nid: str) -> Optional[MemoryNode]:
        with self._lock:
            r = self._conn.execute("SELECT * FROM memories WHERE id=?", (nid,)).fetchone()
        return self._to_node(r) if r else None

    def _get_all_nodes_sync(self) -> list[MemoryNode]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM memories ORDER BY created_at DESC").fetchall()
        return [self._to_node(r) for r in rows]

    def _get_active_nodes_sync(self, min_imp: float = 0.0) -> list[MemoryNode]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM memories WHERE superseded_by IS NULL AND importance >= ?",
                (min_imp,)).fetchall()
        return [self._to_node(r) for r in rows]

    def _count_sync(self, kind: Optional[str] = None) -> int:
        with self._lock:
            if kind:
                return self._conn.execute(
                    "SELECT COUNT(*) FROM memories WHERE kind=?", (kind,)).fetchone()[0]
            return self._conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]

    def _fulltext_search_sync(self, query: str, limit: int = 50) -> list[tuple[str, float]]:
        tokens = query.split()
        if not tokens:
            return []
        safe = " OR ".join(f'"{t}"' for t in tokens if t.strip())
        if not safe:
            return []
        try:
            with self._lock:
                rows = self._conn.execute(
                    "SELECT id, rank FROM memories_fts WHERE content MATCH ? ORDER BY rank LIMIT ?",
                    (safe, limit)).fetchall()
            return [(r["id"], -r["rank"]) for r in rows]
        except Exception:
            return []

    def _query_by_kind_sync(self, kinds: list[str], limit: int = 100) -> list[MemoryNode]:
        ph = ",".join("?" * len(kinds))
        with self._lock:
            rows = self._conn.execute(
                f"SELECT * FROM memories WHERE kind IN ({ph}) ORDER BY created_at DESC LIMIT ?",
                (*kinds, limit)).fetchall()
        return [self._to_node(r) for r in rows]

    def _query_by_tags_sync(self, tags: set[str], limit: int = 100) -> list[MemoryNode]:
        with self._lock:
            all_rows = self._conn.execute(
                "SELECT * FROM memories ORDER BY accessed_at DESC").fetchall()
        out = []
        for r in all_rows:
            if set(json.loads(r["tags"])) & tags:
                out.append(self._to_node(r))
                if len(out) >= limit:
                    break
        return out

    def _query_by_session_sync(self, sid: str) -> list[MemoryNode]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM memories WHERE prov_session_id=? ORDER BY created_at ASC",
                (sid,)).fetchall()
        return [self._to_node(r) for r in rows]

    def _query_by_source_sync(self, src: str, limit: int = 100) -> list[MemoryNode]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM memories WHERE prov_source=? ORDER BY created_at DESC LIMIT ?",
                (src, limit)).fetchall()
        return [self._to_node(r) for r in rows]

    def _query_by_namespace_sync(self, ns: Namespace, limit: int = 100) -> list[MemoryNode]:
        clauses, params = [], []
        if ns.org: clauses.append("ns_org=?"); params.append(ns.org)
        if ns.team: clauses.append("ns_team=?"); params.append(ns.team)
        if ns.agent: clauses.append("ns_agent=?"); params.append(ns.agent)
        if ns.session: clauses.append("ns_session=?"); params.append(ns.session)
        where = " AND ".join(clauses) if clauses else "1=1"
        params.append(limit)
        with self._lock:
            rows = self._conn.execute(
                f"SELECT * FROM memories WHERE {where} ORDER BY created_at DESC LIMIT ?",
                params).fetchall()
        return [self._to_node(r) for r in rows]

    def _query_by_time_range_sync(self, start=None, end=None, limit=100) -> list[MemoryNode]:
        clauses, params = [], []
        if start is not None: clauses.append("created_at >= ?"); params.append(start)
        if end is not None: clauses.append("created_at <= ?"); params.append(end)
        where = " AND ".join(clauses) if clauses else "1=1"
        params.append(limit)
        with self._lock:
            rows = self._conn.execute(
                f"SELECT * FROM memories WHERE {where} ORDER BY created_at DESC LIMIT ?",
                params).fetchall()
        return [self._to_node(r) for r in rows]

    def _load_edges_sync(self) -> list[Edge]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM edges").fetchall()
        return [Edge(source_id=r["source_id"], target_id=r["target_id"],
                     relation=r["relation"], weight=r["weight"],
                     metadata=json.loads(r["metadata"]), created_at=r["created_at"])
                for r in rows]

    def _get_audit_log_sync(self, node_id=None, limit=100) -> list[AuditEvent]:
        with self._lock:
            if node_id:
                rows = self._conn.execute(
                    "SELECT * FROM audit_log WHERE node_id=? ORDER BY timestamp DESC LIMIT ?",
                    (node_id, limit)).fetchall()
            else:
                rows = self._conn.execute(
                    "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
        return [AuditEvent(node_id=r["node_id"], op=AuditOp(r["op"]),
                           timestamp=r["timestamp"], detail=json.loads(r["detail"]))
                for r in rows]

    # GDPR
    def _delete_by_source_sync(self, source: str) -> int:
        with self._lock:
            ids = [r[0] for r in self._conn.execute(
                "SELECT id FROM memories WHERE prov_source=?", (source,)).fetchall()]
            for nid in ids:
                self._conn.execute("DELETE FROM memories WHERE id=?", (nid,))
                self._conn.execute("DELETE FROM memories_fts WHERE id=?", (nid,))
                self._conn.execute("DELETE FROM edges WHERE source_id=? OR target_id=?", (nid, nid))
            self._conn.commit()
            return len(ids)

    def _delete_by_namespace_sync(self, ns: Namespace) -> int:
        clauses, params = [], []
        if ns.org: clauses.append("ns_org=?"); params.append(ns.org)
        if ns.team: clauses.append("ns_team=?"); params.append(ns.team)
        if ns.agent: clauses.append("ns_agent=?"); params.append(ns.agent)
        if ns.session: clauses.append("ns_session=?"); params.append(ns.session)
        if not clauses: return 0
        where = " AND ".join(clauses)
        with self._lock:
            ids = [r[0] for r in self._conn.execute(
                f"SELECT id FROM memories WHERE {where}", params).fetchall()]
            for nid in ids:
                self._conn.execute("DELETE FROM memories WHERE id=?", (nid,))
                self._conn.execute("DELETE FROM memories_fts WHERE id=?", (nid,))
                self._conn.execute("DELETE FROM edges WHERE source_id=? OR target_id=?", (nid, nid))
            self._conn.commit()
            return len(ids)

    def _redact_audit_log_sync(self, node_ids: list[str]) -> int:
        if not node_ids: return 0
        ph = ",".join("?" * len(node_ids))
        with self._lock:
            count = self._conn.execute(
                f"SELECT COUNT(*) FROM audit_log WHERE node_id IN ({ph})", node_ids).fetchone()[0]
            self._conn.execute(
                f"UPDATE audit_log SET detail='{{\"redacted\":true}}' WHERE node_id IN ({ph})",
                node_ids)
            self._conn.commit()
            return count

    def _get_node_ids_by_source_sync(self, source: str) -> list[str]:
        with self._lock:
            return [r[0] for r in self._conn.execute(
                "SELECT id FROM memories WHERE prov_source=?", (source,)).fetchall()]

    def _get_node_ids_by_namespace_sync(self, ns: Namespace) -> list[str]:
        clauses, params = [], []
        if ns.org: clauses.append("ns_org=?"); params.append(ns.org)
        if ns.team: clauses.append("ns_team=?"); params.append(ns.team)
        if ns.agent: clauses.append("ns_agent=?"); params.append(ns.agent)
        if ns.session: clauses.append("ns_session=?"); params.append(ns.session)
        if not clauses: return []
        where = " AND ".join(clauses)
        with self._lock:
            return [r[0] for r in self._conn.execute(
                f"SELECT id FROM memories WHERE {where}", params).fetchall()]

    def _close_sync(self):
        self._conn.close()

    # ---- Async API ----
    async def save_node(self, node): await self._run(self._save_node_sync, node)
    async def save_nodes_batch(self, nodes): await self._run(self._save_nodes_batch_sync, nodes)
    async def delete_node(self, nid): await self._run(self._delete_node_sync, nid)
    async def delete_edges_for_node(self, nid): return await self._run(self._delete_edges_for_node_sync, nid)
    async def save_edge(self, edge): await self._run(self._save_edge_sync, edge)
    async def log_audit(self, event): await self._run(self._log_audit_sync, event)
    async def load_node(self, nid): return await self._run(self._load_node_sync, nid)
    async def get_all_nodes(self): return await self._run(self._get_all_nodes_sync)
    async def get_active_nodes(self, min_imp=0.0): return await self._run(self._get_active_nodes_sync, min_imp)
    async def count(self, kind=None): return await self._run(self._count_sync, kind)
    async def fulltext_search(self, query, limit=50): return await self._run(self._fulltext_search_sync, query, limit)
    async def query_by_kind(self, kinds, limit=100): return await self._run(self._query_by_kind_sync, kinds, limit)
    async def query_by_tags(self, tags, limit=100): return await self._run(self._query_by_tags_sync, tags, limit)
    async def query_by_session(self, sid): return await self._run(self._query_by_session_sync, sid)
    async def query_by_source(self, src, limit=100): return await self._run(self._query_by_source_sync, src, limit)
    async def query_by_namespace(self, ns, limit=100): return await self._run(self._query_by_namespace_sync, ns, limit)
    async def query_by_time_range(self, start=None, end=None, limit=100): return await self._run(self._query_by_time_range_sync, start, end, limit)
    async def load_edges(self): return await self._run(self._load_edges_sync)
    async def get_audit_log(self, node_id=None, limit=100): return await self._run(self._get_audit_log_sync, node_id, limit)
    async def delete_by_source(self, source): return await self._run(self._delete_by_source_sync, source)
    async def delete_by_namespace(self, ns): return await self._run(self._delete_by_namespace_sync, ns)
    async def redact_audit_log(self, node_ids): return await self._run(self._redact_audit_log_sync, node_ids)
    async def get_node_ids_by_source(self, source): return await self._run(self._get_node_ids_by_source_sync, source)
    async def get_node_ids_by_namespace(self, ns): return await self._run(self._get_node_ids_by_namespace_sync, ns)
    async def close(self):
        await self._run(self._close_sync)
        self._executor.shutdown(wait=False)

    def save_node_sync(self, node): self._save_node_sync(node)
    def load_node_sync(self, nid): return self._load_node_sync(nid)
