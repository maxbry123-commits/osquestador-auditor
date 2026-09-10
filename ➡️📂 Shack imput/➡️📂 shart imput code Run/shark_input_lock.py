from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib, json, re

URL_RE = re.compile(r"https?://[^\s)\]}>]+", re.I)
REPO_RE = re.compile(r"\b(?:github\.com|huggingface\.co)/([^\s/]+)/([^\s/#?]+)", re.I)
VERSION_RE = re.compile(r"\bv?\d+(?:\.\d+){1,3}(?:[-+][A-Za-z0-9._-]+)?\b")

@dataclass(frozen=True)
class InputEnvelope:
    raw: str
    sha256: str
    urls: tuple[str, ...]
    repositories: tuple[str, ...]
    versions: tuple[str, ...]

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, sort_keys=True)


def lock_input(raw: str) -> InputEnvelope:
    if not isinstance(raw, str):
        raise TypeError("INPUT_RAW_MUST_BE_STRING")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    urls = tuple(URL_RE.findall(raw))
    repos = tuple(sorted({f"{a}/{b.rstrip('.,;:')}" for a,b in REPO_RE.findall(raw)}))
    versions = tuple(VERSION_RE.findall(raw))
    return InputEnvelope(raw=raw, sha256=digest, urls=urls, repositories=repos, versions=versions)


def assert_literal_integrity(raw: str, envelope: InputEnvelope) -> None:
    if raw != envelope.raw:
        raise RuntimeError("INPUT_LITERAL_MUTATION")
    if hashlib.sha256(raw.encode("utf-8")).hexdigest() != envelope.sha256:
        raise RuntimeError("INPUT_HASH_MISMATCH")
