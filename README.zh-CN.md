<p align="center"><a href="README.md">English</a> · <strong>简体中文</strong></p>

<p align="center">
  <img src="assets/tikaz-ai-skills-hero.svg" alt="TIKAZ AI Skills for Codex：七套可组合、证据优先的工作流" width="100%" />
</p>

<h1 align="center">TIKAZ AI Skills for Codex</h1>

<p align="center">
  <strong>面向 Codex 的可组合、可验证工作流集合</strong><br />
  把一次性提示词变成具备路由、证据、质量门和可移交产物的工作流。
</p>

<p align="center">
  <a href="https://github.com/TIKAZI/TIKAZ-AI-Skills/actions/workflows/validate.yml"><img src="https://github.com/TIKAZI/TIKAZ-AI-Skills/actions/workflows/validate.yml/badge.svg" alt="Skill 校验" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-f4c95d.svg" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/suites-7-60a5fa.svg" alt="7 套工作流" />
  <img src="https://img.shields.io/badge/skills-30-22d3ee.svg" alt="30 个 Skill" />
</p>

<p align="center">
  <a href="https://tikazi.github.io/TIKAZ-AI-Skills/zh/">中文网站</a> ·
  <a href="#60-秒开始">快速开始</a> ·
  <a href="#七套工作流">七套工作流</a> ·
  <a href="docs/skills-catalog.md">30 Skill 目录</a> ·
  <a href="CONTRIBUTING.zh-CN.md">参与贡献</a>
</p>

---

## ✨ 一个合集，七套工作流，一套质量合同

TIKAZ AI Skills 是由 **TIKAZ** 主导设计、整合、独立重构和持续维护的 Monorepo，面向 **Codex 及兼容 Skill 的宿主**。七套工作流放在一起，是因为真实任务经常跨越边界：Context Economy 可以整理最小可靠上下文，视频证据可以进入研究，研究可以变成演示文稿，确认后的设计可以交给工程流程实现。

```text
用户目标
   ↓
一个主工作流  →  仅在需要时调用专业 Skill
   ↓
结构化移交    →  证据 · 不确定性 · 来源 · 许可证
   ↓
质量门        →  渲染 · 测试 · 审查 · 产物证明
   ↓
验证后交付
```

本项目不是 OpenAI 官方仓库。英文是国际默认入口，中文是完整的一等文档镜像；30 个 `SKILL.md` 保持单一英文执行源，避免重复加载和双语版本漂移。

## 🧩 七套工作流

| 套件 | Skill 数 | 主要职责 | 典型路径 |
|---|---:|---|---|
| **[Context Economy](suites/context-economy/README.zh-CN.md)** | 5 | 高保真上下文准备 | pack → checkpoint → audit → benchmark |
| **[Video Intelligence](suites/video-intelligence/README.zh-CN.md)** | 2 | 可追溯的视频学习 | 来源 → 字幕/ASR → 关键帧 → 证据卡 → 综合 |
| **[Frontend Design](suites/frontend-design/README.zh-CN.md)** | 2 | 有辨识度的产品界面 | 页面类型 → Design Read → 方向样板 → 实现 → 视觉 QA |
| **[Engineering](suites/engineering/README.zh-CN.md)** | 6 | 安全的软件交付 | 规格 → 影响图 → 代码 → 测试 → 发布证据 |
| **[Knowledge & Research](suites/knowledge-research/README.zh-CN.md)** | 6 | 可追溯研究与决策 | 问题 → 来源 → 证据台账 → 分歧 → 建议 |
| **[Presentation](suites/presentation/README.zh-CN.md)** | 4 | 经验证的演示文稿 | 叙事 → 格式 → 页面合同 → 渲染 QA → 产物 |
| **[Visual Content](suites/visual-content/README.zh-CN.md)** | 5 | 可发布的内容资产 | 观点 → 风格 → Shot Card → 制作 → 发布 QA |

共有 **30 个可安装 Skill**，其中包含 7 个套件编排器。需要端到端结果时安装套件；只需要一种明确产物时，可以单独安装子 Skill。完整用途请查看 [30 Skill 目录](docs/skills-catalog.md)。

