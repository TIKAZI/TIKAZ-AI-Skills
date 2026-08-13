---
name: context-benchmark
description: Measure context preparation across fixed cases. Use when token savings, hard-budget compliance, protected-fact recall, evidence anchors, determinism, runtime, or downstream answer quality must be demonstrated with reproducible evidence rather than marketing claims.
---

# Context Benchmark

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## Inputs

Accept a versioned benchmark manifest, fixed source fixtures, declared budgets, protected facts, expected anchors, optional route labels, and an optional externally scored downstream-answer rubric. Use identical inputs and settings when comparing systems.

## Workflow

Run a versioned manifest of independent cases and keep raw per-case results. Report efficiency and quality separately:

- source and packed tokens;
- final-budget compliance;
- protected-fact recall;
- evidence-anchor correctness;
- deterministic repeatability;
- preparation runtime;
- optional externally supplied answer score.
- document-route correctness, informative-visual recall, decorative/duplicate skip accuracy, and complex-table fidelity warnings for multimodal fixtures.

Do not hide failures inside averages. A smaller pack with lower fidelity is a regression, not a win. Do not claim superiority until the same files, questions, model/detail settings, budgets, and blind answer rubric are used. Use the shared CLI `benchmark` command and read `../references/benchmark-method.md` when publishing results.

## Output contract

Publish `summary.json`, `metrics.json`, raw `cases.json`, and the generated evidence card together. Keep context efficiency, exact-repeat prompt efficiency, literal fact and anchor fidelity, multimodal routing, and pending provider, vision, or downstream evidence separate; never replace them with one composite fidelity score.

## Validation and fallback

Keep failed cases visible and verify manifest version, fixture identity, budgets, settings, and denominators. Estimated tokens must be labeled estimates. If provider telemetry or blind downstream scoring is unavailable, mark it `Pending`; do not infer superiority from local fixtures.

## Example

```text
Benchmark this context workflow against the fixed manifest. Report efficiency and protected-fact recall separately, retain failed cases, and label provider-token measurements Pending.
```

From the suite directory, run `python scripts/tikaz_context.py benchmark --manifest benchmarks/manifest.json --output <directory>`. Inspect both `summary.json` and `cases.json`; a passing case is not evidence of positive savings or semantic equivalence.
