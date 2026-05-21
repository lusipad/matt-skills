---
name: to-issues
description: 当用户想把计划、spec 或 PRD 转成实现议题，或把工作拆成可独立领取的任务时，用 tracer-bullet vertical slices 发布到项目 issue tracker。
---

# To Issues

用 vertical slices（tracer bullets）把计划拆成可以独立领取的议题。

Issue tracker 和 triage label vocabulary 应该已经提供给你；如果没有，先运行 `/setup-matt-pocock-skills`。

## 流程

### 1. 收集上下文

优先使用当前对话里已经存在的上下文。如果用户传入 issue reference（issue number、URL 或 path）作为参数，就从 issue tracker 获取它，并完整阅读 body 和 comments。

### 2. 探索代码库（可选）

如果还没有探索过代码库，先探索当前代码状态。Issue title 和 description 应使用项目领域 glossary 的词汇，并尊重即将触碰区域的 ADR。

### 3. 起草 vertical slices

把计划拆成 **tracer bullet** issues。每个 issue 都是一条很薄但端到端的 vertical slice，会穿过所有 integration layers，而不是某一层的 horizontal slice。

Slice 可以是 HITL 或 AFK。HITL slices 需要人类互动，例如架构决策或设计评审。AFK slices 可以在无人互动的情况下实现并合并。能选 AFK 时优先 AFK。

<vertical-slice-rules>
- 每个 slice 都交付一条窄但完整的端到端路径（schema、API、UI、tests）
- 完成的 slice 应该可以独立 demo 或验证
- 优先拆成多个薄 slice，而不是少数厚 slice
</vertical-slice-rules>

### 4. 询问用户

把拆分方案用编号列表展示。每个 slice 展示：

- **Title**：短而清楚的名称
- **Type**：HITL / AFK
- **Blocked by**：必须先完成哪些其它 slices（如有）
- **User stories covered**：覆盖哪些 user stories（如果源材料里有）

询问用户：

- 颗粒度是否合适？太粗还是太细？
- 依赖关系是否正确？
- 是否有 slice 应该合并或继续拆分？
- HITL 和 AFK 标记是否正确？

持续迭代，直到用户批准拆分方案。

### 5. 发布议题到 issue tracker

对每个已批准的 slice，在 issue tracker 新建一个 issue。使用下面的 issue body template。这些 issues 视为已经准备好给 AFK agents 接手，所以除非用户另有说明，发布时加上正确的 triage label。

按依赖顺序发布 issues（blockers 先发布），这样 “Blocked by” 字段可以引用真实 issue identifiers。

<issue-template>
## Parent

A reference to the parent issue on the issue tracker (if the source was an existing issue, otherwise omit this section).

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- A reference to the blocking ticket (if any)

Or "None - can start immediately" if no blockers.

</issue-template>

不要关闭或修改任何 parent issue。
