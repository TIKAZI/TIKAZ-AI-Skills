---
name: context-benchmark
description: Measure context preparation across fixed cases. Use when token savings, hard-budget compliance, protected-fact recall, evidence anchors, determinism, runtime, or downstream answer quality must be demonstrated with reproducible evidence rather than marketing claims.
---

# Context Benchmark

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Run a versioned manifest of independent cases and keep raw per-case results. Report efficiency and quality separately:

- source and packed tokens;
- final-budget compliance;
- protected-fact recall;
- evidence-anchor correctness;
- deterministic repeatability;
- preparation runtime;
- optional externally supplied answer score.

Do not hide failures inside averages. A smaller pack with lower fidelity is a regression, not a win. Use the shared CLI `benchmark` command and read `../references/benchmark-method.md` when publishing results.

From the suite directory, run `python scripts/tikaz_context.py benchmark --manifest benchmarks/manifest.json --output <directory>`. Inspect both `summary.json` and `cases.json`; a passing case is not evidence of positive savings or semantic equivalence.
