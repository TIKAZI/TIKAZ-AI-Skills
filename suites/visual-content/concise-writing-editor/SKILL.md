---
name: concise-writing-editor
description: Remove AI filler, vague claims, repetitive structure, inflated transitions, and low-information phrasing while preserving meaning and voice. Use when writing sounds generic, padded, templated, or difficult to trust.
---

# Concise Writing Editor

This clean-room TIKAZ Edition is designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## Inputs and workflow

Accept the original text, intended audience, purpose, voice constraints, protected facts, and desired editing strength. Identify the conclusion, evidence, necessary nuance, repetition, vague claims, generic transitions, and templated structure. Edit only what reduces clarity or trust, preserving the author's meaning and useful voice.

## Output contract

Return the revised text, a concise change summary, protected facts retained, material meaning changes if any, and unresolved claims that need evidence. Provide before and after excerpts when they help review.

## Validation and fallback

Compare names, numbers, URLs, quotes, constraints, causal claims, and limitations against the source. If the desired voice is unclear, perform a conservative pass. Do not make text shorter at the cost of deleting necessary facts, limitations, or causal explanation.

## Example and limits

```text
Use concise-writing-editor on this README. Remove filler and repeated framing, preserve every technical limitation and measured result, and summarize material edits.
```

This Skill improves expression, not the truth of unsupported claims.
