<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><img src="assets/workflow.svg" alt="TIKAZ Video Intelligence for Codex workflow" width="100%" /></p>

# TIKAZ Video Intelligence for Codex

**Evidence-graded video reading with timestamps, keyframes, source cards, and cross-video synthesis.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

This suite can be installed as one routed workflow, while every child Skill can also be installed and invoked on its own. It is an independent community project for Codex-compatible Skill hosts, not an OpenAI-official repository.

## ✨ What makes it different

- Five evidence levels from metadata to primary-source verification.
- Transcript, visual observation, external verification, and inference stay separate.
- Partial failures remain visible in the source ledger.

## 🧩 Skills you can use independently

| Skill | Role | Core promise |
|---|---|---|
| [`video-intelligence`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/video-intelligence/index.html) | Orchestrator | Orchestrate evidence-based video research across platforms, transcripts, Whisper fallback, keyframes, source verification, and cross-video synthesis. |
| [`video-platform-reader`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/video-platform-reader/index.html) | Specialist | Read one or many public-platform or local videos through a portable evidence workflow using available metadata, subtitles, timestamped speech recognition, keyframes, and… |

The root orchestrator owns end-to-end routing. A specialist owns only the output named in its `SKILL.md`; it does not need the orchestrator to be installed.

## 🚀 Try it

```text
Compare these videos with timestamps and label the evidence level behind every important claim.
```

```text
Read this local lecture, inspect keyframes where the transcript is insufficient, and produce an auditable source card.
```

```text
Synthesize these tutorials, show disagreements and missing dependencies, then recommend a workflow with confidence levels.
```

## 📦 Install the suite or one Skill

Copy this suite folder for the complete workflow, or copy one child folder into the Skill directory supported by your Codex host. Keep the destination folder identical to the `name` in `SKILL.md`.

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\suites\video-intelligence' `
  -Destination '.\.agents\skills\video-intelligence'
```

## 🔄 Workflow and output contract

Read [routing](references/routing.md) for owner selection and [output contract](references/output-contract.md) for the verified handoff. The diagram above is editable SVG generated from canonical Skill metadata under the shared [TIKAZ visual system](../../docs/visual-system.md).

## ⚠️ Limitations

- Platform access, subtitles, downloads, and visual inspection depend on the current environment.
- Metadata and search snippets are not watched content.
- Private, paid, DRM-protected, deleted, or inaccessible media remains unresolved rather than bypassed.

## ⚖️ Provenance

Source modes, upstream licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](../../SOURCES.yml) and [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md). TIKAZ authorship applies to original architecture, integration, refactoring, routing, and maintenance; it does not erase third-party ownership.

## 🌐 Explore the TIKAZ workflow family

[🏠 AI Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills) · [⚡ Context Economy](https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy) · [🎨 Frontend Design](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) · [🎬 Video Intelligence](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) · [🛠️ Engineering](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) · [🔬 Research](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) · [📽️ Presentation](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) · [🖼️ Visual Content](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content)
