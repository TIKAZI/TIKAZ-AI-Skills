---
name: context-orchestrator
description: Route long text, files, webpages, code, tables, images, audio, video, or long conversations between default Context Economy and explicit ON-triggered Context On-Premise while keeping one evidence and cost contract.
---

# TIKAZ Context Orchestrator

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## What it owns

This Skill is a controller, not a third compressor. It fixes the task, evidence slots, risk, and budget, chooses exactly one primary route, and requires both routes to return traceable evidence, omissions, Pending items, fallbacks, and separate quality/cost metrics.

## Routing

- Default to `context-economy`: dependency-free, portable, conservative, and source-preserving.
- Use `context-onpremise` only when the first non-empty control word is uppercase `ON` followed by end-of-input, whitespace, `:`, or `：`, or when the user explicitly invokes it.
- Strip the valid `ON` control prefix before passing the remaining task downstream.
- Lowercase `on`, `ONLY`, `ON-board`, `请 ON 分析`, and `ON` appearing later in a sentence do not trigger the local route.

Use `python scripts/route_context.py --text <request>` when deterministic trigger verification is useful. The script parses only the control prefix; it does not open files, install dependencies, start models, or access the network.

## Output contract

Return route, task, budget, evidence slots, context pack, protected facts, anchors, retrieval ledger, cost ledger, omissions, visual Pending items, and fallback reason. Report Recall/Precision, protected-fact recall, estimated tokens, file bytes, image counts, latency, and downstream answer quality separately. If labels or provider telemetry do not exist, mark the metric `Pending`.

## Validation and fallback

A smaller context with lower evidence coverage is a failure. Expand retrieval or preserve the source when required slots are missing, facts conflict, visual evidence is unchecked, or protected literals are lost.

## Example

```text
ON：把这个扫描 PDF 和视频整理成可追溯的 Context Pack，并分别报告命中、保真和估算 Token。
```

## Limits

The controller does not install local runtimes, download models, enable network access, or broaden authorization. Route availability depends on the installed child Skill and current environment.
