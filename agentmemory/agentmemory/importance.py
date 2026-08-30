"""
agentmemory V3 — Importance inference with evolution.

Feature-engineered logistic model for initial scoring.
Bayesian update on recall for importance evolution.
Decay for unaccessed nodes.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from .models import MemoryKind, MemoryNode, MemoryTier

_URGENCY = frozenset(
    "critical urgent important must never always required deadline "
    "emergency breaking failure error crash bug risk blocker "
    "exposed vulnerability breach security incident production "
    "outage downtime alert warning severe fatal".split())
_ENTITY = frozenset(
    "name email phone address company org role title team "
    "ceo cto coo founder president vp director manager".split())
_PREF = frozenset(
    "prefer like dislike want need love hate favorite "
    "always never style format tone tend usually typically enjoy avoid".split())
_QUANT_RE = re.compile(r"\$[\d,.]+|[\d,.]+%|\d{4}-\d{2}-\d{2}|\b\d+[KkMmBb]\b")
_PROPER_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b")
_WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
_NEG = {"not", "never", "no", "don't", "doesn't", "won't", "can't", "shouldn't"}

_KIND_PRIOR = {
    MemoryKind.INSTRUCTION: 0.7, MemoryKind.OBSERVATION: 0.3,
    MemoryKind.SCRATCH: 0.1, MemoryKind.EVENT: 0.4,
    MemoryKind.DIALOGUE: 0.3, MemoryKind.ACTION: 0.5,
    MemoryKind.OUTCOME: 0.6, MemoryKind.FACT: 0.6,
    MemoryKind.ENTITY: 0.7, MemoryKind.PREFERENCE: 0.9,
    MemoryKind.PROCEDURE: 0.6, MemoryKind.BELIEF: 0.5}
_TIER_PRIOR = {
    MemoryTier.WORKING: 0.3, MemoryTier.EPISODIC: 0.5,
    MemoryTier.SEMANTIC: 0.7}

_W = {"kind_prior": 1.2, "tier_prior": 0.6, "urgency": 2.5,
      "entity_density": 1.0, "preference_signal": 6.0,
      "quantitative": 0.7, "specificity": 0.5, "negation": 0.5}
_BIAS = -2.2


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))


def _features(content: str, kind: MemoryKind) -> dict[str, float]:
    words = _WORD_RE.findall(content.lower())
    wc = max(len(words), 1)
    ec = sum(1 for w in words if w in _ENTITY)
    pn = len(_PROPER_RE.findall(content))
    return {
        "kind_prior": _KIND_PRIOR.get(kind, 0.5),
        "tier_prior": _TIER_PRIOR.get(kind.tier, 0.5),
        "urgency": min(1.0, sum(1 for w in words if w in _URGENCY) * 0.25),
        "entity_density": min(1.0, (ec + pn * 0.5) / wc * 5),
        "preference_signal": min(1.0, sum(1 for w in words if w in _PREF) * 0.5),
        "quantitative": min(1.0, len(_QUANT_RE.findall(content)) * 0.3),
        "specificity": min(1.0, len(words) / 30),
        "negation": min(1.0, sum(1 for w in words if w in _NEG) * 0.3),
    }


class ImportanceClassifier:
    """Predicts importance [0, 1] from content and kind."""

    def __init__(self, weights: dict[str, float] | None = None,
                 bias: float | None = None):
        self._w = weights or _W
        self._b = bias if bias is not None else _BIAS

    def predict(self, content: str, kind: MemoryKind) -> float:
        f = _features(content, kind)
        logit = self._b + sum(self._w.get(k, 0) * v for k, v in f.items())
        return round(_sigmoid(logit), 4)

    def predict_with_features(self, content: str, kind: MemoryKind
                              ) -> tuple[float, dict[str, float]]:
        f = _features(content, kind)
        logit = self._b
        contrib = {}
        for k, v in f.items():
            c = self._w.get(k, 0) * v
            contrib[k] = round(c, 4)
            logit += c
        return round(_sigmoid(logit), 4), contrib


class ImportanceEvolver:
    """
    Evolves importance scores over time using Bayesian updates.

    On recall: new_importance = importance + access_weight * (1 - importance)
    On schedule: decay unaccessed nodes toward baseline.
    """

    def __init__(self, access_weight: float = 0.02,
                 decay_rate: float = 0.001,
                 baseline: float = 0.3,
                 stale_hours: float = 168.0):
        self.access_weight = access_weight
        self.decay_rate = decay_rate
        self.baseline = baseline
        self.stale_hours = stale_hours

    def on_access(self, node: MemoryNode) -> float:
        """Bayesian update: increase importance on access."""
        old = node.importance
        node.importance = min(1.0, old + self.access_weight * (1.0 - old))
        return node.importance

    def decay_unaccessed(self, nodes: list[MemoryNode]) -> list[MemoryNode]:
        """Decay importance of nodes not accessed recently."""
        updated = []
        for node in nodes:
            if node.recency_hours > self.stale_hours:
                old = node.importance
                # Exponential decay toward baseline
                delta = (old - self.baseline) * self.decay_rate
                node.importance = max(self.baseline, old - delta)
                if abs(node.importance - old) > 0.001:
                    updated.append(node)
        return updated
