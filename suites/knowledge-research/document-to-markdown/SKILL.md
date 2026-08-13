---
name: document-to-markdown
description: Convert PDF, Office, HTML, images, and audio into structured Markdown while preserving headings, tables, links, and provenance where possible. Use when source documents need extraction or normalization before research and knowledge capture.
---

# Document to Markdown

This TIKAZ Edition is designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## Inputs and workflow

Accept PDF, Office, HTML, image, audio, or other supported source files plus the downstream task. Detect an available structured converter, preserve the original, convert to UTF-8 Markdown, retain page or section provenance where possible, and inspect representative headings, tables, links, reading order, media references, and OCR quality.

## Output contract

Return the Markdown artifact, source-to-output mapping, converter used, extracted assets or references, representative fidelity checks, and a visible loss report for layout, images, complex tables, formulas, or OCR uncertainty.

## Validation and fallback

Verify that output exists and contains representative declared facts. Do not assume a fixed executable path or silently install a converter. If conversion cannot preserve task-relevant evidence, retain the source page or file and recommend visual or manual inspection.

## Example and limits

```text
Use document-to-markdown on this PDF. Preserve page anchors, headings, links, tables, and image references, then report every fidelity loss.
```

Markdown normalization is not proof of semantic, layout, OCR, chart, or formula fidelity.
