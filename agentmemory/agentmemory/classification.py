"""
agentmemory V3 — Auto memory kind classification.

Feature-engineered classifier that determines MemoryKind from content.
No LLM required. Uses the same approach as ImportanceClassifier.
"""

from __future__ import annotations

import re
from collections import Counter

from .models import MemoryKind

_WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
_PROPER_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b")
_QUANT_RE = re.compile(r"\$[\d,.]+|[\d,.]+%|\d{4}-\d{2}-\d{2}")

# Signal word sets for each kind
_FACT_SIGNALS = frozenset(
    "is are was were equals means defined known true false correct "
    "currently officially actually specifically precisely exactly".split())
_ENTITY_SIGNALS = frozenset(
    "name email phone address company org role title team ceo cto "
    "coo founder president director manager engineer developer".split())
_PREFERENCE_SIGNALS = frozenset(
    "prefer like dislike want need love hate favorite always never "
    "style format tone rather avoid enjoy".split())
_PROCEDURE_SIGNALS = frozenset(
    "step first then next finally install run execute deploy configure "
    "setup build create make process procedure workflow how".split())
_EVENT_SIGNALS = frozenset(
    "happened occurred completed finished started began launched "
    "deployed released updated migrated fixed resolved today yesterday".split())
_DIALOGUE_SIGNALS = frozenset(
    "said asked replied told mentioned noted suggested recommended "
    "user assistant human agent conversation chat message".split())
_ACTION_SIGNALS = frozenset(
    "did performed executed ran called triggered sent received "
    "processed handled created deleted updated modified".split())
_OUTCOME_SIGNALS = frozenset(
    "result outcome succeeded failed error success returned output "
    "produced generated caused led achieved".split())
_BELIEF_SIGNALS = frozenset(
    "think believe assume suspect probably maybe likely unlikely "
    "seems appears might could should hypothesis theory".split())
_INSTRUCTION_SIGNALS = frozenset(
    "must should shall required need ensure make sure always never "
    "do don't must not forbidden prohibited mandatory".split())
_SCRATCH_SIGNALS = frozenset(
    "todo note reminder temp temporary draft wip scratch working "
    "thinking brainstorm idea".split())


def _count_signals(words: list[str], signal_set: frozenset) -> int:
    return sum(1 for w in words if w in signal_set)


class KindClassifier:
    """
    Classifies content into MemoryKind without LLM.
    Uses weighted signal matching across word patterns,
    structure analysis, and heuristics.
    """

    def classify(self, content: str) -> MemoryKind:
        """Predict the best MemoryKind for content."""
        scores = self.score_all(content)
        return max(scores, key=scores.get)

    def score_all(self, content: str) -> dict[MemoryKind, float]:
        """Score content against all MemoryKinds."""
        words = _WORD_RE.findall(content.lower())
        wc = max(len(words), 1)

        proper_count = len(_PROPER_RE.findall(content))
        quant_count = len(_QUANT_RE.findall(content))
        has_colon = ":" in content
        has_at = "@" in content
        has_url = "http" in content.lower() or "www." in content.lower()
        is_short = wc < 8
        is_long = wc > 30

        # Base signal counts
        scores: dict[MemoryKind, float] = {}

        fact_s = _count_signals(words, _FACT_SIGNALS)
        entity_s = _count_signals(words, _ENTITY_SIGNALS)
        pref_s = _count_signals(words, _PREFERENCE_SIGNALS)
        proc_s = _count_signals(words, _PROCEDURE_SIGNALS)
        event_s = _count_signals(words, _EVENT_SIGNALS)
        dialog_s = _count_signals(words, _DIALOGUE_SIGNALS)
        action_s = _count_signals(words, _ACTION_SIGNALS)
        outcome_s = _count_signals(words, _OUTCOME_SIGNALS)
        belief_s = _count_signals(words, _BELIEF_SIGNALS)
        instr_s = _count_signals(words, _INSTRUCTION_SIGNALS)
        scratch_s = _count_signals(words, _SCRATCH_SIGNALS)

        # Weighted scoring
        scores[MemoryKind.FACT] = (
            fact_s * 2.0 + quant_count * 1.5 +
            (1.0 if has_colon else 0) +
            (0.5 if proper_count >= 1 else 0)
        )
        scores[MemoryKind.ENTITY] = (
            entity_s * 2.5 + proper_count * 2.0 +
            (2.0 if has_at or has_url else 0) +
            (1.0 if is_short else 0)
        )
        scores[MemoryKind.PREFERENCE] = pref_s * 3.0
        scores[MemoryKind.PROCEDURE] = (
            proc_s * 2.0 +
            (2.0 if is_long else 0) +
            (1.5 if any(w in words for w in ["1", "2", "3"]) else 0)
        )
        scores[MemoryKind.EVENT] = event_s * 2.5
        scores[MemoryKind.DIALOGUE] = (
            dialog_s * 2.5 +
            (2.0 if content.startswith('"') or content.startswith("'") else 0)
        )
        scores[MemoryKind.ACTION] = action_s * 2.0
        scores[MemoryKind.OUTCOME] = outcome_s * 2.5
        scores[MemoryKind.BELIEF] = belief_s * 3.0
        scores[MemoryKind.INSTRUCTION] = instr_s * 2.5
        scores[MemoryKind.SCRATCH] = scratch_s * 3.0
        scores[MemoryKind.OBSERVATION] = 1.0  # baseline fallback

        # Structural bonuses
        # "X is Y" pattern strongly suggests fact or entity
        if re.match(r"^.{3,30}\s+(?:is|are|was|were)\s+", content, re.I):
            if proper_count >= 2:
                scores[MemoryKind.ENTITY] += 3.0
            else:
                scores[MemoryKind.FACT] += 2.0

        # Imperative sentences suggest instructions
        if re.match(r"^(?:Always|Never|Do|Don't|Must|Should|Ensure)\b", content, re.I):
            scores[MemoryKind.INSTRUCTION] += 3.0

        # Past tense suggests events
        if re.search(r"\b\w+ed\b", content) and event_s >= 1:
            scores[MemoryKind.EVENT] += 1.5

        # Preference structural bonuses
        if re.match(r"^I\s+(?:prefer|like|love|hate|dislike|enjoy|avoid|always|never|tend|usually|typically)\b",
                     content, re.I):
            scores[MemoryKind.PREFERENCE] += 5.0
        if re.search(r"\bmy\s+(?:favorite|preferred|go-to)\b", content, re.I):
            scores[MemoryKind.PREFERENCE] += 4.0

        return scores

    def classify_with_confidence(self, content: str) -> tuple[MemoryKind, float]:
        """Return kind and confidence score."""
        scores = self.score_all(content)
        total = sum(scores.values())
        if total == 0:
            return MemoryKind.OBSERVATION, 0.0
        best = max(scores, key=scores.get)
        confidence = scores[best] / total
        return best, round(confidence, 3)
