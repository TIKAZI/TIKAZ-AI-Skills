#!/usr/bin/env python3
"""Generate the public Skill catalog and editable suite workflow diagrams."""

from __future__ import annotations

import argparse
import html
import json
import re
import textwrap
from pathlib import Path


ATTRIBUTION = (
    "Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**."
)
PAGES_BASE = "https://tikazi.github.io/TIKAZ-AI-Skills"

SUITE_LIMITS = {
    "frontend-design": ["Design approval is not runtime verification.", "Optional component libraries and browser tools must be detected before use.", "Existing routes, analytics, accessibility, and legal copy are preserved unless the user authorizes change."],
    "video-intelligence": ["Platform access, subtitles, downloads, and visual inspection depend on the current environment.", "Metadata and search snippets are not watched content.", "Private, paid, DRM-protected, deleted, or inaccessible media remains unresolved rather than bypassed."],
    "engineering": ["Repository instructions and native tests outrank generic playbooks.", "Security review reduces risk but cannot guarantee safety.", "Production deployment, migrations, and destructive actions require explicit scope and rollback evidence."],
    "knowledge-research": ["Conversion is not verification and retrieval is not adoption.", "Source dates, disagreement, confidence, and revalidation needs remain visible.", "Financial, legal, medical, or safety-critical conclusions require appropriate professional review."],
    "presentation": ["A generated file is not visually approved until rendered and inspected.", "HTML, PPTX, and editorial web decks have different editability and compatibility boundaries.", "External media, fonts, templates, and builder licenses remain authoritative."],
    "visual-content": ["The suite does not require or promise a specific image provider.", "Unverified labels or business claims are not turned into definitive visuals.", "Music is downloaded only from sources that explicitly permit it, with license evidence retained."],
}

SUITE_ORDER = {
    "context-economy": ["context-economy", "context-pack", "conversation-checkpoint", "context-audit", "context-benchmark"],
    "frontend-design": ["frontend-design", "frontend-design-studio"],
    "video-intelligence": ["video-intelligence", "video-platform-reader"],
    "engineering": ["engineering", "code-intelligence", "engineering-delivery", "skill-security-audit", "supabase-operations", "video-workbench"],
    "knowledge-research": ["knowledge-research", "document-to-markdown", "academic-research", "product-strategy", "solo-business-operations", "personal-knowledge-memory"],
    "presentation": ["presentation", "html-deck-builder", "powerpoint-deck-builder", "magazine-web-deck"],
    "visual-content": ["visual-content", "concise-writing-editor", "xiaohei-article-illustrator", "zhuge-logistics-illustrator", "legal-free-music"],
}

SUITE_PRESENTATION = {
    "context-economy": ("⚡", "Context Economy", "上下文经济"),
    "frontend-design": ("🎨", "Frontend Design", "前端设计"),
    "video-intelligence": ("🎬", "Video Intelligence", "视频智能"),
    "engineering": ("🛠️", "Engineering", "工程"),
    "knowledge-research": ("🔬", "Knowledge & Research", "知识与研究"),
    "presentation": ("📽️", "Presentation", "演示"),
    "visual-content": ("🖼️", "Visual Content", "视觉内容"),
}

ZH_PROMISES = {
    "context-economy": "自动判断文本、网页、PDF、表格与图片应走 Text、Hybrid 还是 Source，并保留可追溯原始来源。",
    "context-pack": "把文件、目录、代码、日志和结构化数据整理成有预算、可追溯的上下文包。",
    "conversation-checkpoint": "把长对话整理为可恢复的决策、状态、证据与待办。",
    "context-audit": "审计上下文的相关性、重复、可追溯性、安全、缓存与恢复能力。",
    "context-benchmark": "在版本化固定样例上分别测量上下文节省与保真。",
    "frontend-design": "统筹产品艺术方向、实现、响应式 QA 与工程移交。",
    "frontend-design-studio": "设计、实现、审查、打磨并验证有辨识度的生产界面。",
    "video-intelligence": "统筹跨平台视频研究、证据分级与综合报告。",
    "video-platform-reader": "用元数据、时间戳、ASR、关键帧和来源卡阅读公开视频或本地视频。",
    "engineering": "从规格和影响分析一直负责到测试、审查与发布证据。",
    "code-intelligence": "分析仓库结构、语义关系、变更影响、PR 风险与重构范围。",
    "engineering-delivery": "完成有边界的软件实现、测试、审查与发布移交。",
    "skill-security-audit": "安装第三方 Skill 前执行静态安全审计。",
    "supabase-operations": "设计和运营 Supabase 架构、迁移、安全、备份与可观测性。",
    "video-workbench": "从导入、任务状态、处理、复核、导出到部署构建媒体工作台。",
    "knowledge-research": "统筹来源、研究、决策、个人知识与证据反馈。",
    "document-to-markdown": "把文档、网页、图片和音频转换为保留来源的结构化 Markdown。",
    "academic-research": "执行文献综述、证据综合、研究写作与同行评审式审查。",
    "product-strategy": "完成产品发现、定位、优先级、GTM 与分析。",
    "solo-business-operations": "协调一人业务的产品、内容、财务、运营与支持。",
    "personal-knowledge-memory": "检索个人决策，并只记录真正改变执行的知识。",
    "presentation": "选择一种演示格式，并从叙事一直管理到渲染 QA。",
    "html-deck-builder": "构建可在浏览器编辑、可离线使用的 HTML 演示。",
    "powerpoint-deck-builder": "创建并验证原生可编辑 PowerPoint。",
    "magazine-web-deck": "创建杂志或瑞士风格的单文件网页演示。",
    "visual-content": "统筹写作、配图、物流图、音乐、无障碍与发布 QA。",
    "concise-writing-editor": "清除 AI 套话和重复，同时保留原意与声音。",
    "xiaohei-article-illustrator": "用一致角色与手绘隐喻指导中文文章配图。",
    "zhuge-logistics-illustrator": "指导有来源依据的 16:9 中文物流科普图。",
    "legal-free-music": "查找可合法下载的公版、CC 或艺术家授权音乐，并保留许可证证据。",
}


