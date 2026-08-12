# 视觉评审、加粗、提纯与打磨

## 分离评审类型

视觉评审先于实现审计，避免技术 finding 锚定审美判断。

### Visual/product pass

按顺序检查：

1. Mode success：说服、操作、阅读或体验目标是否成立。
2. Focal hierarchy：第一、第二、第三注意层级是否明确。
3. Composition：页面 silhouette、区块节奏和留白是否有意图。
4. Distinctiveness：Persuade/Experience 看遮住品牌后是否仍有项目特征；Operate 看任务模型、信息组织和状态反馈是否针对真实工作，而不是要求装饰性独特；Read 看内容结构和阅读工具是否贴合材料。
5. Coherence：字体、媒体、颜色、形状、图标、材质和 motion 是否属于同一世界。
6. Content truth：真实内容是否主导，装饰与虚构数据是否退场。
7. Responsive art direction：移动版是否保留意图而非机械堆叠。

### Implementation pass

检查响应式、溢出、状态、键盘、触控、reduced motion、控制台、网络、构建、性能和资源清理。

## 视觉 blocker

以下任一项存在时不能交付：

- 第一视口没有清楚主对象、主任务或主 CTA。
- 所有元素权重相近，没有主次。
- 三个以上连续区块重复同一构图语法。
- 页面主要由同质卡片、胶囊、eyebrow 或装饰指标组成。
- 两种以上字体/颜色/形状/材质系统争夺主导权。
- 重要区域依赖无意义渐变、假截图、空洞插图或无关 stock 图。
- DESIGN.md 声称的 signature moment 或 motion 没有真实实现。
- 移动端出现文本溢出、遮挡、失序或只剩长条堆叠。

## `bolder`

用于“安全、普通、像模板”。保持产品事实不变，按优先级强化：

1. 放大主次差距，而不是全体放大。
2. 重组首屏 silhouette 和负空间。
3. 让一个真实媒体/产品状态成为主视觉。
4. 提高颜色比例、材质或字体角色的明确性。
5. 增加一个可解释的 signature moment。

不要用更多渐变、阴影、卡片、动效数量伪装大胆。

## `distill`

用于“杂乱、多个风格、信息平均”。按优先级删除：

1. 不支持主任务的区块和重复 CTA。
2. 重复的容器、标签、eyebrow、图标与说明。
3. 第二套 accent、radius、shadow、字体或 motion 语言。
4. 无事实依据的指标、社会证明和装饰性产品预览。
5. 不改变理解或状态的动画。

提纯后必须重新建立焦点，不能只得到“空但普通”的页面。

## `polish`

概念不变，只处理：对齐、节奏、字宽、换行、颜色对比、图像裁切、状态一致性、交互反馈和 motion timing。一次批量截图、一次集中修复、一次确认后停止。

## 评分方式

用 1-5 分记录下列维度，并附截图证据：mode success、hierarchy、composition、distinctiveness、coherence、content/media、responsive、interaction craft。

- 任何维度 1-2：失败，必须修复。
- Contextual distinctiveness 低但其余高：执行 `bolder`。Operate/Read 的“独特”来自任务模型、信息组织与阅读工具，不要求装饰或实验构图。
- Coherence/hierarchy 低且元素过多：执行 `distill`。
- 所有维度至少 4：允许进入最后技术验收。

分数用于定位，不得把主观判断伪装成客观测量。必须同时说明具体视觉证据。
