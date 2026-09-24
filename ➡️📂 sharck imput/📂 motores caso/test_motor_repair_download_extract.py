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

    def test_source_has_no_actions_or_hf_jobs(self):
        text = MODULE.read_text(encoding="utf-8")
        self.assertNotIn("workflow_dispatch", text)
        self.assertNotIn("run_job", text)
        self.assertIn('"git", "add", "-f"', text)
        self.assertIn("CANONICAL_ENGINE_PATH", text)


if __name__ == "__main__":
    unittest.main()
