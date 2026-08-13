# Benchmark method

Use the versioned public manifest in `../benchmarks/manifest.json`. Each case declares synthetic source files, a task, a complete-output budget, protected facts, and expected source anchors. Interpret profiles separately: `correctness` tests small-input behavior; `efficiency` tests selection from longer sources.

Report four independent measures: complete-pack budget compliance, estimated token savings, literal protected-fact recall, and expected-anchor correctness. Preserve raw per-case failures in `cases.json`; never hide a failed case in the aggregate.

The estimator is deterministic but is not provider billing telemetry. Cases with no declared protected facts are reported as vacuously complete and must not be counted as evidence that all facts were preserved. The benchmark does not measure answer quality or semantic equivalence. Add externally scored answer quality only as a separate field with its evaluator and rubric disclosed.

The bundled efficiency cases reuse one synthetic source across six tasks. Report that limitation whenever publishing their aggregate. Do not compare the percentage directly with command-output filters, model-based compressors, or proxy systems unless all projects run the same corpus, task, tokenizer, budget unit, and downstream evaluation.
