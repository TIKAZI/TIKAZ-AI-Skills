# Spec: Context Economy v0.7 Public Evidence

## Objective

Generate reproducible GitHub-facing evidence for efficiency and fidelity without collapsing unlike measurements into one marketing score.

## Public metric families

1. Context efficiency: source, final pack, reduction, and protocol overhead by profile.
2. Prompt efficiency: exact repeated instruction removal only; no semantic paraphrase claim.
3. Literal fidelity: protected-fact recall and expected-anchor correctness.
4. Multimodal routing: route accuracy, informative-visual count accuracy, decorative/duplicate skip accuracy, and complex-table risk-gate accuracy.
5. Operations: hard-budget compliance, deterministic cases, dependency/network status.
6. Pending evidence: real PDF conversion fidelity, provider input-token telemetry, vision-description accuracy, and downstream blind-answer quality.

## Output

- `benchmarks/results/metrics.json`: machine-readable evidence.
- `benchmarks/results/README.md`: GitHub evidence card with numerators, denominators, methods, and limits.
- `benchmarks/results/cases.json`: raw case results.

## Boundaries

- Never label byte reduction as token reduction.
- Never publish one overall fidelity score.
- A percentage without a sample denominator fails the publication gate.
- Estimated text tokens and provider telemetry remain distinct.
- Pending metrics remain visible instead of being omitted.

## Acceptance criteria

- Multimodal cases are independent synthetic fixtures with declared expected routes and counts.
- Prompt cases measure literal duplicate removal and protected-fact retention.
- The report is deterministically regenerated from the public manifest.
- README links to the evidence report and quotes only generated values.

