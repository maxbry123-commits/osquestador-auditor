"""
agentmemory V4 — MCP Server.

V4: Added memory_feedback, memory_lineage, memory_ingest_document tools.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys

MCP_TOOLS = [
    {"name": "memory_add", "description": "Store a new memory.",
     "input_schema": {"type": "object", "properties": {
         "content": {"type": "string"}, "kind": {"type": "string"},
         "importance": {"type": "number"}, "tags": {"type": "array", "items": {"type": "string"}},
         "source": {"type": "string"}, "event_time": {"type": "number"},
     }, "required": ["content"]}},
    {"name": "memory_recall", "description": "Retrieve relevant memories.",
     "input_schema": {"type": "object", "properties": {
         "query": {"type": "string"}, "limit": {"type": "integer", "default": 10},
         "min_importance": {"type": "number", "default": 0.0},
         "include_expired": {"type": "boolean", "default": False},
     }, "required": ["query"]}},
    {"name": "memory_context", "description": "Build formatted context string.",
     "input_schema": {"type": "object", "properties": {
         "query": {"type": "string"}, "token_budget": {"type": "integer", "default": 4000},
     }, "required": ["query"]}},
    {"name": "memory_ingest", "description": "Ingest conversation into memories.",
     "input_schema": {"type": "object", "properties": {
         "messages": {"type": "array", "items": {"type": "object", "properties": {
             "role": {"type": "string"}, "content": {"type": "string"}}, "required": ["role", "content"]}},
         "session_id": {"type": "string", "default": ""},
     }, "required": ["messages"]}},
    {"name": "memory_ingest_document", "description": "Ingest a long document with semantic chunking.",
     "input_schema": {"type": "object", "properties": {
         "content": {"type": "string"}, "title": {"type": "string", "default": ""},
         "source": {"type": "string", "default": "document"},
     }, "required": ["content"]}},
    {"name": "memory_feedback", "description": "Record whether a memory was used correctly.",
     "input_schema": {"type": "object", "properties": {
         "node_id": {"type": "string"}, "correct": {"type": "boolean"},
     }, "required": ["node_id", "correct"]}},
    {"name": "memory_lineage", "description": "Get complete causal chain for a memory.",
     "input_schema": {"type": "object", "properties": {
         "node_id": {"type": "string"},
     }, "required": ["node_id"]}},
    {"name": "memory_consolidate", "description": "Run full consolidation cycle.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "memory_stats", "description": "Get memory store statistics.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "memory_health", "description": "Get health report.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "memory_delete", "description": "Delete a memory by ID.",
     "input_schema": {"type": "object", "properties": {
         "node_id": {"type": "string"}}, "required": ["node_id"]}},
]


class MCPServer:
    def __init__(self, db_path: str = "agentmemory.db"):
        from .core import MemoryStore
        self._store = MemoryStore(db_path)

    async def handle_tool_call(self, tool_name: str, arguments: dict) -> dict:
        handlers = {
            "memory_add": self._add, "memory_recall": self._recall,
            "memory_context": self._context, "memory_ingest": self._ingest,
            "memory_ingest_document": self._ingest_doc,
            "memory_feedback": self._feedback, "memory_lineage": self._lineage,
            "memory_consolidate": self._consolidate, "memory_stats": self._stats,
            "memory_health": self._health, "memory_delete": self._delete,
        }
        handler = handlers.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}
        try:
            return await handler(arguments)
        except Exception as e:
            return {"error": str(e)}

    async def _add(self, a):
        n = await self._store.async_add(content=a["content"], kind=a.get("kind"),
                                         importance=a.get("importance"), tags=set(a.get("tags", [])),
                                         source=a.get("source"), event_time=a.get("event_time"))
        return {"id": n.id, "kind": n.kind.value, "importance": n.importance}

    async def _recall(self, a):
        results = await self._store.async_recall(
            query=a["query"], limit=a.get("limit", 10),
            min_importance=a.get("min_importance", 0.0),
            include_expired=a.get("include_expired", False))
        return {"results": [{"id": r.node.id, "content": r.node.content,
                             "score": round(r.score, 4), "kind": r.node.kind.value,
                             "valid": r.node.is_valid} for r in results]}

    async def _context(self, a):
        ctx, meta = await self._store.async_build_context(
            query=a["query"], token_budget=a.get("token_budget", 4000))
        return {"context": ctx, **meta}

    async def _ingest(self, a):
        nodes = await self._store.async_ingest_conversation(
            messages=a["messages"], session_id=a.get("session_id", ""))
        return {"memories_created": len(nodes), "ids": [n.id for n in nodes]}

    async def _ingest_doc(self, a):
        nodes = await self._store.async_ingest_document(
            content=a["content"], title=a.get("title", ""), source=a.get("source", "document"))
        return {"memories_created": len(nodes), "ids": [n.id for n in nodes]}

    async def _feedback(self, a):
        node = await self._store.async_feedback(a["node_id"], a["correct"])
        return {"confidence": node.confidence if node else None}

    async def _lineage(self, a):
        report = await self._store.async_lineage(a["node_id"])
        return report.to_dict()

    async def _consolidate(self, a):
        return await self._store.async_consolidate()

    async def _stats(self, a):
        return await self._store.async_stats()

    async def _health(self, a):
        return (await self._store.async_health_check()).to_dict()

    async def _delete(self, a):
        await self._store.async_delete(a["node_id"])
        return {"deleted": a["node_id"]}

    def get_tools(self):
        return MCP_TOOLS

    async def run_stdio(self):
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
        w_transport, w_protocol = await asyncio.get_event_loop().connect_write_pipe(
            asyncio.streams.FlowControlMixin, sys.stdout)
        writer = asyncio.StreamWriter(w_transport, w_protocol, reader, asyncio.get_event_loop())
        while True:
            try:
                line = await reader.readline()
                if not line: break
                request = json.loads(line.decode())
                method, req_id = request.get("method", ""), request.get("id")
                if method == "initialize":
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": {
                        "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                        "serverInfo": {"name": "agentmemory", "version": "4.0.0"}}}
                elif method == "tools/list":
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": self.get_tools()}}
                elif method == "tools/call":
                    p = request.get("params", {})
                    result = await self.handle_tool_call(p.get("name", ""), p.get("arguments", {}))
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": {
                        "content": [{"type": "text", "text": json.dumps(result, default=str)}]}}
                else:
                    resp = {"jsonrpc": "2.0", "id": req_id,
                            "error": {"code": -32601, "message": f"Unknown method: {method}"}}
                writer.write((json.dumps(resp) + "\n").encode())
                await writer.drain()
            except Exception as e:
                pass

    async def close(self):
        await self._store.async_close()


def main():
    parser = argparse.ArgumentParser(description="agentmemory MCP server")
    parser.add_argument("--db", type=str, default="agentmemory.db")
    args = parser.parse_args()
    server = MCPServer(args.db)
    asyncio.run(server.run_stdio())

if __name__ == "__main__":
    main()