SUITE_ADVANTAGES = {
    "frontend-design": [
        ("4 surface modes", "Marketing, product, editorial, and operational interfaces use different design rules.", "4 类界面模式", "营销、产品、编辑与运营界面分别采用不同设计规则。"),
        ("Desktop + mobile proof", "Responsive behavior is rendered and inspected instead of inferred from source code.", "桌面端 + 移动端实证", "响应式结果必须真实渲染检查，而不是只看源码推断。"),
        ("Design-to-code ownership", "One workflow owns art direction, implementation, QA, and engineering handoff.", "设计到代码闭环", "同一工作流负责艺术方向、实现、QA 与工程移交。"),
    ],
    "video-intelligence": [
        ("5 evidence levels", "Metadata, transcript, ASR, keyframes, and directly inspected media are never treated as equivalent.", "5 级证据", "元数据、字幕、ASR、关键帧与直接观看不会被混为同等证据。"),
        ("Timestamped synthesis", "Claims stay connected to timestamps, source cards, and visible access limits.", "带时间戳的综合", "结论保留时间戳、来源卡与访问限制。"),
        ("Partial failure stays visible", "Unavailable subtitles or frames trigger a declared fallback rather than a fabricated summary.", "局部失败透明", "字幕或画面不可用时进入明确降级，不伪造完整总结。"),
    ],
    "engineering": [
        ("6-stage delivery loop", "Specification, impact analysis, implementation, tests, security, and release evidence remain connected.", "6 阶段交付闭环", "规格、影响分析、实现、测试、安全与发布证据保持连贯。"),
        ("Change-impact first", "Repository relationships and blast radius are checked before broad refactors.", "先做变更影响分析", "大范围重构前先检查仓库关系与影响半径。"),
        ("Evidence-backed handoff", "A change is not called complete until native tests and relevant release checks pass.", "证据化移交", "原生测试与相关发布检查通过前，不把改动称为完成。"),
    ],
    "knowledge-research": [
        ("Source-to-decision trace", "Dates, disagreements, confidence, and revalidation needs stay attached to conclusions.", "来源到决策可追溯", "日期、分歧、置信度与复核需要始终跟随结论。"),
        ("Retrieval is not adoption", "Personal knowledge changes execution only when it is relevant and explicitly adopted.", "检索不等于采用", "个人知识只有在相关且明确采用时才改变执行。"),
        ("Structured Markdown handoff", "Documents become source-aware Markdown that downstream Skills can inspect efficiently.", "结构化 Markdown 移交", "文档转为保留来源的 Markdown，便于下游 Skill 高效检查。"),
    ],
    "presentation": [
        ("3 output builders", "HTML, native PowerPoint, and editorial web decks keep distinct compatibility contracts.", "3 类输出构建器", "HTML、原生 PowerPoint 与编辑型网页演示各自保留兼容性合同。"),
        ("One owner per deck", "The orchestrator selects one builder so parallel formats do not create conflicting artifacts.", "一份演示一个负责人", "编排器只选择一个构建器，避免多格式并行产生冲突成品。"),
        ("Rendered QA", "Overflow, typography, hierarchy, and editability are checked on the rendered result.", "渲染后 QA", "在真实渲染结果中检查溢出、排版、层级与可编辑性。"),
    ],
    "visual-content": [
        ("2 distinct illustration identities", "Editorial and logistics visuals keep separate character, evidence, and layout systems.", "2 套独立插画识别", "编辑插画与物流科普图保持不同的角色、证据与版式系统。"),
        ("Claim-aware production", "Unverified business claims are kept out of definitive visuals and captions.", "主张感知制作", "未经核实的商业主张不会被画成确定事实。"),
        ("License-aware media", "Downloadable music retains source and permission evidence for later publication review.", "许可感知媒体", "可下载音乐保留来源与授权证据，便于发布前复核。"),
    ],
}

