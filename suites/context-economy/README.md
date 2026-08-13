# Context Economy for Codex

**Fidelity-first context preparation for files, prompts, conversations, tables, and visual evidence.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Context Economy is not a “compress everything” trick. It prepares the **smallest useful context that can still be checked**: documents become reusable Markdown, task-relevant evidence keeps stable source anchors, protected facts are verified, and visuals follow an explicit Text / Hybrid / Source route instead of being silently discarded or all sent to a vision model.

The optimization target is **lower context cost without silent information loss**. Reduction percentages are evidence from declared benchmarks, not the product promise.

## What it actually does

| Input or condition | Route | Result |
|---|---|---|
| Markdown, text, code, logs, structured data | **Text** | Canonical Markdown, exact/structural deduplication, anchored task selection, hard-budget context pack |
| PDF or Office document with extractable text | **Text or Hybrid** | External conversion to Markdown, page/section anchors, literal fact and table checks |
| Informative figure or complex table | **Hybrid** | Keep Markdown as the primary context and queue only relevant visual evidence for a vision-capable host |
| Decorative or repeated image | **Skip with evidence** | Record why it was omitted instead of spending visual context on it |
| Scan, layout-heavy file, missing converter, or uncertain extraction | **Source** | Preserve the original file/page and expose the unresolved gap; do not pretend conversion succeeded |
| Long conversation | **Checkpoint** | Recoverable state with decisions, constraints, completed evidence, files, numbers, and open questions |
| Repeated prompt instructions | **Exact or Structural** | Remove literal or formatting-only repetition while retaining the first original wording and protected facts |

Image routing is implemented and benchmarked. Image **meaning recognition** is performed only when the host provides vision and is not included in the current 100% literal-fidelity claims.

## Installable workflow

| Skill | Owns |
|---|---|
| `context-economy` | End-to-end routing and completion gate |
| `context-pack` | Canonical ingestion, exact deduplication, anchored selection, and hard-budget output |
| `conversation-checkpoint` | Recoverable conversation-only state |
| `context-audit` | Read-only six-dimension Context Health triage |
| `context-benchmark` | Reproducible efficiency and fidelity measurement |

The default CLI uses only the Python standard library and performs no network calls or model inference. Optional converters remain external and replaceable.

See the reproducible [Context Economy method demonstration](../../examples/context-economy-proof.md) and the [fixed-version comparison](../../docs/research/context-compression-comparison.md). The benchmark separates micro correctness from long-context efficiency so protocol overhead cannot hide behind one average.

## Reproducible evidence — measured, not advertised as universal

Current public synthetic benchmark (`50` cases), plus a separate generated-PDF fixture benchmark:

| Evidence family | Observed result | Scope |
|---|---:|---|
| Long-context efficiency | **69.7% reduction** · 4,698 → 1,422 estimated tokens | 6 task variants over one TIKAZ-authored long fixture |
| Short-input correctness | **143.9% growth** · 1,375 → 3,354 estimated tokens | 30 cases; proves the workflow should pass through small inputs |
| Prompt exact-repeat reduction | **14.6% reduction** · 157 → 134 estimated tokens | 4 cases including 2 structural-format controls with no exact duplicates |
| Prompt structural-repeat reduction | **49.5% reduction** · 95 → 48 estimated tokens | 2 structural variants; first wording retained, no semantic rewrite |
| Protected-fact recall | **100% · 46/46** | Literal declared facts, not semantic equivalence |
| Evidence-anchor correctness | **100% · 39/39** | Declared expected anchors |
| Text / Hybrid / Source routing | **100% · 8/8** | Synthetic labeled routing cases |
| Visual/table filtering checks | **100% · 8/8** | Informative, decorative, duplicate, and complex-table gates |
| Complete-pack budget compliance | **100% · 39/39** | Generated context packs |
| Generated-PDF literal fidelity | **100% text / numbers / table cells / page anchors** | 3 TIKAZ-authored PDFs; installed pdfplumber adapter; visual meaning excluded |

Read the generated [evidence card](benchmarks/results/README.md), [machine-readable metrics](benchmarks/results/metrics.json), [raw cases](benchmarks/results/cases.json), and [PDF fidelity evidence](benchmarks/pdf/results/README.md). Real-world/scanned PDF fidelity, actual provider input-token savings, vision-description accuracy, and downstream blind-answer quality remain explicitly **Pending**.

### How to read these numbers

- **69.7%** describes six long-context task variants over one synthetic source. It is not a universal saving guarantee.
- **14.6% Exact** includes controls with no exact repetition, so safe pass-through lowers the headline number by design.
- **49.5% Structural** removes formatting-only repetition without paraphrasing instructions.
- **100% protected facts and anchors** means every declared literal item survived these cases; it does not prove general semantic equivalence.
- **100% generated-PDF fidelity** covers declared text, numbers, cells, and page anchors—not OCR, layout reconstruction, or diagram interpretation.

## Quick start

```powershell
python .\scripts\tikaz_context.py pack `
  --input .\notes.md `
  --query 'prepare the release validation context' `
  --budget 800 `
  --visual-budget 4 `
  --output .\.context-economy
```

The output includes canonical Markdown, heading-aware indexes, `profile.json`, `visual-evidence.json`, `context-cost-ledger.json`, a bounded `packs/current-task.context.md`, and `savings-report.md`.

Profile routing without building a pack or running vision:

```powershell
python .\scripts\tikaz_context.py profile `
  --input .\notes.md `
  --query 'prepare the release validation context' `
  --visual-budget 4 `
  --output .\.context-economy-profile
```

`text` means Markdown is sufficient, `hybrid` means selected visuals remain as anchored `pending-vision` work, and `source` means safe conversion is unavailable or insufficient. Image presence alone never triggers vision.

Validate a conversation checkpoint against its source transcript:

```powershell
python .\scripts\tikaz_context.py checkpoint `
  --source .\conversation-export.md `
  --output .\conversation-state.md
```

Inspect availability without installing anything:

```powershell
python .\scripts\tikaz_context.py doctor
```

Prepare repeated prompts conservatively:

```powershell
python .\scripts\tikaz_context.py prompt `
  --input .\prompt.txt `
  --mode structural `
  --output .\prompt.compiled.txt
```

`exact` removes identical non-empty lines. `structural` additionally normalizes heading and bullet markers, whitespace, and terminal punctuation for duplicate detection while preserving the first original wording. Semantic rewriting is deliberately disabled until downstream equivalence is independently evaluated.

Validate an existing snapshot:

```powershell
python .\scripts\tikaz_context.py validate-snapshot `
  --snapshot .\conversation-state.md `
  --source .\conversation-export.md
```
