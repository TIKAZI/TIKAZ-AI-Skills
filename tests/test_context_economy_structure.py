import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "suites" / "context-economy"


class ContextEconomyStructureTests(unittest.TestCase):
    def test_suite_contains_orchestrator_and_six_children(self) -> None:
        expected_skills = {
            "context-economy": SUITE / "SKILL.md",
            "content-intake": SUITE / "content-intake" / "SKILL.md",
            "context-ledger": SUITE / "context-ledger" / "SKILL.md",
            "context-budget": SUITE / "context-budget" / "SKILL.md",
            "relevance-gate": SUITE / "relevance-gate" / "SKILL.md",
            "context-packager": SUITE / "context-packager" / "SKILL.md",
            "conversation-checkpoint": SUITE / "conversation-checkpoint" / "SKILL.md",
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

    def test_suite_support_files_exist(self) -> None:
        expected = [
            SUITE / "README.md",
            SUITE / "references" / "routing.md",
            SUITE / "references" / "output-contract.md",
            SUITE / "agents" / "openai.yaml",
            SUITE / "scripts" / "context_economy.py",
        ]
        expected.extend(SUITE.glob("*/agents/openai.yaml"))

        for path in expected:
            self.assertTrue(path.is_file(), f"missing suite support file: {path}")

    def test_workflow_anchors_clear_the_fixed_header(self) -> None:
        styles = (ROOT / "docs" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("scroll-margin-top:90px", styles)


if __name__ == "__main__":
    unittest.main()
