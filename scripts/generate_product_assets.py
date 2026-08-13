#!/usr/bin/env python3
"""Generate the public Skill catalog and editable suite workflow diagrams."""

from __future__ import annotations

import argparse
import html
import json
import re
import textwrap
from pathlib import Path


ATTRIBUTION = (
    "Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**."
)

SUITE_LIMITS = {
    "frontend-design": ["Design approval is not runtime verification.", "Optional component libraries and browser tools must be detected before use.", "Existing routes, analytics, accessibility, and legal copy are preserved unless the user authorizes change."],
    "video-intelligence": ["Platform access, subtitles, downloads, and visual inspection depend on the current environment.", "Metadata and search snippets are not watched content.", "Private, paid, DRM-protected, deleted, or inaccessible media remains unresolved rather than bypassed."],
    "engineering": ["Repository instructions and native tests outrank generic playbooks.", "Security review reduces risk but cannot guarantee safety.", "Production deployment, migrations, and destructive actions require explicit scope and rollback evidence."],
    "knowledge-research": ["Conversion is not verification and retrieval is not adoption.", "Source dates, disagreement, confidence, and revalidation needs remain visible.", "Financial, legal, medical, or safety-critical conclusions require appropriate professional review."],
    "presentation": ["A generated file is not visually approved until rendered and inspected.", "HTML, PPTX, and editorial web decks have different editability and compatibility boundaries.", "External media, fonts, templates, and builder licenses remain authoritative."],
    "visual-content": ["The suite does not require or promise a specific image provider.", "Unverified labels or business claims are not turned into definitive visuals.", "Music is downloaded only from sources that explicitly permit it, with license evidence retained."],
}

SUITE_ORDER = {
    "context-economy": ["context-economy", "context-pack", "conversation-checkpoint", "context-audit", "context-benchmark"],
    "frontend-design": ["frontend-design", "frontend-design-studio"],
    "video-intelligence": ["video-intelligence", "video-platform-reader"],
    "engineering": ["engineering", "code-intelligence", "engineering-delivery", "skill-security-audit", "supabase-operations", "video-workbench"],
    "knowledge-research": ["knowledge-research", "document-to-markdown", "academic-research", "product-strategy", "solo-business-operations", "personal-knowledge-memory"],
    "presentation": ["presentation", "html-deck-builder", "powerpoint-deck-builder", "magazine-web-deck"],
    "visual-content": ["visual-content", "concise-writing-editor", "xiaohei-article-illustrator", "zhuge-logistics-illustrator", "legal-free-music"],
}


def display_name(name: str) -> str:
    return "TIKAZ " + " ".join(part.capitalize() for part in name.split("-"))


def metadata_yaml(name: str, description: str) -> str:
    short = short_promise(description, 58).rstrip(".")
    if len(short) < 25:
        short = f"TIKAZ workflow for {name.replace('-', ' ')}"
    prompt = f"Use ${name} to {short_promise(description, 125)[0].lower() + short_promise(description, 125)[1:]}"
    if not prompt.endswith("."):
        prompt += "."
    return (
        "interface:\n"
        f'  display_name: "{display_name(name)}"\n'
        f'  short_description: "{short.replace(chr(34), chr(39))}"\n'
        f'  default_prompt: "{prompt.replace(chr(34), chr(39))}"\n'
    )


