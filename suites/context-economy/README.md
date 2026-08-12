# Context Economy for Codex

**Spend context where it matters.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Context Economy turns files and long conversations into bounded, traceable context for Codex. It preserves source anchors, makes omissions visible, audits context health, and tests efficiency claims against fixed public cases.

## Installable workflow

| Skill | Owns |
|---|---|
| `context-economy` | End-to-end routing and completion gate |
| `context-pack` | Canonical ingestion, exact deduplication, anchored selection, and hard-budget output |
| `conversation-checkpoint` | Recoverable conversation-only state |
| `context-audit` | Read-only six-dimension Context Health triage |
| `context-benchmark` | Reproducible efficiency and fidelity measurement |

The default CLI uses only the Python standard library and performs no network calls or model inference. Optional converters remain external and replaceable.

See the reproducible [Context Economy method demonstration](../../examples/context-economy-proof.md), including the failed first result and the regression test that corrected it.

## Quick start

```powershell
python .\scripts\tikaz_context.py pack `
  --input .\notes.md `
  --query 'prepare the release validation context' `
  --budget 800 `
  --output .\.context-economy
```

The output includes canonical Markdown, heading-aware indexes, `ledger.json`, a bounded `packs/current-task.context.md`, and `savings-report.md`.

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
