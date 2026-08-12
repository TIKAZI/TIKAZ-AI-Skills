---
name: context-pack
description: Prepare files, folders, code, logs, and structured data as a bounded, traceable context pack for Codex. Use when source material must be converted, deduplicated, selected, budgeted, or handed off with exact evidence anchors.
---

# Context Pack

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Own canonical ingestion, exact deduplication, evidence selection, and final pack size. Assemble one task-ready artifact in this order:

1. task and expected output;
2. selected mode and estimated budget;
3. confirmed constraints and protected facts;
4. exact evidence excerpts with source anchors;
5. decisions, completed work, and current state;
6. conflicts and open questions;
7. omitted-anchor inventory and verification limits.

The pack must distinguish exact source text, structured state, and inference. It must remain useful without the surrounding chat. Count the complete artifact against the budget. If essential protected evidence cannot fit, return a visible budget conflict instead of silently exceeding the limit.

Run `python scripts/tikaz_context.py pack --input <path> --query <task> --budget <tokens> --output <directory>`. Read the final artifact at `<directory>/packs/current-task.context.md`; supporting canonical files, indexes, the ledger, and the savings report remain beside it.
