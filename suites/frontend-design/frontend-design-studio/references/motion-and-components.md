# 动效与组件选择

## 目录

- 动效主张
- 时长与预算
- Vue Bits
- 21st.dev
- 选择矩阵
- 降级与验收

## 动效主张

先用一句话回答：页面中的运动如何帮助用户理解注意力、空间连续性或状态反馈？若答不出来，保持静态。

默认内容立即可见。入口可以增强表达，但不能成为读取内容的前置条件。退出通常比入口更快；避免反射性 bounce/elastic 和大面积持续运动。

## 时长与预算

| 类别 | 建议时长 | 例子 |
|---|---:|---|
| 即时反馈 | 100–150ms | pressed、toggle、短 hover |
| 常规状态 | 150–300ms | focus、菜单、tooltip、卡片状态 |
| 布局变化 | 300–500ms | 折叠、筛选、面板、共享元素 |
| 主焦点入场 | 500–800ms | Hero 或关键叙事段落，仅少量使用 |

每个视口只设置一个主要动态焦点；持续背景最多一个。优先使用 transform 和 opacity。滚动驱动只在滚动位置与叙事或空间关系有关时使用。

## Vue Bits

Vue Bits 适用于 Vue 项目的文本、进入、组件和背景动效候选。`/favorites` 收藏存放在当前浏览器的 `localStorage['savedComponents']`，同一链接不会分享收藏。

推荐映射：

- Hero：Blur Text、Split Text、Scroll Reveal、Gradient Text，保持标题可读且行数受控。
- 区块进入：Animated Content、Fade Content、轻量 stagger。
- 卡片反馈：Glare Hover、Border Glow、Spotlight Card、Tilted Card，避免同时叠加。
- 展示叙事：Scroll Stack、Card Swap、Carousel、Masonry。
- 背景气氛：Aurora、Particles、Threads、Grainient，只选一个并设静态 fallback。
- 操作反馈：Count Up、Click Spark 等短促效果；不要用于删除、支付或错误确认的唯一反馈。

避免在正文、表单、数据密集面板中使用 Glitch、Scramble、cursor trail 或持续 WebGL。移动端和低性能设备默认减少粒子、Three/OGL 和平滑滚动依赖。

Vue Bits 仓库使用 MIT + Commons Clause：通常可在应用和网站中使用与修改，但不得把组件本身作为组件包、模板或移植库销售或再分发。逐组件核对依赖与许可，保留适用声明。

## 21st.dev

21st.dev 主要是 React + Tailwind + shadcn 生态的多作者 registry。优先使用官方 Copy prompt、shadcn CLI 或页面交互选择组件；不要批量抓取站点、预览媒体或结构化元数据。逐作者组件核对许可。Vue 项目把它当行为和构图参考，不直接机械翻译 React 源码。

## 选择矩阵

为每个候选记录：

| 字段 | 必填判断 |
|---|---|
| 目的 | 注意力 / 连续性 / 反馈中的哪一个 |
| 框架 | Vue、React、Web Components、原生 CSS/JS |
| 依赖 | 新增包、包体、WebGL、滚动库 |
| 许可 | 来源、作者、许可、归属要求 |
| 输入方式 | 指针、键盘、触控、滚动 |
| 性能 | 主线程、GPU、持续渲染、图片/字体成本 |
| 降级 | reduced motion、触屏、低性能、无 JS |
| 验收 | 重复操作、中断、路由返回、移动端、真实设备 |

未完成矩阵的复杂动效不进入生产实现。

## 降级与验收

- 用 `@media (prefers-reduced-motion: reduce)` 关闭非必要移动、平滑滚动和自动播放，保留状态变化。
- 触屏不依赖 hover；键盘焦点与 pointer 状态具有等价信息。
- 动画被中断、重复触发或路由返回时不残留错误 transform、opacity 或锁定滚动。
- 关键文本、按钮和表单在脚本失败时仍可读取与操作。
- 浏览器控制台无动画库警告、重复注册、未清理监听器或 hydration 错误。
