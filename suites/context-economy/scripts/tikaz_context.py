#!/usr/bin/env python3
"""Deterministic context preparation primitives for TIKAZ Context Economy."""

from __future__ import annotations

import argparse
import csv
import html
import hashlib
import importlib.util
import ipaddress
import json
import math
import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


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
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*?src=[\"']([^\"']+)[\"'][^>]*?(?:alt=[\"']([^\"']*)[\"'])?[^>]*>", re.I)
DECORATIVE_VISUAL_RE = re.compile(
    r"(?i)\b(?:logo|icon|avatar|badge|watermark|divider|spacer|decoration|decorative|background|bullet)\b|徽标|图标|头像|水印|装饰|背景"
)
INFORMATIVE_VISUAL_RE = re.compile(
    r"(?i)\b(?:chart|graph|diagram|architecture|flow|matrix|screenshot|map|plot|figure|table|schema|timeline)\b|图表|流程|架构|截图|地图|示意|曲线|矩阵|表格|数据"
)
COMPLEX_TABLE_RE = re.compile(r"(?i)merged|merge|rowspan|colspan|multi[- ]?level|color[- ]?coded|跨页|合并单元格|多级表头|颜色编码")
SOURCE_VISUAL_RE = re.compile(r"<!--\s*source-visual:\s*([^>]+?)\s*-->", re.I)
VERSION = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()
DEFAULT_BENCHMARK_MANIFEST = Path(__file__).resolve().parents[1] / "benchmarks" / "manifest.json"


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


class PromptCompileResult(NamedTuple):
    mode: str
    method: str
    source_tokens: int
    compiled_tokens: int
    duplicate_units_removed: int
    protected_facts: int
    protected_fact_recall: float


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


def _default_defuddle_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "adapters" / "defuddle"


def _defuddle_available(
    adapter_dir: Path | str | None = None,
    node_command: Path | str | None = None,
) -> tuple[bool, str | None, str | None]:
    """Discover the optional pinned adapter without installing or changing anything."""

    root = Path(adapter_dir).expanduser().resolve() if adapter_dir else _default_defuddle_dir()
    if node_command:
        candidate = Path(node_command).expanduser()
        node = str(candidate.resolve()) if candidate.is_file() else shutil.which(str(node_command))
    else:
        node = shutil.which("node")
    package = root / "node_modules" / "defuddle" / "package.json"
    bridge = root / "extract.mjs"
    if not node or not Path(node).is_file() or not bridge.is_file() or not package.is_file():
        return False, node, None
    try:
        version = str(json.loads(package.read_text(encoding="utf-8"))["version"])
    except (OSError, KeyError, TypeError, ValueError):
        return False, node, None
    return version == "0.19.2", node, version


def _validate_public_web_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("web URL must be public HTTP(S) without embedded credentials")
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(parsed.hostname, parsed.port or 443)}
    except socket.gaierror as exc:
        raise ValueError(f"web URL host could not be resolved: {parsed.hostname}") from exc
    if not addresses:
        raise ValueError("web URL host did not resolve")
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            raise ValueError("web URL resolves to a private, local, reserved, or link-local address")
    return url


class _SafeWebRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        _validate_public_web_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch_public_html(url: str, timeout: float, max_bytes: int) -> bytes:
    _validate_public_web_url(url)
    request = Request(url, headers={"User-Agent": "TIKAZ-Context-Economy/1.0 (+https://github.com/TIKAZI)"})
    opener = build_opener(_SafeWebRedirectHandler())
    try:
        with opener.open(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"text/html", "application/xhtml+xml"}:
                raise ValueError(f"web source is not HTML: {content_type}")
            declared = response.headers.get("Content-Length")
            if declared and int(declared) > max_bytes:
                raise ValueError(f"web response exceeds {max_bytes} bytes")
            body = response.read(max_bytes + 1)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"web fetch failed: {exc}") from exc
    if len(body) > max_bytes:
        raise ValueError(f"web response exceeds {max_bytes} bytes")
    return body


def _invoke_defuddle(
    html_text: str,
    source_url: str,
    adapter_dir: Path,
    node_command: str,
    timeout: float,
) -> dict[str, object]:
    payload = json.dumps({"html": html_text, "url": source_url}, ensure_ascii=False)
    process = subprocess.run(
        [node_command, str(adapter_dir / "extract.mjs")],
        input=payload,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
        check=False,
    )
    if process.returncode != 0:
        message = process.stderr.strip() or f"adapter exited with code {process.returncode}"
        raise RuntimeError(f"Defuddle extraction failed: {message}")
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Defuddle adapter returned invalid JSON") from exc
    if not isinstance(result, dict):
        raise RuntimeError("Defuddle adapter returned a non-object result")
    return result


