<p align="center"><strong>English</strong> · <a href="CONTRIBUTING.zh-CN.md">简体中文</a></p>

# Contributing

Contributions are welcome when they improve behavior, evidence, portability, or maintainability—not merely rename an existing Skill.

## Contribution contract

1. Keep each Skill independently usable and its directory identical to the frontmatter `name`.
2. Use only `name` and `description` in `SKILL.md` frontmatter. Put trigger conditions in the description.
3. Add a concise `TIKAZ Edition` or contributor section that states the contribution type and concrete behavioral changes.
4. Add or update the matching entry in `SOURCES.yml`. Separate bundled upstream content from research references.
5. Do not add third-party files with an unknown license. Preserve copyright and license notices for permitted derived or vendored work.
6. Do not add credentials, cookies, private vault content, absolute user paths, compiled caches, or claims that optional tools are universally available.
7. Keep the core workflow concise; place detailed procedures in directly linked `references/`, deterministic helpers in `scripts/`, and output resources in `assets/`.
8. Include at least three realistic prompts in the suite routing reference when adding a new route.
9. Run `pwsh -File .\scripts\validate_skills.ps1` and report the exact result in the pull request.

## Source modes

- `original`: authored for this repository.
- `clean-room`: independently written after studying a problem or public interfaces; no protected text/code copied.
- `adapter`: original instructions that call or interoperate with a separately installed tool.
- `derived`: contains modifications of licensed upstream material and must retain its notices and compatible license.
- `vendored`: redistributes upstream files substantially unchanged and requires an explicit reason; simple republishing is normally rejected.

## Pull request evidence

Describe what changed and why, list upstream or research sources, state the license basis, show a representative invocation and output, and include validation evidence. Never describe a contribution as original solely because names, wording, ordering, or branding changed.
