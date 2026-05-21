---
name: setup-matt-pocock-skills
description: 在首次使用 to-issues、to-prd、triage、diagnose、tdd、improve-codebase-architecture 或 zoom-out 前，为仓库配置 Agent skills 块、议题跟踪系统、分诊标签词汇和领域文档布局。
---

# Setup Matt Pocock's Skills

为工程类 skills 搭建它们默认依赖的仓库级配置：

- **Issue tracker**：议题存放在哪里（默认 GitHub，也支持 local markdown）
- **Triage labels**：五个 canonical triage roles 对应的真实标签字符串
- **Domain docs**：`CONTEXT.md` 和 ADR 存放在哪里，以及读取规则

这是一个 prompt-driven skill，不是确定性脚本。先探索，再展示发现，向用户确认，然后写入文件。

## 流程

### 1. 探索

查看当前仓库的起点。已有内容都要读，不要假设：

- `git remote -v` 和 `.git/config`：这是 GitHub 仓库吗？是哪一个？
- 根目录的 `AGENTS.md` 和 `CLAUDE.md`：是否存在？其中是否已经有 `## Agent skills` 小节？
- 根目录的 `CONTEXT.md` 和 `CONTEXT-MAP.md`
- `docs/adr/` 和任何 `src/*/docs/adr/` 目录
- `docs/agents/`：这个 skill 以前的输出是否已经存在？
- `.scratch/`：是否已经在使用 local-markdown issue tracker 约定？

### 2. 展示发现并询问

总结哪些已经存在、哪些缺失。然后带用户逐个完成三个决策：一次只展示一个 section，拿到用户答案后再进入下一个。不要一次性把三个问题全抛出来。

假设用户不知道这些术语是什么意思。每个 section 都先用简短解释说明它是什么、为什么这些 skills 需要它、不同选择会改变什么。然后展示选项和默认值。

**Section A - Issue tracker.**

> 解释：Issue tracker 是这个仓库放议题的地方。`to-issues`、`triage`、`to-prd`、`qa` 等 skills 会读写它，所以它们需要知道应该调用 `gh issue create`，还是在 `.scratch/` 里写 markdown 文件，或遵循你描述的其它工作流。请选择你实际跟踪这个仓库工作的地方。

默认姿态：这些 skills 最初为 GitHub 设计。如果 `git remote` 指向 GitHub，就建议 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自托管 host），就建议 GitLab。否则，或用户偏好不同，就提供：

- **GitHub**：议题存在仓库的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab**：议题存在仓库的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **Local markdown**：议题是仓库 `.scratch/<feature>/` 下的文件（适合个人项目或没有 remote 的仓库）
- **Other**（Jira、Linear 等）：让用户用一段话描述工作流；这个 skill 会把它记录为 freeform prose

**Section B - Triage label vocabulary.**

> 解释：`triage` skill 处理传入议题时，会把它推进一个状态机：需要评估、等待报告者、已准备好由 AFK agent 接手、已准备好给人类处理，或 won't fix。为此，它需要应用与你实际配置一致的标签（或 issue tracker 中的等价状态）。如果你的仓库已经使用不同标签名，例如 `bug:triage` 而不是 `needs-triage`，就在这里映射，避免 skill 创建重复标签。

五个 canonical roles：

- `needs-triage`：maintainer 需要评估
- `needs-info`：等待报告者补充信息
- `ready-for-agent`：已经完整说明，AFK-ready，agent 可以在没有额外人类上下文的情况下接手
- `ready-for-human`：需要人类实现
- `wontfix`：不会处理

默认：每个 role 的标签字符串等于 role 名称。询问用户是否需要覆盖。如果 issue tracker 还没有标签，默认值就可以。

**Section C - Domain docs.**

> 解释：一些 skills（`improve-codebase-architecture`、`diagnose`、`tdd`）会读取 `CONTEXT.md` 学习项目领域语言，并读取 `docs/adr/` 了解过去的架构决策。它们需要知道仓库是一个全局 context，还是多个 context（例如 frontend/backend 分离的 monorepo），这样才能在正确位置查找。

确认布局：

- **Single-context**：根目录一个 `CONTEXT.md` + `docs/adr/`。大多数仓库是这样。
- **Multi-context**：根目录有 `CONTEXT-MAP.md`，指向每个 context 自己的 `CONTEXT.md`，通常用于 monorepo。

### 3. 确认并编辑

向用户展示草稿：

- 要加入仓库 agent instruction file 的 `## Agent skills` 块（选择规则见步骤 4）
- `docs/agents/issue-tracker.md`、`docs/agents/triage-labels.md`、`docs/agents/domain.md` 的内容

让用户在写入前可以修改。

### 4. 写入

**选择要编辑的文件：**

- 如果当前宿主 agent 是 Codex 且存在 `AGENTS.md`，编辑 `AGENTS.md`。
- 如果当前宿主 agent 是 Claude Code 且存在 `CLAUDE.md`，编辑 `CLAUDE.md`。
- 如果 `AGENTS.md` 或 `CLAUDE.md` 只有一个存在，编辑存在的那个。
- 如果两个都存在且用户要求同时支持两个 agent，两个都更新。
- 如果两个都存在但目标 agent 不清楚，询问要更新哪个文件。
- 如果两个都不存在，询问用户要创建哪一个，不要替用户选择。

当其中一个 instruction file 已经存在时，除非用户明确要求 dual-agent setup，否则不要创建另一个。

如果所选文件里已经有 `## Agent skills` 块，就原地更新内容，不要追加重复块。不要覆盖周围 section 中的用户编辑。

块内容：

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

然后用这个 skill 文件夹里的 seed templates 作为起点，写入三个 docs 文件：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md)：local-markdown issue tracker
- [triage-labels.md](./triage-labels.md)：label mapping
- [domain.md](./domain.md)：domain doc consumer rules + layout

对于 “other” issue tracker，根据用户描述从零写 `docs/agents/issue-tracker.md`。

### 5. 完成

告诉用户 setup 已完成，以及哪些工程 skills 会读取这些文件。提醒他们以后可以直接编辑 `docs/agents/*.md`；只有在切换 issue tracker 或想重新开始时，才需要重新运行这个 skill。
