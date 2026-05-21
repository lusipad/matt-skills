---
name: to-prd
description: 当用户想基于当前对话上下文创建 PRD 时，把已有上下文整理成 PRD，并发布到项目 issue tracker。
---

这个 skill 使用当前对话上下文和代码库理解来生成 PRD。不要再采访用户；只综合你已经知道的信息。

Issue tracker 和 triage label vocabulary 应该已经提供给你；如果没有，先运行 `/setup-matt-pocock-skills`。

## 流程

1. 如果还没有探索过仓库，先探索代码库当前状态。PRD 全文使用项目领域 glossary 的词汇，并尊重即将触碰区域的 ADR。

2. 勾勒完成实现需要新建或修改的主要模块。主动寻找可以抽出深模块、并能独立测试的机会。

深模块不同于浅模块：它把大量功能封装在简单、可测试、很少变化的接口后面。

和用户确认这些模块是否符合预期。确认用户希望哪些模块写测试。

3. 使用下面模板写 PRD，然后发布到项目 issue tracker。应用 `ready-for-agent` triage label，不需要额外分诊。

<prd-template>

## Problem Statement

从用户视角描述用户正在面对的问题。

## Solution

从用户视角描述解决方案。

## User Stories

写一个很长的编号 user stories 列表。每条 user story 使用格式：

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

这个列表要尽可能完整，覆盖 feature 的各个方面。

## Implementation Decisions

列出已经做出的实现决策，可以包括：

- 将要新建或修改的模块
- 将要修改的模块接口
- 来自开发者的技术澄清
- 架构决策
- Schema 变更
- API contracts
- 具体交互

不要包含具体文件路径或代码片段。它们很容易快速过期。

例外：如果 prototype 产出的片段比 prose 更准确地表达了某个决策（状态机、reducer、schema、type shape），可以把它内联到相关 decision 中，并简短注明它来自 prototype。只保留承载决策的部分，不要放完整 demo。

## Testing Decisions

列出已经做出的测试决策，包括：

- 什么算好测试：只测试外部行为，不测试实现细节
- 哪些模块需要测试
- 代码库中可参考的已有测试 prior art

## Out of Scope

描述这个 PRD 明确不包含的事项。

## Further Notes

关于这个 feature 的其它备注。

</prd-template>