## 📦 60 秒开始

### 1. 克隆仓库

```bash
git clone https://github.com/TIKAZI/TIKAZ-AI-Skills.git
cd TIKAZ-AI-Skills
```

### 2. 安装一个 Skill

把套件或子 Skill 文件夹复制到 Codex 环境支持的 Skill 目录，目标文件夹名称必须与 `SKILL.md` 中的 `name` 一致。

```powershell
Copy-Item -Recurse `
  -LiteralPath '.\suites\frontend-design\frontend-design-studio' `
  -Destination '.\.agents\skills\frontend-design-studio'
```

### 3. 用自然语言调用

```text
Use frontend-design-studio to redesign this dashboard.
Approve one desktop/mobile representative proof before full implementation.
```

Skill 的执行说明保持英文，以获得更稳定的跨模型与工具兼容性；中文用户可以直接使用中文提出任务，中文 README 提供完整解释与示例。

## 🔄 为什么它不只是提示词合集

- **每个交付物只有一个负责人**：辅助 Skill 不争夺控制权。
- **证据随工作流传递**：时间戳、置信度、来源、许可证与未解决问题不会在移交中丢失。
- **先证明方向，再扩大生产**：前端、演示和视觉内容先验证代表性输出。
- **客观完成标准**：测试、构建、渲染产物与文件状态高于代理自信。
- **可迁移**：不写入私人绝对路径、凭据或对可选工具的普遍承诺。
- **来源可审计**：原创、Clean-room、适配、派生与引用材料明确区分。

## 📊 Context Economy 的证据边界

Context Economy 的定位是“高保真多模态上下文编译器”，不是万能 Token 压缩器。当前公开固定样例中，六个长上下文任务的估算 Token 从 `4,698` 降至 `1,422`，降低 **69.7%**；声明的受保护事实为 **46/46**，预期锚点为 **39/39**。短输入样例会增长 **143.9%**，这一负面结果也公开保留，用于证明协议并非在所有输入上都经济。

这些是限定数据集的证据，不是普遍节省承诺。真实 Provider Token、扫描 PDF 泛化、视觉语义准确率和下游盲测质量仍标记为 **Pending**。

## ✅ 验证

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File '.\scripts\validate_skills.ps1'
```

校验覆盖 30 个 Skill 的结构、独立使用合同、TIKAZ 贡献说明、来源政策、可迁移性、路由、UI 元数据和脚本语法。绿色校验代表仓库一致性，不代表当前环境一定具备所有平台权限或可选工具。

## ⚖️ 作者、来源与许可证

合集架构、TIKAZ Edition 工作流、路由合同、生命周期质量门、模板、可迁移规则和校验工具由 **TIKAZ** 主导设计、整合、独立重构并持续维护。

研究引用不会转移作者权。第三方来源、观察到的许可证、分发状态和具体 TIKAZ 贡献记录在 [SOURCES.yml](SOURCES.yml) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。TIKAZ 原创文件按 [MIT License](LICENSE) 发布。

## 🌐 探索 TIKAZ 项目

- [⚡ Context Economy](https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy) — 高保真多模态上下文编译与可复现证据。
- [🎨 Frontend Design](https://github.com/TIKAZI/TIKAZ-Codex-Frontend-Design) — 从视觉样板到实现的艺术指导型前端工作流。
- [🎬 Video Intelligence](https://github.com/TIKAZI/TIKAZ-Codex-Video-Intelligence) — 带证据分级的跨平台视频阅读与综合。
- [🛠️ Engineering](https://github.com/TIKAZI/TIKAZ-Codex-Engineering) — 从规格到发布的工程交付。
- [🔬 Knowledge & Research](https://github.com/TIKAZI/TIKAZ-Codex-Knowledge-Research) — 可追溯研究、决策和知识反馈。
- [📽️ Presentation](https://github.com/TIKAZI/TIKAZ-Codex-Presentation) — 叙事优先的 HTML 与可编辑 PowerPoint 生产。
- [🖼️ Visual Content](https://github.com/TIKAZI/TIKAZ-Codex-Visual-Content) — 配图、精简写作、合法音乐与发布 QA。
