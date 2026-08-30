"""
agentmemory V4 — LLM extraction pipeline.

Upgrade 3: Semantic chunking and long-document ingestion via ingest_document().
"""

from __future__ import annotations

import re
import time
from typing import Any, Callable, Coroutine, Optional, Union

from .classification import KindClassifier
from .models import ConversationMessage, MemoryKind, MemoryNode, Provenance

ExtractorFn = Union[
    Callable[[list[ConversationMessage]], list[dict[str, Any]]],
    Callable[[list[ConversationMessage]], Coroutine[Any, Any, list[dict[str, Any]]]]
]

DEFAULT_EXTRACTION_PROMPT = """Extract discrete, memorable facts from this conversation.
For each fact, return a JSON object with:
- "content": the fact as a clear, standalone statement
- "kind": one of [fact, entity, preference, procedure, event, belief]
- "importance": float 0-1

Conversation:
{conversation}

Return ONLY a JSON array of objects."""


_PREFERENCE_PATTERNS = [
    re.compile(
        r"\bI\s+(?:prefer|like|love|hate|dislike|enjoy|avoid|always|never|"
        r"tend\s+to|usually|typically|don'?t\s+like|can'?t\s+stand|"
        r"really\s+like|really\s+hate)\b", re.I),
    re.compile(r"\bMy\s+(?:favorite|preferred|go-to|usual)\b", re.I),
    re.compile(r"\bis\s+my\s+(?:favorite|preference|go-to|preferred\s+choice)\b", re.I),
    re.compile(r"\bI'?m\s+a\s+\w+\s+person\b", re.I),
    re.compile(r"\bI\s+(?:always|never)\s+use\b", re.I),
    re.compile(r"\bI\s+(?:always|never)\s+\w+\b", re.I),
]

_ASSISTANT_PREF_CONFIRM = re.compile(
    r"(?:Got\s+it|Noted|I'?ll\s+remember|Understood|Sure),?\s+"
    r"(?:you\s+(?:prefer|like|love|hate|dislike|enjoy|avoid|always|never|tend\s+to|usually))\b",
    re.I)


def _is_preference(text: str) -> bool:
    """Return True if text matches any preference pattern."""
    return any(p.search(text) for p in _PREFERENCE_PATTERNS)