def suite_readme(root: Path, suite_name: str, info: dict) -> str:
    suite = root / "suites" / suite_name
    skills = skills_for_suite(suite)
    rows = []
    for name, description, path in skills:
        relative = path.relative_to(suite).as_posix()
        role = "Orchestrator" if path.parent == suite else "Specialist"
        rows.append(f"| [`{name}`]({relative}) | {role} | {short_promise(description, 170)} |")
    prompts = "\n\n".join(f"```text\n{prompt}\n```" for prompt in info["prompts"])
    highlights = "\n".join(f"- {item}." for item in info["highlights"])
    limits = "\n".join(f"- {item}" for item in SUITE_LIMITS[suite_name])
    title = info["title"]
    return f'''<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><img src="assets/workflow.svg" alt="{title} workflow" width="100%" /></p>

# {title}

**{info['tagline']}**

{ATTRIBUTION}

This suite can be installed as one routed workflow, while every child Skill can also be installed and invoked on its own. It is an independent community project for Codex-compatible Skill hosts, not an OpenAI-official repository.

## What makes it different

{highlights}

## Skills you can use independently

| Skill | Role | Core promise |
|---|---|---|
{chr(10).join(rows)}

The root orchestrator owns end-to-end routing. A specialist owns only the output named in its `SKILL.md`; it does not need the orchestrator to be installed.

## Try it

{prompts}

## Install the suite or one Skill

Copy this suite folder for the complete workflow, or copy one child folder into the Skill directory supported by your Codex host. Keep the destination folder identical to the `name` in `SKILL.md`.

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\\suites\\{suite_name}' `
  -Destination '.\\.agents\\skills\\{suite_name}'
```

## Workflow and output contract

Read [routing](references/routing.md) for owner selection and [output contract](references/output-contract.md) for the verified handoff. The diagram above is editable SVG generated from canonical Skill metadata under the shared [TIKAZ visual system](../../docs/visual-system.md).

## Limitations

{limits}

## Provenance

Source modes, upstream licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](../../SOURCES.yml) and [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md). TIKAZ authorship applies to original architecture, integration, refactoring, routing, and maintenance; it does not erase third-party ownership.
'''


def parse_frontmatter(path: Path) -> tuple[str, str]:
    content = path.read_text(encoding="utf-8")
    name = re.search(r"(?m)^name:\s*[\"']?([^\r\n\"']+)", content)
    description = re.search(r"(?ms)^description:\s*[\"']?(.+?)[\"']?\s*(?=\r?\n---)", content)
    if not name or not description:
        raise ValueError(f"Invalid Skill frontmatter: {path}")
    return name.group(1).strip(), " ".join(description.group(1).split())


def skills_for_suite(suite: Path) -> list[tuple[str, str, Path]]:
    items = []
    for skill_path in sorted(suite.rglob("SKILL.md")):
        name, description = parse_frontmatter(skill_path)
        items.append((name, description, skill_path))
    order = {name: index for index, name in enumerate(SUITE_ORDER.get(suite.name, []))}
    items.sort(key=lambda item: (order.get(item[0], 999), item[0]))
    return items


def short_promise(description: str, limit: int = 150) -> str:
    sentence = re.split(r"(?<=[.!?])\s+", description, maxsplit=1)[0]
    if len(sentence) <= limit:
        return sentence
    return sentence[: limit - 1].rstrip() + "…"


def svg_lines(description: str, width: int = 94) -> list[str]:
    sentence = re.split(r"(?<=[.!?])\s+", description, maxsplit=1)[0]
    lines = textwrap.wrap(sentence, width=width, break_long_words=False, break_on_hyphens=False)
    if len(lines) <= 2:
        return lines
    return [lines[0], textwrap.shorten(" ".join(lines[1:]), width=width, placeholder="…")]


