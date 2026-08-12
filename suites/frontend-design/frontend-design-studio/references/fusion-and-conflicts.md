# 规则融合与冲突裁决

## 目的

把不同资源放在正确层级。不要同时执行全部规则，也不要把多个视觉方向平均混合。

## 来源职责

| 来源 | 负责 | 不负责 |
|---|---|---|
| 用户 brief / 产品事实 | 目标、内容、受众、品牌、平台、边界 | 自动提供视觉答案 |
| Surface mode | 决定页面首先要说服、操作、阅读还是体验 | 具体配色和组件 |
| DESIGN.md | 已批准的唯一视觉世界与实现合同 | 临时灵感收藏 |
| Taste Skill | Persuade/Experience 的反默认偏差、构图野心、资产意识 | 后台/表格/复杂操作模式；绝对真理 |
| Impeccable | new-work 路由、critique/audit/polish、生产质量底线 | 在方向确定前替项目选风格 |
| design.md | 持久化 tokens、设计意图和 diff/lint 思路 | 自动创造审美 |
| Vue Bits / 21st.dev | 组件机制、动效实现候选 | 页面视觉语言、信息架构、统一许可 |
| 灵感网站 | 构图、节奏、交互证据 | 可复制的整页答案 |

## 优先级

发生冲突时按以下顺序裁决：

1. 真实内容、法律/许可、用户明确要求、平台惯例和无障碍需求。
2. Surface mode 与核心任务。
3. 既有品牌系统（preserve 模式）或获批 DESIGN.md（overhaul/greenfield）。
4. 适用于当前模式的 Taste 启发。
5. Impeccable 式 craft floor 与技术审查。
6. 组件库、动效库和灵感来源。

低优先级规则不得默默覆盖高优先级规则。确需例外时，在 DESIGN.md 的 `Exceptions` 记录原因、影响和验收方式。

## 已知冲突及裁决

| 冲突 | 裁决 |
|---|---|
| Taste 鼓励大胆、Impeccable Operate 强调克制 | Operate 保持可扫描和稳定，只在品牌细节、信息对比和关键反馈上大胆。 |
| Taste 的 landing 规则与 dashboard/app 冲突 | 不应用 landing hero、摄影、Awwwards 滚动叙事规则；采用成熟产品设计系统。 |
| Taste 要求 consumer 双主题 | 主题由 brief、品牌和产品需要决定，不默认强制 light+dark。 |
| Taste 偏好某些字体/图标库 | 既有项目、品牌和本环境设计约束优先。不要为了偏好替换稳定依赖。 |
| Taste 示例允许 `transition: all` | 始终禁止；列出实际属性。 |
| Taste 给出固定 Lighthouse/Core Web Vitals 数字 | 以产品目标或测得基线为准；标准指标只作参考，不伪装为已测试结果。 |
| Taste 倾向真实图片，Operate 缺少摄影 | 使用真实产品状态、图表、流程或可运行组件；不要塞无关 stock 图。 |
| “避免卡片”与信息确需容器 | 卡片只在表达独立对象、选择或层级时使用；页面区块不因装饰而卡片化。 |
| 一套规则说 centered hero 常见，brief 明确要求声明式居中 | brief 胜出，但必须用媒体、排版或交互让构图具有项目特征。 |
| 追求 originality 与已有品牌 preserve 冲突 | preserve 模式先保持识别度；用字体、节奏、细节和状态提高质量，不重置品牌。 |

## 反平均化协议

- 方向 A/B/C 之间只能选择，不做“取 A 的字体、B 的颜色、C 的动效”的拼盘。
- 设计过程中出现新灵感，先判断它是否属于当前视觉世界；不属于则记录为 rejected，不进入实现。
- 组件 demo 默认是反参考：保留行为，重做 tokens、比例、排版、内容和动效参数。
- critique 只能指出偏差和修复方向，不能在最后阶段偷偷引入第二种美学。

## 来源与时效

- Taste Skill: `Leonxlnx/taste-skill`, MIT；本地核心说明已读取，官方仓库核验于 2026-08-08。
- Impeccable: `pbakaus/impeccable`, Apache-2.0；Codex Skill v4.0.4 核验于 2026-08-08。
- 规则是本 Skill 的重新编排与摘要，不复制外部检测器或完整命令实现。

