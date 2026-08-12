---
name: {{PRODUCT_NAME}}
status: draft
version: 1
surface: {{SURFACE}}
platform: {{PLATFORM}}
surface_mode: undecided
direction_name: undecided
dials:
  variance: null
  motion: null
  density: null
tokens:
  colors: {}
  typography: {}
  spacing: {}
  radii: {}
  motion: {}
---

# Design Read

Write one sentence: `<surface mode> for <audience>, with <specific visual world>, optimized for <primary outcome>`.

# Product and audience

State the primary user, their context, and the task this interface must make easier.

State whether external inspiration research is required. For narrow Operate/Read work or strict brand-preserve refinement, record why incumbent product, design-system, and rendered evidence are sufficient.

# Visual thesis

Commit to one specific visual world. Define the dominant composition, first/second/third attention hierarchy, material or media language, and why they fit this product. Name the one signature moment and three to five anti-goals. Do not merge abandoned directions.

# Dials and rationale

Set variance, motion, and density from 1-10. Explain how each value follows from the surface mode, audience, and platform.

# Composition map

| Section or state | Single job | Layout family | Contrast role | Media | Motion role |
|---|---|---|---|---|---|

Avoid three consecutive sections with the same grammar. State the explicit mobile recomposition for every multi-column section.

# Art-direction proof

Record the navigation/app frame, first viewport, representative downstream section, real content/media used, desktop/mobile screenshot paths, findings, and approval result. Do not expand the full surface before the proof reads clearly.

# Colors

Define semantic roles, usage ratios, contrast, theme behavior, and status colors. Start from product/brand evidence; there are no starter colors to preserve.

# Typography

Define display, body, label, and data roles; source and fallbacks; line length; wrapping; tracking; and numeric behavior.

# Layout and responsive behavior

Define container, grid, main and side tracks, spacing rhythm, density, breakpoints, overflow, and mobile reflow.

# Elevation, depth, and surfaces

Define borders, shadows, texture, media treatment, layering, and lighting direction.

# Shapes and iconography

Define radius hierarchy, icon family, stroke weight, illustration or photography language, and prohibited clichés.

# Asset plan

List each important media role, aspect ratio, source/rights, treatment, responsive crop, fallback, and replacement owner. Operate surfaces should use real product states rather than unrelated photography.

# Components and states

Define anatomy, variants, default, hover, focus, pressed, disabled, loading, empty, success, error, validation, keyboard, and touch behavior.

# Motion thesis and motion tokens

State how motion directs attention, explains continuity, or confirms state. Define triggers, durations, easing, interruption, cleanup, and reduced-motion fallback. Allow one primary focal motion per viewport.

# Content rules

Define voice, terminology, real data rules, CTA style, error language, and placeholder policy.

# Do / Don't

Write short product-specific positive and negative constraints. Avoid generic anti-pattern lists that are unrelated to this product.

# Exceptions

Record any intentional conflict with the Skill's lower-priority guidance, why the higher-priority brief or platform rule wins, and how the exception will be tested.

# Platform notes

State what is Web-specific and which semantic tokens or behaviors can later map to mobile or desktop.

# Approval

Record approver, date, approved version, approval evidence path, and any explicit exceptions. Set frontmatter `status: approved` only after the evidence exists. Return status to `draft` when the brief, direction, tokens, or platform changes materially.
