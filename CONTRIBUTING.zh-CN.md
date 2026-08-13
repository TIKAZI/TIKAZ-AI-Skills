<p align="center"><a href="CONTRIBUTING.md">English</a> · <strong>简体中文</strong></p>

# 参与贡献

欢迎能够改善真实行为、证据、可迁移性或维护质量的贡献。仅仅改名、换顺序、增加品牌文字或重新发布已有 Skill，不视为有效改进。

## 贡献合同

1. 每个 Skill 必须可以单独使用，文件夹名称与 frontmatter 的 `name` 完全一致。
2. `SKILL.md` frontmatter 只能包含 `name` 和 `description`，触发条件写在 `description` 中。
3. 明确说明贡献类型和具体行为变化。不得用 TIKAZ 署名覆盖第三方作者、版权或许可证。
4. 新增或更新 `SOURCES.yml`，区分实际打包的上游内容与仅用于研究的参考资料。
5. 不添加许可证未知的第三方文件；允许派生或 Vendored 的内容必须保留原版权和许可证声明。
6. 不提交凭据、Cookie、私人知识库、用户绝对路径、编译缓存，也不承诺可选工具在所有环境中都可用。
7. 核心工作流保持简洁；详细方法放入直接链接的 `references/`，确定性工具放入 `scripts/`，输出资源放入 `assets/`。
8. 新增路由时，在套件 `references/routing.md` 中提供至少三个现实示例。
9. 英文 README 是默认源，中文 `README.zh-CN.md` 是完整用户文档镜像。两边必须同步能力、限制、安装方法与链接。
10. 运行 `pwsh -File .\scripts\validate_skills.ps1`，并在 Pull Request 中报告精确结果。

## 来源类型

- `original`：为本仓库原创。
- `clean-room`：研究公开问题或接口后独立编写，没有复制受保护的文字或代码。
- `adapter`：调用或连接独立安装工具的原创说明。
- `derived`：修改了有许可证的上游内容，必须保留通知并满足兼容许可证。
- `vendored`：大体保持上游文件不变地再分发，必须有明确理由；一般不接受简单搬运。

## Pull Request 证据

说明改了什么、为什么改；列出上游或研究来源和许可证；提供代表性调用、输出与验证证据。不能因为改了名称、措辞、顺序或视觉品牌，就把贡献描述成完全原创。
