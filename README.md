<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center">
  <img src="assets/tikaz-ai-skills-hero.svg" alt="TIKAZ AI Skills for Codex — seven composable, evidence-first workflows" width="100%" />
</p>

<h1 align="center">TIKAZ AI Skills for Codex</h1>

<p align="center">
  <strong>面向 Codex 的可组合、可验证工作流集合</strong><br />
  Turn one-off prompts into routed workflows with evidence, quality gates, and portable handoffs.
</p>

<p align="center">
  <a href="https://github.com/TIKAZI/TIKAZ-AI-Skills/actions/workflows/validate.yml"><img src="https://github.com/TIKAZI/TIKAZ-AI-Skills/actions/workflows/validate.yml/badge.svg" alt="Validate Skills" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-f4c95d.svg" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/suites-7-60a5fa.svg" alt="7 suites" />
  <img src="https://img.shields.io/badge/skills-30-22d3ee.svg" alt="30 Skills" />
</p>

<p align="center">
  <a href="https://tikazi.github.io/TIKAZ-AI-Skills/">Live documentation</a> ·
  <a href="https://tikazi.github.io/TIKAZ-AI-Skills/#feedback">Feedback form</a> ·
  <a href="#start-in-60-seconds">Quick start</a> ·
  <a href="#the-seven-suite-system">Seven suites</a> ·
  <a href="examples/prompts.md">Prompts</a> ·
  <a href="docs/skills-catalog.md">30-Skill catalog</a> ·
  <a href="SOURCES.yml">Provenance</a> ·
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

## ✨ One collection. Seven workflows. One quality contract.

TIKAZ AI Skills is a monorepo maintained by **TIKAZ** for **Codex and compatible Skill hosts**, with contributions welcome. Seven suites live together because useful work crosses boundaries: Context Economy can prepare the smallest reliable handoff, video evidence can become research, research can become a deck, and an approved interface can move into engineering delivery.

Each suite remains independently installable. The collection supplies the shared rules that keep handoffs coherent:

```text
USER GOAL
   ↓
ONE PRIMARY SUITE  ──→  specialist Skills only when needed
   ↓
STRUCTURED HANDOFF ──→  evidence · uncertainty · source · license
   ↓
QUALITY GATE       ──→  render · test · review · artifact proof
   ↓
VERIFIED DELIVERY
```

This is not an OpenAI-official repository. It is designed, integrated, refactored, and continuously maintained by **TIKAZ** for real Codex workflows.

## 🚀 Start with the flagships

| | Suite | What makes it different |
|---|---|---|
| **01** | **[Frontend Design](suites/frontend-design)** | Classifies the product surface, commits to one visual world, and requires a desktop/mobile art-direction proof before full implementation. |
| **02** | **[Video Intelligence](suites/video-intelligence)** | Never treats metadata, transcript, keyframe, and primary-source verification as equivalent evidence. Produces timestamped, auditable synthesis. |

```text
Use frontend-design to redesign this dashboard. Write the Design Read,
set the three project dials, and approve a desktop/mobile proof first.
```

```text
Use video-platform-reader to compare these videos. Keep timestamps,
label evidence levels, and list every claim that remains unverified.
```

## 🧩 The seven-suite system

| Suite | Skills | Owns | Typical path |
|---|---:|---|---|
| **[Context Economy](suites/context-economy)** | 5 | Efficient, recoverable context | pack → checkpoint → audit → benchmark |
| **[Video Intelligence](suites/video-intelligence)** | 2 | Auditable video learning | sources → transcript/ASR → keyframes → evidence cards → synthesis |
| **[Frontend Design](suites/frontend-design)** | 2 | Distinctive product interfaces | surface → Design Read → proof → implementation → visual QA |
| **[Engineering](suites/engineering)** | 6 | Safe repository delivery | specification → impact map → code → tests → review → release evidence |
| **[Knowledge & Research](suites/knowledge-research)** | 6 | Traceable decisions | question → sources → evidence ledger → disagreement → recommendation |
| **[Presentation](suites/presentation)** | 4 | Verified decks | narrative → one format → page contracts → render QA → artifact |
| **[Visual Content](suites/visual-content)** | 5 | Publishable content assets | thesis → one style → shot card → creation → publishing QA |

