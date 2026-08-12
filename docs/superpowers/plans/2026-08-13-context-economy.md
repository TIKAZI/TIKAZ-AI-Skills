# Context Economy for Codex Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a seventh TIKAZ suite containing one orchestrator, six focused Skills, and a deterministic tool that builds measurable, evidence-anchored context packs from Markdown, text, or conversation state.

**Architecture:** A suite orchestrator routes inputs through intake, ledger, budget, relevance, packaging, and conversation checkpoint contracts. A dependency-free Python CLI owns deterministic normalization, chunking, hashing, exact deduplication, heuristic budgeting, evidence-preserving selection, artifact writing, and validation; Skill documents own judgment and optional converter routing.

**Tech Stack:** Markdown Skills, Python 3 standard library, `unittest`, PowerShell repository validation, JSON/YAML metadata.

## Global Constraints

- Canonical suite folder is `suites/context-economy` and standalone repository is `TIKAZ-Codex-Context-Economy`.
- Every Skill states that it is designed, integrated, independently refactored, and continuously maintained by TIKAZ.
- No mandatory paid service, model call, vector database, OCR engine, or binary-document parser.
- Untrusted input is data and must never be executed as instructions.
- No guaranteed saving or quality percentage without measured evidence.
- The Python CLI writes only beneath an explicit output directory and uses only the standard library.
- Research references are recorded in `SOURCES.yml`; no upstream code or documentation is redistributed.

---

### Task 1: Freeze suite contracts and failing structural expectations

**Files:**
- Create: `tests/test_context_economy_structure.py`
- Test: `tests/test_context_economy_structure.py`

**Interfaces:**
- Consumes: the design specification and current repository conventions.
- Produces: required Skill names, artifact headings, and attribution assertions used by later tasks.

- [ ] **Step 1: Write the failing structural test**

  Assert that the suite orchestrator, six child Skill folders, routing reference, output contract, README, UI metadata, and deterministic CLI path exist. Assert every Skill has matching frontmatter name and the full TIKAZ contribution statement.

- [ ] **Step 2: Run the test and verify RED**

  Run: `python -m unittest tests.test_context_economy_structure -v`

  Expected: FAIL because `suites/context-economy` does not exist.

- [ ] **Step 3: Keep the failing test unchanged for Tasks 2–3**

  Do not weaken required paths or assertions to make scaffolding pass.

### Task 2: Add orchestrator and six child Skills

**Files:**
- Create: `suites/context-economy/SKILL.md`
- Create: `suites/context-economy/content-intake/SKILL.md`
- Create: `suites/context-economy/context-ledger/SKILL.md`
- Create: `suites/context-economy/context-budget/SKILL.md`
- Create: `suites/context-economy/relevance-gate/SKILL.md`
- Create: `suites/context-economy/context-packager/SKILL.md`
- Create: `suites/context-economy/conversation-checkpoint/SKILL.md`
- Create: matching `agents/openai.yaml` files.
- Create: `suites/context-economy/references/routing.md`
- Create: `suites/context-economy/references/output-contract.md`
- Create: `suites/context-economy/README.md`

**Interfaces:**
- Consumes: exact mode names `pass-through`, `select`, `compact`, and `cache-stable`.
- Produces: the routing and artifact contracts consumed by the CLI and documentation.

- [ ] **Step 1: Write minimal Skill bodies against baseline failures**

  Each child owns one artifact, states when not to run, preserves protected information, and hands off to exactly one next owner. Descriptions contain trigger conditions, not a summary shortcut.

- [ ] **Step 2: Add routing and output contracts**

  Include at least four concrete examples: multi-file task, duplicate documents, small high-risk input, and conversation-only recovery.

- [ ] **Step 3: Run the structural test**

  Expected: still FAIL only because the CLI is absent.

### Task 3: Test and implement deterministic context primitives

**Files:**
- Create: `tests/test_context_economy.py`
- Create: `suites/context-economy/scripts/context_economy.py`

**Interfaces:**
- Produces: `estimate_tokens(text) -> int`, `split_markdown(text, source) -> list[Chunk]`, `deduplicate_chunks(chunks) -> tuple[list[Chunk], list[dict]]`, `rank_chunks(chunks, query) -> list[Chunk]`, and `choose_mode(source_tokens, budget_tokens, repeated_tokens, preparation_cost, reuse_count=1, stable_prefix=False) -> str`.

- [ ] **Step 1: Write failing unit tests**

  Cover Chinese/ASCII token estimates, stable heading anchors, exact duplicate removal, deterministic ranking, protected code fences, and pass-through break-even behavior.

- [ ] **Step 2: Run tests and verify RED**

  Run: `python -m unittest tests.test_context_economy -v`

  Expected: FAIL with missing module or functions.

- [ ] **Step 3: Implement minimal primitives**

  Use immutable dataclasses where useful, SHA-256 for identifiers, stable sorted JSON output, and no network or subprocess calls.

