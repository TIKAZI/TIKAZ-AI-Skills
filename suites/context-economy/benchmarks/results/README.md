# TIKAZ Context Economy — Reproducible Evidence

Dataset: `tikaz-context-economy-public-v1` · Cases: **46** · Text counts: **estimated, not provider billing telemetry**.

## Evidence card

| Metric | Result | Evidence boundary |
|---|---:|---|
| Context reduction | 21.4% (6073 → 4776 estimated tokens) | Aggregate; inspect profiles because short inputs may grow |
| Prompt exact-repeat reduction | 37.1% (62 → 39) | 2 prompt cases; no semantic rewrite claim |
| Protected-fact recall | 100.0% (38/38) | Literal declared facts only |
| Anchor correctness | 100.0% (39/39) | Declared expected anchors only |
| Route accuracy | 100.0% (8/8) | Text / Hybrid / Source labeled cases |
| Visual filtering accuracy | 100.0% (8/8) | Informative, decorative, duplicate, and table-risk counts |
| └ Informative-visual count | 100.0% (7/7) | Human-declared synthetic cases |
| └ Decorative-image skips | 100.0% (7/7) | Human-declared synthetic cases |
| └ Duplicate-image skips | 100.0% (7/7) | Human-declared synthetic cases |
| └ Complex-table risk gate | 100.0% (7/7) | Human-declared synthetic cases |
| Budget compliance | 100.0% (39/39) | Complete generated packs |

## Profile results

| Profile | Cases | Source | Final | Reduction | Passed |
|---|---:|---:|---:|---:|---:|
| correctness | 30 | 1375 | 3354 | -143.9% | 30/30 |
| efficiency | 6 | 4698 | 1422 | 69.7% | 6/6 |

## Pending — not yet claimed

- Real PDF conversion fidelity: **Pending**
- Actual provider input-token savings: **Pending**
- Vision-description accuracy: **Pending**
- Downstream blind-answer quality: **Pending**

## Reproduce

```powershell
python scripts/tikaz_context.py benchmark --manifest benchmarks/manifest.json --output benchmarks/results --prune-artifacts
```

Raw evidence: [`metrics.json`](metrics.json) · [`cases.json`](cases.json) · [`summary.json`](summary.json)

> There is no overall fidelity score. Percentages describe separate, declared checks and include their sample counts.
