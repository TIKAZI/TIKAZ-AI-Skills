# Context Economy for Codex

**Spend context where it matters.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Context Economy turns files and long conversations into bounded, traceable context for Codex. Its multimodal compiler keeps text in reusable Markdown, routes only informative figures or complex tables to a visual-evidence queue, preserves source anchors, and measures the full input cost chain without confusing bytes with tokens.

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

Validate an existing snapshot:

```powershell
python .\scripts\tikaz_context.py validate-snapshot `
  --snapshot .\conversation-state.md `
  --source .\conversation-export.md
```
