# Implementation Plan: Context Economy Original Product Redesign

## Overview

Replace the seven-entry prototype with five independently useful public Skills backed by one deterministic Context Engine. Preserve the original branch as the rollback point, implement every new behavior test-first, and do not merge or publish during this plan.

## Architecture decisions

- Keep one Python standard-library CLI so the zero-network path remains portable.
- Expose five Skills: `context-economy`, `context-pack`, `conversation-checkpoint`, `context-audit`, and `context-benchmark`.
- Keep ledger, budget, ranking, fingerprints, tokenization, protected facts, caching, and packaging internal.
- Reuse external document converters only through adapters; never vendor their code or make them mandatory.
- Treat the complete emitted pack as the budgeted unit.
- Measure efficiency and fidelity separately so a smaller but worse result cannot pass.
- Retain source research in `SOURCES.yml` and describe only independently implemented TIKAZ contributions.

## Task 1: Lock the five-Skill structure

**Acceptance criteria:**
- Structure tests require exactly the orchestrator plus four child Skills.
- Retired public Skill folders are rejected.
- Every public Skill has matching `agents/openai.yaml` and TIKAZ maintenance attribution.

**Verification:**
- Run the new structure test and observe RED before changing folders.
- Run `python -B -m unittest tests.test_context_economy_structure -v` after the change.

**Files likely touched:** structure tests, five Skill folders, routing reference.

## Task 2: Implement core ingestion and hard-budget packing

**Acceptance criteria:**
- Accept files and directories containing core text, code, HTML, JSON/JSONL, CSV/TSV, and YAML formats.
- Preserve source files and create deterministic canonical assets, fingerprints, indexes, evidence JSON, context Markdown, and reports.
- The complete context artifact stays within `--budget`, or returns explicit `budget-conflict` with the required minimum.
- Oversized prose may split safely; code fences and protected blocks are not silently split.
- Unchanged inputs reuse content-addressed canonical/index artifacts and report the cache decision.

**Verification:**
- Add failing tests for every input family, directory filters, oversized first chunks, total protocol overhead, cache reuse, and deterministic output.
- Run the focused pack tests after each slice.

**Files likely touched:** CLI, pack tests, output-contract and conversion-adapter references.

## Task 3: Implement recoverable conversation checkpoints

**Acceptance criteria:**
- Produce the required recovery sections and preserve protected facts.
- Detect missing sections, missing facts, and drift between two checkpoints.
- Keep the original transcript unchanged.

**Verification:**
- Add RED tests for checkpoint creation and drift detection.
- Run focused checkpoint tests.

**Files likely touched:** CLI, checkpoint tests, template, checkpoint Skill.

## Task 4: Implement Context Health audit and doctor

**Acceptance criteria:**
- Report relevance, redundancy, traceability, safety, cacheability, and recoverability as explainable component scores.
- Detect exact repetition, conflicting rule candidates, stale-file signals, prompt-like untrusted instructions, secret-shaped content, private absolute paths, weak anchors, and unstable prefixes.
- Never print the full secret candidate; report source anchor and redacted finding.
- `doctor` reports optional converter/tokenizer availability and actionable fixes without installing anything.

**Verification:**
- Add RED tests for each finding class, redaction, score bounds, JSON stability, and no-source-rewrite behavior.
- Run focused audit and doctor tests.

**Files likely touched:** CLI, audit tests, health-contract reference, audit Skill.

## Task 5: Implement reproducible benchmarks

**Acceptance criteria:**
- Consume a versioned manifest of fixed cases and expected protected facts/anchors.
- Report hard-budget compliance, savings, protected-fact recall, anchor correctness, runtime, and determinism per case.
- Support optional externally produced answer scores without claiming built-in semantic equivalence.
- Ship at least 30 small public fixtures across required categories without private data or copied third-party corpora.

**Verification:**
- Add RED tests for manifest validation, aggregation, failure visibility, and deterministic reports.
- Run the public benchmark and retain raw per-case output.

**Files likely touched:** CLI, benchmark tests, fixtures, benchmark-method reference, benchmark Skill.

## Task 6: Integrate collection metadata and distribution

**Acceptance criteria:**
- Root collection and standalone export report seven suites and 30 public Skills.
- Distribution export includes exactly five Context Economy Skills and current canonical commit metadata.
- `SOURCES.yml` records mechanisms studied, bundling status, licenses, and TIKAZ-owned contributions accurately.
- No credentials, OAuth state, logs, caches, private conversations, or machine-specific paths enter the release tree.

**Verification:**
- Run distribution tests, full repository validator, secret/path scans, and preview-package validator.

**Files likely touched:** manifest, exporter, README, SOURCES, notices, changelog, distribution tests.

## Task 7: Replace claims with product proof

**Acceptance criteria:**
- README and site lead with outcome, one-command use, supported formats, privacy boundary, and a reproducible before/after result.
- Show Token saving next to protected-fact and budget-compliance results.
- Mobile exposes product value before the full collection and keeps essential text at 12px or larger.
- No link points to an unmerged or nonexistent standalone repository.

**Verification:**
- Run website structure tests.
- Capture and inspect desktop 1440x900 and mobile 390x844 screenshots.
- Confirm no horizontal overflow and no browser warnings/errors.

**Files likely touched:** README, examples, docs HTML/CSS/JS, hero asset, website tests.

## Final checkpoint

- `python -B -m unittest discover -s tests -v`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1`
- `git diff --check`
- Export and validate the standalone preview package.
- Confirm the worktree is clean after atomic commits.
- Present merge/push/keep choices; do not choose for the user.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Five Skills still overlap | Confusing triggers | Give each one owned outcome and add trigger/structure tests |
| Budget metadata consumes too much space | Weak usefulness at small budgets | Reserve protocol overhead and return `budget-conflict` when necessary |
| Lexical selection misses semantic evidence | Incorrect answers | Publish fidelity separately; do not claim semantic equivalence; leave semantic retrieval optional |
| Secret scanner reports sensitive text | Privacy leak | Redact values and test that full candidates never appear |
| Optional converters make support misleading | Trust loss | Doctor reports availability; unsupported adapters fail visibly |
| Benchmark becomes marketing-only | Misleading claims | Publish raw per-case failures and fixed aggregation rules |

## Open questions

None blocking. Optional dependencies remain opt-in and cannot be introduced without separate approval.
