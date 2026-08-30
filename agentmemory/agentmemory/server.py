"""
agentmemory V4 — REST server.

python -m agentmemory serve --port 8000

V4 additions: /feedback, /lineage, /ingest_document, /calibration endpoints.
"""

import argparse
from typing import Any, Optional


def create_app(db_path: str = "agentmemory.db"):
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
    except ImportError:
        raise ImportError("pip install fastapi uvicorn")

    from .core import MemoryStore
    from .models import Namespace

    app = FastAPI(title="agentmemory V4", description="Memory operating system for AI agents", version="4.0.0")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    store = MemoryStore(db_path)

    class AddRequest(BaseModel):
        content: str
        kind: Optional[str] = None
        importance: Optional[float] = None
        confidence: float = 1.0
        tags: list[str] = []
        metadata: dict[str, Any] = {}
        source: Optional[str] = None
        event_time: Optional[float] = None
        valid_from: Optional[float] = None
        valid_until: Optional[float] = None
        media_type: str = "text"

    class IngestRequest(BaseModel):
        messages: list[dict[str, Any]]
        session_id: str = ""
        source: str = "conversation"
        agent_id: str = ""

    class DocumentRequest(BaseModel):
        content: str
        title: str = ""
        source: str = "document"
        document_id: str = ""

    class RecallRequest(BaseModel):
        query: str
        limit: int = 10
        min_importance: float = 0.0
        kinds: Optional[list[str]] = None
        tags: Optional[list[str]] = None
        sources: Optional[list[str]] = None
        weights: Optional[dict[str, float]] = None
        include_expired: bool = False

    class ContextRequest(BaseModel):
        query: str
        token_budget: int = 4000
        include_confidence: bool = False
        include_explanations: bool = False

    class FeedbackRequest(BaseModel):
        node_id: str
        correct: bool

    class UpdateRequest(BaseModel):
        updates: dict[str, Any]

    class NamespaceRequest(BaseModel):
        org: str = ""
        team: str = ""
        agent: str = ""
        session: str = ""

    @app.post("/add")
    async def add_memory(req: AddRequest):
        node = await store.async_add(
            content=req.content, kind=req.kind, importance=req.importance,
            confidence=req.confidence, tags=set(req.tags), metadata=req.metadata,
            source=req.source, event_time=req.event_time,
            valid_from=req.valid_from, valid_until=req.valid_until,
            media_type=req.media_type)
        return node.to_dict()

    @app.post("/add_batch")
    async def add_batch(items: list[AddRequest]):
        dicts = [{"content": i.content, "kind": i.kind, "importance": i.importance,
                  "confidence": i.confidence, "tags": i.tags, "metadata": i.metadata} for i in items]
        nodes = await store.async_add_batch(dicts)
        return [n.to_dict() for n in nodes]

    @app.post("/ingest")
    async def ingest(req: IngestRequest):
        nodes = await store.async_ingest_conversation(
            req.messages, session_id=req.session_id, source=req.source, agent_id=req.agent_id)
        return [n.to_dict() for n in nodes]

    @app.post("/ingest_document")
    async def ingest_document(req: DocumentRequest):
        nodes = await store.async_ingest_document(
            content=req.content, title=req.title, source=req.source, document_id=req.document_id)
        return {"memories_created": len(nodes), "ids": [n.id for n in nodes]}

    @app.post("/recall")
    async def recall(req: RecallRequest):
        results = await store.async_recall(
            query=req.query, limit=req.limit, min_importance=req.min_importance,
            kinds=set(req.kinds) if req.kinds else None,
            tags=set(req.tags) if req.tags else None,
            sources=set(req.sources) if req.sources else None,
            weights=req.weights, include_expired=req.include_expired)
        return [{"node": r.node.to_dict(), "score": r.score,
                 "explanation": r.explanation, "components": r.score_components} for r in results]

    @app.post("/context")
    async def build_context(req: ContextRequest):
        ctx, meta = await store.async_build_context(
            req.query, token_budget=req.token_budget,
            include_confidence=req.include_confidence,
            include_explanations=req.include_explanations)
        return {"context": ctx, **meta}

    @app.get("/get/{node_id}")
    async def get_node(node_id: str):
        n = await store.async_get(node_id)
        if not n: raise HTTPException(404, "Node not found")
        return n.to_dict()

    @app.put("/update/{node_id}")
    async def update_node(node_id: str, req: UpdateRequest):
        n = await store.async_update(node_id, **req.updates)
        if not n: raise HTTPException(404, "Node not found")
        return n.to_dict()

    @app.delete("/delete/{node_id}")
    async def delete_node(node_id: str):
        await store.async_delete(node_id)
        return {"deleted": node_id}

    @app.post("/feedback")
    async def feedback(req: FeedbackRequest):
        node = await store.async_feedback(req.node_id, req.correct)
        if not node: raise HTTPException(404, "Node not found")
        return {"confidence": node.confidence, "feedback_correct": node.feedback_correct,
                "feedback_incorrect": node.feedback_incorrect}

    @app.get("/calibration")
    async def calibration():
        return await store.async_calibration_report()

    @app.get("/lineage/{node_id}")
    async def lineage(node_id: str):
        report = await store.async_lineage(node_id)
        return report.to_dict()

    @app.post("/consolidate")
    async def consolidate():
        return await store.async_consolidate()

    @app.get("/stats")
    async def stats():
        return await store.async_stats()

    @app.get("/health")
    async def health():
        report = await store.async_health_check()
        return report.to_dict()

    @app.get("/drift")
    async def drift():
        return await store.async_detect_drift()

    @app.get("/history")
    async def history(node_id: Optional[str] = None, limit: int = 100):
        events = await store.async_history(node_id, limit)
        return [e.to_dict() for e in events]

    @app.post("/delete_user")
    async def delete_user(user_id: str):
        receipt = await store.async_delete_user(user_id)
        return receipt.to_dict()

    @app.get("/export")
    async def export_store():
        return await store.async_export()

    @app.on_event("shutdown")
    async def shutdown():
        await store.async_close()

    return app


def main():
    parser = argparse.ArgumentParser(description="agentmemory V4 REST server")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--db", type=str, default="agentmemory.db")
    args = parser.parse_args()
    import uvicorn
    app = create_app(args.db)
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
