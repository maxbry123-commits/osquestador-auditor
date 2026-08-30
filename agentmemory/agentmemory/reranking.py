"""
agentmemory V4 — Cross-encoder reranking.

Lazy-loads cross-encoder/ms-marco-MiniLM-L-6-v2 from sentence-transformers
for high-accuracy relevance re-scoring of retrieval candidates.
"""

from __future__ import annotations

import math
from typing import Optional

from .models import RetrievalResult


def _sigmoid(x: float) -> float:
    """Normalize a raw CE logit to [0, 1] via sigmoid, clamped to avoid overflow."""
    x = max(-88.0, min(88.0, x))
    return 1.0 / (1.0 + math.exp(-x))


class CrossEncoderReranker:
    """
    Re-ranks retrieval results using a cross-encoder model.
    The model is loaded lazily on first use to avoid import-time overhead.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self._model_name = model_name
        self._model = None
        self.rerank_calls: int = 0  # FIX P2-D: counter incremented on each rerank call

    def _load_model(self):
        if self._model is not None:
            return
        from sentence_transformers import CrossEncoder
        self._model = CrossEncoder(self._model_name)

    def rerank(self, query: str, results: list[RetrievalResult]) -> list[RetrievalResult]:
        """
        Re-rank results by cross-encoder relevance score.
        Processes all candidates in a single batch call for efficiency.
        """
        if not results:
            return results

        self._load_model()
        self.rerank_calls += 1  # FIX P2-D: track total rerank invocations

        # Build pairs for batch prediction
        pairs = [(query, r.node.content) for r in results]
        scores = self._model.predict(pairs)

        # Update scores: blend bi-encoder score with sigmoid-normalized CE score.
        # This keeps scores in [0, 1] range compatible with min_relevance_score thresholds,
        # while using CE signal for ordering. Pre-rerank score is preserved in components.
        for result, ce_score in zip(results, scores):
            ce_norm = _sigmoid(float(ce_score))
            result.score_components["crossencoder"] = ce_norm
            result.score_components["pre_rerank"] = result.score
            # 70% original combined score + 30% CE — ordering dominated by CE, abstention by bi-encoder
            result.score = 0.70 * result.score + 0.30 * ce_norm

        # Sort by blended score descending
        results.sort(key=lambda r: r.score, reverse=True)
        return results
