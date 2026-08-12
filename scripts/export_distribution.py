#!/usr/bin/env python3
"""Build one independently installable distribution from the canonical monorepo."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


MANAGED = {
    ".github", ".gitignore", "README.md", "LICENSE", "CONTRIBUTING.md",
    "SOURCES.yml", "THIRD_PARTY_NOTICES.md", "DISTRIBUTION.yml", "VERSION",
    "SKILL.md", "agents", "assets", "references", "scripts",
}


def read_manifest(root: Path) -> dict:
    return json.loads((root / "distribution" / "manifest.json").read_text(encoding="utf-8"))


def clean_output(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for name in MANAGED:
        target = output / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    for child in output.iterdir():
        if child.name.startswith(".") or child.name in MANAGED:
            continue
        if (child / "SKILL.md").exists():
            shutil.rmtree(child)


def copy_suite(root: Path, suite: str, output: Path) -> None:
    source = root / "suites" / suite
    for item in source.iterdir():
        if item.name == "README.md":
            continue
        destination = output / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)
    for name in ("LICENSE", "CONTRIBUTING.md", "SOURCES.yml", "THIRD_PARTY_NOTICES.md", ".gitignore"):
        shutil.copy2(root / name, output / name)


def hero_svg(title: str, tagline: str, accent: str) -> str:
    safe_title = title.replace("&", "&amp;")
    safe_tagline = tagline.replace("&", "&amp;")
    return f'''<svg width="1440" height="500" viewBox="0 0 1440 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{safe_title}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1440" y2="500"><stop stop-color="#090D18"/><stop offset="1" stop-color="#101A24"/></linearGradient><radialGradient id="g"><stop stop-color="#{accent}" stop-opacity=".34"/><stop offset="1" stop-color="#{accent}" stop-opacity="0"/></radialGradient></defs>
<rect width="1440" height="500" rx="30" fill="url(#bg)"/><circle cx="1180" cy="80" r="520" fill="url(#g)"/><path d="M0 100H1440M0 200H1440M0 300H1440M0 400H1440M240 0V500M480 0V500M720 0V500M960 0V500M1200 0V500" stroke="#94A3B8" stroke-opacity=".055"/>
<g font-family="Segoe UI,Arial,sans-serif"><text x="86" y="92" fill="#{accent}" font-size="18" font-weight="700" letter-spacing="4">PART OF TIKAZ AI SKILLS FOR CODEX</text><text x="82" y="190" fill="#F8FAFC" font-size="58" font-weight="720" letter-spacing="-2">{safe_title}</text><foreignObject x="86" y="224" width="900" height="110"><div xmlns="http://www.w3.org/1999/xhtml" style="color:#CBD5E1;font:24px Segoe UI,Arial,sans-serif;line-height:1.45">{safe_tagline}</div></foreignObject><rect x="86" y="374" width="260" height="58" rx="29" fill="#{accent}"/><text x="128" y="411" fill="#07111B" font-size="16" font-weight="750" letter-spacing="1.3">INSTALL ONE WORKFLOW</text><text x="1080" y="430" fill="#94A3B8" font-size="15">TIKAZ EDITION · v0.2.0</text></g></svg>'''


def workflow_files(owner: str, collection: str, suite: str) -> dict[str, str]:
    validate = '''name: Validate Distribution
on: [push, pull_request]
jobs:
  validate:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v5
      - shell: powershell
        run: .\\scripts\\validate_distribution.ps1
'''
    sync = f'''name: Sync from TIKAZ AI Skills
on:
  workflow_dispatch:
  schedule:
    - cron: "17 3 * * 1"
permissions:
  contents: write
jobs:
  sync:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0
      - uses: actions/checkout@v5
        with:
          repository: {owner}/{collection}
          path: _canonical
      - name: Rebuild distribution
        shell: powershell
        run: |
          python .\\_canonical\\scripts\\export_distribution.py --suite {suite} --output .\\_publish
          git rm -r --ignore-unmatch .
          Get-ChildItem .\\_publish -Force | Copy-Item -Destination . -Recurse -Force
          Remove-Item .\\_canonical, .\\_publish -Recurse -Force
      - name: Validate
        shell: powershell
        run: .\\scripts\\validate_distribution.ps1
      - name: Commit canonical update
        shell: powershell
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add -A
          if (git diff --cached --quiet) {{ Write-Host "Already current"; exit 0 }}
          git commit -m "chore: sync {suite} from canonical collection"
          git push
'''
    return {"validate.yml": validate, "sync.yml": sync}


def validation_script() -> str:
    return r'''$ErrorActionPreference = 'Stop'
$errors = @()
$skills = @(Get-ChildItem (Split-Path $PSScriptRoot -Parent) -Recurse -Filter SKILL.md -File | Where-Object { $_.FullName -notmatch '[\\/]_canonical[\\/]' })
foreach ($skill in $skills) {
  $content = Get-Content -Raw -Encoding UTF8 $skill.FullName
  if ($content -notmatch '(?s)\A---\r?\n.*?name:\s*[a-z0-9-]+.*?description:\s*.+?\r?\n---') { $errors += "Invalid Skill: $($skill.FullName)" }
  if ($content -notmatch '(?is)designed.{0,100}integrated.{0,100}(independently\s+)?refactored.{0,100}(continuously\s+)?maintained.{0,60}TIKAZ') { $errors += "Missing TIKAZ contribution: $($skill.FullName)" }
  if ($content -match '(?i)[A-Z]:\\Users\\|[A-Z]:\\CodexTools') { $errors += "Machine-specific path: $($skill.FullName)" }
}
if (-not (Test-Path (Join-Path (Split-Path $PSScriptRoot -Parent) 'DISTRIBUTION.yml'))) { $errors += 'Missing distribution metadata' }
if ($errors.Count) { $errors | ForEach-Object { Write-Error $_ }; exit 1 }
Write-Output "PASS: validated $($skills.Count) Skills in this distribution."
'''


def readme(info: dict, suite: str, version: str, owner: str, collection: str) -> str:
    repo = info["repository"]
    highlights = "\n".join(f"- **{item}**" for item in info["highlights"])
    prompts = "\n\n".join(f"```text\n{prompt}\n```" for prompt in info["prompts"])
    return f'''<p align="center"><img src="assets/hero.svg" alt="{info['title']}" width="100%" /></p>

<h1 align="center">{info['title']}</h1>
<p align="center"><strong>{info['tagline']}</strong></p>
<p align="center"><a href="https://github.com/{owner}/{repo}/actions/workflows/validate.yml"><img src="https://github.com/{owner}/{repo}/actions/workflows/validate.yml/badge.svg" alt="Validate" /></a> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-f4c95d.svg" alt="MIT" /></a> <img src="https://img.shields.io/badge/version-{version}-{info['accent']}.svg" alt="{version}" /></p>
<p align="center"><a href="https://github.com/{owner}/{collection}">← Explore all six TIKAZ AI Skills for Codex suites</a></p>

---

## One suite, ready to install

This repository is the independently installable **{suite}** distribution from [TIKAZ AI Skills for Codex](https://github.com/{owner}/{collection}). The monorepo is the canonical development source; this repository is automatically synchronized and optimized for people who need only this workflow.

Designed, integrated, refactored, and continuously maintained by **TIKAZ**. This is a community-maintained project, not an OpenAI-official repository.

## What makes it different

{highlights}

## Install

Clone or download this repository, then copy the repository folder into the Skill directory supported by your Codex environment. The root `SKILL.md` is the suite orchestrator; child folders are focused Skills that can also be installed separately.

```bash
git clone https://github.com/{owner}/{repo}.git
```

## Try it

{prompts}

## How the suite works

Read [SKILL.md](SKILL.md) for the owning workflow, [references/routing.md](references/routing.md) for specialist routing, and [references/output-contract.md](references/output-contract.md) for the verified handoff. Optional tools are detected at runtime; local login state or machine-specific software is never promised as universally available.

## Repository structure

```text
./
├─ SKILL.md                 # suite orchestrator
├─ agents/                  # Codex UI metadata
├─ references/              # routing and output contract
├─ <child-skill>/           # independently installable specialists
├─ DISTRIBUTION.yml         # canonical source and sync metadata
└─ scripts/                 # deterministic validation
```

## Canonical source and contributions

Development, source review, and cross-suite architecture live in [TIKAZ-AI-Skills](https://github.com/{owner}/{collection}). This distribution synchronizes from `suites/{suite}` every week and can also be refreshed manually through GitHub Actions.

Source modes, observed licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](SOURCES.yml) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). TIKAZ-authored files are released under the [MIT License](LICENSE).
'''


def build(root: Path, suite: str, output: Path) -> None:
    manifest = read_manifest(root)
    if suite not in manifest["suites"]:
        raise SystemExit(f"Unknown suite: {suite}")
    info = manifest["suites"][suite]
    clean_output(output)
    copy_suite(root, suite, output)
    (output / "assets").mkdir(exist_ok=True)
    (output / "assets" / "hero.svg").write_text(hero_svg(info["title"], info["tagline"], info["accent"]), encoding="utf-8")
    (output / "README.md").write_text(readme(info, suite, manifest["version"], manifest["owner"], manifest["collection"]), encoding="utf-8")
    (output / "VERSION").write_text(manifest["version"] + "\n", encoding="utf-8")
    try:
        commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        commit = "unknown"
    (output / "DISTRIBUTION.yml").write_text(f"suite: {suite}\ncanonical: https://github.com/{manifest['owner']}/{manifest['collection']}\ncanonical_commit: {commit}\nversion: {manifest['version']}\nmaintainer: TIKAZ\nmode: automated-distribution\n", encoding="utf-8")
    workflows = workflow_files(manifest["owner"], manifest["collection"], suite)
    workflow_dir = output / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    for name, content in workflows.items():
        (workflow_dir / name).write_text(content, encoding="utf-8")
    scripts_dir = output / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    (scripts_dir / "validate_distribution.ps1").write_text(validation_script(), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    build(repository_root, args.suite, args.output.resolve())
