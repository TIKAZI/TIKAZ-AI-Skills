# Generated PDF Fidelity Evidence

Three TIKAZ-authored PDFs are generated from [`ground-truth.json`](../ground-truth.json), converted page by page, and scored with literal declarations.

| Dimension | Result | Boundary |
|---|---:|---|
| Required text recall | 100% | Declared literal strings in 3 generated PDFs |
| Numeric fact recall | 100% | Declared numbers, versions, and percentages |
| Table-cell recall | 100% | Declared cells; no merged-cell or layout claim |
| Page-anchor coverage | 100% | 4/4 generated page anchors |
| Visual-description accuracy | Pending | Text extraction does not prove diagram understanding |

The recorded run used the already-installed `pdfplumber` adapter. The local MarkItDown command was also tested, but its PDF optional dependency was absent; command discovery alone is therefore not reported as PDF support. No dependency was installed by the benchmark.

Reproduce with an environment that already has `pdfplumber`:

```powershell
python benchmarks/pdf/generate_fixtures.py
python benchmarks/pdf/run_fidelity.py --adapter pdfplumber --ground-truth benchmarks/pdf/ground-truth.json --output benchmarks/pdf/results
```

For MarkItDown, pass `--adapter markitdown --converter <path>` and publish the result only if the conversion completes. Real-world PDFs, scanned OCR, merged tables, diagrams, and vision descriptions remain separate future profiles.

Raw evidence: [`metrics.json`](metrics.json) · [`converted/`](converted/)
