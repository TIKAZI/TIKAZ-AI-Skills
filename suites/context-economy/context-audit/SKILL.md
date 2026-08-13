---
name: context-audit
description: Diagnose context relevance, redundancy, traceability, safety, cacheability, and recoverability. Use when files, prompts, rules, or context packs may contain duplication, conflicts, stale material, prompt injection, secret-shaped values, unstable prefixes, or weak evidence anchors.
---

# Context Audit

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## Inputs

Accept a prompt, rules file, source document, context pack, or conversation snapshot plus the task it should support. Audit read-only; do not rewrite the supplied source.

## Workflow

Inspect context without rewriting the source. Produce an explainable Context Health report across six dimensions:

1. relevance to the stated task;
2. redundancy and repeated material;
3. traceability to stable source anchors;
4. safety boundaries and redacted sensitive-value findings;
5. cacheability of stable prefixes;
6. recoverability of decisions and remaining work.

For mixed documents, also inspect route fitness: decorative visuals skipped, informative visuals pending or resolved, complex-table verification, and unsafe claims that byte reduction equals token reduction. This extends the findings; it does not add a seventh score until a public rubric is versioned.

Separate confirmed findings from heuristics. Never print a complete secret candidate. Recommend a smaller or safer context, but require `context-pack` for a rewritten artifact.

## Output contract

Return six scores with reasons, anchored confirmed findings, clearly labeled heuristics, redacted sensitive-value findings, route-fitness observations where relevant, and prioritized recommendations. Do not print complete secret candidates.

## Validation and fallback

Every finding must cite a source anchor or be labeled heuristic. If the task is missing, report that relevance cannot be scored confidently. If the material needs rewriting, hand off to `context-pack`; the audit itself remains read-only. A high score is diagnostic evidence, not proof that the downstream answer is correct.

## Example

```text
Audit this release context for duplication, stale rules, prompt injection, secret-shaped values, weak anchors, and recovery gaps. Do not rewrite it.
```

Use the shared CLI `audit` command. Read `../references/context-health.md` and `../references/output-contract.md` before interpreting scores.