class ExtractionPipeline:
    def __init__(self, extractor_fn: Optional[ExtractorFn] = None,
                 auto_classify: bool = True,
                 hierarchical_extraction: bool = True):
        self._extractor = extractor_fn
        self._classifier = KindClassifier() if auto_classify else None
        self._hierarchical = hierarchical_extraction

    async def ingest_conversation(self, messages, session_id="",
                                   source="conversation", agent_id="",
                                   reference_date=None):
        if self._extractor:
            return await self._extract_with_llm(messages, session_id, source, agent_id)

        if self._hierarchical:
            extractor = HierarchicalExtractor(self)
            return extractor.extract_all(
                messages, session_id, source, agent_id, reference_date)

        items = self._extract_rule_based(messages, session_id, source, agent_id,
                                          reference_date=reference_date)
        # Cross-turn extraction: assistant confirmations of preferences
        cross = self._extract_cross_turn(messages, session_id, source, agent_id)
        items.extend(cross)
        return items

    async def _extract_with_llm(self, messages, session_id, source, agent_id):
        import asyncio, json
        result = self._extractor(messages)
        if asyncio.iscoroutine(result):
            extracted = await result
        else:
            extracted = result
        items = []
        for i, entry in enumerate(extracted):
            content = entry.get("content", "")
            if not content or len(content.strip()) < 5:
                continue
            kind = entry.get("kind", "observation")
            if self._classifier and kind == "observation":
                kind = self._classifier.classify(content).value
            items.append({
                "content": content.strip(), "kind": kind,
                "importance": entry.get("importance"),
                "confidence": entry.get("confidence", 0.9),
                "provenance": Provenance(source=source, session_id=session_id,
                                          agent_id=agent_id, conversation_turn=entry.get("turn", i),
                                          extraction_method="llm"),
                "tags": set(entry.get("tags", [])),
                "metadata": entry.get("metadata", {}),
            })
        return items

    def _extract_rule_based(self, messages, session_id, source, agent_id,
                            reference_date=None):
        items = []
        from .temporal import TemporalGrounder
        from datetime import datetime as _dt

        # Compute reference timestamps
        conv_end_time = None
        conv_start_time = None
        for msg in reversed(messages):
            if msg.timestamp is not None:
                conv_end_time = msg.timestamp
                break
        for msg in messages:
            if msg.timestamp is not None:
                conv_start_time = msg.timestamp
                break

        if reference_date is not None:
            rd = float(reference_date) if isinstance(reference_date, (int, float)) else reference_date.timestamp()
            if conv_end_time is None:
                conv_end_time = rd
            if conv_start_time is None:
                conv_start_time = rd - (len(messages) * 60)
        elif conv_end_time is not None and conv_start_time is None:
            conv_start_time = conv_end_time - (len(messages) * 60)

        grounder = TemporalGrounder()
        num_turns = max(len(messages), 1)

        for turn, msg in enumerate(messages):
            if msg.role == "system":
                continue
            extracts = self._extract_from_message(msg.content)

            # Compute effective timestamp for this message (Upgrade 4)
            msg_effective_ts = msg.timestamp
            if msg_effective_ts is None and conv_start_time is not None and conv_end_time is not None:
                # Linear interpolation by turn position
                frac = turn / num_turns
                msg_effective_ts = conv_start_time + frac * (conv_end_time - conv_start_time)

            for content in extracts:
                kind = self._classifier.classify(content).value if self._classifier else "observation"
                if _is_preference(content):
                    kind = "preference"
                confidence = 0.85 if _is_preference(content) else 0.7

                # Determine event_time: prefer temporal grounding, fallback to message ts
                event_time = msg_effective_ts
                if conv_end_time is not None:
                    ref_dt = _dt.fromtimestamp(msg_effective_ts or conv_end_time)
                    resolved_pairs = grounder.resolve_all(content, reference_date=ref_dt)
                    if resolved_pairs:
                        # Use the most specific resolved timestamp
                        event_time = resolved_pairs[0][1]

                items.append({
                    "content": content.strip(), "kind": kind, "confidence": confidence,
                    "provenance": Provenance(source=source, session_id=session_id,
                                              agent_id=agent_id, conversation_turn=turn,
                                              parent_message_role=msg.role,
                                              extraction_method="rule_based"),
                    "tags": set(), "metadata": {"role": msg.role},
                    "event_time": event_time,
                })
        return items

    def _extract_cross_turn(self, messages, session_id, source, agent_id):
        """Extract preferences from assistant confirmation of user preferences."""
        items = []
        for i in range(1, len(messages)):
            msg = messages[i]
            if msg.role != "assistant":
                continue
            prev = messages[i - 1]
            if prev.role != "user":
                continue
            # Check if assistant confirms a preference
            if _ASSISTANT_PREF_CONFIRM.search(msg.content):
                # Extract the preference from the assistant content
                items.append({
                    "content": msg.content.strip(),
                    "kind": "preference",
                    "confidence": 0.9,
                    "provenance": Provenance(source=source, session_id=session_id,
                                              agent_id=agent_id, conversation_turn=i,
                                              parent_message_role="assistant",
                                              extraction_method="cross_turn_confirmation"),
                    "tags": set(), "metadata": {"role": "assistant", "confirms_turn": i - 1},
                    "event_time": msg.timestamp,
                })
        return items

    def _extract_from_message(self, content: str) -> list[str]:
        sentences = re.split(r'(?<=[.!?])\s+', content.strip())
        extracted = []
        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 10 or sent.endswith("?"):
                # Preference-matched sentences get a lower bar: 3+ words
                wc = len(sent.split())
                if wc >= 3 and _is_preference(sent):
                    extracted.append(sent)
                continue
            lower = sent.lower()
            if any(lower.startswith(s) for s in [
                "hi ", "hello", "hey ", "thanks", "thank you",
                "okay", "ok ", "sure", "yes", "no ", "i see",
                "got it", "right", "well,", "so,", "hmm"]):
                # Still allow if it's a preference statement
                if _is_preference(sent):
                    extracted.append(sent)
                continue

            # Preference bypass: include regardless of other heuristics
            if _is_preference(sent):
                extracted.append(sent)
                continue

            has_proper = bool(re.search(r'\b[A-Z][a-z]+\b', sent))
            has_number = bool(re.search(r'\d', sent))
            # Base verbs for all sentences
            _base_verb_re = (
                r'\b(?:is|are|was|were|has|have|had|will|should|can|'
                r'uses?|runs?|works?|manages?|handles?|requires?|'
                r'needs?|prefers?|likes?|deployed|created|built|'
                r'started|finished|completed)\b'
            )
            # ITER-37: Extended past-tense verbs — ONLY for first-person user statements
            # (sentences starting with "I"). Restricting to first-person avoids extracting
            # assistant advice like "I got you covered" or "I received your question",
            # which would dilute context with noise and cause MS/SSP regressions.
            _is_first_person = lower.strip().startswith(("i ", "i'", "i've", "i'm", "i'd", "i'll", "i had", "i have", "i am", "i was", "i got", "i did", "i do", "i can"))
            _fp_verb_re = (
                r'\b(?:got|received|gave|took|bought|found|saw|made|been|went|came|'
                r'told|showed|brought|sent|spent|said|felt|heard|tried|joined|'
                r'moved|kept|left|saved|paid|met|added|attended|visited|earned|'
                r'signed|recovered|graduated|adopted|rescued|donated|quit|resigned|'
                r'hired|fired|promoted|won|lost|sold|fixed|repaired|assembled|'
                r'installed|traveled|flew|drove|walked|ran|jogged|hiked|'
                r'cooked|baked|brewed|prepared|watched|read|listened|played|'
                r'collected|organized|sorted|cleaned|packed|shipped|delivered|'
                r'booked|reserved|checked|confirmed|approved|accepted|rejected|'
                r'learned|studied|practiced|trained|taught|achieved|reached|'
                r'realized|noticed|decided|chose|picked|selected|ordered|'
                r'switched|changed|updated|upgraded|replaced|removed|deleted)\b'
            )
            has_verb = bool(re.search(_base_verb_re, lower))
            if not has_verb and _is_first_person:
                has_verb = bool(re.search(_fp_verb_re, lower))
            # Duration pattern for "for N months/weeks/years" — key for temporal facts
            has_duration = _is_first_person and bool(re.search(
                r'\bfor\s+(?:a\s+)?(?:few|one|two|three|four|five|six|seven|eight|nine|'
                r'ten|eleven|twelve|twenty|thirty|forty|fifty|sixty|\d+)\s+'
                r'(?:day|week|month|year|hour|minute)s?\b',
                lower))
            wc = len(sent.split())
            if wc >= 5 and (has_proper or has_number or has_verb or has_duration):
                extracted.append(sent)
            elif wc >= 8 and has_verb:
                extracted.append(sent)
        return extracted


