# TIKAZ Visual System

This document is the source of truth for repository Heroes, workflow diagrams, evidence cards, and the GitHub Pages gallery. Visual assets remain editable SVG or self-contained HTML; generated raster imagery is not used for product explanation.

## Brand direction

TIKAZ uses a white documentation canvas and a deep blue-black presentation surface. Blue is the collection-level brand color. A suite may use one secondary accent to aid recognition, but the structure, typography, spacing, and diagram grammar remain shared.

| Token | Value | Use |
|---|---|---|
| `page` | `#FFFFFF` | README and documentation canvas |
| `card-start` | `#080D18` | Hero and dark diagram surface |
| `card-end` | `#18253A` | Blue-led gradient endpoint |
| `ink` | `#F8FAFC` | Primary text on dark surfaces |
| `muted` | `#CBD5E1` | Supporting text |
| `soft` | `#94A3B8` | Metadata and inactive connectors |
| `line` | `#334155` | Structural borders and connectors |
| `primary` | `#60A5FA` | TIKAZ collection accent and primary action |
| `purple` | `#A78BFA` | Engineering suite accent |
| `radius` | `30px` | Hero radius; diagrams use `16px` or less |

## Suite accents

| Suite | Accent |
|---|---|
| Context Economy | `#60A5FA` |
| Video Intelligence | `#22D3EE` |
| Frontend Design | `#8B5CF6` |
| Engineering | `#A78BFA` |
| Knowledge & Research | `#34D399` |
| Presentation | `#F59E0B` |
| Visual Content | `#F472B6` |

## Hero contract

- Use the same 1440 × 500 composition for every suite.
- Keep a short collection eyebrow, one title, one concise promise, one action label, and one suite accent.
- Use a subtle grid only inside the Hero.
- Do not use drop shadows, fake screenshots, decorative version telemetry, or photographic backgrounds.
- Keep the title within two lines and the promise within three lines.

## Diagram contract

- Prefer an editable inline SVG embedded in a self-contained HTML file; publish a matching SVG for GitHub README use.
- Select a diagram only when relationships are clearer than prose or a table.
- Use orthogonal connectors with rounded turns. Never route a connector through a node.
- Use neutral nodes and reserve the suite accent for the active route or one to two important decisions.
- Use no shadows. Use `16px` node corners and a target information density of 4/10.
- Include a title, a one-sentence reading guide, accessible `<title>` and `<desc>`, and text labels that remain readable at 900px width.
- Use the dark grid only for Heroes. Workflow diagrams use a clean dark surface with sparse guide lines.

## Evidence and examples

- Use real checked-in inputs and outputs. Label synthetic fixtures explicitly.
- Keep estimates, measured values, pending work, and limitations visually distinct.
- Never turn a benchmark into a universal product claim.
- Every visual claim must link to its source artifact or reproducible command.

## Ownership

The TIKAZ visual system is designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.