def extract_web_content(
    *,
    output_dir: Path | str,
    input_path: Path | str | None = None,
    url: str | None = None,
    task: str = "",
    adapter_dir: Path | str | None = None,
    node_command: Path | str | None = None,
    timeout: float = 15.0,
    max_bytes: int = 5_000_000,
) -> dict[str, object]:
    """Extract a web page conservatively and emit a source-preserving route report."""

    if bool(input_path) == bool(url):
        raise ValueError("provide exactly one of input_path or url")
    if timeout <= 0 or max_bytes <= 0:
        raise ValueError("timeout and max_bytes must be positive")
    output = Path(output_dir).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    source_url = _validate_public_web_url(url) if url else ""
    if input_path:
        source = Path(input_path).expanduser().resolve()
        if not source.is_file() or source.suffix.lower() not in {".html", ".htm"}:
            raise ValueError("local web input must be an existing .html or .htm file")
        raw_bytes = source.read_bytes()
        if len(raw_bytes) > max_bytes:
            raise ValueError(f"web source exceeds {max_bytes} bytes")
    else:
        try:
            raw_bytes = _fetch_public_html(source_url, timeout, max_bytes)
        except (RuntimeError, ValueError) as exc:
            failed_fetch: dict[str, object] = {
                "status": "fetch-failed",
                "route": "source",
                "adapter": "defuddle",
                "adapter_version": "0.19.2",
                "source_url": source_url,
                "original_bytes": 0,
                "cleaned_html_bytes": 0,
                "markdown_bytes": 0,
                "original_estimated_tokens": 0,
                "markdown_estimated_tokens": 0,
                "estimated_reduction_ratio": 0.0,
                "parse_time_ms": 0,
                "protected_facts": list(extract_protected_facts(source_url)),
                "visual_evidence": [],
                "warnings": ["web-fetch-failed", str(exc)],
                "task": task,
                "measurement_status": "estimated-not-provider-telemetry",
            }
            _write_json(output, Path("web-profile.json"), failed_fetch)
            return failed_fetch
    adapter_source_url = source.as_uri() if input_path else source_url
    (output / "source.html").write_bytes(raw_bytes)
    html_text = raw_bytes.decode("utf-8", errors="replace")
    root = Path(adapter_dir).expanduser().resolve() if adapter_dir else _default_defuddle_dir()
    available, node, adapter_version = _defuddle_available(root, node_command)

    base: dict[str, object] = {
        "status": "dependency-unavailable",
        "route": "source",
        "adapter": "defuddle",
        "adapter_version": adapter_version or "0.19.2",
        "source_url": source_url,
        "original_bytes": len(raw_bytes),
        "cleaned_html_bytes": 0,
        "markdown_bytes": 0,
        "original_estimated_tokens": estimate_tokens(html_text),
        "markdown_estimated_tokens": 0,
        "estimated_reduction_ratio": 0.0,
        "parse_time_ms": 0,
        "protected_facts": list(extract_protected_facts(html_text)),
        "visual_evidence": [],
        "warnings": ["defuddle-dependency-unavailable"],
        "task": task,
        "measurement_status": "estimated-not-provider-telemetry",
    }
    if not available or not node:
        _write_json(output, Path("web-profile.json"), base)
        return base
    try:
        extracted = _invoke_defuddle(html_text, adapter_source_url, root, node, timeout)
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        base["status"] = "extraction-failed"
        base["warnings"] = ["defuddle-extraction-failed", str(exc)]
        _write_json(output, Path("web-profile.json"), base)
        return base

    cleaned_html = normalize_text(str(extracted.get("content") or ""))
    markdown = normalize_text(str(extracted.get("contentMarkdown") or ""))
    title = str(extracted.get("title") or "").strip()
    markdown_headings = {
        match.group(1).strip().casefold()
        for match in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", markdown)
    }
    if title and title.casefold() not in markdown_headings:
        markdown = normalize_text(f"# {title}\n\n{markdown}")
    parse_time = extracted.get("parseTime", 0)
    base["parse_time_ms"] = parse_time if isinstance(parse_time, (int, float)) else 0
    if len(re.sub(r"\s+", "", markdown)) < 20:
        base["status"] = "extraction-insufficient"
        base["warnings"] = ["dynamic-or-empty-page-source-preserved"]
        _write_json(output, Path("metadata.json"), {key: extracted.get(key) for key in (
            "title", "author", "description", "domain", "published", "site", "wordCount", "parseTime"
        )})
        _write_json(output, Path("web-profile.json"), base)
        return base

    _write_text(output, Path("cleaned.html"), cleaned_html)
    _write_text(output, Path("content.md"), markdown)
    metadata = {key: extracted.get(key) for key in (
        "title", "author", "description", "domain", "published", "site", "language", "image",
        "wordCount", "parseTime", "schemaOrgData",
    )}
    _write_json(output, Path("metadata.json"), metadata)
    profile = profile_document_text(markdown, "content.md", task)
    complex_html_table = bool(re.search(r"(?is)<t(?:able|h|d)\b[^>]*(?:rowspan|colspan)\s*=", cleaned_html))
    warnings = list(profile["warnings"])
    route = str(profile["route"])
    if complex_html_table:
        route = "hybrid"
        if "visual-verification-required" not in warnings:
            warnings.append("visual-verification-required")
    original_tokens = int(base["original_estimated_tokens"])
    markdown_tokens = estimate_tokens(markdown)
    base.update({
        "status": "ok",
        "route": route,
        "cleaned_html_bytes": len(cleaned_html.encode("utf-8")),
        "markdown_bytes": len(markdown.encode("utf-8")),
        "markdown_estimated_tokens": markdown_tokens,
        "estimated_reduction_ratio": round(max(0.0, (original_tokens - markdown_tokens) / original_tokens), 4) if original_tokens else 0.0,
        "protected_facts": list(extract_protected_facts(markdown)),
        "visual_evidence": profile["visual_evidence"],
        "warnings": warnings,
    })
    _write_json(output, Path("web-profile.json"), base)
    return base


