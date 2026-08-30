"""
agentmemory V4 — Query expansion for lexical signal recovery.

Three strategies:
  1. Synonym expansion from hardcoded conversational memory dictionary
  2. Entity normalization (strip titles/honorifics)
  3. Question reformulation (question → declarative alternatives)
"""

from __future__ import annotations

import re
from typing import Optional


# ---- Strategy 1: Synonym expansion (bidirectional) ----

_SYNONYM_GROUPS: list[list[str]] = [
    ["prefer", "like", "love", "enjoy", "favor", "tend to", "always use", "go with"],
    ["job", "role", "position", "work as", "employed as", "title", "occupation"],
    ["manager", "boss", "supervisor", "reports to", "works for"],
    ["live", "reside", "located in", "based in", "from"],
    ["graduated", "studied at", "went to school", "attended", "alma mater"],
    ["born", "grew up", "hometown", "birthplace"],
    ["use", "prefer", "work with", "rely on", "tool", "technology"],
    ["deadline", "due date", "target date", "scheduled for", "due by"],
    ["budget", "cost", "price", "expense", "spending"],
    ["dislike", "hate", "avoid", "can't stand", "don't like"],
    ["name", "called", "known as", "goes by"],
    ["team", "group", "department", "division"],
    ["project", "initiative", "effort", "work on"],
    ["meeting", "standup", "sync", "call", "session"],
]

_SYNONYM_MAP: dict[str, list[str]] = {}


def _build_synonym_map():
    if _SYNONYM_MAP:
        return
    for group in _SYNONYM_GROUPS:
        for term in group:
            key = term.lower().strip()
            new_syns = [t.lower().strip() for t in group if t.lower().strip() != key]
            if key in _SYNONYM_MAP:
                # Merge with existing synonyms, dedup
                existing = set(_SYNONYM_MAP[key])
                for s in new_syns:
                    if s not in existing:
                        _SYNONYM_MAP[key].append(s)
                        existing.add(s)
            else:
                _SYNONYM_MAP[key] = new_syns


# ---- Strategy 2: Entity normalization ----

_TITLES_RE = re.compile(
    r"\b(?:Dr\.?|Mr\.?|Mrs\.?|Ms\.?|Prof\.?|Professor|"
    r"CEO|CTO|CIO|COO|CFO|VP|Director|Manager|Senior|Junior|Lead|"
    r"Sir|Dame|Rev\.?|Hon\.?)\s+",
    re.I)


def _normalize_entities(query: str) -> list[str]:
    """Strip titles/honorifics to generate normalized name variants."""
    stripped = _TITLES_RE.sub("", query).strip()
    results = []
    if stripped != query.strip():
        results.append(stripped)
    # Also extract just the last name if multi-word proper noun
    proper_nouns = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", query)
    for pn in proper_nouns:
        parts = pn.split()
        if len(parts) >= 2:
            results.append(parts[-1])  # last name only
            results.append(parts[0])   # first name only
    return results


# ---- Strategy 3: Question reformulation ----

_QUESTION_PATTERNS: list[tuple[re.Pattern, list[str]]] = [
    # "What does X prefer?" → "X prefers", "X likes", "X always"
    (re.compile(r"what\s+does\s+(\w+(?:\s+\w+)?)\s+prefer", re.I),
     ["{0} prefers", "{0} likes", "{0} always", "{0} favorite"]),
    # "What does X like?" → "X likes", "X enjoys"
    (re.compile(r"what\s+does\s+(\w+(?:\s+\w+)?)\s+like", re.I),
     ["{0} likes", "{0} enjoys", "{0} prefers"]),
    # "Who is X's manager?" → "X reports to", "X works for", "X's manager"
    (re.compile(r"who\s+is\s+(\w+(?:'s)?(?:\s+\w+)?)\s+manager", re.I),
     ["{0} reports to", "{0} works for", "{0} manager"]),
    # "Who is X's boss?" → same
    (re.compile(r"who\s+is\s+(\w+(?:'s)?(?:\s+\w+)?)\s+boss", re.I),
     ["{0} reports to", "{0} works for", "{0} boss"]),
    # "Where does X live?" → "X lives", "X resides", "X based in"
    (re.compile(r"where\s+does\s+(\w+(?:\s+\w+)?)\s+live", re.I),
     ["{0} lives", "{0} resides", "{0} based in", "{0} located"]),
    # "Where does X work?" → "X works at", "X employed"
    (re.compile(r"where\s+does\s+(\w+(?:\s+\w+)?)\s+work", re.I),
     ["{0} works at", "{0} employed", "{0} job", "{0} role"]),
    # "When did X happen?" → "X happened", "X occurred", "X was"
    (re.compile(r"when\s+did\s+(\w+(?:\s+\w+){0,5})\s+(?:happen|occur|start|begin)", re.I),
     ["{0} happened", "{0} occurred", "{0} was", "{0} started"]),
    # "How many X?" → "X count", "total X", "number of X"
    (re.compile(r"how\s+many\s+(\w+(?:\s+\w+){0,3})", re.I),
     ["{0} count", "total {0}", "number of {0}"]),
    # "What is X's role/job?" → "X works as", "X is a"
    (re.compile(r"what\s+is\s+(\w+(?:'s)?(?:\s+\w+)?)\s+(?:role|job|title|position)", re.I),
     ["{0} works as", "{0} is a", "{0} role", "{0} title"]),
    # "What language/tool does X use?" → "X uses", "X prefers"
    (re.compile(r"what\s+(?:language|tool|framework|technology)\s+does\s+(\w+(?:\s+\w+)?)\s+(?:use|prefer)", re.I),
     ["{0} uses", "{0} prefers", "{0} works with"]),
]


class QueryExpander:
    """
    Expands search queries with synonyms, entity normalization,
    and question reformulation to improve lexical recall.
    """

    def __init__(self):
        _build_synonym_map()

    def expand(self, query: str) -> list[str]:
        """
        Return a list of expanded terms and alternative phrasings.
        The original query is NOT included in the output.
        """
        terms: list[str] = []

        # Strategy 1: Synonym expansion
        words = re.findall(r"[a-z]+(?:\s+[a-z]+)?", query.lower())
        for word in words:
            synonyms = _SYNONYM_MAP.get(word, [])
            terms.extend(synonyms)
            # Also check bigrams
            for i, w in enumerate(words):
                if i + 1 < len(words):
                    bigram = f"{words[i]} {words[i+1]}"
                    syns = _SYNONYM_MAP.get(bigram, [])
                    terms.extend(syns)

        # Strategy 2: Entity normalization
        terms.extend(_normalize_entities(query))

        # Strategy 3: Question reformulation
        for pattern, templates in _QUESTION_PATTERNS:
            m = pattern.search(query)
            if m:
                entity = m.group(1)
                for tmpl in templates:
                    terms.append(tmpl.format(entity))

        # Deduplicate while preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for t in terms:
            t_lower = t.lower().strip()
            if t_lower and t_lower not in seen:
                seen.add(t_lower)
                unique.append(t)

        return unique
