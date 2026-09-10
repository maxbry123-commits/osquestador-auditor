import json, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shark_input_lock import lock_input, assert_literal_integrity
from role_router import route_roles
from research_dispatch import build_plan

class SharkCoreTests(unittest.TestCase):
    def test_literal_roundtrip(self):
        raw = "  INPUT literal\nMCP + código áéí\n"
        env = lock_input(raw)
        self.assertEqual(env.raw, raw)
        assert_literal_integrity(raw, env)
        self.assertEqual(lock_input(raw).sha256, env.sha256)
    def test_multi_role(self):
        roles = {r['role'] for r in route_roles('Diseña UI en React y analiza video YouTube')}
        self.assertIn('software_architect', roles)
        self.assertIn('ui_ux_designer', roles)
        self.assertIn('video_engineer', roles)
    def test_registry_count(self):
        data = json.loads((ROOT/'community_registry.json').read_text())
        self.assertGreaterEqual(len(data['sources']), 50)
    def test_plan(self):
        plan = build_plan('Necesito arquitectura Python MCP en GitHub')
        self.assertEqual(plan['schema'], 'wanted-shark.prellm.plan.v1')
        self.assertTrue(plan['llm_policy']['focus_ai_cannot_mutate_input_raw'])

if __name__ == '__main__':
    unittest.main()
