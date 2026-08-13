<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><img src="assets/workflow.svg" alt="TIKAZ Knowledge & Research for Codex workflow" width="100%" /></p>

# TIKAZ Knowledge & Research for Codex

**Traceable research and decisions with evidence ledgers, disagreement, confidence, and knowledge feedback.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

This suite can be installed as one routed workflow, while every child Skill can also be installed and invoked on its own. It is an independent community project for Codex-compatible Skill hosts, not an OpenAI-official repository.

## ✨ What makes it different

- Question and evidence threshold are fixed before synthesis.
- Conversion, retrieval, evidence, inference, and recommendation remain distinct.
- Personal knowledge is adopted only when it changes execution.

## 🧩 Skills you can use independently

| Skill | Role | Core promise |
|---|---|---|
| [`knowledge-research`](SKILL.md) | Orchestrator | Orchestrate source ingestion, academic research, product decisions, personal knowledge retrieval, and evidence-backed memory feedback. |
| [`document-to-markdown`](document-to-markdown/SKILL.md) | Specialist | Convert PDF, Office, HTML, images, and audio into structured Markdown while preserving headings, tables, links, and provenance where possible. |
| [`academic-research`](academic-research/SKILL.md) | Specialist | Plan literature reviews, search and evaluate sources, synthesize evidence, draft research writing, and perform peer-review-style critique. |
| [`product-strategy`](product-strategy/SKILL.md) | Specialist | Support product discovery, market research, positioning, prioritization, execution planning, go-to-market, and product analytics. |
| [`solo-business-operations`](solo-business-operations/SKILL.md) | Specialist | Plan and operate a one-person business across product, content, finance, operations, legal coordination, customer support, and engineering. |
| [`personal-knowledge-memory`](personal-knowledge-memory/SKILL.md) | Specialist | Retrieve relevant personal project decisions, playbooks, knowledge, skills, and verified outcomes before important work, then record only knowledge that materially affec… |

The root orchestrator owns end-to-end routing. A specialist owns only the output named in its `SKILL.md`; it does not need the orchestrator to be installed.

## 🚀 Try it

```text
Compare these papers with inclusion criteria, contrary evidence, confidence, and claims that need revalidation.
```

```text
Convert this document to Markdown, inspect fidelity, then extract decision-ready claims without inventing citations.
```

```text
Retrieve relevant personal project decisions and record only knowledge that materially changes the plan.
```

## 📦 Install the suite or one Skill

Copy this suite folder for the complete workflow, or copy one child folder into the Skill directory supported by your Codex host. Keep the destination folder identical to the `name` in `SKILL.md`.

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\suites\knowledge-research' `
  -Destination '.\.agents\skills\knowledge-research'
```

## 🔄 Workflow and output contract

Read [routing](references/routing.md) for owner selection and [output contract](references/output-contract.md) for the verified handoff. The diagram above is editable SVG generated from canonical Skill metadata under the shared [TIKAZ visual system](../../docs/visual-system.md).

## ⚠️ Limitations

- Conversion is not verification and retrieval is not adoption.
- Source dates, disagreement, confidence, and revalidation needs remain visible.
- Financial, legal, medical, or safety-critical conclusions require appropriate professional review.

## ⚖️ Provenance

Source modes, upstream licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](../../SOURCES.yml) and [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md). TIKAZ authorship applies to original architecture, integration, refactoring, routing, and maintenance; it does not erase third-party ownership.

## 🌐 Explore the TIKAZ workflow family

[🏠 AI Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills) · [⚡ Context Economy](https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy) · [🎨 Frontend Design](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) · [🎬 Video Intelligence](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) · [🛠️ Engineering](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) · [🔬 Research](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) · [📽️ Presentation](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) · [🖼️ Visual Content](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content)
