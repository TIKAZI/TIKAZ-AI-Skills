<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><img src="assets/workflow.svg" alt="TIKAZ Frontend Design for Codex workflow" width="100%" /></p>

# TIKAZ Frontend Design for Codex

**Art-directed frontend workflows that prove the visual direction before scaling implementation.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

This suite can be installed as one routed workflow, while every child Skill can also be installed and invoked on its own. It is an independent community project for Codex-compatible Skill hosts, not an OpenAI-official repository.

## ✨ What makes it different

- Four product-surface modes instead of one landing-page aesthetic.
- Design Read and three project dials before implementation.
- Revision-bound desktop/mobile proof and engineering QA.

## 🧩 Skills you can use independently

| Skill | Role | Core promise |
|---|---|---|
| [`frontend-design`](SKILL.md) | Orchestrator | Orchestrate product-aware frontend art direction, implementation, responsive QA, code impact analysis, and engineering handoff. |
| [`frontend-design-studio`](frontend-design-studio/SKILL.md) | Specialist | Direct, design, implement, animate, critique, audit, polish, and deploy distinctive production frontend interfaces for websites, landing pages, web apps, dashboards, mob… |

The root orchestrator owns end-to-end routing. A specialist owns only the output named in its `SKILL.md`; it does not need the orchestrator to be installed.

## 🚀 Try it

```text
Redesign this dashboard. Classify the surface and approve a desktop/mobile art-direction proof before expanding the full product.
```

```text
Audit this interface for generic visual patterns, then distill it without turning it into a marketing page.
```

```text
Create a DESIGN.md for this app, implement the representative viewport, and verify responsive and reduced-motion states.
```

## 📦 Install the suite or one Skill

Copy this suite folder for the complete workflow, or copy one child folder into the Skill directory supported by your Codex host. Keep the destination folder identical to the `name` in `SKILL.md`.

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\suites\frontend-design' `
  -Destination '.\.agents\skills\frontend-design'
```

## 🔄 Workflow and output contract

Read [routing](references/routing.md) for owner selection and [output contract](references/output-contract.md) for the verified handoff. The diagram above is editable SVG generated from canonical Skill metadata under the shared [TIKAZ visual system](../../docs/visual-system.md).

## ⚠️ Limitations

- Design approval is not runtime verification.
- Optional component libraries and browser tools must be detected before use.
- Existing routes, analytics, accessibility, and legal copy are preserved unless the user authorizes change.

## ⚖️ Provenance

Source modes, upstream licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](../../SOURCES.yml) and [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md). TIKAZ authorship applies to original architecture, integration, refactoring, routing, and maintenance; it does not erase third-party ownership.

## 🌐 Explore the TIKAZ workflow family

[🏠 AI Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills) · [⚡ Context Economy](https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy) · [🎨 Frontend Design](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) · [🎬 Video Intelligence](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) · [🛠️ Engineering](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) · [🔬 Research](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) · [📽️ Presentation](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) · [🖼️ Visual Content](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content)
