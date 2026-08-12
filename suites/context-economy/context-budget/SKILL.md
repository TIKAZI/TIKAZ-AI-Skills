---
name: context-budget
description: Use when an agent must decide whether context preparation, selection, compaction, or stable-prefix reuse is worth its processing cost and information risk.
---

# Context Budget

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Choose one primary mode from observable conditions:

| Mode | Choose when |
|---|---|
| `pass-through` | The source fits the budget, is already dense, or precision risk dominates. |
| `select` | Exact relevant sections fit while the whole source does not. |
| `compact` | Repetition is material and a structured state can preserve protected facts and anchors. |
| `cache-stable` | A repeated prefix or canonical asset should remain byte-stable for reuse. |

Estimate source tokens, target budget, conversion/compression overhead, expected reuse, and verification cost. Refuse an optimization when expected savings do not exceed overhead or when quality cannot be tested. Estimates are planning values, not provider billing totals.
