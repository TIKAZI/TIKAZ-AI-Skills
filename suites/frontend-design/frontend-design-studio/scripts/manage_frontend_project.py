#!/usr/bin/env python3
'''Initialize frontend workflow artifacts, update state, and enforce phase gates.'''

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any, Optional


STATE_PATH = Path('.design-frontend-studio') / 'state.json'


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def project_path(value: str) -> Path:
    project = Path(value).expanduser().resolve()
    if not project.is_dir():
        raise SystemExit(f'Project directory does not exist: {project}')
    return project


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except FileNotFoundError:
        raise SystemExit(f'Missing workflow state: {path}. Run init first.')
    except json.JSONDecodeError as error:
        raise SystemExit(f'Invalid JSON in {path}: {error}')


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def render_template(name: str, replacements: dict[str, str]) -> str:
    text = (skill_root() / 'assets' / name).read_text(encoding='utf-8')
    for token, value in replacements.items():
        text = text.replace(token, json.dumps(value, ensure_ascii=False))
    return text


def default_state(name: str) -> dict[str, Any]:
    return {
        'schema_version': 3,
        'project': name,
        'phase': 'intake',
        'brief': {
            'approved': False,
            'primary_user': '',
            'primary_action': '',
            'surface_mode': '',
            'scope_defined': False,
            'claims_resolved': False,
            'access_preflight_complete': False,
            'approval_evidence': '',
        },
        'research': {
            'complete': False,
            'evidence_kinds': [],
            'external_sources_required': True,
            'source_waiver_reason': '',
            'component_licenses_resolved': False,
        },
        'design': {'approved': False, 'contract_path': 'DESIGN.md', 'approval_evidence': ''},
        'implementation': {'complete': False, 'build_passed': False, 'build_evidence': '', 'revision': ''},
        'qa': {
            'acceptance_defined': False,
            'art_direction_proof_approved': False,
            'visual_scores': {
                'mode_success': 0,
                'hierarchy': 0,
                'composition': 0,
                'distinctiveness': 0,
                'coherence': 0,
                'content_media': 0,
                'responsive': 0,
                'interaction_craft': 0,
            },
            'blocker_open': 0,
            'major_open': 0,
            'desktop_rendered': False,
            'mobile_rendered': False,
            'keyboard_checked': False,
            'touch_checked': False,
            'reduced_motion_checked': False,
            'evidence_paths': [],
            'desktop_evidence_paths': [],
            'mobile_evidence_paths': [],
            'scorecard_evidence_path': '',
            'evidence_revision': '',
        },
        'deployment': {
            'mode': 'none',
            'target': '',
            'preview_url': '',
            'preview_approved': False,
            'preview_approval_evidence': '',
            'rollback_recorded': False,
            'production_url': '',
            'smoke_passed': False,
        },
        'learning': {
            'observation_complete': False,
            'acceptance_recorded': False,
            'evidence_recorded': False,
            'evidence_paths': [],
        },
        'history': [],
    }


def default_references() -> dict[str, Any]:
    return {'schema_version': 1, 'updated_at': None, 'sources': [], 'components': [], 'claims': []}


def migrate_state(state: dict[str, Any]) -> dict[str, Any]:
    defaults = default_state(str(state.get('project', 'frontend-project')))

    def fill(current: dict[str, Any], expected: dict[str, Any]) -> None:
        for key, value in expected.items():
            if key not in current:
                current[key] = value
            elif isinstance(value, dict) and isinstance(current[key], dict):
                fill(current[key], value)

    fill(state, defaults)
    state['schema_version'] = 3
    return state


def initialize(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    replacements = {
        '{{PROJECT_NAME}}': args.name,
        '{{PRODUCT_NAME}}': args.name,
        '{{SURFACE}}': args.surface,
        '{{PLATFORM}}': args.platform,
    }
    targets = {
        project / 'BRIEF.md': 'BRIEF.template.md',
        project / 'DESIGN.md': 'DESIGN.template.md',
        project / 'QA.md': 'QA.template.md',
    }
    created: list[str] = []
    skipped: list[str] = []
    for target, template in targets.items():
        if target.exists():
            skipped.append(str(target))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_template(template, replacements).replace('\r\n', '\n'), encoding='utf-8')
        created.append(str(target))
    json_targets = {
        project / STATE_PATH: default_state(args.name),
        project / '.design-frontend-studio' / 'references.json': default_references(),
    }
    for target, value in json_targets.items():
        if target.exists():
            skipped.append(str(target))
            continue
        write_json(target, value)
        created.append(str(target))
    print(json.dumps({'created': created, 'skipped_existing': skipped}, ensure_ascii=False, indent=2))
    return 0


