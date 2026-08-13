# TIKAZ Skill Project Pages and Evidence Design

## Goal

Give every published Skill a bilingual, independently shareable project page while keeping one English `SKILL.md` as the only executable instruction source.

## Information hierarchy

Each project page presents information in this order:

1. A one-sentence capability promise.
2. Three evidence or quality-gate cards.
3. The exact task the Skill owns and when to use it.
4. An independent installation command and invocation example.
5. A link to the canonical execution contract and neighboring Skills in the same workflow.

The main README, Chinese mirror, Pages catalog, seven suite READMEs, and seven standalone distributions link directly to these rendered Pages URLs. The 30 pages remain grouped under seven workflow families; they are not split into 30 repositories.

## Claim policy

- Context Economy may show checked-in benchmark measurements only with the dataset and measurement boundary visible.
- `69.73%` means estimated token reduction on six fixed long-context tasks (`4,698 → 1,422`), not universal savings.
- `27.78%` means estimated reduction across six fixed exact/structural prompt cases (`252 → 182`); semantic rewriting remains disabled pending equivalence evaluation.
- `46/46` means literal recall of declared protected facts, not semantic or downstream answer accuracy.
- `39/39` means expected source anchors were retained on the fixed public cases.
- Three generated PDFs retain all declared text, numbers, table cells, and page anchors; visual-description accuracy remains unscored and cannot be claimed.
- The `+143.93%` short-input overhead remains visible to show when protocol structure costs more than it saves.
- Other suites show inspectable workflow properties, stage counts, routing rules, and quality gates. They do not receive invented performance percentages.

## Visual system

Evidence cards use the existing blue-led TIKAZ system: `#60A5FA` as the primary accent, dark surfaces, editable HTML/CSS, and responsive one-column stacking on mobile. Numeric results are visually prominent; claim boundaries and evidence links remain directly below them.

## Validation

- Generate 30 English and 30 Chinese project pages deterministically.
- Verify every public entry links all 30 Skills.
- Verify evidence headings and claim boundaries in both languages.
- Build all seven standalone distributions and verify individual Skill links.
- Render representative English and Chinese pages at desktop and mobile widths, check console errors and horizontal overflow.