There are **30 installable Skills**, including the seven suite orchestrators. Use a suite orchestrator for an end-to-end outcome; install a child Skill when you need only one focused capability.

Browse the generated [30-Skill Catalog](docs/skills-catalog.md). Every entry links to its canonical `SKILL.md` and is checked for an independent trigger, input, output, example, validation, fallback, limitation, TIKAZ contribution, and Codex UI metadata.

### Every Skill, individually installable

Each link below opens that Skill's own executable contract. Install an **orchestrator** for the complete routed workflow, or copy only a **specialist** folder when that focused output is all you need.

| Workflow | Skill | Role | Use it on its own for |
|---|---|---|---|
| Context Economy | [`context-economy`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/context-economy/index.html) | Orchestrator | Automatically route pasted text, files, PDFs, tables, and visuals into the safest compact context path. |
| Context Economy | [`context-pack`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/context-pack/index.html) | Specialist | Build a bounded, traceable context pack from files, folders, code, logs, or structured data. |
| Context Economy | [`conversation-checkpoint`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/conversation-checkpoint/index.html) | Specialist | Turn a long conversation into recoverable decisions, state, evidence, and open questions. |
| Context Economy | [`context-audit`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/context-audit/index.html) | Specialist | Audit relevance, repetition, traceability, safety, cacheability, and recoverability. |
| Context Economy | [`context-benchmark`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/context-benchmark/index.html) | Specialist | Measure savings and fidelity on versioned, reproducible cases. |
| Frontend Design | [`frontend-design`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/frontend-design/index.html) | Orchestrator | Route product art direction, implementation, responsive QA, and engineering handoff. |
| Frontend Design | [`frontend-design-studio`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/frontend-design-studio/index.html) | Specialist | Design, implement, critique, polish, and verify a distinctive production interface. |
| Video Intelligence | [`video-intelligence`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/video-intelligence/index.html) | Orchestrator | Coordinate cross-platform video research with evidence levels and synthesis. |
| Video Intelligence | [`video-platform-reader`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/video-platform-reader/index.html) | Specialist | Read public or local videos with metadata, timestamps, ASR, keyframes, and source cards. |
| Engineering | [`engineering`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/engineering/index.html) | Orchestrator | Own production delivery from specification and impact mapping through release evidence. |
| Engineering | [`code-intelligence`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/code-intelligence/index.html) | Specialist | Map repository structure, semantic relationships, change impact, PR risk, and refactors. |
| Engineering | [`engineering-delivery`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/engineering-delivery/index.html) | Specialist | Implement a scoped software change with tests, review, and release handoff. |
| Engineering | [`skill-security-audit`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/skill-security-audit/index.html) | Specialist | Statically inspect a third-party Skill before installation. |
| Engineering | [`supabase-operations`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/supabase-operations/index.html) | Specialist | Design and operate Supabase schema, migrations, security, backups, and observability. |
| Engineering | [`video-workbench`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/video-workbench/index.html) | Specialist | Engineer a repository-backed media processing workbench from ingestion to deployment. |
| Knowledge & Research | [`knowledge-research`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/knowledge-research/index.html) | Orchestrator | Route sources, research, decisions, personal knowledge, and evidence feedback. |
| Knowledge & Research | [`document-to-markdown`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/document-to-markdown/index.html) | Specialist | Convert documents, webpages, images, and audio to structured, source-aware Markdown. |
| Knowledge & Research | [`academic-research`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/academic-research/index.html) | Specialist | Run literature review, evidence synthesis, research writing, and peer-style critique. |
| Knowledge & Research | [`product-strategy`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/product-strategy/index.html) | Specialist | Work through product discovery, positioning, priorities, GTM, and analytics. |
| Knowledge & Research | [`solo-business-operations`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/solo-business-operations/index.html) | Specialist | Coordinate a one-person business across product, content, finance, operations, and support. |
| Knowledge & Research | [`personal-knowledge-memory`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/personal-knowledge-memory/index.html) | Specialist | Retrieve relevant personal decisions and record only knowledge that changes execution. |
| Presentation | [`presentation`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/presentation/index.html) | Orchestrator | Choose and govern one presentation format from narrative through rendered QA. |
| Presentation | [`html-deck-builder`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/html-deck-builder/index.html) | Specialist | Build a browser-editable, offline-safe HTML deck. |
| Presentation | [`powerpoint-deck-builder`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/powerpoint-deck-builder/index.html) | Specialist | Create and verify a native editable PowerPoint deck. |
| Presentation | [`magazine-web-deck`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/magazine-web-deck/index.html) | Specialist | Create an editorial or Swiss-inspired single-file web presentation. |
| Visual Content | [`visual-content`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/visual-content/index.html) | Orchestrator | Route writing, illustration, logistics diagrams, music, accessibility, and publishing QA. |
| Visual Content | [`concise-writing-editor`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/concise-writing-editor/index.html) | Specialist | Remove AI filler and repetition while preserving meaning and voice. |
| Visual Content | [`xiaohei-article-illustrator`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/xiaohei-article-illustrator/index.html) | Specialist | Art-direct concise hand-drawn Chinese article illustrations with a consistent character. |
| Visual Content | [`zhuge-logistics-illustrator`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/zhuge-logistics-illustrator/index.html) | Specialist | Art-direct source-aware 16:9 Chinese logistics explainers. |
| Visual Content | [`legal-free-music`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/legal-free-music/index.html) | Specialist | Find lawfully downloadable public-domain, CC, or artist-authorized music with license evidence. |

