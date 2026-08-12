import re
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "suites" / "context-economy"


class ContextEconomyStructureTests(unittest.TestCase):
    def test_suite_contains_orchestrator_and_four_children(self) -> None:
        expected_skills = {
            "context-economy": SUITE / "SKILL.md",
            "context-pack": SUITE / "context-pack" / "SKILL.md",
            "conversation-checkpoint": SUITE / "conversation-checkpoint" / "SKILL.md",
            "context-audit": SUITE / "context-audit" / "SKILL.md",
            "context-benchmark": SUITE / "context-benchmark" / "SKILL.md",
        }

        for name, path in expected_skills.items():
            self.assertTrue(path.is_file(), f"missing Skill: {path}")
            content = path.read_text(encoding="utf-8")
            self.assertRegex(content, rf"(?m)^name:\s*{re.escape(name)}\s*$")
            self.assertRegex(
                content,
                r"(?is)designed.{0,100}integrated.{0,100}independently\s+refactored"
                r".{0,100}continuously\s+maintained.{0,60}TIKAZ",
            )

        actual = {
            path.parent.name if path.parent != SUITE else "context-economy"
            for path in SUITE.glob("**/SKILL.md")
        }
        self.assertEqual(actual, set(expected_skills))

    def test_suite_support_files_exist(self) -> None:
        expected = [
            SUITE / "README.md",
            SUITE / "references" / "routing.md",
            SUITE / "references" / "output-contract.md",
            SUITE / "references" / "benchmark-method.md",
            SUITE / "references" / "conversion-adapters.md",
            SUITE / "references" / "context-health.md",
            SUITE / "agents" / "openai.yaml",
            SUITE / "scripts" / "tikaz_context.py",
        ]
        expected.extend(SUITE.glob("*/agents/openai.yaml"))

        for path in expected:
            self.assertTrue(path.is_file(), f"missing suite support file: {path}")

    def test_public_benchmark_has_at_least_thirty_versioned_cases(self) -> None:
        manifest_path = SUITE / "benchmarks" / "manifest.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        self.assertGreaterEqual(len(manifest["cases"]), 30)
        categories = {case["category"] for case in manifest["cases"]}
        self.assertTrue({"chinese", "english", "code", "log", "conversation", "long-form", "structured"} <= categories)

    def test_workflow_anchors_clear_the_fixed_header(self) -> None:
        styles = (ROOT / "docs" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("scroll-margin-top:90px", styles)


if __name__ == "__main__":
    unittest.main()
