#!/usr/bin/env python3
"""Deterministic context preparation primitives for TIKAZ Context Economy."""

from __future__ import annotations

import argparse
import csv
import html
import hashlib
import json
import math
import re
import shutil
import sys
from pathlib import Path
from typing import NamedTuple, Sequence


CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
ASCII_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[^\sA-Za-z0-9_\u3400-\u9fff]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
URL_RE = re.compile(r"https?://[^\s)>\]}]+")
NUMBER_RE = re.compile(r"(?<!\w)(?:v?\d+(?:\.\d+){1,}|[+-]?\d[\d,]*(?:\.\d+)?%?)(?!\w)", re.I)
TERM_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]*|[\u3400-\u9fff]")
REQUIRED_SNAPSHOT_SECTIONS = (
    "Goal",
    "Confirmed Constraints",
    "Decisions",
    "Completed",
    "Remaining",
    "Evidence",
    "Open Questions",
)
CORE_SUFFIXES = {
    ".md", ".markdown", ".txt", ".json", ".jsonl", ".csv", ".tsv",
    ".yaml", ".yml", ".html", ".htm", ".py", ".js", ".jsx", ".ts",
    ".tsx", ".java", ".go", ".rs", ".c", ".cpp", ".cs", ".php", ".rb",
    ".swift", ".kt", ".scala", ".sh", ".ps1", ".sql", ".css", ".xml",
    ".toml", ".ini", ".cfg", ".log",
}


class Chunk(NamedTuple):
    source: str
    anchor: str
    heading: str
    text: str
    token_estimate: int
    content_hash: str
    protected_facts: tuple[str, ...]


class BuildResult(NamedTuple):
    mode: str
    source_tokens: int
    unique_tokens: int
    packed_tokens: int
    duplicate_tokens: int
    selected_chunks: int
    omitted_chunks: int


class ValidationResult(NamedTuple):
    valid: bool
    missing_sections: tuple[str, ...]
    missing_protected_facts: tuple[str, ...]


class CheckpointDrift(NamedTuple):
    removed_protected_facts: tuple[str, ...]
    added_protected_facts: tuple[str, ...]


class AuditReport(NamedTuple):
    scores: dict[str, int]
    reasons: dict[str, str]
    findings: tuple[dict[str, str], ...]


class BenchmarkResult(NamedTuple):
    total_cases: int
    passed_cases: int
    failed_cases: int
    total_source_tokens: int
    total_packed_tokens: int
    overall_savings_ratio: float
    declared_protected_facts: int


def normalize_text(text: str) -> str:
    """Normalize line endings and trailing whitespace without rewriting content."""

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(line.rstrip() for line in lines).strip() + ("\n" if text else "")


def _expand_inputs(inputs: Sequence[Path | str]) -> list[Path]:
    expanded: list[Path] = []
    for value in inputs:
        path = Path(value).expanduser().resolve()
        if path.is_file():
            expanded.append(path)
        elif path.is_dir():
            expanded.extend(
                child for child in sorted(path.rglob("*"))
                if child.is_file() and child.suffix.lower() in CORE_SUFFIXES
                and not any(part.startswith(".") for part in child.relative_to(path).parts)
            )
        else:
            raise FileNotFoundError(path)
    if not expanded:
        raise ValueError("at least one supported input is required")
    return expanded


def _canonical_name(path: Path) -> str:
    return path.name if path.suffix.lower() in {".md", ".markdown", ".txt"} else f"{path.name}.md"


def _canonicalize(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm"}:
        text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", raw)
        text = re.sub(r"(?i)</?(h[1-6]|p|div|li|tr|br|section|article)[^>]*>", "\n", text)
        return normalize_text(html.unescape(re.sub(r"<[^>]+>", "", text)))
    if suffix == ".json":
        return normalize_text(json.dumps(json.loads(raw), ensure_ascii=False, indent=2))
    if suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        rows = list(csv.reader(raw.splitlines(), delimiter=delimiter))
        return normalize_text("\n".join(" | ".join(cell for cell in row) for row in rows))
    return normalize_text(raw)


def estimate_tokens(text: str) -> int:
    """Estimate tokens for budgeting; never use this as provider billing telemetry."""

    if not text:
        return 0
    cjk_count = len(CJK_RE.findall(text))
    without_cjk = CJK_RE.sub("", text)
    ascii_units = sum(len(unit) for unit in ASCII_TOKEN_RE.findall(without_cjk))
    return cjk_count + math.ceil(ascii_units / 4)


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u3400-\u9fff]+", "-", value)
    return value.strip("-") or "section"


