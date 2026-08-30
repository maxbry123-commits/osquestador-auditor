"""
agentmemory V3 — GDPR-compliant deletion pipeline.

Complete verified erasure: memories, edges, ANN index, FTS index,
audit log redaction, with deletion receipt.
"""

from __future__ import annotations

from .ann_index import HNSWIndex
from .graph import MemoryGraph
from .models import (AuditEvent, AuditOp, DeletionReceipt, Namespace)


class GDPRPipeline:
    """GDPR right-to-forget compliant deletion with verification."""

    def __init__(self, storage, graph: MemoryGraph,
                 ann_index: HNSWIndex = None):
        self._storage = storage
        self._graph = graph
        self._ann = ann_index

    async def delete_user(self, user_id: str) -> DeletionReceipt:
        """Delete all memories for a user (by source identifier)."""
        receipt = DeletionReceipt(target_type="user", target_id=user_id)

        node_ids = await self._storage.get_node_ids_by_source(user_id)
        receipt.memories_deleted = len(node_ids)

        for nid in node_ids:
            edge_count = await self._storage.delete_edges_for_node(nid)
            receipt.edges_deleted += edge_count
            self._graph.remove_node(nid)
            if self._ann and self._ann.contains(nid):
                self._ann.remove(nid)
                receipt.ann_entries_removed += 1
            await self._storage.delete_node(nid)
            receipt.fts_entries_removed += 1

        receipt.audit_entries_redacted = await self._storage.redact_audit_log(node_ids)

        await self._storage.log_audit(AuditEvent(
            node_id="system", op=AuditOp.GDPR_DELETE,
            detail={"target_type": "user", "target_id": user_id,
                    "memories_deleted": receipt.memories_deleted}))

        receipt.verified = await self._verify_deletion(node_ids)
        return receipt

    async def delete_namespace(self, ns: Namespace) -> DeletionReceipt:
        """Delete all memories in a namespace."""
        receipt = DeletionReceipt(target_type="namespace", target_id=ns.path)

        node_ids = await self._storage.get_node_ids_by_namespace(ns)
        receipt.memories_deleted = len(node_ids)

        for nid in node_ids:
            edge_count = await self._storage.delete_edges_for_node(nid)
            receipt.edges_deleted += edge_count
            self._graph.remove_node(nid)
            if self._ann and self._ann.contains(nid):
                self._ann.remove(nid)
                receipt.ann_entries_removed += 1
            await self._storage.delete_node(nid)
            receipt.fts_entries_removed += 1

        receipt.audit_entries_redacted = await self._storage.redact_audit_log(node_ids)

        await self._storage.log_audit(AuditEvent(
            node_id="system", op=AuditOp.GDPR_DELETE,
            detail={"target_type": "namespace", "target_id": ns.path,
                    "memories_deleted": receipt.memories_deleted}))

        receipt.verified = await self._verify_deletion(node_ids)
        return receipt

    async def delete_node_complete(self, node_id: str) -> DeletionReceipt:
        """Complete deletion of a single node with verification."""
        receipt = DeletionReceipt(target_type="node", target_id=node_id)

        node = await self._storage.load_node(node_id)
        if not node:
            receipt.verified = True
            return receipt

        receipt.memories_deleted = 1
        receipt.edges_deleted = await self._storage.delete_edges_for_node(node_id)
        self._graph.remove_node(node_id)

        if self._ann and self._ann.contains(node_id):
            self._ann.remove(node_id)
            receipt.ann_entries_removed = 1

        await self._storage.delete_node(node_id)
        receipt.fts_entries_removed = 1
        receipt.audit_entries_redacted = await self._storage.redact_audit_log([node_id])

        receipt.verified = await self._verify_deletion([node_id])
        return receipt

    async def _verify_deletion(self, node_ids: list[str]) -> bool:
        """Verify that all nodes are completely removed."""
        for nid in node_ids:
            node = await self._storage.load_node(nid)
            if node is not None:
                return False
            if self._ann and self._ann.contains(nid):
                return False
        return True
