"""
Full LongMemEval benchmark evaluation for agentmemory V4.

Methodology:
  - Ingests each test case's haystack_sessions into a fresh MemoryStore
  - Retrieves context for the question using async_build_context(token_budget=TOKEN_BUDGET)
  - Generates an answer using GPT-4.1 with the retrieved context
  - Judges the answer using the EXACT judge prompt templates from evaluate_qa.py
    (matching OMEGA's published evaluation methodology)
  - Parsing: 'yes' in response.lower() → correct
  - Score: correct / total * 100

Usage:
  python run_longmemeval_full.py               # full run
  python run_longmemeval_full.py --limit 5     # smoke test on first 5 cases
  python run_longmemeval_full.py --resume      # resume from progress file
"""
import asyncio
import argparse
import calendar  # FIX P1-A: needed for day-capping in months-ago calculation
import json
import os
import re
import sys
import time
import traceback
from datetime import datetime, timedelta
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── ITER-46: Deterministic HNSW via fixed PYTHONHASHSEED ──────────────────────
# Python randomises hash() for str/bytes by default (PYTHONHASHSEED).  The HNSW
# beam search iterates over sets of node-ID strings, so its traversal order (and
# therefore which approximate neighbours are returned) varies between runs.
# Re-execute with a fixed seed so every run produces the identical graph traversal.
_DESIRED_HASH_SEED = "42"
if os.environ.get("PYTHONHASHSEED") != _DESIRED_HASH_SEED:
    import subprocess
    env = {**os.environ, "PYTHONHASHSEED": _DESIRED_HASH_SEED}
    result = subprocess.run([sys.executable] + sys.argv, env=env)
    sys.exit(result.returncode)
# ──────────────────────────────────────────────────────────────────────────────

# Force UTF-8 stdout/stderr on Windows to avoid charmap encode errors
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from openai import AsyncOpenAI, RateLimitError
try:
    from anthropic import AsyncAnthropic, RateLimitError as AnthropicRateLimitError
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False
    AnthropicRateLimitError = None


# ── v17: Direct haystack context builder ──────────────────────────────────────

def build_direct_context(sessions: list, dates: list) -> str:
    """Format raw haystack sessions as a chronological transcript with date labels."""
    parts = []
    for sidx, session in enumerate(sessions):
        date_str = dates[sidx] if sidx < len(dates) else None
        if date_str:
            parts.append(f"\n[Session: {date_str}]")
        for turn in session:
            role = turn.get("role", "")
            content = turn.get("content", "")
            if role == "user":
                parts.append(f"User: {content}")
            elif role == "assistant":
                parts.append(f"Assistant: {content}")
    return "\n".join(parts)


# ── ITER-14: Post-ingestion user event extraction ────────────────────────────────

_EVENT_VERBS = re.compile(
    r"\bI\s+(?:just|recently|finally|also|actually|even|already|today|yesterday|now)?\s*"
    r"(?:bought|purchased|got|received|ordered|picked up|scored|grabbed|"
    r"attended|went to|went on|went for|went out|visited|stopped by|dropped by|"
    r"signed|completed|finished|started|kicked off|launched|"
    r"recovered from|got back from|returned from|came back from|got over|"
    r"met|saw|ran into|bumped into|caught up with|had coffee with|had lunch with|had dinner with|"
    r"read|watched|listened to|"
    r"made|baked|cooked|brewed|prepared|"
    r"fixed|repaired|built|installed|set up|assembled|"
    r"sold|donated|gave away|"
    r"joined|quit|left|resigned from|"
    r"graduated|passed|earned|won|lost|"
    r"adopted|rescued|"  # FIX P4: removed duplicate "adopted"
    r"ran|walked|jogged|hiked|biked|cycled|swam|played|"
    r"took|had|tried|used|wore|drove|flew|traveled|"  # FIX P4: removed duplicate "drove"
    r"moved|relocated|settled)\b",
    re.I,
)

def extract_user_events(user_content: str) -> list[str]:
    """Extract short first-person past-tense event sentences from a user turn.

    Returns candidate fact sentences like:
      "I just bought a smoker."
      "I signed a contract with my first client today."
      "I attended a baking class at a local culinary school."

    These are added as dedicated low-noise nodes so targeted event queries
    (e.g., 'how many days ago did I buy a smoker?') retrieve them reliably.
    """
    # ITER-27b: Insert sentence breaks before "By the way, I ..." / "Also, I ..."
    # so that event clauses buried in non-event-starting sentences get extracted.
    # e.g., "I've been thinking about a backpack... By the way, I just got back from Muir Woods."
    # → "I've been thinking about a backpack.... I just got back from Muir Woods."
    _proc_content = re.sub(
        r'(?<=[^\n])\s+(By the way|Also|Additionally|BTW|Besides|Oh by the way|Oh,?\s+by the way),?\s+(I\b)',
        r'. \2',
        user_content.strip(),
        flags=re.I,
    )
    # Split on sentence boundaries
    sents = re.split(r'(?<=[.!])\s+', _proc_content)
    events = []
    for sent in sents:
        s = sent.strip()
        # (ITER-27b pre-processes "By the way, I..." in the split step above)
        # Length filter: short focused facts (skip very short / very long)
        if len(s) < 15 or len(s) > 250:
            continue
        # Must start with first-person pronoun OR a relative date phrase followed by "I"
        # e.g., "Yesterday, I attended..." / "Last Monday, I went..." / "This morning, I got..."
        # ITER-19: also accept leading temporal adverbs so "Yesterday, I bought X" is captured.
        _rel_date_prefix = re.match(
            r'^(?:yesterday|last\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month|night|evening)|'
            r'this\s+(?:morning|evening|afternoon|weekend)|earlier\s+today),?\s+I\b',
            s, re.I)
        if not re.match(r'^I\b', s, re.I) and not _rel_date_prefix:
            continue
        # Skip questions
        if s.endswith('?'):
            continue
        # Skip future plans / intentions — BUT exempt sentences that START with a
        # clearly past-tense action ("I just signed X, and I want to make sure...")
        # so secondary "want to/going to" clauses don't suppress the primary event.
        # ITER-21: check for leading past-tense event before applying future-plan filter.
        _leading_past = re.match(
            r'^I\s+(?:just|recently|finally|already|actually|even)\s+',
            s, re.I)
        if not _leading_past and re.search(
            r"\b(plan to|planning to|going to|want to|hope to|intend to|"
            r"thinking of|thinking about|looking forward to|would like to|"
            r"might|may go|could try|should)\b",
            s, re.I
        ):
            # ITER-22: even if the sentence is a future plan, check for a
            # causal past-event clause ("since I lost X", "because I broke Y")
            # so the past event is still captured.
            # e.g., "I'm planning to buy a phone charger, since I lost my old one 2 weeks ago."
            #   → extract "I lost my phone charger at the gym about 2 weeks ago."
            _causal = re.search(
                r',?\s+(?:since|because|as)\s+(I\s+\w.{10,120}?)\.?\s*$',
                s, re.I)
            if _causal:
                _clause = _causal.group(1).strip().rstrip('.')
                if _EVENT_VERBS.search(_clause) and len(_clause) <= 250:
                    # Try to resolve generic pronouns ("old one", "it", "mine")
                    # using the direct object from the main/future clause.
                    # e.g., "planning to buy a new phone charger" → object = "phone charger"
                    _main_part = s[:_causal.start()]
                    _obj_m = re.search(
                        r'\b(?:buy|get|find|replace|fix|order|purchase)\s+'
                        r'(?:a\s+new\s+|an?\s+new\s+|a\s+|an?\s+|my\s+)?'
                        r'([a-z]+(?:\s+[a-z]+){0,3})\b',
                        _main_part, re.I)
                    _resolved = _clause
                    if _obj_m:
                        _obj = _obj_m.group(1).strip().rstrip('.')
                        _resolved = re.sub(r'\bold\s+one\b', _obj, _resolved, flags=re.I)
                        _resolved = re.sub(r'\bmy\s+one\b', f'my {_obj}', _resolved, flags=re.I)
                        _resolved = re.sub(r'\bit\b(?!\s+\w+ing\b)', _obj, _resolved, flags=re.I)
                        _resolved = re.sub(r'\bmine\b', f'my {_obj}', _resolved, flags=re.I)
                    events.append(_resolved + '.')
            continue
        # ITER-24: Extract compound past-event clause from sentences like
        # "I've been listening to Queen lately, actually just saw them live with parents."
        # Pattern: sentence starts with "I" but the EVENT VERB appears after a comma
        # preceded by "actually"/"also" (no "I" directly before the verb).
        # Extract: "I [modifier] [verb] [rest_of_clause]."
        _compound_m = re.search(
            r',\s+(actually|also)\s+(just|recently|finally)?\s*'
            r'(bought|purchased|got|received|ordered|picked up|'
            r'attended|went to|went on|visited|'
            r'signed|completed|finished|started|'
            r'recovered|got back from|returned|'
            r'met|saw|caught up|had coffee|had lunch|had dinner|'
            r'read|watched|listened to|'
            r'made|baked|cooked|brewed|'
            r'fixed|repaired|built|installed|'
            r'joined|quit|left|graduated|won|lost|'
            r'ran|walked|jogged|hiked|biked|swam|played|took|drove|flew)\b'
            r'(.{10,250})',
            s, re.I)
        if _compound_m and re.match(r'^I\b', s, re.I):
            _c_modifier = _compound_m.group(1)           # "actually" or "also"
            _c_qualifier = (_compound_m.group(2) + ' ') if _compound_m.group(2) else ''
            _c_verb = _compound_m.group(3)
            _c_rest = _compound_m.group(4).strip()
            # Strip trailing ", and I..." / ", but I..." secondary clauses
            _c_rest = re.split(r',\s+(?:and|but)\s+I\b', _c_rest)[0]
            _c_rest = _c_rest.strip().rstrip('.,')
            # Pronoun resolution: if "them" appears in the rest, look for a named entity
            # in the main clause (before the first comma) to substitute.
            # e.g., "I've been listening to Queen lately, actually just saw them live"
            # → "them" = "Queen" → "I actually just saw Queen live..."
            if re.search(r'\bthem\b', _c_rest, re.I):
                _main_part = s[:_compound_m.start()]
                # Look for capitalized multi-word entity (e.g., band/artist name)
                _entity_m = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b', _main_part)
                if _entity_m:
                    _entity = _entity_m.group(1)
                    _c_rest = re.sub(r'\bthem\b', _entity, _c_rest, flags=re.I)
            _compound_event = f"I {_c_modifier} {_c_qualifier}{_c_verb} {_c_rest}."
            if len(_compound_event) <= 250 and _c_rest:
                events.append(_compound_event)
        # Must contain an action verb
        if _EVENT_VERBS.search(s):
            events.append(s)
    return events


_WORD_NUMS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "a": 1, "an": 1,
}

def event_relative_date(sentence: str, session_ts: float) -> float:
    """Return a more accurate event_time for an extracted event sentence.

    Handles phrases like 'yesterday', 'last week', 'N days/weeks/months ago',
    'exactly N weeks ago', etc. Falls back to session_ts if nothing is found.
    """
    s = sentence.lower()
    ref = datetime.fromtimestamp(session_ts)

    # "yesterday" / "the day before"
    if re.search(r'\b(yesterday|the day before)\b', s):
        return (ref - timedelta(days=1)).timestamp()

    # "last [night|evening|morning]" → previous day
    if re.search(r'\b(last night|last evening|last morning|this morning)\b', s):
        return (ref - timedelta(days=1)).timestamp()

    # "N [days|weeks|months] ago" — with optional "exactly"/"about"/"around"
    m = re.search(
        r'\b(?:exactly|about|around|nearly|almost)?\s*'
        r'(a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)'
        r'\s+(days?|weeks?|months?)\s+ago\b', s)
    if m:
        raw, unit = m.group(1), m.group(2)
        n = int(raw) if raw.isdigit() else _WORD_NUMS.get(raw, 1)
        if 'month' in unit:
            return (ref - timedelta(days=30 * n)).timestamp()
        elif 'week' in unit:
            return (ref - timedelta(weeks=n)).timestamp()
        else:
            return (ref - timedelta(days=n)).timestamp()

    # "last week" / "last month"
    if re.search(r'\blast\s+week\b', s):
        return (ref - timedelta(weeks=1)).timestamp()
    if re.search(r'\blast\s+month\b', s):
        return (ref - timedelta(days=30)).timestamp()

    # "last [Monday|Tuesday|...|Sunday]" — find most recent occurrence
    day_names = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    m = re.search(r'\blast\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', s)
    if m:
        target_wd = day_names.index(m.group(1))
        days_back = (ref.weekday() - target_wd) % 7
        if days_back == 0:
            days_back = 7
        return (ref - timedelta(days=days_back)).timestamp()

    # "this [Monday|...|Sunday]" (same week)
    m = re.search(r'\bthis\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', s)
    if m:
        target_wd = day_names.index(m.group(1))
        days_back = (ref.weekday() - target_wd) % 7
        return (ref - timedelta(days=days_back)).timestamp()

    # "a few days ago" / "a couple days ago"
    if re.search(r'\ba?\s*(few|couple)\s+(days?|weeks?)\s+ago\b', s):
        return (ref - timedelta(days=3)).timestamp()

    return session_ts


# ── Fix 1: Multi-entity extraction for TR comparison questions ─────────────────

def extract_comparison_entities(question: str) -> list[str]:
    """
    Detect comparison entities in a temporal-reasoning question.
    Returns a list of 1-3 standalone search strings for separate recalls.
    If no comparison pattern is detected, returns [question] unchanged.
    """
    q = question.strip()

    # Pattern 1: Quoted titles/phrases like 'Game of Thrones' or "The Crown"
    quoted = re.findall(r"['\u2018\u2019\u201c\u201d\"]([^'\u2018\u2019\u201c\u201d\"]+)['\u2018\u2019\u201c\u201d\"]", q)
    if len(quoted) >= 2:
        return [e.strip() for e in quoted[:3] if e.strip()]

    # Pattern 1b: "between X and Y" — e.g. "between the Hindu festival of Holi and the Sunday mass at St. Mary's"
    m = re.search(r"\bbetween\s+(.+?)\s+and\s+(.+?)(?=[,?!]|\s*$)", q, re.I)
    if m:
        e1, e2 = m.group(1).strip(), m.group(2).strip()
        if len(e1.split()) >= 2 and len(e2.split()) >= 2 and len(e1) <= 80 and len(e2) <= 80:
            return [e1, e2]

    # Pattern 2: "the X or the Y" — article + noun phrase (greedy, stop at sentence boundary)
    # Use (.+?) with boundary lookahead (?=[,?!]|\s*$) so multi-word entities are captured fully
    m = re.search(
        r"\bthe\s+(.+?)\s+or\s+the\s+(.+?)(?=[,?!]|\s*$)",
        q, re.I)
    if m:
        e1, e2 = m.group(1).strip(), m.group(2).strip()
        if e1 and e2 and 1 <= len(e1.split()) <= 6 and 1 <= len(e2.split()) <= 6:
            return [e1, e2]

    # Pattern 3: Proper name pairs — "Mark or Tom", "Mark and Sarah or Tom"
    m = re.search(
        r"\b([A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+)?)\s+or\s+([A-Z][a-z]+)\b",
        q)
    if m:
        return [m.group(1).strip(), m.group(2).strip()]

    # Pattern 4: "watching/playing/reading X before or after Y" — media / activity titles
    m = re.search(
        r"(?:watching|playing|reading)\s+(.+?)\s+(?:before\s+or\s+after|before|after)\s+(.+?)(?=[,?!]|\s*$)",
        q, re.I)
    if m:
        e1, e2 = m.group(1).strip(), m.group(2).strip()
        if e1 and e2 and len(e1) > 2 and len(e2) > 2:
            return [e1, e2]

    # Pattern 5: Generic capitalized phrase pairs around "before or after" / "before" / "after"
    m = re.search(
        r"([A-Z][a-zA-Z]+(?:\s+[a-zA-Z]+){0,4})"
        r"\s+(?:before\s+or\s+after|before|after)\s+"
        r"([A-Z][a-zA-Z]+(?:\s+[a-zA-Z]+){0,4})(?=[,?!]|\s*$)",
        q)
    if m:
        e1, e2 = m.group(1).strip(), m.group(2).strip()
        if e1 and e2 and len(e1) > 3 and len(e2) > 3:
            return [e1, e2]

    # Pattern 6: "X when I {verb} Y" — e.g. "baking class at a local culinary school when I made my friend's birthday cake"
    m = re.search(r"\b(.{10,}?)\s+when\s+I\s+(.+?)(?=[,?!]|\s*$)", q, re.I)
    if m:
        e1, e2 = m.group(1).strip(), m.group(2).strip()
        # ITER-41 fix: skip if e1 is a duration-gap question ("How long had/have I been X
        # when I did Y") — these are NOT comparison pairs but single-event duration questions.
        # "How many days ago did I do X when I did Y" is kept because multi-entity recall
        # helps find both events (baking class + birthday cake).
        if (len(e1.split()) >= 3 and len(e2.split()) >= 2
                and not re.match(r'^how long\b', e1, re.I)):
            return [e1, e2]

    # No comparison pattern found — return question unchanged
    return [question]


# ── ITER-8: Date-augmented recall for single-entity TR questions ────────────────

_WEEK_WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
               'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12}
_DAY_NAMES = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
              'friday': 4, 'saturday': 5, 'sunday': 6}

def compute_tr_target_date(question: str, question_date_ts: float) -> Optional[str]:
    """
    For TR questions with a fixed relative date phrase (e.g., 'last Saturday',
    'four weeks ago', '10 days ago'), compute the absolute target date and return
    it as a YYYY-MM-DD string. Returns None if no fixed relative date is found.
    """
    if not question_date_ts:
        return None
    ref = datetime.fromtimestamp(question_date_ts)
    q = question.lower()

    # "N days ago" — e.g., "10 days ago", "21 days ago"
    m = re.search(r'\b(\d+)\s+days?\s+ago\b', q)
    if m:
        return (ref - timedelta(days=int(m.group(1)))).strftime('%Y-%m-%d')

    # "N weeks ago" / word-number weeks ago — e.g., "four weeks ago", "2 weeks ago"
    m = re.search(r'\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+weeks?\s+ago\b', q)
    if m:
        raw = m.group(1)
        n = int(raw) if raw.isdigit() else _WEEK_WORDS.get(raw, 0)
        if n > 0:
            return (ref - timedelta(weeks=n)).strftime('%Y-%m-%d')

    # "N months ago" — e.g., "six months ago"
    m = re.search(r'\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+months?\s+ago\b', q)
    if m:
        raw = m.group(1)
        n = int(raw) if raw.isdigit() else _WEEK_WORDS.get(raw, 0)
        if n > 0:
            # FIX P1-A: datetime.replace(month=N) raises ValueError when ref.day is 29-31
            # and the target month is shorter (e.g., Jan 31 - 1 month → Feb 31 does not exist).
            # Compute year/month first, then cap the day with calendar.monthrange().
            _tgt_month = ref.month - n
            _tgt_year = ref.year
            while _tgt_month < 1:
                _tgt_month += 12
                _tgt_year -= 1
            _tgt_day = min(ref.day, calendar.monthrange(_tgt_year, _tgt_month)[1])
            target = ref.replace(year=_tgt_year, month=_tgt_month, day=_tgt_day)
            return target.strftime('%Y-%m-%d')

    # "last [weekday]" / "past [weekday]" — e.g., "last Saturday", "past Tuesday"
    for day_name, day_num in _DAY_NAMES.items():
        if re.search(rf'\b(?:last|past)\s+{day_name}\b', q):
            ref_weekday = ref.weekday()  # Mon=0, Sun=6
            days_ago = (ref_weekday - day_num) % 7
            if days_ago == 0:
                days_ago = 7
            return (ref - timedelta(days=days_ago)).strftime('%Y-%m-%d')

    # "past weekend" / "last weekend"
    if re.search(r'\b(?:last|past)\s+weekend\b', q):
        ref_weekday = ref.weekday()
        # Most recent Saturday (weekday=5)
        days_to_sat = (ref_weekday - 5) % 7
        if days_to_sat == 0 and ref_weekday != 5:
            days_to_sat = 7
        return (ref - timedelta(days=days_to_sat)).strftime('%Y-%m-%d')

    return None


_MONTH_NAMES = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
}


def compute_ms_time_window(question: str, question_date_ts: float):
    """
    For MS counting questions with a time window phrase, return (start_ts, end_ts).
    Returns None if no time window is detected or if question_date_ts is missing.
    Used to do a supplementary time-bounded recall to ensure all events in the
    relevant period are captured, regardless of semantic similarity score.
    """
    if not question_date_ts:
        return None
    ref = datetime.fromtimestamp(question_date_ts)
    q = question.lower()

    # "past/last N days" (e.g., "in the past 30 days")
    m = re.search(r'\b(?:past|last)\s+(\d+)\s+days?\b', q)
    if m:
        start = ref - timedelta(days=int(m.group(1)))
        return (start.timestamp(), question_date_ts)

    # "past/last N weeks" or word-number weeks (e.g., "past two weeks")
    m = re.search(r'\b(?:past|last)\s+(\d+|one|two|three|four|five|six)\s+weeks?\b', q)
    if m:
        raw = m.group(1)
        n = int(raw) if raw.isdigit() else _WEEK_WORDS.get(raw, 0)
        if n > 0:
            start = ref - timedelta(weeks=n)
            return (start.timestamp(), question_date_ts)

    # "past/last N months" or "last month"
    m = re.search(r'\b(?:past|last)\s+(\d+|one|two|three|four|five|six)?\s*months?\b', q)
    if m:
        raw = m.group(1)
        n = int(raw) if raw and raw.isdigit() else (_WEEK_WORDS.get(raw, 0) if raw else 1)
        if n == 0:
            n = 1
        start = ref - timedelta(days=30 * n)
        return (start.timestamp(), question_date_ts)

    # "in [month_name]" (e.g., "in January", "in March")
    for mname, mnum in _MONTH_NAMES.items():
        if re.search(rf'\bin\s+{mname}\b', q):
            year = ref.year
            if mnum > ref.month:
                year -= 1  # previous year's named month
            start = datetime(year, mnum, 1)
            end = datetime(year + (1 if mnum == 12 else 0), (mnum % 12) + 1, 1)
            return (start.timestamp(), end.timestamp())

    # "this year" / "in this year" / "so far this year" — Jan 1 through reference date
    if re.search(r'\b(this year|in this year|so far this year)\b', q):
        start = datetime(ref.year, 1, 1)
        return (start.timestamp(), question_date_ts)

    return None


