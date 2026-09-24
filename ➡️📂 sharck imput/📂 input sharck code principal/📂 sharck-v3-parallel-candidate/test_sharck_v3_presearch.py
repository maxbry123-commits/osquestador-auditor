from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import sharck_v3_presearch as p


class PresearchBridgeTests(unittest.TestCase):
    def test_native_presearch_pass_no_hf(self):
        packet = {
            "run_id": "rp-test",
            "input": {"verbatim_preserved": True},
            "records": [{
                "source_id": "github",
                "source_kind": "code",
                "source_weight": 1.0,
                "title": "Example",
                "url": "https://github.com/example/example",
                "snippet": "evidence",
                "provider": "github_api",
                "score": 100.0,
                "estimated_tokens": 10,
            }],
            "sources_requested": ["github", "stackoverflow"],
            "source_status": {"github": {"state": "PASS", "results": 1}},
            "context_packet": "packet.json",
            "context_md": "context.md",
            "cache_state": "MISS",
            "estimated_context_tokens": 10,
            "llm_used": False,
        }
        spec = SimpleNamespace(raw="INPUT literal")
        with tempfile.TemporaryDirectory() as td:
            with patch.object(p, "_run_prepass_sync", return_value=packet):
                result = asyncio.run(p.native_presearch_lane(spec, Path(td)))
        self.assertEqual(result.status, "PASS")
        self.assertEqual(len(result.evidence), 1)
        self.assertTrue(result.metrics["no_hf"])
        self.assertFalse(result.metrics["llm_used"])

    def test_native_presearch_fail_closed(self):
        spec = SimpleNamespace(raw="INPUT literal")
        with tempfile.TemporaryDirectory() as td:
            with patch.object(p, "_run_prepass_sync", side_effect=RuntimeError("network")):
                result = asyncio.run(p.native_presearch_lane(spec, Path(td)))
        self.assertEqual(result.status, "GAP")
        self.assertTrue(any(x.startswith("presearch_exception:") for x in result.gaps))


if __name__ == "__main__":
    unittest.main()