CONTEXT_EVIDENCE = {
    "context-economy": [
        ("69.73%", "estimated token reduction", "6 fixed long-context tasks: 4,698 → 1,422", "估算 Token 减少", "6 个固定长上下文任务：4,698 → 1,422"),
        ("27.78%", "estimated prompt reduction", "6 fixed prompt cases: 252 → 182", "估算提示词减少", "6 个固定提示词样例：252 → 182"),
        ("46/46", "declared protected facts retained", "literal recall, not semantic accuracy", "声明保护事实保留", "字面召回，不等同语义准确率"),
        ("39/39", "expected anchors retained", "fixed public benchmark", "预期锚点保留", "固定公开基准"),
        ("3/3", "generated PDF literal checks complete", "text, numbers, tables, and page anchors; visual accuracy pending", "生成 PDF 字面检查完成", "文字、数字、表格与页锚点；视觉准确率待测"),
    ],
    "context-pack": [
        ("69.73%", "estimated token reduction", "6 fixed long-context tasks: 4,698 → 1,422", "估算 Token 减少", "6 个固定长上下文任务：4,698 → 1,422"),
        ("46/46", "declared protected facts retained", "literal recall on declared facts", "声明保护事实保留", "声明事实的字面召回"),
        ("39/39", "expected anchors retained", "source anchors stay traceable", "预期锚点保留", "来源锚点保持可追溯"),
    ],
    "context-benchmark": [
        ("50", "versioned public cases", "30 correctness + 6 efficiency + 14 routing/filtering cases", "版本化公开样例", "30 个正确性 + 6 个效率 + 14 个路由/过滤样例"),
        ("69.73%", "long-context reduction", "estimated tokens on the fixed efficiency profile", "长上下文减少", "固定效率组的估算 Token"),
        ("+143.93%", "short-input overhead", "negative result remains visible", "短输入开销", "负向结果保持公开"),
    ],
    "context-audit": [
        ("8/8", "route labels matched", "fixed labeled routing cases", "路由标签匹配", "固定标注路由样例"),
        ("7/7", "table risk gates matched", "fixed labeled table cases", "表格风险门匹配", "固定标注表格样例"),
        ("No universal score", "claim boundary enforced", "audit dimensions stay separate", "不设通用总分", "各审计维度保持分离"),
    ],
    "conversation-checkpoint": [
        ("Decisions", "recoverable state", "confirmed choices are separated from discussion", "决策", "可恢复状态", "已确认选择与讨论内容分离"),
        ("Evidence", "traceable anchors", "sources and unresolved limits remain visible", "证据", "可追溯锚点", "来源与未解决限制保持可见"),
        ("Next actions", "restart-ready handoff", "the next session can resume without replaying the full chat", "下一步", "可续接移交", "下次会话无需重放完整对话即可继续"),
    ],
}


def display_name(name: str) -> str:
    return "TIKAZ " + " ".join(part.capitalize() for part in name.split("-"))


def metadata_yaml(name: str, description: str) -> str:
    short = short_promise(description, 58).rstrip(".")
    if len(short) < 25:
        short = f"TIKAZ workflow for {name.replace('-', ' ')}"
    prompt = f"Use ${name} to {short_promise(description, 125)[0].lower() + short_promise(description, 125)[1:]}"
    if not prompt.endswith("."):
        prompt += "."
    return (
        "interface:\n"
        f'  display_name: "{display_name(name)}"\n'
        f'  short_description: "{short.replace(chr(34), chr(39))}"\n'
        f'  default_prompt: "{prompt.replace(chr(34), chr(39))}"\n'
    )


