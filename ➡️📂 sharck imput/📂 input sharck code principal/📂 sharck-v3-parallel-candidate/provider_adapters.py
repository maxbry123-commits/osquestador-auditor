from __future__ import annotations

import asyncio
import json
import os
import threading
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Sequence


class HttpJsonClient:
    """Tiny stdlib HTTP JSON client used by SHARCK provider adapters.

    Network I/O runs in a thread so the SHARCK event loop remains non-blocking.
    """

    def __init__(self, timeout_s: float = 15.0, user_agent: str = "sharck-input-v3-candidate/0.1") -> None:
        self.timeout_s = timeout_s
        self.user_agent = user_agent

    def _sync_get(self, url: str, headers: dict[str, str] | None = None) -> Any:
        req_headers = {"Accept": "application/json", "User-Agent": self.user_agent}
        req_headers.update(headers or {})
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:  # nosec: URL is provider-configured
            return json.loads(resp.read().decode("utf-8"))

    async def get(self, url: str, headers: dict[str, str] | None = None) -> Any:
        return await asyncio.to_thread(self._sync_get, url, headers)


class EnvApiKeyPool:
    """Round-robin pool over environment variable names; secret values never persist to disk."""

    def __init__(self, env_names: Sequence[str]) -> None:
        self.env_names = [n for n in env_names if os.getenv(n)]
        self._i = 0
        self._lock = threading.Lock()

    @classmethod
    def numbered(cls, prefix: str, maximum: int = 100) -> "EnvApiKeyPool":
        return cls([f"{prefix}_{i:02d}" for i in range(1, maximum + 1)])

    def next(self) -> tuple[str, str] | None:
        if not self.env_names:
            return None
        with self._lock:
            name = self.env_names[self._i % len(self.env_names)]
            self._i += 1
        return name, os.environ[name]

    @property
    def size(self) -> int:
        return len(self.env_names)


@dataclass
class LocalRouterSearchProvider:
    name: str = "local-router"
    endpoint_env: str = "SHARCK_LOCAL_SEARCH_URL"
    client: HttpJsonClient = HttpJsonClient()

    async def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        endpoint = os.getenv(self.endpoint_env)
        if not endpoint:
            return [{"source": self.name, "error": "LOCAL_ROUTER_NOT_CONFIGURED", "query": query}]
        url = endpoint + ("&" if "?" in endpoint else "?") + urllib.parse.urlencode({"q": query, "limit": limit})
        data = await self.client.get(url)
        rows = data.get("results", data.get("items", [])) if isinstance(data, dict) else data
        return [{"source": self.name, **r} for r in list(rows)[:limit] if isinstance(r, dict)]


@dataclass
class WebApiSearchProvider:
    """Universal web-router adapter.

    Configure `SHARCK_WEB_SEARCH_URL` and up to 100 `SHARCK_WEB_API_KEY_XX` env vars.
    The endpoint must accept `q` and `limit`, and return `results` or `items` JSON.
    """

    name: str = "web-api-router"
    endpoint_env: str = "SHARCK_WEB_SEARCH_URL"
    key_header: str = "Authorization"
    key_prefix: str = "Bearer "
    client: HttpJsonClient = HttpJsonClient()

    def __post_init__(self) -> None:
        self.keys = EnvApiKeyPool.numbered("SHARCK_WEB_API_KEY", 100)

    async def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        endpoint = os.getenv(self.endpoint_env)
        if not endpoint:
            return [{"source": self.name, "error": "WEB_ROUTER_NOT_CONFIGURED", "query": query}]
        url = endpoint + ("&" if "?" in endpoint else "?") + urllib.parse.urlencode({"q": query, "limit": limit})
        headers: dict[str, str] = {}
        pair = self.keys.next()
        if pair:
            _, secret = pair
            headers[self.key_header] = self.key_prefix + secret
        data = await self.client.get(url, headers)
        rows = data.get("results", data.get("items", [])) if isinstance(data, dict) else data
        return [{"source": self.name, **r} for r in list(rows)[:limit] if isinstance(r, dict)]


