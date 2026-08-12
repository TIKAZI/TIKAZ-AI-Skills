---
name: relevance-gate
description: Use when a bounded task needs exact sections selected and ordered from a larger indexed source without turning retrieval into unsupported summarization.
---

# Relevance Gate

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Select evidence for the current task, not for the document in general.

1. Extract task terms, required entities, constraints, time boundary, and output type.
2. Rank chunks by direct term overlap, heading match, protected-fact relevance, and source priority.
3. Keep exact excerpts with source anchors. Prefer a smaller complete section over disconnected keyword fragments.
4. Order task definition and constraints first, evidence next, exceptions beside the claim they limit, and secondary context last.
5. List omitted anchors instead of implying the complete source was reviewed.

Do not treat ranking as truth verification. If two sections conflict, retain both and label the conflict for `context-packager`.