def suite_readme(root: Path, suite_name: str, info: dict) -> str:
    suite = root / "suites" / suite_name
    skills = skills_for_suite(suite)
    rows = []
    for name, description, path in skills:
        role = "Orchestrator" if path.parent == suite else "Specialist"
        rows.append(f"| [`{name}`]({PAGES_BASE}/skills/{name}/index.html) | {role} | {short_promise(description, 170)} |")
    prompts = "\n\n".join(f"```text\n{prompt}\n```" for prompt in info["prompts"])
    highlights = "\n".join(f"- {item}." for item in info["highlights"])
    limits = "\n".join(f"- {item}" for item in SUITE_LIMITS[suite_name])
    title = info["title"]
    return f'''<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><img src="assets/workflow.svg" alt="{title} workflow" width="100%" /></p>

# {title}

**{info['tagline']}**

{ATTRIBUTION}

This suite can be installed as one routed workflow, while every child Skill can also be installed and invoked on its own. It is an independent community project for Codex-compatible Skill hosts, not an OpenAI-official repository.

## ✨ What makes it different

{highlights}

## 🧩 Skills you can use independently

| Skill | Role | Core promise |
|---|---|---|
{chr(10).join(rows)}

The root orchestrator owns end-to-end routing. A specialist owns only the output named in its `SKILL.md`; it does not need the orchestrator to be installed.

## 🚀 Try it

{prompts}

## 📦 Install the suite or one Skill

Copy this suite folder for the complete workflow, or copy one child folder into the Skill directory supported by your Codex host. Keep the destination folder identical to the `name` in `SKILL.md`.

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\\suites\\{suite_name}' `
  -Destination '.\\.agents\\skills\\{suite_name}'
```

## 🔄 Workflow and output contract

Read [routing](references/routing.md) for owner selection and [output contract](references/output-contract.md) for the verified handoff. The diagram above is editable SVG generated from canonical Skill metadata under the shared [TIKAZ visual system](../../docs/visual-system.md).

## ⚠️ Limitations

{limits}

## ⚖️ Provenance

Source modes, upstream licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](../../SOURCES.yml) and [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md). TIKAZ authorship applies to original architecture, integration, refactoring, routing, and maintenance; it does not erase third-party ownership.

## 🌐 Explore the TIKAZ workflow family

[🏠 AI Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills) · [⚡ Context Economy](https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy) · [🎨 Frontend Design](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) · [🎬 Video Intelligence](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) · [🛠️ Engineering](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) · [🔬 Research](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) · [📽️ Presentation](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) · [🖼️ Visual Content](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content)
'''


def parse_frontmatter(path: Path) -> tuple[str, str]:
    content = path.read_text(encoding="utf-8")
    name = re.search(r"(?m)^name:\s*[\"']?([^\r\n\"']+)", content)
    description = re.search(r"(?ms)^description:\s*[\"']?(.+?)[\"']?\s*(?=\r?\n---)", content)
    if not name or not description:
        raise ValueError(f"Invalid Skill frontmatter: {path}")
    return name.group(1).strip(), " ".join(description.group(1).split())


def skills_for_suite(suite: Path) -> list[tuple[str, str, Path]]:
    items = []
    for skill_path in sorted(suite.rglob("SKILL.md")):
        name, description = parse_frontmatter(skill_path)
        items.append((name, description, skill_path))
    order = {name: index for index, name in enumerate(SUITE_ORDER.get(suite.name, []))}
    items.sort(key=lambda item: (order.get(item[0], 999), item[0]))
    return items


def feedback_catalog(root: Path) -> dict[str, list[str]]:
    """Return the canonical workflow-to-Skill map used by the public feedback form."""

    return {
        suite_name: [name for name, _, _ in skills_for_suite(root / "suites" / suite_name)]
        for suite_name in SUITE_ORDER
    }


def feedback_data_javascript(root: Path) -> str:
    payload = json.dumps(feedback_catalog(root), ensure_ascii=False, separators=(",", ":"))
    return (
        f"const TIKAZ_FEEDBACK_DATA={payload};\n"
        "if(typeof window!=='undefined')window.TIKAZ_FEEDBACK_DATA=TIKAZ_FEEDBACK_DATA;\n"
        "if(typeof module!=='undefined')module.exports=TIKAZ_FEEDBACK_DATA;\n"
    )


def short_promise(description: str, limit: int = 150) -> str:
    sentence = re.split(r"(?<=[.!?])\s+", description, maxsplit=1)[0]
    if len(sentence) <= limit:
        return sentence
    return sentence[: limit - 1].rstrip() + "…"


def first_example(path: Path, name: str, language: str) -> str:
    content = path.read_text(encoding="utf-8")
    examples = re.findall(r"```text\s*\n(.*?)\n```", content, flags=re.DOTALL)
    if examples:
        return examples[0].strip()
    if language == "zh-CN":
        return f"使用 {name} 完成这项任务，并保留验证证据与未解决限制。"
    return f"Use {name} to complete this task and retain verification evidence and unresolved limits."


