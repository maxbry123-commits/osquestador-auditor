"""
agentmemory V4 — Memory health and observability API.

Upgrade 9: low_quality_consolidations count from audit log.
Upgrade 5: expired_memories count.
Upgrade 4: calibration_gap metric.
"""

from __future__ import annotations

import math
import time

from .models import AuditOp, HealthReport


class HealthMonitor:
    def __init__(self, storage, graph, ann_index=None):
        self._storage = storage
        self._graph = graph
        self._ann = ann_index
        self._quality_history: list[float] = []

    async def health_check(self) -> HealthReport:
        nodes = await self._storage.get_all_nodes()
        active = [n for n in nodes if n.superseded_by is None]
        report = HealthReport()
        report.total_memories = len(nodes)
        report.active_memories = len(active)
        report.edges = self._graph.edge_count
        report.ann_index_size = self._ann.size if self._ann else 0

        for n in active:
            report.by_tier[n.tier.value] = report.by_tier.get(n.tier.value, 0) + 1
            report.by_kind[n.kind.value] = report.by_kind.get(n.kind.value, 0) + 1

        contra_edges = self._graph.find_by_relation("contradicts")
        report.contradiction_rate = round(len(contra_edges) / max(len(active), 1), 4) if active else 0

        conf_buckets = {"0.0-0.2": 0, "0.2-0.4": 0, "0.4-0.6": 0, "0.6-0.8": 0, "0.8-1.0": 0}
        imp_buckets = {"0.0-0.2": 0, "0.2-0.4": 0, "0.4-0.6": 0, "0.6-0.8": 0, "0.8-1.0": 0}
        for n in active:
            b = "0.8-1.0" if n.confidence >= 0.8 else "0.6-0.8" if n.confidence >= 0.6 else "0.4-0.6" if n.confidence >= 0.4 else "0.2-0.4" if n.confidence >= 0.2 else "0.0-0.2"
            conf_buckets[b] += 1
            b2 = "0.8-1.0" if n.importance >= 0.8 else "0.6-0.8" if n.importance >= 0.6 else "0.4-0.6" if n.importance >= 0.4 else "0.2-0.4" if n.importance >= 0.2 else "0.0-0.2"
            imp_buckets[b2] += 1
        report.confidence_distribution = conf_buckets
        report.importance_distribution = imp_buckets
        report.importance_entropy = self._entropy([n.importance for n in active])

        now = time.time()
        stale = sum(1 for n in active if (now - n.accessed_at) > 7 * 24 * 3600)
        report.stale_memory_fraction = round(stale / max(len(active), 1), 4)

        # Upgrade 5: expired memories
        report.expired_memories = sum(
            1 for n in active if n.valid_until is not None and now > n.valid_until)

        namespaces = {n.namespace.path for n in active if n.namespace.path}
        report.namespace_count = len(namespaces)

        # Upgrade 9: low quality consolidations from audit
        audit = await self._storage.get_audit_log(limit=5000)
        report.low_quality_consolidations = sum(
            1 for e in audit if e.op == AuditOp.LOW_QUALITY_CONSOLIDATION)

        # Upgrade 4: calibration gap
        feedback_nodes = [n for n in active if n.feedback_correct + n.feedback_incorrect > 0]
        if feedback_nodes:
            gaps = []
            for n in feedback_nodes:
                total = n.feedback_correct + n.feedback_incorrect
                observed = n.feedback_correct / total
                gaps.append(abs(n.confidence - observed))
            report.calibration_gap = round(sum(gaps) / len(gaps), 4)

        report.retrieval_quality_trend = list(self._quality_history[-20:])
        return report

    def record_quality_score(self, score: float):
        self._quality_history.append(score)
        if len(self._quality_history) > 1000:
            self._quality_history = self._quality_history[-500:]

    @staticmethod
    def _entropy(values):
        if not values: return 0.0
        bins = [0] * 10
        for v in values:
            bins[min(9, int(v * 10))] += 1
        total = sum(bins)
        if total == 0: return 0.0
        return round(-sum(p * math.log2(p) for p in (c / total for c in bins if c > 0)), 4)

    async def calibrate_abstention_threshold(self) -> float:
        """
        Compute adaptive abstention threshold from store content.
        Returns 10th percentile of importance * confidence across active nodes.
        """
        nodes = await self._storage.get_all_nodes()
        active = [n for n in nodes if n.superseded_by is None]
        if not active:
            return 0.12  # default
        scores = sorted(n.importance * n.confidence for n in active)
        idx = max(0, int(len(scores) * 0.10) - 1)
        return round(scores[idx], 4)

    async def detect_drift(self):
        report = await self.health_check()
        warnings = []
        if report.contradiction_rate > 0.1:
            warnings.append(f"High contradiction rate: {report.contradiction_rate:.1%}")
        if report.stale_memory_fraction > 0.5:
            warnings.append(f"High stale fraction: {report.stale_memory_fraction:.1%}")
        if report.importance_entropy < 0.5 and report.active_memories > 50:
            warnings.append(f"Low importance entropy: {report.importance_entropy:.2f}")
        if report.low_quality_consolidations > 5:
            warnings.append(f"Low quality consolidations: {report.low_quality_consolidations}")
        if report.calibration_gap > 0.2:
            warnings.append(f"Poor confidence calibration (gap={report.calibration_gap:.2f})")
        low_conf = report.confidence_distribution.get("0.0-0.2", 0)
        if report.active_memories > 0 and low_conf / report.active_memories > 0.3:
            warnings.append(f"High low-confidence fraction")
        return {"healthy": len(warnings) == 0, "warnings": warnings, "report": report.to_dict()}
