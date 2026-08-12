---
name: context-ledger
description: Use when canonical text must be fingerprinted, split into stable sections, deduplicated, and made traceable across repeated agent tasks.
---

# Context Ledger

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Build an auditable map before selecting content.

- Fingerprint each source and section with a stable content hash.
- Split Markdown by headings and preserve code fences as indivisible blocks.
- Remove exact duplicates only; flag near-duplicates for review rather than silently merging them.
- Record source, anchor, hash, estimated tokens, protected facts, and duplicate target.
- Reuse an unchanged canonical asset instead of converting or rereading it.

The ledger describes what exists and what repeats. It does not decide relevance or truth. Hand the ledger to `context-budget` and `relevance-gate`.