def project_evidence(suite_name: str, name: str, language: str) -> tuple[str, str]:
    is_zh = language == "zh-CN"
    if name in CONTEXT_EVIDENCE:
        cards = []
        for card in CONTEXT_EVIDENCE[name]:
            if len(card) == 5:
                value_en, label_en, note_en, label_zh, note_zh = card
                value_zh = value_en
            else:
                value_en, label_en, note_en, value_zh, label_zh, note_zh = card
            value = value_zh if is_zh else value_en
            label = label_zh if is_zh else label_en
            note = note_zh if is_zh else note_en
            cards.append(
                f'<article><strong>{html.escape(value)}</strong><span>{html.escape(label)}</span><small>{html.escape(note)}</small></article>'
            )
        boundary = (
            "固定公开基准；Token 为确定性估算，不是供应商账单。短输入可能因协议开销增大，结果不代表通用准确率或跨项目优越性。"
            if is_zh else
            "Fixed public benchmark; tokens are deterministic estimates, not provider billing. Short inputs may grow from protocol overhead. Results are not universal accuracy or cross-project superiority claims."
        )
        source_label = "查看完整证据卡" if is_zh else "Open the full evidence card"
        source = "https://github.com/TIKAZI/TIKAZ-AI-Skills/blob/main/suites/context-economy/benchmarks/results/README.md"
        return "".join(cards), f'{html.escape(boundary)} <a href="{source}">{source_label} →</a>'

    advantages = SUITE_ADVANTAGES[suite_name]
    cards = []
    for value_en, note_en, value_zh, note_zh in advantages:
        value = value_zh if is_zh else value_en
        note = note_zh if is_zh else note_en
        cards.append(
            f'<article><strong>{html.escape(value)}</strong><small>{html.escape(note)}</small></article>'
        )
    boundary = (
        "这里展示的是可检查的工作流结构与质量门，不是未经测试的性能百分比。"
        if is_zh else
        "These are inspectable workflow properties and quality gates, not untested performance percentages."
    )
    return "".join(cards), html.escape(boundary)


def skill_project_page(root: Path, suite_name: str, name: str, description: str, path: Path, language: str) -> str:
    emoji, suite_en, suite_zh = SUITE_PRESENTATION[suite_name]
    is_zh = language == "zh-CN"
    role = "编排器" if is_zh and path.parent.name == suite_name else "专项 Skill" if is_zh else "Orchestrator" if path.parent.name == suite_name else "Specialist Skill"
    promise = ZH_PROMISES[name] if is_zh else short_promise(description, 220)
    source = path.relative_to(root).as_posix()
    folder = path.parent.relative_to(root).as_posix()
    example = first_example(path, name, language)
    evidence_cards, evidence_boundary = project_evidence(suite_name, name, language)
    peers = skills_for_suite(root / "suites" / suite_name)
    peer_links = "".join(
        f'<a class="project-peer{" active" if peer_name == name else ""}" href="../{peer_name}/index.html">{html.escape(peer_name)}</a>'
        for peer_name, _, _ in peers
    )
    if is_zh:
        language_link = f"../../../skills/{name}/index.html"
        labels = {
            "language": "EN", "language_label": "切换到英文", "eyebrow": "可独立安装的 TIKAZ Skill",
            "back": "返回 30 Skill 目录", "what": "它解决什么", "when": "适合何时使用",
            "when_copy": "当这一项明确能力就是你的完整目标时，直接安装并调用它；需要跨能力端到端结果时，改用所属工作流编排器。",
            "install": "独立安装", "install_copy": "只复制这个 Skill 文件夹即可；不需要安装同组其他 Skill。目标文件夹名称保持与 Skill 名称一致。",
            "try": "直接这样调用", "contract": "执行合同", "contract_copy": "执行细节、输入输出、验证、降级与限制以唯一英文执行源为准。中文页只负责用户说明，不复制第二份执行规则。",
            "source": "打开执行源", "suite": "所属工作流", "peers": "同组 Skill", "advantages": "证据与核心优势",
            "maintainer": "由 TIKAZ 主导设计、整合、独立重构和持续维护。第三方来源与许可证仍保留原始归属。",
        }
        page_title = f"{name} — TIKAZ Skill 中文介绍"
        lang_attr = "zh-CN"
        suite_label = suite_zh
    else:
        language_link = f"../../zh/skills/{name}/index.html"
        labels = {
            "language": "中文", "language_label": "切换到简体中文", "eyebrow": "Independently installable TIKAZ Skill",
            "back": "Back to the 30-Skill catalog", "what": "What it owns", "when": "When to use it",
            "when_copy": "Install and invoke this Skill directly when its named capability is the complete task. Use the suite orchestrator when the outcome crosses multiple capabilities.",
            "install": "Install independently", "install_copy": "Copy only this Skill folder. No sibling Skill is required. Keep the destination folder identical to the Skill name.",
            "try": "Try it directly", "contract": "Execution contract", "contract_copy": "The single English execution source owns inputs, outputs, validation, fallback, and limits. User documentation never creates a second executable rule set.",
            "source": "Open the execution source", "suite": "Workflow group", "peers": "Skills in this group", "advantages": "Evidence and core advantages",
            "maintainer": "Designed, integrated, independently refactored, and continuously maintained by TIKAZ. Third-party sources and licenses retain their original attribution.",
        }
        page_title = f"{name} — TIKAZ Skill"
        lang_attr = "en"
        suite_label = suite_en
    install = f"Copy-Item -Recurse -LiteralPath '.\\{folder.replace('/', chr(92))}' -Destination '.\\.agents\\skills\\{name}'"
    stylesheet = "../../../styles.css" if is_zh else "../../styles.css"
    logo = "../../../assets/tikaz-logo.svg" if is_zh else "../../assets/tikaz-logo.svg"
    return f'''<!doctype html>
<html lang="{lang_attr}"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" /><meta name="description" content="{html.escape(promise)}" /><title>{html.escape(page_title)}</title><link rel="icon" href="{logo}" type="image/svg+xml" /><link rel="stylesheet" href="{stylesheet}" /></head>
<body class="project-page"><header class="project-header"><a class="brand" href="../../index.html"><img class="brand-mark" src="{logo}" alt="" /><span>TIKAZ</span></a><a class="language-link" href="{language_link}" aria-label="{labels['language_label']}">{labels['language']}</a></header>
<main><section class="project-hero"><a class="project-back" href="../index.html">← {labels['back']}</a><p class="identity">{emoji} {labels['eyebrow']}</p><h1>{html.escape(name)}</h1><p class="project-promise">{html.escape(promise)}</p><div class="project-meta"><span>{labels['suite']}: <strong>{html.escape(suite_label)}</strong></span><span>{html.escape(role)}</span></div><section class="project-evidence" aria-labelledby="evidence-title"><h2 id="evidence-title">{labels['advantages']}</h2><div>{evidence_cards}</div><p>{evidence_boundary}</p></section></section>
<section class="project-details"><article><p>01</p><h2>{labels['what']}</h2><div>{html.escape(promise)}</div></article><article><p>02</p><h2>{labels['when']}</h2><div>{labels['when_copy']}</div></article><article class="wide"><p>03</p><h2>{labels['install']}</h2><div><span>{labels['install_copy']}</span><pre><code>{html.escape(install)}</code></pre></div></article><article class="wide"><p>04</p><h2>{labels['try']}</h2><div><pre><code>{html.escape(example)}</code></pre></div></article><article class="wide"><p>05</p><h2>{labels['contract']}</h2><div><span>{labels['contract_copy']}</span><a class="project-source" href="https://github.com/TIKAZI/TIKAZ-AI-Skills/blob/main/{source}">{labels['source']} ↗</a></div></article></section>
<section class="project-peers"><p class="identity">{labels['peers']}</p><div>{peer_links}</div></section></main>
<footer class="project-footer"><strong>TIKAZ</strong><p>{labels['maintainer']}</p></footer></body></html>'''


