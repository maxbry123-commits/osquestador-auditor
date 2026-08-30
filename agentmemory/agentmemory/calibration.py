"""
agentmemory V4 — Confidence calibration (Upgrade 4).

Bayesian feedback loop: mem.feedback(node_id, correct=True/False)
updates confidence using observed accuracy. Reports calibration curves.
"""

from __future__ import annotations

import math
from typing import Optional

from .models import AuditEvent, AuditOp, EventType, MemoryEvent, MemoryNode


class CalibrationEngine:
    """Tracks and corrects confidence calibration from feedback."""

    def __init__(self, storage, event_bus=None):
        self._storage = storage
        self._event_bus = event_bus

    async def record_feedback(self, node_id: str, correct: bool) -> Optional[MemoryNode]:
        """Record whether a memory was used correctly by the agent."""
        node = await self._storage.load_node(node_id)
        if not node:
            return None

        if correct:
            node.feedback_correct += 1
        else:
            node.feedback_incorrect += 1

        total = node.feedback_correct + node.feedback_incorrect
        observed = node.feedback_correct / total

        # Bayesian update: weight increases naturally with observation count.
        # At total=1, weight=0.1; at total=5, weight=0.5; at total=10+, weight=1.0.
        weight = min(1.0, total / 10.0)
        updated_confidence = node.confidence * (1 - weight) + observed * weight
        node.confidence = round(max(0.05, min(1.0, updated_confidence)), 4)

        node.version += 1
        await self._storage.save_node(node)
        await self._storage.log_audit(AuditEvent(
            node_id=node_id, op=AuditOp.FEEDBACK,
            detail={"correct": correct,
                    "feedback_correct": node.feedback_correct,
                    "feedback_incorrect": node.feedback_incorrect,
                    "new_confidence": node.confidence}))

        if self._event_bus:
            await self._event_bus.emit(MemoryEvent(
                event_type=EventType.FEEDBACK_RECEIVED,
                node_id=node_id,
                data={"correct": correct, "confidence": node.confidence}))

        return node

    async def calibration_report(self) -> dict:
        """Generate calibration report across all memories with feedback."""
        nodes = await self._storage.get_all_nodes()
        buckets: dict[str, dict] = {}
        for label in ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]:
            buckets[label] = {"count": 0, "total_feedback": 0,
                              "correct": 0, "predicted_conf": 0.0}

        nodes_with_feedback = [n for n in nodes
                               if n.feedback_correct + n.feedback_incorrect > 0]

        for n in nodes_with_feedback:
            total = n.feedback_correct + n.feedback_incorrect
            observed = n.feedback_correct / total if total > 0 else 0
            if n.confidence < 0.2:
                b = "0.0-0.2"
            elif n.confidence < 0.4:
                b = "0.2-0.4"
            elif n.confidence < 0.6:
                b = "0.4-0.6"
            elif n.confidence < 0.8:
                b = "0.6-0.8"
            else:
                b = "0.8-1.0"
            buckets[b]["count"] += 1
            buckets[b]["total_feedback"] += total
            buckets[b]["correct"] += n.feedback_correct
            buckets[b]["predicted_conf"] += n.confidence

        calibration_gap = 0.0
        calibrated_buckets = 0
        result_buckets = {}
        for label, data in buckets.items():
            if data["count"] == 0:
                result_buckets[label] = {"count": 0}
                continue
            avg_predicted = data["predicted_conf"] / data["count"]
            actual_accuracy = data["correct"] / data["total_feedback"] if data["total_feedback"] > 0 else 0
            gap = abs(avg_predicted - actual_accuracy)
            calibration_gap += gap
            calibrated_buckets += 1
            result_buckets[label] = {
                "count": data["count"],
                "avg_predicted_confidence": round(avg_predicted, 3),
                "actual_accuracy": round(actual_accuracy, 3),
                "calibration_gap": round(gap, 3),
            }

        avg_gap = calibration_gap / calibrated_buckets if calibrated_buckets > 0 else 0

        return {
            "total_memories_with_feedback": len(nodes_with_feedback),
            "total_feedback_events": sum(
                n.feedback_correct + n.feedback_incorrect for n in nodes_with_feedback),
            "average_calibration_gap": round(avg_gap, 4),
            "buckets": result_buckets,
            "well_calibrated": avg_gap < 0.15,
        }
