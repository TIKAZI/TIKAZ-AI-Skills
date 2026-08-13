# Implementation Plan: Context Economy v0.6 Multimodal Compiler

## Phase 1: Behavioral contract

- Add failing tests for informative/decorative/duplicate image routing and table fidelity flags.
- Add failing tests for profile and cost-ledger CLI artifacts.

## Phase 2: Standard-library compiler

- Add deterministic document profiling and conservative PDF metadata inspection.
- Add `text` / `hybrid` / `source` routing.
- Add a bounded visual-evidence queue and safe pending status.
- Expand `pack` with prompt and visual budgets while preserving existing defaults.

## Phase 3: Skill workflow and distribution

- Update the suite and context-pack instructions for host vision handling.
- Update routing, output contract, conversion adapters, examples, README, version, and distribution metadata.
- Export the standalone context-economy distribution.

## Phase 4: Verification

- Run focused tests, full test discovery, all-skill validation, standalone validation, and a sensitive-path scan.
- Record observed metrics only; leave cross-project superiority unclaimed until matched A/B and downstream blind tests exist.