def skill_project_index(root: Path, language: str) -> str:
    is_zh = language == "zh-CN"
    groups = []
    for suite_name in SUITE_ORDER:
        emoji, suite_en, suite_zh = SUITE_PRESENTATION[suite_name]
        links = "".join(
            f'<a href="{name}/index.html"><strong>{html.escape(name)}</strong><small>{html.escape(ZH_PROMISES[name] if is_zh else short_promise(description, 100))}</small></a>'
            for name, description, _ in skills_for_suite(root / "suites" / suite_name)
        )
        groups.append(f'<article><h2>{emoji} {suite_zh if is_zh else suite_en}<span>{len(SUITE_ORDER[suite_name])}</span></h2>{links}</article>')
    language_link = "../../skills/index.html" if is_zh else "../../zh/skills/index.html"
    home = "../index.html"
    title = "30 个可独立安装的 Skill" if is_zh else "30 independently installable Skills"
    intro = "按七套工作流分组浏览。每个 Skill 都有独立中英文项目页、安装入口和唯一执行源。" if is_zh else "Browse seven workflow groups. Every Skill has its own bilingual project page, installation entry, and single execution source."
    stylesheet = "../../styles.css" if is_zh else "../styles.css"
    logo = "../../assets/tikaz-logo.svg" if is_zh else "../assets/tikaz-logo.svg"
    feedback_label = "反馈与建议" if is_zh else "Send feedback"
    issue_label = "GitHub Issue 表单" if is_zh else "GitHub Issue forms"
    return f'''<!doctype html><html lang="{'zh-CN' if is_zh else 'en'}"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" /><title>{title} — TIKAZ</title><link rel="icon" href="{logo}" type="image/svg+xml" /><link rel="stylesheet" href="{stylesheet}" /></head><body class="project-page"><header class="project-header"><a class="brand" href="{home}"><img class="brand-mark" src="{logo}" alt="" /><span>TIKAZ</span></a><a class="language-link" href="{language_link}">{'EN' if is_zh else '中文'}</a></header><main><section class="project-hero index-hero"><p class="identity">TIKAZ AI SKILLS FOR CODEX</p><h1>{title}</h1><p class="project-promise">{intro}</p><div class="index-actions"><a class="button primary" href="../index.html#feedback">{feedback_label}</a><a class="button secondary" href="https://github.com/TIKAZI/TIKAZ-AI-Skills/issues/new/choose">{issue_label}</a></div></section><section class="skill-index-groups">{''.join(groups)}</section></main></body></html>'''


