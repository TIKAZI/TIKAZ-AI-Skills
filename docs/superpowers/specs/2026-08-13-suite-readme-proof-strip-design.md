# Suite README Proof Strip Design

## Goal

Give every standalone suite repository an immediate, credible four-item proof strip before its introduction, in both English and Simplified Chinese.

## Design read

GitHub-native developer documentation for open-source adopters. The visual language is precise, evidence-first, Primer-compatible, and restrained within the TIKAZ brand.

- Design variance: 4. The strip adds hierarchy without changing repository information architecture.
- Motion intensity: 1. GitHub README content is static.
- Visual density: 5. Four short proof cells provide a fast scan before the detailed explanation.

## Layout

The strip sits after the repository badges and collection link, before the first explanatory heading. It uses one native HTML table with four equal 200px cells. This fills a typical GitHub repository README column while GitHub's own table wrapper provides bounded horizontal scrolling on narrower screens. Each cell contains:

1. one short, prominent value;
2. one concise label;
3. an accessible title containing the full evidence note.

No custom CSS, images, fake charts, or decorative cards are required. The table must remain readable in GitHub light and dark themes and degrade to horizontal scrolling on very narrow screens without clipping text.

## Evidence policy

- Context Economy may use measured fixed-benchmark results, with the scope stated in the labels and notes.
- Other suites use verifiable structural counts, explicit workflow contracts, and QA gates.
- No universal accuracy, adoption, superiority, or performance claim may be inferred from a structural count.
- Every suite has exactly four proof items and both languages share the same values.

## Source of truth

`distribution/manifest.json` owns each suite's proof values, English labels, Chinese labels, and evidence notes. Export code renders the same data into both language variants, preventing drift between standalone repositories.

## Acceptance criteria

- Seven suites each define exactly four proof items.
- English and Chinese standalone READMEs show all four items in the approved location.
- Values and labels are non-empty, concise, and HTML-safe.
- Context Economy includes the fixed-benchmark scope and links to detailed evidence.
- Automated tests validate source data, rendering, ordering, and bilingual parity.
- All existing repository, Skill, and distribution validation remains green.
