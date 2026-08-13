<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><img src="assets/workflow.svg" alt="TIKAZ Presentation Workflows for Codex workflow" width="100%" /></p>

# TIKAZ Presentation Workflows for Codex

**Narrative-first HTML, PPTX, and editorial web decks with page contracts and rendered QA.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

This suite can be installed as one routed workflow, while every child Skill can also be installed and invoked on its own. It is an independent community project for Codex-compatible Skill hosts, not an OpenAI-official repository.

## ✨ What makes it different

- Choose exactly one output builder for each final deck.
- Every slide receives a claim, evidence, visual job, and speaker intent.
- Rendered overflow, media licensing, and final artifact integrity are completion gates.

## 🧩 Skills you can use independently

| Skill | Role | Core promise |
|---|---|---|
| [`presentation`](SKILL.md) | Orchestrator | Route and govern presentation creation across browser-editable HTML decks, native editable PowerPoint, and magazine-style web decks. |
| [`html-deck-builder`](html-deck-builder/SKILL.md) | Specialist | Plan and build browser-editable HTML presentations with narrative contracts, responsive slide layouts, keyboard navigation, offline-safe assets, and render verification. |
| [`powerpoint-deck-builder`](powerpoint-deck-builder/SKILL.md) | Specialist | Plan, create, revise, and verify native editable PowerPoint presentations with source-aware content, reusable layouts, speaker notes, and rendered visual QA. |
| [`magazine-web-deck`](magazine-web-deck/SKILL.md) | Specialist | Create editorial or Swiss-inspired single-file web presentations with strong typographic hierarchy, horizontal navigation, responsive composition, and restrained motion. |

The root orchestrator owns end-to-end routing. A specialist owns only the output named in its `SKILL.md`; it does not need the orchestrator to be installed.

## 🚀 Try it

```text
Choose HTML or PPTX for this talk, write page contracts, and render representative pages before completing the deck.
```

```text
Create an editable PowerPoint from this brief and inspect every dense slide for overflow and collisions.
```

```text
Turn this essay into a single-file editorial web deck with restrained motion and offline verification.
```

## 📦 Install the suite or one Skill

Copy this suite folder for the complete workflow, or copy one child folder into the Skill directory supported by your Codex host. Keep the destination folder identical to the `name` in `SKILL.md`.

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\suites\presentation' `
  -Destination '.\.agents\skills\presentation'
```

## 🔄 Workflow and output contract

Read [routing](references/routing.md) for owner selection and [output contract](references/output-contract.md) for the verified handoff. The diagram above is editable SVG generated from canonical Skill metadata under the shared [TIKAZ visual system](../../docs/visual-system.md).

## ⚠️ Limitations

- A generated file is not visually approved until rendered and inspected.
- HTML, PPTX, and editorial web decks have different editability and compatibility boundaries.
- External media, fonts, templates, and builder licenses remain authoritative.

## ⚖️ Provenance

Source modes, upstream licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](../../SOURCES.yml) and [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md). TIKAZ authorship applies to original architecture, integration, refactoring, routing, and maintenance; it does not erase third-party ownership.

## 🌐 Explore the TIKAZ workflow family

[🏠 AI Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills) · [⚡ Context Economy](https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy) · [🎨 Frontend Design](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) · [🎬 Video Intelligence](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) · [🛠️ Engineering](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) · [🔬 Research](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) · [📽️ Presentation](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) · [🖼️ Visual Content](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content)
