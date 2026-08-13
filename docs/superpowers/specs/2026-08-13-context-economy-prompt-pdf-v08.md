# Spec: Context Economy v0.8 Prompt and PDF Evidence

## Objective

Improve prompt preparation beyond byte-for-byte repetition while keeping instruction drift measurable, and add a real generated-PDF conversion benchmark with known ground truth.

## Prompt modes

- `exact`: remove identical repeated non-empty lines only.
- `structural`: normalize whitespace, bullet markers, heading markers, and terminal punctuation for duplicate detection while preserving the first original wording.
- `semantic`: reserved for an optional model/evaluator path; disabled by default and excluded from public savings until downstream equivalence passes.

All modes preserve literal protected facts. Report each mode separately and use pass-through when preparation overhead is not economical.

## PDF fidelity dimensions

- required text recall;
- numeric fact recall;
- table-cell recall;
- page-anchor coverage;
- conversion warnings;
- visual inspection status.

The benchmark uses TIKAZ-authored PDFs generated from declared ground truth. Text-first, table-first, and illustrated documents remain separate. Scanned OCR and AI vision-description accuracy are later profiles.

## Boundaries

- MarkItDown is an external adapter; its version/path is recorded, not bundled.
- Text extraction is not layout or image understanding.
- A rendered-page visual check verifies fixture quality, not conversion correctness by itself.
- No model/API call or secret access is required.

