---
name: visual-content
description: Orchestrate article illustration, logistics explainers, writing cleanup, and lawful music discovery with explicit style routing, asset provenance, accessibility text, and visual QA. Use for content packages that need coherent visuals without generic image generation.
---

# Visual Content

Designed, integrated, refactored, and continuously maintained by **TIKAZ**.

## Inputs and routing

Accept the content or thesis, audience, publishing surface, required asset, factual sources, accessibility needs, and license boundary. Use one child Skill directly when writing cleanup, one illustration identity, or lawful music discovery is the whole task.

## TIKAZ method

1. Extract the content thesis, audience, publishing surface, visual jobs, claims, and accessibility needs.
2. Use `concise-writing-editor` only when the source is padded or generic; preserve facts and author voice.
3. Route to exactly one illustrator: `xiaohei-article-illustrator` or `zhuge-logistics-illustrator`.
4. Create a shot card: message, scene/mechanism, composition, labels, character role, palette, forbidden elements, source assets, and license status.
5. Review at publishing size for message clarity, text accuracy, character consistency, cropping, hierarchy, and alt text.
6. Use `legal-free-music` only when music is requested; retain license and attribution evidence with the selected file.

## Boundary

This suite intentionally excludes `生图-Image2`. It defines content and QA workflows without requiring a specific image-generation provider.

## Output, fallback, and limits

Return the selected route, shot or editing contract, source and license ledger, accessible text, publishing-size QA, and final asset or explicit creation handoff. If no drawing or generation tool is available, deliver an editable SVG/HTML specification or shot card rather than pretending an image was produced. Never turn uncertain labels or claims into definitive visuals.

## Example

```text
Use visual-content to clean this article, choose one illustration route, create a sourced shot card, and verify labels, licenses, alt text, and publishing-size clarity.
```

Read [references/routing.md](references/routing.md) and [references/output-contract.md](references/output-contract.md).
