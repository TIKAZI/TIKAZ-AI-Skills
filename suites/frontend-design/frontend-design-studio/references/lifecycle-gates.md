# 项目闭环与阶段门

## 适用范围

对新网站、大改版、需要预览或生产部署的任务使用完整闭环。单文件视觉修复可跳过状态机，但仍需运行受影响检查和渲染验证。

## 初始化

先解析 Skill 绝对目录，然后运行：

```powershell
python '<skill-root>/scripts/manage_frontend_project.py' init --project '<project-path>' --name '<project-name>' --surface '<surface>' --platform web
```

命令只创建不存在的 `BRIEF.md`、`DESIGN.md`、`QA.md`、`.design-frontend-studio/state.json` 和 `.design-frontend-studio/references.json`，默认拒绝覆盖。状态文件只记录非敏感事实、证据路径与门禁结果。脚本要求 Python 3.9+；按环境使用 `python`、`python3` 或 Windows 的 `py -3`。

## 阶段

| 阶段 | 必须形成的事实或证据 | 退出门 |
|---|---|---|
| Intake | 页面类型、用户、主任务/CTA、范围、内容、仓库、访问条件、质量目标 | brief 字段完整并获批准 |
| Research | 结构、视觉、动效所需的 2–3 类证据；组件依赖与许可；内容 claim 来源 | research complete，未知许可组件不得进入实现 |
| Design | 页面结构、真实草稿、方向、tokens、组件状态、动效主张 | 用户或明确代理人批准 `DESIGN.md` 版本 |
| Implementation | 基线命令与 git 状态、变更边界、依赖清单、静态和动态实现 | 生产构建通过，需求可追踪到验证方法 |
| Local QA | 自动检查、桌面/移动、状态、键盘、触控、reduced motion、控制台 | blocker/major 清零 |
| Preview | 预览 URL、revision、内容/视觉/功能/许可签收 | preview approved |
| Production | build ID、环境、配置差异、前一版本和回滚命令 | production release succeeded |
| Smoke | 核心业务链路、深链/404、资产、表单、TLS、缓存、SEO/OG、日志 | smoke passed；关键失败立即回滚 |
| Observation | 约定观察期、错误与用户反馈 | observation complete |
| Learning | 实际偏差、可复用结论、反例、用户或客观验收 | 只把有证据的结论回写设计契约或个人知识 |

## 状态更新和门禁

更新单个字段：

```powershell
python '<skill-root>/scripts/manage_frontend_project.py' set --project '<project-path>' --key brief.approved --value true
```

查看状态或验证门：

```powershell
python '<skill-root>/scripts/manage_frontend_project.py' status --project '<project-path>'
python '<skill-root>/scripts/manage_frontend_project.py' gate --project '<project-path>' --name implement
```

可用门：`implement`、`preview`、`production`、`close`。门失败时输出缺失条件；门通过时自动推进 `phase`。顺序不可跳跃或倒退：`implement` 只从 intake/design/implementation，`preview` 只从 implementation/preview，`production` 只从 preview/production，`close` 只从 preview/production/closed 进入。`set` 只接受状态文件已有字段，且不能直接改 `phase`。

门禁同时验证状态与真实文件，不接受只改布尔值：

- `implement`：非空 `BRIEF.md`、`DESIGN.md` 的 frontmatter 均为 `status: approved`；两份批准证据路径存在；surface mode 有效；需要外部研究时至少两个不同 http(s) 来源，不需要时必须记录豁免理由和至少一个既有产品/设计/渲染证据；组件许可状态与依赖已解决；claim 状态和发布标记有效。
- `preview`：另需 `QA.md status: passed`、非空构建证据、revision、通过的桌面/移动艺术指导样片、八项 4-5 分视觉评分、分别存在的桌面与移动图片/录屏、评分证据文件，以及与当前 implementation revision 相同的 `qa.evidence_revision`。
- `production`：另需 `deployment.mode: production`、预览 URL、预览批准证据、部署目标和回滚记录。
- `close`：另需观察、验收、学习状态与实际学习证据；production 模式还需生产 URL 与 smoke 通过。

证据字段使用项目相对路径（推荐，便于移交）或绝对路径；目标必须存在且非空。桌面/移动视觉证据必须分别记录为图片或录屏，不能用任意文本文件替代。评分证据通常指向 `QA.md`，并写明对应 revision、视口、截图和具体判断。Markdown 自身可以作为批准/学习证据，但必须写明批准人或客观验收、时间、版本与结论。

部署模式只有三种：

- `none`：本地交付。完整 QA、观察、验收与学习后可 close，不要求 URL。
- `preview`：预览交付。close 必须有 `http(s)` preview URL、`preview_approved: true` 和实际批准证据。
- `production`：生产发布。必须先过 production 门；close 还需 production URL 与 smoke 结果。

范围、方向、依赖或线上证据变化时，用受控命令回到更早阶段；它会清除下游放行状态并记录原因。方向、tokens 或视觉世界变化必须回到 design，不能只回到 implementation：

```powershell
python '<skill-root>/scripts/manage_frontend_project.py' reopen --project '<project-path>' --phase design --reason '<visual direction changed>'
```

## 内容与来源账本

把参考、第三方组件和营销 claims 写入 `.design-frontend-studio/references.json`：

- `sources`: http(s) URL 或本地 `location`、访问时间、证据类别、借鉴原则、产品化变形、不可复制项。
- `sources` 的证据类别字段名为 `evidence_kind`。
- `components`: 名称、来源、框架、版本、依赖、`license_status`（`verified-compatible` / `not-used` / `approved-exception`）、`dependencies_resolved`、降级和实际使用位置。
- `claims`: 文案或指标、来源、状态 `verified` / `remove` / `draft-only`；`remove` 和 `draft-only` 必须显式 `published: false`。

同一 URL 与组件去重更新。放弃来源可以删除；若它支撑已批准决策，则保留并标记 `rejected` 及原因。截图保留到设计与 preview 批准；最终只保留 QA 引用的证据和必要对比图，其余临时截图清理。

## 缺陷与重试

- Blocker：核心任务不可用、数据或发布错误。立即停止放行。
- Major：重要状态、响应式、无障碍或动效降级失败。修复后才能 preview/production。
- Minor：不阻断任务的细节问题，可经明确记录后延期。
- 同一缺陷两次复现，停止局部补丁并做根因诊断；第三次仍失败时标记 blocked并附证据。
- 修复引入回归时恢复最近通过的检查点，再缩小变更。

## 重新入环条件

内容或范围重大变化回到 Intake；方向或 token 变化回到 Design；依赖、框架、浏览器目标或组件版本变化回到 Implementation/QA；上线错误、表单失败、指标异常或用户反馈触发 Smoke/QA；有客观新证据时才更新 Learning。