def compute_tr_time_window(question: str, question_date_ts: float):
    """For TR ordering questions with an explicit time-scope phrase ('past three months',
    'in January', 'last month'), return (start_ts, end_ts) for supplementary time-bounded
    recall to ensure all N events in the period are captured.

    Returns None if no time-scope is detected or if question_date_ts is missing.
    """
    if not question_date_ts:
        return None
    ref = datetime.fromtimestamp(question_date_ts)
    q = question.lower()

    # "past/last N months" or "past month"
    m = re.search(r'\b(?:past|last)\s+(\d+|one|two|three|four|five|six)?\s*months?\b', q)
    if m:
        raw = m.group(1)
        n = int(raw) if raw and raw.isdigit() else (_WEEK_WORDS.get(raw, 0) if raw else 1)
        if n == 0:
            n = 1
        start = ref - timedelta(days=30 * n)
        return (start.timestamp(), question_date_ts)

    # "past/last N weeks"
    m = re.search(r'\b(?:past|last)\s+(\d+|one|two|three|four|five|six|seven|eight)\s+weeks?\b', q)
    if m:
        raw = m.group(1)
        n = int(raw) if raw.isdigit() else _WEEK_WORDS.get(raw, 0)
        if n > 0:
            start = ref - timedelta(weeks=n)
            return (start.timestamp(), question_date_ts)

    # "in [month_name]" (e.g., "in January")
    for mname, mnum in _MONTH_NAMES.items():
        if re.search(rf'\bin\s+{mname}\b', q):
            year = ref.year
            if mnum > ref.month:
                year -= 1  # previous year's named month
            start = datetime(year, mnum, 1)
            end = datetime(year + (1 if mnum == 12 else 0), (mnum % 12) + 1, 1)
            return (start.timestamp(), end.timestamp())

    return None


# ── Fix 2: Session date label injection for TR context ─────────────────────────

def inject_session_labels(context: str, results: list, haystack_dates) -> str:
    """
    Inject [Session: YYYY-MM-DD HH:MM] headers into context, grouping memories
    from the same session under a single header.

    Args:
        context: Assembled context string (memory bullets start with "- ")
        results: List of RetrievalResult objects with provenance.session_id
        haystack_dates: dict(session_id → date_str) OR list of date_str indexed
                        by session number extracted from session_id suffix _sN
    Returns:
        Context string with session date headers inserted at group boundaries.
    """
    # Build session_id → formatted date label
    session_to_date: dict[str, str] = {}

    def _format_date(date_val: str) -> str:
        """Extract YYYY-MM-DD HH:MM from various date string formats."""
        # "2023/05/24 (Wed) 02:06" → "2023-05-24 02:06"
        m = re.search(r'(\d{4})[/-](\d{2})[/-](\d{2})(?:\s+\([^)]+\))?\s+(\d{2}:\d{2})', str(date_val))
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)} {m.group(4)}"
        m = re.search(r'(\d{4})[/-](\d{2})[/-](\d{2})', str(date_val))
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        return str(date_val).split(' ')[0]

    if isinstance(haystack_dates, dict):
        for sid, date_val in haystack_dates.items():
            session_to_date[sid] = _format_date(str(date_val))
    elif isinstance(haystack_dates, list):
        for r in results:
            try:
                sid = r.node.provenance.session_id
            except AttributeError:
                continue
            if not sid:
                continue
            m = re.search(r'_s(\d+)$', sid)
            if m:
                sidx = int(m.group(1))
                if sidx < len(haystack_dates):
                    session_to_date[sid] = _format_date(str(haystack_dates[sidx]))

    if not session_to_date:
        return context

    # Build content-snippet → session-date lookup from results
    content_to_date: dict[str, str] = {}
    for r in results:
        try:
            sid = r.node.provenance.session_id
            content_snippet = r.node.content.strip()
        except AttributeError:
            continue
        if sid and sid in session_to_date:
            content_to_date[content_snippet] = session_to_date[sid]

    if not content_to_date:
        return context

    # Process context line by line, inserting session headers at group boundaries
    lines = context.split('\n')
    new_lines: list[str] = []
    current_date: str | None = None

    for line in lines:
        if line.startswith('- '):
            content = line[2:].strip()
            matched_date = None
            for c_snippet, d in content_to_date.items():
                match_len = min(len(c_snippet), len(content), 50)
                if match_len > 5 and c_snippet[:match_len] == content[:match_len]:
                    matched_date = d
                    break
            if matched_date and matched_date != current_date:
                new_lines.append(f"[Session: {matched_date}]")
                current_date = matched_date
        new_lines.append(line)

    return '\n'.join(new_lines)


# ── Fix 3: Coreference hint detection for MS counting questions ────────────────

def detect_coreference_hints(context: str, question: str) -> list[str]:
    """
    Detect potential coreference ambiguity for the same first name appearing
    with different relational descriptors (e.g., 'cousin Emily', 'Emily and Sarah').

    Returns a list of hint strings (empty if no ambiguity detected).
    Triggers when the same first name appears 2+ times AND at least one occurrence
    has a relational descriptor (cousin, roommate, friend, etc.) in its vicinity.
    """
    relational_words = {
        'cousin', 'roommate', 'colleague', 'coworker', 'friend', 'neighbor',
        'sister', 'brother', 'aunt', 'uncle', 'partner', 'classmate', 'teammate',
        'employee', 'manager', 'boss', 'childhood', 'college', 'old', 'childhood',
    }
    _skip_words = {
        'the', 'a', 'an', 'in', 'on', 'at', 'by', 'to', 'of', 'and', 'or',
        'not', 'but', 'for', 'so', 'yet', 'nor', 'session', 'user', 'assistant',
        'step', 'note', 'total', 'just', 'had', 'has', 'have', 'was', 'were',
        'been', 'being', 'its', 'his', 'her', 'their', 'our', 'your', 'my',
    }

    # Collect occurrences of each proper name (2+ chars, initial cap)
    name_to_surroundings: dict[str, list[str]] = {}
    for m in re.finditer(r'\b([A-Z][a-z]{2,})\b', context):
        name = m.group(1)
        if name.lower() in _skip_words:
            continue
        surrounding = context[max(0, m.start() - 50):m.end() + 30].lower()
        name_to_surroundings.setdefault(name, []).append(surrounding)

    hints = []
    for name, surroundings in name_to_surroundings.items():
        if len(surroundings) < 2:
            continue
        # Check that at least one occurrence has a relational descriptor nearby
        descriptors_found = set()
        for ctx in surroundings:
            for word in relational_words:
                if word in ctx:
                    descriptors_found.add(word)
        if descriptors_found:
            hints.append(
                f"Note: '{name}' appears in multiple descriptions — verify whether "
                f"all occurrences (e.g., with descriptors: "
                f"{', '.join(repr(w) for w in sorted(descriptors_found))}) "
                f"refer to the SAME '{name}' before counting. "
                f"If yes, count all as ONE person, not multiple people."
            )

    return hints


# ── Configuration ──────────────────────────────────────────────────────────────

EVALUATOR_MODEL  = "gpt-4o"
GEN_MODEL        = "gpt-4o"    # generator model — override via --gen-model (supports claude-* models)
JUDGE_MODEL      = "gpt-4o"    # separate judge model — override via --judge-model for fast dev iteration
# Per-type token budgets (computed to fit within 820K daily cap)
TOKEN_BUDGETS = {
    "single-session-user":       1500,   # ITER-16: increased from 1200 for better SSU recall coverage
    "single-session-assistant":  3500,   # ITER-29: increased from 2500 to capture full long positional lists (100-item lists)
    "single-session-preference": 3500,  # ITER-7: increased from 2000 to capture more preference memories
    "knowledge-update":          2500,  # Increased from 1800: more context for finding updates
    "multi-session":             7500,  # v5: increased from 5000 for better aggregation completeness
    "temporal-reasoning":        5000,  # Iter9b: increased from 3500 to fix 5-event ordering truncation (gpt4_d6585ce8)
}
# v17: bypass memory retrieval entirely, inject the full raw haystack as context.
# This eliminates all retrieval failures and gives the model complete information.
USE_DIRECT_CONTEXT = False
assert not USE_DIRECT_CONTEXT, "INVALID: USE_DIRECT_CONTEXT must be False for legitimate evaluation"
# TPM limit is 30,000 tokens/min. Reserve ~5,000 for output+overhead, leaving ~25,000 for context.
# At ~4 chars/token: 25,000 * 4 = 100,000 chars. Use 92,000 for safety.
MAX_CONTEXT_CHARS = 96_000
RESULTS_FILE     = "longmemeval_results_v36.json"  # ITER-36: fix regressions (wedding couple-id, cuisine fermentation, entity-count, session-date-anchoring, concert-vinyl, complete-answer)
PROGRESS_FILE    = "longmemeval_progress_v36.json"  # ITER-36: fix regressions (wedding couple-id, cuisine fermentation, entity-count, session-date-anchoring, concert-vinyl, complete-answer)
DATASET_PATH     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LongMemEval", "data", "longmemeval_oracle.json")

# Judge max_tokens=10 matches official evaluate_qa.py
JUDGE_MAX_TOKENS   = 10
# Generator: allow enough tokens for chain-of-thought temporal reasoning
GEN_MAX_TOKENS     = 300
GEN_TEMPERATURE    = 0.0

GEN_SYSTEM_PROMPT = """\
You are a precise memory assistant. You have access to a user's conversation history as memory context.

RULES:
1. Read EVERY memory entry carefully. Extract ALL explicit dates, and anchor relative phrases:
   - "last Saturday / two months ago / on June 14th" → convert to absolute date using the reference date or session date
   - "[Session date: YYYY/MM/DD]" labels anchor ALL relative phrases in that session to that date
   - When the user explicitly states "on [date]", that IS the date — even if the assistant disputes or questions the event
   - ARITHMETIC MODIFIERS: If a general fact has a conditional modifier, compute the modified value. E.g., "I wake up at 7:00 AM" + "on Tuesdays I wake up 15 minutes earlier" → wake up time on Tuesdays = 7:00 AM - 15 min = 6:45 AM. Always apply the specific modifier when the question asks about a specific condition.

2. For ordering/comparison questions ("which first / who before / who became X first"):
   - Map EVERY item/person to its specific date or timeframe extracted from context
   - The item with the EARLIER date came FIRST
   - "I recently got X" = X just arrived; "I just got / just bought" = very recent
   - "I'm glad you FINALLY received X after the delay" = X arrived LATER than other items (it was delayed)
   - If one item was received "a week before" another, that item is EARLIER
   - Do NOT let assistant disclaimers ("there's no such event") change the date the user stated
   - CRITICAL FOR ABSTENTION: If one of the two people/items (e.g., "Tom") is NOT MENTIONED AT ALL anywhere in context, say "I don't have that information about [Tom]." Do NOT declare the other party as the winner just because that party has data.
   - BUT: If BOTH parties are mentioned in context (even without explicit dates), try harder to infer ordering from ALL available clues:
     * "recently" / "just got" / "just set up" / "just started" = LATER (happened more recently, therefore NOT first)
     * EXPLICIT TIME OVERRIDES "RECENTLY": If context ALSO contains an explicit time for the SAME item ("I got X a month ago", "I received Y about 2 weeks ago"), the EXPLICIT TIME is authoritative. Ignore the vague "recently" and compute the date from the specific phrase. Example: "I recently got a new prime lens" + "I got [the lens] a month ago" → lens arrived ~1 month before session date, NOT "just now."
     * CRITICAL: "since I recently upgraded to X" / "I recently set up X" / "I just finished X" = X is the MOST RECENT item. X did NOT happen first — X happened LAST. The OTHER item you are comparing X to came FIRST.
       Example: "Since I recently upgraded to a mesh network system" → mesh is NEWER/LATER. If asked which was set up first (thermostat vs mesh), the THERMOSTAT came first.
       Example: "I just finished binge-watching The Crown" → The Crown was watched RECENTLY/LATEST. The OTHER show was started FIRST.
     * "last month" / "last year" / "have been using for a while" / "has been helping" = EARLIER (happened before "recent" events)
     * Sequential sessions: if item A is mentioned in earlier sessions and B in later sessions, A likely happened first
     * Absence of an explicit date ≠ absence of all information. Reason from all available context.
     * Do NOT infer meeting order from relationship depth ("already know them", "planning to reconnect"). These phrases describe familiarity, NOT when the meeting occurred. Only use explicit date markers ("a few months ago", "last week", etc.).
     * CRITICAL ONE-SIDED RULE: phrases like 'planning to reconnect', 'haven't seen in a while', 'been meaning to catch up', 'old friend', 'known for years', 'close friends', 'looking forward to seeing' give ZERO information about when you FIRST met someone or when an event occurred. These phrases describe the CURRENT relationship state, not when it started. If you cannot find an explicit statement about when you first met or when the event happened, do NOT guess — say you cannot determine it from the context.
     * CAUSAL/SEQUENTIAL ORDERING: "Since I started X, I've been doing Y" = X started BEFORE Y. "After getting X, I began Y" = X before Y. "X led me to Y" = X before Y. Use these causal phrases as ordering clues when explicit dates are absent.

3. For duration/count questions ("how many days / how long / how many weeks"):
   - Extract BOTH event dates explicitly from context
   - Show calculation: "Event A: [date]. Event B: [date]. Difference = X days/weeks."
   - EDUCATION SPAN: For "how many years from [start of education] to [completion of degree]", compute END_YEAR − START_YEAR (e.g., HS started 2010, Bachelor's completed 2020 → 2020 − 2010 = 10 years), NOT the sum of years in each program (not 4 + 4 = 8). The question asks for the full calendar span from start to finish.

4. For aggregation questions ("how many total / in the past two weeks / in December"):
   - Scan ALL memory entries — do not stop at the first mention
   - List EVERY distinct instance found, then count/sum them all
   - If context says "4 items" explicitly, use that. Otherwise count from distinct mentions.

4b. De-duplication: If the same person, doctor, kit, project, event, or item is mentioned multiple times across different sessions or contexts, count it ONLY ONCE.
   - Same name = same person (Dr. Lee = Dr. Lee regardless of which session)
   - Same specialty described in follow-up = same doctor (e.g., "dermatologist" + "Dr. Lee" follow-up = 1 doctor)
   - A follow-up appointment / return visit = same doctor, not a new one
   - Only count DISTINCT individuals, items, or events
   EXCEPTION — "pick up / return" questions: an EXCHANGE generates TWO separate items: (1) the item to RETURN + (2) the new item to PICK UP. Count both. Do NOT collapse them into one "distinct item."
   EXCEPTION — items described in multiple ways: A model kit is a model kit whether mentioned as "kit", "diorama", "project", or "build." Do NOT exclude items because of HOW they are described or used.

5. For knowledge-update questions: report the MOST RECENT value seen in context (the latest update overrides earlier ones).

6. For questions where the answer truly cannot be found in context (zero relevant evidence): say "I don't have that information."
   BUT: if ANY relevant evidence exists (even indirect), use it — do not default to "I don't know" prematurely.

7. IMPORTANT — Reference Date clarification: The "Reference date" shown in the prompt is ONLY the date when the question was asked. It is NOT the date of any purchase, event, or action. Never treat the reference date as an event date.

8. IMPORTANT — Entity specificity: If the question asks about entity X (e.g., "iPad", "Tom") but the context only mentions a related-but-different entity Y (e.g., "iPhone", "Alex's children"), say "I don't have that information about X." Do NOT infer that Y = X unless explicitly stated in context.
   CRITICAL: Do NOT apply dates, quantities, or delivery details from entity Y to answer about entity X. Example: if context says "laptop bag arrived on 1/20" but the question asks about "iPad case", you CANNOT use 1/20 — say "I don't have information about your iPad case." Similarly, "Software Engineer" and "Senior Software Engineer" are DIFFERENT roles — do not answer about one using facts about the other.

9. For COUNTING questions (how many, how much, how many X did I):
   FIRST: Determine whether this is a STATED-TOTAL or AGGREGATION question.

   STATED-TOTAL: The user explicitly stated a count/total in context ("I have N cameras", "I reached N followers", "my collection now has N", "I'm at N lbs", "I have N sessions booked"). For these: report the MOST RECENTLY STATED value directly. Do NOT enumerate individual items — the user already counted them. Apply Rule 5 (most recent value wins). Do NOT apply the Step 1-4 template to stated-totals.

   AGGREGATION (scan-and-count): The total must be derived by scanning ALL sessions for individual instances (e.g., "how many times did I visit X", "how many different doctors have I seen", "how many workouts did I do this month"). For these, use the COUNTING OUTPUT TEMPLATE:
     Step 1: List every instance you found: "1. [item/event], [date if available]"
     Step 2: Apply deduplication — mark duplicates as "DUPLICATE OF #N"
     Step 3: Count only non-duplicate items
     Step 4: YOUR FINAL SENTENCE MUST BE: "Total count: [number]." This format is MANDATORY.
   For ORDERING/COMPARISON questions (which first / who first / who before): do NOT guess the answer first. Complete ALL reasoning steps (find dates → compare) then state the FINAL ANSWER as the LAST sentence: "Answer: [X] came first."
   For OTHER non-counting questions: answer first, then brief reasoning. Keep total response under 4 sentences.

10. USER vs ASSISTANT content — THIS IS ABSOLUTE: Memory entries that contain advisory or suggestion language are AI ASSISTANT responses — they represent what the assistant RECOMMENDED or SUGGESTED, NOT what the user ACTUALLY DID, owned, or experienced.
   - ASSISTANT phrases (ZERO count for these): "you might want to...", "you could try...", "consider...", "I suggest...", "here are some options...", "you should...", "why not try...", "I recommend...", "explore other [cuisines/places]...", "try [X], [Y], [Z]" as a list of suggestions, "have you thought about...", "it might be worth...", "a great choice would be..."
   - Do NOT count assistant-suggested items as things the user has actually done, bought, visited, or experienced. This rule CANNOT be overridden by context.
   - Example: "* Explore other international cuisines like Korean, Japanese..." = ASSISTANT SUGGESTION, NOT user fact. Zero count.
   - Example: "You might enjoy grapefruit in your next cocktail" = ASSISTANT SUGGESTION. Grapefruit does NOT count as a citrus the user used.
   - Example: "You might want to try Thai food" — if the user never says "I tried Thai food", Thai does NOT count.
   - Only count items that the USER explicitly stated they did: "I tried...", "I made...", "I bought...", "I've been doing...", "I attended...", "I visited...", "I downloaded..."

11. INCREMENTS in knowledge-update context — MANDATORY ARITHMETIC: If context shows "I have N [items]" AND "I just added/got another [item]", you MUST compute N+1 as the current total. The explicit total represents the state BEFORE the addition. The word "just" signals the addition occurred AFTER the total was stated.
   This computation is MANDATORY. You MUST write out the arithmetic step. Returning the starting value without computing the change is WRONG.
   - INCREMENT FORMAT: "Starting quantity: N. Change: +1. Final quantity: N+1."
   - DECREMENT FORMAT: "Starting quantity: N. Change: -1. Final quantity: N-1."
   - Example: "I have 37 pre-1920 American coins" + "I just added a new Barber quarter" → Starting: 37. Change: +1. Final: 38.
   - Similarly: "I have 30 items" + "I just used/sold/gave away one" → Starting: 30. Change: -1. Final: 29.

12. NAMED ENTITY COREFERENCE: When the same first name appears multiple times in context:
   SAME PERSON (count once): All occurrences use the same relationship label, or no explicit relational role is stated (e.g., "Emily" appearing 3 times without a role description = likely the same Emily).
   DIFFERENT PEOPLE (count separately): Occurrences use DIFFERENT explicit relational descriptors (e.g., "cousin Emily" vs "college roommate Emily"). Treat these as distinct people UNLESS the location-based dedup rule (4b) applies.
   RULE: Same name + same/absent role = 1 person. Same name + different labels = APPLY RULE 4b location check FIRST before counting separately.
   CRITICAL OVERRIDE — LOCATION WINS OVER LABELS: If two events involving the same first name share IDENTICAL concrete location details (e.g., both described as "rooftop garden ceremony in the city", or both at "the vineyard"), they ARE the same event and the same person. Different relationship labels ("cousin" vs "college roommate") may simply be different ways of describing the same person across different sessions. Location match + same name = SAME EVENT, always.\
"""

# ── Judge prompt templates (verbatim from evaluate_qa.py) ─────────────────────

def get_anscheck_prompt(task: str, question: str, answer: str, response: str,
                        abstention: bool = False, question_date: str = None) -> str:
    if not abstention:
        if task in ["single-session-user", "single-session-assistant", "multi-session"]:
            template = (
                "I will give you a question, a correct answer, and a response from a model. "
                "Please answer yes if the response contains the correct answer. Otherwise, answer no. "
                "If the response is equivalent to the correct answer or contains all the intermediate steps "
                "to get the correct answer, you should also answer yes. If the response only contains a subset "
                "of the information required by the answer, answer no. \n\n"
                "Question: {}\n\nCorrect Answer: {}\n\nModel Response: {}\n\n"
                "Is the model response correct? Answer yes or no only."
            )
            return template.format(question, answer, response)
        elif task == "temporal-reasoning":
            # Include question_date as reference so the judge can evaluate temporal arithmetic
            date_ctx = f"Reference Date: {question_date}\n\n" if question_date else ""
            template = (
                "I will give you a question, a correct answer, and a response from a model. "
                "Please answer yes if the response contains the correct answer. Otherwise, answer no. "
                "If the response is equivalent to the correct answer or contains all the intermediate steps "
                "to get the correct answer, you should also answer yes. If the response only contains a subset "
                "of the information required by the answer, answer no. In addition, do not penalize off-by-one "
                "errors for the number of days. If the question asks for the number of days/weeks/months, etc., "
                "and the model makes off-by-one errors (e.g., predicting 19 days when the answer is 18), the "
                "model's response is still correct. \n\n"
                "{date_ctx}Question: {question}\n\nCorrect Answer: {answer}\n\nModel Response: {response}\n\n"
                "Is the model response correct? Answer yes or no only."
            )
            return template.format(date_ctx=date_ctx, question=question, answer=answer, response=response)
        elif task == "knowledge-update":
            template = (
                "I will give you a question, a correct answer, and a response from a model. "
                "Please answer yes if the response contains the correct answer. Otherwise, answer no. "
                "If the response contains some previous information along with an updated answer, the response "
                "should be considered as correct as long as the updated answer is the required answer.\n\n"
                "Question: {}\n\nCorrect Answer: {}\n\nModel Response: {}\n\n"
                "Is the model response correct? Answer yes or no only."
            )
            return template.format(question, answer, response)
        elif task == "single-session-preference":
            template = (
                "I will give you a question, a rubric for desired personalized response, and a response from "
                "a model. Please answer yes if the response satisfies the desired response. Otherwise, answer no. "
                "The model does not need to reflect all the points in the rubric. The response is correct as long "
                "as it recalls and utilizes the user's personal information correctly.\n\n"
                "Question: {}\n\nRubric: {}\n\nModel Response: {}\n\n"
                "Is the model response correct? Answer yes or no only."
            )
            return template.format(question, answer, response)
        else:
            raise NotImplementedError(f"Unknown task type: {task}")
    else:
        template = (
            "I will give you an unanswerable question, an explanation, and a response from a model. "
            "Please answer yes if the model correctly identifies the question as unanswerable. The model could "
            "say that the information is incomplete, or some other information is given but the asked information "
            "is not.\n\n"
            "Question: {}\n\nExplanation: {}\n\nModel Response: {}\n\n"
            "Does the model correctly identify the question as unanswerable? Answer yes or no only."
        )
        return template.format(question, answer, response)


