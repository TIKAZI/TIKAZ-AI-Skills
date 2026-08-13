---
name: html-deck-builder
description: Plan and build browser-editable HTML presentations with narrative contracts, responsive slide layouts, keyboard navigation, offline-safe assets, and render verification. Use when the final presentation should be an HTML file or browser-based deck rather than a native PPTX.
---

# HTML Deck Builder

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## TIKAZ Edition

- Type: original workflow; no upstream deck engine or assets are bundled.
- TIKAZ contribution: page contracts, early representative rendering, offline dependency policy, interaction/accessibility checks, and export evidence.

## Inputs

Accept a brief or source material, audience, duration, browser target, aspect ratio, editability needs, offline boundary, and requested exports.

## Workflow

1. Freeze audience, duration, narrative goal, delivery browser, editability, offline needs, and export formats.
2. Write a page contract for every slide: role, one claim, evidence, visual job, content limit, speaker intent, and source/license status.
3. Choose one visual system and define type scale, grid, spacing, palette, image treatment, and motion budget.
4. Build the opening, one dense representative slide, and the ending first. Render desktop and target projector sizes before completing the deck.
5. Author semantic HTML with keyboard navigation, visible focus, reduced-motion support, and no network dependency unless the user accepts it.
6. Verify overflow, contrast, legibility, source labels, media licenses, navigation, browser console, and requested export files.

Do not invent citations, download unlicensed media, or claim PowerPoint editability for an HTML-only output.

## Output contract

Return a self-contained or explicitly packaged HTML deck, page contracts, asset and license ledger, navigation behavior, rendered preview evidence, requested exports, and known browser limitations.

## Validation and fallback

Open the final HTML in the target browser, test keyboard navigation, focus, reduced motion, target viewports, console, overflow, and offline behavior. If export tooling is unavailable, deliver the verified HTML and mark the missing export rather than fabricating it.

## Example

```text
Use html-deck-builder to create an offline browser-editable product deck, render the opening and densest slide early, and verify keyboard navigation.
```