# ---- Upgrade 2 (Prompt 2): Hierarchical conversation extraction ----

_ADJACENCY_CONFIRMS = re.compile(
    r"(?:Got\s+it|Noted|I'?ll\s+remember|So\s+you|You\s+mentioned|"
    r"I\s+understand\s+that\s+you|That\s+makes\s+sense,?\s+so\s+you)",
    re.I)

_QA_QUESTION_RE = re.compile(r"[?]\s*$")


class HierarchicalExtractor:
    """
    Three-pass extraction over a full conversation:
      Pass 1: Single-message extraction (existing rule-based)
      Pass 2: Adjacency pair extraction (assistant confirmations)
      Pass 3: Question-answer pair extraction (short answers to questions)
    """

    def __init__(self, pipeline: ExtractionPipeline):
        self._pipeline = pipeline

    def extract_all(self, messages, session_id, source, agent_id,
                    reference_date=None) -> list[dict]:
        # Pass 1: standard rule-based
        items = self._pipeline._extract_rule_based(
            messages, session_id, source, agent_id, reference_date=reference_date)

        # Pass 2: adjacency pair extraction
        items.extend(self._adjacency_pairs(messages, session_id, source, agent_id))

        # Pass 3: question-answer pair extraction
        items.extend(self._qa_pairs(messages, session_id, source, agent_id))

        # Deduplicate by content hash
        seen: set[str] = set()
        deduped: list[dict] = []
        for item in items:
            key = item["content"].strip().lower()
            if key not in seen:
                seen.add(key)
                deduped.append(item)
        return deduped

    def _adjacency_pairs(self, messages, session_id, source, agent_id) -> list[dict]:
        """Pass 2: Extract facts from assistant confirmation phrases."""
        items = []
        for i in range(1, len(messages)):
            msg = messages[i]
            if msg.role != "assistant":
                continue
            prev = messages[i - 1]
            if prev.role != "user":
                continue
            m = _ADJACENCY_CONFIRMS.search(msg.content)
            if m:
                # Extract the remainder after the confirmation phrase
                after = msg.content[m.end():].strip().lstrip(",").strip()
                if len(after) > 5:
                    items.append({
                        "content": after,
                        "kind": "preference" if _is_preference(after) else "fact",
                        "confidence": 0.90,
                        "provenance": Provenance(source=source, session_id=session_id,
                                                  agent_id=agent_id, conversation_turn=i,
                                                  parent_message_role="assistant",
                                                  extraction_method="adjacency_confirmation"),
                        "tags": set(),
                        "metadata": {"role": "assistant", "confirms_turn": i - 1},
                        "event_time": msg.timestamp,
                    })
        return items

    def _qa_pairs(self, messages, session_id, source, agent_id) -> list[dict]:
        """Pass 3: Combine assistant questions with short user answers."""
        items = []
        for i in range(1, len(messages)):
            msg = messages[i]
            if msg.role != "user":
                continue
            prev = messages[i - 1]
            if prev.role != "assistant":
                continue
            # Check if previous was a question
            if not _QA_QUESTION_RE.search(prev.content):
                continue
            # Check if this is a short answer
            answer = msg.content.strip()
            if len(answer.split()) > 8:
                continue
            # Extract the question topic and combine
            q_text = prev.content.strip()
            fact = self._combine_qa(q_text, answer)
            if fact and len(fact) > 5:
                items.append({
                    "content": fact,
                    "kind": "fact",
                    "confidence": 0.85,
                    "provenance": Provenance(source=source, session_id=session_id,
                                              agent_id=agent_id, conversation_turn=i,
                                              parent_message_role="user",
                                              extraction_method="qa_pair"),
                    "tags": set(),
                    "metadata": {"role": "user", "question_turn": i - 1},
                    "event_time": msg.timestamp,
                })
        return items

    @staticmethod
    def _combine_qa(question: str, answer: str) -> Optional[str]:
        """Combine a question and short answer into a declarative fact."""
        q_lower = question.lower().strip().rstrip("?").strip()

        # "What's your name?" / "I'm Alex Chen" → "Name is Alex Chen"
        if re.search(r"what(?:'?s| is) your name", q_lower):
            cleaned = answer.replace("I'm ", "").replace("I am ", "").strip() if answer else None
            return f"Name is {cleaned}" if cleaned else None

        # "Where do you work?" / "DataFlow Inc." → "Works at DataFlow Inc."
        if re.search(r"where do you work", q_lower):
            return f"Works at {answer}"

        # "What do you do?" / answer → answer directly (likely a role)
        if re.search(r"what do you do", q_lower):
            return answer

        # "What's your favorite X?" / answer → "Favorite X is answer"
        m = re.search(r"what(?:'?s| is) your (?:favorite|preferred) (\w+(?:\s+\w+)?)", q_lower)
        if m:
            return f"Favorite {m.group(1)} is {answer}"

        # Generic: if question asks about user, return answer as-is
        if len(answer.split()) >= 2:
            return answer

        return None


