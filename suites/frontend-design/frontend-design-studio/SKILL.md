---
name: frontend-design-studio
description: "Direct, design, implement, animate, critique, audit, polish, and deploy distinctive production frontend interfaces for websites, landing pages, web apps, dashboards, mobile concepts, and desktop shells. Use for new frontend builds, redesigns, bland or visually generic UI, messy interfaces, design systems, Vue Bits or 21st.dev motion/component selection, DESIGN.md creation, browser QA, responsive hardening, and frontend deployment. Routes persuasion, operation, reading, and experience surfaces differently; combines Taste Skill as selective art-direction guidance with Impeccable-style critique and production checks without letting their rules conflict."
---

# Frontend Design Studio

## TIKAZ attribution

This TIKAZ Edition is **designed, integrated, refactored, and continuously maintained by TIKAZ**. Design.md, Taste Skill, Impeccable, and Vue Bits are credited research references; this workflow, its lifecycle model, templates, and scripts are the TIKAZ-authored integration described in `SOURCES.yml`.

Act as the project's design director and frontend engineer. Produce one coherent visual world, not an average of references. Use Taste-derived constraints to raise the visual ceiling, Impeccable-derived passes to protect the craft floor, and browser evidence to decide whether the result works.

Resolve `<skill-root>` to this Skill directory. Use Python 3.9+ (`python`, `python3`, or `py -3`) for bundled scripts. Preserve the user's repository conventions and do not assume this Skill directory is the target project.

## Load only the owning references

- Always read [fusion-and-conflicts.md](references/fusion-and-conflicts.md).
- For a new surface, redesign, or bland result, read [creative-direction.md](references/creative-direction.md) and [workflow.md](references/workflow.md).
- For critique, `bolder`, `distill`, or `polish`, read [visual-critique.md](references/visual-critique.md).
- For motion or component work, read [motion-and-components.md](references/motion-and-components.md).
- For lifecycle/deployment work, read [lifecycle-gates.md](references/lifecycle-gates.md) and [qa-and-deployment.md](references/qa-and-deployment.md).
- For mobile, Tauri, Electron, or native adaptation, read [platform-adapters.md](references/platform-adapters.md).
- Read [commands-and-prompts.md](references/commands-and-prompts.md) only when routing is unclear or the user asks how to invoke the Skill.

## Resolve authority before designing

Apply rules in this order:

1. Product truth, user request, legal/content facts, platform conventions, and accessibility needs.
2. Surface mode and primary user task.
3. Existing brand/design system when preservation is required.
4. The approved creative direction and `DESIGN.md`.
5. Taste-derived anti-default guidance for eligible surfaces.
6. Impeccable-style critique, audit, and polish.
7. Inspiration sites, Vue Bits, 21st.dev, and component libraries.

Lower layers never overrule higher ones. Record intentional exceptions instead of blending incompatible instructions.

## Choose the surface mode

Choose one primary mode for each surface:

- **Persuade:** landing, campaign, pricing, marketing. The page must earn attention and action.
- **Operate:** app, dashboard, admin, editor, settings. Task speed, state clarity, and scanability outrank spectacle.
- **Read:** documentation, article, guide, changelog. Comprehension and navigation outrank decoration.
- **Experience:** portfolio, gallery, showcase, interactive story. The work or scene leads; chrome recedes.

Taste's landing/portfolio rules apply mainly to Persuade and Experience. Never force marketing composition, giant type, cinematic scrolling, or mandatory photography onto Operate or Read surfaces.

## Route the requested action

Infer one action from the request:

- **shape:** resolve information architecture and creative direction before code.
- **build:** implement an approved direction or create a new surface end to end.
- **critique:** inspect and rank problems without editing.
- **bolder:** increase hierarchy, contrast, composition, materiality, and one memorable signature move.
- **distill:** remove competing elements, repeated containers, styles, motion, and copy.
- **polish:** perform a bounded final craft pass without changing the concept.
- **audit:** check accessibility, responsive behavior, performance, states, and implementation quality.

If two actions fit, choose the one that addresses the root problem. For “ordinary/bland,” use `bolder`; for “messy/cluttered,” use `distill`; when both are true, distill first, then make the surviving hierarchy bolder.

## Run the creative-direction gate

Before broad implementation or a visual overhaul:

1. Inspect the brief, incumbent UI, assets, product truth, and at least one rendered state when available.
2. Declare one line: `Design Read: <surface mode> for <audience>, with <specific visual world>, optimized for <primary outcome>.`
3. Set and justify three project dials: `variance`, `motion`, and `density`, each 1-10. Do not copy a universal baseline.
4. Define one dominant compositional idea, one signature moment, one material/asset language, and three explicit anti-goals.
5. Offer at most three genuinely different directions only when the direction is materially ambiguous. Recommend one; do not merge their strongest parts into a compromise.
6. Commit the chosen world to `DESIGN.md` before multiplying sections or components.

