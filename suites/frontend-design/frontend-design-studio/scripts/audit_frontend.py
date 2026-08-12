#!/usr/bin/env python3
'''Run dependency-free heuristic checks over frontend source files.'''

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


EXTENSIONS = {'.html', '.htm', '.css', '.scss', '.sass', '.less', '.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte', '.astro', '.mdx'}
SKIP_DIRS = {'.git', '.next', '.nuxt', '.output', '.turbo', 'build', 'coverage', 'dist', 'node_modules', 'target', 'vendor'}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', help='Frontend project directory')
    parser.add_argument('--json', action='store_true', help='Emit JSON')
    parser.add_argument('--strict', action='store_true', help='Exit 1 on warnings')
    return parser.parse_args()


def source_files(root: Path):
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        try:
            if path.stat().st_size <= 2_000_000:
                yield path
        except OSError:
            continue


def line_at(text: str, offset: int) -> int:
    return text.count('\n', 0, offset) + 1


def matches(findings, root, path, text, pattern, code, message, flags=0):
    for match in re.finditer(pattern, text, flags):
        findings.append(Finding('warning', code, path.relative_to(root).as_posix(), line_at(text, match.start()), message))


def audit(root: Path, path: Path, text: str, findings: list[Finding]) -> None:
    suffix = path.suffix.lower()
    matches(findings, root, path, text, r'lorem\s+ipsum', 'placeholder-copy', 'Replace placeholder copy.', re.I)
    matches(findings, root, path, text, r'\b(?:Acme|SmartFlow|Cloudly)\b', 'generic-brand-copy', 'Verify this is real product copy, not a generic placeholder brand.', re.I)
    matches(findings, root, path, text, r'(?<![\w-])100vh(?![\w-])', 'legacy-vh', 'Review 100vh on mobile; 100dvh is usually safer.')
    matches(findings, root, path, text, r'(?<![\w-])h-screen(?![\w-])', 'tailwind-h-screen', 'Review h-screen on mobile; min-h-[100dvh] is usually safer.')
    matches(findings, root, path, text, r'\btransition-all\b', 'tailwind-transition-all', 'List intentional Tailwind transition properties instead of transition-all.')
    matches(findings, root, path, text, r'window\.addEventListener\s*\(\s*[\x22\x27]scroll[\x22\x27]', 'raw-scroll-listener', 'Use a scoped motion/scroll primitive or IntersectionObserver and clean it up.')
    matches(findings, root, path, text, r'(?:bg-clip-text[^\n\x22\x27>]{0,120}text-transparent|text-transparent[^\n\x22\x27>]{0,120}bg-clip-text)', 'gradient-text', 'Confirm gradient text is part of the approved visual world, not a generic AI styling default.', re.I)

    if suffix in {'.css', '.scss', '.sass', '.less', '.vue', '.svelte', '.astro'}:
        matches(findings, root, path, text, r'transition(?:-property)?\s*:[^;}]*(?:\btop\b|\bleft\b|\bwidth\b|\bheight\b)', 'layout-animation', 'Prefer transform or opacity for animation.', re.I)
        matches(findings, root, path, text, r'transition(?:-property)?\s*:\s*all\b', 'transition-all', 'List intentional transition properties instead of transition: all.', re.I)

    if suffix in {'.html', '.htm'} and re.search(r'<!doctype\b|<html\b|<head\b', text, re.I):
        relative = path.relative_to(root).as_posix()
        if not re.search(r'<title\b', text, re.I):
            findings.append(Finding('error', 'missing-title', relative, 1, 'Document has no title element.'))
        if not re.search(r'<meta\b[^>]*\bname\s*=\s*[\x22\x27]viewport', text, re.I):
            findings.append(Finding('error', 'missing-viewport', relative, 1, 'Document has no viewport meta tag.'))
        if not re.search(r'<meta\b[^>]*\bname\s*=\s*[\x22\x27]description', text, re.I):
            findings.append(Finding('warning', 'missing-description', relative, 1, 'Document has no meta description.'))

    if suffix in {'.html', '.htm', '.jsx', '.tsx', '.vue', '.svelte', '.astro', '.mdx'}:
        relative = path.relative_to(root).as_posix()
        for match in re.finditer(r'<img\b[^>]*>', text, re.I | re.S):
            if not re.search(r'(?:\balt|:alt|v-bind:alt)\s*=', match.group(0), re.I):
                findings.append(Finding('error', 'missing-alt', relative, line_at(text, match.start()), 'Image has no alt attribute or binding.'))


def main() -> int:
    args = parse_args()
    root = Path(args.project).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f'Project directory does not exist: {root}')

    findings: list[Finding] = []
    scanned = 0
    motion_found = False
    reduced_motion_found = False
    card_shell_hits = 0
    eyebrow_hits = 0
    for path in source_files(root):
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        scanned += 1
        audit(root, path, text, findings)
        card_shell_hits += len(re.findall(r'rounded-(?:lg|xl|2xl|3xl)[^\n\x22\x27>]{0,160}\bborder\b', text))
        eyebrow_hits += len(re.findall(r'\buppercase\b[^\n\x22\x27>]{0,120}\btracking-', text))
        if path.suffix.lower() in {'.css', '.scss', '.sass', '.less', '.vue', '.svelte', '.astro'}:
            motion_found = motion_found or bool(re.search(r'\b(animation|transition)\s*:', text))
            reduced_motion_found = reduced_motion_found or 'prefers-reduced-motion' in text

    if motion_found and not reduced_motion_found:
        findings.append(Finding('warning', 'reduced-motion', '.', 1, 'Project motion exists without a detected prefers-reduced-motion fallback.'))
    if card_shell_hits >= 6:
        findings.append(Finding('warning', 'repeated-card-shells', '.', 1, f'Detected {card_shell_hits} rounded+border card-shell patterns; review whether page sections became a component catalogue.'))
    if eyebrow_hits >= 4:
        findings.append(Finding('warning', 'repeated-eyebrows', '.', 1, f'Detected {eyebrow_hits} uppercase tracking-label patterns; review repetitive section grammar and visual clutter.'))

    findings.sort(key=lambda item: (item.path, item.line, item.code))
    payload = {'project': str(root), 'files_scanned': scanned, 'findings': [asdict(item) for item in findings]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f'Scanned {scanned} frontend source files; found {len(findings)} issue(s).')
        for item in findings:
            print(f'{item.path}:{item.line}: {item.severity} {item.code}: {item.message}')

    has_errors = any(item.severity == 'error' for item in findings)
    return 1 if has_errors or (args.strict and findings) else 0


if __name__ == '__main__':
    raise SystemExit(main())