### Install a complete suite separately

The monorepo is the **single source of truth**. Seven focused repositories are automatically generated from it so each suite can be discovered, starred, cloned, and installed on its own without creating eight drifting codebases.

| Standalone distribution | Best entry point |
|---|---|
| [TIKAZ Context Economy for Codex](suites/context-economy) *(canonical preview)* | Hard-budget packs, recoverable checkpoints, context audit, and reproducible benchmarks |
| [TIKAZ Frontend Design for Codex](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) | Interface art direction, implementation, and visual QA |
| [TIKAZ Video Intelligence for Codex](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) | Timestamped video evidence and synthesis |
| [TIKAZ Engineering Workflows for Codex](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) | Repository delivery, impact analysis, review, and operations |
| [TIKAZ Knowledge & Research for Codex](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) | Research, source normalization, decisions, and reusable memory |
| [TIKAZ Presentation Workflows for Codex](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) | HTML, editable PPTX, and editorial web decks |
| [TIKAZ Visual Content for Codex](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content) | Illustration direction, concise writing, and lawful music |

Each distribution records the exact canonical commit in `DISTRIBUTION.yml`, validates independently, and synchronizes weekly or on demand. Cross-suite development and source-of-truth Issues stay in this repository.

## 📦 Start in 60 seconds

### 1. Clone

```bash
git clone https://github.com/TIKAZI/TIKAZ-AI-Skills.git
cd TIKAZ-AI-Skills
```

### 2. Install one Skill

Copy the suite or child folder into the Skill directory supported by your Codex environment. Keep the folder name identical to the `name` in `SKILL.md`.

Project-local example on PowerShell:

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\suites\frontend-design\frontend-design-studio' `
  -Destination '.\.agents\skills\frontend-design-studio'
