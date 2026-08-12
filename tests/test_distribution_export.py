import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORT_PATH = ROOT / "scripts" / "export_distribution.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("export_distribution", EXPORT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ContextEconomyDistributionTests(unittest.TestCase):
    def test_manifest_and_export_publish_seventh_suite(self) -> None:
        exporter = load_exporter()
        manifest = exporter.read_manifest(ROOT)

        self.assertEqual(manifest["version"], "0.4.0")
        self.assertIn("context-economy", manifest["suites"])
        self.assertEqual(len(manifest["suites"]), 7)

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "distribution"
            exporter.build(ROOT, "context-economy", output)

            readme = (output / "README.md").read_text(encoding="utf-8")
            hero = (output / "assets" / "hero.svg").read_text(encoding="utf-8")
            skills = list(output.rglob("SKILL.md"))

            self.assertEqual(len(skills), 7)
            self.assertIn("all seven TIKAZ AI Skills for Codex suites", readme)
            self.assertIn("v0.4.0", hero)
            self.assertEqual((output / "VERSION").read_text(encoding="utf-8"), "0.4.0\n")


if __name__ == "__main__":
    unittest.main()
