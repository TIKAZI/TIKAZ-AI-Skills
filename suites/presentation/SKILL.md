---
name: presentation
description: Route and govern presentation creation across browser-editable HTML decks, native editable PowerPoint, and magazine-style web decks. Use when a presentation request needs narrative planning, format selection, source tracking, rendering QA, and verified delivery.
---

# Presentation

Designed, integrated, refactored, and continuously maintained by **TIKAZ**.

## Inputs and routing

Accept the topic, audience, outcome, duration, source material, delivery environment, editability, template, and required formats. Use one child builder directly when HTML, PPTX, or editorial web output is already decided; otherwise use the orchestrator to choose exactly one primary format.

## TIKAZ method

1. Define audience, decision or learning outcome, duration, source material, delivery environment, and required editability.
2. Create one narrative brief before slide production: opening tension, section logic, evidence, takeaway, and ending action.
3. Route to exactly one builder: `html-deck-builder`, `powerpoint-deck-builder`, or `magazine-web-deck`.
4. Use a shared page contract: role, title, claim, evidence, visual job, content limits, speaker intent, and source/license status.
5. Render representative pages early; test full deck after authoring.
6. Check overflow, contrast, repetition, media licenses, chart truth, speaker flow, export integrity, and final file existence.

## License boundary

Builders keep their own upstream licenses. In particular, AGPL-derived builders remain separately licensed and must not be presented as solely covered by the collection license.

## Output, fallback, and limits

Return the narrative brief, page contracts, chosen builder, rendered QA evidence, source and license notes, final artifact path, and unresolved compatibility risks. If rendering or export is unavailable, do not treat file creation as visual approval. Do not claim native editability for flattened or HTML-only output.

## Example

```text
Use presentation to choose HTML or PPTX for this talk, write page contracts, render representative slides early, and verify the final artifact.
```

Read [references/routing.md](references/routing.md) and [references/output-contract.md](references/output-contract.md).
