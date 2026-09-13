import asyncio
import os

from provider_adapters import (
    DataGovDatasetsProvider,
    EnvApiKeyPool,
    HuggingFaceSkillsProvider,
    McpRegistryProvider,
    ZenodoDatasetsProvider,
)


class FakeClient:
    def __init__(self, payload):
        self.payload = payload
        self.urls = []

    async def get(self, url, headers=None):
        self.urls.append((url, headers or {}))
        return self.payload


def test_hf_skills_parser_pins_source():
    payload = {"entries": [{
        "identifier": "urn:hf:test", "displayName": "hf-test", "description": "research sdk",
        "url": "skill://hf-test/SKILL.md", "metadata": {"digest": "sha256:abc"},
    }]}
    p = HuggingFaceSkillsProvider(FakeClient(payload))
    rows = asyncio.run(p.discover("research sdk", 5))
    assert rows[0]["source_repo"] == "huggingface/skills"
    assert rows[0]["source_ref"] == "f3186efbbc322121eb5d0f31e8a1d669ee961159"
    assert rows[0]["license"] == "Apache-2.0"


def test_dataset_and_mcp_parsers():
    zen = ZenodoDatasetsProvider(FakeClient({"hits": {"hits": [{"id": 1, "metadata": {"title": "T", "description": "D"}, "links": {"html": "https://z/1"}}]}}))
    assert asyncio.run(zen.discover("sdk", 3))[0]["name"] == "T"

    gov = DataGovDatasetsProvider(FakeClient({"success": True, "result": {"results": [{"id": "1", "title": "G", "notes": "N", "name": "g"}]}}))
    assert asyncio.run(gov.discover("sdk", 3))[0]["url"].endswith("/g")

    mcp_payload = {"servers": [{"server": {"name": "io.test/server", "description": "SDK search", "version": "1.0.0"}}]}
    mcp = McpRegistryProvider(FakeClient(mcp_payload))
    row = asyncio.run(mcp.discover("sdk", 3))[0]
    assert row["transport"] == "MCP"
    assert row["trust"] == 0.95


def test_api_key_pool_reads_only_configured_envs():
    os.environ["SHARCK_TEST_KEY_01"] = "secret-a"
    os.environ["SHARCK_TEST_KEY_03"] = "secret-c"
    pool = EnvApiKeyPool.numbered("SHARCK_TEST_KEY", 3)
    assert pool.size == 2
    assert pool.next()[0] == "SHARCK_TEST_KEY_01"
    assert pool.next()[0] == "SHARCK_TEST_KEY_03"
    del os.environ["SHARCK_TEST_KEY_01"]
    del os.environ["SHARCK_TEST_KEY_03"]


if __name__ == "__main__":
    test_hf_skills_parser_pins_source()
    test_dataset_and_mcp_parsers()
    test_api_key_pool_reads_only_configured_envs()
    print("3 provider tests PASS")
