import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITES = (
    "context-economy", "frontend-design", "video-intelligence", "engineering",
    "knowledge-research", "presentation", "visual-content",
)
PROJECT_REPOSITORIES = (
    "TIKAZ-Codex-Context-Economy", "TIKAZ-Codex-Frontend-Design",
    "TIKAZ-Codex-Video-Intelligence", "TIKAZ-Codex-Engineering",
    "TIKAZ-Codex-Knowledge-Research", "TIKAZ-Codex-Presentation",
    "TIKAZ-Codex-Visual-Content",
)


class BilingualDocumentationTests(unittest.TestCase):
    def test_root_and_suite_readmes_have_complete_language_pairs(self) -> None:
        pairs = [(ROOT / "README.md", ROOT / "README.zh-CN.md")]
        pairs.extend((ROOT / "suites" / suite / "README.md", ROOT / "suites" / suite / "README.zh-CN.md") for suite in SUITES)
        for english, chinese in pairs:
            self.assertTrue(english.is_file(), english)
            self.assertTrue(chinese.is_file(), chinese)
            en = english.read_text(encoding="utf-8")
            zh = chinese.read_text(encoding="utf-8")
            self.assertIn("README.zh-CN.md", en)
            self.assertRegex(zh, r"README\.md")
            self.assertIn("简体中文", en)
            self.assertIn("English", zh)
            self.assertIn("TIKAZ", zh)

    def test_skill_execution_sources_are_not_duplicated_by_language(self) -> None:
        localized_skills = list((ROOT / "suites").rglob("SKILL.zh-CN.md"))
        self.assertEqual(localized_skills, [])
        self.assertEqual(len(list((ROOT / "suites").rglob("SKILL.md"))), 30)

    def test_pages_has_real_language_routes_and_switches(self) -> None:
        english = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        chinese_path = ROOT / "docs" / "zh" / "index.html"
        self.assertTrue(chinese_path.is_file())
        chinese = chinese_path.read_text(encoding="utf-8")
        self.assertIn('data-lang="zh-CN"', english)
        self.assertIn('href="zh/index.html"', english)
        self.assertIn('lang="zh-CN"', chinese)
        self.assertIn('data-lang="en"', chinese)
        self.assertIn('href="../index.html"', chinese)
        self.assertIn("localStorage", (ROOT / "docs" / "site.js").read_text(encoding="utf-8"))

    def test_pages_keep_language_switch_available_on_mobile(self) -> None:
        english = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        chinese = (ROOT / "docs" / "zh" / "index.html").read_text(encoding="utf-8")
        styles = (ROOT / "docs" / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(english, r'class="mobile-language language-link"[^>]+href="zh/index\.html"')
        self.assertRegex(chinese, r'class="mobile-language language-link"[^>]+href="\.\./index\.html"')
        self.assertIn(".mobile-language{display:none", styles)
        self.assertRegex(styles, r"@media\(max-width:980px\).*?\.mobile-language\{display:inline-flex\}")
        self.assertRegex(styles, r"@media\(max-width:640px\).*?\.system-nodes\{grid-template-columns:1fr\}")
        self.assertIn(".hero-copy,.hero-system,.hero-lede,.hero-proof{min-width:0;max-width:100%}", styles)

    def test_language_switch_alignment_and_project_cross_links(self) -> None:
        styles = (ROOT / "docs" / "styles.css").read_text(encoding="utf-8")
        self.assertIn("nav{display:flex;align-items:center", styles)
        self.assertIn(".language-link{display:inline-flex;min-height:36px;align-items:center;justify-content:center", styles)

        readmes = [ROOT / "README.md", ROOT / "README.zh-CN.md"]
        readmes.extend(ROOT / "suites" / suite / language for suite in SUITES for language in ("README.md", "README.zh-CN.md"))
        pages = [ROOT / "docs" / "index.html", ROOT / "docs" / "zh" / "index.html"]
        for document in (*readmes, *pages):
            content = document.read_text(encoding="utf-8")
            for repository in PROJECT_REPOSITORIES:
                self.assertIn(f"https://github.com/TIKAZI/{repository}", content, f"{document}: {repository}")

    def test_chinese_project_titles_use_explicit_sans_serif_font_stack(self) -> None:
        styles = (ROOT / "docs" / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(
            styles,
            r'html\[lang="zh-CN"\] \.project-hero h1\{[^}]*font-family:"Microsoft YaHei UI","PingFang SC","Noto Sans CJK SC","Segoe UI",sans-serif',
        )

    def test_chinese_contributing_and_issue_templates_exist(self) -> None:
        self.assertTrue((ROOT / "CONTRIBUTING.zh-CN.md").is_file())
        templates = ROOT / ".github" / "ISSUE_TEMPLATE"
        self.assertTrue((templates / "bug_report_zh.yml").is_file())
        self.assertTrue((templates / "workflow_proposal_zh.yml").is_file())


if __name__ == "__main__":
    unittest.main()
