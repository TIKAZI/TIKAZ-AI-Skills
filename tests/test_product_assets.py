import importlib.util
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_product_assets.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_product_assets", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ProductAssetTests(unittest.TestCase):
    def test_every_skill_is_listed_in_catalog_and_bilingual_suite_readmes(self) -> None:
        skill_files = sorted((ROOT / "suites").rglob("SKILL.md"))
        self.assertEqual(len(skill_files), 30)
        catalog = (ROOT / "docs" / "skills-catalog.md").read_text(encoding="utf-8")
        catalog_names = set(re.findall(r"\| \[`([a-z0-9-]+)`\]\(", catalog))
        skill_names = {}
        for skill_file in skill_files:
            content = skill_file.read_text(encoding="utf-8")
            match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", content)
            self.assertIsNotNone(match, skill_file)
            skill_names[skill_file] = match.group(1)
        self.assertEqual(catalog_names, set(skill_names.values()))

        for suite_dir in sorted(path for path in (ROOT / "suites").iterdir() if path.is_dir()):
            expected = {name for path, name in skill_names.items() if suite_dir in path.parents}
            for readme_name in ("README.md", "README.zh-CN.md"):
                readme = (suite_dir / readme_name).read_text(encoding="utf-8")
                for name in expected:
                    self.assertRegex(readme, rf"(?<![a-z0-9-])`{re.escape(name)}`(?![a-z0-9-])", f"{suite_dir.name}/{readme_name}: {name}")

        public_entries = (
            ROOT / "README.md", ROOT / "README.zh-CN.md",
            ROOT / "docs" / "index.html", ROOT / "docs" / "zh" / "index.html",
        )
        for document in public_entries:
            content = document.read_text(encoding="utf-8")
            for name in skill_names.values():
                self.assertRegex(content, rf"(?<![a-z0-9-]){re.escape(name)}(?![a-z0-9-])", f"{document}: {name}")

    def test_generate_catalog_and_suite_workflows(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            generator.generate(ROOT, output)

            catalog = (output / "skills-catalog.md").read_text(encoding="utf-8")
            self.assertIn("30 independently installable Skills", catalog)
            self.assertIn("`context-pack`", catalog)
            self.assertIn("Designed, integrated", catalog)

            workflows = list((output / "diagrams").glob("*-workflow.svg"))
            self.assertEqual(len(workflows), 7)
            context = (output / "diagrams" / "context-economy-workflow.svg").read_text(encoding="utf-8")
            self.assertIn("#60A5FA", context)
            self.assertIn("<title id=", context)
            self.assertIn("<desc id=", context)
            self.assertNotIn("filter=", context)

    def test_generated_assets_are_deterministic(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            generator.generate(ROOT, Path(first))
            generator.generate(ROOT, Path(second))
            first_files = sorted(path.relative_to(first) for path in Path(first).rglob("*") if path.is_file())
            second_files = sorted(path.relative_to(second) for path in Path(second).rglob("*") if path.is_file())
            self.assertEqual(first_files, second_files)
            for relative in first_files:
                self.assertEqual((Path(first) / relative).read_bytes(), (Path(second) / relative).read_bytes())

    def test_metadata_contract_is_valid(self) -> None:
        generator = load_generator()
        metadata = generator.metadata_yaml("academic-research", "Plan literature reviews and synthesize evidence.")
        self.assertIn('display_name: "TIKAZ Academic Research"', metadata)
        self.assertIn('default_prompt: "Use $academic-research', metadata)
        self.assertNotIn("\n  brand_color:", metadata)


if __name__ == "__main__":
    unittest.main()
