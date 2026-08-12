---
project: {{PROJECT_NAME}}
status: draft
version: 1
release: unreleased
---

# Acceptance traceability

| Requirement | Surface or state | Verification method | Evidence | Result |
|---|---|---|---|---|

# Automated checks

Record exact lint, typecheck, test, audit, and production-build commands with timestamps and results.

# Rendered evidence

Record route, viewport, browser, state, screenshot or recording path, console result, keyboard, touch, and reduced-motion result.

Record desktop and mobile media paths separately and identify the exact implementation revision they show. Text notes are supporting evidence, not substitutes for rendered media.

# Visual/product scorecard

| Dimension | Score 1-5 | Screenshot evidence | Finding or rationale |
|---|---:|---|---|
| Mode success | | | |
| Focal hierarchy | | | |
| Composition and rhythm | | | |
| Contextual distinctiveness | | | |
| Visual coherence | | | |
| Content and media | | | |
| Responsive art direction | | | |
| Interaction craft | | | |

Any score below 3 blocks delivery. All dimensions must reach at least 4 before the final technical gate. Scores must cite visible evidence and are diagnostic judgments, not objective measurements.

# Art-direction proof gate

Record the first-viewport and representative-section desktop/mobile screenshots, the dominant composition, signature moment, identified visual blockers, consolidated fix, and approval to expand the full surface.

# Defects and regression

| Severity | Defect | Root cause | Fix | Regression scope | Status |
|---|---|---|---|---|---|

Blocker or major defects prevent preview approval and production release. If one defect reproduces twice after fixes, stop patching symptoms and escalate root-cause diagnosis. If the third attempt fails, mark the task blocked with evidence. Restore the latest passing checkpoint when a fix introduces regression.

# Preview approval

Record preview URL, deployed revision, content/design/function/license sign-off, approver, timestamp, approval evidence path, and remaining minor defects.

# Production release

Record provider project and environment, production URL, revision/build ID, deployment timestamp, configuration difference summary, previous stable release, rollback command, and rollback verification.

# Post-deploy smoke test

Check status and assets, hard refresh and deep links, 404, CTA/form end to end, TLS, cache behavior, SEO/OG, robots/sitemap when applicable, logs, console, desktop, and mobile.

# Observation and learning

Record observation window, monitoring owner, errors or user feedback, acceptance outcome, differences from `DESIGN.md`, reusable evidence-backed lessons, and what must not be generalized.

Set frontmatter `status: passed` only when the art-direction proof was approved, every visual score is at least 4, build and acceptance traceability pass, desktop/mobile rendering and interactions are evidenced, and blocker/major defects are zero.
