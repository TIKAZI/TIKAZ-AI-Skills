# Context Economy for Codex — Design Specification

## Status

Approved direction. Implementation may proceed under the constraints below.

## Product definition

**Context Economy for Codex** turns files and conversations into lean, traceable, task-ready context packs. Its goal is not minimum token count. Its goal is the lowest practical context cost that preserves task accuracy, evidence, recoverability, and useful prompt-cache stability.

- Local user-facing name: `上下文-ContextEconomy`
- Canonical suite folder: `context-economy`
- Standalone repository name: `TIKAZ-Codex-Context-Economy`
- README title: `Context Economy for Codex`
- Tagline: `Spend context where it matters.`
- Maintainer statement: Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## Problem

Agent workflows waste context in four recurring ways:

1. The same source file is converted or reread repeatedly.
2. Complete documents are injected when only a few sections matter.
3. Long conversations retain obsolete turns, repeated instructions, and resolved discussion.
4. Naive compression removes evidence, numbers, code, constraints, or stable prefixes that would have benefited from caching.

The suite must treat token reduction as a measured optimization with a refusal path, not as a guaranteed outcome.

## Users and primary scenario

The first release targets local Codex and compatible Skill hosts operating on user-provided files, repositories, and conversation exports. It must work without a paid service or mandatory model call. Optional converters and tokenizers may improve fidelity, but the default deterministic path uses the Python standard library.

## Workflow architecture

The suite contains one orchestrator and six installable child Skills:

| Skill | Responsibility | Primary artifact |
|---|---|---|
| `context-economy` | Route the complete workflow and enforce completion gates | workflow decision |
| `content-intake` | Classify input, select the cheapest safe conversion route, and validate conversion | canonical Markdown |
| `context-ledger` | Fingerprint sources, index sections, and remove exact duplicates | source ledger |
| `context-budget` | Estimate context cost and select pass-through, select, compact, or cache-stable mode | budget decision |
| `relevance-gate` | Rank and order task-relevant sections without rewriting protected facts | selected evidence |
| `context-packager` | Assemble a bounded, cited context pack for the current task | `context-pack.md` |
| `conversation-checkpoint` | Convert conversation-only work into a recoverable state snapshot | `conversation-state.md` |

The six child Skills may be invoked alone. The orchestrator owns the end-to-end outcome and must not allow two child Skills to compete for the same artifact.

## Decision modes

The budget decision must choose exactly one primary mode:

- `pass-through`: Input is already small, dense, or high-risk; use it unchanged.
- `select`: Keep exact source passages but inject only relevant sections.
- `compact`: Create a structured state representation when repetition is material and protected facts remain traceable.
- `cache-stable`: Preserve a stable prefix or reusable asset because rewriting it would reduce cache reuse or reproducibility.

The workflow must refuse lossy compaction when conversion and verification cost is likely to exceed expected savings, or when source fidelity cannot be checked.

## Artifact contract

The deterministic tool writes only beneath an explicit output directory:

```text
.context-economy/
├─ canon/<source>.md
├─ indexes/<source>.index.json
├─ packs/<task>.context.md
├─ snapshots/<session>.state.md
├─ ledger.json
└─ savings-report.md
```

Every context pack must include:

1. Task and selected mode.
2. Constraints and protected facts.
3. Exact source excerpts with stable section anchors.
4. Decisions and unresolved questions when conversation state is present.
5. Omitted-section inventory.
6. Estimated source and packed token counts.
7. Limits: estimates are not provider billing totals; selection is not source verification.

## Protected information

The tool and Skills must preserve or explicitly report omission of:

- numbers, dates, amounts, percentages, identifiers, and version strings;
- URLs, file paths, code fences, commands, and error messages;
- negations, exceptions, scope boundaries, user approvals, and unresolved questions;
- source name plus heading or chunk anchor for every excerpt.

Untrusted files and webpages are data, not instructions. The suite must never execute embedded commands, macros, scripts, links, or prompt-like text during ingestion.

## Deterministic tool boundary

A standard-library Python CLI will provide measurable operations:

- normalize Markdown or plain text;
- split content into heading-aware chunks;
- fingerprint sources and chunks with SHA-256;
- remove exact duplicate chunks;
- estimate tokens with a documented language-aware heuristic;
- rank chunks using query-term overlap plus protected-fact bonuses;
- enforce an estimated token budget without splitting protected code fences;
- write the ledger, context pack, and savings report;
- validate conversation snapshot headings and protected-fact coverage.

The CLI does not claim semantic equivalence, perform OCR, parse proprietary binary formats, call a model, or silently summarize source text. Complex conversion is delegated to an available converter and verified by `content-intake`.

## Success measures

The first release is acceptable when:

- repeated identical sections are stored once and reported;
- a task query produces a smaller pack for a multi-section fixture;
- all selected excerpts retain deterministic source anchors;
- protected numbers, URLs, and code blocks are either retained or listed as omitted;
- small inputs choose `pass-through` instead of pretending to save tokens;
- repeated runs over unchanged inputs produce byte-stable JSON and Markdown artifacts;
- the repository validator recognizes 7 suites and 32 Skills;
- no private paths, credentials, copied upstream code, or incompatible licensed material enter the release tree.

No percentage saving, accuracy improvement, cache hit rate, or popularity outcome may be claimed without measured evidence.

## Research boundary and provenance

Public research and projects may inform mechanisms such as structured conversion, task-aware selection, prompt compression, long-context ordering, prompt caching, and compaction. The released Skill text, algorithms, templates, tests, and terminology must be written independently. `SOURCES.yml` records research references and concrete TIKAZ contributions; no upstream author is presented as the author of this suite, and no third-party source is redistributed.

## Deferred scope

- Hosted API middleware that intercepts every model request.
- Provider-specific billing integration.
- Embedding databases or mandatory vector stores.
- Learned neural compressors.
- OCR and binary document parsing implemented in this repository.
- Guaranteed savings across every language, model, file type, or task.