```

### 3. Invoke it naturally

```text
Use frontend-design-studio to turn this bland landing page into one coherent
visual world. Show the first viewport and one representative section before
expanding the whole page.
```

See [copy-ready prompts](examples/prompts.md) for every suite.

Method demonstrations: [Context Economy fixture](examples/context-economy-proof.md) · [frontend art-direction proof](examples/frontend-design-proof.md) · [video evidence card](examples/video-evidence-card.md)

### Context Economy evidence snapshot

Context Economy is positioned as a **fidelity-first multimodal context compiler**, not a universal “Token compressor.” It converts supported documents into reusable Markdown, preserves facts and source anchors, routes informative visuals and complex tables separately, and exposes uncertain inputs instead of silently flattening them. The checked-in public benchmark separates efficiency from fidelity instead of publishing one composite score:

In practical use, users can paste text or attach files without choosing a pipeline first. Plain text is compacted conservatively; supported documents are converted to Markdown and checked; documents containing images or complex tables split into compact text, visual filtering, bounded vision work, and source fallback; long conversations become recoverable checkpoints.

- long-context profile: **69.7% estimated reduction** (`4,698 → 1,422`, 6 task variants over one synthetic source);
- prompt exact-repeat profile: **14.6% estimated reduction** (`157 → 134`, 4 cases including no-exact-duplicate controls);
- prompt structural-repeat profile: **49.5% estimated reduction** (`95 → 48`, 2 synthetic variants; first wording retained);
- protected facts: **46/46 retained**;
- expected anchors: **39/39 retained**;
- Text / Hybrid / Source routing: **8/8 labeled cases**;
- visual/table filtering: **8/8 labeled cases**;
- short-input profile: **143.9% growth**, retained publicly to show when the protocol is not economical.

The product claim is the workflow and its verification boundary: build the smallest useful context that remains checkable. The percentages above are scoped evidence, not universal promises. Visual routing is measured; vision-description accuracy is still Pending.

See the [generated evidence card](suites/context-economy/benchmarks/results/README.md), [machine-readable metrics](suites/context-economy/benchmarks/results/metrics.json), and [generated-PDF fidelity evidence](suites/context-economy/benchmarks/pdf/results/README.md). Real-world/scanned PDF fidelity, actual provider Token usage, vision accuracy, and downstream blind-answer quality are still marked **Pending**.

## 🔄 Why it is more than a prompt collection

- **One owner per deliverable** — supporting Skills cannot compete for control.
- **Evidence travels with work** — claims retain timestamps, confidence, sources, and unresolved gaps.
- **Visual proof before scale** — frontend, presentation, and illustration workflows verify representative output early.
- **Objective completion gates** — builds, tests, rendered artifacts, and file state outrank agent confidence.
- **Portable by design** — no private drive paths, embedded credentials, or universal claims about optional tools.
- **Auditable provenance** — clean-room work, adapters, references, and removed upstream material are distinguished explicitly.

## 🗂️ Repository map

```text
TIKAZ-AI-Skills/
├─ suites/                    # seven independently installable workflow suites
│  ├─ context-economy/        # context budgeting, selection, packaging, and recovery
│  ├─ frontend-design/        # flagship: art direction + implementation gates
│  ├─ video-intelligence/     # flagship: evidence-based video understanding
│  ├─ engineering/
│  ├─ knowledge-research/
│  ├─ presentation/
│  └─ visual-content/
├─ examples/                  # copy-ready invocation prompts
├─ scripts/                   # repository validation gate
├─ SOURCES.yml                # source mode, license, and TIKAZ contribution
└─ THIRD_PARTY_NOTICES.md     # research acknowledgements and boundaries
```

## ✅ Validation

Every push runs the repository policy gate on GitHub Actions.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File '.\scripts\validate_skills.ps1'
```

It checks all 30 Skills for structure, attribution, source policy, portability, routing, UI metadata, generated files, and Python syntax. A green check proves repository consistency; optional platform access still depends on the user's environment and permissions.

## ⚖️ Authorship, sources, and license

The collection architecture, TIKAZ Edition workflows, routing contracts, lifecycle gates, templates, portability rules, and validation scripts are designed, integrated, refactored, and continuously maintained by **TIKAZ**.

Research references do not transfer authorship. Their URLs, observed licenses, distribution status, and the concrete TIKAZ contribution are recorded in [SOURCES.yml](SOURCES.yml) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

TIKAZ-authored files are released under the [MIT License](LICENSE). Contributions should improve behavior, evidence, portability, or verification—not merely rename an existing Skill. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 🌐 Explore TIKAZ projects

- [⚡ Context Economy](https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy) — fidelity-first multimodal context compilation with reproducible evidence.
- [🎨 Frontend Design](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) — art-directed frontend workflows from visual proof to implementation.
- [🎬 Video Intelligence](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) — evidence-graded cross-platform video reading and synthesis.
- [🛠️ Engineering](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) — specification-to-release engineering delivery.
- [🔬 Knowledge & Research](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) — traceable research, decisions, and knowledge feedback.
- [📽️ Presentation](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) — narrative-first HTML and editable PowerPoint production.
- [🖼️ Visual Content](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content) — illustration, concise writing, lawful music, and publishing QA.
