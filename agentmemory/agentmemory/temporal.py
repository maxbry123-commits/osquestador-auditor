"""
agentmemory V4 — Temporal grounding.

Resolves relative date language in conversation text into absolute Unix timestamps,
anchored to a provided reference date. Zero external dependencies — uses only
stdlib re and datetime.
"""

from __future__ import annotations

import calendar
import re
from datetime import datetime, timedelta
from typing import Optional


def _safe_ts(dt: datetime) -> Optional[float]:
    """Return dt.timestamp(), or None if the OS rejects the date (e.g., pre-1970 on Windows)."""
    try:
        return dt.timestamp()
    except (OSError, OverflowError, ValueError):
        return None


_MONTH_NAMES = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "aug": 8, "sep": 9, "sept": 9,
    "oct": 10, "nov": 11, "dec": 12,
}

_DAY_NAMES = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
    "mon": 0, "tue": 1, "tues": 1, "wed": 2, "thu": 3, "thur": 3,
    "thurs": 3, "fri": 4, "sat": 5, "sun": 6,
}

_ORDINAL_RE = re.compile(r"(\d+)(?:st|nd|rd|th)")

_WORD_NUMS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "thirty": 30,
}


def _parse_num(s: str) -> Optional[int]:
    s = s.strip().lower()
    if s.isdigit():
        return int(s)
    m = _ORDINAL_RE.match(s)
    if m:
        return int(m.group(1))
    return _WORD_NUMS.get(s)


def _last_weekday(ref: datetime, weekday: int) -> datetime:
    """Return the most recent occurrence of weekday before ref."""
    days_back = (ref.weekday() - weekday) % 7
    if days_back == 0:
        days_back = 7
    return ref - timedelta(days=days_back)


def _next_weekday(ref: datetime, weekday: int) -> datetime:
    """Return the next occurrence of weekday after ref."""
    days_fwd = (weekday - ref.weekday()) % 7
    if days_fwd == 0:
        days_fwd = 7
    return ref + timedelta(days=days_fwd)


