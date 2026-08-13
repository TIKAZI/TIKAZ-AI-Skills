# Context compression comparison

Checked on 2026-08-13. Percentages below describe different workloads and are not a single leaderboard.

| Project | Fixed version | Public scope | Published result | Local status |
|---|---|---|---|---|
| TIKAZ Context Economy | `9fbf283` + current benchmark changes | Bounded, anchored packs from files and conversations | Long-context efficiency profile: 4,698 → 1,422 estimated tokens, 69.73% reduction; 6/6 declared-fact and anchor cases pass | Reproduced locally |
| RTK | `v0.45.0` | Bash and developer-command output | Up to 90% less bash output; README explicitly says this is not 90% off the bill and estimates tokens as bytes/4 | Official fixed-release evidence only; CLI not installed |
| Headroom | `v0.34.0` | Tool output, logs, JSON, files, RAG, history, proxy workflows | Published aggregate 23,921 → 8,110, 66.1%; JSON example 10,144 → 1,260, 87.6%, with four answer checks | Official fixed-release evidence only; CLI not installed |
| LLMLingua | `v0.2.2` | Model-driven natural-language prompt compression | Official example 2,365 → 211, 11.2×; repository claims up to 20× with downstream evaluations | Official fixed-release evidence only; model stack not installed |

## What the TIKAZ result proves

- Six task-specific selections over one synthetic long source fit their complete output budgets.
- All 11 declared literal facts and six expected anchors are present.
- The deterministic estimator reports a 69.73% reduction for the efficiency profile.
- The zero-network path uses the Python standard library and preserves an omitted-anchor inventory.

## What it does not prove

- It is not a head-to-head run on the competitors' datasets or tokenizers.
- The six efficiency cases reuse one TIKAZ-authored source, so they are not six independent corpora.
- Literal fact recall is not semantic equivalence or downstream answer accuracy.
- Estimated tokens are not provider billing telemetry.
- RTK targets command output, Headroom covers a broader proxy/compression stack, and LLMLingua uses model inference. Their highest percentages cannot be transferred to this workflow.

## Reproduce TIKAZ

From the repository root:

```powershell
python -B .\suites\context-economy\scripts\tikaz_context.py benchmark `
  --manifest .\suites\context-economy\benchmarks\manifest.json `
  --output .\.context-economy-benchmark
```

Inspect both `summary.json` and `cases.json`. A passing correctness case is not necessarily a savings case.

## Fixed public sources

- [RTK v0.45.0](https://github.com/rtk-ai/rtk/tree/v0.45.0), Apache-2.0.
- [Headroom v0.34.0](https://github.com/headroomlabs-ai/headroom/tree/v0.34.0), Apache-2.0.
- [LLMLingua v0.2.2](https://github.com/microsoft/LLMLingua/tree/v0.2.2), MIT.

No third-party code, benchmark corpus, or distinctive documentation is redistributed in TIKAZ Context Economy.
