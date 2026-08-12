# Distribution architecture

`TIKAZ-AI-Skills` is the canonical source. Seven focused GitHub repositories are generated from `suites/*`; they are discovery and installation surfaces, not independent forks.

## Rules

- Edit suite content only in the canonical monorepo.
- Define public repository identity, highlights, prompts, and version in `manifest.json`.
- Run `python scripts/export_distribution.py --suite <name> --output <path>` to reproduce a distribution.
- Keep `DISTRIBUTION.yml` in every published repository so a release is traceable to its canonical commit.
- Let each distribution's scheduled workflow pull from the public canonical repository; no personal access token is required.
- Validate all seven generated repositories in canonical CI before publishing changes.

The generated repositories intentionally include the collection-level source and license records. This favors transparent provenance over a smaller but ambiguous package.
