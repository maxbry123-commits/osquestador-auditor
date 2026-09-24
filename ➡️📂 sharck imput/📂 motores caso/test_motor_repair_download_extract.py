from __future__ import annotations

import importlib.util
import pathlib
import tempfile
import unittest

MODULE = pathlib.Path(__file__).with_name("motor_repair_download_extract.py")
spec = importlib.util.spec_from_file_location("motor_repair_download_extract", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


class RepairMotorTests(unittest.TestCase):
    def test_materializes_in_root_file_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            target = root / "source.txt"
            target.write_text("same-bytes", encoding="utf-8")
            link = root / "copy.txt"
            link.symlink_to(target.name)
            self.assertEqual(mod.deref_in_root(root), 1)
            self.assertFalse(link.is_symlink())
            self.assertEqual(link.read_bytes(), target.read_bytes())

    def test_materializes_in_root_directory_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            target = root / "real"
            target.mkdir()
            (target / "a.txt").write_text("a", encoding="utf-8")
            link = root / "alias"
            link.symlink_to(target.name, target_is_directory=True)
            self.assertEqual(mod.deref_in_root(root), 1)
            self.assertTrue((link / "a.txt").is_file())
            self.assertFalse(link.is_symlink())

    def test_rejects_escape_symlink(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside:
            root = pathlib.Path(td)
            ext = pathlib.Path(outside) / "outside.txt"
            ext.write_text("secret", encoding="utf-8")
            (root / "escape").symlink_to(ext)
            with self.assertRaisesRegex(RuntimeError, "SYMLINK_ESCAPES_TREE"):
                mod.deref_in_root(root)

    def test_materializes_gitlink_contract(self):
        class FakeEngine:
            def __init__(self, root):
                self.root = root
                self.calls = []
            def run(self, argv, cwd=None, env=None, check=True):
                self.calls.append(list(argv))
                if argv[:3] == ["git", "ls-files", "--stage"]:
                    return "160000 deadbeef 0\tlexbor"
                if argv[:4] == ["git", "submodule", "update", "--init"]:
                    d = self.root / "lexbor"
                    d.mkdir(exist_ok=True)
                    (d / "README").write_text("ok", encoding="utf-8")
                return ""
            def no_lfs(self, directory):
                self.calls.append(["no_lfs", str(directory)])

        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / ".gitmodules").write_text('[submodule "lexbor"]\npath = lexbor\nurl = https://example.invalid/lexbor\n', encoding="utf-8")
            eng = FakeEngine(root)
            self.assertEqual(mod.materialize_gitlinks(root, eng), 1)
            self.assertTrue((root / "lexbor" / "README").is_file())
            self.assertTrue(any(call[:3] == ["git", "submodule", "update"] for call in eng.calls))

    def test_source_has_no_actions_or_hf_jobs(self):
        text = MODULE.read_text(encoding="utf-8")
        self.assertNotIn("workflow_dispatch", text)
        self.assertNotIn("run_job", text)
        self.assertIn('"git", "add", "-f"', text)
        self.assertIn("CANONICAL_ENGINE_PATH", text)
        self.assertIn('"submodule", "update"', text)


if __name__ == "__main__":
    unittest.main()