def diagram_svg(title: str, accent: str, skills: list[tuple[str, str, Path]]) -> str:
    width = 1440
    height = 440 + len(skills) * 126
    start_x = 126
    node_x = 260
    node_width = 1040
    node_height = 86
    first_y = 330
    title_safe = html.escape(title)
    nodes = []
    connectors = []
    for index, (name, description, _) in enumerate(skills):
        y = first_y + index * 126
        connectors.append(
            f'<path d="M{start_x} {y - 43} H{node_x}" stroke="#{accent}" stroke-width="2" fill="none" stroke-linecap="round"/>'
        )
        number = f"{index + 1:02d}"
        name_safe = html.escape(name)
        promise_lines = svg_lines(description)
        promise_svg = "".join(
            f'<tspan x="102" dy="{18 if line_index else 0}">{html.escape(line)}</tspan>'
            for line_index, line in enumerate(promise_lines)
        )
        nodes.append(
            f'<g transform="translate({node_x} {y - node_height})">'
            f'<rect width="{node_width}" height="{node_height}" rx="16" fill="#101827" stroke="#334155"/>'
            f'<rect width="6" height="{node_height}" rx="3" fill="#{accent}"/>'
            f'<text x="34" y="34" fill="#{accent}" font-size="13" font-weight="700" letter-spacing="2">{number}</text>'
            f'<text x="102" y="37" fill="#F8FAFC" font-size="23" font-weight="700">{name_safe}</text>'
            f'<text x="102" y="58" fill="#94A3B8" font-size="14">{promise_svg}</text>'
            f'</g>'
        )
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
<title id="title">{title_safe} workflow</title>
<desc id="desc">The suite orchestrator routes work through {len(skills) - 1} independently installable specialist Skills.</desc>
<rect width="{width}" height="{height}" rx="24" fill="#080D18"/>
<g font-family="Segoe UI, Arial, sans-serif">
<text x="92" y="84" fill="#{accent}" font-size="14" font-weight="700" letter-spacing="3">TIKAZ AI SKILLS FOR CODEX</text>
<text x="92" y="138" fill="#F8FAFC" font-size="40" font-weight="720">{title_safe} workflow</text>
<text x="92" y="176" fill="#CBD5E1" font-size="18">Install the suite for orchestration, or use any specialist on its own.</text>
<path d="M{start_x} {first_y - 43} V{first_y + (len(skills) - 1) * 126 - 43}" stroke="#{accent}" stroke-width="2" fill="none" stroke-linecap="round"/>
<circle cx="{start_x}" cy="{first_y - 43}" r="11" fill="#{accent}"/>
{''.join(connectors)}
{''.join(nodes)}
<text x="92" y="{height - 58}" fill="#94A3B8" font-size="13">Editable SVG · neutral structure · one suite accent · no raster generation</text>
</g>
</svg>'''


def catalog_markdown(root: Path, manifest: dict) -> str:
    rows = []
    count = 0
    for suite_name, info in manifest["suites"].items():
        suite = root / "suites" / suite_name
        for name, description, path in skills_for_suite(suite):
            count += 1
            kind = "Orchestrator" if path.parent == suite else "Specialist"
            relative = path.relative_to(root).as_posix()
            rows.append(
                f"| [`{name}`](../{relative}) | {info['title'].replace('TIKAZ ', '').replace(' for Codex', '')} | {kind} | {short_promise(description, 170)} |"
            )
    return f'''# TIKAZ AI Skills Catalog

**{count} independently installable Skills across seven composable Codex workflows.**

Install an orchestrator for an end-to-end outcome. Install a specialist when the named output is the whole task. Every entry links to its canonical `SKILL.md`; suite READMEs provide human-facing examples and evidence.

| Skill | Suite | Role | Core promise |
|---|---|---|---|
{chr(10).join(rows)}

## Independent-use contract

Every Skill must state its trigger and accepted input, owned workflow, output contract, validation and fallback behavior, copy-ready examples, limits, and TIKAZ contribution. Detailed reference material belongs in suite-level `references/`; Skill folders stay concise.

{ATTRIBUTION}
'''


def generate(root: Path, output: Path) -> None:
    manifest = json.loads((root / "distribution" / "manifest.json").read_text(encoding="utf-8"))
    output.mkdir(parents=True, exist_ok=True)
    diagrams = output / "diagrams"
    diagrams.mkdir(parents=True, exist_ok=True)
    (output / "skills-catalog.md").write_text(catalog_markdown(root, manifest), encoding="utf-8")
    for suite_name, info in manifest["suites"].items():
        skills = skills_for_suite(root / "suites" / suite_name)
        title = info["title"].replace("TIKAZ ", "").replace(" for Codex", "")
        (diagrams / f"{suite_name}-workflow.svg").write_text(
            diagram_svg(title, info["accent"], skills), encoding="utf-8"
        )


def publish_suite_assets(root: Path, generated: Path) -> None:
    for workflow in (generated / "diagrams").glob("*-workflow.svg"):
        suite_name = workflow.name.removesuffix("-workflow.svg")
        assets = root / "suites" / suite_name / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        (assets / "workflow.svg").write_bytes(workflow.read_bytes())


def publish_metadata_and_pages(root: Path, manifest: dict) -> None:
    for suite_name, info in manifest["suites"].items():
        suite = root / "suites" / suite_name
        for name, description, path in skills_for_suite(suite):
            metadata = path.parent / "agents" / "openai.yaml"
            if not metadata.exists():
                metadata.parent.mkdir(parents=True, exist_ok=True)
                metadata.write_text(metadata_yaml(name, description), encoding="utf-8")
        if suite_name != "context-economy":
            (suite / "README.md").write_text(suite_readme(root, suite_name, info), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    destination = (args.output or repository_root / "docs").resolve()
    generate(repository_root, destination)
    if args.output is None:
        publish_suite_assets(repository_root, destination)
        manifest = json.loads((repository_root / "distribution" / "manifest.json").read_text(encoding="utf-8"))
        publish_metadata_and_pages(repository_root, manifest)
