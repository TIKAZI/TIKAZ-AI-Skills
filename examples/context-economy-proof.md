# Context Economy method demonstration

This is a reproducible fixture, not a universal performance claim.

## Task

Prepare two Markdown files for this query:

```text
release version 0.4.0 validation tests commands evidence anchors
```

Run:

```powershell
python .\suites\context-economy\scripts\context_economy.py pack `
  --input .\examples\context-economy-source.md `
  --input .\examples\context-economy-extra.md `
  --query 'release version 0.4.0 validation tests commands evidence anchors' `
  --budget 180 `
  --output .\.context-economy-demo
```

## Observed fixture result

| Measurement | Estimated tokens |
|---|---:|
| Source input | 364 |
| Unique content after exact deduplication | 329 |
| Exact duplicate content removed | 35 |
| Final context pack including protocol labels | 306 |
| Net difference | 58 fewer (15.9%) |

The run selected `select` mode, retained two anchored sections, and listed four omitted anchors. It preserved version `0.4.0`, the source URL, and the complete PowerShell validation block.

The first implementation failed this demonstration: protocol labels and duplicated protected facts produced a 448-token pack from a 364-token input. That regression is now fixed by a test requiring positive end-to-end savings on this fixture. The change also stopped repeating protected facts already present in exact evidence and added a relative relevance threshold rather than filling the budget with weak matches.

## Limits

- Counts use the repository's documented deterministic heuristic, not provider billing telemetry.
- A different task query, source language, tokenizer, or risk profile may save more, save less, or correctly choose `pass-through`.
- Lexical relevance does not establish source truth or semantic equivalence.