def publish_skill_project_pages(root: Path, output: Path, manifest: dict) -> None:
    english_root = output / "skills"
    chinese_root = output / "zh" / "skills"
    english_root.mkdir(parents=True, exist_ok=True)
    chinese_root.mkdir(parents=True, exist_ok=True)
    (english_root / "index.html").write_text(skill_project_index(root, "en"), encoding="utf-8")
    (chinese_root / "index.html").write_text(skill_project_index(root, "zh-CN"), encoding="utf-8")
    for suite_name in manifest["suites"]:
        for name, description, path in skills_for_suite(root / "suites" / suite_name):
            for language, destination in (("en", english_root), ("zh-CN", chinese_root)):
                page_dir = destination / name
                page_dir.mkdir(parents=True, exist_ok=True)
                (page_dir / "index.html").write_text(skill_project_page(root, suite_name, name, description, path, language), encoding="utf-8")


def publish_project_entry_links(root: Path, output: Path, manifest: dict) -> None:
    documents = {
        root / "README.md": ("README_EN",),
        root / "README.zh-CN.md": ("README_ZH",),
        output / "index.html": ("PAGE_EN",),
        output / "zh" / "index.html": ("PAGE_ZH",),
    }
    for document, (kind,) in documents.items():
        content = document.read_text(encoding="utf-8")
        for suite_name in manifest["suites"]:
            for name, _, skill_path in skills_for_suite(root / "suites" / suite_name):
                relative = skill_path.relative_to(root).as_posix()
                if kind == "README_EN":
                    target = f"{PAGES_BASE}/skills/{name}/index.html"
                    content = content.replace(f"]({relative})", f"]({target})")
                    content = content.replace(f"](docs/skills/{name}/index.html)", f"]({target})")
                elif kind == "README_ZH":
                    target = f"{PAGES_BASE}/zh/skills/{name}/index.html"
                    content = content.replace(f"]({relative})", f"]({target})")
                    content = content.replace(f"](docs/zh/skills/{name}/index.html)", f"]({target})")
                else:
                    old = f'href="https://github.com/TIKAZI/TIKAZ-AI-Skills/blob/main/{relative}"'
                    content = content.replace(old, f'href="skills/{name}/index.html"')
        document.write_text(content, encoding="utf-8")
    for suite_name in manifest["suites"]:
        suite = root / "suites" / suite_name
        for readme_name, language_root in (("README.md", "skills"), ("README.zh-CN.md", "zh/skills")):
            readme = suite / readme_name
            content = readme.read_text(encoding="utf-8")
            for name, _, skill_path in skills_for_suite(suite):
                relative = skill_path.relative_to(suite).as_posix()
                target = f"{PAGES_BASE}/{language_root}/{name}/index.html"
                content = content.replace(f"]({relative})", f"]({target})")
                content = content.replace(f"](../../docs/{language_root}/{name}/index.html)", f"]({target})")
            readme.write_text(content, encoding="utf-8")


def svg_lines(description: str, width: int = 94) -> list[str]:
    sentence = re.split(r"(?<=[.!?])\s+", description, maxsplit=1)[0]
    lines = textwrap.wrap(sentence, width=width, break_long_words=False, break_on_hyphens=False)
    if len(lines) <= 2:
        return lines
    return [lines[0], textwrap.shorten(" ".join(lines[1:]), width=width, placeholder="…")]


def diagram_svg(title: str, accent: str, skills: list[tuple[str, str, Path]]) -> str:
    width = 1440
    height = 440 + len(skills) * 126
    start_x = 126
    node_x = 260
    node_width = 1040
    node_height = 86
    first_y = 330
    title_safe = html.escape(title)
    nodes = []
    connectors = []
    for index, (name, description, _) in enumerate(skills):
        y = first_y + index * 126
        connectors.append(
            f'<path d="M{start_x} {y - 43} H{node_x}" stroke="#{accent}" stroke-width="2" fill="none" stroke-linecap="round"/>'
        )
        number = f"{index + 1:02d}"
        name_safe = html.escape(name)
        promise_lines = svg_lines(description)
        promise_svg = "".join(
            f'<tspan x="102" dy="{18 if line_index else 0}">{html.escape(line)}</tspan>'
            for line_index, line in enumerate(promise_lines)
        )
        nodes.append(
            f'<g transform="translate({node_x} {y - node_height})">'
            f'<rect width="{node_width}" height="{node_height}" rx="16" fill="#101827" stroke="#334155"/>'
            f'<rect width="6" height="{node_height}" rx="3" fill="#{accent}"/>'
            f'<text x="34" y="34" fill="#{accent}" font-size="13" font-weight="700" letter-spacing="2">{number}</text>'
            f'<text x="102" y="37" fill="#F8FAFC" font-size="23" font-weight="700">{name_safe}</text>'
            f'<text x="102" y="58" fill="#94A3B8" font-size="14">{promise_svg}</text>'
            f'</g>'
        )
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
<title id="title">{title_safe} workflow</title>
<desc id="desc">The suite orchestrator routes work through {len(skills) - 1} independently installable specialist Skills.</desc>
<rect width="{width}" height="{height}" rx="24" fill="#080D18"/>
<g font-family="Segoe UI, Arial, sans-serif">
<text x="92" y="84" fill="#{accent}" font-size="14" font-weight="700" letter-spacing="3">TIKAZ AI SKILLS FOR CODEX</text>
<text x="92" y="138" fill="#F8FAFC" font-size="40" font-weight="720">{title_safe} workflow</text>
<text x="92" y="176" fill="#CBD5E1" font-size="18">Install the suite for orchestration, or use any specialist on its own.</text>
<path d="M{start_x} {first_y - 43} V{first_y + (len(skills) - 1) * 126 - 43}" stroke="#{accent}" stroke-width="2" fill="none" stroke-linecap="round"/>
<circle cx="{start_x}" cy="{first_y - 43}" r="11" fill="#{accent}"/>
{''.join(connectors)}
{''.join(nodes)}
<text x="92" y="{height - 58}" fill="#94A3B8" font-size="13">Editable SVG · neutral structure · one suite accent · no raster generation</text>
</g>
</svg>'''


def catalog_markdown(root: Path, manifest: dict) -> str:
    rows = []
    count = 0
    for suite_name, info in manifest["suites"].items():
        suite = root / "suites" / suite_name
        for name, description, path in skills_for_suite(suite):
            count += 1
            kind = "Orchestrator" if path.parent == suite else "Specialist"
            rows.append(
                f"| [`{name}`]({PAGES_BASE}/skills/{name}/index.html) | {info['title'].replace('TIKAZ ', '').replace(' for Codex', '')} | {kind} | {short_promise(description, 170)} |"
            )
    return f'''# TIKAZ AI Skills Catalog

