# Matt Pocock Skills

一组 agent skills（slash commands 和 behaviors），同时打包给 Codex 和 Claude Code。Skills 按 bucket 组织，并由 `/setup-matt-pocock-skills` 生成的 per-repo configuration 消费。

## 语言

**Issue tracker**：
承载仓库 issues 的工具，例如 GitHub Issues、Linear、本地 `.scratch/` markdown 约定或类似系统。`to-issues`、`to-prd`、`triage`、`qa` 等 skills 会读写它。
_Avoid_: backlog manager、backlog backend、issue host

**Issue**：
**Issue tracker** 中被跟踪的单个工作单元，可以是 bug、task、PRD，或 `to-issues` 产出的 slice。
_Avoid_: ticket（只有引用外部系统原话时才使用 ticket）

**Triage role**：
分诊时应用到 **Issue** 上的 canonical state-machine label，例如 `needs-triage`、`ready-for-afk`。每个 role 都会通过 `docs/agents/triage-labels.md` 映射到 **Issue tracker** 中真实使用的 label 字符串。

## 关系

- 一个 **Issue tracker** 持有多个 **Issues**
- 一个 **Issue** 同一时间携带一个 **Triage role**

## 已标记歧义

- “backlog” 过去同时表示承载 issues 的工具和工具里的工作集合。已解决：工具称为 **Issue tracker**；“backlog” 不再作为领域术语使用。
- “backlog backend” / “backlog manager” 已解决：合并为 **Issue tracker**。
