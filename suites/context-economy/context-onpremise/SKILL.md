---
name: context-onpremise
description: Use deployed local conversion, OCR, audio/video, visual, retrieval, reranking, and guarded compression to build high-fidelity bounded Codex context. Use only for a valid uppercase ON prefix or explicit invocation.
---

# TIKAZ Context On-Premise

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## Core promise

Find the right evidence before deciding whether to compress. Use local dependencies for complex documents, multimodal material, and semantic retrieval while keeping sources, facts, anchors, privacy, failures, and cost measurable.

## Workflow

1. Fix the task, required evidence slots, risk, text budget, and visual budget.
2. Profile the input once and invoke only the necessary local route: document conversion, webpage extraction, media understanding, local retrieval/compression, or safe structured parsing.
3. Protect numbers, versions, URLs, commands, errors, citations, table cells, approvals, and source anchors.
4. Combine lexical evidence slots, BGE-M3, local reranking, and diversity-aware selection. Query expansions are retrieval hints, never source facts.
5. Use LLMLingua-2 only for over-budget, low-risk natural-language prose. Never send protected blocks, code, commands, contracts, finance, tables, or security evidence to learned compression.
6. Fall back visibly to deterministic selection or the original source when local models fail, evidence coverage is low, protected facts drop, or the budget conflicts with safety.

## Output contract

Return canonical Markdown or a safe structured result, Context Pack, evidence ledger, retrieval ledger, cost ledger, omissions, and Pending items. Report Recall@K, Precision@K, MRR, nDCG@K, evidence-slot coverage, protected-fact recall, estimated tokens, latency, and fallback state separately. Without relevance labels, do not invent hit-rate percentages.

## Validation and fallback

Validate protected literals, source anchors, required evidence slots, hard budget, adapter identity, and unresolved visual/table evidence before accepting the pack. If any required gate fails, return deterministic selection or the original source with the reason instead of claiming successful compression.

## Installation

This Skill describes the route. The optional engine, adapters, fixtures, benchmark artifacts, and setup documentation live in [TIKAZ Codex Context On-Premise](https://github.com/TIKAZI/TIKAZ-Codex-Context-OnPremise). It never installs dependencies or downloads models during a run.

## Example

```text
ON 分析这批 PDF、表格和录屏，保留来源锚点并生成有预算的 Context Pack。
```

## Limits

Fixed synthetic benchmarks do not establish universal accuracy, real provider Token savings, or downstream-answer correctness. Model weights and third-party tools retain their own licenses and are not bundled with this Skill.