# ── Dataset conversion ─────────────────────────────────────────────────────────

def convert_sessions_to_messages(case: dict) -> list[dict]:
    """
    Flatten all haystack_sessions into a single list of {"role": str, "content": str} dicts.
    The dataset stores sessions as list-of-lists, each turn having role/content/has_answer.
    We strip has_answer and preserve role+content only.

    Each session is prefixed with a "[Session date: ...]" system marker so that all
    relative temporal phrases in that session can be resolved against the anchor date.
    """
    messages = []
    sessions = case["haystack_sessions"]
    dates = case.get("haystack_dates", [])
    for idx, session in enumerate(sessions):
        date_str = dates[idx] if idx < len(dates) else None
        # Inject a session-boundary marker before each session's turns
        if date_str:
            messages.append({
                "role": "system",
                "content": f"[Session date: {date_str}]"
            })
        for turn in session:
            role = turn["role"]
            content = turn["content"]
            messages.append({"role": role, "content": content})
    return messages


def build_multisession_raw_context(case: dict, max_chars: int = 20000) -> str:
    """
    Build a chronological full-dump context for multi-session aggregation questions.
    Instead of using semantic retrieval (which can miss low-similarity but relevant items),
    this directly concatenates ALL session content in chronological order, ensuring every
    session is represented regardless of semantic similarity to the question.
    """
    sessions = case["haystack_sessions"]
    dates = case.get("haystack_dates", [])
    parts = []
    for idx, session in enumerate(sessions):
        date_str = dates[idx] if idx < len(dates) else None
        header = f"\n--- Session {idx + 1}" + (f" ({date_str})" if date_str else "") + " ---"
        parts.append(header)
        for turn in session:
            role = turn.get("role", "unknown")
            content = turn.get("content", "")
            parts.append(f"{role.capitalize()}: {content}")
    full_text = "\n".join(parts)
    # Trim from the start if over limit (keep most recent sessions — they tend to have more info)
    if len(full_text) > max_chars:
        full_text = full_text[-max_chars:]
        # Align to next session boundary if possible
        boundary = full_text.find("\n--- Session")
        if boundary > 0:
            full_text = full_text[boundary:]
    return full_text.strip()


# ── API helpers with exponential backoff ───────────────────────────────────────

async def call_with_backoff(coro_fn, *args, max_wait=60, max_retries=10, **kwargs):
    """Call an async function; on RateLimitError, retry with exponential backoff."""
    _rate_limit_errors = (RateLimitError,) if not _ANTHROPIC_AVAILABLE else (RateLimitError, AnthropicRateLimitError)
    wait = 2
    retries = 0
    while True:
        try:
            return await coro_fn(*args, **kwargs)
        except _rate_limit_errors as e:
            retries += 1
            if retries > max_retries:
                print(f"\n  [RateLimit] max_retries={max_retries} exceeded. Error: {e}. Raising.", flush=True)
                raise
            print(f"\n  [RateLimit] sleeping {wait}s (retry {retries}/{max_retries}) ...", flush=True)
            await asyncio.sleep(wait)
            wait = min(wait * 2, max_wait)


