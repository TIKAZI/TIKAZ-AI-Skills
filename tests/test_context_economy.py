import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "suites" / "context-economy" / "scripts" / "context_economy.py"


def load_context_economy():
    if not MODULE_PATH.is_file():
        raise AssertionError(f"missing implementation: {MODULE_PATH}")
    spec = importlib.util.spec_from_file_location("context_economy", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ContextEconomyPrimitiveTests(unittest.TestCase):
    def test_estimate_tokens_handles_empty_ascii_and_cjk(self) -> None:
        ce = load_context_economy()

        self.assertEqual(ce.estimate_tokens(""), 0)
        self.assertGreater(ce.estimate_tokens("release version 2.4.1"), 0)
        self.assertGreaterEqual(ce.estimate_tokens("上下文经济"), 5)

    def test_split_markdown_creates_stable_unique_heading_anchors(self) -> None:
        ce = load_context_economy()
        text = "# Project Plan\nAlpha.\n\n## Risks\nOne.\n\n## Risks\nTwo."

        chunks = ce.split_markdown(text, "plan.md")

        self.assertEqual([chunk.anchor for chunk in chunks], ["project-plan", "risks", "risks-2"])
        self.assertTrue(all(chunk.source == "plan.md" for chunk in chunks))

    def test_split_markdown_keeps_fenced_code_in_one_chunk(self) -> None:
        ce = load_context_economy()
        text = "# Command\nRun exactly:\n\n```powershell\ngit status\ngit diff\n```\n\nDo not edit it."

        chunks = ce.split_markdown(text, "runbook.md")

        self.assertEqual(len(chunks), 1)
        self.assertIn("```powershell\ngit status\ngit diff\n```", chunks[0].text)

    def test_deduplicate_chunks_removes_only_exact_content(self) -> None:
        ce = load_context_economy()
        first = ce.split_markdown("# Rule\nKeep 42 days.", "a.md")[0]
        duplicate = ce.split_markdown("# Rule\nKeep 42 days.", "b.md")[0]
        different = ce.split_markdown("# Rule\nKeep 43 days.", "c.md")[0]

        unique, duplicates = ce.deduplicate_chunks([first, duplicate, different])

        self.assertEqual(len(unique), 2)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0]["duplicate_source"], "b.md")
        self.assertEqual(duplicates[0]["canonical_source"], "a.md")

    def test_rank_chunks_is_task_aware_and_deterministic(self) -> None:
        ce = load_context_economy()
        chunks = []
        chunks += ce.split_markdown("# License\nThe project uses MIT.", "legal.md")
        chunks += ce.split_markdown("# Deploy\nRun the release validation before deployment.", "release.md")

        first = ce.rank_chunks(chunks, "release deployment validation")
        second = ce.rank_chunks(chunks, "release deployment validation")

        self.assertEqual(first[0].source, "release.md")
        self.assertEqual([(c.source, c.anchor) for c in first], [(c.source, c.anchor) for c in second])

    def test_choose_mode_uses_break_even_and_stable_reuse(self) -> None:
        ce = load_context_economy()

        self.assertEqual(ce.choose_mode(300, 500, 0, 20), "pass-through")
        self.assertEqual(ce.choose_mode(3000, 800, 100, 80), "select")
        self.assertEqual(ce.choose_mode(3000, 800, 1600, 80), "compact")
        self.assertEqual(
            ce.choose_mode(3000, 800, 100, 80, reuse_count=5, stable_prefix=True),
            "cache-stable",
        )


