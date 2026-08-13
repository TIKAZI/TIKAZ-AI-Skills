# Benchmark method

Use the versioned public manifest in `../benchmarks/manifest.json`. Each case declares synthetic source files, a task, a complete-output budget, protected facts, and expected source anchors. Interpret profiles separately: `correctness` tests small-input behavior; `efficiency` tests selection from longer sources.

Report four independent measures: complete-pack budget compliance, estimated token savings, literal protected-fact recall, and expected-anchor correctness. Preserve raw per-case failures in `cases.json`; never hide a failed case in the aggregate.

The estimator is deterministic but is not provider billing telemetry. Cases with no declared protected facts are reported as vacuously complete and must not be counted as evidence that all facts were preserved. The benchmark does not measure answer quality or semantic equivalence. Add externally scored answer quality only as a separate field with its evaluator and rubric disclosed.

The bundled efficiency cases reuse one synthetic source across six tasks. Report that limitation whenever publishing their aggregate. Do not compare the percentage directly with command-output filters, model-based compressors, or proxy systems unless all projects run the same corpus, task, tokenizer, budget unit, and downstream evaluation.

For multimodal claims, add independent files with human-labeled informative/decorative visuals, duplicate targets, simple/complex tables, required source anchors, and blind downstream questions. Hold the model, image detail, page rendering, prompt, and token telemetry constant. Report routing accuracy, informative-visual recall, decorative skip precision, table-cell fidelity, answer correctness, latency, and input cost separately.

Report prompt preparation by mode. `exact` is the conservative baseline. `structural` may normalize formatting for duplicate detection but must keep the first original wording. Include no-duplicate controls so a mode is not rewarded merely for receiving easy repeated inputs. Keep semantic compression disabled or separately labeled until a downstream equivalence rubric passes.

For PDF conversion, generate fixtures from declared ground truth, render and visually inspect the fixtures, then convert page by page. Score required text, numeric facts, table cells, and page anchors separately. Record the adapter and failed capability probes. Literal extraction must never be presented as layout fidelity, diagram understanding, OCR accuracy, or real-world corpus coverage.
