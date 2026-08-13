# Implementation Plan: TIKAZ AI Skills Productization

## Objective

Turn the canonical collection into one blue-led visual system, seven independently understandable suite product pages, and thirty Skills that remain usable when installed without their parent suite.

## Architecture decisions

- Keep one canonical monorepo and seven generated distribution repositories.
- Do not create thirty separate repositories or add README files inside Skill folders.
- Make each `SKILL.md` close its own input, workflow, output, validation, fallback, example, and limitation loop.
- Generate repeated catalog and SVG assets deterministically from repository metadata.
- Use `#60A5FA` as the collection and Context Economy primary blue; move `#A78BFA` to Engineering.
- Keep source and license attribution factual. TIKAZ contribution statements do not replace upstream notices.

## Phases

### Phase 1: Foundation

- [x] Record the blue-led TIKAZ visual system.
- [x] Add deterministic workflow SVG and Skills Catalog generation.
- [x] Add independent-usage validation without inventing capabilities.

Verification: generated assets are deterministic, valid UTF-8, and repository validation stays green.

### Phase 2: Context Economy reference implementation

- [x] Close the five Skill contracts.
- [x] Add a workflow SVG and suite-level Skill catalog.
- [x] Add copy-ready examples, limitations, and evidence links.

Verification: all existing Context Economy tests pass and every public claim points to checked-in evidence.

### Phase 3: Six-suite expansion

- [x] Apply the product-page structure to the remaining suites.
- [x] Add one workflow SVG and copy-ready examples per suite.
- [x] Add all missing `agents/openai.yaml` files.

Verification: every suite can be installed and understood without reading the root README.

### Phase 4: Thirty-Skill closure

- [x] Bring each Skill to the independent-use contract.
- [x] Re-scope `video-workbench` as a reusable media-application engineering workflow.
- [x] Generate and review the collection-wide Skills Catalog.

Verification: the independent-use validator reports no missing contract fields.

### Phase 5: Release readiness

- [x] Run unit tests, repository validation, distribution builds, UTF-8 checks, and visual review.
- [x] Review provenance, limitations, and generated diffs.
- [x] Publish after explicit release authorization and verify the live Pages deployment.

### Phase 6: Bilingual project pages and evidence-first positioning

- [x] Generate one English and one Chinese project page for every Skill without duplicating the execution source.
- [x] Group all 30 project pages under the seven workflow families.
- [x] Put verified measurements or inspectable quality gates before usage details.
- [x] Link the root, suite, Pages, and standalone distribution entry points to rendered project pages.
- [x] Complete desktop/mobile visual QA, full validation, and publication sync.

Verification: 30 English and 30 Chinese project pages exist; all public links resolve; measured claims preserve their fixed-benchmark boundary; other suites do not invent performance percentages.

## Risks

| Risk | Mitigation |
|---|---|
| Repetitive documentation inflates context | Keep Skill bodies concise and move detail to suite references |
| Generated pages drift from Skills | Generate catalogs from frontmatter and validate on every push |
| Marketing overstates optional tools | Document host capability checks and explicit fallback routes |
| Visual consistency becomes decorative sameness | Share tokens and grammar while preserving suite-specific semantic diagrams |
| Third-party origin becomes unclear | Preserve `SOURCES.yml`, notices, licenses, and concrete contribution statements |

## Release boundary

Implementation and local verification are authorized. Git push, GitHub Release creation, and synchronization to standalone repositories remain separate release actions and require final verified state.
