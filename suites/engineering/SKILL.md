---
name: engineering
description: Orchestrate production software delivery through specification, repository intelligence, implementation, testing, security review, data operations, and release evidence. Use for substantial code changes that cross files, systems, or deployment boundaries.
---

# Engineering

Designed, integrated, refactored, and continuously maintained by **TIKAZ**.

## TIKAZ method

1. Freeze scope, non-goals, acceptance criteria, and evidence required for completion.
2. Use `code-intelligence` to map architecture and impact before editing unfamiliar or cross-cutting code.
3. Use `engineering-delivery` as the lifecycle owner: plan small slices, implement, test, review, and report.
4. Route only domain-specific work to `supabase-operations` or `video-workbench`.
5. Run `skill-security-audit` before importing unfamiliar executable skills or dependencies.
6. Keep an evidence ledger: commands, results, artifacts, regressions checked, and remaining risk.

## Conflict rule

`code-intelligence` advises; `engineering-delivery` executes. Domain adapters cannot expand scope without explicit acceptance criteria.

## Completion gate

Require repository-native validation, final diff review, no leaked secrets, an explicit release/rollback note when applicable, and objective evidence for every acceptance criterion.

Read [references/routing.md](references/routing.md) and [references/output-contract.md](references/output-contract.md).
