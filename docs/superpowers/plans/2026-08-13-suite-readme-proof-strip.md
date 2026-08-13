# Suite README Proof Strip Implementation Plan

> **For agentic workers:** Follow the repository engineering, test, and verification contracts task by task.

**Goal:** Add a polished, bilingual four-item proof strip to each of the seven standalone suite READMEs.

**Architecture:** Store proof metadata once in the distribution manifest. Render it through a small GitHub-native HTML helper for English and Chinese exports, then validate the generated repositories.

**Tech stack:** Python 3, JSON, GitHub Markdown/HTML, unittest, PowerShell validation, GitHub Actions.

## Global constraints

- Do not invent performance or accuracy metrics.
- Keep exactly four concise items per suite.
- Preserve existing repository URLs, headings, installation instructions, and Skill links.
- Keep English and Chinese values identical and labels localized.
- Use native GitHub rendering with no external CSS or runtime dependency.

## Tasks

1. Add failing tests for manifest shape, bilingual parity, four-cell rendering, and placement.
2. Add suite-specific proof metadata to `distribution/manifest.json`.
3. Implement the reusable proof-strip renderer and inject it into both exported READMEs.
4. Build and validate all seven standalone distributions.
5. Run full tests, repository validation, diff checks, and GitHub-rendered visual QA.
6. Commit and push the canonical repository, then verify synchronized suite repositories.
