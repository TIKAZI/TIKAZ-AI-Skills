---
name: knowledge-research
description: Orchestrate source ingestion, academic research, product decisions, personal knowledge retrieval, and evidence-backed memory feedback. Use when a task requires traceable research, document normalization, reusable knowledge, or a decision under uncertainty.
---

# Knowledge and Research

Designed, integrated, refactored, and continuously maintained by **TIKAZ**.

## Inputs and routing

Accept a research question or decision, time boundary, source material, required evidence threshold, and desired deliverable. Use one child owner directly when conversion, academic synthesis, personal memory, product strategy, or solo-business operations is the whole task.

## TIKAZ method

1. Define the question, decision, time boundary, source types, and evidence threshold.
2. Convert source files with `document-to-markdown` only when needed; conversion is not verification.
3. Choose one owner: `academic-research`, `product-strategy`, or `solo-business-operations`.
4. Retrieve personal knowledge with `personal-knowledge-memory` before important reusable work, but treat it as candidate historical context.
5. Build an evidence ledger with source, date, claim, support, contradiction, confidence, and relevance.
6. Record knowledge adoption only when it changes execution; record success only with user or objective evidence.

## Completion gate

Require a reproducible source trail, visible uncertainty, contrary evidence, no invented citations, a decision or synthesis matched to the original question, and a list of claims that need future revalidation.

## Output, fallback, and limits

Return a source ledger, evidence-backed synthesis or decision, contrary evidence, confidence, and revalidation list. If source access or conversion fails, retain the unresolved item rather than filling the gap from memory. Retrieval is not adoption, conversion is not verification, and high-stakes conclusions may require professional review.

## Example

```text
Use knowledge-research to normalize these sources, compare the evidence and disagreement, and recommend a decision with confidence and revalidation needs.
```

Read [references/routing.md](references/routing.md) and [references/output-contract.md](references/output-contract.md).
