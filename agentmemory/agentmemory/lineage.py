"""
agentmemory V4 — Memory lineage visualization API (Upgrade 11).

Returns complete causal chain: creation, consolidation, contradiction,
feedback, and downstream references for any memory node.
"""

from __future__ import annotations

from .models import AuditOp, LineageEntry, LineageReport


class LineageEngine:
    """Builds lineage reports for individual memory nodes."""

    def __init__(self, storage, graph):
        self._storage = storage
        self._graph = graph

    async def lineage(self, node_id: str) -> LineageReport:
        node = await self._storage.load_node(node_id)
        if not node:
            return LineageReport(node_id=node_id)

        report = LineageReport(
            node_id=node_id,
            current_content=node.content,
            current_kind=node.kind.value,
            current_confidence=node.confidence,
            current_importance=node.importance,
            created_from=node.provenance.source,
            creation_method=node.provenance.extraction_method,
            superseded_by=node.superseded_by or "",
            feedback_summary={
                "correct": node.feedback_correct,
                "incorrect": node.feedback_incorrect,
            },
        )

        # Build history from audit log
        events = await self._storage.get_audit_log(node_id, limit=500)
        for evt in reversed(events):  # chronological order
            desc = self._describe_event(evt)
            related = ""
            if evt.detail:
                related = (evt.detail.get("superseded_by", "") or
                           evt.detail.get("winner", "") or
                           evt.detail.get("contradicted_by", ""))
            report.history.append(LineageEntry(
                event=evt, related_node_id=related, description=desc))

        # Find contradictions
        from .graph import MemoryGraph
        for nb_id, edge in self._graph.neighbors(node_id, relation="contradicts",
                                                   direction="both"):
            report.contradictions.append(nb_id)

        # Find consolidated_from
        consolidated_from = node.metadata.get("consolidated_from", [])
        report.consolidated_from = consolidated_from

        # Find downstream references (nodes that reference this one)
        for nb_id, edge in self._graph.neighbors(node_id, direction="in"):
            if edge.relation in ("consolidated_into", "superseded_by", "mentions"):
                report.referenced_by.append(nb_id)

        return report

    @staticmethod
    def _describe_event(evt) -> str:
        op = evt.op
        if op == AuditOp.CREATE:
            return f"Created as {evt.detail.get('kind', 'unknown')} with importance {evt.detail.get('importance', '?')}"
        elif op == AuditOp.UPDATE:
            changes = evt.detail.get("changes", {})
            return f"Updated fields: {', '.join(changes.keys())}"
        elif op == AuditOp.SUPERSEDE:
            return f"Superseded by {evt.detail.get('superseded_by', '?')}"
        elif op == AuditOp.CONSOLIDATE:
            from_ids = evt.detail.get("from_ids", [])
            return f"Consolidated from {len(from_ids)} source memories"
        elif op == AuditOp.CONTRADICTION_RESOLVED:
            return f"Contradiction resolved, winner: {evt.detail.get('winner', '?')} via {evt.detail.get('method', '?')}"
        elif op == AuditOp.CONFIDENCE_DECAY:
            return f"Confidence decayed from {evt.detail.get('old', '?')} to {evt.detail.get('new', '?')}"
        elif op == AuditOp.PROMOTE:
            return f"Promoted from {evt.detail.get('from', '?')} to {evt.detail.get('to', '?')}"
        elif op == AuditOp.ROLLBACK:
            return f"Rolled back from v{evt.detail.get('from', '?')} to v{evt.detail.get('to', '?')}"
        elif op == AuditOp.DELETE:
            return f"Deleted: {evt.detail.get('reason', 'manual')}"
        elif op == AuditOp.FEEDBACK:
            return f"Feedback: correct={evt.detail.get('correct', '?')}"
        elif op == AuditOp.FACT_INVALIDATED:
            return f"Fact invalidated, valid_until set"
        elif op == AuditOp.LOW_QUALITY_CONSOLIDATION:
            return f"Low quality consolidation (score={evt.detail.get('quality_score', '?')})"
        return f"Operation: {op.value}"