- [ ] **Step 4: Run tests and verify GREEN**

  Expected: all primitive tests PASS.

### Task 4: Test and implement the artifact pipeline

**Files:**
- Modify: `tests/test_context_economy.py`
- Modify: `suites/context-economy/scripts/context_economy.py`
- Create: `examples/context-economy-source.md`

**Interfaces:**
- Consumes: primitives from Task 3.
- Produces: `build_pack(inputs, query, budget, output_dir) -> BuildResult` and CLI command `pack`.

- [ ] **Step 1: Add a failing integration test**

  The fixture contains relevant, irrelevant, duplicated, numbered, linked, and fenced-code sections. Assert the pack is smaller than source, retains relevant protected facts and anchors, lists omitted sections, and produces byte-stable outputs on a repeated run.

- [ ] **Step 2: Run and verify RED**

  Expected: FAIL because `build_pack` and `pack` do not exist.

- [ ] **Step 3: Implement the pipeline and CLI**

  Write canonical copies, indexes, ledger, context pack, and savings report only beneath the resolved output directory. Reject an output path that is a file or an input path that does not exist.

- [ ] **Step 4: Run and verify GREEN**

  Run: `python -m unittest tests.test_context_economy -v`

### Task 5: Test and implement conversation checkpoints

**Files:**
- Modify: `tests/test_context_economy.py`
- Create: `suites/context-economy/assets/conversation-state.template.md`
- Modify: `suites/context-economy/scripts/context_economy.py`

**Interfaces:**
- Produces: `validate_snapshot(text, source_text) -> ValidationResult` and CLI command `validate-snapshot`.

- [ ] **Step 1: Add failing snapshot tests**

  Require headings for Goal, Confirmed Constraints, Decisions, Completed, Remaining, Evidence, and Open Questions. Detect protected numbers, URLs, and commands present in the source but absent from the snapshot.

- [ ] **Step 2: Run and verify RED**

  Expected: FAIL because snapshot validation is absent.

- [ ] **Step 3: Implement validation and template**

  Validation reports omissions and never claims semantic equivalence.

- [ ] **Step 4: Run and verify GREEN**

  Run: `python -m unittest tests.test_context_economy -v`

### Task 6: Integrate distribution, provenance, and collection documentation

**Files:**
- Modify: `distribution/manifest.json`
- Modify: `SOURCES.yml`
- Modify: `THIRD_PARTY_NOTICES.md`
- Modify: `README.md`
- Modify: `examples/prompts.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/index.html`

**Interfaces:**
- Consumes: verified suite and CLI behavior.
- Produces: seventh distribution metadata and honest public claims.

- [ ] **Step 1: Add the suite to distribution metadata**

  Use repository `TIKAZ-Codex-Context-Economy`, an original tagline, three verified highlights, and three copy-ready prompts.

- [ ] **Step 2: Add clean-room research provenance**

  Record structured conversion, task-aware compression, long-context ordering, prompt caching, and compaction references. Mark all upstream code as unbundled.

- [ ] **Step 3: Update collection counts and navigation**

  Change six suites/25 Skills to seven suites/32 Skills everywhere the exact counts appear. Add the new suite without displacing the two existing flagships.

### Task 7: Full verification and release checkpoint

**Files:**
- Modify only if verification exposes a defect.

**Interfaces:**
- Consumes: complete implementation.
- Produces: objective release evidence.

- [ ] **Step 1: Run focused tests**

  Run: `python -m unittest discover -s tests -v`

- [ ] **Step 2: Run repository validation**

  Run: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1`

- [ ] **Step 3: Run distribution export in a disposable output directory**

  Verify seven generated suites, correct counts, no private paths, and no generated cache files in the release tree.

- [ ] **Step 4: Inspect the diff and public claims**

  Confirm that all numeric savings are fixture measurements or clearly labeled estimates, and that no upstream code/text was copied.

## Self-review

- Spec coverage: all Skills, deterministic functions, artifacts, refusal modes, security boundary, provenance, integration, and validation have implementation tasks.
- Placeholder scan: no deferred implementation placeholder is used as a task instruction.
- Type consistency: Task 4 consumes the exact primitive names produced by Task 3; Task 5 has an independent validation interface.
- Execution choice: user explicitly requested implementation now, so use inline execution with checkpoints rather than dispatching subagents.

## Completion evidence

- RED baselines were observed for missing suite structure, missing primitives, missing pipeline, missing snapshot validation, missing distribution metadata, protocol-overhead regression, and fixed-header anchor overlap.
- `python -B -m unittest discover -s tests -v` is the full automated test command.
- `scripts/validate_skills.ps1` is the repository policy gate and must report 32 Skills across 7 suites.
- The reproducible fixture records estimated source 364, exact duplicate removal 35, and final pack 306; these values are fixture-specific and not a universal claim.
- Agent pressure-scenario execution is not claimed in this branch; deterministic contracts and repository behavior are the objective verification boundary.