class HuggingFaceSkillsProvider:
    name = "huggingface-skills"
    CATALOG = "https://raw.githubusercontent.com/huggingface/skills/f3186efbbc322121eb5d0f31e8a1d669ee961159/index/latest/ai-catalog.json"

    def __init__(self, client: HttpJsonClient | None = None) -> None:
        self.client = client or HttpJsonClient()

    async def discover(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        data = await self.client.get(self.CATALOG)
        terms = [t for t in query.lower().split() if len(t) > 2]
        out = []
        for e in data.get("entries", []):
            text = " ".join(str(e.get(k, "")) for k in ("displayName", "description", "tags")).lower()
            score = sum(t in text for t in terms)
            meta = e.get("metadata", {}) or {}
            out.append({
                "id": e.get("identifier"), "name": e.get("displayName"), "description": e.get("description"),
                "url": e.get("url"), "source_repo": "huggingface/skills",
                "source_ref": "f3186efbbc322121eb5d0f31e8a1d669ee961159", "license": "Apache-2.0",
                "digest": meta.get("digest"), "score_hint": score, "trust": 0.95, "freshness": 0.95,
            })
        out.sort(key=lambda x: (x["score_hint"], x.get("name") or ""), reverse=True)
        return out[:limit]


class HuggingFaceDatasetsProvider:
    name = "huggingface-datasets"

    def __init__(self, client: HttpJsonClient | None = None) -> None:
        self.client = client or HttpJsonClient()

    async def discover(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        url = "https://huggingface.co/api/datasets?" + urllib.parse.urlencode({"search": query, "limit": limit, "sort": "downloads"})
        rows = await self.client.get(url)
        return [{
            "id": r.get("id"), "name": r.get("id"), "description": "Hugging Face dataset",
            "url": f"https://huggingface.co/datasets/{r.get('id')}", "downloads": r.get("downloads", 0),
            "likes": r.get("likes", 0), "source_type": "dataset-catalog", "trust": 0.85,
        } for r in rows[:limit] if isinstance(r, dict) and r.get("id")]


class ZenodoDatasetsProvider:
    name = "zenodo"

    def __init__(self, client: HttpJsonClient | None = None) -> None:
        self.client = client or HttpJsonClient()

    async def discover(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        url = "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": query, "size": limit})
        data = await self.client.get(url)
        hits = data.get("hits", {}).get("hits", [])
        return [{
            "id": str(r.get("id")), "name": (r.get("metadata") or {}).get("title"),
            "description": (r.get("metadata") or {}).get("description", "")[:1000],
            "url": (r.get("links") or {}).get("html"), "source_type": "dataset-catalog", "trust": 0.9,
        } for r in hits[:limit] if isinstance(r, dict)]


class DataGovDatasetsProvider:
    name = "data-gov"

    def __init__(self, client: HttpJsonClient | None = None) -> None:
        self.client = client or HttpJsonClient()

    async def discover(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        url = "https://catalog.data.gov/api/3/action/package_search?" + urllib.parse.urlencode({"q": query, "rows": limit})
        data = await self.client.get(url)
        rows = (data.get("result") or {}).get("results", []) if data.get("success") else []
        return [{
            "id": r.get("id"), "name": r.get("title"), "description": r.get("notes", "")[:1000],
            "url": "https://catalog.data.gov/dataset/" + str(r.get("name", "")),
            "source_type": "government-dataset-catalog", "trust": 0.95,
        } for r in rows[:limit] if isinstance(r, dict)]


class McpRegistryProvider:
    name = "official-mcp-registry"

    def __init__(self, client: HttpJsonClient | None = None) -> None:
        self.client = client or HttpJsonClient()

    async def discover(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        # Official Registry API: GET /v0.1/servers?search=...&version=latest
        url = "https://registry.modelcontextprotocol.io/v0.1/servers?" + urllib.parse.urlencode({
            "search": query, "version": "latest", "limit": min(limit, 100)
        })
        data = await self.client.get(url)
        rows = data.get("servers", data.get("items", [])) if isinstance(data, dict) else []
        out = []
        for row in rows[:limit]:
            server = row.get("server", row) if isinstance(row, dict) else {}
            name = server.get("name")
            out.append({
                "id": name, "name": name, "description": server.get("description", ""),
                "url": f"https://registry.modelcontextprotocol.io/?q={urllib.parse.quote(str(name or ''))}",
                "transport": "MCP", "source_type": "official-registry", "trust": 0.95,
                "version": server.get("version"), "packages": server.get("packages"), "remotes": server.get("remotes"),
            })
        return out


async def smoke_catalogs(query: str) -> dict[str, Any]:
    """Optional network smoke; no secrets required for public catalogs."""
    providers = [
        HuggingFaceSkillsProvider(), HuggingFaceDatasetsProvider(), ZenodoDatasetsProvider(),
        DataGovDatasetsProvider(), McpRegistryProvider(),
    ]
    batches = await asyncio.gather(*(p.discover(query, 3) for p in providers), return_exceptions=True)
    return {
        p.name: ({"error": type(r).__name__} if isinstance(r, BaseException) else {"count": len(r), "items": r})
        for p, r in zip(providers, batches)
    }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(smoke_catalogs("research search sdk")), ensure_ascii=False, indent=2))
