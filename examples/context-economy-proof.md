# Context Economy method demonstration

This is a reproducible fixture, not a universal performance claim.

## Task

Prepare two Markdown files for this query:

```text
release version 0.4.0 validation tests commands evidence anchors
```

Run:

```powershell
python .\suites\context-economy\scripts\tikaz_context.py pack `
  --input .\examples\context-economy-source.md `
  --input .\examples\context-economy-extra.md `
  --query 'release version 0.4.0 validation tests commands evidence anchors' `
  --budget 360 `
  --output .\.context-economy-demo
```

## Observed fixture result

| Measurement | Estimated tokens |
|---|---:|
| Source input | 364 |
| Unique content after exact deduplication | 329 |
| Exact duplicate content removed | 35 |
| Final context pack including protocol labels | 311 |
| Net difference | 53 fewer (14.6%) |

The run selected `pass-through` mode, retained three unique anchored sections, and removed one exact duplicate. It preserved version `0.4.0`, the source URL, and the complete PowerShell validation block.

The 30-case public correctness suite separately reports 100% budget compliance, declared protected-fact recall, and expected-anchor correctness on its synthetic fixtures. Across the suite, 1,375 estimated source tokens become 3,588 packed tokens, a 160.95% increase because protocol labels dominate. Only 14 cases declare protected facts, so this is neither an all-facts claim nor a savings claim. This longer fixture demonstrates the break-even case instead.

## Limits

- Counts use the repository's documented deterministic heuristic, not provider billing telemetry.
- A different task query, source language, tokenizer, or risk profile may save more, save less, or correctly choose `pass-through`.
- Lexical relevance does not establish source truth or semantic equivalence.
