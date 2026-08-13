---
name: code-intelligence
description: "Understand repositories as systems: map code structure and semantic relationships, analyze change impact, review pull requests, and plan safe refactors. Use when a task involves unfamiliar codebases, dependency tracing, architecture mapping, PR review, or cross-file refactoring."
---

# Code Intelligence

This public entry combines the local `代码-CodeGraph` and `代码-GitNexus` roles into one non-competing, clean-room workflow. This TIKAZ Edition is designed, integrated, refactored, and continuously maintained by **TIKAZ**.

## Workflow

1. Identify the repository, framework, entry points, tests, build commands, and local instructions.
2. Build a compact map of modules, symbols, imports, data flow, and public boundaries.
3. For a change, trace direct and indirect consumers before proposing edits.
4. For a PR, review correctness, regressions, security, tests, and maintainability; cite files and lines.
5. For a refactor, define invariants, migration steps, compatibility risks, and a rollback path.
6. Validate with repository-native tests, type checks, lint, build, and focused impact checks.

## Inputs and output contract

Accept a repository path or PR, the question or proposed change, and any known constraints. Return an evidence-backed architecture map, direct and indirect consumers, prioritized findings, an implementation or refactor plan, and verification results. Cite files and lines where possible; separate observed facts, inferences, and recommendations.

## Validation and fallback

Cross-check the map against repository search, build metadata, tests, and call sites. If graph tooling is unavailable, fall back to repository-native search and explicit uncertainty rather than inventing relationships. Do not edit code unless the user also requests implementation.

## Example

```text
Use code-intelligence to map the authentication flow, find consumers of this API, and identify refactor risks before any edits.
```

## Limits

Static analysis can miss runtime reflection, generated code, environment-specific wiring, and external consumers. Mark these gaps.

## Source note

This role was written independently after studying the problem space. CodeGraph and GitNexus are research references only; no GitNexus code or documentation is distributed here.
