"""
agentmemory V4 — Constitutional write validation pipeline.

Fix 3: ContradictionPreCheckRule uses pre-loaded nearby nodes
from context dict, eliminating silent skip on non-SQLite backends.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from .ann_index import HNSWIndex
from .models import MemoryKind, MemoryNode, Namespace


@dataclass
class ValidationResult:
    valid: bool = True
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    near_duplicate_id: Optional[str] = None
    contradiction_ids: list[str] = field(default_factory=list)


class ValidationRule:
    name: str = "base"
    def validate(self, node: MemoryNode, context: dict) -> ValidationResult:
        return ValidationResult()


class NearDuplicateRule(ValidationRule):
    name = "near_duplicate"
    def __init__(self, threshold: float = 0.95):
        self.threshold = threshold
    def validate(self, node: MemoryNode, context: dict) -> ValidationResult:
        result = ValidationResult()
        ann: Optional[HNSWIndex] = context.get("ann")
        if not ann or not node.embedding or ann.size == 0:
            return result
        radius = 1.0 - self.threshold
        hits = ann.query_radius(node.embedding, radius, max_results=1)
        for nid, dist in hits:
            if nid != node.id:
                result.valid = False
                result.near_duplicate_id = nid
                result.reasons.append(
                    f"Near-duplicate of {nid} (similarity={1.0-dist:.3f})")
                break
        return result


class ContradictionPreCheckRule(ValidationRule):
    """Fix 3: Uses pre-loaded nearby_nodes from context dict."""
    name = "contradiction_precheck"
    def __init__(self, confidence_threshold: float = 0.8):
        self.confidence_threshold = confidence_threshold

    def validate(self, node: MemoryNode, context: dict) -> ValidationResult:
        result = ValidationResult()
        nearby_nodes: dict = context.get("nearby_nodes", {})
        contra_fn = context.get("contradiction_detector")

        for nid, other in nearby_nodes.items():
            if other.confidence >= self.confidence_threshold:
                is_contra = (contra_fn(node, other) if contra_fn
                             else _structural_contradiction(node.content, other.content))
                if is_contra:
                    result.warnings.append(
                        f"Contradicts high-confidence memory {nid}: "
                        f"'{other.content[:60]}...'")
                    result.contradiction_ids.append(nid)
        return result


class SchemaValidationRule(ValidationRule):
    name = "schema"
    def validate(self, node: MemoryNode, context: dict) -> ValidationResult:
        result = ValidationResult()
        if not node.content or not node.content.strip():
            result.valid = False
            result.reasons.append("Content is empty")
        if len(node.content) > 100_000:
            result.valid = False
            result.reasons.append("Content exceeds 100KB limit")
        if node.importance < 0 or node.importance > 1:
            result.valid = False
            result.reasons.append(f"Importance {node.importance} outside [0,1]")
        if node.confidence < 0 or node.confidence > 1:
            result.valid = False
            result.reasons.append(f"Confidence {node.confidence} outside [0,1]")
        if node.decay_rate < 0:
            result.valid = False
            result.reasons.append(f"Decay rate {node.decay_rate} is negative")
        return result


class ImportanceFloorRule(ValidationRule):
    name = "importance_floor"
    def __init__(self, floor: float = 0.1):
        self.floor = floor
    def validate(self, node: MemoryNode, context: dict) -> ValidationResult:
        result = ValidationResult()
        if node.kind.tier.value == "semantic" and node.importance < self.floor:
            result.warnings.append(
                f"Semantic memory importance {node.importance} below floor {self.floor}")
            node.importance = self.floor
        return result


class SourceAuthorizationRule(ValidationRule):
    name = "source_authorization"
    def __init__(self, allowed_sources: Optional[set[str]] = None,
                 blocked_sources: Optional[set[str]] = None):
        self.allowed = allowed_sources
        self.blocked = blocked_sources or set()
    def validate(self, node: MemoryNode, context: dict) -> ValidationResult:
        result = ValidationResult()
        src = node.provenance.source
        if self.blocked and src in self.blocked:
            result.valid = False
            result.reasons.append(f"Source '{src}' is blocked")
        if self.allowed is not None and src not in self.allowed:
            result.valid = False
            result.reasons.append(f"Source '{src}' is not in allowed set")
        return result


class ContentLengthRule(ValidationRule):
    name = "content_length"
    def __init__(self, min_length: int = 3, max_length: int = 50_000):
        self.min_length = min_length
        self.max_length = max_length
    def validate(self, node: MemoryNode, context: dict) -> ValidationResult:
        result = ValidationResult()
        cl = len(node.content.strip())
        if cl < self.min_length:
            result.valid = False
            result.reasons.append(f"Content too short ({cl} chars)")
        if cl > self.max_length:
            result.valid = False
            result.reasons.append(f"Content too long ({cl} chars)")
        return result


class WriteValidator:
    def __init__(self, rules: Optional[list[ValidationRule]] = None):
        self._rules: list[ValidationRule] = rules or self._default_rules()

    @staticmethod
    def _default_rules() -> list[ValidationRule]:
        return [
            SchemaValidationRule(),
            ContentLengthRule(),
            ImportanceFloorRule(),
            NearDuplicateRule(threshold=0.98),
            ContradictionPreCheckRule(),
        ]

    def add_rule(self, rule: ValidationRule):
        self._rules.append(rule)

    def remove_rule(self, name: str):
        self._rules = [r for r in self._rules if r.name != name]

    def validate(self, node: MemoryNode, context: dict) -> ValidationResult:
        combined = ValidationResult()
        for rule in self._rules:
            result = rule.validate(node, context)
            if not result.valid:
                combined.valid = False
                combined.reasons.extend(result.reasons)
            combined.warnings.extend(result.warnings)
            if result.near_duplicate_id:
                combined.near_duplicate_id = result.near_duplicate_id
            combined.contradiction_ids.extend(result.contradiction_ids)
        return combined


def _structural_contradiction(ta: str, tb: str) -> bool:
    if ta == tb:
        return False
    al, bl = ta.lower().strip(), tb.lower().strip()
    wa = re.findall(r"[a-z0-9']+", al)
    wb = re.findall(r"[a-z0-9']+", bl)
    if not wa or not wb:
        return False
    pfx = 0
    for x, y in zip(wa, wb):
        if x == y:
            pfx += 1
        else:
            break
    if pfx >= 3 and len(wa) > pfx and len(wb) > pfx:
        if " ".join(wa[pfx:]) != " ".join(wb[pfx:]):
            return True
    pat = re.compile(r"^(.{5,}?)\s+(?:is|are|was|were|=)\s+(.+)$", re.I)
    ma, mb = pat.match(ta.strip()), pat.match(tb.strip())
    if ma and mb:
        sa = set(re.findall(r"[a-z0-9]+", ma.group(1).lower()))
        sb = set(re.findall(r"[a-z0-9]+", mb.group(1).lower()))
        if sa and sb:
            overlap = len(sa & sb) / max(len(sa), len(sb))
            if overlap >= 0.6:
                if ma.group(2).lower().strip() != mb.group(2).lower().strip():
                    return True
    sa, sb = set(wa), set(wb)
    if sa and sb:
        jaccard = len(sa & sb) / len(sa | sb)
        if jaccard >= 0.5 and al != bl:
            return True
    return False
