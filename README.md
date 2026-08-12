# TIKAZ AI Skills

[![Validate Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills/actions/workflows/validate.yml/badge.svg)](https://github.com/TIKAZI/TIKAZ-AI-Skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Suites](https://img.shields.io/badge/suites-6-7c3aed.svg)](#six-suites)
[![Skills](https://img.shields.io/badge/skills-25-0ea5e9.svg)](#six-suites)

A curated collection of six composable AI-agent workflows for video intelligence, frontend design, engineering, research, presentations, and visual content.

The collection architecture, routing contracts, clean-room adaptations, portability rules, and validation gates are designed, integrated, refactored, and continuously maintained by **TIKAZ**.

> **TIKAZ AI Skills：面向 Codex 的工作流集合**
>
> 把一次性的提示词，组织成可路由、可验证、可迁移的工作流。每套 Skill 都有明确的负责人、输入输出合同和完成门禁。

## Why this collection

Most Skill collections stop at instructions that sound useful. TIKAZ AI Skills treats a Skill as a small product workflow: route to one owner, carry evidence and uncertainty through handoffs, verify the result, and keep it portable across environments.

Start with the two flagship suites: [`frontend-design`](suites/frontend-design) for distinctive interfaces and [`video-intelligence`](suites/video-intelligence) for auditable video learning.

## What is original here

This is not a renamed mirror of other skill repositories. The TIKAZ Edition adds a shared operating model:

- exactly one primary Skill owns each deliverable;
- evidence, confidence, source, and license status travel with handoffs;
- visual work requires an early representative proof and rendered QA;
- engineering work requires impact analysis and objective verification;
- local paths, credentials, private knowledge bases, and provider assumptions are excluded;
- a release gate blocks missing attribution, unknown licenses, private paths, and invalid routing.

Research references and upstream projects are named in [SOURCES.yml](SOURCES.yml) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Public source code does not automatically become TIKAZ-owned; third-party rights remain with their authors.

## Six suites

| Suite | Included Skills | Workflow |
|---|---:|---|
| `video-intelligence` | 2 | inventory sources → acquire evidence → timestamps/keyframes → source cards → compare |
| `frontend-design` | 2 | classify surface → Design Read → art-direction proof → build → visual and engineering QA |
| `engineering` | 6 | specify → map impact → implement → test → review → release evidence |
| `knowledge-research` | 6 | frame question → normalize sources → evidence ledger → synthesize → knowledge feedback |
| `presentation` | 4 | narrative brief → choose one format → page contracts → render QA → verify artifact |
| `visual-content` | 5 | extract thesis → choose one style → shot card → create → publishing-size QA |

The count includes each suite-level orchestrator. There are **25 installable Skills** in total.

## Install

Clone the repository, then copy either a suite folder or an individual child Skill into the Skill directory supported by your agent host. Keep the folder name unchanged because it must match the `name` in `SKILL.md`.

Example for a project-local Codex installation:

```powershell
Copy-Item -Recurse -LiteralPath '.\suites\frontend-design\frontend-design-studio' -Destination '.\.agents\skills\frontend-design-studio'
```

Some Skills orchestrate optional external tools. They detect what the current environment actually provides and must not claim unavailable platform access or local executables.

## 60-second start

Clone the repository, copy one suite or child Skill into the directory supported by your Codex host, then name the Skill in your prompt:

```text
Use frontend-design to redesign this dashboard. First produce a Design Read and a desktop/mobile proof; do not expand the full page until the proof passes.
```

```text
Use video-platform-reader to compare these videos. Keep timestamps, label evidence levels, and list every claim that could not be verified.
```

More copy-ready prompts are in [examples/prompts.md](examples/prompts.md).

## Example prompts

- “Use `video-platform-reader` to compare these three videos, keep timestamps, and tell me which visual claims remain unverified.”
- “Use `frontend-design` to redesign this dashboard. Approve a desktop/mobile art-direction proof before expanding the full product.”
- “Use `engineering` to map the impact of this API change, implement it in small slices, and give me test and rollback evidence.”
- “Use `knowledge-research` to compare these sources, separate fact from inference, and show contradictory evidence.”
- “Use `presentation` to choose HTML or PPTX for this talk, then render and inspect the finished deck.”
- “Use `visual-content` to turn this logistics article into a sourced 16:9 explainer with alt text.”

## Validate before publishing

```powershell
pwsh -File .\scripts\validate_skills.ps1
```

The command validates structure, attribution, source policy, portability, routing targets, UI metadata, and Python syntax. A successful local run is evidence of repository consistency, not proof that every external tool or platform is available.

## License and attribution

TIKAZ-authored files are available under the [MIT License](LICENSE). Research references are not bundled dependencies and remain under their own licenses. If future contributions vendor third-party files, their original notices and compatible license must travel with them; unknown-license material is rejected.

See [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a Skill.