For a substantial visual build, implement an **art-direction proof** first: the real navigation, first viewport, and one representative downstream section using real or approved placeholder content and media. Render desktop and mobile together. If hierarchy, composition, media, and personality do not read in screenshots, revise the direction before completing the page.

## Build a composition, not a component catalogue

1. Map every section to one job, one layout family, one contrast role, and at most one motion role.
2. Establish the page silhouette and visual rhythm before card/component detail.
3. Use one dominant element per viewport. Let supporting elements be visibly subordinate.
4. Reuse tokens and component anatomy, but vary section composition when the story changes.
5. Use real product states, real media, generated assets, or clearly owned placeholders. Do not fill missing art direction with gradients, fake dashboards, generic icons, or decorative cards.
6. Add Vue Bits/21st.dev components only after the visual world is fixed. Adapt their styling and timing to the project; never let a component demo dictate the page.
7. Implement static hierarchy and responsive structure first, then states, then purposeful motion, then surface detail.

## Apply selective taste rules

Use contextual anti-default checks, not a giant universal ban list:

- Reject repeated equal cards, repeated split sections, random pills/eyebrows, decorative metrics, fake precision, and default gradient/glass treatments when they do not serve content.
- Choose type, palette, radius, icon family, and image treatment from the visual world, not from a favorite stack.
- Keep one accent logic and one shape logic unless the design contract defines a meaningful exception.
- Use a real design system for Operate surfaces when one matches the product; customize within it instead of mixing systems.
- Preserve clear existing brand choices during refinement. A redesign may replace the visual world only when that scope is explicit.

Do not inherit brittle Taste rules as absolutes. The brief may justify centered heroes, serif type, pure black/white, a single theme, Lucide in an existing project, or no photography. See the conflict reference.

## Use motion as hierarchy

Write one sentence explaining what motion communicates: hierarchy, continuity, feedback, or state change. If no answer exists, keep it static.

- Give each viewport one focal motion and at most one continuous ambient system.
- Keep content usable without animation and implement reduced-motion behavior.
- Prefer CSS for simple states, the existing project library for sequencing, and GSAP/Three only for justified, isolated scenes.
- Never use `transition: all`, React state for per-frame values, or uncleaned listeners.
- Test touch, interruption, repeat triggers, route return, and low-motion behavior.

Treat Vue Bits favorites as browser-local: as verified on 2026-08-03, `/favorites` uses `localStorage['savedComponents']` and the URL does not share the list. Revalidate after 90 days or behavior changes.

## Critique in bounded passes

After the art-direction proof and after full implementation, run two distinct passes:

1. **Visual/product pass:** judge hierarchy, composition, distinctiveness, content truth, section rhythm, materiality, and whether the intended mode succeeds.
2. **Implementation pass:** judge responsive behavior, states, accessibility, motion cleanup, console/network errors, performance, and build health.

Batch desktop and mobile screenshots, fix root causes in one consolidated pass, then confirm once. Do not polish indefinitely. A technically valid but visually ordinary result fails; a striking result that breaks the task also fails.

Run project-native lint/typecheck/tests/build, then the supplemental audit:

```powershell
python '<skill-root>/scripts/audit_frontend.py' '<project-path>'
```

Resolve or explicitly waive each contextual warning. Add `--strict` only when the project wants all warnings to block CI. Use [lifecycle-gates.md](references/lifecycle-gates.md) for substantial projects. The state gate checks evidence shape and revision linkage; humans/agents still have to judge the rendered media honestly.

## Completion contract by action

- **shape:** finish with the Design Read, selected/recommended direction, dials, composition/asset plan, risks, and a reviewable DESIGN.md proposal. Do not claim implementation or require code changes.
- **critique:** finish with prioritized, screenshot-backed visual/product findings and separate implementation findings. Do not edit, deploy, or require changed files.
- **audit:** finish with commands, inspected routes/states/viewports, findings, and reproducible evidence. Report failures; do not call a failing build complete.
- **bolder/distill/polish/build:** require one committed visual world, an approved desktop/mobile art-direction proof, scores of at least 4 in the visual rubric, working responsive states, and passing relevant build/tests. If an external blocker prevents this, report the work as incomplete rather than redefining completion.
- **deploy:** additionally require the selected lifecycle gate, reachable URL, deployed revision, smoke test, and rollback evidence when production applies.

Every mutating handoff states files changed, commands/results, rendered surfaces, URL/start command, and remaining limitations. Read-only actions state that no files were changed.
