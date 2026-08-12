# DESIGN.md 设计契约

## 目录

- 目的
- 文件结构
- 写作规则
- 反模板检查
- 更新规则

## 目的

把 `DESIGN.md` 作为产品视觉与交互的长期真源。YAML front matter 存放机器可读 tokens；正文说明设计意图、使用理由、组件行为和明确禁忌。Tokens 负责一致，具体 prose 负责让设计不落入模板。

## 文件结构

推荐顺序：

1. Design Read
2. Product and audience
3. Visual thesis and signature moment
4. Dials and rationale
5. Composition map
6. Art-direction proof
7. Colors and typography
8. Layout and responsive behavior
9. Surfaces, shapes, iconography, and assets
10. Components and states
11. Motion thesis and motion tokens
12. Content rules and anti-goals
13. Exceptions and platform notes

可以增加项目特有字段，但避免重复章节和同义 token。

## 写作规则

- 记录“为什么”和“何时使用”，不只记录数值。
- 先声明 Persuade、Operate、Read 或 Experience；不要让整个产品类型替代当前 surface 的目标。
- 写清 variance、motion、density 三个旋钮及项目理由，不继承固定默认值。
- 用真实产品对象描述视觉世界，例如仓储标签、编辑批注、实验仪器、街区导视；不要停在“高级、未来感、极简”。
- 只保留一个获批视觉世界；被放弃的方向不得继续贡献字体、颜色或动效。
- Composition map 为每个区块指定单一任务、layout family、contrast、media 和 motion role。
- Art-direction proof 必须引用首屏与代表区块的桌面/移动截图，通过后再扩展整页。
- Colors 包含背景、表面、文字、弱文字、边框、主色、状态色及对比用途。
- Typography 包含字体来源、回退、显示/正文/标签/数据角色、字宽和换行规则。
- Layout 包含容器、主轨/侧轨、间距、断点、密度和溢出策略。
- Components 说明组成、状态、变体、键盘与触控行为。
- Motion 同时记录用途、持续时间、缓动、触发、取消、中断和 reduced-motion 降级。

## 反模板检查

除非 brief 明确需要，否则避免：

- 用同尺寸图标卡片充当整个信息架构。
- 无意义的 `01/02/03`、eyebrow、胶囊标签和假技术 mono 字体。
- 默认紫蓝渐变、渐变文字、装饰性玻璃和每块内容都带阴影边框。
- 只有“巨型标题 + 小标签 + 两按钮”的通用 Hero。
- 三个等宽功能卡、三个等高价格塔、三条带圆点的评价轮播。
- 把 dashboard 做成装饰性数据，或把操作界面做成滚动叙事。

规则必须服从真实 brief。反模板不是反对常见模式，而是要求模式有明确的信息或行为理由。

## 更新规则

设计变更先更新契约，再修改多处实现。完成后把实际落地的偏差回写，删除已放弃方向，保留简短决策理由。通用规则与 brief 冲突时在 Exceptions 说明高优先级依据。外部 `design.md` CLI 可作为可选 lint/export 适配器；其格式仍可能变化，不把 Skill 强耦合到特定 CLI 版本。