class TemporalGrounder:
    """
    Resolves relative date expressions to absolute Unix timestamps.

    Usage:
        g = TemporalGrounder()
        ts = g.resolve("yesterday", reference_date=datetime(2024, 3, 15))
        # returns Unix timestamp for 2024-03-14T00:00:00
    """

    def resolve(self, text: str, reference_date: Optional[datetime] = None) -> Optional[float]:
        """
        Resolve a relative date expression to a Unix timestamp.

        Args:
            text: Natural language date expression.
            reference_date: Anchor date. Defaults to now.

        Returns:
            Unix timestamp (float) or None if unresolvable.
        """
        if reference_date is None:
            reference_date = datetime.now()

        ref = reference_date.replace(hour=0, minute=0, second=0, microsecond=0)
        t = text.strip().lower()

        # === Explicit dates ===

        # "March 15, 2024" or "March 15 2024"
        m = re.match(
            r"(?:on\s+)?(" + "|".join(_MONTH_NAMES) + r")\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})",
            t, re.I)
        if m:
            month = _MONTH_NAMES[m.group(1).lower()]
            day = int(m.group(2))
            year = int(m.group(3))
            try:
                return _safe_ts(datetime(year, month, day))
            except ValueError:
                return None

        # "January 5th" or "March 15" (no year — use ref year, pick closest past)
        m = re.match(
            r"(?:on\s+)?(" + "|".join(_MONTH_NAMES) + r")\s+(\d{1,2})(?:st|nd|rd|th)?$",
            t, re.I)
        if m:
            month = _MONTH_NAMES[m.group(1).lower()]
            day = int(m.group(2))
            try:
                candidate = datetime(ref.year, month, day)
                if candidate > ref:
                    candidate = datetime(ref.year - 1, month, day)
                return _safe_ts(candidate)
            except ValueError:
                return None

        # "the 3rd" — same month, interpret as a day of the current month
        m = re.match(r"(?:the\s+)?(\d{1,2})(?:st|nd|rd|th)$", t, re.I)
        if m:
            day = int(m.group(1))
            try:
                candidate = datetime(ref.year, ref.month, day)
                if candidate > ref:
                    # go to prior month
                    if ref.month == 1:
                        candidate = datetime(ref.year - 1, 12, day)
                    else:
                        candidate = datetime(ref.year, ref.month - 1, day)
                return _safe_ts(candidate)
            except ValueError:
                return None

        # "2024-03-15" ISO format
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", t)
        if m:
            try:
                return _safe_ts(datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))))
            except ValueError:
                return None

        # === Simple relative days ===
        if t in ("yesterday",):
            return _safe_ts((ref - timedelta(days=1)))
        if t in ("today",):
            return _safe_ts(ref)
        if t in ("tomorrow",):
            return _safe_ts((ref + timedelta(days=1)))

        # === Day references: "last Monday", "next Friday", "this weekend" ===
        m = re.match(r"last\s+(" + "|".join(_DAY_NAMES) + r")$", t, re.I)
        if m:
            weekday = _DAY_NAMES[m.group(1).lower()]
            return _safe_ts(_last_weekday(ref, weekday))

        m = re.match(r"next\s+(" + "|".join(_DAY_NAMES) + r")$", t, re.I)
        if m:
            weekday = _DAY_NAMES[m.group(1).lower()]
            return _safe_ts(_next_weekday(ref, weekday))

        if t in ("this weekend",):
            # Saturday of this week
            days_to_sat = (5 - ref.weekday()) % 7
            if days_to_sat == 0:
                days_to_sat = 0  # if today is Saturday, return today
            return _safe_ts((ref + timedelta(days=days_to_sat)))

        # === Week references ===
        if t == "last week":
            return _safe_ts((ref - timedelta(weeks=1)))
        if t == "next week":
            return _safe_ts((ref + timedelta(weeks=1)))

        m = re.match(r"(\w+)\s+weeks?\s+ago", t, re.I)
        if m:
            n = _parse_num(m.group(1))
            if n is not None:
                return _safe_ts((ref - timedelta(weeks=n)))

        m = re.match(r"in\s+(\w+)\s+weeks?$", t, re.I)
        if m:
            n = _parse_num(m.group(1))
            if n is not None:
                return _safe_ts((ref + timedelta(weeks=n)))

        # === Month references ===
        if t == "last month":
            if ref.month == 1:
                return _safe_ts(datetime(ref.year - 1, 12, ref.day))
            else:
                day = min(ref.day, calendar.monthrange(ref.year, ref.month - 1)[1])
                return _safe_ts(datetime(ref.year, ref.month - 1, day))

        if t == "next month":
            if ref.month == 12:
                return _safe_ts(datetime(ref.year + 1, 1, ref.day))
            else:
                day = min(ref.day, calendar.monthrange(ref.year, ref.month + 1)[1])
                return _safe_ts(datetime(ref.year, ref.month + 1, day))

        m = re.match(r"(\w+)\s+months?\s+ago", t, re.I)
        if m:
            n = _parse_num(m.group(1))
            if n is not None:
                year = ref.year
                month = ref.month - n
                while month < 1:
                    month += 12
                    year -= 1
                day = min(ref.day, calendar.monthrange(year, month)[1])
                return _safe_ts(datetime(year, month, day))

        m = re.match(r"in\s+(\w+)\s+months?$", t, re.I)
        if m:
            n = _parse_num(m.group(1))
            if n is not None:
                year = ref.year
                month = ref.month + n
                while month > 12:
                    month -= 12
                    year += 1
                day = min(ref.day, calendar.monthrange(year, month)[1])
                return _safe_ts(datetime(year, month, day))

        # "in January" — month name alone
        m = re.match(r"(?:in\s+)?(" + "|".join(_MONTH_NAMES) + r")$", t, re.I)
        if m:
            month = _MONTH_NAMES[m.group(1).lower()]
            # Most recent occurrence of that month's 1st
            candidate = datetime(ref.year, month, 1)
            if candidate > ref:
                candidate = datetime(ref.year - 1, month, 1)
            return _safe_ts(candidate)

        # === Numeric deltas ===
        # "3 days ago", "two weeks from now", "in 10 days"
        m = re.match(r"(\w+)\s+days?\s+ago", t, re.I)
        if m:
            n = _parse_num(m.group(1))
            if n is not None:
                return _safe_ts((ref - timedelta(days=n)))

        m = re.match(r"in\s+(\w+)\s+days?$", t, re.I)
        if m:
            n = _parse_num(m.group(1))
            if n is not None:
                return _safe_ts((ref + timedelta(days=n)))

        m = re.match(r"(\w+)\s+(?:days?|weeks?)\s+from\s+now", t, re.I)
        if m:
            n = _parse_num(m.group(1))
            if n is not None:
                if "week" in t.lower():
                    return _safe_ts((ref + timedelta(weeks=n)))
                return _safe_ts((ref + timedelta(days=n)))

        m = re.match(r"(\w+)\s+years?\s+ago", t, re.I)
        if m:
            n = _parse_num(m.group(1))
            if n is not None:
                try:
                    return _safe_ts(datetime(ref.year - n, ref.month, ref.day))
                except ValueError:
                    return _safe_ts(datetime(ref.year - n, ref.month, 28))

        return None

    def resolve_all(self, text: str, reference_date: Optional[datetime] = None) -> list[tuple[str, float]]:
        """
        Find and resolve all temporal expressions in a longer text.

        Returns list of (matched_phrase, unix_timestamp) tuples.
        """
        if reference_date is None:
            reference_date = datetime.now()

        results = []
        # Try to find temporal phrases in the text
        patterns = [
            # Explicit dates
            r"(?:on\s+)?(?:" + "|".join(_MONTH_NAMES) + r")\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{4}",
            r"(?:on\s+)?(?:" + "|".join(_MONTH_NAMES) + r")\s+\d{1,2}(?:st|nd|rd|th)?",
            r"\d{4}-\d{2}-\d{2}",
            # Relative
            r"yesterday", r"today", r"tomorrow",
            r"last\s+(?:" + "|".join(_DAY_NAMES) + r")",
            r"next\s+(?:" + "|".join(_DAY_NAMES) + r")",
            r"this\s+weekend",
            r"last\s+week", r"next\s+week",
            r"\w+\s+weeks?\s+ago",
            r"in\s+\w+\s+weeks?",
            r"last\s+month", r"next\s+month",
            r"\w+\s+months?\s+ago",
            r"in\s+\w+\s+months?",
            r"\w+\s+days?\s+ago",
            r"in\s+\w+\s+days?",
            r"\w+\s+(?:days?|weeks?)\s+from\s+now",
            r"\w+\s+years?\s+ago",
        ]

        combined = "|".join(f"({p})" for p in patterns)
        for match in re.finditer(combined, text, re.I):
            phrase = match.group(0)
            ts = self.resolve(phrase, reference_date)
            if ts is not None:
                results.append((phrase, ts))

        return results
