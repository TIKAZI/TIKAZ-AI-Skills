<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><img src="assets/workflow.svg" alt="TIKAZ Engineering Workflows for Codex workflow" width="100%" /></p>

# TIKAZ Engineering Workflows for Codex

**Production delivery from specification and impact mapping to tests, review, and release evidence.**

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

This suite can be installed as one routed workflow, while every child Skill can also be installed and invoked on its own. It is an independent community project for Codex-compatible Skill hosts, not an OpenAI-official repository.

## ✨ What makes it different

- One lifecycle owner from acceptance criteria to handoff.
- Unified clean-room code intelligence for architecture and impact.
- Security, Supabase, and video-workbench adapters route without expanding scope.

## 🧩 Skills you can use independently

| Skill | Role | Core promise |
|---|---|---|
| [`engineering`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/engineering/index.html) | Orchestrator | Orchestrate production software delivery through specification, repository intelligence, implementation, testing, security review, data operations, and release evidence. |
| [`code-intelligence`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/code-intelligence/index.html) | Specialist | Understand repositories as systems: map code structure and semantic relationships, analyze change impact, review pull requests, and plan safe refactors. |
| [`engineering-delivery`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/engineering-delivery/index.html) | Specialist | Run production software work from specification through planning, implementation, testing, review, and release. |
| [`skill-security-audit`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/skill-security-audit/index.html) | Specialist | Statically inspect third-party agent skills before installation for prompt injection, destructive commands, credential access, dependency risk, hidden network behavior,… |
| [`supabase-operations`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/supabase-operations/index.html) | Specialist | Design, deploy, and operate Supabase projects with explicit schema, migration, security, backup, and observability checks. |
| [`video-workbench`](https://tikazi.github.io/TIKAZ-AI-Skills/skills/video-workbench/index.html) | Specialist | Engineer repository-backed media processing workbenches across ingestion, job state, processing, review, export, frontend states, QA evidence, and deployment configurati… |

The root orchestrator owns end-to-end routing. A specialist owns only the output named in its `SKILL.md`; it does not need the orchestrator to be installed.

## 🚀 Try it

```text
Map the impact of this API change, implement it in small slices, and provide test and rollback evidence.
```

```text
Review this unfamiliar repository and produce an architecture map before proposing a cross-file refactor.
```

```text
Audit this third-party Skill for credential, permission, dependency, and prompt-injection risks before installation.
```

## 📦 Install the suite or one Skill

Copy this suite folder for the complete workflow, or copy one child folder into the Skill directory supported by your Codex host. Keep the destination folder identical to the `name` in `SKILL.md`.

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\suites\engineering' `
  -Destination '.\.agents\skills\engineering'
```

## 🔄 Workflow and output contract

Read [routing](references/routing.md) for owner selection and [output contract](references/output-contract.md) for the verified handoff. The diagram above is editable SVG generated from canonical Skill metadata under the shared [TIKAZ visual system](../../docs/visual-system.md).

## ⚠️ Limitations

- Repository instructions and native tests outrank generic playbooks.
- Security review reduces risk but cannot guarantee safety.
- Production deployment, migrations, and destructive actions require explicit scope and rollback evidence.

## ⚖️ Provenance

Source modes, upstream licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](../../SOURCES.yml) and [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md). TIKAZ authorship applies to original architecture, integration, refactoring, routing, and maintenance; it does not erase third-party ownership.

## 🌐 Explore the TIKAZ workflow family

[🏠 AI Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills) · [⚡ Context Economy](https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy) · [🎨 Frontend Design](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) · [🎬 Video Intelligence](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) · [🛠️ Engineering](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) · [🔬 Research](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) · [📽️ Presentation](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) · [🖼️ Visual Content](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content)
