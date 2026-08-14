# Implementation Plan: Context Economy Productization

## Architecture Decisions

- Develop in the monorepo and export the focused repository deterministically.
- Package the existing implementation rather than duplicate its logic.
- Keep `scripts/tikaz_context.py` as a compatibility wrapper.
- Use GitHub installation first; registry publication remains a separate decision.
- Record provenance and maintainership without altering public history.

## Phase 1: Identity and Contracts

- [ ] Configure the canonical and local distribution repositories with the correct
      TIKAZ GitHub noreply identity.
- [ ] Add `.mailmap` and `MAINTAINERS.md` without changing old commits.
- [ ] Add tests for exported maintainer and package files.

Checkpoint: repository status is understood and new commits resolve to `TIKAZI`.

## Phase 2: Installable Core

- [ ] Add package metadata and an importable package with a console entry point.
- [ ] Preserve the existing script path through a thin compatibility wrapper.
- [ ] Add version and installed-resource discovery behavior.
- [ ] Add clean-environment CLI installation and smoke tests.

Checkpoint: a locally built wheel installs and runs without repository-relative
imports or mandatory third-party dependencies.

## Phase 3: Security and Automation

- [ ] Add a Context Economy threat model and expand responsible reporting guidance.
- [ ] Add dependency updates, CodeQL, package build, and cross-platform CLI checks.
- [ ] Generate checksums and build artifacts without publishing registry packages.

Checkpoint: local tests and GitHub Actions cover build, security, and installed use.

## Phase 4: Documentation and Evidence

- [ ] Replace clone-and-copy-only instructions with package and Skill installation.
- [ ] Add a one-minute bilingual quickstart and representative input/output contract.
- [ ] Add an adoption/showcase route that accepts verifiable community submissions.
- [ ] State measured, pending, and unavailable evidence separately.

Checkpoint: a new user can install, run, inspect, and report a result from the README.

## Phase 5: Distribution and Release

- [ ] Export and validate the Context Economy distribution.
- [ ] Commit and push atomic canonical changes.
- [ ] Synchronize the independent repository and publish a versioned GitHub release.
- [ ] Verify all Actions and public repository pages.

Checkpoint: canonical and independent repositories agree on version and content.

## Phase 6: Application

- [ ] Refresh public repository metrics after release.
- [ ] Populate the official Codex for Open Source form with factual project,
      maintainer, API-credit, and security-use descriptions.
- [ ] Stop before the final Submit action for user review.

## Rollback

- Revert product commits normally; no force push is required.
- Keep the previous GitHub Release available until the new release is verified.
- If package installation fails, retain the existing direct script invocation and
  Skill-folder installation paths as supported fallbacks.

