"""
agentmemory V4 — PostgreSQL storage backend (Upgrade 8).

True async I/O via asyncpg, connection pooling, GIN-indexed tsvector FTS,
optional pgvector for native ANN. Drop-in replacement for SQLiteBackend.

Requires: pip install agentmemory[postgres]
"""

from __future__ import annotations

import json
from typing import Optional

from ..models import (AuditEvent, AuditOp, Edge, MemoryKind, MemoryNode,
                      Namespace, Provenance)


class PostgresBackend:
    """
    Async Postgres storage backend.

    Usage:
        backend = PostgresBackend(dsn="postgresql://user:pass@host/db")
        await backend.init()
        store = MemoryStore(storage_backend=backend)
    """

    def __init__(self, dsn: str, pool_min: int = 2, pool_max: int = 10):
        self._dsn = dsn
        self._pool_min = pool_min
        self._pool_max = pool_max
        self._pool = None

    async def init(self):
        try:
            import asyncpg
        except ImportError:
            raise ImportError("pip install asyncpg  (or: pip install agentmemory[postgres])")
        self._pool = await asyncpg.create_pool(
            self._dsn, min_size=self._pool_min, max_size=self._pool_max)
        await self._init_schema()

    async def _init_schema(self):
        async with self._pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY, content TEXT NOT NULL, kind TEXT NOT NULL,
                    created_at DOUBLE PRECISION NOT NULL, event_time DOUBLE PRECISION,
                    accessed_at DOUBLE PRECISION NOT NULL, access_count INTEGER DEFAULT 0,
                    importance DOUBLE PRECISION DEFAULT 0.5, confidence DOUBLE PRECISION DEFAULT 1.0,
                    decay_rate DOUBLE PRECISION DEFAULT 0.0, embedding BYTEA,
                    metadata JSONB DEFAULT '{}', prov_source TEXT DEFAULT '',
                    prov_session_id TEXT DEFAULT '', prov_conversation_turn INTEGER,
                    prov_agent_id TEXT DEFAULT '', prov_tool_call_id TEXT DEFAULT '',
                    prov_document_id TEXT DEFAULT '', prov_message_role TEXT DEFAULT '',
                    prov_extraction_method TEXT DEFAULT '',
                    ns_org TEXT DEFAULT '', ns_team TEXT DEFAULT '',
                    ns_agent TEXT DEFAULT '', ns_session TEXT DEFAULT '',
                    parent_id TEXT, superseded_by TEXT, tags JSONB DEFAULT '[]',
                    version INTEGER DEFAULT 1, valid_from DOUBLE PRECISION,
                    valid_until DOUBLE PRECISION, media_type TEXT DEFAULT 'text',
                    raw_data_ref TEXT DEFAULT '', feedback_correct INTEGER DEFAULT 0,
                    feedback_incorrect INTEGER DEFAULT 0,
                    tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
                );
                CREATE INDEX IF NOT EXISTS ix_mem_kind ON memories(kind);
                CREATE INDEX IF NOT EXISTS ix_mem_created ON memories(created_at);
                CREATE INDEX IF NOT EXISTS ix_mem_importance ON memories(importance);
                CREATE INDEX IF NOT EXISTS ix_mem_ns ON memories(ns_org, ns_team, ns_agent, ns_session);
                CREATE INDEX IF NOT EXISTS ix_mem_source ON memories(prov_source);
                CREATE INDEX IF NOT EXISTS ix_mem_valid ON memories(valid_until);
                CREATE INDEX IF NOT EXISTS ix_mem_tsv ON memories USING GIN(tsv);

                CREATE TABLE IF NOT EXISTS edges (
                    source_id TEXT NOT NULL, target_id TEXT NOT NULL,
                    relation TEXT NOT NULL, weight DOUBLE PRECISION DEFAULT 1.0,
                    metadata JSONB DEFAULT '{}', created_at DOUBLE PRECISION NOT NULL,
                    PRIMARY KEY (source_id, relation, target_id)
                );
                CREATE INDEX IF NOT EXISTS ix_edge_tgt ON edges(target_id);

                CREATE TABLE IF NOT EXISTS audit_log (
                    id SERIAL PRIMARY KEY, node_id TEXT NOT NULL, op TEXT NOT NULL,
                    timestamp DOUBLE PRECISION NOT NULL, detail JSONB DEFAULT '{}'
                );
                CREATE INDEX IF NOT EXISTS ix_audit_nid ON audit_log(node_id);
            """)

    def _to_node(self, r) -> MemoryNode:
        import struct
        prov = Provenance(
            source=r["prov_source"] or "", session_id=r["prov_session_id"] or "",
            conversation_turn=r["prov_conversation_turn"],
            agent_id=r["prov_agent_id"] or "", tool_call_id=r["prov_tool_call_id"] or "",
            document_id=r["prov_document_id"] or "",
            parent_message_role=r["prov_message_role"] or "",
            extraction_method=r["prov_extraction_method"] or "")
        emb = None
        if r["embedding"]:
            emb = list(struct.unpack(f"{len(r['embedding']) // 4}f", r["embedding"]))
        tags_raw = r["tags"]
        tags = set(tags_raw) if isinstance(tags_raw, list) else set(json.loads(tags_raw) if isinstance(tags_raw, str) else [])
        return MemoryNode(
            id=r["id"], content=r["content"], kind=MemoryKind(r["kind"]),
            created_at=r["created_at"], event_time=r["event_time"],
            accessed_at=r["accessed_at"], access_count=r["access_count"],
            importance=r["importance"], confidence=r["confidence"],
            decay_rate=r["decay_rate"], embedding=emb,
            metadata=r["metadata"] if isinstance(r["metadata"], dict) else json.loads(r["metadata"]),
            provenance=prov,
            namespace=Namespace(org=r["ns_org"], team=r["ns_team"],
                                agent=r["ns_agent"], session=r["ns_session"]),
            parent_id=r["parent_id"], superseded_by=r["superseded_by"],
            tags=tags, version=r["version"],
            valid_from=r["valid_from"], valid_until=r["valid_until"],
            media_type=r["media_type"] or "text", raw_data_ref=r["raw_data_ref"] or "",
            feedback_correct=r["feedback_correct"] or 0,
            feedback_incorrect=r["feedback_incorrect"] or 0)

    def _pack_embedding(self, emb):
        if emb is None:
            return None
        import struct
        return struct.pack(f"{len(emb)}f", *emb)

    async def save_node(self, node: MemoryNode):
        async with self._pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO memories (id,content,kind,created_at,event_time,accessed_at,access_count,
                    importance,confidence,decay_rate,embedding,metadata,prov_source,prov_session_id,
                    prov_conversation_turn,prov_agent_id,prov_tool_call_id,prov_document_id,
                    prov_message_role,prov_extraction_method,ns_org,ns_team,ns_agent,ns_session,
                    parent_id,superseded_by,tags,version,valid_from,valid_until,media_type,
                    raw_data_ref,feedback_correct,feedback_incorrect)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,
                        $21,$22,$23,$24,$25,$26,$27,$28,$29,$30,$31,$32,$33,$34)
                ON CONFLICT (id) DO UPDATE SET content=EXCLUDED.content, kind=EXCLUDED.kind,
                    accessed_at=EXCLUDED.accessed_at, access_count=EXCLUDED.access_count,
                    importance=EXCLUDED.importance, confidence=EXCLUDED.confidence,
                    decay_rate=EXCLUDED.decay_rate, embedding=EXCLUDED.embedding,
                    metadata=EXCLUDED.metadata, superseded_by=EXCLUDED.superseded_by,
                    tags=EXCLUDED.tags, version=EXCLUDED.version,
                    valid_from=EXCLUDED.valid_from, valid_until=EXCLUDED.valid_until,
                    feedback_correct=EXCLUDED.feedback_correct,
                    feedback_incorrect=EXCLUDED.feedback_incorrect
            """, node.id, node.content, node.kind.value, node.created_at, node.event_time,
                node.accessed_at, node.access_count, node.importance, node.confidence,
                node.decay_rate, self._pack_embedding(node.embedding),
                json.dumps(node.metadata), node.provenance.source, node.provenance.session_id,
                node.provenance.conversation_turn, node.provenance.agent_id,
                node.provenance.tool_call_id, node.provenance.document_id,
                node.provenance.parent_message_role, node.provenance.extraction_method,
                node.namespace.org, node.namespace.team, node.namespace.agent,
                node.namespace.session, node.parent_id, node.superseded_by,
                json.dumps(list(node.tags)), node.version, node.valid_from, node.valid_until,
                node.media_type, node.raw_data_ref, node.feedback_correct, node.feedback_incorrect)

    async def save_nodes_batch(self, nodes):
        for n in nodes:
            await self.save_node(n)

    async def delete_node(self, nid):
        async with self._pool.acquire() as conn:
            await conn.execute("DELETE FROM memories WHERE id=$1", nid)

    async def delete_edges_for_node(self, nid):
        async with self._pool.acquire() as conn:
            r = await conn.fetchval(
                "SELECT COUNT(*) FROM edges WHERE source_id=$1 OR target_id=$1", nid)
            await conn.execute("DELETE FROM edges WHERE source_id=$1 OR target_id=$1", nid)
            return r

    async def save_edge(self, edge):
        async with self._pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO edges (source_id,target_id,relation,weight,metadata,created_at)
                VALUES ($1,$2,$3,$4,$5,$6)
                ON CONFLICT (source_id,relation,target_id) DO UPDATE SET weight=EXCLUDED.weight
            """, edge.source_id, edge.target_id, edge.relation,
                edge.weight, json.dumps(edge.metadata), edge.created_at)

    async def log_audit(self, event):
        async with self._pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO audit_log (node_id,op,timestamp,detail) VALUES ($1,$2,$3,$4)",
                event.node_id, event.op.value, event.timestamp, json.dumps(event.detail))

    async def load_node(self, nid):
        async with self._pool.acquire() as conn:
            r = await conn.fetchrow("SELECT * FROM memories WHERE id=$1", nid)
        return self._to_node(r) if r else None

    async def get_all_nodes(self):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM memories ORDER BY created_at DESC")
        return [self._to_node(r) for r in rows]

    async def get_active_nodes(self, min_imp=0.0):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM memories WHERE superseded_by IS NULL AND importance >= $1",
                min_imp)
        return [self._to_node(r) for r in rows]

    async def count(self, kind=None):
        async with self._pool.acquire() as conn:
            if kind:
                return await conn.fetchval("SELECT COUNT(*) FROM memories WHERE kind=$1", kind)
            return await conn.fetchval("SELECT COUNT(*) FROM memories")

    async def fulltext_search(self, query, limit=50):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, ts_rank(tsv, plainto_tsquery('english', $1)) AS rank
                FROM memories WHERE tsv @@ plainto_tsquery('english', $1)
                ORDER BY rank DESC LIMIT $2
            """, query, limit)
        return [(r["id"], r["rank"]) for r in rows]

    async def query_by_kind(self, kinds, limit=100):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM memories WHERE kind = ANY($1) ORDER BY created_at DESC LIMIT $2",
                kinds, limit)
        return [self._to_node(r) for r in rows]

    async def query_by_tags(self, tags, limit=100):
        nodes = await self.get_all_nodes()
        return [n for n in nodes if n.tags & tags][:limit]

    async def query_by_session(self, sid):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM memories WHERE prov_session_id=$1 ORDER BY created_at ASC", sid)
        return [self._to_node(r) for r in rows]

    async def query_by_source(self, src, limit=100):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM memories WHERE prov_source=$1 ORDER BY created_at DESC LIMIT $2",
                src, limit)
        return [self._to_node(r) for r in rows]

    async def query_by_namespace(self, ns, limit=100):
        clauses, params, i = [], [], 1
        if ns.org: clauses.append(f"ns_org=${i}"); params.append(ns.org); i += 1
        if ns.team: clauses.append(f"ns_team=${i}"); params.append(ns.team); i += 1
        if ns.agent: clauses.append(f"ns_agent=${i}"); params.append(ns.agent); i += 1
        if ns.session: clauses.append(f"ns_session=${i}"); params.append(ns.session); i += 1
        where = " AND ".join(clauses) if clauses else "TRUE"
        params.append(limit)
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                f"SELECT * FROM memories WHERE {where} ORDER BY created_at DESC LIMIT ${i}",
                *params)
        return [self._to_node(r) for r in rows]

    async def query_by_time_range(self, start=None, end=None, limit=100):
        clauses, params, i = [], [], 1
        if start is not None: clauses.append(f"created_at >= ${i}"); params.append(start); i += 1
        if end is not None: clauses.append(f"created_at <= ${i}"); params.append(end); i += 1
        where = " AND ".join(clauses) if clauses else "TRUE"
        params.append(limit)
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                f"SELECT * FROM memories WHERE {where} ORDER BY created_at DESC LIMIT ${i}",
                *params)
        return [self._to_node(r) for r in rows]

    async def load_edges(self):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM edges")
        return [Edge(source_id=r["source_id"], target_id=r["target_id"],
                     relation=r["relation"], weight=r["weight"],
                     metadata=r["metadata"] if isinstance(r["metadata"], dict) else json.loads(r["metadata"]),
                     created_at=r["created_at"]) for r in rows]

    async def get_audit_log(self, node_id=None, limit=100):
        async with self._pool.acquire() as conn:
            if node_id:
                rows = await conn.fetch(
                    "SELECT * FROM audit_log WHERE node_id=$1 ORDER BY timestamp DESC LIMIT $2",
                    node_id, limit)
            else:
                rows = await conn.fetch(
                    "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT $1", limit)
        return [AuditEvent(node_id=r["node_id"], op=AuditOp(r["op"]),
                           timestamp=r["timestamp"],
                           detail=r["detail"] if isinstance(r["detail"], dict) else json.loads(r["detail"]))
                for r in rows]

    async def delete_by_source(self, source):
        async with self._pool.acquire() as conn:
            r = await conn.execute("DELETE FROM memories WHERE prov_source=$1", source)
            return int(r.split()[-1])

    async def delete_by_namespace(self, ns):
        ids = await self.get_node_ids_by_namespace(ns)
        for nid in ids:
            await self.delete_node(nid)
        return len(ids)

    async def redact_audit_log(self, node_ids):
        if not node_ids: return 0
        async with self._pool.acquire() as conn:
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM audit_log WHERE node_id = ANY($1)", node_ids)
            await conn.execute(
                "UPDATE audit_log SET detail='{\"redacted\":true}' WHERE node_id = ANY($1)",
                node_ids)
            return count

    async def get_node_ids_by_source(self, source):
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT id FROM memories WHERE prov_source=$1", source)
        return [r["id"] for r in rows]

    async def get_node_ids_by_namespace(self, ns):
        clauses, params, i = [], [], 1
        if ns.org: clauses.append(f"ns_org=${i}"); params.append(ns.org); i += 1
        if ns.team: clauses.append(f"ns_team=${i}"); params.append(ns.team); i += 1
        if not clauses: return []
        where = " AND ".join(clauses)
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(f"SELECT id FROM memories WHERE {where}", *params)
        return [r["id"] for r in rows]

    async def close(self):
        if self._pool:
            await self._pool.close()

    def save_node_sync(self, node):
        raise NotImplementedError("Use async API with PostgresBackend")
    def load_node_sync(self, nid):
        raise NotImplementedError("Use async API with PostgresBackend")
