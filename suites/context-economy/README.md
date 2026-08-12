# Context Economy for Codex

**Spend context where it matters.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

Context Economy converts files and conversations into lean, traceable, task-ready context packs. It measures whether preparation is worthwhile, preserves evidence anchors, and refuses compression when the expected saving or information safety is weak.

## Installable workflow

| Skill | Owns |
|---|---|
| `context-economy` | End-to-end routing and completion gate |
| `content-intake` | Canonical Markdown conversion and fidelity checks |
| `context-ledger` | Fingerprinting, indexing, and exact deduplication |
| `context-budget` | Pass-through/select/compact/cache-stable decision |
| `relevance-gate` | Task-aware exact excerpt selection |
| `context-packager` | Portable bounded context pack |
| `conversation-checkpoint` | Recoverable conversation-only state |

The default CLI uses only the Python standard library and performs no network calls or model inference. Optional converters remain external and replaceable.

See the reproducible [Context Economy method demonstration](../../examples/context-economy-proof.md), including the failed first result and the regression test that corrected it.

## Quick start

```powershell
python .\scripts\context_economy.py pack `
  --input .\notes.md `
  --query 'prepare the release validation context' `
  --budget 800 `
  --output .\.context-economy
```

The output includes canonical Markdown, heading-aware indexes, `ledger.json`, a bounded `packs/current-task.context.md`, and `savings-report.md`.

Validate a conversation checkpoint against its source transcript:

```powershell
python .\scripts\context_economy.py validate-snapshot `
  --snapshot .\conversation-state.md `
  --source .\conversation-export.md
```
