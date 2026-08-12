# 命令路由与调用示例

## 常用动作

| 动作 | 适用请求 | 结果 |
|---|---|---|
| shape | 先定结构和视觉方向 | Design Read、方向卡、DESIGN.md 草案、样片计划 |
| build | 新建或按获批方向实现 | 可运行前端、样片门、完整页面与 QA |
| critique | 只诊断不修改 | 按严重度排序的视觉与 UX finding |
| bolder | 页面普通、保守、模板化 | 更强焦点、构图、媒体和 signature moment |
| distill | 页面杂乱、风格冲突、信息平均 | 删除重复语法，统一世界，重建主次 |
| polish | 概念正确但完成度不足 | 有界细节修复，不换设计方向 |
| audit | 上线前技术检查 | a11y、响应式、状态、性能、构建证据 |

## 推荐调用

新网站：

```text
使用 frontend-design-studio build。先给 Design Read 和最多 3 个实质不同方向，推荐一个；先做首屏+代表区块样片并截图验收，通过后再完成整页。目标用户是……，主 CTA 是……，不要……
```

页面普通：

```text
使用 frontend-design-studio bolder。保留功能和真实内容，重做视觉层级与首屏构图，只保留一个 signature moment；桌面和移动端截图对比后再交付。
```

页面杂乱：

```text
使用 frontend-design-studio distill。先列出冲突的视觉系统和重复区块，再删除；不要只换颜色。提纯后重新建立主焦点，并用相同视口复核。
```

只评审：

```text
使用 frontend-design-studio critique，不改代码。分别做视觉/产品评审和实现评审，按 blocker/major/minor 输出截图证据。
```

App/EXE：

```text
使用 frontend-design-studio build，surface mode 设为 Operate。保持平台原生导航与窗口行为，不套 Landing Page；先完成核心工作区和完整状态，再加入克制的品牌细节和动效。
```

## 最小输入

用户不必写完整 brief。最有价值的输入是：产品/页面是什么、谁使用、核心动作、必须保留什么、明确讨厌什么、已有品牌/图片/截图、目标平台。其余低风险内容由 Skill 从仓库和上下文推断。

## 不推荐调用

- “参考这些网站全部融合一下”：会造成视觉平均化。改为指定想借鉴的关系，例如构图、摄影、转场或信息节奏。
- “多加点动效高级感”：没有叙事目的。改为说明希望突出哪一步、哪种状态或哪段故事。
- “像 Awwwards 但又像企业后台”：先拆成 marketing 的 Persuade 和产品内页的 Operate，两套 surface brief 共享品牌 tokens，不共享构图规则。