def _table_profiles(text: str) -> list[dict[str, object]]:
    """Describe Markdown tables conservatively without claiming visual fidelity."""

    lines = text.splitlines()
    tables: list[dict[str, object]] = []
    index = 0
    while index < len(lines) - 1:
        if "|" not in lines[index] or not re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1]):
            index += 1
            continue
        start = index
        block = [lines[index], lines[index + 1]]
        index += 2
        while index < len(lines) and "|" in lines[index] and lines[index].strip():
            block.append(lines[index])
            index += 1
        column_count = max(0, len([cell for cell in block[0].strip().strip("|").split("|")]))
        nearby = "\n".join(lines[max(0, start - 2):min(len(lines), index + 1)])
        complex_table = column_count >= 6 or len(block) >= 18 or bool(COMPLEX_TABLE_RE.search(nearby))
        source_visual = SOURCE_VISUAL_RE.search(nearby)
        tables.append({
            "anchor": f"table-{len(tables) + 1}",
            "columns": column_count,
            "rows": max(0, len(block) - 2),
            "complex": complex_table,
            "source_visual": source_visual.group(1).strip() if source_visual else None,
        })
    return tables


def _visual_relevance(alt: str, target: str, query: str) -> int:
    haystack = f"{alt} {target}".lower()
    return sum(3 for term in set(_query_terms(query)) if term in haystack) + (2 if INFORMATIVE_VISUAL_RE.search(haystack) else 0)


def profile_document_text(text: str, source: str, query: str = "") -> dict[str, object]:
    """Profile text, tables, and visual references without executing vision."""

    visuals: list[tuple[str, str]] = [(match.group(1).strip(), match.group(2).strip()) for match in MARKDOWN_IMAGE_RE.finditer(text)]
    visuals.extend((match.group(2) or "", match.group(1)) for match in HTML_IMAGE_RE.finditer(text))
    seen_targets: set[str] = set()
    evidence: list[dict[str, object]] = []
    decorative = 0
    duplicates = 0
    for position, (alt, target) in enumerate(visuals, 1):
        normalized_target = target.strip().casefold()
        label = f"{alt} {target}"
        if normalized_target in seen_targets:
            duplicates += 1
            continue
        seen_targets.add(normalized_target)
        if DECORATIVE_VISUAL_RE.search(label) and not INFORMATIVE_VISUAL_RE.search(label):
            decorative += 1
            continue
        evidence.append({
            "anchor": f"{source}#image-{position}",
            "source": source,
            "target": target,
            "alt": alt,
            "reason": "informative-label" if INFORMATIVE_VISUAL_RE.search(label) else "unclassified-visual",
            "relevance_score": _visual_relevance(alt, target, query),
            "status": "pending-vision",
        })
    tables = _table_profiles(text)
    complex_tables = sum(1 for table in tables if table["complex"])
    warnings: list[str] = []
    if complex_tables:
        warnings.append("visual-verification-required" if any(table["source_visual"] for table in tables if table["complex"]) else "complex-table-source-visual-unavailable")
    route = "hybrid" if evidence or complex_tables else "text"
    return {
        "source": source,
        "route": route,
        "vision_executed": False,
        "visuals_detected": len(visuals),
        "informative_visuals": len(evidence),
        "decorative_visuals_skipped": decorative,
        "duplicate_visuals_skipped": duplicates,
        "tables_detected": len(tables),
        "complex_tables": complex_tables,
        "tables": tables,
        "visual_evidence": evidence,
        "warnings": warnings,
    }


