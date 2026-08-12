# Conversion adapters

The standard-library core directly reads Markdown, text, JSON/JSONL, CSV/TSV, YAML, HTML, common code, configuration, and log files. It does not silently OCR or parse proprietary binary formats.

For PDF or Office input, use an available external converter such as the local `文档-MarkItDown` workflow, inspect representative pages or sections for fidelity, and pass the resulting Markdown to `tikaz-context pack`. Keep the original file unchanged and report losses. Run `doctor` to inspect availability; it never installs software.