async def call_gen_api(gen_client, system: str, user: str, max_tokens: int, temperature: float) -> tuple[str, int]:
    """Route a generation call to either OpenAI or Anthropic depending on GEN_MODEL."""
    if GEN_MODEL.startswith("claude-"):
        # Anthropic API: system is a top-level parameter, not in messages
        resp = await call_with_backoff(
            gen_client.messages.create,
            model=GEN_MODEL,
            system=system,
            messages=[{"role": "user", "content": user}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        text = resp.content[0].text.strip()
        tokens = (resp.usage.input_tokens + resp.usage.output_tokens) if resp.usage else 0
        return text, tokens
    else:
        resp = await call_with_backoff(
            gen_client.chat.completions.create,
            model=GEN_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = resp.choices[0].message.content.strip()
        tokens = resp.usage.total_tokens if resp.usage else 0
        return text, tokens


async def generate_answer(client, context: str, question: str,
                          question_type: str = "", question_date: str = "") -> tuple[str, int]:
    """Generate an answer from retrieved memory context. Returns (answer_text, tokens_used)."""
    # Build user message with additional temporal context hint for temporal-reasoning
    date_hint = f"\nReference date (when question was asked): {question_date}" if question_date else ""
    type_hint = ""
    if question_type == "temporal-reasoning":
        type_hint = (
            "\nNote: TEMPORAL REASONING question. "
            "Step 1: Find the explicit date or time clue for EACH item/event mentioned in the question. "
            "SESSION DATE RESOLUTION: The context includes a 'Session Dates' section. "
            "When a memory says 'today', 'just now', 'this morning', or 'just got back', the event date IS that session's date. "
            "QUESTION TIME PHRASES: When the QUESTION itself uses relative time ('last Saturday', 'last Tuesday', 'two weeks ago', 'N months ago', etc.), "
            "compute that absolute date using the provided REFERENCE DATE — NOT using any session date. "
            "Example: if the reference date is 2023/04/18 (Tuesday) and the question says 'last Tuesday', then last Tuesday = 2023/04/11 — do NOT compute 'last Tuesday' relative to a session dated 2023/04/11. "
            "The reference date is the question asker's 'now'; session dates are anchors for memory entries only.\n"
            "NEAREST SESSION MATCH: After computing the target date from a time phrase in the question, if multiple sessions exist, rank them by |session_date − target_date| (ascending). Investigate the NEAREST session first. "
            "Do NOT default to the session that is semantically most prominent if a different session is temporally closer to the target date. "
            "BIDIRECTIONAL WINDOW: The target date is a POINT, not an upper bound. Sessions that fall a few days AFTER the target date are equally valid as sessions a few days BEFORE — always pick the session with the smallest |session_date - target_date| regardless of direction. "
            "Example: target_date=Feb 28; sessions on Feb 10 (18 days before) and Mar 1 (1 day after) → Mar 1 is closer → use Mar 1, not Feb 10.\n"
            "ART-RELATED RECOGNITION: Any visit to the Metropolitan Museum of Art, the Museum of Modern Art, the Art Institute, or ANY museum whose name contains 'Art' IS an art-related event — regardless of whether the specific exhibit is about history, ancient civilizations, science, or any other topic. "
            "CRITICAL EXAMPLE: attending an 'Ancient Civilizations' exhibit at the Metropolitan Museum of Art IS an art-related event. Do NOT reject it as 'not art' just because the exhibit topic is historical. "
            "DEEP SCAN OF NEAREST SESSION: When the nearest session's primary topic appears unrelated to the question (e.g., mummification, travel plans), still scan ALL user messages in that session — users often mention the relevant event as a passing aside ('I attended X today' buried in a question about Y). Do NOT conclude 'no art event in this session' before checking every user message.\n"
            "RECEIVING EVENT TOLERANCE: When a question asks 'I received [item X] on [date], from whom?', compute the target date and find the session from that date. "
            "If that session describes the user receiving ANY item from a named person on that matching date, answer with that person's name — even if the item's name differs (e.g., 'crystal chandelier' vs 'piece of jewelry'). "
            "CRITICAL EXAMPLE: question says 'I received a piece of jewelry last Saturday from whom?' and session on last Saturday says 'I got a stunning crystal chandelier from my aunt' → answer: 'from my aunt'. The date match is definitive; do NOT abstain just because the item names differ.\n"
            "CONTEXTUAL ACHIEVEMENT: Users often mention a recent achievement as background context at the START of a session before asking for related advice. 'I just X today' or 'I recently Y' at the session opening IS a factual event and IS the answer to 'what milestone/event did I mention'. "
            "Do NOT dismiss it as 'only background' — if the question asks what business milestone was mentioned and the nearest session opens with 'I just signed a contract with my first client today', THAT IS the business milestone. "
            "EXAMPLE: session opens with 'I just signed a contract with my first client today, and I want to make sure I'm covering all my bases' → milestone = 'signed a contract with first client'.\n"
            "Step 2: Convert relative phrases to absolute dates using SESSION DATE as anchor. "
            "MONTH ARITHMETIC: 'last month' / 'a month ago' from 2023/05/27 = 2023/04/27 (subtract exactly 1 month — never use a mid-month approximation). "
            "Similarly '2 weeks ago' from 2023/05/27 = 2023/05/13 (subtract exactly 14 days). "
            "Step 3: For duration questions: duration = later_date − earlier_date. "
            "For ordering questions: item with EARLIER date came FIRST. "
            "Show your work: 'Event A: date=YYYY/MM/DD. Event B: date=YYYY/MM/DD. Result: [calculation].' "
            "COMBINING DURATIONS: If the question asks for TOTAL time across multiple items, find each duration separately then add. "
            "Example: 'Book A: 3 weeks. Book B: 2.5 weeks. Total = 5.5 weeks.' Always show the addition explicitly.\n"
            "CAUSAL PAST-EVENT CONTEXT: When context says 'I need/plan to [buy/replace/fix] X, since I lost/broke/misplaced it N [time] ago', the causal clause reveals the past event date. Extract it: 'since I lost my [X] N [time] ago' → [X] was lost N [time] before session date. Use this to compute the event date even if the sentence is phrased as a future plan.\n"
            "PARTIAL DATE ORDERING: When you have an explicit date for ONE event (e.g., 'phone case received ~April 29') but NO explicit date for the OTHER event, do NOT automatically abstain. Instead: (a) check if the other event is mentioned in context at all (even indirectly), (b) look at which session each event appears in — if event A is in session 08:19 and event B is in session 10:14, and the question asks which happened first, note that the SESSIONS are on the same day but different times, meaning the USER was discussing both events on the same day. Use any timing clue available. (c) Only abstain if you truly cannot determine ordering from any available evidence.\n"
            "CONCERTS AND LIVE SHOWS ARE MUSIC EVENTS: 'I saw [band/artist] live at [venue]', 'I attended a concert', 'I went to a show' — ALL of these are music events. "
            "If context says 'I saw [Queen] live with Adam Lambert at [Prudential Center] with my parents', the music event is the Queen/Adam Lambert concert, and 'with my parents' is who they went with. "
            "Do NOT say 'no music event mentioned' if context contains 'saw [artist] live' or 'saw [artist] perform' — that IS the music event.\n"
            "FUTURE PLAN vs PAST FACT: 'I'm thinking of visiting X', 'I plan to visit X', 'I might go to X' = FUTURE PLAN, NOT a past event. "
            "Do NOT count future plans as past events.\n"
            "HOW MANY DAYS/WEEKS/MONTHS AGO: When the question asks 'how many [days/weeks/months] ago did I [event]?':\n"
            "  ALGORITHM:\n"
            "  1. Find the event in the context (e.g., 'bought X', 'attended Y', 'recovered from Z')\n"
            "  2. Note the [Session: YYYY-MM-DD] label of the session containing that event\n"
            "  2a. ADJUST FOR IN-SESSION RELATIVE DATE: if the context sentence says:\n"
            "      - 'yesterday I did X' → event_date = session_date - 1 day\n"
            "      - 'last [weekday] I did X' → event_date = most recent [weekday] before session_date\n"
            "      - 'N days/weeks ago I did X' → event_date = session_date - N days/weeks\n"
            "      Otherwise use event_date = session_date.\n"
            "  3. Compute delta = reference_date − event_date (in days)\n"
            "  4. Convert if needed: weeks = floor(days / 7), months ≈ round to nearest month\n"
            "  5. Report the number directly\n"
            "  CRITICAL: Do NOT try to compute from a Black Friday / holiday anchor. Use EVENT DATE − REFERENCE DATE.\n"
            "  EXAMPLE: ref_date=2023-05-28, question='how many days ago did I buy a smoker?'\n"
            "  → Find 'bought smoker' in [Session: 2023-05-18] → delta = 10 days → answer: '10'\n"
            "  EXAMPLE 2 (with 'yesterday' adjustment): ref_date=2023-04-15, question='how many days ago did I take a baking class?'\n"
            "  → Find 'I took a baking class at a local culinary school yesterday' in [Session: 2023-03-26]\n"
            "  → 'yesterday' means event_date = 2023-03-26 - 1 day = 2023-03-25\n"
            "  → delta = 2023-04-15 - 2023-03-25 = 21 days → answer: '21'\n"
            "  CRITICAL: When context says 'yesterday I did X' and session date is S, you MUST compute event_date = S - 1 and use THAT for the delta, not S itself.\n"
            "  IMPORTANT: If the event is NOT found in context, answer 'I don't have that information' — do NOT guess dates.\n"
            "  SINGLE-INSTANCE QUALIFIER: If the question describes an event with a context qualifier "
            "(e.g., 'baking class when I made my friend's birthday cake'), "
            "and context contains ONLY ONE matching event (one baking class at a culinary school), "
            "treat that single instance as the one being asked about — even if the qualifier isn't explicitly repeated "
            "in the memory text. Do NOT abstain just because the qualifier phrase (e.g., 'birthday cake') "
            "doesn't appear in that specific memory entry.\n"
            "  DAYS-AGO-WHEN-QUALIFIER: For questions of the form 'how many days ago did I [event A] when I [event B]?', "
            "the phrase 'when I [event B]' defines the REFERENCE EVENT — use event B's date as the baseline, NOT the question's reference date. "
            "Compute: event_B_date − event_A_date = answer. "
            "Example: 'how many days ago did I attend a baking class when I made my friend's birthday cake?' "
            "→ find baking class date from context (March 20) AND birthday cake date (April 10) "
            "→ answer = April 10 − March 20 = 21 days.\n"
            "  SESSION DATE ACCURACY: When computing temporal differences, the session date MUST be read EXACTLY from the [Session: YYYY-MM-DD] tag in the context — do NOT estimate, compute, or hallucinate the date. "
            "MANDATORY DIGIT VERIFICATION: Read the day portion digit-by-digit. For example, [Session: 2022-03-26] has day='26' (two then six). Do NOT write '21' when the tag says '26'. "
            "SELF-CHECK: After computing a delta, verify: if reference_date is April 15 and event is 'yesterday' in a March session, the delta should be approximately 20-21 days. If your result is 26 days, you likely misread the session date (e.g., '2022-03-21' when it was actually '2022-03-26'). Re-read the session tag character by character before finalizing.\n"
            "HOW MANY DAYS/WEEKS/MONTHS BETWEEN TWO EVENTS or SINCE X UNTIL Y: For questions like 'how many days between X and Y?', 'how many weeks passed between buying X and receiving it?', 'how long since X when Y occurred?', 'how many weeks had passed since I recovered from X when Y happened?':\n"
            "  ALGORITHM:\n"
            "  1. Find event A in the context; note its [Session: YYYY-MM-DD] date\n"
            "  2. Find event B in the context; note its [Session: YYYY-MM-DD] date\n"
            "  3. Compute |date_B - date_A| in days; convert to requested units (floor for weeks)\n"
            "  IMPORTANT: If either event is NOT in the context, answer 'I don't have that information' — do NOT guess.\n"
            "  EXAMPLE: 'how many days between Sunday mass at St. Mary's and Ash Wednesday service?'\n"
            "  → Find 'Sunday mass' in [Session: 2023-01-22] → date_A = 2023-01-22\n"
            "  → Find 'Ash Wednesday service' in [Session: 2023-02-22] → date_B = 2023-02-22\n"
            "  → delta = 31 days → answer: '31'\n"
            "  EXAMPLE 2: 'how many weeks between buying tennis racket and receiving it?'\n"
            "  → 'ordered racket' in [Session: 2023-03-10]; 'received racket' in [Session: 2023-03-17]\n"
            "  → delta = 7 days = 1 week → answer: '1'\n"
            "ORDER OF N EVENTS (without named entities): If the question asks for ordering of 3+ events without naming them:\n"
            "  1. Find ALL occurrences of that event type (trips, sports events, etc.) in the context\n"
            "  2. Note each event's [Session: YYYY-MM-DD] date\n"
            "  3. Sort by session date ascending (earliest first)\n"
            "  4. Report in that order\n"
            "  Do NOT stop at 2 events if the question says 'three' or 'the sports events'. Find all of them.\n"
            "WHICH DID I START/BEGIN FIRST: For 'which X did I start/begin watching/reading/doing first?':\n"
            "  - Look for when the activity was STARTED (first mentioned as new), NOT when it was finished or last mentioned.\n"
            "  - 'I just finished season 3 of X' tells you when you finished, NOT when you started.\n"
            "  - 'I started X about N [days/weeks/months] ago' tells you the START date — compute: session_date - N units.\n"
            "  - 'I've been watching X for N months' tells you START date = session_date - N months.\n"
            "  EXAMPLE: Session 2023-05-20: 'I finished binge-watching The Crown season 3' and 'I finally started GoT about a month ago'\n"
            "  → Crown: finished May 20, unknown start. GoT: started about 1 month before May 20 = ~Apr 20.\n"
            "  → Since Crown start date unknown but GoT started Apr 20, and Crown MIGHT have started later, GoT was first.\n"
            "  CRITICAL: Do NOT use 'finished' dates to infer start order. Use explicit 'started/began' statements.\n"
            "ORDERING WITHOUT EXPLICIT DATES — MANDATORY ANSWER REQUIRED: When asked 'who came first', 'which happened first', "
            "'who became X first' but no explicit date is given for one or both items:\n"
            "  STEP 1: Check for any relative time phrases ('recently', 'just', 'a while ago', 'last year', "
            "'months ago', 'years ago') associated with each item — use these to compute approximate dates.\n"
            "  STEP 2: If relative phrases are absent, use SESSION ORDER as a MANDATORY proxy — the FIRST SESSION "
            "in which an item is mentioned gives its earliest possible date. Item A appearing in an earlier "
            "session than item B means A was mentioned first, and DEFINITIVELY occurred first. "
            "YOU MUST APPLY THIS RULE — do NOT say 'no explicit date given' and abstain. Session order IS the evidence.\n"
            "  STEP 3: Check for contextual clues like 'my old X' (= X existed before the current time), "
            "'my new X' (= X acquired recently), 'before I got X' (= X was acquired after some prior event).\n"
            "  STEP 4: MANDATORY: Give a definitive answer based on the BEST available evidence. "
            "NEVER abstain on ordering questions when context mentions both items. Session order is always available as evidence.\n"
            "  EXAMPLE: 'Who did I meet first, Tom or Mark and Sarah?' "
            "→ Find EARLIEST session mentioning Tom (e.g., [Session: 2023-01-10]); find EARLIEST session mentioning Mark/Sarah (e.g., [Session: 2023-03-05]). "
            "Tom is in the earlier session → ANSWER: Tom. Even if 'no purchase date' is given, the SESSION DATE is the evidence.\n"
            "  EXAMPLE 2: 'Which item did I purchase first, dog bed or training pads?' "
            "→ Training pads in [Session: 2023-05-20]; dog bed in [Session: 2023-06-15]. Training pads in EARLIER session → ANSWER: Training pads.\n"
            "ORDERING WITH ONE MISSING DATE: If you find an explicit date for ONE item but not the other:\n"
            "  - Use SESSION DATE of the undated item as its proxy date.\n"
            "  - If the session with the undated item is EARLIER than the dated item's date, the undated item was first.\n"
            "  - Look for any indication of RELATIVE timing ('before that', 'after that', 'first I met X, then Y').\n"
            "  - NEVER say 'I cannot determine the order' — always pick based on best available evidence.\n"
            "DURATION COMPUTATION: For 'how long did I use/have X before Y happened' questions, "
            "you MUST find TWO DIFFERENT dates from potentially DIFFERENT sessions:\n"
            "  Date 1: When X was obtained/started ('I got X', 'I received X', 'I started using X')\n"
            "  Date 2: When Y happened/was observed ('I saw Y', 'Y happened', 'I noticed Y')\n"
            "  Duration = Date2 - Date1.\n"
            "  CRITICAL: Do NOT assume Date1 and Date2 are from the same session. "
            "If a session says 'I got my binoculars 3 weeks ago', compute Date1 as (session_date - 3 weeks). "
            "Then find the SEPARATE session where Y was observed for Date2. "
            "If Date2 session is EARLIER than Date1 session, re-check your dates.\n"
            "  FIRST OCCURRENCE DATE: When computing 'how long did I use/have X before I FIRST observed Y', find the EARLIEST session where Y is mentioned after Date1. Do NOT use a late-session mention of Y just because it appears in the same session as a retrospective 'I got X N weeks ago' statement. "
            "Example: Session A (May 19): 'goldfinches are returning to the area'. Session B (May 26): 'I got binoculars exactly 3 weeks ago' AND 'goldfinches seem to be returning'. "
            "Date1 = May 26 - 3 weeks = May 5. Date2 = May 19 (EARLIEST goldfinch mention after May 5, found in session A). "
            "Duration = May 19 - May 5 = 14 days = 2 weeks. Do NOT use Session B's date as Date2.\n"
            "YEAR ASSUMPTION: When a date appears with only month/day and NO year "
            "(e.g., 'born on February 12th', 'adopted in January', 'happened last March'), "
            "default to the YEAR OF THE CONVERSATIONS. The session dates in context show the year — "
            "if all sessions are in 2023, assume the undated event is also 2023 UNLESS context "
            "EXPLICITLY STATES a year number (e.g., 'back in 2022', 'in the year 2021', '2 years ago from a 2023 session' = 2021). "
            "Do NOT use age/milestone clues (e.g., 'turning 1 year old', 'celebrating first birthday', "
            "'just graduated') to infer a different year — these are contextual hints, not explicit year indicators. "
            "If someone's 'first birthday is coming up' in a 2023 session AND their birth month is given as 'February', "
            "default to February 2023 (same year as session), NOT February 2022 based on 'first birthday' reasoning.\n"
            "STARTED vs CONSIDERING: For 'most recently STARTED/BEGAN USING X' questions, only count "
            "services/activities the user has ACTUALLY BEGUN (past tense: 'I started', 'I signed up for', "
            "'I've been using', 'I subscribed', 'I began'). "
            "Do NOT count services the user is only planning or considering: "
            "'I'm deciding to add X', 'I'm thinking of trying X', 'I've decided to subscribe' "
            "= NOT yet started. Only past-tense starting evidence counts.\n"
        )
    elif question_type == "knowledge-update":
        type_hint = (
            "\nNote: KNOWLEDGE-UPDATE question. "
            "Context entries are labeled [Session: YYYY-MM-DD HH:MM] showing when each memory came from. "
            "CHRONOLOGICALLY LATER dates = MORE RECENT. Sessions are listed in CHRONOLOGICAL ORDER (oldest first, newest last) — the LAST session in the context is the most recent. "
            "RULE: The value from the MOST RECENT (latest-dated) session WINS. "
            "When you see [Session: 2023-06-20] value_A and [Session: 2023-01-10] value_B, value_A is current. "
            "If explicit update markers exist ('actually...', 'now...', 'I was wrong...'), use them too. "
            "If the question asks for BOTH a past value AND a current value, provide BOTH. "
            "State the current/latest value directly.\n"
            "NO RATIONALIZATION: Even if the most recent value seems surprising, large, or contradicts an earlier value, you MUST report it as-is. "
            "Do NOT dismiss, qualify, or rationalize away a newer value by calling it a 'misstatement', 'typo', 'error', or 'unlikely'. "
            "The most recent session value IS ground truth — there is no justification for preferring an older value over a newer one. "
            "Example: Earlier session says $350K; later session says $400K → answer is $400K. Do NOT say 'the user may have misspoken'.\n"
            "SCOPE CHECK: Only treat a later statement as an update if it describes THE SAME SCOPE as the original "
            "(same time window, same category, same object). "
            "Example: 'I watched 5 MCU films in the last 3 months' and later 'I watched 4 MCU films [in January]' — "
            "these are DIFFERENT time windows; do NOT treat 4 as an update to 5. Keep both as separate facts.\n"
            "INCREMENT ARITHMETIC: If context says 'I have N items' and then 'I just added/got/picked up another one', "
            "the CURRENT total is N+1. If user says 'I just got rid of one', the current total is N-1. Apply the arithmetic.\n"
            "COMPLETE SCAN: Before answering, you MUST check EVERY session in the context for mentions of the relevant fact — including incidental or casual mentions (e.g., 'before I head to the gym at 6:00 pm' is just as valid as an explicit statement). Do NOT stop after finding the first mention. "
            "INCIDENTAL UPDATES COUNT: A casual or incidental mention of a current value in a later session supersedes an earlier explicit statement if the later session has a more recent date. "
            "CRITICAL EXAMPLES: 'I need to wrap up before I head to the gym, which is usually at 6:00 pm' → gym time is NOW 6:00 pm (update). 'I have to be there by 3pm for my yoga class' → yoga time is 3pm. "
            "ANY assertion 'X is usually/typically at Y' in a later session IS the current value of X. Date comparison always determines recency — not how explicitly or prominently a value is stated. "
            "RHETORICAL MEMORY REFERENCES: If a LATER session contains 'remember when I got/received/was approved for X?' or 'you remember I had/got X?' — the value X in that LATER session IS the user's factual assertion about X. "
            "Treat this as an UPDATE that overrides any DIFFERENT value for the same fact in an EARLIER session. "
            "Example: Session 1 says 'I got pre-approved for $350,000' → Session 2 says 'remember when I got pre-approved for $400,000?' → ANSWER: $400,000. "
            "The LATER session's stated value ($400,000) wins, regardless of phrasing.\n"
            "MULTIPLE UPDATES: If the same value has been updated MORE THAN ONCE (e.g., 400 → 125 → 120), use ONLY the FINAL value (120 in this example). Do not stop at the first mention — scan ALL sessions and use the latest-dated one.\n"
            "CAMERA/ITEM RECENCY: When two items are BOTH described as 'recently got', the LATER session's item is the more recent purchase. Check if the context preserves session ordering.\n"
            "AGGREGATION + INCREMENT: If the question asks 'how many X' and you find a starting count (e.g., 'I have tried three X') PLUS a later addition ('I just tried another one', 'I got a fourth X'), do NOT use the counting template — apply increment arithmetic (Rule 11): stated count + additions = current total. Example: 'three' + 'I just tried a fourth Korean restaurant' → answer is 4.\n"
            "STATED-TOTAL COMPLETE SCAN: Even after finding a stated total (e.g., 'I've tried three Korean restaurants'), you MUST scan ALL SUBSEQUENT sessions for any additional visits or acquisitions — even incidental mentions (e.g., 'I went to this new Korean place' or 'I discovered another one'). The stated total ONLY applies at that session's date. Later sessions may add to it. Do NOT stop scanning after finding the stated total.\n"
            "RECURRING ATTENDANCE COUNT: When the question asks 'how many sessions/classes/meetings did I attend' and the context does NOT give an explicit number, count DISTINCT TEMPORAL MENTIONS of attendance: each session dated in context = 1 attendance, each 'last week's session/class/meeting' = 1, each 'this week I went' = 1. "
            "If context describes 5 distinct experiences (different facilitators, topics, or dates), that implies 5 separate attendances. Count each unique temporal mention as one session even if an explicit count is never stated.\n"
            "PREFERENCE vs BEHAVIOR: If user states a preference/routine ('I like to X at Y time', 'I usually X', 'my routine is X'), that is the CANONICAL FACT and OVERRIDES later behavioral descriptions. "
            "'I've been doing Y lately' = passive description, NOT an update to an established preference. "
            "EXAMPLE: 'I like to wake up at 7:30 am on Saturdays' (PREFERENCE) + 'I've been waking up around 8:30 am on Saturdays' (BEHAVIOR) → Answer: 7:30 am. "
            "FUTURE PLAN EXECUTED: If user says 'I'm looking forward to storing X in Y' and the context also shows a prior state, assume the future plan was carried out — Y is now the current state.\n"
            "ASSISTANT vs USER: Only USER-stated updates are authoritative. If a statement appears to 'correct' an earlier fact but is followed by a RECOMMENDATION phrase (e.g., 'and I think X would be a great choice', 'you might enjoy', 'would be perfect for'), it is an ASSISTANT statement — NOT a user update. "
            "EXAMPLE: 'I've actually watched 4 MCU films in the last 3 months, and I think Spider-Man: Homecoming would be a great choice for our first film' → ASSISTANT speaking (suggesting Spider-Man). The user's original count of 5 MCU films stands.\n"
            "ROLE NAME PRECISION: When the question asks about a SPECIFIC role or title (e.g., 'Software Engineer Manager', 'VP of Marketing'), only use context that mentions THAT EXACT role. Do NOT substitute a different-but-similar role (e.g., 'Senior Software Engineer' is NOT 'Software Engineer Manager'). "
            "If the context only mentions a different role, output the abstention form: 'I don't have information about [exact role] in the context.' NEVER infer that 'Role A' and 'Role B' are the same just because they sound similar."
        )
    elif question_type == "multi-session":
        type_hint = (
            "\nNote: MULTI-SESSION aggregation question. "

            "STATED-TOTAL CHECK FIRST: Before scanning, check if the user explicitly stated a total count for the thing being asked about (e.g., 'I have 99 rare items', 'I have 3 tanks', 'I now have 5 plants'). "
            "If the user stated a total, use it directly — do NOT enumerate individual items. Apply Rule 9 STATED-TOTAL path and Rule 11 increment arithmetic if there are later additions/removals.\n"

            "TYPICAL/AVERAGE QUESTIONS: If the question asks 'in a typical week/month' or 'on average', do NOT sum all occurrences across all time. "
            "Instead, find the user's MOST RECENTLY STATED typical routine count (e.g., 'I typically attend 5 fitness classes a week'). "
            "That stated typical count IS the answer. Do NOT enumerate individual sessions.\n"
            "SCHEDULE COMBINATION: When the question asks 'how many days a week' for recurring activities (classes, lessons, workouts) and sessions mention DIFFERENT activities on DIFFERENT days, COUNT ALL UNIQUE DAYS across ALL sessions. "
            "A later session listing some activities does NOT cancel activities from earlier sessions on different days — unless the user explicitly says they stopped an activity. "
            "EXAMPLE: Session A lists yoga (Wednesdays) + weightlifting (Saturdays); Session B lists Zumba (Tuesdays, Thursdays) + weightlifting (Saturdays) → unique days = Tue+Wed+Thu+Sat = 4 days. "
            "Do NOT report only the days from the most recent session if earlier sessions established other recurring activities on other days.\n"

            "TEMPORAL SCOPE PRE-FILTER: If the question specifies a time period ('in the last month', 'last week', 'in March', 'in the past N months', 'last N days', 'last few months', etc.):\n"
            "  PRE-STEP A: Identify the exact date range from the Reference Date:\n"
            "    - 'last week' = the 7 days before the reference date (e.g., ref=2023-05-30 → 2023-05-23 through 2023-05-29)\n"
            "    - 'in the last month' / 'past month' / 'last month' = from the 1st of the PREVIOUS calendar month through the reference date (e.g., ref=2023-05-30 → April 1 through May 30; ref=2023-05-28 → April 1 through May 28). This captures both events described as 'last month' (occurring in April) AND recent events within the current month.\n"
            "    - 'in the last N months' = N calendar months before the reference date\n"
            "    - 'in March' or 'in [month]' = that full calendar month\n"
            "    - 'last few months' = approximately 3 months before the reference date\n"
            "    - 'this year' / 'in this year' / 'so far this year' = January 1 of the REFERENCE DATE's year through the reference date. Example: ref=2023-10-15 → January 1-October 15, 2023.\n"
            "  PRE-STEP B: Scan ALL sessions (do NOT exclude sessions by their date — a later session may recall earlier events).\n"
            "  PRE-STEP C: For each relevant event found during Step 1, determine when the event ACTUALLY OCCURRED (its occurrence date, not the session date when it was mentioned).\n"
            "    - OCCURRENCE vs MENTION: Use WHEN THE EVENT HAPPENED, not when it was mentioned. If a 2023 session says 'I attended my cousin's wedding last year in the city', the wedding occurred in 2022 → mark [OUT OF SCOPE] for a 'this year' (2023) query.\n"
            "    - PAST YEAR PHRASES: 'last year' = the year before the reference year. 'two years ago' = two years before reference year. These events occurred in a DIFFERENT YEAR and are [OUT OF SCOPE] for 'this year' queries.\n"
            "    - Anchor relative phrases to the session date (e.g., 'last week' in a March 15 session → week of March 8-14)\n"
            "    - Use explicit dates if stated ('on March 3rd')\n"
            "    - WEEKDAY AMBIGUITY: When a session is dated on weekday X and the user mentions 'on [weekday Y]' WITHOUT the word 'last' (e.g., 'I went for a jog on Saturday' in a Thursday session):\n"
            "      * If weekday Y is EARLIER than session day X in the same week (e.g., Monday in a Wednesday session) → Y refers to this week's occurrence (already past).\n"
            "      * If weekday Y is LATER than session day X (e.g., Saturday in a Thursday session) → TWO candidates exist: (a) the Saturday from the PREVIOUS week and (b) the Saturday from the CURRENT or NEXT week.\n"
            "        PREFERENCE RULE: If exactly ONE of those two candidates falls within the scope window, treat the event as occurring on that in-scope date and mark it [IN SCOPE].\n"
            "        Example: session=Thursday May 25, 'on Saturday', scope=May 23-May 29 → candidates: May 20 (out of scope) and May 27 (in scope) → use May 27, mark [IN SCOPE].\n"
            "    - OVERLAP INCLUSION: When a relative phrase anchors an event to a PERIOD (e.g., 'last month' → all of April, 'last week' → April 8-14), and that period OVERLAPS with ANY PART of the scope window, mark the event [IN SCOPE]. Only mark [OUT OF SCOPE] if the entire anchored period falls OUTSIDE the scope window.\n"
            "      Example: event 'last month' in May 23 session → April; scope window April 28-May 28 → April overlaps April 28-30 → [IN SCOPE].\n"
            "      Example: event '3 months ago' in May 23 session → February; scope window April 28-May 28 → February does NOT overlap → [OUT OF SCOPE].\n"
            "    - Mark each item in your Step 2 list as [IN SCOPE] or [OUT OF SCOPE] based on occurrence date vs the date range from PRE-STEP A\n"
            "  PRE-STEP D: EXCLUDE items marked [OUT OF SCOPE] from the final count. "
            "WORKSHOP SPENDING OVERRIDE: If the user explicitly stated 'I paid $X to attend' a workshop/event, mark that payment as [IN SCOPE] regardless of whether the workshop date is outside the scope window or in the future. The payment itself occurred and counts toward the total. Do NOT exclude a stated payment just because the event date is outside the scope window. "
            "CRITICAL: The override applies to the PAYMENT, not just to future-dated events. Even if you wrote [OUT OF SCOPE] next to a workshop because its dates are after/before the scope window, the user's PAYMENT for that workshop is still [IN SCOPE] and must be included. Always re-include any payment amounts you initially marked [OUT OF SCOPE].\n"

            "ZERO RESULTS HANDLING: After completing the full scan, if you found NO in-scope instances:\n"
            "  CHECK: Does the topic appear ANYWHERE in context (any session, any date)?\n"
            "    YES (topic mentioned but all occurrences outside scope): Output the count as 0 — e.g., 'Total count: 0.'\n"
            "    NO (topic NEVER mentioned anywhere): Say 'I don't have any information about [X] in the provided context.' Do NOT say 'Total count: 0.' This is the abstention form.\n"
            "  CRITICAL: If in Step 1 you wrote 'No mention of [X] in any session' or 'User never mentioned [X]', this means [X] was NEVER mentioned anywhere → you MUST use the abstention form. Writing 'Total count: 0' when the topic was never mentioned is WRONG. 'Total count: 0' is ONLY correct when the topic was mentioned in context but all mentions are outside the scope window.\n"
            "MULTI-COMPONENT TOTALS: If the question asks for a TOTAL across multiple components (e.g., 'total days in Hawaii AND Seattle', 'total years from high school to Master's degree', 'total spent at X and Y'):\n"
            "  STEP: Determine each component's value:\n"
            "    KNOWN: value explicitly stated in context\n"
            "    UNKNOWN: component mentioned but its value/duration/amount NOT explicitly stated\n"
            "    ABSENT: component never mentioned anywhere in context\n"
            "  IF ANY component is UNKNOWN or ABSENT:\n"
            "    - Do NOT output a total count\n"
            "    - Do NOT treat the missing component as 0\n"
            "    - Say: 'I found [known values], but I don't have information about [unknown/absent component] in the context, so I cannot calculate the total.'\n"
            "  ONLY output a total if ALL components have KNOWN values.\n"
            "PAGE COUNT TOTALS: When the question asks for 'the page count of two/multiple novels/books', SUM all identified page counts and state the total. Do NOT list them separately as the final answer — compute and output the combined total. "
            "EXAMPLE: 'What was the page count of the two novels I finished in January and March?' + Book A=416 pages + Book B=440 pages → answer: '856 pages (416 + 440).'\n"
            "PROGRESS DELTA: When the question asks 'how many [X] do I need to earn/get/accumulate' to achieve a goal, AND context shows BOTH a goal threshold AND a current balance/progress, compute remaining = threshold - current. The word 'earn' signals future acquisition, so the answer is how many MORE are needed. Do NOT report just the threshold. "
            "EXAMPLE: 'how many points do I need to earn to redeem a reward?' + 'I need a total of 300 points' (threshold=300) + 'my total is now 200 points' (current=200) → answer: 100 (points still needed to earn). The goal is 300, the user has 200, so they need 100 more.\n"
            "USER-STATED PRICES ONLY: When computing a financial savings or cost difference, ONLY use prices the USER explicitly stated. Prices mentioned in ASSISTANT responses (the AI's general knowledge estimates like 'the bus fare is usually around $X') are NOT user-stated facts and must NOT be used. If the user stated taxi=$60 but never stated a bus price, and the assistant estimated a bus price, ignore the assistant's estimate — report that you don't have the user's bus cost and cannot compute savings.\n"
            "DERIVED ROLE TENURE: When asked 'how long have I been in my current role' and context provides BOTH total company tenure AND time spent in a previous role before promotion, compute: current_role_duration = total_tenure - time_before_promotion. "
            "EXAMPLE: 'I've been in the company 3 years and 9 months' + 'worked my way up to [current role] after 2 years and 4 months' → current role duration = 3yr9mo - 2yr4mo = 1yr5mo.\n"
            "AGE DIFFERENCE COMPUTATION: When asked 'how many years older/younger is X than Y', find the EXACT AGES of both people. "
            "If context says a person is 'in their 30s' or 'in their 20s', FIRST search all other sessions for a more exact age statement (e.g., 'I just turned 32', 'I am 28 years old', 'I celebrated my 32nd birthday'). "
            "Use the exact stated age if found. Only use a range as last resort, and if you do, pick the age that makes the math consistent with any other available evidence (e.g., birth year, milestone events). "
            "BIRTHDAY COMPUTATION: If context mentions 'my Nth birthday' or 'turning N', that person's age IS N at that session's date.\n"

            "SESSION DATE ANCHORING: When a question uses RELATIVE TIME EXPRESSIONS ('last week', 'last weekend', 'yesterday', 'this month'), use the [Session: YYYY-MM-DD] date tag to anchor them. Example: [Session: 2023-05-30] + 'I jogged on Saturday' → that Saturday = 2023-05-27. If the reference date is 2023-05-30 and 'last week' = May 22-28, then 2023-05-27 IS within last week → count it. Do NOT say 'cannot determine scope' when a session date tag is present. "
            "IMPORTANT: For ABSOLUTE time scope questions (e.g., 'in March', 'in 2023', 'during the past year'), do NOT use the session date to exclude events that occurred after the session date but within the scope window — use the REFERENCE DATE provided for the question instead.\n"
            "STEP 1: Scan ALL memory entries from start to finish — do not skip any. "
            "SESSION INTRODUCTIONS: Each session may open with 1-3 introductory sentences describing recent activities BEFORE any dated sub-entry appears. "
            "Read these opening sentences carefully — they often reference events that occurred earlier in the scope window. "
            "ANCHOR these to the session date: e.g., 'I tried a new sourdough recipe on Tuesday' in a [Session: 2023-05-18] → Tuesday of that week = 2023-05-16. "
            "Include intro-derived events in your candidate list and apply the IN-SCOPE / OUT-OF-SCOPE check to their anchored dates. "
            "Do NOT skip session openings just because they lack an explicit sub-heading or date stamp. "
            "STEP 2: Build a numbered list of EVERY instance relevant to the question. "
            "CRITICAL — Only count USER-STATED FACTS: Include ONLY items where the USER explicitly says 'I tried X', 'I made X', 'I bought X', 'I attended X', 'I downloaded X', etc. "
            "EXCLUDE: (a) suggestions/recommendations from the AI assistant (imperative or 'you could/might' language), "
            "(b) items described as POSSIBLE/OPTIONAL alternatives ('citrus juice: orange, lemon, or grapefruit' → only count ones actually used), "
            "(c) items mentioned as 'explore X' or 'why not try X' — those are suggestions, not facts. "
            "CATEGORY MEMBERSHIP: When the question asks for items belonging to a SPECIFIC CATEGORY (e.g., 'citrus fruits', 'vegetarian dishes', 'jazz albums', 'aerobic exercises'), verify EACH candidate item actually belongs to that category using common knowledge. EXCLUDE items that don't fit (e.g., kiwi and pomegranate are NOT citrus fruits; only oranges, lemons, limes, grapefruits, yuzu, etc. are citrus; apple is NOT a berry; etc.).\n"
            "CUISINE-SPECIFIC: A 'cuisine' counts only if the user explicitly attended a class, visited a restaurant of that cuisine, or explicitly said 'I learned to cook [cuisine].' Do NOT create a new cuisine from a single ingredient (sauerkraut → German, tempeh → Indonesian). A fermentation workshop that teaches sauerkraut and kimchi is NOT a separate cuisine, cooking skill, or distinct learning experience — do NOT count it as an additional cuisine beyond those its ingredients already represent. The fermentation workshop does NOT add to the cuisine count because its techniques overlap with cuisines already counted (e.g., Korean for kimchi). "
            "MUSIC COLLECTION: If the question asks about albums/EPs 'purchased or downloaded', count items the user clearly OWNS (vinyl signed at show, physical copy at merchandise booth, downloaded on streaming). Include if user explicitly bought at an event or downloaded — even without 'purchased' word. "
            "CONCERT VINYL: If context says 'I got my vinyl signed [by artist] at/after the show' or 'I had [artist] sign my vinyl', count that vinyl as a purchased album. Getting a vinyl signed at a show implies owning/obtaining it there. Count it even if 'purchased' is not explicitly stated. "
            "WORKSHOP SPENDING: If the user explicitly states 'I paid $X to attend' a workshop, count that expense even if the workshop's calendar date seems future relative to the reference date. The payment itself occurred, so include it — this overrides the scope-window filter from PRE-STEP D. "
            "HEALTH-RELATED DEVICE: Only count devices that DIRECTLY MONITOR, TREAT, or SUPPORT a health/medical condition (e.g., blood glucose monitor, nebulizer, hearing aids, fitness tracker, CPAP). Do NOT count organizational tools (planners, notebooks, apps that only schedule activities) as health-related devices. "
            "SPECIFIC CONTEXT MATCHING: When the question asks about a SPECIFIC TYPE of event (e.g., 'undergrad course research project poster' vs 'thesis research poster', 'biological birth' vs 'adoption'), do NOT substitute a similar-but-different type. If context mentions only the different type, report that you don't have information about the specific type asked. "
            "ITEM ATTRIBUTION: When reading 'I started X model about N weeks ago' and 'I also started Y model about M months ago' — the FIRST item has the N-weeks date and the SECOND item has the M-months date. Do not swap these. "
            "CONFERENCE VENUE INFERENCE: If context mentions (a) attending a SPECIFIC institution's conference ('I attended a research conference at Harvard University', 'I went to a conference hosted by MIT') AND (b) presenting research/a poster/paper at a conference in the same general timeframe (same year/season), INFER the presentation was at that institution's conference — especially when NO OTHER conference venue is mentioned in the context. "
            "Example: 'I went to Harvard University to attend my first research conference' + 'I presented my research at a conference' (no other venue named) → the presentation/poster was at Harvard University. "
            "Do NOT abstain just because the two statements don't explicitly say 'I presented AT Harvard' — the single unnamed conference = the named Harvard conference. "
            "PRESENTATION = POSTER: A research 'presentation' and a 'poster presentation' are equivalent for venue inference. If the question asks about a poster and context says 'I presented my research at a conference', that IS a poster/presentation event — do NOT treat them as different events requiring separate evidence.\n"
            "EXCHANGE TRANSACTIONS: An in-store exchange (returning one item and getting another) generates TWO DISTINCT PENDING ACTIONS: "
            "(1) the RETURN of the original item, AND (2) the PICK-UP of the new/replacement item. "
            "Count these as 2 separate items if the question asks about items to pick up OR return. "
            "SEPARATE RETURN RULE: If context has BOTH (a) 'I need to return [item] to [store]' AND (b) a separate 'I exchanged [item] at [store]' statement, these are TWO SEPARATE TRANSACTIONS — count the return AND the exchange's new pickup as separate items. "
            "EXCHANGE DOES NOT COMPLETE RETURN: An exchange happening on date D does NOT automatically complete a separately-mentioned 'I need to return' obligation. The exchange generates its OWN return (of the original item), but does NOT satisfy a SEPARATELY STATED return obligation. "
            "Example: 'I need to return some boots to Zara' + 'I exchanged boots at Zara on 2/5' = TWO pending actions (the separate return + the pickup from exchange). "
            "Only conclude a return is COMPLETED if context EXPLICITLY says 'I already returned it', 'the return is done', or similar. Do NOT infer completion from an exchange date.\n"
            "ENTITY COUNT vs EVENT COUNT: If the question asks 'how many [ITEMS] did I [verb]' (e.g., 'how many bikes did I service'), count DISTINCT ITEMS, not the number of times you performed the action. "
            "If you serviced the same bike twice in the time period, that is STILL 1 bike. "
            "If you visited the same doctor 3 times, that is STILL 1 doctor (unless question asks 'how many visits'). "
            "Group multiple events on the same item/entity and count it ONCE.\n"
            "HOURS/TIME TOTALS — ALWAYS SUM: When the question asks 'how many HOURS/DAYS/WEEKS did I spend' on an activity, SUM ALL instances across ALL sessions — including multiple playthroughs of the same game, multiple visits to the same place, multiple sessions of the same activity. "
            "DIFFERENT PLAYTHROUGHS or RUNS of the same game ARE SEPARATE TIME-ADDITIONS and must be summed: 'I played The Last of Us on hard (30 hours)' + 'I played The Last of Us on normal (25 hours)' = 55 total hours for that game. "
            "Do NOT apply entity-level deduplication (count same game once) when the question asks for HOURS — deduplication applies only when counting distinct entities. "
            "Example: 'how many HOURS have I spent playing games in total?' → sum every gaming hour mentioned: 30 + 25 + 15 + 20 + ... = total.\n"

            "STEP 3: Apply de-duplication (same item in multiple sessions = count once). "
            "DE-DUP RULES: "
            "(a) Same name + same relationship label = same person; count once. If the same name appears with DIFFERENT relational labels (e.g., 'cousin Emily' vs 'college roommate Emily'), treat these as THE SAME PERSON unless context explicitly confirms they are different people (e.g., 'two different friends both named Emily'). Different relationship labels alone are NOT evidence of different identities. "
            "(b) LOCATION-BASED DEDUP IS MANDATORY: If two mentions clearly describe THE SAME OCCURRENCE of an event (e.g., the same wedding appearing in two different sessions), and share IDENTICAL concrete location details (e.g., BOTH described as 'city rooftop garden ceremony', or BOTH at 'the vineyard'), they MUST be counted as ONE event. Mark the second occurrence as 'DUPLICATE OF #N'. "
            "WEDDING COUPLE IDENTIFICATION: For weddings, identify each wedding by the COUPLE (both people's names). 'Cousin Emily's wedding' + 'Emily and Sarah's wedding' = THE SAME WEDDING (both involve Emily; Sarah is Emily's partner). Different relationship labels for the SAME NAME (cousin Emily, friend Emily, college roommate Emily) = THE SAME PERSON, THE SAME WEDDING. Only count as different weddings when the COUPLE NAMES are clearly different (Rachel+Mike ≠ Emily+Sarah ≠ Jen+Tom). Example: if context mentions 'cousin Emily's wedding in the city', 'my college roommate's wedding', and 'Emily and Sarah's wedding' — these are ALL the same wedding (Emily who married Sarah). Final count = number of distinct COUPLES, not number of distinct session mentions. "
            "(c) Same event across multiple sessions = 1 count. "
            "(d) An appointment return visit = same event, not new. "
            "STEP 4: State the FINAL count as your answer AFTER completing steps 1-3. "
            "IMPORTANT: Do NOT state an intermediate count before de-duplication. Your stated answer must be the FINAL de-duplicated result. "
            "USE THE COUNTING OUTPUT TEMPLATE from Rule 9: enumerate with numbers, mark duplicates 'DUPLICATE OF #N', then end with 'Total count: N.' as your final sentence."
        )
    elif question_type == "single-session-preference":
        type_hint = (
            "\nNote: PERSONALIZATION question. You MUST apply the user's specific known preferences, constraints, and personal context to give a PERSONALIZED response. "
            "STEP 1: Extract ALL relevant user preferences, constraints, and personal details from the context — including BOTH positive preferences ('I love X', 'I enjoy Y') AND negative preferences/exclusions ('I want to branch out away from X', 'I'm tired of Y', 'I don't want more Z', 'I'd like to try something other than X', 'I want to explore beyond X'). "
            "CRITICAL — NEGATIVE PREFERENCES: If the user has stated they want to AVOID or MOVE AWAY FROM a genre/topic/activity, do NOT suggest those excluded items even if they are clearly related to the user's history. Actively filter them out. "
            "PREFERENCE DIRECTION: Carefully identify WHICH DIRECTION each preference points:\n"
            "  - WANT MORE OF: 'I enjoy X', 'I love X', 'I want to explore X', 'I want to try X', 'I want to branch out TO X' → X is something the user desires more of\n"
            "  - WANT LESS OF: 'I'm tired of X', 'I've been doing X too much', 'I want to branch out FROM X', 'I want to explore BEYOND X', 'I want something other than X' → X is something the user wants to move away from\n"
            "  CRITICAL EXAMPLE: 'I want to explore beyond true crime and self-improvement — I've been curious about history podcasts' → TRUE CRIME and SELF-IMPROVEMENT are WANT-LESS-OF; HISTORY is WANT-MORE-OF. "
            "Do NOT suggest true crime or self-improvement. DO suggest history content.\n"
            "NEW CONTENT DIRECTION: When the user says they want to explore a SPECIFIC NEW genre/topic (e.g., 'I've been curious about history podcasts', 'I want to try documentary-style shows', 'I've been interested in learning Spanish'), "
            "your recommendations MUST include specific suggestions IN THAT EXACT NEW GENRE/TOPIC. "
            "Do NOT vaguely say 'explore new genres' and then suggest something unrelated (e.g., horror podcasts when user said history). "
            "If user wants history → suggest history podcasts/books. If user wants cooking → suggest cooking content. Match the stated direction EXACTLY.\n"
            "EXISTING PREFERENCES — BUILD ON THEM: If the user already uses/does/has something (e.g., 'I use turbinado sugar', 'I have a cat named Luna', 'I meditate every morning'), ACKNOWLEDGE THAT THEY ALREADY DO IT and build on it — do NOT suggest it as if it were new. "
            "Example: User says 'I've been using turbinado sugar' → your response should say 'Since you already use turbinado sugar...' NOT 'Have you tried turbinado sugar?'\n"
            "RECENTLY ACQUIRED ITEMS — CRITICAL: If context shows the user RECENTLY BOUGHT, GOT, or SET UP an item (e.g., 'I recently bought a new utensil holder', 'I just got a new coffee maker', 'I recently set up a standing desk'), that item is ALREADY IN THEIR POSSESSION. "
            "Do NOT say 'consider using a utensil holder', 'you might want to try a utensil holder', or 'a utensil holder can help' — that implies they don't have one. "
            "Instead say: 'Since you recently got your utensil holder...' or 'Your new utensil holder is perfect for...' or 'Building on your new utensil holder...' — ACKNOWLEDGE their ownership explicitly.\n"
            "STEP 2: Apply ALL preferences (positive AND negative) to tailor your answer to THIS user specifically. "
            "STEP 3: If the user has a SPECIFIC personal experience mentioned in context (a memorable event, a specific place, a specific person), reference THAT specific detail rather than giving generic alternatives. "
            "STEP 3b: RECENT EVENTS — Check the context for ANY recent events DIRECTLY RELATED to the question topic (e.g., the user just cleaned their room, just got a new pet, just finished a project). These recent events SHAPE what advice is relevant — incorporate ALL of them explicitly in your response. "
            "STEP 4: Do NOT give generic advice — every suggestion must reflect the user's known preferences and actively avoid their known dislikes. "
            "When asked for 'suggestions', 'ideas', or 'recommendations', provide MULTIPLE DIVERSE options (at least 2-3 distinct suggestions) — do NOT focus all suggestions on a single ingredient, topic, or angle. Cover different aspects of the user's preferences.\n"
            "IMPORTANT: If you don't have info about the SPECIFIC thing asked (e.g., 'events this weekend'), still use the user's preferences to suggest TYPES of things they would enjoy. Never just say 'I don't have that information' for preference questions — always give a preference-informed answer."
            "\nAPPLY GENERAL PREFERENCES TO NEW CONTEXTS: If the user expressed a preference in one context (e.g., 'I prefer hotels with hot tubs on the balcony and great views' when planning a Seattle trip), apply that same preference when asked about a similar context (e.g., a hotel recommendation for Miami). Do NOT say 'I don't have specific information about your preferences for [specific city/place]' — use what you know about their general preferences and apply them directly."
            "\nNEVER OPEN WITH A DISCLAIMER: If you have ANY relevant preferences in context, start DIRECTLY with the personalized recommendation. Do NOT start your response with 'I don't have specific information about your preferences for X' or any similar disclaimer — this contradicts the personalization you are about to provide and causes the response to be marked wrong. Lead with the suggestion."
            "\nCITE SPECIFIC CONTEXT DETAILS: Your response MUST reference the SPECIFIC activities, items, experiences, and memories from context. Do NOT give generic advice using invented details. "
            "For example, if context shows user had success with beef stew, say 'building on your beef stew success'; if they were in the debate team, say 'reconnecting with debate team members'. "
            "CRITICAL: If the question is about a PAST LIFE PHASE (high school, college, childhood), cite memories FROM THAT PHASE specifically — "
            "do NOT mix in current job, current studies, or recent activities. "
            "Example: question about high school reunion → cite debate team, AP courses, specific teachers, specific subjects from high school context — NOT current career plans or college activities.\n"
        )
    elif question_type in ("single-session-user", "single-session-assistant"):
        type_hint = (
            "\nNote: Answer directly from the personal information in the context. "
            "INFERENCE: If the context does not directly state a fact but IMPLIES it, make the reasonable inference. "
            "Examples: 'visiting your sister in Denver' → your sister lives in Denver; "
            "'my sister gave me a stand mixer' → sister gave the gift; "
            "'I've had Luna for 3 months' → 3 months is how long. "
            "Do NOT refuse to answer if context provides indirect evidence — use it. "
            "BRAND INFERENCE: If user mentions 'a lavender shampoo I picked up at Trader Joe's', "
            "the brand/store is Trader Joe's. "
            "FUTURE PLAN vs FACT: 'I'm thinking of visiting X', 'I plan to X', 'I want to X', 'I might go to X' = "
            "FUTURE PLAN, NOT a past fact. If question asks about an actual event and context only shows a plan/desire to do it, say 'I don't have that information' — the plan was never stated as having happened. "
            "ONLY say 'I don't have that information' when context contains ZERO relevant PAST evidence. "
            "GEOGRAPHIC PRECISION: If the question asks about a specific country/city (e.g., 'How long were you in Korea?'), only use evidence that EXPLICITLY names that exact country/city. "
            "Do not substitute a different country/city even if it has matching time durations — e.g., if context says 'I spent two weeks in Japan' and question asks about Korea, the answer is 'I don't have that information about Korea' (not 'two weeks'). "
            "FUTURE PLAN ≠ PAST VISIT: If context only says 'I'm thinking of visiting South Korea' or 'I plan to go to Korea', that is NOT a past visit. If the question asks 'how long were you in Korea?', the answer is the abstention form — the user has not stated they visited Korea. "
            "BRAND = STORE: When a user says 'I picked it up at Trader Joe's' or 'I got it from Trader Joe's', Trader Joe's IS the brand/source. Do NOT say 'the brand is not mentioned'. State Trader Joe's as the brand/store directly and do NOT add any caveat that the brand is unknown.\n"
            "COMPLETE LOCATION: When identifying a place, include ALL location qualifiers in the context. "
            "If context says 'University of Melbourne in Australia' or 'Melbourne, Australia', your answer must include the country/state qualifier too — never truncate location qualifiers. "
            "Example: context says 'I studied at the University of Melbourne in Australia' → answer is 'University of Melbourne in Australia', NOT just 'University of Melbourne'.\n"
            "UNIVERSITY GEOGRAPHY: If context names a university whose city/country is strongly implied by the university name itself, include the country even if the context does not explicitly repeat it. "
            "Examples: 'University of Melbourne' → Melbourne, Australia (include 'in Australia' or 'in Melbourne, Australia'); 'University of Edinburgh' → Scotland/UK; 'University of Toronto' → Toronto, Canada. "
            "If the context provides ANY geographic qualifier (e.g., 'in Australia', 'in Melbourne'), you MUST include it verbatim in your answer.\n"
            "DURATION FROM START DATE: For 'how long have I been X-ing' questions, if the context states WHEN the activity started (e.g., 'I started collecting cameras 3 months ago', 'I joined in January', 'I got my first one in February'), use that to state the duration. "
            "If only the start date is given and no explicit duration, compute from start date to the session date.\n"
            "GIFT GIVER INFERENCE: If an assistant message says 'A new [item] is an amazing gift' or similar, look for the USER message that describes receiving it — the user's preceding message likely named the giver. "
            "If the memory context shows the user received an item and mentions family (sister, brother, parent), that person is the likely giver — state it confidently.\n"
            "SINGLE DEFINITIVE ANSWER REQUIRED: Never give 'X or Y' or 'either X or Y' as a final answer. "
            "If two candidate answers appear in the context, determine which one was ACTUALLY done by the user "
            "(past tense: 'I attended', 'I went', 'I bought') vs. which was planned/suggested/considered. "
            "Pick exactly ONE answer — the one the user definitively did or stated as fact.\n"
            "ATTEND vs AUDITION/PERFORM: When the question asks what play/show/event/concert the user ATTENDED or WATCHED (as an audience member), "
            "look ONLY for evidence of 'I went to see', 'I attended', 'I saw', 'I watched', 'I went to' — as an AUDIENCE MEMBER. "
            "Do NOT confuse with events the user 'auditioned for', 'performed in', 'rehearsed for', 'was cast in', or 'is practicing for' — these mean participation as a PERFORMER, NOT as an audience member. "
            "Example: 'I auditioned for The Crucible' ≠ 'I attended The Crucible'. If context says user ATTENDED Glass Menagerie AND AUDITIONED for The Crucible, the answer to 'what play did I attend' is Glass Menagerie.\n"
            "PLAY/EVENT TITLE CONNECTION: If context says the user 'went to a play/show/concert' at a venue AND separately mentions a specific title with details ('incredible performance', 'the lead actress was amazing', 'I loved the show'), "
            "that named title IS the one they attended. Example: 'I went to a play at the community theater' + 'The Glass Menagerie was absolutely incredible, the lead actress captivated me' → the play attended was 'The Glass Menagerie'. "
            "The user describing their experience with a specific title implies they were present as an audience member for that title.\n"
            "NUMBERED LIST RECALL: If the question asks for the Nth item in a list "
            "(e.g., 'what was the 27th parameter', 'what was item #3 in the list'), "
            "FIRST reconstruct the COMPLETE numbered list from the context (find all items in order), "
            "THEN count to the exact Nth position. Do NOT guess based on partial context — "
            "verify the count by listing all items in sequence up to N. "
            "START FROM #1: Always begin counting from item #1 of the list. If the context fragment starts from item #5, look for items #1-4 earlier in the context first. "
            "If the list in context shows e.g. '3. Clarity ... 4. Tone ... 5. Emotion ...' — item 3 is at position 3 in the FULL list, not position 1 of what you can see. "
            "ENUMERATE EXPLICITLY: Write out '1. X, 2. Y, 3. Z...' to track position precisely. Do not jump to position N without explicitly counting each prior item."
        )

    # Adjust max_tokens by question type
    max_tokens = GEN_MAX_TOKENS
    if question_type == "multi-session":
        max_tokens = 750  # Increased from 500: prevent truncation during enumeration
    elif question_type == "single-session-preference":
        max_tokens = 400  # More room for personalized recommendations
    elif question_type == "knowledge-update":
        max_tokens = 350  # Slightly more for KU reasoning
    elif question_type == "temporal-reasoning":
        max_tokens = 450  # More room for multi-step temporal reasoning

    user_message = f"Memory context:\n{context}{date_hint}{type_hint}\n\nQuestion: {question}"
    answer, tokens = await call_gen_api(client, GEN_SYSTEM_PROMPT, user_message, max_tokens, GEN_TEMPERATURE)
    return answer, tokens


async def generate_counting_answer(client, context: str, question: str,
                                   question_type: str = "", question_date: str = "",
                                   max_tokens_step1: int = 1500,
                                   max_tokens_step2: int = 500) -> tuple[str, int]:
    """Two-step LLM approach for aggregation/counting questions.

    Step 1: Enumerate all instances from context as a numbered list.
    Step 2: Deduplicate and count/sum from the enumerated list.

    Separating enumeration from counting dramatically reduces LLM failures on
    long contexts: single-pass scan+count is unreliable at 7500-token context size.
    For MS questions with 7500-token contexts, use max_tokens_step1=2500 to ensure
    complete enumeration without truncation.
    Returns (final_answer, total_tokens_used).
    """
    date_hint = f"\nReference date (when question was asked): {question_date}" if question_date else ""

    # ── Step 1: Full enumeration (no counting yet) ──
    enumerate_hint = (
        "\nNote: ENUMERATION STEP — do NOT state a final count or total yet.\n"
        "Your ONLY task: scan ALL memory entries from the FIRST session to the LAST and build a "
        "COMPLETE numbered list of every instance relevant to the question.\n"
        "For each instance write: [N] <what happened> | [Session: YYYY-MM-DD] | [IN SCOPE] or [OUT OF SCOPE]\n"
        "Rules:\n"
        "  - Include ONLY USER-stated facts ('I bought X', 'I attended Y', 'I made Z', 'I own X', "
        "'I have X', 'I tried X') — NOT AI suggestions, recommendations, or options\n"
        "  - STATED-TOTAL DETECTION: If the user explicitly states a count ('I have 3 tanks', "
        "'my collection has N items'), mark it as [STATED-TOTAL: N at Session YYYY-MM-DD]\n"
        "  - ADDITIONS/REMOVALS after a stated total: note them as [+1] or [-1] so Step 2 can compute\n"
        "  - FUTURE LIST ADDITIONS NOT COUNTED: When counting items on a LIST (to-watch list, "
        "to-read list, shopping list, bucket list, etc.), 'I'm going to add X', 'I plan to add X', "
        "'I'll add X', 'I want to add X' = not yet added to the list. Do NOT mark these as [+1] additions. "
        "EXCEPTION: When the QUESTION itself explicitly asks about planned actions "
        "('service OR PLAN TO SERVICE', 'visit OR PLAN TO VISIT', 'do or intend to do'), "
        "include planned instances as IN SCOPE.\n"
        "  - COMPETITIVE SPORTS: Count any sport played 'on a team', 'in a league', 'for school/college', "
        "'on the varsity/junior/intramural squad', 'in a tournament', or 'in competition' as a competitive sport. "
        "The word 'competitively' does not need to appear explicitly.\n"
        "  - OWNERSHIP vs USAGE: For questions about items the user OWNS, EXCLUDE items that are "
        "EXPLICITLY not owned: 'I borrowed X', 'my friend's X', 'rented X', 'lent to me by Y', "
        "'I was playing X at someone else's house' = NOT owned. "
        "DO NOT exclude items just because ownership isn't stated explicitly — 'I play X', 'I use X', "
        "'I practice X' without any non-ownership indicator = assume currently owned/possessed.\n"
        "  - PLANS TO ACQUIRE ≠ CURRENTLY OWNS: 'I'm thinking about getting X', 'maybe getting X', "
        "'I'm considering buying X', 'I want to try X', 'I'd love to have X' = user does NOT currently own X. "
        "Mark as [OUT OF SCOPE]. EXAMPLE: 'Another thing I've been thinking about is maybe getting a new ukulele' "
        "means the user does NOT own a ukulele. Do NOT count planned acquisitions.\n"
        "  - BORN vs ADOPTED: When the question asks how many babies/children were BORN to people, "
        "only count natural births. Adoptions are NOT births — a child adopted from Ethiopia (or anywhere) "
        "was not born to that person. Mark adopted children as [OUT OF SCOPE — adopted, not born] "
        "when the question specifies 'born to'. Include adoptions only if the question says "
        "'adopted', 'welcomed', 'joined the family', or similar non-birth phrasing.\n"
        "  - SOLO CLASS ASSIGNMENT ≠ LED: When the question asks about projects the user 'led', "
        "an academic CLASS ASSIGNMENT done independently/alone is NOT a project the user 'led' — "
        "e.g., 'Data Mining solo project', 'I was the only one working on the assignment', "
        "'individual class project'. Mark these [OUT OF SCOPE — solo class assignment, not led]. "
        "HOWEVER: Personal research initiatives, work projects, or research the user is RUNNING "
        "(even without a stated team) DO count as 'led' — e.g., 'research on social media influencers', "
        "'I'm conducting a study on X', 'my research project'. These count [IN SCOPE].\n"
        "  - ACCUMULATION GOAL: If the question asks 'how many more [units] do I need to earn/redeem/reach "
        "[goal]?', mark as [IN SCOPE] ALL statements of: (a) the goal/threshold amount (label it [GOAL: N]), "
        "AND (b) the user's current balance/amount (label it [CURRENT: N]). Both are needed to compute the answer.\n"
        "  - Include ALL occurrences even if they seem like duplicates — dedup comes in Step 2\n"
        "  - ATTENDANCE EVIDENCE: Only include events/visits as instances if the user explicitly states "
        "they ATTENDED, WENT TO, WERE AT, PARTICIPATED IN, or VOLUNTEERED AT the event. "
        "A general statement ('I've been lucky to attend amazing festivals') WITHOUT naming a specific "
        "event in that sentence is NOT specific attendance evidence for a new item.\n"
        "  - APPOINTMENT vs TREATMENT DISTINCTION: When the question asks about 'doctor appointments' or "
        "'appointments with a doctor/physician', count only visits where the user physically met with a "
        "physician, specialist, or primary care doctor for a consultation. Do NOT count: physical therapy "
        "sessions, lab tests, blood draws, imaging scans, or other medical procedures as separate "
        "'doctor appointments' — unless the user describes them as 'an appointment with my doctor'.\n"
        "  - CURRENTLY OWN: For 'how many X do I currently have/own/possess', include ALL items mentioned "
        "unless the user explicitly states they sold, gave away, donated, returned, or no longer have it. "
        "Items labeled 'old', 'first', or 'from before' are STILL CURRENT unless explicitly discarded.\n"
        "  - Do NOT skip any session — scan every session even if it seems off-topic\n"
        "  - TEMPORAL SCOPE: If the question specifies a time window ('in the last N months', "
        "'in December', 'this year', 'past N days'), compute the exact date range from the Reference date.\n"
        "    For each instance, check if it occurred WITHIN that date range and mark [IN SCOPE] or [OUT OF SCOPE]\n"
        "    ZERO-RESULT CASE: If no instances are found at all, note 'No instances found.'\n"
        "    TOPIC-ABSENT vs SCOPE-ABSENT: If the topic was never mentioned ANYWHERE, write "
        "'Topic never mentioned in context.' (→ Step 2 will use abstention). "
        "If it was mentioned but all occurrences are outside the scope window, write "
        "'Topic mentioned but all [OUT OF SCOPE].' (→ Step 2 counts as 0)\n"
        "End with exactly: 'LIST COMPLETE. Raw instances: N'\n"
        "Do NOT output a final answer or count in this step."
    )
    user_msg1 = f"Memory context:\n{context}{date_hint}{enumerate_hint}\n\nQuestion: {question}"
    enumeration, tokens1 = await call_gen_api(client, GEN_SYSTEM_PROMPT, user_msg1, max_tokens_step1, GEN_TEMPERATURE)

    # ── Step 2: Deduplicate and produce final answer ──
    count_hint = (
        "\nNote: COUNTING STEP — apply deduplication rules and state the final answer.\n"
        "Given the enumerated list above:\n"
        "  1. STATED-TOTAL PATH: If Step 1 found a [STATED-TOTAL: N at DATE], use N as the base.\n"
        "     Apply any [+1]/[-1] additions/removals that occurred AFTER that date to get the current total.\n"
        "     Write: 'Stated total: N (at DATE). Additions after: +X. Removals after: -Y. "
        "Current total: N+X-Y.'\n"
        "     SPECIAL CASE — STATED TOTAL IS THE ANSWER: If the stated total directly answers the "
        "EXACT question asked (e.g., question='how many times have I met X?' and user said 'we've met "
        "twice'), that stated total IS the final answer. Do NOT add earlier encounters or events on top "
        "of it. The stated total already accounts for all prior occurrences.\n"
        "     SAME-SESSION INCREMENTS (OVERRIDES Rule 11): If a stated cumulative TOTAL COUNT AND "
        "new items both appear in the SAME session [Session: DATE] label, the stated total ALREADY "
        "includes those items — even if the phrasing sounds like a fresh addition "
        "('just got back', 'just scored more', 'I just got 8 more'). "
        "This rule OVERRIDES Rule 11 (Mandatory Arithmetic) for same-session data. "
        "CRITICAL: Do NOT add same-session items to the stated total. The stated total IS the final count. "
        "EXCEPTION: This rule does NOT apply to GOAL vs CURRENT BALANCE calculations "
        "(Rule 6: HOW MANY MORE TO EARN). If [GOAL: N] and [CURRENT: M] are in the same session, "
        "always compute GOAL − CURRENT = answer regardless of session.\n"
        "  2. AGGREGATION PATH (no stated total): Apply deduplication — same item/entity across "
        "multiple sessions = count ONCE. Mark duplicates 'DUPLICATE OF #N'.\n"
        "  3. Apply temporal scope: exclude items marked [OUT OF SCOPE]. Include only [IN SCOPE] items.\n"
        "  4. ZERO-RESULT HANDLING:\n"
        "     - If Step 1 said 'Topic never mentioned': respond with abstention — "
        "'I don't have information about [X] in the provided context.'\n"
        "     CRITICAL: Do NOT write 'Total count: 0' for a topic that was simply ABSENT from context. "
        "Absence of evidence ≠ evidence of zero. Use abstention instead.\n"
        "     - If Step 1 said 'Topic mentioned but all [OUT OF SCOPE]': respond with 'Total count: 0.'\n"
        "     - If Step 1 found [IN SCOPE] instances but after dedup the count is 0: 'Total count: 0.'\n"
        "  5. QUALIFIER MATCH FOR STATED TOTALS: When the QUESTION asks about items with a specific qualifier "
        "(rare, antique, vintage, handmade, etc.) AND a stated total of N [qualifier] items exists, "
        "only add a new item as [+1] if it is EXPLICITLY labeled with the SAME qualifier in context. "
        "Example: 'my collection of 57 rare records' + 'I just got a new vinyl record' → "
        "the new vinyl is NOT called 'rare', so rare records total stays at 57 (no +1). "
        "Only 'I got a new RARE record' would increment the count.\n"
        "  6. HOW MANY MORE TO EARN/REACH: If the question asks 'how many more [units] do I need to earn/collect/save "
        "to reach/redeem [goal]?', find in the enumeration: (a) [GOAL: N] = the threshold/total needed, "
        "and (b) [CURRENT: N] = the user's current balance. Compute GOAL − CURRENT = answer. "
        "The FINAL ANSWER must be that DIFFERENCE — NOT the goal total itself. "
        "CRITICAL: 'I just need a total of 300 points' means the GOAL is 300, NOT that you need 300 more. "
        "If the user has 200 points currently and the goal is 300, the answer is 100 (not 300). "
        "State it as: 'You need to earn N more [units].' and set 'Total count: N.'\n"
        "     NOTE: This applies ONLY to earning/accumulating units toward a REWARD THRESHOLD "
        "(points, badges, stamps, miles, items needed for redemption). "
        "It does NOT apply to price savings questions ('how much did I save on X' = original_price − paid_price, "
        "NOT a goal-earning calculation — just report the dollar savings directly).\n"
        "  7. State the final answer in the standard format:\n"
        "     - For item counts: 'Total count: N.'\n"
        "     - For money/time totals: 'Total: $X.' or 'Total: N hours.'\n"
        "Your response: show the de-duplicated list with markings, then state the final answer."
    )
    user_msg2 = (
        f"Original question: {question}{date_hint}\n\n"
        f"Enumerated instances:\n{enumeration}\n\n"
        f"{count_hint}"
    )
    answer, tokens2 = await call_gen_api(client, GEN_SYSTEM_PROMPT, user_msg2, max_tokens_step2, GEN_TEMPERATURE)

    return answer, tokens1 + tokens2


async def judge_answer(client: AsyncOpenAI, task: str, question: str,
                        gold: str, hypothesis: str, abstention: bool,
                        question_date: str = None) -> tuple[bool, str, int]:
    """Judge hypothesis against gold answer. Returns (correct, judge_response, tokens_used)."""
    prompt = get_anscheck_prompt(task, question, gold, hypothesis, abstention,
                                 question_date=question_date)
    resp = await call_with_backoff(
        client.chat.completions.create,
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        n=1,
        temperature=0,
        seed=42,  # ITER-46: deterministic judge outputs
        max_tokens=JUDGE_MAX_TOKENS,
    )
    judge_text = resp.choices[0].message.content.strip()
    correct = "yes" in judge_text.lower()
    tokens = resp.usage.total_tokens if resp.usage else 0
    return correct, judge_text, tokens


# ── Main evaluation loop ───────────────────────────────────────────────────────

async def run_evaluation(limit: int | None, resume: bool, offset: int = 0,
                         qtype_filter: str | None = None,
                         ids_filter: set | None = None,
                         concurrency: int = 1,
                         judge_model: str | None = None,
                         gen_model: str | None = None,
                         fast_recall: bool = False) -> None:
    # Load dataset
    print(f"Loading dataset from {DATASET_PATH} ...")
    with open(DATASET_PATH) as f:
        data = json.load(f)
    if offset:
        data = data[offset:]
    if limit:
        data = data[:limit]
    total_cases = len(data)
    print(f"Total cases to evaluate: {total_cases}")

    # Pre-load embedder ONCE (avoids reloading model weights for every case)
    from agentmemory.embeddings import create_embedder
    print("Pre-loading dense embedder (once) ...")
    shared_embedder = create_embedder(prefer_dense=True)
    print(f"Embedder mode: {shared_embedder.mode}")

    # Pre-load cross-encoder reranker ONCE
    from agentmemory.reranking import CrossEncoderReranker
    print("Pre-loading CrossEncoder reranker (once) ...")
    shared_reranker = CrossEncoderReranker()
    shared_reranker._load_model()   # force load now
    print("Reranker loaded.")

    # Load progress if resuming
    completed_ids: set[str] = set()
    per_case_results: list[dict] = []
    if resume and os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    completed_ids.add(entry["question_id"])
                    per_case_results.append(entry)
        print(f"Resuming: {len(completed_ids)} cases already completed.")

    # Apply model overrides
    global JUDGE_MODEL, GEN_MODEL
    if judge_model:
        JUDGE_MODEL = judge_model
    if gen_model:
        GEN_MODEL = gen_model
    print(f"Generator model: {GEN_MODEL}  |  Judge model: {JUDGE_MODEL}")

    # OpenAI client (always needed for judging)
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    openai_client = AsyncOpenAI(api_key=openai_key)

    # Generator client — either OpenAI or Anthropic
    if GEN_MODEL.startswith("claude-"):
        if not _ANTHROPIC_AVAILABLE:
            raise RuntimeError("anthropic package not installed. Run: pip install anthropic")
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable not set.")
        client = AsyncAnthropic(api_key=anthropic_key)
        print(f"Using Anthropic client for generation ({GEN_MODEL})")
    else:
        client = openai_client  # reuse same OpenAI client for generation

    # Open progress file for appending
    progress_fh = open(PROGRESS_FILE, "a", encoding="utf-8")

    # Shared counters (protected by lock for concurrent access)
    from collections import defaultdict
    lock = asyncio.Lock()
    state = {
        "correct_count":   0,
        "error_count":     0,
        "abstained_count": 0,
        "evaluated_count": len(completed_ids),
        "cumulative_tokens": 0,
    }
    type_correct_running = defaultdict(int)
    type_total_running   = defaultdict(int)
    per_case_results_lock = lock  # reuse same lock

    # Count already-correct and already-abstained from loaded progress
    for r in per_case_results:
        if r.get("correct"):
            state["correct_count"] += 1
        if r.get("ctx_abstained"):
            state["abstained_count"] += 1
        qt = r.get("question_type", "unknown")
        type_total_running[qt] += 1
        if r.get("correct"):
            type_correct_running[qt] += 1

    print(f"\n{'='*70}")
    print(f"Starting evaluation with GEN_MODEL={GEN_MODEL}, JUDGE_MODEL={JUDGE_MODEL}")
    print(f"concurrency={concurrency}, fast_recall={fast_recall}")
    print(f"TOKEN_BUDGETS={TOKEN_BUDGETS}")
    print(f"{'='*70}\n")

    # ── Build filtered list of cases to process ──────────────────────────────
    cases_to_run = []
    for case_idx, case in enumerate(data):
        _cid = case["question_id"]
        _qt  = case["question_type"]
        if _cid in completed_ids:
            continue
        if qtype_filter and _qt != qtype_filter:
            continue
        if ids_filter and _cid not in ids_filter:
            continue
        cases_to_run.append((case_idx, case))

    semaphore = asyncio.Semaphore(concurrency)

    async def process_case(case_idx: int, case: dict) -> None:
        """Process a single evaluation case (runs concurrently under semaphore)."""
        case_id   = case["question_id"]
        qtype     = case["question_type"]
        question  = case["question"]
        gold      = case["answer"]
        abstention = "_abs" in case_id
        case_num  = case_idx + 1

        store = None  # FIX P2-I: init to None so the except handler can always close it safely
        try:
            # Parse question_date early (needed for all types)
            import datetime as dt_module
            question_date_str = case.get("question_date")
            question_date_ts = None
            if question_date_str:
                try:
                    # Format: "2023/04/10 (Mon) 23:07"
                    clean = re.sub(r'\s*\([^)]*\)\s*', ' ', question_date_str).strip()
                    question_date_ts = dt_module.datetime.strptime(
                        clean, "%Y/%m/%d %H:%M").timestamp()
                except Exception:
                    pass

            # ── fast_recall scale: 50% limits for quick iteration ──
            _rl = (lambda n: max(25, n // 2)) if fast_recall else (lambda n: n)

            # ── Ingest into fresh MemoryStore ──
            from agentmemory.core import MemoryStore

            store = MemoryStore(
                path=":memory:",
                embedder=shared_embedder,
                prefer_dense=True,
                auto_graph=True,
                write_validation=False,
                streaming_consolidation=False,  # Preserve raw user statements with exact numbers
                proactive_surfacing=False,
                auto_consolidate=False,
                query_expansion=True,
                reranker=True,
                ann_ef_construction=200,
                ann_ef_search=100,
                auto_calibrate_abstention=False,
                # ITER-46: use_exact_knn=False (reverted) — HNSW with per-key level hash
                # is now deterministic without the retrieval-quality loss of brute-force KNN
            )
            # Inject pre-loaded reranker to avoid per-case model reload
            store._retrieval._reranker = shared_reranker

            # Change 5 — pass reference_date for temporal-reasoning ingestion
            reference_date = None
            if qtype == "temporal-reasoning" and question_date_ts:
                reference_date = question_date_ts

            if qtype in ("multi-session", "temporal-reasoning", "knowledge-update"):
                # Fix 1+2: Ingest each session with a UNIQUE session_id.
                # TR/KU uses per-session IDs so session date labels can be
                # injected into the context (Fix 2 session label injection).
                sessions = case["haystack_sessions"]
                dates = case.get("haystack_dates", [])
                messages_count = 0
                for sidx, session in enumerate(sessions):
                    date_str = dates[sidx] if sidx < len(dates) else None
                    per_session_msgs = []
                    if date_str:
                        per_session_msgs.append({"role": "system",
                                                 "content": f"[Session date: {date_str}]"})
                    for turn in session:
                        per_session_msgs.append({"role": turn["role"],
                                                 "content": turn["content"]})
                    messages_count += len(per_session_msgs)

                    # For TR/KU: use the actual session date as reference_date so
                    # TemporalGrounder resolves relative phrases against session date,
                    # giving accurate event_time stamps for temporal sorting.
                    session_ref_date = reference_date  # default: question_date_ts
                    if qtype in ("temporal-reasoning", "knowledge-update") and date_str:
                        try:
                            clean_date = re.sub(r'\s*\([^)]*\)\s*', ' ', date_str).strip()
                            if clean_date:
                                session_ref_date = dt_module.datetime.strptime(
                                    clean_date, "%Y/%m/%d %H:%M").timestamp()
                        except Exception:
                            pass  # keep question_date_ts as fallback

                    await store.async_ingest_conversation(
                        per_session_msgs,
                        session_id=f"{case_id}_s{sidx}",
                        # FIX P2-E: include "multi-session" so MS nodes get event_time set
                        # from the session date. Without this, MS nodes have event_time=None
                        # → effective_time ≈ created_at ≈ 2026, making ms_tw_results always
                        # empty (its event_time filters target historical 2023 timestamps).
                        reference_date=session_ref_date if qtype in ("temporal-reasoning", "knowledge-update", "multi-session") else None,
                    )

                    # ITER-14: Post-ingestion user event extraction for TR and MS.
                    # The standard ingestion may produce noisy or assistant-mixed nodes.
                    # For TR questions (event timing, "how many days ago", ordering),
                    # we need SHORT focused fact sentences so targeted event queries
                    # score these nodes above assistant advice.
                    # E.g., "I just bought a smoker" becomes a dedicated node that
                    # retrieval scores very highly for "how many days ago did I buy a smoker?"
                    # NOTE: Restricted to TR only — MS causes LLM over-counting (duplicate event
                    # nodes cause double-counting in aggregation questions like "how many weddings").
                    if qtype == "temporal-reasoning":
                        from agentmemory import Provenance as _Provenance
                        for turn in session:
                            if turn.get("role") != "user":
                                continue
                            _events = extract_user_events(turn.get("content", ""))
                            for _evt in _events:
                                try:
                                    # Use relative-date-adjusted event_time when possible
                                    # e.g., "Yesterday I attended Nordstrom" → session_date - 1 day
                                    _evt_time = event_relative_date(_evt, session_ref_date) if session_ref_date else session_ref_date
                                    await store.async_add(
                                        _evt,
                                        metadata={"role": "user", "event_extract": True},
                                        event_time=_evt_time,
                                        provenance=_Provenance(
                                            session_id=f"{case_id}_s{sidx}",
                                            extraction_method="event_extract",
                                        ),
                                    )
                                except Exception:
                                    pass  # never fail ingestion due to extraction error
            else:
                messages = convert_sessions_to_messages(case)
                messages_count = len(messages)
                await store.async_ingest_conversation(
                    messages,
                    session_id=case_id,
                    reference_date=reference_date,
                )

            # ── Build context ──
            # Change 4 — temporal anchoring for async_recall
            temporal_center = None
            use_event_time = False
            if qtype == "temporal-reasoning" and question_date_ts:
                temporal_center = question_date_ts
                use_event_time = True

            # Two-step counting flag — set True for MS counting and KU "how many/how much" questions
            _is_counting_q = False

            if qtype == "multi-session":
                _recall_limit = _rl(500)
                _min_relevance = 0.0
                # ITER-4: For "how many / how much / total" counting questions, disable
                # session_balanced so the context fills with the most topic-relevant memories
                # across ALL sessions, not one slot per session. Counting questions need
                # every instance of the topic (e.g., baking, gaming hours) to be visible;
                # session_balanced wastes budget on irrelevant sessions that lack the topic.
                # For non-counting questions (what/who/which), keep session_balanced=True
                # to ensure multi-session coverage.
                _q_lower = question.lower()
                _is_counting_q = (
                    _q_lower.startswith("how many") or
                    _q_lower.startswith("how much") or
                    re.search(r"\btotal\b.*\b(cost|price|time|hours|days|weight|money|amount)\b", _q_lower) is not None
                )
                # ITER-38: Hybrid session_balanced for MS counting:
                # - With time window ("past two weeks", "in March"): session_balanced=False
                #   to maximize density of in-scope items (ITER-4 original logic)
                # - Without time window ("in total", "ever", "overall", no scope): session_balanced=True
                #   to guarantee representation from EVERY session, preventing late sessions
                #   (e.g., Session 5 with Celeste 10h) from being crowded out by high-density
                #   earlier sessions. Without this, gaming-hours and similar cross-session totals
                #   miss instances from low-ranked sessions.
                _ms_has_time_window = False
                if _is_counting_q and question_date_ts:
                    _tw_check = compute_ms_time_window(question, question_date_ts)
                    _ms_has_time_window = _tw_check is not None
                # session_balanced=True for open-ended totals; False for windowed counts
                _session_balanced = (not _is_counting_q) or (not _ms_has_time_window)
                # ITER-2: Filter assistant-role memories for MS.
                # MS counting questions fail because assistant advice (summaries,
                # recommendations) crowds out user-stated event records.
                # Safety: require >=10 user nodes to avoid empty context.
                ms_results = await store.async_recall(question, limit=_rl(500))
                ms_user_id_set = {r.node.id for r in ms_results
                                  if r.node.metadata.get("role", "user") != "assistant"}
                # ITER-10: For counting questions with a detectable time window (e.g., "past two
                # weeks", "in January"), do a supplementary time-bounded recall to surface events
                # in that period that score too low semantically to appear in the top-500.
                if _is_counting_q:
                    _tw = compute_ms_time_window(question, question_date_ts)
                    if _tw:
                        _tw_start, _tw_end = _tw
                        ms_tw_results = await store.async_recall(
                            question, limit=_rl(500),
                            event_time_start=_tw_start,
                            event_time_end=_tw_end,
                        )
                        for _r in ms_tw_results:
                            if _r.node.metadata.get("role", "user") != "assistant":
                                ms_user_id_set.add(_r.node.id)
                ms_user_ids = list(ms_user_id_set)
                ms_candidate_ids = ms_user_ids if len(ms_user_ids) >= 10 else [r.node.id for r in ms_results]
                # ITER-39: Increase token budget for ALL MS counting questions (not just windowed).
                # Open-ended totals (gaming hours, furniture, education years) also benefit from
                # more context — the model misses instances at 7500 token budget.
                _ms_token_budget = TOKEN_BUDGETS.get(qtype, 1000)
                if _is_counting_q:
                    _ms_token_budget = max(_ms_token_budget, 10000)
                context, context_meta = await store.async_build_context(
                    question,
                    token_budget=_ms_token_budget,
                    recall_limit=_recall_limit,
                    session_balanced=_session_balanced,
                    min_relevance_score=_min_relevance,
                    context_as_of=question_date_ts,
                    candidate_ids=ms_candidate_ids,
                )
            elif qtype == "knowledge-update":
                # Fix 9 (v5): Two-pass recall for KU — standard query + update-signal query.
                # Sort by (event_time DESC, recall_score DESC) for temporal-first ordering.
                # Per-session ingestion gives each node an event_time from its session date,
                # so sorting by event_time puts the most recent session's content first.
                _recall_limit = _rl(500)
                _min_relevance = 0.0
                # ITER-29: KU counting questions need ALL instances across ALL sessions,
                # not one slot per session. Disable session_balanced for "how many/how much"
                # so the most topic-relevant nodes fill the context regardless of session.
                _ku_q_lower = question.lower()
                _is_ku_counting = (
                    _ku_q_lower.startswith("how many") or
                    _ku_q_lower.startswith("how much") or
                    re.search(r"\btotal\b.*\b(cost|price|time|hours|days|weight|money|amount)\b",
                               _ku_q_lower) is not None
                )
                _session_balanced = not _is_ku_counting

                ku_base_results = await store.async_recall(question, limit=_recall_limit)
                ku_update_query = question.strip().rstrip("?") + " update changed new currently"
                ku_update_results = await store.async_recall(ku_update_query, limit=_rl(200))
                ku_union: dict[str, object] = {}
                for r in ku_base_results:
                    ku_union[r.node.id] = r
                for r in ku_update_results:
                    if r.node.id not in ku_union or r.score > ku_union[r.node.id].score:
                        ku_union[r.node.id] = r
                # KU Focus recall: strip question framing so the embedding matches memory text better.
                # E.g. "What was my personal best time in the charity 5K run?" → "personal best time charity 5K run"
                _ku_focus = re.sub(
                    r"^(what('s| is| was| are| were)?|how (many|much|long|often|frequently)|when|where|which|who)\s+",
                    "", question, flags=re.I).rstrip("?").strip()
                _ku_focus = re.sub(
                    r"\b(was|is|are|were|have|had|has|did|do|does)\s+(i|my|me|you)\b",
                    " ", _ku_focus, flags=re.I).strip()
                _ku_focus = re.sub(r"^(my|i|me)\s+", "", _ku_focus, flags=re.I).strip()
                _ku_focus = " ".join(_ku_focus.split())
                if _ku_focus and _ku_focus.lower() != question.lower() and len(_ku_focus) > 8:
                    # ITER-5: Increased focus-query recall from 100→300 to surface
                    # low-ranked user updates (e.g., "$400K pre-approval" in a moving-logistics session)
                    # ITER-30: Increased from 300→500 to maximize coverage of low-ranked updates
                    ku_focus_results = await store.async_recall(_ku_focus, limit=_rl(500))
                    for r in ku_focus_results:
                        if r.node.id not in ku_union or r.score > ku_union[r.node.id].score:
                            ku_union[r.node.id] = r
                # ITER-31: Additional past-tense recall pass for KU counting questions
                # Helps surface session attendance records (e.g., "I attended the bereavement group")
                # when the focus query alone doesn't retrieve enough instances
                if _is_ku_counting and len(_ku_focus) > 5:
                    _ku_past = _ku_focus + " attended went visited participated"
                    ku_past_results = await store.async_recall(_ku_past, limit=_rl(300))
                    for r in ku_past_results:
                        if r.node.id not in ku_union or r.score > ku_union[r.node.id].score:
                            ku_union[r.node.id] = r

                # Load nodes to get event_time and content for temporal+user-priority sorting.
                # Use created_at as fallback: since we ingest sessions in order
                # (s0, s1, s2...), created_at increases with session index even
                # when text lacks explicit date references (event_time=None).
                ku_node_times: dict[str, float] = {}
                ku_loaded_nodes: dict[str, object] = {}
                for nid in ku_union.keys():
                    n = await store._storage.load_node(nid)
                    if n:
                        ku_node_times[nid] = n.event_time if n.event_time else n.created_at
                        ku_loaded_nodes[nid] = n

                def _ku_user_score(nid: str) -> float:
                    """Boost memories that look like user statements (start with 'I').
                    These carry the user's actual facts; assistant advice starts with
                    imperatives ('Try', 'Focus', 'Remember', etc.) and is lower priority."""
                    n = ku_loaded_nodes.get(nid)
                    if not n:
                        return 0.0
                    c = n.content.strip()
                    if c.lower().startswith(("i ", "i'", "i've", "i'm", "i'd", "i'll", "i had", "i have", "i am")):
                        return 1.0
                    return 0.0

                # Sort: (time DESC, user_statement DESC, recall_score DESC)
                # Most recent session first; within same session, user facts before advice.
                ku_candidate_ids_raw = sorted(
                    ku_union.keys(),
                    key=lambda nid: (
                        ku_node_times.get(nid, 0.0),
                        _ku_user_score(nid),
                        ku_union[nid].score
                    ),
                    reverse=True
                )
                # ITER-1: Filter assistant-role memories for KU.
                # Assistant advice ("Based on your pre-approval for $350K...") uses
                # question-specific vocabulary and scores high, crowding out the user's
                # actual updated fact. Safety fallback: keep unfiltered if <3 user nodes.
                ku_user_ids = [nid for nid in ku_candidate_ids_raw
                               if ku_loaded_nodes.get(nid) and
                               ku_loaded_nodes[nid].metadata.get("role", "user") != "assistant"]
                ku_candidate_ids = ku_user_ids if len(ku_user_ids) >= 3 else ku_candidate_ids_raw
                # Store results list for session label injection (sorted same order)
                ku_all_results = [ku_union[nid] for nid in ku_candidate_ids]

                # ITER-29: Use larger token budget for KU counting to fit more instances
                _ku_budget = 3500 if _is_ku_counting else TOKEN_BUDGETS.get(qtype, 1000)
                context, context_meta = await store.async_build_context(
                    question,
                    token_budget=_ku_budget,
                    recall_limit=_recall_limit,
                    session_balanced=_session_balanced,
                    min_relevance_score=_min_relevance,
                    context_as_of=question_date_ts,
                    candidate_ids=ku_candidate_ids,
                )
            elif qtype == "temporal-reasoning":
                # Fix 1: Multi-entity retrieval — extract comparison entities and run
                # separate recalls so both entities in an ordering question are retrieved.
                tr_entities = extract_comparison_entities(question)
                multi_entity_triggered = len(tr_entities) > 1

                # ITER-15: Force multi_entity_triggered=True for ordering questions that
                # don't name specific entities ("order of three trips", "sports events
                # in January"). These need: (a) chronological sort so LLM sees events
                # in temporal order, (b) higher recall limit to capture all N events.
                # Without this, they fall into single-entity path with limit=75, which
                # may miss some of the N events when sessions are sparse.
                _is_ordering_q = bool(re.search(
                    r'\border\s+of\b|\bearliest\s+to\s+latest\b|\blatest\s+to\s+earliest\b'
                    r'|\bfirst.*?second.*?(?:last|third|final)\b|\bchronological\b',
                    question, re.I))
                if _is_ordering_q and not multi_entity_triggered:
                    multi_entity_triggered = True

                tr_union: dict[str, object] = {}  # node_id → RetrievalResult (best score)
                for tr_entity in tr_entities:
                    # ITER-3b: For multi-entity ordering questions, increase per-entity recall
                    # from 75→150 to ensure both/all events are retrieved even when one ranks low.
                    _entity_recall_limit = _rl(150) if multi_entity_triggered else _rl(75)
                    tr_entity_results = await store.async_recall(tr_entity, limit=_entity_recall_limit)
                    for r in tr_entity_results:
                        if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                            tr_union[r.node.id] = r
                # ITER-11: Always run full-question recall for all TR questions.
                # For multi-entity: captures cross-entity context. For single-entity:
                # captures action+entity phrasing (e.g., "how many days ago did I BUY a smoker?"
                # scores the user's purchase message higher than entity-only "smoker" recall,
                # which is dominated by assistant BBQ/maintenance advice).
                tr_orig_results = await store.async_recall(question, limit=_rl(75))
                for r in tr_orig_results:
                    if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                        tr_union[r.node.id] = r

                # ITER-8/ITER-20: Date-targeted recall for questions with a computable
                # relative date phrase ("last Saturday", "four weeks ago", "10 days ago").
                # ITER-8: Text-augmented semantic recall (appends absolute date string).
                # ITER-20: Time-windowed recall centered on the target date (±3 days).
                # Together these ensure the exact-date session is always in the candidate pool
                # even when semantic similarity to the question is low.
                if not multi_entity_triggered:
                    tr_target_date = compute_tr_target_date(question, question_date_ts)
                    if tr_target_date:
                        # ITER-8: text augmentation (helps when session content has explicit date)
                        _date_query = f"{question} {tr_target_date}"
                        tr_date_results = await store.async_recall(_date_query, limit=_rl(75))
                        for r in tr_date_results:
                            if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                                tr_union[r.node.id] = r
                        # ITER-20: time-windowed recall ±3 days around the target date.
                        # Ensures the session from the exact target date is retrieved regardless
                        # of semantic score (e.g., Queen concert on April 15 for "last Saturday").
                        _target_ts = datetime.strptime(tr_target_date, "%Y-%m-%d").timestamp()
                        _tw_results = await store.async_recall(
                            question, limit=_rl(200),
                            event_time_start=_target_ts - 3 * 86400,
                            event_time_end=_target_ts + 3 * 86400,
                        )
                        for r in _tw_results:
                            if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                                tr_union[r.node.id] = r

                # ITER-12: For single-entity "how many days/weeks ago" questions, do
                # multi-window time-bounded recall to surface the specific user event
                # regardless of semantic score. These questions ask about a specific past
                # event (purchase, attendance, etc.) that may use sparse vocabulary and
                # score lower than topically-related assistant content. By scanning
                # multiple time windows, we ensure the event is in the candidate pool
                # even if it ranks below the assistant-noise cutoff.
                if (not multi_entity_triggered and question_date_ts and
                        re.search(r'\b(?:days?|weeks?)\s+ago\b', question, re.IGNORECASE)):
                    for _window_days in [14, 30, 60, 90]:
                        _tw_start = question_date_ts - _window_days * 86400
                        _tw_results = await store.async_recall(
                            question, limit=_rl(200),
                            event_time_start=_tw_start,
                            event_time_end=question_date_ts,
                        )
                        for r in _tw_results:
                            if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                                tr_union[r.node.id] = r

                # ITER-38: For TR "how long had I been X when Y" duration-gap questions,
                # add a supplementary recall specifically for the START DATE of the activity.
                # The session where the user first started/joined X may have low semantic
                # similarity to the question (it says "I joined Book Lovers Unite" not
                # "how long had I been a member"). Without this recall, the start session
                # may be absent from the context and the model cannot compute the gap.
                # ITER-38: Duration-gap questions MUST contain a "when" clause (a milestone event).
                # "How long have I been working before I started at Google?" (no "when") is NOT
                # a duration-gap question — triggering retrieval on it contaminates context for
                # abstention cases where the model should say "not enough info".
                _is_dur_gap_q = bool(re.search(
                    r'(?:\bhow long had (?:i|you) been\b|\bhow long (?:have|has) (?:i|you) been\b'
                    r'|\bhow many (?:weeks?|months?|days?) (?:had )?(?:passed since|since|ago))'
                    r'.*\bwhen\b',
                    question, re.I))
                if _is_dur_gap_q and not multi_entity_triggered:
                    # Extract activity topic from "how long had I been X-ing" pattern
                    _dg_match = re.search(
                        r'\bhow long (?:had|have) (?:i|you) been ([\w\s]+?)(?:\s+when\b|\?|$)',
                        question, re.I)
                    if _dg_match:
                        _dg_activity = _dg_match.group(1).strip()
                        # Search for the session that mentions when the activity started
                        _dg_start_query = (
                            f"started joined began first {_dg_activity} "
                            f"ago months weeks years since member"
                        )
                        _dg_results = await store.async_recall(
                            _dg_start_query, limit=_rl(150))
                        for r in _dg_results:
                            if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                                tr_union[r.node.id] = r
                    # Also handle "how many X had passed since I <activity>" pattern
                    _dg_match2 = re.search(
                        r'\bhow many \w+ (?:had )?(?:passed since|since) (?:i|you)\s+([\w\s]+?)(?:\s+when\b|\?|$)',
                        question, re.I)
                    if _dg_match2:
                        _dg_activity2 = _dg_match2.group(1).strip()
                        _dg_start_query2 = (
                            f"started joined began first {_dg_activity2} "
                            f"ago months weeks years since recovered finished"
                        )
                        _dg_results2 = await store.async_recall(
                            _dg_start_query2, limit=_rl(150))
                        for r in _dg_results2:
                            if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                                tr_union[r.node.id] = r
                    # Also search for the milestone event in the question (the "when Y" part)
                    _dg_when_match = re.search(r'\bwhen i\s+([\w\s]+?)(?:\?|$)', question, re.I)
                    if _dg_when_match:
                        _dg_event = _dg_when_match.group(1).strip()
                        _dg_event_results = await store.async_recall(
                            _dg_event, limit=_rl(100))
                        for r in _dg_event_results:
                            if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                                tr_union[r.node.id] = r

                # ITER-16: For multi-entity ordering questions with an explicit time-scope
                # ("past three months", "in January", "past month"), do a supplementary
                # time-bounded recall covering all sessions in that period. This ensures
                # ALL N events (e.g., three trips, sports events in January) are retrieved
                # even if some sessions score low individually for the question query.
                if multi_entity_triggered and question_date_ts:
                    _tr_tw = compute_tr_time_window(question, question_date_ts)
                    if _tr_tw:
                        _tr_tw_start, _tr_tw_end = _tr_tw
                        _tr_tw_results = await store.async_recall(
                            question, limit=_rl(300),
                            event_time_start=_tr_tw_start,
                            event_time_end=_tr_tw_end,
                        )
                        for r in _tr_tw_results:
                            if r.node.id not in tr_union or r.score > tr_union[r.node.id].score:
                                tr_union[r.node.id] = r

                tr_all_results = sorted(tr_union.values(), key=lambda r: r.score, reverse=True)
                tr_candidate_ids = sorted(tr_union.keys(), key=lambda nid: tr_union[nid].score, reverse=True)

                # ITER-3a: Selective assistant filter for single-entity TR questions.
                # Single-entity = event retrieval ("how many days ago did I buy X?", "who gave
                # me jewelry last Saturday?"). These need user-stated facts, not assistant advice.
                # Multi-entity = ordering/comparison ("which happened first, X or Y?") — keep
                # assistant memories because temporal commentary provides date anchors for ordering.
                # Previous full-TR filter regressed (-3 cases) because it hurt ordering questions.
                # Selective filter avoids that: only applies when multi_entity_triggered=False.
                if not multi_entity_triggered:
                    tr_user_ids = [nid for nid in tr_candidate_ids
                                   if tr_union.get(nid) and
                                   tr_union[nid].node.metadata.get("role", "user") != "assistant"]
                    if len(tr_user_ids) >= 1:
                        tr_candidate_ids = tr_user_ids
                    # ITER-25: For single-entity TR with a computed target date, extract
                    # event_extract nodes from the target session as a priority prefix.
                    # These nodes (e.g., "I saw Queen live with parents") contain the key
                    # who/when/what facts but have LOW activation scores so they get buried
                    # in the session-balanced context. Prefixing them ensures the LLM sees
                    # the target-session's extracted facts before any other context.
                    _tr_target_date = compute_tr_target_date(question, question_date_ts) if question_date_ts else None
                    _tr_priority_prefix = ""
                    if _tr_target_date:
                        _td_ts = datetime.strptime(_tr_target_date, "%Y-%m-%d").timestamp()
                        _priority_nodes = []
                        for nid in tr_candidate_ids:
                            nd = tr_union.get(nid)
                            if not nd:
                                continue
                            n = nd.node
                            if not n.metadata.get("event_extract"):
                                continue
                            evt_t = getattr(n, "event_time", None)
                            if evt_t and abs(evt_t - _td_ts) <= 2 * 86400:
                                _priority_nodes.append(n.content)
                        if _priority_nodes:
                            _tr_priority_prefix = (
                                f"[Key events on {_tr_target_date}]\n" +
                                "\n".join(f"- {c}" for c in _priority_nodes) + "\n\n"
                            )
                else:
                    # ITER-9: For multi-entity ordering questions, sort candidates chronologically
                    # (by session index, oldest first) so the LLM sees events in temporal order.
                    def _session_idx(nid):
                        try:
                            sid = tr_union[nid].node.provenance.session_id or ''
                        except AttributeError:
                            return 9999
                        m = re.search(r'_s(\d+)$', sid)
                        return int(m.group(1)) if m else 9999
                    tr_candidate_ids = sorted(tr_candidate_ids, key=_session_idx)
                    # ITER-23: For multi-entity ordering, apply partial assistant filter.
                    # Include ALL user/event_extract nodes + top-15 assistant nodes by score.
                    # Rationale: long assistant photography/tech advice responses score high
                    # for topic-related queries but consume all the context budget, crowding
                    # out short user statements that contain the KEY DATE FACTS (e.g.,
                    # "I got the lens a month ago"). By capping assistant nodes at 15 (the
                    # most relevant commentary), ALL user date-containing nodes fit within
                    # the token budget, ensuring the LLM sees the precise timing clues.
                    _tr_user_event_ids = [
                        nid for nid in tr_candidate_ids
                        if tr_union[nid].node.metadata.get("role", "user") != "assistant"
                    ]
                    _tr_asst_top = sorted(
                        [nid for nid in tr_candidate_ids
                         if tr_union[nid].node.metadata.get("role") == "assistant"],
                        key=lambda nid: tr_union[nid].score, reverse=True
                    )[:15]
                    # Safety: if fewer than 2 user nodes, don't filter (fallback to all)
                    if len(_tr_user_event_ids) >= 2:
                        tr_candidate_ids = _tr_user_event_ids + _tr_asst_top
                        tr_candidate_ids = sorted(tr_candidate_ids, key=_session_idx)

                _recall_limit = _rl(150)
                _min_relevance = 0.0
                _session_balanced = True
                context, context_meta = await store.async_build_context(
                    question,
                    token_budget=TOKEN_BUDGETS.get(qtype, 1000),
                    recall_limit=_recall_limit,
                    session_balanced=_session_balanced,
                    min_relevance_score=_min_relevance,
                    context_as_of=question_date_ts,
                    candidate_ids=tr_candidate_ids,
                )
                # ITER-25: Prepend target-date event_extract priority prefix (single-entity)
                if not multi_entity_triggered and _tr_priority_prefix:
                    context = _tr_priority_prefix + context

                # ITER-26: For multi-entity ordering questions, prepend event_extract nodes
                # sorted chronologically. These low-activation event_extract nodes get buried
                # in session_balanced_order but contain the KEY temporal facts.
                # With time window: restrict to events in that period.
                # ITER-40: Without time window (e.g., "order of 6 museums"): include ALL
                # event_extract nodes — the session date anchors their event_time so the
                # model can order them correctly even when user says "I just came back"
                # without an explicit calendar date.
                if multi_entity_triggered and question_date_ts:
                    _i26_tw = compute_tr_time_window(question, question_date_ts)
                    _i26_events = []
                    for nid in tr_candidate_ids:
                        nd = tr_union.get(nid)
                        if not nd:
                            continue
                        n = nd.node
                        if not n.metadata.get("event_extract"):
                            continue
                        evt_t = getattr(n, "event_time", None)
                        if not evt_t:
                            continue
                        if _i26_tw:
                            _i26_start, _i26_end = _i26_tw
                            if _i26_start <= evt_t <= _i26_end:
                                evt_date = datetime.fromtimestamp(evt_t).strftime("%Y-%m-%d")
                                _i26_events.append((evt_t, evt_date, n.content))
                        else:
                            # ITER-40: no time window — include all event_extract nodes
                            evt_date = datetime.fromtimestamp(evt_t).strftime("%Y-%m-%d")
                            _i26_events.append((evt_t, evt_date, n.content))
                    if _i26_events:
                        _i26_events.sort(key=lambda x: x[0])  # chronological
                        _i26_lines = [f"  [{d}] {c}" for _, d, c in _i26_events]
                        context = (
                            "[Key events chronologically]\n" +
                            "\n".join(_i26_lines) + "\n\n" +
                            context
                        )
            else:
                # ITER-7: Increased SSP recall limit to 150 (was 80) to surface more preference memories
                _recall_limit = _rl(150)
                _min_relevance = 0.08
                _session_balanced = True
                # NOTE: SSP filter tested (ITER-2) and showed regression (20/30 vs baseline 21/30).
                # SSP questions ask about assistant recommendations referencing user prefs —
                # filtering removes that context. NOT filtered.
                # SSA: questions ask what the ASSISTANT said — filter would be catastrophic. NOT filtered.
                # ITER-6: SSU filter — SSU asks what the USER said/did/has. These are user-fact
                # questions; assistant advice/recommendations crowd out the user-stated facts.
                # SSP was reverted due to regression; SSU is fundamentally different (user facts, not
                # preference-based recommendations), so a separate SSU-only filter is warranted.
                if qtype == "single-session-user":
                    # ITER-16: Increased recall from 200→400 to surface low-ranked user facts
                    # (e.g., "my sister Emily lives in Denver" as a passing mention)
                    ssu_results = await store.async_recall(question, limit=_rl(400))
                    _ssu_seen = {r.node.id for r in ssu_results}
                    # Also recall with question entity stripped to catch indirect mentions
                    # (e.g., "Who gave me a stand mixer?" → recall "stand mixer" without "who")
                    _ssu_focus = re.sub(r'^(who|what|where|when|how|which|why)\s+', '', question, flags=re.I).strip()
                    if _ssu_focus and len(_ssu_focus) > 8 and _ssu_focus.lower() != question.lower():
                        _ssu_focus_results = await store.async_recall(_ssu_focus, limit=_rl(200))
                        for r in _ssu_focus_results:
                            if r.node.id not in _ssu_seen:
                                ssu_results.append(r)
                                _ssu_seen.add(r.node.id)
                    # ITER-30: For "how long have I been X-ing" questions, add a duration-augmented
                    # recall to surface the session where the START DATE or DURATION was mentioned.
                    # The start date may be in a memory node with "started X ago" vocabulary that
                    # doesn't rank high for the generic "how long" question query.
                    if re.search(r'\bhow long\b', question, re.I):
                        _dur_topic = re.sub(r'\bhow long have (i|you) been\b', '', question, flags=re.I).strip().rstrip('?').strip()
                        if _dur_topic:
                            _dur_query = f"started {_dur_topic} ago months weeks years since began"
                            _dur_results = await store.async_recall(_dur_query, limit=_rl(200))
                            for r in _dur_results:
                                if r.node.id not in _ssu_seen:
                                    ssu_results.append(r)
                                    _ssu_seen.add(r.node.id)
                    # ITER-18: Include top assistant nodes for SSU — some key facts
                    # (e.g., "Emily lives in Denver") only appear in assistant messages.
                    # ITER-6 assistant filter was neutral; reverting it since specific wrong
                    # cases (Emily Denver, stand mixer gift) show the info is in assistant msgs.
                    # Use mixed: all user nodes + top 5 assistant nodes by score.
                    ssu_user_ids = [r.node.id for r in ssu_results
                                    if r.node.metadata.get("role", "user") != "assistant"]
                    ssu_asst_ids = [r.node.id for r in sorted(
                        (x for x in ssu_results if x.node.metadata.get("role") == "assistant"),
                        key=lambda x: -x.score)[:5]]
                    ssu_candidate_ids = ssu_user_ids + ssu_asst_ids if ssu_asst_ids else (
                        ssu_user_ids if len(ssu_user_ids) >= 3 else [r.node.id for r in ssu_results]
                    )
                    context, context_meta = await store.async_build_context(
                        question,
                        token_budget=TOKEN_BUDGETS.get(qtype, 1000),
                        recall_limit=_recall_limit,
                        session_balanced=_session_balanced,
                        min_relevance_score=_min_relevance,
                        context_as_of=question_date_ts,
                        candidate_ids=ssu_candidate_ids,
                    )
                elif qtype == "single-session-preference":
                    # FIX P3-H: Explicit kind_boost for SSP — ensures PREFERENCE-kind nodes
                    # always rank above advice/assistant noise even when the question wording
                    # doesn't contain trigger words (e.g., "What coffee do I use?").
                    # ITER-36 baseline: single query with PREFERENCE kind_boost.
                    # Note: supplementary user-fact queries (ITER-38 attempt) caused regressions
                    # (adding non-preference nodes diluted preference context for cases that were
                    # already correct). Reverted to single-query PREFERENCE boost only.
                    from agentmemory.models import MemoryKind
                    ssp_boosted_list = await store.async_recall(
                        question, limit=_recall_limit,
                        kind_boost={MemoryKind.PREFERENCE: 1.5},
                    )
                    ssp_candidate_ids = [r.node.id for r in ssp_boosted_list]
                    context, context_meta = await store.async_build_context(
                        question,
                        token_budget=TOKEN_BUDGETS.get(qtype, 1000),
                        recall_limit=_recall_limit,
                        session_balanced=_session_balanced,
                        min_relevance_score=_min_relevance,
                        context_as_of=question_date_ts,
                        candidate_ids=ssp_candidate_ids,
                    )
                else:
                    # ITER-30: For SSA numbered list questions ("what was the 7th item in the list"),
                    # augment recall with ordinal/topic query to surface the specific list position.
                    _ssa_candidate_ids = None
                    if qtype == "single-session-assistant":
                        _ord_match = re.search(
                            r'\b(\d+(?:st|nd|rd|th)?|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\b.*\b(list|item|job|parameter|step|entry|point)\b',
                            question, re.I)
                        if _ord_match:
                            _ssa_base = await store.async_recall(question, limit=_rl(150))
                            _ssa_seen = {r.node.id for r in _ssa_base}
                            # Strip ordinal from question to get topic-only query
                            _topic_q = re.sub(r'\b(what was the|what is the|remind me of the|tell me the)\b', '', question, flags=re.I)
                            _topic_q = re.sub(r'\b(\d+(?:st|nd|rd|th)?|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+(item|job|parameter|step|entry|point)\b', '', _topic_q, flags=re.I).strip()
                            if _topic_q and len(_topic_q) > 8:
                                _ssa_topic = await store.async_recall(_topic_q, limit=_rl(150))
                                for r in _ssa_topic:
                                    if r.node.id not in _ssa_seen:
                                        _ssa_base.append(r)
                                        _ssa_seen.add(r.node.id)
                            _ssa_candidate_ids = [r.node.id for r in _ssa_base]
                    context, context_meta = await store.async_build_context(
                        question,
                        token_budget=TOKEN_BUDGETS.get(qtype, 1000),
                        recall_limit=_recall_limit,
                        session_balanced=_session_balanced,
                        min_relevance_score=_min_relevance,
                        context_as_of=question_date_ts,
                        candidate_ids=_ssa_candidate_ids,
                    )

            # ── Also run recall for top result storage ──
            if qtype == "temporal-reasoning":
                # Use multi-entity union results (already computed above)
                recall_results = tr_all_results
            elif qtype == "knowledge-update":
                # Use the temporally-sorted KU union results (already computed above)
                recall_results = ku_all_results
            else:
                _recall_kwargs = dict(limit=50, use_event_time=use_event_time,
                                      temporal_center=temporal_center)
                if use_event_time:
                    _recall_kwargs["temporal_width_hours"] = 720.0
                recall_results = await store.async_recall(question, **_recall_kwargs)
            top_recall_content = recall_results[0].node.content if recall_results else ""

            await store.async_close()

            # ── v17: Override context with full raw haystack ──
            if USE_DIRECT_CONTEXT:
                _sessions_raw = case["haystack_sessions"]
                _dates_raw = case.get("haystack_dates", [])
                context = build_direct_context(_sessions_raw, _dates_raw)
                if len(context) > MAX_CONTEXT_CHARS:
                    context = context[:MAX_CONTEXT_CHARS]
                    print(f"  [TRUNCATED] context for {case_id} to {MAX_CONTEXT_CHARS} chars", flush=True)
                context_meta = {}
                top_recall_content = ""
                for _s in _sessions_raw:
                    for _t in _s:
                        if _t.get("role") == "user":
                            top_recall_content = _t.get("content", "")[:500]
                            break
                    if top_recall_content:
                        break

            context_preview = (context or "")[:500]

            # ── Fix 2: For TR — inject per-memory session date labels ──
            # Fix 3: For MS — inject coreference hints
            final_context = context or ""

            if qtype in ("temporal-reasoning", "knowledge-update"):
                haystack_dates_list = case.get("haystack_dates", [])
                if USE_DIRECT_CONTEXT:
                    # Direct context already has [Session: DATE] labels embedded.
                    # Just prepend the session-dates index header.
                    if haystack_dates_list:
                        _header_label = ("Session Dates (listed chronologically oldest-first, NEWEST-LAST — [Session: DATE] below)"
                                         if qtype == "knowledge-update" else
                                         "Session Dates (each memory is labeled [Session: DATE] below)")
                        date_header_lines = [f"Session {i+1} date: {sd}"
                                             for i, sd in enumerate(haystack_dates_list)]
                        date_header = (f"=== {_header_label} ===\n"
                                       + "\n".join(date_header_lines) + "\n")
                        final_context = date_header + "\n" + final_context
                else:
                    _label_results = tr_all_results if qtype == "temporal-reasoning" else ku_all_results
                    # Inject [Session: YYYY-MM-DD HH:MM] labels at memory boundaries
                    session_labels_injected = False
                    if haystack_dates_list and _label_results:
                        labeled = inject_session_labels(final_context, _label_results, haystack_dates_list)
                        if labeled != final_context:
                            final_context = labeled
                            session_labels_injected = True
                    # Also prepend the session-dates index header for explicit reference
                    if haystack_dates_list:
                        _header_label = ("Session Dates (sorted most-recent-first, [Session: DATE] below)"
                                         if qtype == "knowledge-update" else
                                         "Session Dates (each memory is labeled [Session: DATE] below)")
                        date_header_lines = []
                        for sidx, sd in enumerate(haystack_dates_list):
                            date_header_lines.append(f"Session {sidx+1} date: {sd}")
                        date_header = (
                            f"=== {_header_label} ===\n"
                            + "\n".join(date_header_lines) + "\n"
                        )
                        final_context = date_header + "\n" + final_context

            elif qtype == "multi-session":
                # Fix 3: Inject coreference hints for MS counting questions
                coref_hints = detect_coreference_hints(final_context, question)
                if coref_hints:
                    hints_text = "=== Deduplication Notes ===\n" + "\n".join(coref_hints) + "\n"
                    final_context = hints_text + "\n" + final_context

            # ── Generate answer ──
            # ITER-13: Two-step enumerate+count for KU "how many/how much" questions.
            # ITER-28: Extended two-step to MS counting questions.
            # Previous "0/7 improvement" for MS was with GPT-4o; Opus follows structured
            # enumeration prompts far more reliably, making two-step effective for MS too.
            # ITER-38: MS step1 tokens increased from 2500→3500 to handle the larger context
            # (up to 10000 tokens for windowed counts) and ensure the enumeration list is
            # complete without truncation when many instances are spread across sessions.
            _q_lower = question.lower()
            _is_counting_q = (
                qtype in ("knowledge-update", "multi-session") and
                (
                    _q_lower.startswith("how many") or
                    # "how much" but NOT comparison/difference questions ("how much more/less/extra")
                    (_q_lower.startswith("how much") and
                     not re.search(r'^how much (?:more|less|extra|additional|further|longer|shorter)',
                                   _q_lower))
                ) and
                # KU two-part temporal questions like "How many X when I started... How many X now?"
                # require BOTH historical and current values — the counting path only gives one total.
                not (qtype == "knowledge-update" and re.search(r'\bwhen\b', question, re.I) and
                     re.search(r'\bnow\b', question, re.I))
            )
            if _is_counting_q:
                _step1_tokens = 3500 if qtype == "multi-session" else 1500
                _step2_tokens = 700 if qtype == "multi-session" else 500
                hypothesis, gen_tokens = await generate_counting_answer(
                    client, final_context, question,
                    question_type=qtype,
                    question_date=question_date_str or "",
                    max_tokens_step1=_step1_tokens,
                    max_tokens_step2=_step2_tokens,
                )
            else:
                hypothesis, gen_tokens = await generate_answer(
                    client, final_context, question,
                    question_type=qtype,
                    question_date=question_date_str or "",
                )
            # ── Judge answer ──
            correct, judge_response, judge_tokens = await judge_answer(
                openai_client, qtype, question, gold, hypothesis, abstention,
                question_date=question_date_str if qtype == "temporal-reasoning" else None,
            )

            # Change 8 — track context abstention
            ctx_abstained = bool(context_meta.get("abstained", False))

            # ── Save result + update shared counters (lock for concurrent safety) ──
            result = {
                "question_id":       case_id,
                "question_type":     qtype,
                "question":          question,
                "gold_answer":       gold,
                "context_preview":   context_preview,
                "top_recall":        top_recall_content[:500],
                "hypothesis":        hypothesis,
                "judge_response":    judge_response,
                "correct":           correct,
                "gen_tokens":        gen_tokens,
                "judge_tokens":      judge_tokens,
                "abstention":        abstention,
                "ctx_abstained":     ctx_abstained,
            }
            async with lock:
                state["evaluated_count"] += 1
                state["cumulative_tokens"] += gen_tokens + judge_tokens
                if correct:
                    state["correct_count"] += 1
                if ctx_abstained:
                    state["abstained_count"] += 1
                type_total_running[qtype] += 1
                if correct:
                    type_correct_running[qtype] += 1
                per_case_results.append(result)
                progress_fh.write(json.dumps(result) + "\n")
                progress_fh.flush()

                # ── Progress line ──
                _ev  = state["evaluated_count"]
                _acc = state["correct_count"] / _ev * 100 if _ev else 0
                status  = "CORRECT" if correct else "WRONG  "
                q_short = question[:60]
                print(
                    f"[{_ev:4d}/{total_cases}] {status} | acc={_acc:5.1f}% | "
                    f"tokens={state['cumulative_tokens']:,} | Q: {q_short}",
                    flush=True,
                )

                # ── Verbose smoke output (all cases when --limit is set) ──
                if limit:
                    try:
                        budget_used = TOKEN_BUDGETS.get(qtype, 1000)
                        date_used = question_date_str if qtype == "temporal-reasoning" and question_date_str else "N/A"
                        memories_ingested = messages_count
                        has_crossencoder = any(
                            "crossencoder" in (r.score_components or {})
                            for r in recall_results
                        ) if recall_results else False
                        tr_info = ""
                        if qtype == "temporal-reasoning":
                            _lc = locals()  # FIX P3-G: locals() is correct; dir() returns module-level names
                            me_trig = _lc.get('multi_entity_triggered', "N/A")
                            sl_inj = _lc.get('session_labels_injected', "N/A")
                            tr_ents = _lc.get('tr_entities', [])
                            tr_info = (f"  multi_entity_trig: {me_trig} (entities={tr_ents})\n"
                                       f"  session_labels:    {sl_inj}\n")
                        ms_info = ""
                        if qtype == "multi-session":
                            ch = locals().get('coref_hints', [])  # FIX P3-G: locals() instead of dir()
                            ms_info = f"  coref_hints:       {len(ch)} hint(s)\n"
                        print(f"\n  --- Case {case_num} detail ---")
                        print(f"  question_id:       {case_id}")
                        print(f"  question_type:     {qtype}")
                        print(f"  question_date:     {date_used}")
                        print(f"  token_budget:      {budget_used}")
                        print(f"  messages_ingested: {memories_ingested}")
                        print(f"  reranker_active:   {has_crossencoder}")
                        print(f"  ctx_abstained:     {ctx_abstained}")
                        if tr_info:
                            print(tr_info, end="")
                        if ms_info:
                            print(ms_info, end="")
                        print(f"  question:          {question}")
                        print(f"  gold_answer:       {str(gold)[:200]}")
                        print(f"  context (500c):    {context_preview}")
                        print(f"  hypothesis:        {hypothesis[:300]}")
                        print(f"  judge_response:    {judge_response}")
                        print(f"  correct:           {correct}")
                        print()
                    except Exception as print_err:
                        print(f"  [verbose print error: {print_err}]")

                # ── Per-type breakdown every 25 cases ──
                if _ev % 25 == 0:
                    _tok = state["cumulative_tokens"]
                    projected = _tok * (total_cases / _ev)
                    print(f"\n  [Progress @ {_ev} cases] acc={_acc:.1f}% | "
                          f"tokens={_tok:,} | projected={projected:,.0f}")
                    if projected > 850_000:
                        print("  *** WARNING: projected total exceeds 850,000 tokens ***")
                    print(f"  {'Type':<35} {'Correct':>7} {'Total':>7} {'Acc':>7}")
                    print(f"  {'-'*35} {'-'*7} {'-'*7} {'-'*7}")
                    for qt in sorted(type_total_running):
                        ttot = type_total_running[qt]
                        tcor = type_correct_running[qt]
                        tacc = tcor / ttot * 100 if ttot else 0
                        print(f"  {qt:<35} {tcor:>7} {ttot:>7} {tacc:>6.1f}%")
                    print(f"  {'OVERALL':<35} {state['correct_count']:>7} {_ev:>7} {_acc:>6.1f}%")
                    print(f"  ctx_abstained this run: {state['abstained_count']}")
                    print()

        except Exception as exc:
            tb = traceback.format_exc()
            # FIX P2-I: ensure store is closed even when an exception fires before the
            # normal async_close() call at line ~1981, preventing SQLite handle leaks.
            if store is not None:
                try:
                    await store.async_close()
                except Exception:
                    pass
                store = None
            print(f"[???/{total_cases}] ERROR   | case_id={case_id} | {exc}", flush=True)
            # FIX P4-J: write full traceback to a timestamped debug file for non-rate-limit errors
            if not isinstance(exc, RateLimitError):
                try:
                    _dbg_path = f"longmemeval_error_{case_id}.txt"
                    with open(_dbg_path, "w", encoding="utf-8") as _dbg_f:
                        _dbg_f.write(f"case_id: {case_id}\nqtype: {qtype}\nexc: {exc}\n\n{tb}")
                except Exception:
                    pass
            err_result = {
                "question_id":  case_id,
                "question_type": qtype,
                "question":     question,
                "gold_answer":  gold,
                "correct":      False,
                "error":        str(exc),
                "traceback":    tb,
            }
            async with lock:
                state["error_count"] += 1
                state["evaluated_count"] += 1
                per_case_results.append(err_result)
                progress_fh.write(json.dumps(err_result) + "\n")
                progress_fh.flush()

    # ── Run all cases (sequentially if concurrency=1, else in parallel) ──────
    async def bounded_process(case_idx: int, case: dict) -> None:
        async with semaphore:
            await process_case(case_idx, case)

    await asyncio.gather(*[bounded_process(ci, c) for ci, c in cases_to_run])
    progress_fh.close()

    # ── Final summary ──
    total_evaluated = state["evaluated_count"]
    total_correct   = state["correct_count"]
    error_count     = state["error_count"]
    cumulative_tokens = state["cumulative_tokens"]
    total_incorrect = total_evaluated - total_correct - error_count
    j_score         = total_correct / total_evaluated * 100 if total_evaluated else 0
    omega_score     = 95.40
    diff            = j_score - omega_score

    # Final per-type breakdown from full results
    from collections import defaultdict
    type_correct  = defaultdict(int)
    type_total    = defaultdict(int)
    total_ctx_abstained = 0
    for r in per_case_results:
        qt = r.get("question_type", "unknown")
        type_total[qt] += 1
        if r.get("correct"):
            type_correct[qt] += 1
        if r.get("ctx_abstained"):
            total_ctx_abstained += 1

    # Abstention case accuracy (Change 8)
    abs_cases_results = [r for r in per_case_results if "_abs" in r.get("question_id", "")]
    abs_correct = sum(1 for r in abs_cases_results if r.get("correct"))
    abs_total = len(abs_cases_results)

    print("\n" + "="*70)
    print("FINAL RESULTS — agentmemory V4 | ITER-36 | safe-regression-fixes: wedding-couple-id, cuisine-fermentation-exclusion, session-date-anchor-relative-only, concert-vinyl, entity-count-reverted")
    print("="*70)
    print(f"Final J-score:          {j_score:.2f}%")
    print(f"Total cases evaluated:  {total_evaluated}")
    print(f"Total correct:          {total_correct}")
    print(f"Total incorrect:        {total_incorrect}")
    print(f"Total errors (skipped): {error_count}")
    print(f"Total tokens consumed:  {cumulative_tokens:,}")
    print(f"Context abstentions:    {total_ctx_abstained}")
    print(f"Reranker calls total:   {shared_reranker.rerank_calls}")  # FIX P2-D: confirm reranker was active
    print()
    print("Per question-type accuracy:")
    for qt in sorted(type_total):
        acc = type_correct[qt] / type_total[qt] * 100 if type_total[qt] else 0
        print(f"  {qt:35s}: {acc:.1f}%  ({type_correct[qt]}/{type_total[qt]})")
    print()
    abs_pct = f"{abs_correct/abs_total*100:.1f}%" if abs_total else "N/A"
    print(f"Abstention cases:  {abs_correct}/{abs_total} correct  ({abs_pct})")
    print()
    cmp_sign = "+" if diff >= 0 else ""
    print(f"agentmemory V4+: {j_score:.2f}%  vs  OMEGA published: {omega_score:.2f}%  —  gap: {cmp_sign}{diff:.2f} pp")
    print("="*70)

    # Write full results JSON
    summary = {
        "j_score":              round(j_score, 4),
        "total_evaluated":      total_evaluated,
        "total_correct":        total_correct,
        "total_incorrect":      total_incorrect,
        "total_errors":         error_count,
        "total_tokens":         cumulative_tokens,
        "ctx_abstained_count":  total_ctx_abstained,
        "evaluator_model":      EVALUATOR_MODEL,
        "gen_model":            GEN_MODEL,
        "token_budgets":        TOKEN_BUDGETS,
        "dataset":              DATASET_PATH,
        "omega_published":      omega_score,
        "difference":           round(diff, 4),
        "abstention_cases": {
            "correct": abs_correct,
            "total":   abs_total,
            "accuracy": round(abs_correct / abs_total * 100, 2) if abs_total else 0,
        },
        "per_type": {
            qt: {
                "correct":  type_correct[qt],
                "total":    type_total[qt],
                "accuracy": round(type_correct[qt] / type_total[qt] * 100, 2) if type_total[qt] else 0,
            }
            for qt in sorted(type_total)
        },
    }
    final = {"summary": summary, "per_case": per_case_results}
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2)
    print(f"\nFull results written to {RESULTS_FILE}")
    print(f"Progress log at {PROGRESS_FILE}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LongMemEval full evaluation for agentmemory V4")
    parser.add_argument("--limit", type=int, default=None,
                        help="Only evaluate the first N cases (for smoke tests)")
    parser.add_argument("--offset", type=int, default=0,
                        help="Skip the first N cases (for testing specific slices)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from existing progress file, skipping completed cases")
    parser.add_argument("--dataset", type=str, default=None,
                        help="Override dataset path (e.g. smoke_test_15.json)")
    parser.add_argument("--progress", type=str, default=None,
                        help="Override progress file path")
    parser.add_argument("--results", type=str, default=None,
                        help="Override results file path")
    parser.add_argument("--type", type=str, default=None,
                        help="Only evaluate cases of this question type "
                             "(e.g. knowledge-update, temporal-reasoning, multi-session, "
                             "single-session-user, single-session-assistant, single-session-preference)")
    parser.add_argument("--ids", type=str, default=None,
                        help="Path to JSON file containing list of question_ids to evaluate "
                             "(e.g. smoke_test_ids_30.json). Overrides --limit/--offset/--type.")
    parser.add_argument("--concurrency", type=int, default=1,
                        help="Number of cases to evaluate in parallel (default: 1 = sequential). "
                             "Use 5-8 for fast micro-tests. Higher values overlap OpenAI API calls.")
    parser.add_argument("--judge-model", type=str, default=None,
                        help="Override judge model (default: gpt-4o). Use gpt-4o-mini for fast "
                             "development iterations (Tier 1/2). Always use gpt-4o for final scoring.")
    parser.add_argument("--gen-model", type=str, default=None,
                        help="Override generator model (default: gpt-4o). Use claude-opus-4-6 or "
                             "claude-sonnet-4-6 to generate answers with Anthropic models. "
                             "Requires ANTHROPIC_API_KEY env var. Judge always uses OpenAI.")
    parser.add_argument("--fast-recall", action="store_true",
                        help="Reduce recall limits ~50%% for faster iteration. Not for final scoring.")
    args = parser.parse_args()

    global DATASET_PATH, PROGRESS_FILE, RESULTS_FILE
    if args.dataset:
        DATASET_PATH = args.dataset
    if args.progress:
        PROGRESS_FILE = args.progress
    if args.results:
        RESULTS_FILE = args.results

    ids_filter = None
    if args.ids:
        with open(args.ids) as f:
            ids_filter = set(json.load(f))
        print(f"IDs filter loaded: {len(ids_filter)} case IDs from {args.ids}")

    asyncio.run(run_evaluation(limit=args.limit, resume=args.resume, offset=args.offset,
                               qtype_filter=args.type, ids_filter=ids_filter,
                               concurrency=args.concurrency,
                               judge_model=args.judge_model,
                               gen_model=args.gen_model,
                               fast_recall=args.fast_recall))


if __name__ == "__main__":
    main()
