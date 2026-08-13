---
name: powerpoint-deck-builder
description: Plan, create, revise, and verify native editable PowerPoint presentations with source-aware content, reusable layouts, speaker notes, and rendered visual QA. Use when the deliverable must be an editable .pptx or must reuse an existing PowerPoint template.
---

# PowerPoint Deck Builder

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## TIKAZ Edition

- Type: original tool-agnostic workflow; no third-party templates, fonts, images, or scripts are bundled.
- TIKAZ contribution: narrative-to-page contract, editability gate, template fidelity rules, render/overflow QA, and delivery evidence.

## Inputs

Accept a brief or source files, audience, duration, aspect ratio, required template, editability, notes, charts, language, and delivery constraints.

## Workflow

1. Determine audience, talk length, aspect ratio, required template, editability, notes, charts, and delivery constraints.
2. Convert the narrative into page contracts with one claim and one visual job per slide.
3. Use the available PowerPoint-capable runtime; inspect a provided template before authoring and preserve its layout rules.
4. Keep text, charts, tables, and core shapes editable. Record the license and source for external media.
5. Render the deck to images and inspect representative and dense slides; iterate on overflow, collisions, hierarchy, contrast, and repetition.
6. Reopen or inspect the final `.pptx`, confirm slide count and notes, and report the exact artifact plus verification evidence.

Do not treat successful file generation as visual approval, and do not claim editable output when important content was flattened without disclosure.

## Output contract

Return the editable `.pptx`, narrative and page contracts, template or font substitutions, source and license ledger, speaker notes when requested, rendered slide evidence, and final file inspection results.

## Validation and fallback

Render every slide, inspect dense and representative slides, verify overflow and collisions, reopen the final deck, and confirm slide count, notes, and editability. If the required template, font, or renderer is unavailable, disclose the substitution or stop before claiming fidelity.

## Example

```text
Use powerpoint-deck-builder to create an editable 16:9 deck from this brief, preserve the supplied template, render every slide, and report substitutions.
```
