# 灵感与实现来源

## 使用原则

先提出具体问题，再选来源。动态站点必须实际浏览并观察时间、滚动、hover、触控和转场；文本抓取只能确认结构与说明。每个方向组合两到三个不同来源，并回到本产品内容和约束中重构，避免整页仿制。

## 来源分工

| 来源 | 最适合回答 | 不应承担 |
|---|---|---|
| [Landing Love](https://www.landing.love/) | Hero 动画、转场、微交互、动态落地页 | 技术实现和许可判断 |
| [Land-book](https://land-book.com/) | 成熟商业版式、行业与页面类型参考 | 实验性动效完整细节 |
| [Awwwards](https://www.awwwards.com/) | 实验视觉、叙事、交互趋势和高上限案例 | 默认生产可行性或性能保证 |
| [One Page Love](https://onepagelove.com/) | 单页站结构、信息节奏、转化路径 | 复杂产品后台架构 |
| [Lapa Ninja](https://www.lapa.ninja/) | 按行业、风格、区块寻找 Landing 模式 | 动效源码和框架兼容性 |
| [21st.dev](https://21st.dev/) | React/shadcn 组件、实现 prompt 和模式 | Vue 直接安装或统一许可假设 |
| [SiteInspire](https://www.siteinspire.com/) | 按风格、类型、行业形成视觉方向板 | 组件实现细节 |
| [Vue Bits](https://vue-bits.dev/) | Vue 动效预览、参数和单组件实现 | 个人收藏的链接分享 |

Landing Love / Lapa Ninja 主要看运动证据；One Page Love 看区块结构；Land-book / SiteInspire 看成熟商业审美；只在需要实验突破时提高 Awwwards 权重。

遇到登录墙、反爬或不可见动态时，记录限制并换用官方页面、仓库或用户提供截图。不要绕过访问控制。

## 研究记录

每条记录包含：URL 或本地 location、访问日期、研究问题、借鉴原则、如何转成当前产品规则、禁止复制项、框架、依赖、许可状态和证据类型。新建 Persuade/Experience 或替换视觉世界时默认使用 2–3 个互补外部来源；仅当结构、视觉语言和运动机制都需要独立证据时要求至少三个。小型既有界面、严格 brand-preserve、纯 Operate/Read 改造可将 `external_sources_required` 设为 false，但必须记录豁免理由，并把至少一个既有产品、设计系统、源文件或真实渲染写入 `location`。不要为了过门填无关灵感链接。重新生成品牌资产、文案、比例、tokens 和动效参数。

## 已核验外部项目

核验日期：2026-08-08（Vue Bits 收藏行为仍沿用 2026-08-03 的实测）。90 天后、网站行为变化、组件升级或许可异常时重新检查官方来源，并更新访问日期和证据。

- [google-labs-code/design.md](https://github.com/google-labs-code/design.md)：以 `DESIGN.md` 结合机器 tokens 与人类设计意图；CLI 提供 lint/diff/export，但格式仍可能演进。Apache-2.0。
- [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)：适用于 landing、portfolio 和 redesign 的反默认偏差、三个视觉旋钮、资产意识和 pre-flight 思路；其核心文件明确不负责 dashboard、复杂产品 UI 或原生移动。MIT。
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable)：v4.0.4 的 surface mode、new-work、critique/audit/polish 和有界评审思路适用于更广泛 UI。Apache-2.0。
- [DavidHDev/vue-bits](https://github.com/DavidHDev/vue-bits)：Vue 动效与组件来源；收藏实现使用浏览器 localStorage。MIT + Commons Clause。
- [21st.dev Terms](https://21st.dev/terms)：多作者组件需逐项检查权属和许可；不要未经允许批量抓取或再分发站点内容。

本 Skill 只提炼职责边界、工作流与设计原则，并以中文优先级重新实现；未复制 Taste Skill 的完整禁令、Impeccable 的检测器/命令脚本或组件代码。Taste 负责适用页面的视觉上限，Impeccable 负责成型后的评审与工程下限，冲突按 `fusion-and-conflicts.md` 裁决。
