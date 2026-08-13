# Implementation Plan: Context Economy v0.7 Public Evidence

1. Add failing tests for prompt compilation, multimodal expectations, aggregate fidelity rates, and report generation.
2. Extend the benchmark schema with `context`, `prompt`, and multimodal expectation fields while retaining schema v1 compatibility.
3. Add independent public fixtures and regenerate raw results, metrics JSON, and Markdown evidence card.
4. Link generated evidence from the suite and collection README; record methodology and pending evidence.
5. Run full regression, distribution validation, sensitive scan, and commit only to the isolated branch.

