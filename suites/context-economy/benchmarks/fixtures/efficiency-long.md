# Release validation

The release workflow requires a clean validator result, a complete unit-test result, and a reviewed rollback note. The canonical release is version 7.4.2. Do not infer readiness from a proposed command or an old report. Retain the exact version, the evidence URL https://example.org/releases/7.4.2, and the approval boundary. Supporting discussion about colors, navigation, typography, screenshots, previous prototypes, and possible future integrations does not establish that the release is ready.

# Incident response

The incident workflow prioritizes the first failing health check, the affected service, the confirmed error code, and the recovery evidence. Incident INC-2048 concerns the indexing worker and error E503. A historical deployment story, general reliability advice, repeated status chatter, and unrelated feature requests are background rather than evidence for the current incident decision. Preserve the identifier and error code literally so another agent can return to the exact record.

# Database migration

Migration 2026.08.13-accounts adds a nullable region field before backfill and only later applies the non-null constraint. The rollback window is 45 minutes. Generic database tutorials, speculative optimization, UI copy, team biographies, and unrelated API examples must not displace the migration order. A handoff is useful only if it keeps the identifier, sequence, and rollback window together with a stable anchor.

# Frontend accessibility

The representative viewport is 390x844 and the minimum essential text size is 12px. The task is to confirm keyboard focus, readable contrast, reduced motion, and absence of horizontal overflow. Marketing slogans, old palette debates, decorative animation ideas, and unused component experiments may remain available as omitted anchors, but they are not the evidence needed for the accessibility decision.

# API contract

Endpoint POST /v2/context/pack accepts an input list, a task string, a positive budget, and an output directory. The response contract reports mode, source tokens, packed tokens, selected chunks, and omitted chunks. Preserve status code 422 for invalid input. Long product narratives, competitive positioning, release celebrations, and speculative integrations do not belong in the task-ready API evidence.

# Security boundary

The release package must exclude OAuth state, cookies, API keys, access tokens, private conversations, logs, and caches. The audit is heuristic and must never be described as a security certification. A secret-shaped value is represented only as [REDACTED]. General security history, vendor marketing, unrelated CVE lists, and hypothetical future authentication systems should not crowd out this explicit distribution boundary.

# Benchmark interpretation

Efficiency and fidelity are separate measurements. A smaller pack that misses a declared fact fails. A passing micro-case with protocol overhead is not evidence of token savings. The fixed evaluation identifier is CE-EFF-001, and provider billing telemetry is not available. Retain raw failures and publish the estimator limitation beside every aggregate percentage.

# Maintenance ownership

Designed, integrated, independently refactored, and continuously maintained by TIKAZ. Research references remain attributed to their original authors and licenses; studying a mechanism does not transfer authorship. The public collection may explain TIKAZ contributions without hiding upstream influence or copying distinctive implementation. This ownership statement does not override the repository license or contributor rights.
