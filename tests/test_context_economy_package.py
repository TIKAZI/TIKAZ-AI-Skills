import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "suites" / "context-economy"
SCRIPT = SUITE / "scripts" / "tikaz_context.py"
VERSION = "0.10.0"


class ContextEconomyPackageTests(unittest.TestCase):
    def test_bilingual_readmes_publish_install_privacy_and_adoption_contracts(self) -> None:
        required = (
            "pipx install git+https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy.git",
            "python -m pip install git+https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy.git",
            "tikaz-context doctor",
            "pipx uninstall tikaz-context-economy",
            "references/threat-model.md",
            "issues/new?template=context_economy_showcase.yml",
        )

        for readme_name in ("README.md", "README.zh-CN.md"):
            content = (SUITE / readme_name).read_text(encoding="utf-8")
            with self.subTest(readme=readme_name):
                for marker in required:
                    self.assertIn(marker, content)
                self.assertIn("telemetry", content.lower())

    def test_cli_reports_the_release_version(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--version"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), f"tikaz-context {VERSION}")

    def test_package_metadata_exposes_a_dependency_free_console_script(self) -> None:
        metadata = tomllib.loads((SUITE / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(metadata["project"]["name"], "tikaz-context-economy")
        self.assertEqual(metadata["project"]["version"], VERSION)
        self.assertEqual(metadata["project"]["dependencies"], [])
        self.assertEqual(
            metadata["project"]["scripts"]["tikaz-context"],
            "tikaz_context_economy:main",
        )
        self.assertEqual((SUITE / "VERSION").read_text(encoding="utf-8").strip(), VERSION)

    def test_benchmark_uses_the_bundled_manifest_when_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "benchmark"
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "benchmark", "--output", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue((output / "summary.json").is_file())

    def test_distribution_includes_security_and_package_automation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "distribution"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "export_distribution.py"),
                    "--suite",
                    "context-economy",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue((output / "pyproject.toml").is_file())
            self.assertTrue((output / "references" / "threat-model.md").is_file())
            self.assertTrue((output / ".github" / "workflows" / "package.yml").is_file())
            self.assertTrue((output / ".github" / "workflows" / "codeql.yml").is_file())
            self.assertTrue((output / ".github" / "dependabot.yml").is_file())
            readme = (output / "README.md").read_text(encoding="utf-8")
            self.assertIn(
                "pipx install git+https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy.git",
                readme,
            )
            self.assertIn("tikaz-context benchmark", readme)
            self.assertIn("references/threat-model.md", readme)
            self.assertIn("issues/new?template=context_economy_showcase.yml", readme)


if __name__ == "__main__":
    unittest.main()