**{count} independently installable Skills across seven composable Codex workflows.**

[Open the public feedback form]({PAGES_BASE}/#feedback) · [Open GitHub Issue forms](https://github.com/TIKAZI/TIKAZ-AI-Skills/issues/new/choose)

Install an orchestrator for an end-to-end outcome. Install a specialist when the named output is the whole task. Every entry links to its canonical `SKILL.md`; suite READMEs provide human-facing examples and evidence.

| Skill | Suite | Role | Core promise |
|---|---|---|---|
{chr(10).join(rows)}

## Independent-use contract

Every Skill must state its trigger and accepted input, owned workflow, output contract, validation and fallback behavior, copy-ready examples, limits, and TIKAZ contribution. Detailed reference material belongs in suite-level `references/`; Skill folders stay concise.

{ATTRIBUTION}
'''


def generate(root: Path, output: Path) -> None:
    manifest = json.loads((root / "distribution" / "manifest.json").read_text(encoding="utf-8"))
    output.mkdir(parents=True, exist_ok=True)
    asset_output = output / "assets"
    asset_output.mkdir(parents=True, exist_ok=True)
    (asset_output / "tikaz-logo.svg").write_bytes((root / "assets" / "tikaz-logo.svg").read_bytes())
    (output / "feedback-data.js").write_text(feedback_data_javascript(root), encoding="utf-8")
    diagrams = output / "diagrams"
    diagrams.mkdir(parents=True, exist_ok=True)
    (output / "skills-catalog.md").write_text(catalog_markdown(root, manifest), encoding="utf-8")
    for suite_name, info in manifest["suites"].items():
        skills = skills_for_suite(root / "suites" / suite_name)
        title = info["title"].replace("TIKAZ ", "").replace(" for Codex", "")
        (diagrams / f"{suite_name}-workflow.svg").write_text(
            diagram_svg(title, info["accent"], skills), encoding="utf-8"
        )
    publish_skill_project_pages(root, output, manifest)
    if output.resolve() == (root / "docs").resolve():
        publish_project_entry_links(root, output, manifest)


def publish_suite_assets(root: Path, generated: Path) -> None:
    for workflow in (generated / "diagrams").glob("*-workflow.svg"):
        suite_name = workflow.name.removesuffix("-workflow.svg")
        assets = root / "suites" / suite_name / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        (assets / "workflow.svg").write_bytes(workflow.read_bytes())


def publish_metadata_and_pages(root: Path, manifest: dict) -> None:
    for suite_name, info in manifest["suites"].items():
        suite = root / "suites" / suite_name
        for name, description, path in skills_for_suite(suite):
            metadata = path.parent / "agents" / "openai.yaml"
            if not metadata.exists():
                metadata.parent.mkdir(parents=True, exist_ok=True)
                metadata.write_text(metadata_yaml(name, description), encoding="utf-8")
        if suite_name != "context-economy":
            (suite / "README.md").write_text(suite_readme(root, suite_name, info), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    destination = (args.output or repository_root / "docs").resolve()
    generate(repository_root, destination)
    if args.output is None:
        publish_suite_assets(repository_root, destination)
        manifest = json.loads((repository_root / "distribution" / "manifest.json").read_text(encoding="utf-8"))
        publish_metadata_and_pages(repository_root, manifest)
