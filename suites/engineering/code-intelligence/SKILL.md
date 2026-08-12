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

## Output

Return an evidence-backed architecture map, impact list, prioritized findings, implementation plan, and verification results. Separate observed facts, inferences, and recommendations.

## Source note

This role was written independently after studying the problem space. CodeGraph and GitNexus are research references only; no GitNexus code or documentation is distributed here.