# ---- Upgrade 3: Semantic chunking for long documents ----

class DocumentChunker:
    """Splits long documents into semantically coherent chunks."""

    def __init__(self, max_chunk_chars: int = 1500,
                 overlap_chars: int = 200,
                 min_chunk_chars: int = 100):
        self.max_chunk = max_chunk_chars
        self.overlap = overlap_chars
        self.min_chunk = min_chunk_chars

    def chunk(self, content: str) -> list[str]:
        """Split content into semantic chunks."""
        paragraphs = self._split_paragraphs(content)
        chunks = []
        current = ""
        for para in paragraphs:
            if len(current) + len(para) + 1 <= self.max_chunk:
                current = (current + "\n\n" + para).strip()
            else:
                if current and len(current) >= self.min_chunk:
                    chunks.append(current)
                if len(para) > self.max_chunk:
                    sub_chunks = self._split_sentences(para)
                    chunks.extend(sub_chunks)
                    current = ""
                else:
                    overlap_text = current[-self.overlap:] if self.overlap and current else ""
                    current = (overlap_text + "\n\n" + para).strip()
        if current and len(current) >= self.min_chunk:
            chunks.append(current)
        return chunks if chunks else [content]

    def _split_paragraphs(self, text: str) -> list[str]:
        parts = re.split(r'\n\s*\n', text)
        return [p.strip() for p in parts if p.strip()]

    def _split_sentences(self, text: str) -> list[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current = ""
        for sent in sentences:
            if len(current) + len(sent) + 1 <= self.max_chunk:
                current = (current + " " + sent).strip()
            else:
                if current:
                    chunks.append(current)
                current = sent
        if current:
            chunks.append(current)
        return chunks


class DocumentIngestionPipeline:
    """Upgrade 3: Long-document ingestion with semantic chunking."""

    def __init__(self, chunker: Optional[DocumentChunker] = None,
                 classifier: Optional[KindClassifier] = None):
        self._chunker = chunker or DocumentChunker()
        self._classifier = classifier or KindClassifier()

    def process_document(self, content: str, title: str = "",
                         source: str = "document",
                         document_id: str = "") -> list[dict[str, Any]]:
        """Process a long document into memory items."""
        chunks = self._chunker.chunk(content)
        items = []

        # Create document-level entity node
        doc_content = f"Document: {title}" if title else f"Document ({len(chunks)} sections)"
        items.append({
            "content": doc_content,
            "kind": "entity",
            "importance": 0.7,
            "provenance": Provenance(source=source, document_id=document_id,
                                      extraction_method="document_ingestion"),
            "tags": {"document"},
            "metadata": {"title": title, "chunk_count": len(chunks),
                         "total_chars": len(content)},
        })

        # Process each chunk
        for i, chunk in enumerate(chunks):
            kind = self._classifier.classify(chunk).value
            items.append({
                "content": chunk,
                "kind": kind,
                "confidence": 0.8,
                "provenance": Provenance(
                    source=source, document_id=document_id,
                    extraction_method="document_chunk",
                    conversation_turn=i),
                "tags": {"document_chunk"},
                "metadata": {"title": title, "chunk_index": i,
                             "total_chunks": len(chunks)},
            })
        return items


def create_default_llm_extractor(llm_fn, prompt_template=DEFAULT_EXTRACTION_PROMPT):
    import json
    def extractor(messages):
        conv_text = "\n".join(f"[{m.role}]: {m.content}" for m in messages)
        prompt = prompt_template.format(conversation=conv_text)
        response = llm_fn(prompt)
        try:
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            return []
    return extractor
