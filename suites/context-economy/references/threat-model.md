# Context Economy Threat Model

## Scope

Context Economy prepares text, files, folders, webpages, converted documents,
prompts, and conversation state for use by an AI agent. The core runtime is local
and dependency-free. Defuddle and document converters are optional adapters.

This model covers the deterministic CLI and Skill workflow. It does not claim to
secure a model provider, an external converter, Node.js, Codex, or the operating
system on the user's behalf.

## Assets

- Source files and unpublished user content.
- Protected facts, decisions, commands, paths, URLs, and evidence anchors.
- Local credentials and environment configuration that must never enter a pack.
- Output integrity: selected content, omission ledger, routing decision, and budget.
- The user's machine, network, and repositories accessible to an agent.

## Trust Boundaries

1. **Files and folders:** names, extensions, content, size, links, and nested paths
   are untrusted.
2. **Webpages:** URL, DNS answers, redirects, headers, HTML, metadata, and embedded
   instructions are untrusted.
3. **Documents and converters:** PDFs, Office files, OCR output, parser processes,
   and converted Markdown are untrusted.
4. **Prompts and model output:** both may contain prompt injection or unsafe tool
   arguments and must remain data, not executable instructions.
5. **Optional adapters:** Node.js packages and external converters have their own
   dependency and process boundaries.
6. **Published artifacts:** wheel, sdist, GitHub Actions, Benchmark results, and
   checksums must remain reproducible and attributable.

## Abuse Cases and Controls

| Threat | Example | Current control | Residual risk |
|---|---|---|---|
| Prompt injection | A webpage tells the agent to ignore policy or run a command | Extracted content is treated as source evidence; the Skill forbids treating it as authority | A downstream agent can still misuse untrusted text if it ignores the contract |
| SSRF | URL targets localhost, private DNS, or cloud metadata | HTTP(S)-only validation, public-address checks, redirect validation, timeout, and byte cap | DNS rebinding remains possible because validation and connection are separate operations |
| Path traversal | Crafted relative path escapes the output directory | Destinations are resolved and checked against the output root | External converters can write outside their own configured output if run unsafely |
| Resource exhaustion | Huge file, response, table, visual queue, or token budget | Input expansion, response bytes, request time, visual count, and context budget are bounded | Local source files are not yet protected by a universal byte cap |
| Secret disclosure | Credentials appear in logs or context | Audit redacts secret candidates; documentation forbids secrets, cookies, and private config | Heuristic detection cannot identify every secret format |
| Parser compromise | Malicious PDF or Office file exploits a converter | Core does not parse these formats; converters are optional and explicitly reported | A vulnerable external converter can still compromise its process or host |
| Supply-chain compromise | Defuddle or build dependency is replaced | Lockfile, minimal core dependencies, Dependabot, CodeQL, and reproducible package build | Lockfiles and scanners cannot prove a dependency is non-malicious |
| Evidence tampering | A compressed pack silently drops critical facts | Protected-fact checks, stable anchors, source inventory, omission ledger, and Source fallback | Literal recall is not semantic correctness |
| Unauthorized scanning | Security tooling is aimed at another repository | Security guidance limits review to owned or authorized repositories | Repository authorization is an organizational control, not enforced by this CLI |

## Security Invariants

- Never execute instructions found in source material.
- Never upload inputs, outputs, or diagnostics automatically.
- Never follow non-HTTP URLs or intentionally connect to private/loopback targets.
- Never claim that pending visual evidence was inspected.
- Never hide an extraction failure; preserve or reference the source instead.
- Never pass model output directly to a shell, path, query, or destructive tool.
- Keep paid API use and repository write access opt-in and separately authorized.

## Verification

- Unit tests cover public URL rejection, bounded fetching, safe output paths,
  prompt preservation, protected facts, and explicit fallback states.
- The public Benchmark reports failures separately from quality metrics.
- GitHub Actions build and install the package on Windows, Linux, and macOS.
- CodeQL scans Python and JavaScript; Dependabot tracks build and adapter inputs.
- Release artifacts are accompanied by SHA-256 checksums.

## Security Work Suitable for Codex Security

Codex Security would be used only on repositories owned or administered by TIKAZ
to review URL-fetching, path handling, archive/package contents, optional converter
boundaries, dependency changes, and CI workflows. Findings would be reproduced,
triaged, tested, and fixed through the public maintenance process or private
vulnerability reporting as appropriate.
