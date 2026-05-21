# Out-of-Scope Knowledge Base

仓库里的 `.out-of-scope/` 目录用于持久记录被拒绝的功能请求。它有两个目的：

1. **组织记忆**：记录某个功能为什么被拒绝，避免 issue 关闭后理由丢失
2. **去重**：新 issue 与历史拒绝相似时，skill 可以提出之前的决策，而不是重新辩论一遍

## 目录结构

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

每个**概念**一个文件，不是每个 issue 一个文件。多个 issue 请求同一件事时，归到同一个文件下。

## 文件格式

文件应该用宽松、易读的风格写，更像短设计文档，而不是数据库记录。使用段落、代码示例和例子，让第一次看到它的人也能理解理由。

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42 — "Add dark mode support"
- #87 — "Night theme for accessibility"
- #134 — "Dark theme option"
```

### 文件命名

使用短而清楚的 kebab-case 概念名：`dark-mode.md`、`plugin-system.md`、`graphql-api.md`。文件名应足够可识别，让浏览目录的人不用打开文件也知道被拒绝的是什么。

### 写理由

理由要有实质内容，不是 “we don't want this”，而是为什么。好的理由会引用：

- 项目范围或理念（“This project focuses on X; theming is a downstream concern”）
- 技术约束（“Supporting this would require Y, which conflicts with our Z architecture”）
- 战略决策（“We chose to use A instead of B because...”）

理由应该耐久。避免引用临时情况（“we're too busy right now”）；那不是实际拒绝，而是延期。

## 何时检查 `.out-of-scope/`

分诊时（Step 1: Gather context）读取 `.out-of-scope/` 中所有文件。评估新 issue 时：

- 检查请求是否匹配已有 out-of-scope 概念
- 匹配看概念相似度，不只看关键词；“night theme” 可以匹配 `dark-mode.md`
- 如果匹配，告诉 maintainer：“This is similar to `.out-of-scope/dark-mode.md`; we rejected this before because [reason]. Do you still feel the same way?”

Maintainer 可以：

- **Confirm**：把新 issue 加到已有文件的 “Prior requests” 列表，然后关闭
- **Reconsider**：删除或更新 out-of-scope 文件，让 issue 进入正常分诊
- **Disagree**：两个 issues 相关但不同，继续正常分诊

## 何时写入 `.out-of-scope/`

只有 **enhancement**（不是 bug）被拒绝为 `wontfix` 时才写。流程：

1. Maintainer 决定某个 feature request 不在范围内
2. 检查是否已经存在匹配的 `.out-of-scope/` 文件
3. 如果存在，把新 issue 追加到 “Prior requests” 列表
4. 如果不存在，用概念名、decision、reason 和第一个 prior request 创建新文件
5. 在 issue 上发布 comment 解释决策，并提到 `.out-of-scope/` 文件
6. 使用 `wontfix` label 关闭 issue

## 更新或移除 out-of-scope 文件

如果 maintainer 改变了对某个历史拒绝概念的看法：

- 删除 `.out-of-scope/` 文件
- skill 不需要重新打开旧 issues；它们是历史记录
- 触发重新考虑的新 issue 继续走正常分诊
