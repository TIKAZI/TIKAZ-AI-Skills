# Spec: Context Economy v0.6 Multimodal Compiler

## Objective

Compile mixed documents into a traceable, task-bounded context asset instead of blindly converting every file to plain text or sending every page image to a model. Preserve useful tables and visual evidence while measuring file preparation, canonical text, prompt/protocol, visual routing, and final context separately.

## Confirmed decisions

- Route on **informative visual evidence**, not merely the presence of an image.
- Use `text`, `hybrid`, or `source` document routes.
- Keep the standard-library core offline and dependency-free.
- Treat external conversion, OCR, page rendering, tokenizer telemetry, and vision inference as optional adapters.
- Emit a visual-evidence queue that an image-capable Codex host can inspect; never claim an image was understood when no vision step ran.
- Keep original files unchanged, retain SHA-256 and source/page anchors, and make conversion risks visible.
- Report bytes and estimated tokens as separate units. Never convert byte reduction into token reduction.

## Commands

```powershell
python .\suites\context-economy\scripts\tikaz_context.py profile --input .\report.md --query "compare revenue" --output .\.context-economy
python .\suites\context-economy\scripts\tikaz_context.py pack --input .\report.md --query "compare revenue" --budget 800 --visual-budget 4 --output .\.context-economy
python -m unittest discover -s tests -p "test_context_economy*.py"
```

## Architecture

- `profile_document`: inspect supported text/Markdown plus conservative PDF metadata without model calls.
- `route_document`: choose `text`, `hybrid`, or `source` from informative visuals, table complexity, extraction confidence, and available adapters.
- `build_visual_evidence_queue`: deduplicate visual references, skip likely decoration, rank task relevance, and cap the queue.
- `build_pack`: retain the current hard-budget text pack and add document profiles, visual queue, and a Context Cost Ledger.
- Skill instructions: let Codex inspect queued images when an image-capable tool is available, write anchored descriptions, and otherwise leave them pending.

## Route contract

| Route | Conditions | Output |
|---|---|---|
| `text` | No informative visuals; tables are structurally safe | Canonical Markdown and text pack |
| `hybrid` | Informative images or complex tables exist and can be individually referenced | Markdown plus bounded visual-evidence queue |
| `source` | Scan/layout-heavy source, missing safe extraction path, or low fidelity | Preserve source and request source/page visual handling |

## Testing strategy

- Unit tests for image classification, duplicate filtering, table-complexity flags, and route selection.
- CLI test for `profile` and `pack --visual-budget` artifacts.
- Regression tests for all existing pack, checkpoint, audit, doctor, and benchmark behavior.
- Standalone distribution validation after export.

## Boundaries

- Always: label estimates, retain anchors/hashes, show pending visual work and conversion warnings.
- Ask first: install OCR/rendering/model dependencies or send private documents to an external API.
- Never: silently discard complex visuals, invent image descriptions, claim semantic equivalence, or claim market leadership without matched A/B evidence.

## Success criteria

- Informative Markdown images trigger `hybrid`; decorative/repeated images do not consume the visual budget.
- Complex tables receive `visual-verification-required` when a source visual exists or a clear warning when it does not.
- `profile.json`, `visual-evidence.json`, and `context-cost-ledger.json` are reproducible.
- The cost ledger separates original bytes, canonical text estimate, prompt/protocol estimate, selected evidence, final pack, and visual item counts.
- Missing optional vision/conversion capability degrades safely without installation.

