---
name: review
description: 当用户想 review 一个 branch、PR、work-in-progress changes，或要求 "review since X" 时，从固定点开始按 Standards 和 Spec 两个轴并行审查变更。
---

# Review

审查用户提供的 fixed point 和 `HEAD` 之间的 diff，分成两个轴：

- **Standards**：代码是否符合这个仓库记录下来的 coding standards？
- **Spec**：代码是否忠实实现了源 issue / PRD / spec 要求？

两个轴分别由**并行子代理**执行，避免互相污染上下文；这个 skill 负责汇总发现。

Issue tracker 应该已经提供给你；如果缺少 `docs/agents/issue-tracker.md`，先运行 `/setup-matt-pocock-skills`。

## 流程

### 1. 固定比较点

用户说的就是 fixed point：commit SHA、branch name、tag、`main`、`HEAD~5` 等。不要擅自解释，原样传入。如果用户没指定，问：“Review against what — a branch, a commit, or `main`?” 拿到答案前不要继续。

记录一次 diff command：`git diff <fixed-point>...HEAD`（three-dot，和 merge-base 比较）。同时用 `git log <fixed-point>..HEAD --oneline` 记录 commits 列表。

### 2. 找到 spec 来源

按顺序查找源 spec：

1. Commit messages 中的 issue references（`#123`、`Closes #45`、GitLab `!67` 等），按 `docs/agents/issue-tracker.md` 中的 workflow 获取。
2. 用户参数中传入的路径。
3. `docs/`、`specs/` 或 `.scratch/` 下与 branch name 或 feature 匹配的 PRD/spec 文件。
4. 如果找不到，询问用户 spec 在哪里。如果用户说没有 spec，**Spec** 子代理跳过，并报告 “no spec available”。

### 3. 找到 standards 来源

收集仓库中记录“代码应该如何写”的任何文件。常见位置：

- `CLAUDE.md`、`AGENTS.md`
- `CONTRIBUTING.md`
- `CONTEXT.md`、`CONTEXT-MAP.md`、per-context `CONTEXT.md`
- `docs/adr/`（架构决策也是 standards）
- `.editorconfig`、`eslint.config.*`、`biome.json`、`prettier.config.*`、`tsconfig.json`（机器强制的 standards，记录它们但不要重复检查 tooling 已经检查的内容）
- repo root 或 `docs/` 下任何 `STYLE.md`、`STANDARDS.md`、`STYLEGUIDE.md` 或类似文件

收集文件列表，交给 **Standards** 子代理读取。

### 4. 并行启动两个子代理

发送一条消息，包含两个 `Agent` tool calls。两个都用 `general-purpose` subagent。

**Standards sub-agent prompt** 包含：

- 完整 diff command 和 commit list。
- 步骤 3 找到的 standards-source files 列表。
- Brief："Read the standards docs. Then read the diff. Report — per file/hunk where relevant — every place the diff violates a documented standard. Cite the standard (file + the rule). Distinguish hard violations from judgement calls. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** 包含：

- diff command 和 commit list。
- spec 路径或获取到的 spec 内容。
- Brief："Read the spec. Then read the diff. Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

如果缺少 spec，跳过 Spec 子代理，并在最终报告中说明。

### 5. 汇总

把两个报告分别放在 `## Standards` 和 `## Spec` 标题下，原样或轻微清理。不要合并或重新排序 findings；两个轴刻意分开，让用户能独立看见它们。

最后给一行 summary：每个轴的 finding 总数，以及最严重的单个问题（如有）。

## 为什么分成两个轴

一个变更可能通过一个轴、失败另一个轴：

- 代码符合所有标准，但实现了错误的东西 -> **Standards pass, Spec fail.**
- 代码完全实现 issue 要求，但违反项目约定 -> **Spec pass, Standards fail.**

分开报告可以避免一个轴遮住另一个轴。
