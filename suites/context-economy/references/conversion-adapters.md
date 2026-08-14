# Conversion adapters

The standard-library core directly reads Markdown, text, JSON/JSONL, CSV/TSV, YAML, HTML, common code, configuration, and log files. It does not silently OCR or parse proprietary binary formats.

For PDF or Office input, use an available external converter such as a local document-to-Markdown workflow, inspect representative pages or sections for fidelity, and pass the resulting Markdown to `tikaz-context pack`. Keep the original file unchanged and report losses. Run `doctor` to inspect availability; it never installs software.

Executable discovery is only a probe, not a capability guarantee. A converter can exist while its PDF/OCR extras are missing. Run a known fixture before declaring a format supported, record the adapter used, and retain conversion failures as evidence. The public generated-PDF benchmark supports explicit `markitdown` and `pdfplumber` adapters without bundling either one.

## Webpage adapter

The optional `adapters/defuddle` bridge pins Defuddle `0.19.2` and linkedom `0.18.13`. Install it explicitly with `npm ci` inside that adapter directory; the Python core and `doctor` never run package installation. The bridge parses supplied HTML without executing page scripts, uses `separateMarkdown: true`, retains images, and disables Defuddle's third-party async fallback with `useAsync: false`.

```powershell
python .\scripts\tikaz_context.py web `
  --url 'https://example.com/article' `
  --task 'extract release evidence' `
  --output .\.context-economy-web
```

Only public HTTP(S) targets are accepted. Local, private, reserved, and link-local addresses are rejected; redirects are revalidated; fetches have explicit size and timeout bounds. Dynamic client-rendered shells, extraction failures, and missing dependencies return `source` instead of pretending Markdown is complete.

Use the profiler before conversion decisions:

- pure text and structurally safe tables -> `text`;
- text plus informative figures or complex tables -> `hybrid`;
- scans, design/layout-heavy assets, low-confidence extraction, or missing page references -> `source`.

In `hybrid`, Markdown is the primary text asset. Put only task-relevant figures or source visuals into `visual-evidence.json`, deduplicate repeated targets, cap `--visual-budget`, and let an image-capable host resolve queued items. Keep descriptions, detected values, uncertainty, and the original page/image anchor together. If no vision capability is available, keep `pending-vision` and recommend the relevant source page rather than silently flattening it.
