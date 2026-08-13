---
name: engineering-delivery
description: Run production software work from specification through planning, implementation, testing, review, and release. Use for substantial repository changes that require explicit acceptance criteria and verification evidence.
---

# Engineering Delivery

This TIKAZ Edition is designed, integrated, refactored, and continuously maintained by **TIKAZ**. External engineering playbooks are research references, not redistributed content.

## Inputs

Accept a repository and an authorized change request with constraints, acceptance criteria, and release boundary. Inspect local repository instructions and current worktree state before changing files.

## Workflow

1. Read repository instructions, architecture, scripts, and current worktree state.
2. Convert the request into scope, constraints, acceptance criteria, and non-goals.
3. Plan small implementation slices and identify risky dependencies.
4. Implement in the repository's established style.
5. Run focused tests, then broader lint, type checks, build, and security checks in proportion to risk.
6. Review the final diff for regressions, unnecessary changes, secrets, and missing documentation.
7. Report completed work, verification evidence, viewing instructions, and remaining risks.

## Output contract

Return the implemented diff, acceptance-criteria mapping, commands and results, viewing instructions, rollback or release note, and unresolved risk. Preserve unrelated user changes.

## Validation and fallback

Do not claim success from agent confidence alone. Require user confirmation or objective file, test, build, or runtime evidence. If a required environment, credential, or production authority is missing, deliver the verified local state and name the blocker; do not simulate deployment.

## Example and limits

```text
Use engineering-delivery to implement this confirmed feature in small slices, run repository-native checks, and report the exact verification evidence.
```

This Skill does not expand scope, authorize destructive operations, or substitute generic checks for repository-native validation.