def extract_protected_facts(text: str) -> tuple[str, ...]:
    facts = set(URL_RE.findall(text))
    facts.update(match.group(0) for match in NUMBER_RE.finditer(text))
    for fence in re.findall(r"```[^\n]*\n.*?```", text, flags=re.S):
        facts.add(fence)
    return tuple(sorted(facts))


def _make_chunk(source: str, anchor: str, heading: str, lines: list[str]) -> Chunk:
    text = normalize_text("\n".join(lines))
    return Chunk(
        source=source,
        anchor=anchor,
        heading=heading,
        text=text,
        token_estimate=estimate_tokens(text),
        content_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        protected_facts=extract_protected_facts(text),
    )


def split_markdown(text: str, source: str) -> list[Chunk]:
    """Split Markdown at headings while keeping fenced code intact."""

    normalized = normalize_text(text)
    if not normalized.strip():
        return []

    chunks: list[Chunk] = []
    current_lines: list[str] = []
    current_heading = "Document"
    current_anchor = "document"
    anchor_counts: dict[str, int] = {}
    in_fence = False

    def unique_anchor(heading: str) -> str:
        base = _slugify(heading)
        anchor_counts[base] = anchor_counts.get(base, 0) + 1
        return base if anchor_counts[base] == 1 else f"{base}-{anchor_counts[base]}"

    for line in normalized.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence

        heading_match = None if in_fence else HEADING_RE.match(line)
        if heading_match:
            if current_lines:
                chunks.append(_make_chunk(source, current_anchor, current_heading, current_lines))
            current_heading = heading_match.group(2).strip()
            current_anchor = unique_anchor(current_heading)
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        chunks.append(_make_chunk(source, current_anchor, current_heading, current_lines))
    return chunks


def deduplicate_chunks(chunks: Sequence[Chunk]) -> tuple[list[Chunk], list[dict[str, str]]]:
    """Remove exact normalized duplicates and retain their canonical anchors."""

    unique: list[Chunk] = []
    duplicates: list[dict[str, str]] = []
    by_hash: dict[str, Chunk] = {}
    for chunk in chunks:
        canonical = by_hash.get(chunk.content_hash)
        if canonical is None:
            by_hash[chunk.content_hash] = chunk
            unique.append(chunk)
            continue
        duplicates.append(
            {
                "duplicate_source": chunk.source,
                "duplicate_anchor": chunk.anchor,
                "canonical_source": canonical.source,
                "canonical_anchor": canonical.anchor,
                "content_hash": chunk.content_hash,
            }
        )
    return unique, duplicates


def _query_terms(query: str) -> list[str]:
    return [term.lower() for term in TERM_RE.findall(query) if len(term) > 1 or CJK_RE.fullmatch(term)]


def _chunk_relevance_score(chunk: Chunk, query: str) -> int:
    terms = sorted(set(_query_terms(query)))
    text = chunk.text.lower()
    heading = chunk.heading.lower()
    overlap = 5 * sum(1 for term in terms if term in text)
    heading_bonus = 4 * sum(1 for term in terms if term in heading)
    fact_bonus = 5 * sum(1 for fact in chunk.protected_facts if fact.lower() in query.lower())
    return overlap + heading_bonus + fact_bonus


def rank_chunks(chunks: Sequence[Chunk], query: str) -> list[Chunk]:
    """Rank exact chunks with a transparent lexical heuristic."""

    def score(chunk: Chunk) -> tuple[int, int, str, str]:
        return (-_chunk_relevance_score(chunk, query), chunk.token_estimate, chunk.source, chunk.anchor)

    return sorted(chunks, key=score)


def choose_mode(
    source_tokens: int,
    budget_tokens: int,
    repeated_tokens: int,
    preparation_cost: int,
    reuse_count: int = 1,
    stable_prefix: bool = False,
) -> str:
    """Choose a primary mode from budget, overhead, repetition, and reuse."""

    if min(source_tokens, budget_tokens, repeated_tokens, preparation_cost) < 0:
        raise ValueError("token and cost values must be non-negative")
    if source_tokens <= budget_tokens:
        return "pass-through"
    if source_tokens - budget_tokens <= preparation_cost:
        return "pass-through"
    return "select"