class ContextEconomyPipelineTests(unittest.TestCase):
    def test_repository_demo_has_positive_end_to_end_context_saving(self) -> None:
        ce = load_context_economy()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = ce.build_pack(
                [
                    ROOT / "examples" / "context-economy-source.md",
                    ROOT / "examples" / "context-economy-extra.md",
                ],
                query="release version 0.4.0 validation tests commands evidence anchors",
                budget_tokens=180,
                output_dir=Path(temp_dir) / "artifacts",
            )

            self.assertLess(result.packed_tokens, result.source_tokens)

    def test_build_pack_writes_smaller_stable_anchored_artifacts(self) -> None:
        ce = load_context_economy()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "release.md"
            second = root / "duplicate.md"
            output = root / ".context-economy"
            first.write_text(
                "# Deployment\n"
                "Release version 2.4.1 only after validation.\n"
                "Source: https://example.com/release\n\n"
                "```powershell\npython -m unittest discover -s tests -v\n```\n\n"
                "# Background\n"
                + ("Historical material unrelated to release validation. " * 30)
                + "\n\n# Shared Rule\nKeep evidence anchors.\n",
                encoding="utf-8",
            )
            second.write_text(
                "# Shared Rule\nKeep evidence anchors.\n\n"
                "# Visual Notes\n"
                + ("Color and typography notes outside this task. " * 25),
                encoding="utf-8",
            )

            result = ce.build_pack(
                [first, second],
                query="release deployment validation 2.4.1",
                budget_tokens=120,
                output_dir=output,
            )
            first_bytes = {
                path.relative_to(output).as_posix(): path.read_bytes()
                for path in sorted(output.rglob("*"))
                if path.is_file()
            }
            repeated = ce.build_pack(
                [first, second],
                query="release deployment validation 2.4.1",
                budget_tokens=120,
                output_dir=output,
            )
            second_bytes = {
                path.relative_to(output).as_posix(): path.read_bytes()
                for path in sorted(output.rglob("*"))
                if path.is_file()
            }

            pack = (output / "packs" / "current-task.context.md").read_text(encoding="utf-8")
            report = (output / "savings-report.md").read_text(encoding="utf-8")
            ledger = (output / "ledger.json").read_text(encoding="utf-8")

            self.assertLess(result.packed_tokens, result.source_tokens)
            self.assertEqual(result, repeated)
            self.assertEqual(first_bytes, second_bytes)
            self.assertIn("[release.md#deployment]", pack)
            self.assertIn("2.4.1", pack)
            self.assertIn("https://example.com/release", pack)
            self.assertIn("python -m unittest discover -s tests -v", pack)
            self.assertIn("Omitted Anchors", pack)
            self.assertIn("estimated", report.lower())
            self.assertIn('"duplicate_source": "duplicate.md"', ledger)

    def test_validate_snapshot_requires_state_headings_and_protected_facts(self) -> None:
        ce = load_context_economy()
        source = (
            "Goal: ship release 2.4.1. Source https://example.com/release\n\n"
            "```powershell\npython -m unittest discover -s tests -v\n```"
        )
        incomplete = "# Goal\nShip the release.\n\n# Decisions\nUse the tested path."

        result = ce.validate_snapshot(incomplete, source)

        self.assertFalse(result.valid)
        self.assertIn("Confirmed Constraints", result.missing_sections)
        self.assertIn("2.4.1", result.missing_protected_facts)
        self.assertIn("https://example.com/release", result.missing_protected_facts)

    def test_validate_snapshot_accepts_complete_recoverable_state(self) -> None:
        ce = load_context_economy()
        source = "Release 2.4.1 from https://example.com/release"
        snapshot = (
            "# Goal\nShip release 2.4.1 from https://example.com/release\n\n"
            "# Confirmed Constraints\nPreserve evidence.\n\n"
            "# Decisions\nUse exact anchors.\n\n"
            "# Completed\nTests prepared.\n\n"
            "# Remaining\nRun release validation.\n\n"
            "# Evidence\nObjective test output.\n\n"
            "# Open Questions\nNone.\n"
        )

        result = ce.validate_snapshot(snapshot, source)

        self.assertTrue(result.valid)
        self.assertEqual(result.missing_sections, ())
        self.assertEqual(result.missing_protected_facts, ())


if __name__ == "__main__":
    unittest.main()
