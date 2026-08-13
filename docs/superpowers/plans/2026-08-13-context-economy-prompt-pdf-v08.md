# Implementation Plan: Context Economy v0.8 Prompt and PDF Evidence

1. Add failing tests for structural prompt deduplication, protected-fact retention, explicit adapter discovery, and PDF fidelity scoring.
2. Implement prompt modes, `prompt` CLI, adapter-aware doctor, and `pdf-fidelity` CLI.
3. Generate TIKAZ-owned PDFs from ground-truth manifests; render and inspect them.
4. Convert with the local MarkItDown wrapper and publish separate fidelity dimensions.
5. Regenerate public metrics, document negative/pending results, validate distribution, and commit locally.

