# Conversion adapters

The standard-library core directly reads Markdown, text, JSON/JSONL, CSV/TSV, YAML, HTML, common code, configuration, and log files. It does not silently OCR or parse proprietary binary formats.

For PDF or Office input, use an available external converter such as a local document-to-Markdown workflow, inspect representative pages or sections for fidelity, and pass the resulting Markdown to `tikaz-context pack`. Keep the original file unchanged and report losses. Run `doctor` to inspect availability; it never installs software.

Use the profiler before conversion decisions:

- pure text and structurally safe tables -> `text`;
- text plus informative figures or complex tables -> `hybrid`;
- scans, design/layout-heavy assets, low-confidence extraction, or missing page references -> `source`.

In `hybrid`, Markdown is the primary text asset. Put only task-relevant figures or source visuals into `visual-evidence.json`, deduplicate repeated targets, cap `--visual-budget`, and let an image-capable host resolve queued items. Keep descriptions, detected values, uncertainty, and the original page/image anchor together. If no vision capability is available, keep `pending-vision` and recommend the relevant source page rather than silently flattening it.
