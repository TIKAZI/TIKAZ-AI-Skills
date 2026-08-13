---
name: conversation-checkpoint
description: Use when a long or repetitive conversation has no source file and must be converted into a recoverable task state before continuation, handoff, or compaction.
---

# Conversation Checkpoint

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## Input

Accept a long or repetitive conversation transcript and, when known, the next task or handoff audience. Use this Skill when no authoritative source file already captures the current state.

## Workflow

Create a state snapshot with these required sections:

- Goal
- Confirmed Constraints
- Decisions
- Completed
- Remaining
- Evidence
- Open Questions

Preserve the latest user instruction, approvals, rejected directions, file paths, identifiers, numbers, URLs, commands, errors, and objective verification. Separate completed facts from proposed work. Remove conversational repetition only after its surviving decision or constraint is recorded.

Validate the snapshot against the available transcript. Missing protected facts must be restored or listed as omissions. A concise snapshot is not proof that the underlying work succeeded.

## Output contract

Return one self-contained Markdown checkpoint containing the seven required sections, the latest user instruction, objective verification state, unresolved conflicts, protected identifiers, and visible omissions. Separate confirmed completion from proposals and agent assumptions.

## Validation and fallback

Compare the checkpoint with the transcript using `validate-snapshot`. Restore missing numbers, paths, URLs, commands, approvals, rejections, or error text. If the transcript is incomplete or contradictory, preserve the conflict instead of choosing silently. Never mark work complete solely because the conversation said it was complete.

## Example

```text
Create a recoverable checkpoint from this conversation before handoff. Preserve decisions, rejected directions, completed evidence, file paths, commands, numbers, and open questions.
```

Run `python scripts/tikaz_context.py checkpoint --source <transcript.md> --output <checkpoint.md>`. Use `validate-snapshot` when checking an edited checkpoint against its original transcript.