def _safe_destination(output_root: Path, relative_path: Path) -> Path:
    destination = (output_root / relative_path).resolve()
    try:
        destination.relative_to(output_root)
    except ValueError as error:
        raise ValueError(f"artifact path escapes output directory: {relative_path}") from error
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination


def _write_text(output_root: Path, relative_path: Path, content: str) -> None:
    destination = _safe_destination(output_root, relative_path)
    destination.write_text(content, encoding="utf-8", newline="\n")


def _write_json(output_root: Path, relative_path: Path, value: object) -> None:
    serialized = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    _write_text(output_root, relative_path, serialized)


def _select_within_budget(chunks: Sequence[Chunk], budget_tokens: int) -> tuple[list[Chunk], list[Chunk]]:
    selected: list[Chunk] = []
    omitted: list[Chunk] = []
    used = 0
    for chunk in chunks:
        if not selected or used + chunk.token_estimate <= budget_tokens:
            selected.append(chunk)
            used += chunk.token_estimate
        else:
            omitted.append(chunk)
    return selected, omitted


def _split_prose_chunk(chunk: Chunk, max_tokens: int) -> list[Chunk]:
    if chunk.token_estimate <= max_tokens or "```" in chunk.text or max_tokens < 8:
        return [chunk]
    words = re.findall(r"\S+\s*", chunk.text)
    pieces: list[Chunk] = []
    current: list[str] = []
    for word in words:
        candidate = "".join(current + [word])
        if current and estimate_tokens(candidate) > max_tokens:
            index = len(pieces) + 1
            pieces.append(_make_chunk(chunk.source, f"{chunk.anchor}-part-{index}", chunk.heading, ["".join(current)]))
            current = [word]
        else:
            current.append(word)
    if current:
        index = len(pieces) + 1
        pieces.append(_make_chunk(chunk.source, f"{chunk.anchor}-part-{index}", chunk.heading, ["".join(current)]))
    return pieces


