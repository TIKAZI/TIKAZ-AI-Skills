import importlib.util
import re
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
    def test_every_suite_declares_four_bilingual_proof_items(self) -> None:
        exporter = load_exporter()
        manifest = exporter.read_manifest(ROOT)

        for suite, info in manifest["suites"].items():
            with self.subTest(suite=suite):
                self.assertEqual(len(info["proofs"]), 4)
                for proof in info["proofs"]:
                    self.assertTrue(proof["value"].strip())
                    self.assertTrue(proof["label_en"].strip())
                    self.assertTrue(proof["label_zh"].strip())
                    self.assertTrue(proof["note_en"].strip())
                    self.assertTrue(proof["note_zh"].strip())

    def test_borderless_proof_strip_renders_before_suite_introduction_in_both_languages(self) -> None:
        exporter = load_exporter()
        manifest = exporter.read_manifest(ROOT)

        with tempfile.TemporaryDirectory() as temp_dir:
            for suite, info in manifest["suites"].items():
                output = Path(temp_dir) / suite
                exporter.build(ROOT, suite, output)
                readme = (output / "README.md").read_text(encoding="utf-8")
                chinese_readme = (output / "README.zh-CN.md").read_text(encoding="utf-8")
                proof_svg = (output / "assets" / "proof-strip.svg").read_text(encoding="utf-8")
                proof_svg_zh = (output / "assets" / "proof-strip.zh-CN.svg").read_text(encoding="utf-8")

                with self.subTest(suite=suite):
                    self.assertIn('src="assets/proof-strip.svg"', readme)
                    self.assertIn('src="assets/proof-strip.zh-CN.svg"', chinese_readme)
                    self.assertNotIn("<table", readme)
                    self.assertNotIn("<table", chinese_readme)
                    self.assertNotIn("\n---\n\n## ✨ One suite", readme)
                    self.assertEqual(proof_svg.count('class="proof"'), 4)
                    self.assertEqual(proof_svg_zh.count('class="proof"'), 4)
                    self.assertNotIn("<rect", proof_svg)
                    self.assertNotIn("<line", proof_svg)
                    self.assertIn("font: 750 54px", proof_svg)
                    self.assertIn("font: 600 24px", proof_svg)
                    self.assertLess(readme.index('assets/proof-strip.svg'), readme.index("## ✨ One suite"))
                    for proof in info["proofs"]:
                        self.assertIn(proof["value"], proof_svg)
                        self.assertIn(proof["value"], proof_svg_zh)
                        self.assertIn(proof["label_en"], proof_svg)
                        self.assertIn(proof["label_zh"], proof_svg_zh)

    def test_distribution_hero_keeps_button_and_version_text_inside_centered_containers(self) -> None:
        exporter = load_exporter()
        svg = exporter.hero_svg("TIKAZ Visual Content for Codex", "Provider-neutral publishing workflow.", "F472B6", "0.8.0")

        button = re.search(r'<rect id="install-button" x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"', svg)
        button_text = re.search(r'<text id="install-label" x="(\d+)" y="(\d+)"[^>]*text-anchor="middle"', svg)
        version = re.search(r'<rect id="version-badge" x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"', svg)
        version_text = re.search(r'<text id="version-label" x="(\d+)" y="(\d+)"[^>]*text-anchor="middle"', svg)

        self.assertIsNotNone(button)
        self.assertIsNotNone(button_text)
        self.assertIsNotNone(version)
        self.assertIsNotNone(version_text)
        self.assertEqual(int(button_text.group(1)), int(button.group(1)) + int(button.group(3)) // 2)
        self.assertEqual(int(version_text.group(1)), int(version.group(1)) + int(version.group(3)) // 2)
        self.assertGreaterEqual(int(button.group(3)), 300)
        self.assertLessEqual(int(version.group(1)) + int(version.group(3)), 1354)

    def test_manifest_and_export_publish_seventh_suite(self) -> None:
        exporter = load_exporter()
        manifest = exporter.read_manifest(ROOT)

        self.assertEqual(manifest["version"], "0.9.0")
        self.assertIn("context-economy", manifest["suites"])
        self.assertEqual(len(manifest["suites"]), 7)

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "distribution"
            exporter.build(ROOT, "context-economy", output)

            readme = (output / "README.md").read_text(encoding="utf-8")
            chinese_readme = (output / "README.zh-CN.md").read_text(encoding="utf-8")
            hero = (output / "assets" / "hero.svg").read_text(encoding="utf-8")
            skills = list(output.rglob("SKILL.md"))

            self.assertEqual(len(skills), 5)
            self.assertIn("all seven TIKAZ AI Skills for Codex suites", readme)
            self.assertIn("v0.9.0", hero)
            self.assertIn("简体中文", readme)
            self.assertIn("English", chinese_readme)
            self.assertIn("](SOURCES.yml)", chinese_readme)
            self.assertNotIn("../../SOURCES.yml", chinese_readme)
            self.assertIn("https://tikazi.github.io/TIKAZ-AI-Skills/skills/context-pack/index.html", readme)
            self.assertIn("https://tikazi.github.io/TIKAZ-AI-Skills/zh/skills/context-pack/index.html", chinese_readme)
            self.assertEqual((output / "VERSION").read_text(encoding="utf-8"), "0.9.0\n")
            self.assertIn("*.pdf binary", (output / ".gitattributes").read_text(encoding="utf-8"))
            self.assertIn(
                "288499007+TIKAZI@users.noreply.github.com",
                (output / ".mailmap").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "https://github.com/TIKAZI",
                (output / "MAINTAINERS.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                'git config user.name "TIKAZ"',
                (output / ".github" / "workflows" / "sync.yml").read_text(encoding="utf-8"),
            )
            self.assertIn(
                'git config user.email "288499007+TIKAZI@users.noreply.github.com"',
                (output / ".github" / "workflows" / "sync.yml").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