def parse_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        stripped = value.strip()
        if stripped.startswith('[') and stripped.endswith(']'):
            inner = stripped[1:-1].strip()
            if not inner:
                return []
            return [item.strip().strip(chr(34)).strip(chr(39)) for item in inner.split(',')]
        return value


def set_nested(state: dict[str, Any], dotted_key: str, value: Any) -> None:
    keys = dotted_key.split('.')
    if any(not key for key in keys):
        raise SystemExit(f'Invalid key: {dotted_key}')
    current: dict[str, Any] = state
    for key in keys[:-1]:
        if key not in current:
            raise SystemExit(f'Unknown state key: {dotted_key}')
        child = current[key]
        if not isinstance(child, dict):
            raise SystemExit(f'Cannot descend through non-object key: {key}')
        current = child
    if keys[-1] not in current:
        raise SystemExit(f'Unknown state key: {dotted_key}')
    if dotted_key == 'phase':
        raise SystemExit('phase is controlled by gate/reopen commands and cannot be set directly')
    current[keys[-1]] = value


def update_state(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    path = project / STATE_PATH
    state = migrate_state(read_json(path))
    if args.key == 'deployment.mode' and state.get('phase') in {'production', 'closed'}:
        raise SystemExit('deployment.mode is locked after the production gate; use reopen before changing release mode')
    value = parse_value(args.value)
    set_nested(state, args.key, value)
    write_json(path, state)
    print(f'{args.key}={json.dumps(value, ensure_ascii=False)}')
    return 0


def get_value(state: dict[str, Any], dotted_key: str) -> Any:
    current: Any = state
    for key in dotted_key.split('.'):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def require(failures: list[str], state: dict[str, Any], key: str, predicate, message: str) -> None:
    value = get_value(state, key)
    if not predicate(value):
        failures.append(f'{key}: {message}')


def resolve_evidence_path(project: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (project / path).resolve()


def require_file(failures: list[str], project: Path, label: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        failures.append(f'{label}: evidence path is required')
        return
    path = resolve_evidence_path(project, value)
    if not path.is_file() or path.stat().st_size == 0:
        failures.append(f'{label}: file does not exist or is empty: {value}')


def require_files(failures: list[str], project: Path, label: str, values: Any) -> None:
    if not isinstance(values, list) or not values:
        failures.append(f'{label}: at least one evidence path is required')
        return
    for index, value in enumerate(values):
        require_file(failures, project, f'{label}[{index}]', value)


def require_media_files(failures: list[str], project: Path, label: str, values: Any) -> None:
    media_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.mp4', '.webm'}
    if not isinstance(values, list) or not values:
        failures.append(f'{label}: at least one screenshot or recording is required')
        return
    for index, value in enumerate(values):
        require_file(failures, project, f'{label}[{index}]', value)
        if isinstance(value, str) and Path(value).suffix.lower() not in media_extensions:
            failures.append(f'{label}[{index}]: evidence must be an image or video file')


def frontmatter_status(path: Path) -> Optional[str]:
    if not path.is_file() or path.stat().st_size == 0:
        return None
    text = path.read_text(encoding='utf-8-sig')
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == '---')
    except StopIteration:
        return None
    for line in lines[1:end]:
        match = re.match(r'^status\s*:\s*(.*?)\s*$', line, re.IGNORECASE)
        if match:
            return match.group(1).strip().strip(chr(34)).strip(chr(39)).lower()
    return None


def set_frontmatter_status(path: Path, status: str) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding='utf-8-sig')
    updated, count = re.subn(
        r'(?m)^(status\s*:\s*).+$',
        lambda match: f'{match.group(1)}{status}',
        text,
        count=1,
    )
    if count:
        path.write_text(updated.replace('\r\n', '\n'), encoding='utf-8')


def require_document_status(
    failures: list[str], project: Path, filename: str, expected: str
) -> None:
    status = frontmatter_status(project / filename)
    if status != expected:
        failures.append(f'{filename}: frontmatter status must be {expected!r}; found {status!r}')


def validate_references(
    failures: list[str], project: Path, external_sources_required: bool
) -> set[str]:
    path = project / '.design-frontend-studio' / 'references.json'
    try:
        references = json.loads(path.read_text(encoding='utf-8-sig'))
    except FileNotFoundError:
        failures.append('.design-frontend-studio/references.json: file is required')
        return set()
    except json.JSONDecodeError as error:
        failures.append(f'.design-frontend-studio/references.json: invalid JSON: {error}')
        return set()
    if not isinstance(references, dict):
        failures.append('.design-frontend-studio/references.json: root must be an object')
        return set()

    sources = references.get('sources')
    valid_sources = []
    external_urls = set()
    if isinstance(sources, list):
        for index, item in enumerate(sources):
            if not isinstance(item, dict):
                failures.append(f'references.sources[{index}]: must be an object')
                continue
            evidence_kind = item.get('evidence_kind')
            url = item.get('url')
            location = item.get('location')
            valid_url = isinstance(url, str) and url.startswith(('http://', 'https://'))
            valid_location = isinstance(location, str) and bool(location.strip())
            if not isinstance(evidence_kind, str) or not evidence_kind.strip():
                failures.append(f'references.sources[{index}].evidence_kind: non-empty value is required')
                continue
            if not valid_url and not valid_location:
                failures.append(f'references.sources[{index}]: http(s) url or local location is required')
                continue
            valid_sources.append(item)
            if valid_url:
                external_urls.add(url.strip())
    if external_sources_required and len(external_urls) < 2:
        failures.append('references.sources: at least two distinct http(s) sources are required')
    if not external_sources_required and not valid_sources:
        failures.append('references.sources: record at least one incumbent, product, or rendered evidence source')

    components = references.get('components')
    if not isinstance(components, list):
        failures.append('references.components: must be a list')
    else:
        for index, component in enumerate(components):
            if not isinstance(component, dict):
                failures.append(f'references.components[{index}]: must be an object')
                continue
            license_status = str(component.get('license_status', '')).strip().lower()
            allowed_license_statuses = {'verified-compatible', 'not-used', 'approved-exception'}
            if license_status not in allowed_license_statuses:
                failures.append(
                    f'references.components[{index}].license_status: use verified-compatible, not-used, or approved-exception'
                )
            if component.get('dependencies_resolved') is not True:
                failures.append(f'references.components[{index}].dependencies_resolved: must be true')

    claims = references.get('claims')
    if not isinstance(claims, list):
        failures.append('references.claims: must be a list')
    else:
        allowed = {'verified', 'remove', 'draft-only'}
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                failures.append(f'references.claims[{index}]: must be an object')
                continue
            status = claim.get('status')
            if status not in allowed:
                failures.append(
                    f'references.claims[{index}].status: must be verified, remove, or draft-only'
                )
            if not isinstance(claim.get('claim'), str) or not claim['claim'].strip():
                failures.append(f'references.claims[{index}].claim: non-empty text is required')
            if not isinstance(claim.get('source'), str) or not claim['source'].strip():
                failures.append(f'references.claims[{index}].source: non-empty source is required')
            if status in {'remove', 'draft-only'} and claim.get('published') is not False:
                failures.append(f'references.claims[{index}].published: remove/draft-only claims must be false')
    return {item['evidence_kind'].strip() for item in valid_sources}


def require_phase(failures: list[str], state: dict[str, Any], name: str) -> None:
    allowed = {
        'implement': {'intake', 'design', 'implementation'},
        'preview': {'implementation', 'preview'},
        'production': {'preview', 'production'},
        'close': {'preview', 'production', 'closed'},
    }
    phase = state.get('phase')
    if phase not in allowed[name]:
        failures.append(
            f'phase: gate {name!r} is not allowed from {phase!r}; expected one of {sorted(allowed[name])}'
        )


def gate_failures(project: Path, state: dict[str, Any], name: str) -> list[str]:
    failures: list[str] = []
    ordered = ['implement', 'preview', 'production', 'close']
    if name not in ordered:
        raise SystemExit(f'Unknown gate: {name}')
    level = ordered.index(name)
    require_phase(failures, state, name)

    require_document_status(failures, project, 'BRIEF.md', 'approved')
    require_document_status(failures, project, 'DESIGN.md', 'approved')
    require_file(failures, project, 'brief.approval_evidence', get_value(state, 'brief.approval_evidence'))
    require_file(failures, project, 'design.approval_evidence', get_value(state, 'design.approval_evidence'))
    external_sources_required = get_value(state, 'research.external_sources_required')
    if external_sources_required is not True:
        require(
            failures,
            state,
            'research.source_waiver_reason',
            lambda value: isinstance(value, str) and len(value.strip()) >= 12,
            'record why incumbent/product evidence is sufficient without external inspiration',
        )
    source_kinds = validate_references(failures, project, external_sources_required is True)
    state_kinds = get_value(state, 'research.evidence_kinds')
    if isinstance(state_kinds, list):
        normalized_state_kinds = {item.strip() for item in state_kinds if isinstance(item, str) and item.strip()}
        has_invalid_kind = any(not isinstance(item, str) or not item.strip() for item in state_kinds)
        if has_invalid_kind or not normalized_state_kinds.issubset(source_kinds):
            failures.append('research.evidence_kinds: every state kind must be a non-empty source evidence_kind')

    require(failures, state, 'brief.approved', lambda value: value is True, 'brief must be approved')
    require(failures, state, 'brief.primary_user', lambda value: isinstance(value, str) and bool(value.strip()), 'primary user is required')
    require(failures, state, 'brief.primary_action', lambda value: isinstance(value, str) and bool(value.strip()), 'primary task or CTA is required')
    require(failures, state, 'brief.surface_mode', lambda value: value in {'persuade', 'operate', 'read', 'experience'}, 'surface mode must be persuade, operate, read, or experience')
    require(failures, state, 'brief.scope_defined', lambda value: value is True, 'scope and non-goals are required')
    require(failures, state, 'brief.claims_resolved', lambda value: value is True, 'claims must be verified, removed, or draft-only')
    require(failures, state, 'brief.access_preflight_complete', lambda value: value is True, 'access preflight must be recorded')
    require(failures, state, 'research.complete', lambda value: value is True, 'research must be complete')
    required_kind_count = 2 if external_sources_required is True else 1
    require(
        failures,
        state,
        'research.evidence_kinds',
        lambda value: isinstance(value, list)
        and len({item.strip() for item in value if isinstance(item, str) and item.strip()}) >= required_kind_count,
        f'record at least {required_kind_count} relevant evidence kind(s)',
    )
    require(failures, state, 'research.component_licenses_resolved', lambda value: value is True, 'component licenses and dependencies must be resolved')
    require(failures, state, 'design.approved', lambda value: value is True, 'approved DESIGN.md version is required')

    if level >= 1:
        require_document_status(failures, project, 'QA.md', 'passed')
        require(failures, state, 'implementation.complete', lambda value: value is True, 'implementation must be complete')
        require(failures, state, 'implementation.build_passed', lambda value: value is True, 'production build must pass')
        require(failures, state, 'implementation.revision', lambda value: isinstance(value, str) and bool(value.strip()), 'record revision or build source')
        require_file(failures, project, 'implementation.build_evidence', get_value(state, 'implementation.build_evidence'))
        require(failures, state, 'qa.acceptance_defined', lambda value: value is True, 'acceptance traceability is required')
        require(failures, state, 'qa.art_direction_proof_approved', lambda value: value is True, 'desktop/mobile art-direction proof must be approved')
        visual_scores = get_value(state, 'qa.visual_scores')
        expected_scores = {
            'mode_success',
            'hierarchy',
            'composition',
            'distinctiveness',
            'coherence',
            'content_media',
            'responsive',
            'interaction_craft',
        }
        if not isinstance(visual_scores, dict) or set(visual_scores) != expected_scores:
            failures.append('qa.visual_scores: all eight visual dimensions are required')
        else:
            for score_name, score in visual_scores.items():
                if not isinstance(score, int) or isinstance(score, bool) or score < 4 or score > 5:
                    failures.append(f'qa.visual_scores.{score_name}: score must be an integer from 4 to 5')
        require(failures, state, 'qa.blocker_open', lambda value: value == 0, 'open blockers must be zero')
        require(failures, state, 'qa.major_open', lambda value: value == 0, 'open major defects must be zero')
        for key in ['desktop_rendered', 'mobile_rendered', 'keyboard_checked', 'touch_checked', 'reduced_motion_checked']:
            require(failures, state, f'qa.{key}', lambda value: value is True, 'required rendered or interaction evidence is missing')
        require_files(failures, project, 'qa.evidence_paths', get_value(state, 'qa.evidence_paths'))
        require_media_files(failures, project, 'qa.desktop_evidence_paths', get_value(state, 'qa.desktop_evidence_paths'))
        require_media_files(failures, project, 'qa.mobile_evidence_paths', get_value(state, 'qa.mobile_evidence_paths'))
        require_file(failures, project, 'qa.scorecard_evidence_path', get_value(state, 'qa.scorecard_evidence_path'))
        require(
            failures,
            state,
            'qa.evidence_revision',
            lambda value: isinstance(value, str) and value.strip() == get_value(state, 'implementation.revision'),
            'visual evidence must identify the current implementation revision',
        )

    mode = get_value(state, 'deployment.mode')
    if mode not in {'none', 'preview', 'production'}:
        failures.append('deployment.mode: must be none, preview, or production')
    if name == 'production':
        require(failures, state, 'deployment.mode', lambda value: value == 'production', 'production gate requires production mode')
    preview_needed = (
        name == 'production'
        or (name == 'preview' and mode in {'preview', 'production'})
        or (name == 'close' and mode in {'preview', 'production'})
    )
    if preview_needed:
        require(failures, state, 'deployment.preview_url', lambda value: isinstance(value, str) and value.startswith(('http://', 'https://')), 'preview URL is required')
        require(failures, state, 'deployment.preview_approved', lambda value: value is True, 'preview must be approved')
        require_file(failures, project, 'deployment.preview_approval_evidence', get_value(state, 'deployment.preview_approval_evidence'))
    if name == 'production':
        require(failures, state, 'deployment.target', lambda value: isinstance(value, str) and bool(value.strip()), 'deployment target is required')
        require(failures, state, 'deployment.rollback_recorded', lambda value: value is True, 'rollback path must be recorded')

    if level >= 3:
        if mode == 'production':
            require(failures, state, 'deployment.production_url', lambda value: isinstance(value, str) and value.startswith(('http://', 'https://')), 'production URL is required')
            require(failures, state, 'deployment.smoke_passed', lambda value: value is True, 'post-deploy smoke test must pass')
        require(failures, state, 'learning.observation_complete', lambda value: value is True, 'observation window must complete')
        require(failures, state, 'learning.acceptance_recorded', lambda value: value is True, 'user or objective acceptance must be recorded')
        require(failures, state, 'learning.evidence_recorded', lambda value: value is True, 'evidence-backed learning must be recorded')
        require_files(failures, project, 'learning.evidence_paths', get_value(state, 'learning.evidence_paths'))
    return failures


def check_gate(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    path = project / STATE_PATH
    state = migrate_state(read_json(path))
    failures = gate_failures(project, state, args.name)
    if failures:
        print(json.dumps({'gate': args.name, 'passed': False, 'missing': failures}, ensure_ascii=False, indent=2))
        return 1
    previous_phase = state.get('phase')
    next_phase = {'implement': 'implementation', 'preview': 'preview', 'production': 'production', 'close': 'closed'}[args.name]
    state['phase'] = next_phase
    history = state.get('history')
    if not isinstance(history, list):
        history = []
        state['history'] = history
    history.append({
        'event': 'gate',
        'gate': args.name,
        'from': previous_phase,
        'to': next_phase,
        'mode': get_value(state, 'deployment.mode'),
        'revision': get_value(state, 'implementation.revision'),
        'at': datetime.now(timezone.utc).isoformat(),
    })
    write_json(path, state)
    print(json.dumps({'gate': args.name, 'passed': True, 'phase': next_phase}, ensure_ascii=False, indent=2))
    return 0


def show_status(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    print(json.dumps(migrate_state(read_json(project / STATE_PATH)), ensure_ascii=False, indent=2))
    return 0


def reopen_project(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    path = project / STATE_PATH
    state = migrate_state(read_json(path))
    order = {'intake': 0, 'design': 1, 'implementation': 2, 'preview': 3, 'production': 4, 'closed': 5}
    current = state.get('phase')
    if current not in order:
        raise SystemExit(f'Unknown current phase: {current!r}')
    if order[args.phase] >= order[current]:
        raise SystemExit(f'Reopen target must be earlier than current phase {current!r}')

    if args.phase == 'intake':
        state['brief']['approved'] = False
        state['brief']['approval_evidence'] = ''
        state['design']['approved'] = False
        state['design']['approval_evidence'] = ''
        set_frontmatter_status(project / 'BRIEF.md', 'draft')
        set_frontmatter_status(project / 'DESIGN.md', 'draft')
    if args.phase == 'design':
        state['design']['approved'] = False
        state['design']['approval_evidence'] = ''
        set_frontmatter_status(project / 'DESIGN.md', 'draft')
    if args.phase in {'intake', 'design', 'implementation'}:
        state['implementation'].update({
            'complete': False,
            'build_passed': False,
            'build_evidence': '',
            'revision': '',
        })
        state['qa'].update({
            'acceptance_defined': False,
            'art_direction_proof_approved': False,
            'visual_scores': {
                'mode_success': 0,
                'hierarchy': 0,
                'composition': 0,
                'distinctiveness': 0,
                'coherence': 0,
                'content_media': 0,
                'responsive': 0,
                'interaction_craft': 0,
            },
            'blocker_open': 0,
            'major_open': 0,
            'desktop_rendered': False,
            'mobile_rendered': False,
            'keyboard_checked': False,
            'touch_checked': False,
            'reduced_motion_checked': False,
            'evidence_paths': [],
            'desktop_evidence_paths': [],
            'mobile_evidence_paths': [],
            'scorecard_evidence_path': '',
            'evidence_revision': '',
        })
    if args.phase in {'intake', 'design', 'implementation', 'preview'}:
        state['deployment'].update({
            'target': '',
            'preview_url': '',
            'preview_approved': False,
            'preview_approval_evidence': '',
            'rollback_recorded': False,
            'production_url': '',
            'smoke_passed': False,
        })
        state['learning'].update({
            'observation_complete': False,
            'acceptance_recorded': False,
            'evidence_recorded': False,
            'evidence_paths': [],
        })
    state['phase'] = args.phase
    history = state.get('history')
    if not isinstance(history, list):
        history = []
        state['history'] = history
    history.append({
        'event': 'reopen',
        'from': current,
        'to': args.phase,
        'reason': args.reason,
        'at': datetime.now(timezone.utc).isoformat(),
    })
    write_json(path, state)
    print(json.dumps({'reopened': True, 'from': current, 'phase': args.phase}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='command', required=True)

    init_parser = subparsers.add_parser('init', help='Create missing workflow artifacts')
    init_parser.add_argument('--project', required=True)
    init_parser.add_argument('--name', required=True)
    init_parser.add_argument('--surface', default='primary web surface')
    init_parser.add_argument('--platform', default='web')
    init_parser.set_defaults(handler=initialize)

    set_parser = subparsers.add_parser('set', help='Set one dotted state key')
    set_parser.add_argument('--project', required=True)
    set_parser.add_argument('--key', required=True)
    set_parser.add_argument('--value', required=True)
    set_parser.set_defaults(handler=update_state)

    gate_parser = subparsers.add_parser('gate', help='Validate a lifecycle gate')
    gate_parser.add_argument('--project', required=True)
    gate_parser.add_argument('--name', required=True, choices=['implement', 'preview', 'production', 'close'])
    gate_parser.set_defaults(handler=check_gate)

    status_parser = subparsers.add_parser('status', help='Print workflow state')
    status_parser.add_argument('--project', required=True)
    status_parser.set_defaults(handler=show_status)

    reopen_parser = subparsers.add_parser(
        'reopen', help='Move to an earlier phase and invalidate downstream evidence'
    )
    reopen_parser.add_argument('--project', required=True)
    reopen_parser.add_argument('--phase', required=True, choices=['intake', 'design', 'implementation', 'preview'])
    reopen_parser.add_argument('--reason', required=True)
    reopen_parser.set_defaults(handler=reopen_project)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == '__main__':
    raise SystemExit(main())
