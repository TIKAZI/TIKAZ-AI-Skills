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

The public benchmark now separates two profiles. The 30 micro correctness cases pass their declared budget, fact, and anchor checks but grow from 1,375 to 3,354 estimated tokens, a 143.93% increase caused by protocol overhead. The six long-context efficiency tasks reuse one synthetic source and shrink from 4,698 to 1,422, a 69.73% reduction, while retaining their declared facts and expected anchors. This is not a downstream semantic-equivalence test or a cross-project leaderboard. See the [fixed-version comparison](../docs/research/context-compression-comparison.md).

## Limits

- Counts use the repository's documented deterministic heuristic, not provider billing telemetry.
- A different task query, source language, tokenizer, or risk profile may save more, save less, or correctly choose `pass-through`.
- Lexical relevance does not establish source truth or semantic equivalence.
