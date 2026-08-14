import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_product_assets.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_product_assets", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class FeedbackBoardTests(unittest.TestCase):
    def test_generated_feedback_data_contains_every_suite_and_skill(self) -> None:
        generator = load_generator()
        expected = {
            generator.parse_frontmatter(path)[0]
            for path in (ROOT / "suites").rglob("SKILL.md")
        }
        payload = generator.feedback_catalog(ROOT)

        self.assertEqual(set(payload), set(generator.SUITE_ORDER))
        self.assertEqual(
            {skill for skills in payload.values() for skill in skills},
            expected,
        )
        self.assertEqual(sum(len(skills) for skills in payload.values()), 30)

        generated = (ROOT / "docs" / "feedback-data.js").read_text(encoding="utf-8")
        for suite, skills in payload.items():
            self.assertIn(json.dumps(suite), generated)
            for skill in skills:
                self.assertIn(json.dumps(skill), generated)

    def test_bilingual_homepages_expose_the_same_feedback_contract(self) -> None:
        english = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        chinese = (ROOT / "docs" / "zh" / "index.html").read_text(encoding="utf-8")
        for content in (english, chinese):
            self.assertIn('href="#feedback"', content)
            self.assertIn('id="feedback"', content)
            self.assertIn('id="feedback-form"', content)
            self.assertIn('name="feedback-type"', content)
            self.assertIn('id="feedback-workflow"', content)
            self.assertIn('id="feedback-skill"', content)
            self.assertIn('id="feedback-title"', content)
            self.assertIn('id="feedback-details"', content)
            self.assertIn('id="feedback-list"', content)
            self.assertIn('aria-live="polite"', content)
            self.assertIn('feedback-data.js', content)
            self.assertIn('feedback.js', content)
        self.assertIn("Feedback &amp; Ideas", english)
        self.assertIn("反馈与建议", chinese)
        self.assertIn("Do not include credentials", english)
        self.assertIn("不要提交凭据", chinese)

    def test_feedback_entry_is_visible_on_home_and_catalogs(self) -> None:
        english = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        chinese = (ROOT / "docs" / "zh" / "index.html").read_text(encoding="utf-8")
        english_index = (ROOT / "docs" / "skills" / "index.html").read_text(encoding="utf-8")
        chinese_index = (ROOT / "docs" / "zh" / "skills" / "index.html").read_text(encoding="utf-8")
        catalog = (ROOT / "docs" / "skills-catalog.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

        self.assertIn('class="button secondary feedback-entry" href="#feedback"', english)
        self.assertIn('class="button secondary feedback-entry" href="#feedback"', chinese)
        for content in (english_index, chinese_index):
            self.assertIn('class="index-actions"', content)
            self.assertIn('issues/new/choose', content)
        self.assertIn("TIKAZ-AI-Skills/#feedback", catalog)
        self.assertIn("issues/new/choose", catalog)
        self.assertIn("TIKAZ-AI-Skills/#feedback", readme)
        self.assertIn("TIKAZ-AI-Skills/zh/#feedback", readme_zh)

    def test_feedback_url_keeps_optional_scope_and_encodes_user_text(self) -> None:
        script = r"""
const feedback = require('./docs/feedback.js');
const value = feedback.buildFeedbackUrl({
  type: 'bug', workflow: 'context-economy', skill: 'context-pack',
  title: 'URL & table issue', details: 'Expected 2.4.1\nActual: <empty>', language: 'en'
});
process.stdout.write(value);
"""
        completed = subprocess.run(
            ["node", "-e", script], cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", check=True,
        )
        parsed = urlparse(completed.stdout)
        query = parse_qs(parsed.query)
        self.assertEqual(parsed.path, "/TIKAZI/TIKAZ-AI-Skills/issues/new")
        self.assertEqual(query["labels"], ["feedback,bug"])
        self.assertIn("[Bug][context-economy/context-pack]", query["title"][0])
        self.assertIn("URL & table issue", query["title"][0])
        self.assertIn("Expected 2.4.1", query["body"][0])
        self.assertIn("Actual: <empty>", query["body"][0])

        optional_script = r"""
const feedback = require('./docs/feedback.js');
process.stdout.write(feedback.buildFeedbackUrl({
  type: 'idea', workflow: '', skill: '', title: 'A thought', details: 'Details', language: 'en'
}));
"""
        optional = subprocess.run(
            ["node", "-e", optional_script], cwd=ROOT, capture_output=True,
            text=True, encoding="utf-8", check=True,
        )
        optional_query = parse_qs(urlparse(optional.stdout).query)
        self.assertIn("Scope: Not specified", optional_query["body"][0])

    def test_feedback_runtime_has_safe_loading_empty_and_error_states(self) -> None:
        script = (ROOT / "docs" / "feedback.js").read_text(encoding="utf-8")
        self.assertIn("api.github.com/repos/TIKAZI/TIKAZ-AI-Skills/issues", script)
        self.assertIn("feedback-loading", script)
        self.assertIn("feedback-empty", script)
        self.assertIn("feedback-error", script)
        self.assertIn("textContent", script)
        self.assertNotIn("innerHTML", script)
        self.assertIn("noopener,noreferrer", script)
        self.assertIn("AbortController", script)

    def test_issue_forms_offer_optional_workflow_and_skill_scope(self) -> None:
        templates = ROOT / ".github" / "ISSUE_TEMPLATE"
        for name in (
            "bug_report.yml", "bug_report_zh.yml",
            "workflow_proposal.yml", "workflow_proposal_zh.yml",
            "general_feedback.yml", "general_feedback_zh.yml",
        ):
            content = (templates / name).read_text(encoding="utf-8")
            self.assertIn("labels:", content)
            self.assertIn("feedback", content)
            self.assertRegex(content, r"id:\s*(suite|workflow)")
            self.assertIn("id: skill", content)
            self.assertIn("context-economy", content)
            self.assertIn("context-pack", content)
            self.assertNotRegex(content, r"id:\s*(suite|workflow)[\s\S]{0,180}required:\s*true")
            self.assertNotRegex(content, r"id:\s*skill[\s\S]{0,180}required:\s*true")


if __name__ == "__main__":
    unittest.main()