def _context_pack_markdown(
    query: str,
    mode: str,
    budget_tokens: int,
    selected: Sequence[Chunk],
    omitted: Sequence[Chunk],
) -> str:
    selected_facts = sorted({fact for chunk in selected for fact in chunk.protected_facts})
    omitted_facts = sorted({fact for chunk in omitted for fact in chunk.protected_facts})
    lines = [
        "# Context Pack",
        f"Task: {query}",
        f"Mode: `{mode}` | final budget {budget_tokens}t estimated",
        f"Protected: {len(selected_facts)} retained; {len(omitted_facts)} omitted",
        "## Evidence Excerpts",
    ]
    for chunk in selected:
        lines.extend(
            [
                f"### [{chunk.source}#{chunk.anchor}] {chunk.heading}",
                chunk.text.rstrip(),
            ]
        )
    lines.extend(
        [
            "## Omitted Anchors",
        ]
    )
    if omitted:
        lines.append("- " + ", ".join(f"[{chunk.source}#{chunk.anchor}]" for chunk in omitted))
    if not omitted:
        lines.append("- None.")
    lines.extend(
        [
        "## Limits",
        "Estimated only; lexical selection is not semantic proof.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_pack(
    inputs: Sequence[Path | str],
    query: str,
    budget_tokens: int,
    output_dir: Path | str,
) -> BuildResult:
    """Build deterministic canonical, index, ledger, pack, and report artifacts."""

    if budget_tokens <= 0:
        raise ValueError("budget_tokens must be positive")
    if not query.strip():
        raise ValueError("query must not be empty")

    output_root = Path(output_dir).expanduser().resolve()
    if output_root.exists() and not output_root.is_dir():
        raise ValueError(f"output path is not a directory: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)

    resolved_inputs = _expand_inputs(inputs)
    for path in resolved_inputs:
        if path.suffix.lower() not in CORE_SUFFIXES:
            raise ValueError(f"unsupported core input: {path}")

    canonical_names = [_canonical_name(path) for path in resolved_inputs]
    if len(canonical_names) != len(set(canonical_names)):
        raise ValueError("input files must have unique canonical names")

    all_chunks: list[Chunk] = []
    source_records: list[dict[str, object]] = []
    for path, canonical_name in zip(resolved_inputs, canonical_names):
        canonical = _canonicalize(path)
        _write_text(output_root, Path("canon") / canonical_name, canonical)
        chunks = split_markdown(canonical, canonical_name)
        all_chunks.extend(chunks)
        index = [
            {
                "anchor": chunk.anchor,
                "content_hash": chunk.content_hash,
                "heading": chunk.heading,
                "protected_facts": list(chunk.protected_facts),
                "token_estimate": chunk.token_estimate,
            }
            for chunk in chunks
        ]
        _write_json(output_root, Path("indexes") / f"{Path(canonical_name).stem}.index.json", index)
        source_records.append(
            {
                "canonical": canonical_name,
                "content_hash": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
                "input_name": path.name,
                "token_estimate": sum(chunk.token_estimate for chunk in chunks),
            }
        )

    unique_chunks, duplicates = deduplicate_chunks(all_chunks)
    token_by_hash = {chunk.content_hash: chunk.token_estimate for chunk in all_chunks}
    duplicate_tokens = sum(token_by_hash[item["content_hash"]] for item in duplicates)
    source_tokens = sum(chunk.token_estimate for chunk in all_chunks)
    unique_tokens = sum(chunk.token_estimate for chunk in unique_chunks)
    preparation_cost = max(12, math.ceil(source_tokens * 0.03))
    mode = choose_mode(source_tokens, budget_tokens, duplicate_tokens, preparation_cost)

    ranked = rank_chunks(unique_chunks, query)
    if mode == "pass-through":
        candidates = list(unique_chunks)
    else:
        highest_score = _chunk_relevance_score(ranked[0], query) if ranked else 0
        minimum_score = max(1, math.ceil(highest_score * 0.5))
        candidates = [chunk for chunk in ranked if _chunk_relevance_score(chunk, query) >= minimum_score]
    protected_oversize = next(
        (chunk for chunk in candidates if chunk.token_estimate > budget_tokens and "```" in chunk.text),
        None,
    )
    if protected_oversize is not None:
        mode = "budget-conflict"
        selected = []
        omitted = list(ranked)
        pack = "# Context Pack\n\nMode: `budget-conflict`\n\nEssential protected material exceeds the final budget. See the savings report.\n"
    else:
        protocol_floor = estimate_tokens(_context_pack_markdown(query, mode, budget_tokens, [], ranked))
        evidence_budget = max(0, budget_tokens - protocol_floor)
        expanded_candidates = [piece for chunk in candidates for piece in _split_prose_chunk(chunk, evidence_budget)]
        selected, _ = _select_within_budget(expanded_candidates, evidence_budget)
        def current_omissions() -> list[Chunk]:
            return [
                chunk for chunk in ranked
                if not any(
                    selected_chunk.source == chunk.source
                    and selected_chunk.anchor.startswith(chunk.anchor)
                    for selected_chunk in selected
                )
            ]

        omitted = current_omissions()
        pack = _context_pack_markdown(query, mode, budget_tokens, selected, omitted)
        while selected and estimate_tokens(pack) > budget_tokens:
            selected.pop()
            omitted = current_omissions()
            pack = _context_pack_markdown(query, mode, budget_tokens, selected, omitted)
        if estimate_tokens(pack) > budget_tokens:
            mode = "budget-conflict"
            pack = "# Context Pack\n\nMode: `budget-conflict`\n\nThe required omitted-anchor inventory exceeds the final budget. See the savings report.\n"
    packed_tokens = estimate_tokens(pack)
    _write_text(output_root, Path("packs") / "current-task.context.md", pack)

    ledger = {
        "duplicate_chunks": duplicates,
        "estimation_method": "CJK characters plus ceil(non-CJK lexical characters / 4)",
        "mode": mode,
        "query": query,
        "sources": source_records,
        "unique_chunks": [
            {
                "anchor": chunk.anchor,
                "content_hash": chunk.content_hash,
                "source": chunk.source,
                "token_estimate": chunk.token_estimate,
            }
            for chunk in unique_chunks
        ],
    }
    _write_json(output_root, Path("ledger.json"), ledger)

    report_lines = [
        "# Context Economy Savings Report",
        "",
        f"- Selected mode: `{mode}`",
        f"- Source tokens (estimated): {source_tokens}",
        f"- Unique tokens after exact deduplication (estimated): {unique_tokens}",
        f"- Duplicate tokens removed (estimated): {duplicate_tokens}",
        f"- Packed artifact tokens including labels (estimated): {packed_tokens}",
        f"- Preparation overhead used for break-even decision (estimated): {preparation_cost}",
        f"- Selected chunks: {len(selected)}",
        f"- Omitted chunks: {len(omitted)}",
        "- Budget conflict: essential protected material exceeds the requested budget; minimum viable size must be reviewed."
        if mode == "budget-conflict" else "- Budget conflict: none.",
        "- Method: CJK characters plus ceil(non-CJK lexical characters / 4).",
        "- Limit: estimates are not provider billing telemetry or a semantic-equivalence score.",
        "",
    ]
    _write_text(output_root, Path("savings-report.md"), "\n".join(report_lines))

    return BuildResult(
        mode=mode,
        source_tokens=source_tokens,
        unique_tokens=unique_tokens,
        packed_tokens=packed_tokens,
        duplicate_tokens=duplicate_tokens,
        selected_chunks=len(selected),
        omitted_chunks=len(omitted),
    )


def validate_snapshot(snapshot_text: str, source_text: str) -> ValidationResult:
    """Check snapshot shape and literal protected-fact coverage."""

    headings = {
        match.group(1).strip().casefold()
        for match in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", snapshot_text)
    }
    missing_sections = tuple(
        section for section in REQUIRED_SNAPSHOT_SECTIONS if section.casefold() not in headings
    )
    missing_protected = tuple(
        fact for fact in extract_protected_facts(source_text) if fact not in snapshot_text
    )
    return ValidationResult(
        valid=not missing_sections and not missing_protected,
        missing_sections=missing_sections,
        missing_protected_facts=missing_protected,
    )


def create_checkpoint(source_text: str) -> str:
    """Create a conservative recovery artifact without rewriting the transcript."""

    normalized = normalize_text(source_text).rstrip()
    return (
        "# Goal\n\nRecover and continue the recorded task.\n\n"
        "# Confirmed Constraints\n\nPreserve the latest user direction and protected facts.\n\n"
        "# Decisions\n\nReview the exact evidence before treating inferred decisions as confirmed.\n\n"
        "# Completed\n\nNot established by deterministic checkpoint creation.\n\n"
        "# Remaining\n\nResolve the goal from the evidence and continue only verified work.\n\n"
        "# Evidence\n\n" + normalized + "\n\n"
        "# Open Questions\n\nWhich remaining action should be completed next?\n"
    )


def compare_checkpoints(previous: str, current: str) -> CheckpointDrift:
    before = set(extract_protected_facts(previous))
    after = set(extract_protected_facts(current))
    return CheckpointDrift(tuple(sorted(before - after)), tuple(sorted(after - before)))


SECRET_RE = re.compile(
    r"(?i)(?:api[_-]?key|token|secret|password)\s*[:=]\s*([A-Za-z0-9_\-]{12,})|\bsk-[A-Za-z0-9_-]{16,}\b"
)
PROMPT_INJECTION_RE = re.compile(
    r"(?i)(ignore|disregard|override)\s+(?:all\s+)?(?:previous|prior)\s+instructions"
)


def audit_context(text: str, task: str = "") -> AuditReport:
    """Return explainable heuristic context-health signals without source mutation."""

    normalized = normalize_text(text)
    lines = [line.strip() for line in normalized.splitlines() if line.strip()]
    duplicate_count = len(lines) - len(set(lines))
    chunks = split_markdown(normalized, "context.md")
    relevant = sum(1 for chunk in chunks if _chunk_relevance_score(chunk, task) > 0) if task else len(chunks)
    findings: list[dict[str, str]] = []
    first_line_by_text: dict[str, int] = {}
    duplicate_lines: list[int] = []
    for line_number, line in enumerate(normalized.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped in first_line_by_text:
            duplicate_lines.append(line_number)
        else:
            first_line_by_text[stripped] = line_number
    if duplicate_count:
        findings.append({"type": "redundancy", "severity": "medium", "anchor": f"context.md:L{duplicate_lines[0]}", "detail": f"{duplicate_count} repeated non-empty lines"})
    injection = PROMPT_INJECTION_RE.search(normalized)
    if injection:
        line_number = normalized[:injection.start()].count("\n") + 1
        findings.append({"type": "prompt-injection", "severity": "high", "anchor": f"context.md:L{line_number}", "detail": "instruction-like untrusted text detected"})
    for match in SECRET_RE.finditer(normalized):
        line_number = normalized[:match.start()].count("\n") + 1
        findings.append({"type": "secret-shaped-value", "severity": "high", "anchor": f"context.md:L{line_number}", "detail": "[REDACTED]"})
    heading_count = len(HEADING_RE.findall(normalized))
    protected_count = len(extract_protected_facts(normalized))
    has_recovery = all(f"# {section}" in normalized for section in REQUIRED_SNAPSHOT_SECTIONS)
    scores = {
        "relevance": max(0, min(100, round(100 * relevant / max(1, len(chunks))))),
        "redundancy": max(0, 100 - duplicate_count * 15),
        "traceability": min(100, 50 + heading_count * 10 + min(30, protected_count * 3)),
        "safety": max(0, 100 - 35 * sum(1 for item in findings if item["severity"] == "high")),
        "cacheability": max(0, 100 - duplicate_count * 5) if normalized else 0,
        "recoverability": 100 if has_recovery else min(70, 20 + heading_count * 8),
    }
    reasons = {
        "relevance": f"{relevant} of {len(chunks)} heading chunks have lexical overlap with the stated task" if task else "No task supplied; all chunks are provisionally relevant",
        "redundancy": f"{duplicate_count} repeated non-empty lines detected",
        "traceability": f"{heading_count} headings and {protected_count} protected facts contribute inspectable structure",
        "safety": f"{sum(1 for item in findings if item['severity'] == 'high')} high-severity heuristic findings; this is not a security certification",
        "cacheability": f"Stable-text heuristic reduced by {duplicate_count} repeated lines; freshness is not verified",
        "recoverability": "All checkpoint sections are present" if has_recovery else "Required checkpoint sections are incomplete",
    }
    return AuditReport(scores, reasons, tuple(findings))


def run_benchmark(manifest_path: Path | str, output_dir: Path | str) -> BenchmarkResult:
    """Run fixed local cases and retain raw failures alongside aggregate metrics."""

    manifest_file = Path(manifest_path).expanduser().resolve()
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("cases"), list):
        raise ValueError("benchmark manifest must use schema_version 1 and contain cases")
    output_root = Path(output_dir).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    for case in manifest["cases"]:
        case_id = str(case["id"])
        inputs = [(manifest_file.parent / value).resolve() for value in case["inputs"]]
        case_output = output_root / "artifacts" / case_id
        built = build_pack(inputs, str(case["task"]), int(case["budget"]), case_output)
        pack = (case_output / "packs" / "current-task.context.md").read_text(encoding="utf-8")
        expected_facts = [str(value) for value in case.get("protected_facts", [])]
        expected_anchors = [str(value) for value in case.get("expected_anchors", [])]
        retained_facts = sum(1 for value in expected_facts if value in pack)
        retained_anchors = sum(1 for value in expected_anchors if value in pack)
        failures: list[str] = []
        if built.packed_tokens > int(case["budget"]):
            failures.append("budget-exceeded")
        if retained_facts < len(expected_facts):
            failures.append("protected-fact-missing")
        if retained_anchors < len(expected_anchors):
            failures.append("expected-anchor-missing")
        results.append({
            "id": case_id,
            "profile": str(case.get("profile", "correctness")),
            "source_tokens": built.source_tokens,
            "packed_tokens": built.packed_tokens,
            "savings_ratio": 0 if not built.source_tokens else round(1 - built.packed_tokens / built.source_tokens, 4),
            "budget_compliant": built.packed_tokens <= int(case["budget"]),
            "protected_fact_recall": 1 if not expected_facts else round(retained_facts / len(expected_facts), 4),
            "anchor_correctness": 1 if not expected_anchors else round(retained_anchors / len(expected_anchors), 4),
            "failures": failures,
        })
    _write_json(output_root, Path("cases.json"), results)
    passed = sum(1 for result in results if not result["failures"])
    total_source = sum(int(result["source_tokens"]) for result in results)
    total_packed = sum(int(result["packed_tokens"]) for result in results)
    declared_facts = sum(len(case.get("protected_facts", [])) for case in manifest["cases"])
    summary = BenchmarkResult(
        len(results),
        passed,
        len(results) - passed,
        total_source,
        total_packed,
        0 if not total_source else round(1 - total_packed / total_source, 4),
        declared_facts,
    )
    summary_payload = summary._asdict()
    profiles: dict[str, dict[str, object]] = {}
    for profile in sorted({str(result["profile"]) for result in results}):
        group = [result for result in results if result["profile"] == profile]
        source_total = sum(int(result["source_tokens"]) for result in group)
        packed_total = sum(int(result["packed_tokens"]) for result in group)
        profiles[profile] = {
            "cases": len(group),
            "passed": sum(1 for result in group if not result["failures"]),
            "source_tokens": source_total,
            "packed_tokens": packed_total,
            "savings_ratio": 0 if not source_total else round(1 - packed_total / source_total, 4),
        }
    summary_payload["profiles"] = profiles
    _write_json(output_root, Path("summary.json"), summary_payload)
    return summary


def doctor_report() -> dict[str, object]:
    """Report core and optional local capabilities without changing the environment."""

    tokenizer = next((name for name in ("tiktoken", "tokenizers") if __import__("importlib").util.find_spec(name)), None)
    converter = shutil.which("markitdown") or shutil.which("pandoc")
    return {
        "python": {
            "available": True,
            "version": ".".join(str(value) for value in sys.version_info[:3]),
            "standard_library_core": True,
        },
        "tokenizer": {
            "available": tokenizer is not None,
            "provider": tokenizer,
            "required": False,
            "note": "Core budgets use an estimate; optional tokenizers are not billing telemetry.",
        },
        "document_converter": {
            "available": converter is not None,
            "command": converter,
            "required": False,
            "note": "Core text formats work without a converter; complex binaries need an external adapter.",
        },
        "installed_anything": False,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build deterministic TIKAZ Context Economy artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    pack = subparsers.add_parser("pack", help="Build a context pack from canonical Markdown or text.")
    pack.add_argument("--input", action="append", required=True, dest="inputs")
    pack.add_argument("--query", required=True)
    pack.add_argument("--budget", required=True, type=int, dest="budget_tokens")
    pack.add_argument("--output", required=True, dest="output_dir")
    snapshot = subparsers.add_parser("validate-snapshot", help="Validate a conversation state snapshot.")
    snapshot.add_argument("--snapshot", required=True)
    snapshot.add_argument("--source", required=True)
    checkpoint = subparsers.add_parser("checkpoint", help="Create a conservative conversation checkpoint.")
    checkpoint.add_argument("--source", required=True)
    checkpoint.add_argument("--output", required=True)
    audit = subparsers.add_parser("audit", help="Run a read-only heuristic Context Health audit.")
    audit.add_argument("--input", required=True)
    audit.add_argument("--task", default="")
    subparsers.add_parser("doctor", help="Report core and optional local capabilities without installation.")
    benchmark = subparsers.add_parser("benchmark", help="Run a versioned local benchmark manifest.")
    benchmark.add_argument("--manifest", required=True)
    benchmark.add_argument("--output", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "pack":
        result = build_pack(args.inputs, args.query, args.budget_tokens, args.output_dir)
        print(json.dumps(result._asdict(), ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "validate-snapshot":
        snapshot_text = Path(args.snapshot).read_text(encoding="utf-8")
        source_text = Path(args.source).read_text(encoding="utf-8")
        result = validate_snapshot(snapshot_text, source_text)
        print(json.dumps(result._asdict(), ensure_ascii=False, sort_keys=True))
        return 0 if result.valid else 1
    if args.command == "checkpoint":
        source_text = Path(args.source).read_text(encoding="utf-8")
        checkpoint_text = create_checkpoint(source_text)
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(checkpoint_text, encoding="utf-8", newline="\n")
        result = validate_snapshot(checkpoint_text, source_text)
        print(json.dumps(result._asdict(), ensure_ascii=False, sort_keys=True))
        return 0 if result.valid else 1
    if args.command == "audit":
        report = audit_context(Path(args.input).read_text(encoding="utf-8"), args.task)
        print(json.dumps(report._asdict(), ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "doctor":
        print(json.dumps(doctor_report(), ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "benchmark":
        result = run_benchmark(args.manifest, args.output)
        print(json.dumps(result._asdict(), ensure_ascii=False, sort_keys=True))
        return 0 if result.failed_cases == 0 else 1
    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
