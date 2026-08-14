# Security and responsible reporting

Do not include API keys, tokens, cookies, private media, personal knowledge-base content, or exploit details in a public Issue.

For ordinary prompt-injection, dependency, permission, portability, or unsafe-command findings, open a [Bug report](https://github.com/TIKAZI/TIKAZ-AI-Skills/issues/new?template=bug_report.yml) with a minimal sanitized reproduction.

For a credential exposure or a vulnerability that should not be public before remediation, use GitHub's private vulnerability reporting when it is available for this repository. If that surface is unavailable, open a public Issue containing only a request for a private reporting channel—do not post the sensitive details.

Static validation and Skill review reduce risk but do not guarantee safety. Install third-party tools with least privilege and verify commands before execution.

## Context Economy security scope

Context Economy accepts untrusted local files, converted documents, webpages,
prompts, and model-facing context. Its trust boundaries, abuse cases, controls,
residual risks, and authorized Codex Security use are documented in
[`suites/context-economy/references/threat-model.md`](suites/context-economy/references/threat-model.md).

The project does not automatically upload user inputs, context packs, diagnostics,
or usage telemetry. Optional converters and the Defuddle adapter remain separate
dependencies and must be reviewed in the environment where they run.
