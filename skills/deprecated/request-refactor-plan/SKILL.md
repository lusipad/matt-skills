---
name: request-refactor-plan
description: 当用户想规划重构、创建重构 RFC，或把重构拆成安全增量步骤时，通过用户访谈生成包含微小提交的详细重构计划，并归档为 GitHub issue。
---

当用户想创建重构请求时，调用这个 skill。按下面步骤执行；如果某步确实不需要，可以跳过。

1. 询问用户想解决的问题，以及他们已经想到的潜在方案。

2. 探索仓库，验证用户陈述，并理解代码库当前状态。

3. 询问用户是否考虑过其它选择，并主动提出可能的替代方案。

4. 围绕实现细节采访用户。要细致、彻底。

5. 确定具体实现范围。弄清楚计划改变什么，以及明确不改变什么。

6. 检查这片代码的测试覆盖。如果覆盖不足，询问用户的测试计划。

7. 把实现拆成极小的提交计划。记住 Martin Fowler 的建议：“make each refactoring step as small as possible so that the program is always working.”

8. 使用重构计划创建 GitHub issue。Issue description 使用下面模板：

<refactor-plan-template>

## Problem Statement

从开发者视角描述开发者正在面对的问题。

## Solution

从开发者视角描述问题的解决方案。

## Commits

一份长而详细的实现计划。用 simple English 写，把实现拆成尽可能小的 commits。每个 commit 都应该让代码库保持 working state。

## Implementation Decisions

列出已经做出的实现决策，可以包括：

- 将要新建或修改的模块
- 将要修改的模块接口
- 来自开发者的技术澄清
- 架构决策
- Schema changes
- API contracts
- 具体交互

不要包含具体文件路径或代码片段。它们很快会过期。

## Testing Decisions

列出已经做出的测试决策，包括：

- 什么算好测试：只测试外部行为，不测试实现细节
- 哪些模块需要测试
- 代码库中可参考的已有测试 prior art

## Out of Scope

描述这次重构明确不包含的事项。

## Further Notes (optional)

关于这次重构的其它备注。

</refactor-plan-template>