def profile_inputs(
    inputs: Sequence[Path | str], query: str, output_dir: Path | str, visual_budget: int = 4,
) -> dict[str, object]:
    """Write a deterministic routing profile and a bounded pending-vision queue."""

    if visual_budget < 0:
        raise ValueError("visual_budget must be non-negative")
    output_root = Path(output_dir).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    documents: list[dict[str, object]] = []
    original_assets: list[dict[str, object]] = []
    for value in inputs:
        path = Path(value).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        raw = path.read_bytes()
        original_assets.append({"name": path.name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        if path.suffix.lower() == ".pdf":
            page_markers = len(re.findall(rb"/Type\s*/Page\b", raw))
            documents.append({
                "source": path.name, "route": "source", "vision_executed": False,
                "visuals_detected": None, "informative_visuals": None,
                "decorative_visuals_skipped": 0, "duplicate_visuals_skipped": 0,
                "tables_detected": None, "complex_tables": None, "visual_evidence": [],
                "warnings": ["binary-pdf-needs-conversion-adapter", "page-images-and-layout-not-profiled"],
                "pages_estimated": page_markers or None,
            })
        elif path.suffix.lower() in CORE_SUFFIXES:
            documents.append(profile_document_text(_canonicalize(path), path.name, query))
        else:
            documents.append({
                "source": path.name, "route": "source", "vision_executed": False,
                "visuals_detected": None, "informative_visuals": None,
                "decorative_visuals_skipped": 0, "duplicate_visuals_skipped": 0,
                "tables_detected": None, "complex_tables": None, "visual_evidence": [],
                "warnings": ["unsupported-binary-needs-conversion-adapter"],
            })
    route_order = {"text": 0, "hybrid": 1, "source": 2}
    recommended = max((str(document["route"]) for document in documents), key=route_order.get, default="text")
    candidates = [item for document in documents for item in document.get("visual_evidence", [])]
    candidates.sort(key=lambda item: (-int(item["relevance_score"]), str(item["anchor"])))
    selected = candidates[:visual_budget]
    deferred = candidates[visual_budget:]
    queue = {
        "vision_executed": False,
        "visual_budget": visual_budget,
        "selected_count": len(selected),
        "deferred_count": len(deferred),
        "items": selected,
        "deferred": deferred,
        "instruction": "Inspect selected items with an available image-capable host and append anchored observations; otherwise leave pending.",
    }
    payload = {
        "schema_version": 1,
        "recommended_route": recommended,
        "vision_executed": False,
        "documents": documents,
        "original_assets": original_assets,
        "visual_queue": {"selected": len(selected), "deferred": len(deferred)},
    }
    _write_json(output_root, Path("profile.json"), payload)
    _write_json(output_root, Path("visual-evidence.json"), queue)
    return payload


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


def _prompt_unit_key(line: str, mode: str) -> str:
    key = line.strip()
    if mode == "exact":
        return key
    key = re.sub(r"^#{1,6}\s+", "", key)
    key = re.sub(r"^(?:[-*+]|•)\s+", "", key)
    key = re.sub(r"\s+", " ", key)
    key = re.sub(r"[.!?。！？]+$", "", key)
    return key.casefold()


def compile_prompt(text: str, mode: str = "exact") -> tuple[str, PromptCompileResult]:
    """Remove exact or structural duplicate lines without semantic rewriting."""

    if mode not in {"exact", "structural"}:
        raise ValueError("prompt mode must be exact or structural; semantic mode requires an external evaluator")

    normalized = normalize_text(text)
    seen: set[str] = set()
    kept: list[str] = []
    removed = 0
    for line in normalized.splitlines():
        key = _prompt_unit_key(line, mode)
        if key and key in seen:
            removed += 1
            continue
        if key:
            seen.add(key)
        kept.append(line)
    compiled = normalize_text("\n".join(kept))
    facts = extract_protected_facts(normalized)
    retained = sum(1 for fact in facts if fact in compiled)
    result = PromptCompileResult(
        mode=mode,
        method="exact-line-deduplication" if mode == "exact" else "format-normalized-line-deduplication",
        source_tokens=estimate_tokens(normalized),
        compiled_tokens=estimate_tokens(compiled),
        duplicate_units_removed=removed,
        protected_facts=len(facts),
        protected_fact_recall=1.0 if not facts else round(retained / len(facts), 4),
    )
    return compiled, result


def score_pdf_fidelity(expected: dict[str, object], markdown: str) -> dict[str, object]:
    """Score literal PDF-to-Markdown fidelity against declared ground truth."""

    categories = {
        "required_text": [str(value) for value in expected.get("required_text", [])],
        "numeric_facts": [str(value) for value in expected.get("numeric_facts", [])],
        "table_cells": [str(value) for value in expected.get("table_cells", [])],
    }
    missing = {name: [value for value in values if value not in markdown] for name, values in categories.items()}
    pages = int(expected.get("pages", 0))
    anchors = {int(value) for value in re.findall(r"<!--\s*page:\s*(\d+)\s*-->", markdown, re.I)}
    missing_pages = [str(page) for page in range(1, pages + 1) if page not in anchors]
    missing["page_anchors"] = missing_pages

    def recall(name: str) -> float:
        total = len(categories[name])
        return 1.0 if not total else round((total - len(missing[name])) / total, 4)

    return {
        "required_text_recall": recall("required_text"),
        "numeric_fact_recall": recall("numeric_facts"),
        "table_cell_recall": recall("table_cells"),
        "page_anchor_coverage": 1.0 if not pages else round((pages - len(missing_pages)) / pages, 4),
        "declared": {name: len(values) for name, values in categories.items()} | {"pages": pages},
        "missing": missing,
        "claim_boundary": "Literal declared-item recall; not visual or semantic equivalence.",
    }


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
    visual_budget: int = 4,
    prompt_text: str = "",
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

    profile = profile_inputs(resolved_inputs, query, output_root, visual_budget)

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

    visual_queue = json.loads((output_root / "visual-evidence.json").read_text(encoding="utf-8"))
    canonical_bytes = sum((output_root / "canon" / name).stat().st_size for name in canonical_names)
    original_bytes = sum(int(asset["bytes"]) for asset in profile["original_assets"])
    protocol_tokens = estimate_tokens(_context_pack_markdown(query, mode, budget_tokens, [], []))
    prompt_tokens = estimate_tokens(prompt_text or query)
    cost_ledger = {
        "schema_version": 1,
        "measurement_status": "estimated-not-provider-telemetry",
        "original_assets": {
            "count": len(profile["original_assets"]),
            "bytes": original_bytes,
            "items": profile["original_assets"],
        },
        "canonical_text": {
            "bytes": canonical_bytes,
            "estimated_tokens": source_tokens,
            "byte_reduction_ratio": 0 if not original_bytes else round(1 - canonical_bytes / original_bytes, 4),
            "warning": "Byte reduction is not token reduction.",
        },
        "prompt_and_protocol": {
            "task_prompt_estimated_tokens": prompt_tokens,
            "protocol_floor_estimated_tokens": protocol_tokens,
            "warning": "Prompt estimates are not provider billing telemetry.",
        },
        "selected_text_evidence": {
            "chunks": len(selected),
            "estimated_tokens": sum(chunk.token_estimate for chunk in selected),
        },
        "visual_routing": {
            "route": profile["recommended_route"],
            "selected_items": visual_queue["selected_count"],
            "deferred_items": visual_queue["deferred_count"],
            "vision_executed": False,
            "image_tokens": None,
            "warning": "Image-token cost requires the selected model, detail level, dimensions, and provider telemetry or a documented calculator.",
        },
        "final_context": {
            "budget_estimated_tokens": budget_tokens,
            "packed_estimated_tokens": packed_tokens,
            "canonical_to_pack_reduction_ratio": 0 if not source_tokens else round(1 - packed_tokens / source_tokens, 4),
        },
    }
    _write_json(output_root, Path("context-cost-ledger.json"), cost_ledger)

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
        f"- Document route: `{profile['recommended_route']}`",
        f"- Visual evidence selected/deferred: {visual_queue['selected_count']}/{visual_queue['deferred_count']}",
        f"- Original/canonical bytes: {original_bytes}/{canonical_bytes} (not a token comparison)",
        f"- Task prompt tokens (estimated): {prompt_tokens}",
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
        if case.get("kind") == "profile":
            profiled = profile_inputs(inputs, str(case.get("task", "")), case_output, int(case.get("visual_budget", 4)))
            documents = profiled["documents"]
            actual_route = str(profiled["recommended_route"])
            informative = sum(int(item.get("informative_visuals") or 0) for item in documents)
            decorative = sum(int(item.get("decorative_visuals_skipped") or 0) for item in documents)
            duplicates = sum(int(item.get("duplicate_visuals_skipped") or 0) for item in documents)
            complex_tables = sum(int(item.get("complex_tables") or 0) for item in documents)
            checks = {
                "route_correct": actual_route == str(case["expected_route"]) if "expected_route" in case else None,
                "informative_visual_count_correct": informative == int(case["expected_informative_visuals"]) if "expected_informative_visuals" in case else None,
                "decorative_skip_count_correct": decorative == int(case["expected_decorative_skips"]) if "expected_decorative_skips" in case else None,
                "duplicate_skip_count_correct": duplicates == int(case["expected_duplicate_skips"]) if "expected_duplicate_skips" in case else None,
                "table_risk_count_correct": complex_tables == int(case["expected_complex_tables"]) if "expected_complex_tables" in case else None,
            }
            failures = [name.replace("_correct", "-mismatch") for name, value in checks.items() if value is False]
            results.append({
                "id": case_id, "kind": "profile", "profile": str(case.get("profile", "multimodal-routing")),
                "source_tokens": 0, "packed_tokens": 0, "savings_ratio": 0, "budget_compliant": None,
                "protected_fact_recall": None, "protected_facts_retained": 0, "protected_facts_declared": 0,
                "anchor_correctness": None, "anchors_retained": 0, "anchors_declared": 0,
                "route": actual_route, "visual_counts_correct": all(value for value in checks.values() if value is not None),
                "informative_visuals": informative, "decorative_skips": decorative,
                "duplicate_skips": duplicates, "complex_tables": complex_tables,
                **checks, "failures": failures,
            })
            continue
        if case.get("kind") == "prompt":
            source = "\n".join(path.read_text(encoding="utf-8") for path in inputs)
            prompt_mode = str(case.get("prompt_mode", "exact"))
            compiled, prompt_result = compile_prompt(source, prompt_mode)
            expected_facts = [str(value) for value in case.get("protected_facts", [])]
            retained_facts = sum(1 for value in expected_facts if value in compiled)
            failures: list[str] = []
            expected_removed = case.get("expected_duplicate_units_removed")
            if expected_removed is not None and prompt_result.duplicate_units_removed != int(expected_removed):
                failures.append("prompt-duplicate-count-mismatch")
            if retained_facts < len(expected_facts):
                failures.append("protected-fact-missing")
            results.append({
                "id": case_id,
                "kind": "prompt",
                "profile": str(case.get("profile", "prompt")),
                "source_tokens": prompt_result.source_tokens,
                "packed_tokens": prompt_result.compiled_tokens,
                "savings_ratio": 0 if not prompt_result.source_tokens else round(1 - prompt_result.compiled_tokens / prompt_result.source_tokens, 4),
                "budget_compliant": True,
                "protected_fact_recall": 1 if not expected_facts else round(retained_facts / len(expected_facts), 4),
                "protected_facts_retained": retained_facts,
                "protected_facts_declared": len(expected_facts),
                "anchor_correctness": None,
                "anchors_retained": 0,
                "anchors_declared": 0,
                "duplicate_units_removed": prompt_result.duplicate_units_removed,
                "prompt_mode": prompt_result.mode,
                "prompt_method": prompt_result.method,
                "failures": failures,
            })
            continue
        built = build_pack(inputs, str(case["task"]), int(case["budget"]), case_output)
        pack = (case_output / "packs" / "current-task.context.md").read_text(encoding="utf-8")
        document_profile = json.loads((case_output / "profile.json").read_text(encoding="utf-8"))
        documents = document_profile["documents"]
        actual_route = str(document_profile["recommended_route"])
        informative = sum(int(item.get("informative_visuals") or 0) for item in documents)
        decorative = sum(int(item.get("decorative_visuals_skipped") or 0) for item in documents)
        duplicates = sum(int(item.get("duplicate_visuals_skipped") or 0) for item in documents)
        complex_tables = sum(int(item.get("complex_tables") or 0) for item in documents)
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
        route_correct = None if "expected_route" not in case else actual_route == str(case["expected_route"])
        visual_checks = []
        detailed_checks: dict[str, bool | None] = {}
        for expected_key, actual in (
            ("expected_informative_visuals", informative),
            ("expected_decorative_skips", decorative),
            ("expected_duplicate_skips", duplicates),
            ("expected_complex_tables", complex_tables),
        ):
            if expected_key in case:
                is_correct = actual == int(case[expected_key])
                visual_checks.append(is_correct)
                detailed_checks[{
                    "expected_informative_visuals": "informative_visual_count_correct",
                    "expected_decorative_skips": "decorative_skip_count_correct",
                    "expected_duplicate_skips": "duplicate_skip_count_correct",
                    "expected_complex_tables": "table_risk_count_correct",
                }[expected_key]] = is_correct
        visual_counts_correct = None if not visual_checks else all(visual_checks)
        if route_correct is False:
            failures.append("route-mismatch")
        if visual_counts_correct is False:
            failures.append("visual-count-mismatch")
        results.append({
            "id": case_id,
            "kind": str(case.get("kind", "context")),
            "profile": str(case.get("profile", "correctness")),
            "source_tokens": built.source_tokens,
            "packed_tokens": built.packed_tokens,
            "savings_ratio": 0 if not built.source_tokens else round(1 - built.packed_tokens / built.source_tokens, 4),
            "budget_compliant": built.packed_tokens <= int(case["budget"]),
            "protected_fact_recall": 1 if not expected_facts else round(retained_facts / len(expected_facts), 4),
            "protected_facts_retained": retained_facts,
            "protected_facts_declared": len(expected_facts),
            "anchor_correctness": 1 if not expected_anchors else round(retained_anchors / len(expected_anchors), 4),
            "anchors_retained": retained_anchors,
            "anchors_declared": len(expected_anchors),
            "route": actual_route,
            "route_correct": route_correct,
            "visual_counts_correct": visual_counts_correct,
            "informative_visuals": informative,
            "decorative_skips": decorative,
            "duplicate_skips": duplicates,
            "complex_tables": complex_tables,
            **detailed_checks,
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
    _write_public_metrics(output_root, manifest, results, summary_payload)
    return summary


def prune_benchmark_artifacts(output_dir: Path | str) -> bool:
    """Remove reproducible per-case artifacts while retaining public result files."""

    output_root = Path(output_dir).expanduser().resolve()
    artifacts = (output_root / "artifacts").resolve()
    try:
        artifacts.relative_to(output_root)
    except ValueError as error:
        raise ValueError("benchmark artifact path escapes output directory") from error
    if artifacts.is_dir():
        shutil.rmtree(artifacts)
        return True
    return False


def _rate(results: Sequence[dict[str, object]], field: str, predicate=None) -> dict[str, object]:
    eligible = [item for item in results if item.get(field) is not None and (predicate is None or predicate(item))]
    numerator = sum(1 for item in eligible if item.get(field) is True or item.get(field) == 1)
    return {"value": None if not eligible else round(numerator / len(eligible), 4), "numerator": numerator, "denominator": len(eligible)}


def _mean_score(results: Sequence[dict[str, object]], field: str) -> dict[str, object]:
    eligible = [float(item[field]) for item in results if item.get(field) is not None]
    return {"value": None if not eligible else round(sum(eligible) / len(eligible), 4), "denominator": len(eligible)}


def _declared_recall(results: Sequence[dict[str, object]], retained_field: str, declared_field: str) -> dict[str, object]:
    denominator = sum(int(item.get(declared_field, 0)) for item in results)
    numerator = sum(int(item.get(retained_field, 0)) for item in results)
    return {"value": None if not denominator else round(numerator / denominator, 4), "numerator": numerator, "denominator": denominator}


def _percent(rate: dict[str, object]) -> str:
    value = rate.get("value")
    return "Pending" if value is None else f"{float(value) * 100:.1f}% ({rate.get('numerator', 'n/a')}/{rate['denominator']})"


def _write_public_metrics(
    output_root: Path, manifest: dict[str, object], results: Sequence[dict[str, object]], summary: dict[str, object],
) -> None:
    context_results = [item for item in results if item.get("kind") == "context"]
    efficiency_results = [item for item in context_results if item.get("profile") in {"correctness", "efficiency"}]
    routing_results = [item for item in results if item.get("kind") in {"context", "profile"}]
    prompt_results = [item for item in results if item.get("kind") == "prompt"]
    budget_rate = _rate(context_results, "budget_compliant")
    route_rate = _rate(routing_results, "route_correct")
    visual_rate = _rate(routing_results, "visual_counts_correct")
    informative_rate = _rate(routing_results, "informative_visual_count_correct")
    decorative_rate = _rate(routing_results, "decorative_skip_count_correct")
    duplicate_rate = _rate(routing_results, "duplicate_skip_count_correct")
    table_rate = _rate(routing_results, "table_risk_count_correct")
    fact_rate = _declared_recall(results, "protected_facts_retained", "protected_facts_declared")
    anchor_rate = _declared_recall(context_results, "anchors_retained", "anchors_declared")
    prompt_source = sum(int(item["source_tokens"]) for item in prompt_results)
    prompt_final = sum(int(item["packed_tokens"]) for item in prompt_results)
    prompt_modes = {}
    for mode in ("exact", "structural"):
        mode_results = [item for item in prompt_results if item.get("prompt_mode", "exact") == mode]
        mode_source = sum(int(item["source_tokens"]) for item in mode_results)
        mode_final = sum(int(item["packed_tokens"]) for item in mode_results)
        prompt_modes[mode] = {
            "cases": len(mode_results),
            "source_estimated_tokens": mode_source,
            "compiled_estimated_tokens": mode_final,
            "reduction_ratio": 0 if not mode_source else round(1 - mode_final / mode_source, 4),
            "duplicate_units_removed": sum(int(item.get("duplicate_units_removed", 0)) for item in mode_results),
        }
    context_source = sum(int(item["source_tokens"]) for item in efficiency_results)
    context_final = sum(int(item["packed_tokens"]) for item in efficiency_results)
    pdf_metrics_path = output_root.parent / "pdf" / "results" / "metrics.json"
    pdf_metrics = json.loads(pdf_metrics_path.read_text(encoding="utf-8")) if pdf_metrics_path.is_file() else None
    metrics = {
        "schema_version": 1,
        "dataset": manifest.get("dataset", "unnamed"),
        "generated_from_cases": len(results),
        "measurement_labels": {"text_tokens": "estimated", "provider_tokens": "pending"},
        "context_efficiency": {
            "source_estimated_tokens": context_source,
            "final_estimated_tokens": context_final,
            "reduction_ratio": 0 if not context_source else round(1 - context_final / context_source, 4),
            "profiles": {name: value for name, value in summary["profiles"].items() if name in {"correctness", "efficiency"}},
        },
        "prompt_efficiency": {
            "cases": len(prompt_results),
            "source_estimated_tokens": prompt_source,
            "compiled_estimated_tokens": prompt_final,
            "reduction_ratio": 0 if not prompt_source else round(1 - prompt_final / prompt_source, 4),
            "duplicate_units_removed": sum(int(item.get("duplicate_units_removed", 0)) for item in prompt_results),
            **prompt_modes,
            "semantic": "disabled-pending-equivalence-evaluation",
        },
        "generated_pdf_fidelity": pdf_metrics,
        "fidelity": {
            "protected_fact_recall": fact_rate,
            "anchor_correctness": anchor_rate,
            "route_accuracy": route_rate,
            "visual_filtering_accuracy": visual_rate,
            "informative_visual_count_accuracy": informative_rate,
            "decorative_skip_accuracy": decorative_rate,
            "duplicate_skip_accuracy": duplicate_rate,
            "table_risk_gate_accuracy": table_rate,
            "budget_compliance": budget_rate,
        },
        "pending": {
            "real_world_pdf_corpus_fidelity": "pending-real-corpus",
            "provider_input_token_telemetry": "pending-api-run",
            "vision_description_accuracy": "pending-human-labels-and-model-run",
            "downstream_blind_answer_quality": "pending-blind-evaluation",
        },
        "claim_boundary": "No overall fidelity score and no cross-project superiority claim.",
    }
    _write_json(output_root, Path("metrics.json"), metrics)
    efficiency = metrics["context_efficiency"]
    prompt = metrics["prompt_efficiency"]
    lines = [
        "# TIKAZ Context Economy — Reproducible Evidence",
        "",
        f"Dataset: `{metrics['dataset']}` · Cases: **{len(results)}** · Text counts: **estimated, not provider billing telemetry**.",
        "",
        "## Evidence card",
        "",
        "| Metric | Result | Evidence boundary |",
        "|---|---:|---|",
        f"| Context reduction | {float(efficiency['reduction_ratio']) * 100:.1f}% ({efficiency['source_estimated_tokens']} → {efficiency['final_estimated_tokens']} estimated tokens) | Aggregate; inspect profiles because short inputs may grow |",
        f"| Prompt exact-repeat reduction | {float(prompt['exact']['reduction_ratio']) * 100:.1f}% ({prompt['exact']['source_estimated_tokens']} → {prompt['exact']['compiled_estimated_tokens']}) | {prompt['exact']['cases']} prompt cases; literal duplicate lines only |",
        f"| Prompt structural-repeat reduction | {float(prompt['structural']['reduction_ratio']) * 100:.1f}% ({prompt['structural']['source_estimated_tokens']} → {prompt['structural']['compiled_estimated_tokens']}) | {prompt['structural']['cases']} cases; formatting-normalized detection, first wording retained |",
        f"| Protected-fact recall | {_percent(fact_rate)} | Literal declared facts only |",
        f"| Anchor correctness | {_percent(anchor_rate)} | Declared expected anchors only |",
        f"| Route accuracy | {_percent(route_rate)} | Text / Hybrid / Source labeled cases |",
        f"| Visual filtering accuracy | {_percent(visual_rate)} | Informative, decorative, duplicate, and table-risk counts |",
        f"| └ Informative-visual count | {_percent(informative_rate)} | Human-declared synthetic cases |",
        f"| └ Decorative-image skips | {_percent(decorative_rate)} | Human-declared synthetic cases |",
        f"| └ Duplicate-image skips | {_percent(duplicate_rate)} | Human-declared synthetic cases |",
        f"| └ Complex-table risk gate | {_percent(table_rate)} | Human-declared synthetic cases |",
        f"| Budget compliance | {_percent(budget_rate)} | Complete generated packs |",
        "",
        "## Profile results",
        "",
        "| Profile | Cases | Source | Final | Reduction | Passed |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, profile in sorted(efficiency["profiles"].items()):
        lines.append(f"| {name} | {profile['cases']} | {profile['source_tokens']} | {profile['packed_tokens']} | {float(profile['savings_ratio']) * 100:.1f}% | {profile['passed']}/{profile['cases']} |")
    lines.extend([
        "",
        "## Pending — not yet claimed",
        "",
        f"- Generated PDF literal fidelity: **{'available in `../pdf/results/metrics.json`' if pdf_metrics else 'Pending'}**",
        "- Real-world PDF corpus fidelity: **Pending**",
        "- Actual provider input-token savings: **Pending**",
        "- Vision-description accuracy: **Pending**",
        "- Downstream blind-answer quality: **Pending**",
        "",
        "## Reproduce",
        "",
        "```powershell",
        "python scripts/tikaz_context.py benchmark --manifest benchmarks/manifest.json --output benchmarks/results --prune-artifacts",
        "```",
        "",
        "Raw evidence: [`metrics.json`](metrics.json) · [`cases.json`](cases.json) · [`summary.json`](summary.json)",
        "",
        "> There is no overall fidelity score. Percentages describe separate, declared checks and include their sample counts.",
        "",
    ])
    _write_text(output_root, Path("README.md"), "\n".join(lines))


def doctor_report(document_converter: Path | str | None = None) -> dict[str, object]:
    """Report core and optional local capabilities without changing the environment."""

    tokenizer = next((name for name in ("tiktoken", "tokenizers") if importlib.util.find_spec(name)), None)
    explicit_converter = Path(document_converter).expanduser().resolve() if document_converter else None
    if explicit_converter and not explicit_converter.is_file():
        raise FileNotFoundError(explicit_converter)
    converter = str(explicit_converter) if explicit_converter else (shutil.which("markitdown") or shutil.which("pandoc"))
    web_available, web_node, web_version = _defuddle_available()
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
            "pdf_support": "unverified" if converter else "unavailable",
            "required": False,
            "note": "Command discovery does not prove PDF capability; run a fixture conversion before claiming support.",
        },
        "web_extractor": {
            "available": web_available,
            "provider": "defuddle",
            "version": web_version,
            "node_command": web_node,
            "required": False,
            "note": "Optional webpage-only adapter; discovery never installs dependencies.",
        },
        "installed_anything": False,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tikaz-context",
        description="Build deterministic TIKAZ Context Economy artifacts.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    pack = subparsers.add_parser("pack", help="Build a context pack from canonical Markdown or text.")
    pack.add_argument("--input", action="append", required=True, dest="inputs")
    pack.add_argument("--query", required=True)
    pack.add_argument("--budget", required=True, type=int, dest="budget_tokens")
    pack.add_argument("--output", required=True, dest="output_dir")
    pack.add_argument("--visual-budget", type=int, default=4)
    pack.add_argument("--prompt-text", default="")
    profile = subparsers.add_parser("profile", help="Profile document fidelity and build a pending visual-evidence queue.")
    profile.add_argument("--input", action="append", required=True, dest="inputs")
    profile.add_argument("--query", default="")
    profile.add_argument("--visual-budget", type=int, default=4)
    profile.add_argument("--output", required=True, dest="output_dir")
    snapshot = subparsers.add_parser("validate-snapshot", help="Validate a conversation state snapshot.")
    snapshot.add_argument("--snapshot", required=True)
    snapshot.add_argument("--source", required=True)
    checkpoint = subparsers.add_parser("checkpoint", help="Create a conservative conversation checkpoint.")
    checkpoint.add_argument("--source", required=True)
    checkpoint.add_argument("--output", required=True)
    audit = subparsers.add_parser("audit", help="Run a read-only heuristic Context Health audit.")
    audit.add_argument("--input", required=True)
    audit.add_argument("--task", default="")
    doctor = subparsers.add_parser("doctor", help="Report core and optional local capabilities without installation.")
    doctor.add_argument("--document-converter")
    web = subparsers.add_parser("web", help="Extract webpage content with the optional Defuddle adapter.")
    web_source = web.add_mutually_exclusive_group(required=True)
    web_source.add_argument("--input", dest="input_path")
    web_source.add_argument("--url")
    web.add_argument("--task", default="")
    web.add_argument("--output", required=True, dest="output_dir")
    web.add_argument("--adapter-dir")
    web.add_argument("--node-command")
    web.add_argument("--timeout", type=float, default=15.0)
    web.add_argument("--max-bytes", type=int, default=5_000_000)
    prompt = subparsers.add_parser("prompt", help="Remove exact or structural prompt repetition without semantic rewriting.")
    prompt.add_argument("--input", required=True)
    prompt.add_argument("--mode", choices=("exact", "structural"), default="exact")
    prompt.add_argument("--output", required=True)
    pdf_fidelity = subparsers.add_parser("pdf-fidelity", help="Score converted Markdown against declared PDF ground truth.")
    pdf_fidelity.add_argument("--expected", required=True)
    pdf_fidelity.add_argument("--markdown", required=True)
    pdf_fidelity.add_argument("--output", required=True)
    benchmark = subparsers.add_parser("benchmark", help="Run a versioned local benchmark manifest.")
    benchmark.add_argument("--manifest", default=str(DEFAULT_BENCHMARK_MANIFEST))
    benchmark.add_argument("--output", required=True)
    benchmark.add_argument("--prune-artifacts", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "pack":
        result = build_pack(
            args.inputs, args.query, args.budget_tokens, args.output_dir,
            visual_budget=args.visual_budget, prompt_text=args.prompt_text,
        )
        print(json.dumps(result._asdict(), ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "profile":
        result = profile_inputs(args.inputs, args.query, args.output_dir, args.visual_budget)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
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
        print(json.dumps(doctor_report(args.document_converter), ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "web":
        result = extract_web_content(
            input_path=args.input_path, url=args.url, task=args.task, output_dir=args.output_dir,
            adapter_dir=args.adapter_dir, node_command=args.node_command,
            timeout=args.timeout, max_bytes=args.max_bytes,
        )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "ok" else 2
    if args.command == "prompt":
        source = Path(args.input).read_text(encoding="utf-8")
        compiled, result = compile_prompt(source, args.mode)
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(compiled, encoding="utf-8", newline="\n")
        print(json.dumps(result._asdict(), ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "pdf-fidelity":
        expected = json.loads(Path(args.expected).read_text(encoding="utf-8"))
        markdown = Path(args.markdown).read_text(encoding="utf-8")
        report = score_pdf_fidelity(expected, markdown)
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "benchmark":
        result = run_benchmark(args.manifest, args.output)
        if args.prune_artifacts:
            prune_benchmark_artifacts(args.output)
        print(json.dumps(result._asdict(), ensure_ascii=False, sort_keys=True))
        return 0 if result.failed_cases == 0 else 1
    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
