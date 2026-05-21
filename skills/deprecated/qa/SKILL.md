---
name: qa
description: 当用户想通过对话报告 bugs、做 QA、创建 issues，或提到 "QA session" 时，运行交互式 QA 会话，并把问题整理成 GitHub issues。
---

# QA Session

运行一次交互式 QA 会话。用户描述他们遇到的问题；你轻量澄清，后台探索代码库上下文，然后创建耐久、用户视角、使用项目领域语言的 GitHub issues。

## 对用户提出的每个问题

### 1. 倾听并轻量澄清

让用户用自己的话描述问题。最多问 **2-3 个短澄清问题**，聚焦：

- 他们期望发生什么，实际发生什么
- 复现步骤（如果不明显）
- 问题是稳定出现还是偶发

不要过度采访。如果描述已经足够创建 issue，就继续。

### 2. 后台探索代码库

一边和用户对话，一边启动一个 Agent（`subagent_type=Explore`）在后台理解相关区域。目标不是找修复方案，而是：

- 学习该区域使用的领域语言（检查 `UBIQUITOUS_LANGUAGE.md`）
- 理解这个 feature 应该做什么
- 识别用户可见行为边界

这些上下文能帮助你写出更好的 issue，但 issue 本身不要引用具体文件、行号或内部实现细节。

### 3. 判断范围：单个 issue 还是拆分？

创建前先判断这是**单个 issue**，还是需要**拆成多个 issues**。

需要拆分的情况：

- 修复跨多个独立区域，例如 “form validation 错了 AND success message 缺失 AND redirect 坏了”
- 存在明显可分离的关注点，不同人可以并行处理
- 用户描述了多个不同 failure modes 或 symptoms

保持单个 issue 的情况：

- 同一个地方的一个行为不对
- 所有症状都来自同一个根行为

### 4. 创建 GitHub issue(s)

使用 `gh issue create` 创建 issues。不要先让用户 review；直接创建并分享 URLs。

Issues 必须**耐久**，即使经过大重构也应该仍然说得通。用用户视角写。

#### 单个 issue

使用模板：

```
## What happened

[Describe the actual behavior the user experienced, in plain language]

## What I expected

[Describe the expected behavior]

## Steps to reproduce

1. [Concrete, numbered steps a developer can follow]
2. [Use domain terms from the codebase, not internal module names]
3. [Include relevant inputs, flags, or configuration]

## Additional context

[Any extra observations from the user or from codebase exploration that help frame the issue — e.g. "this only happens when using the Docker layer, not the filesystem layer" — use domain language but don't cite files]
```

#### 拆分为多个 issues

按依赖顺序创建 issues（blockers 先创建），这样可以引用真实 issue numbers。

每个 sub-issue 使用模板：

```
## Parent issue

#<parent-issue-number> (if you created a tracking issue) or "Reported during QA session"

## What's wrong

[Describe this specific behavior problem — just this slice, not the whole report]

## What I expected

[Expected behavior for this specific slice]

## Steps to reproduce

1. [Steps specific to THIS issue]

## Blocked by

- #<issue-number> (if this issue can't be fixed until another is resolved)

Or "None — can start immediately" if no blockers.

## Additional context

[Any extra observations relevant to this slice]
```

拆分时：

- **优先多个薄 issues，而不是少数厚 issues**：每个 issue 都应该能独立修复和验证
- **诚实标注 blocking relationships**：如果 B 确实必须等 A 修好才能测试，就写出来。如果独立，就标 “None — can start immediately”
- **按依赖顺序创建 issues**，这样 “Blocked by” 可以引用真实 issue numbers
- **最大化并行**：目标是多个人或多个 agents 可以同时领取不同 issues

#### 所有 issue body 的规则

- **不要写文件路径或行号**，它们会过期
- **使用项目领域语言**（如果存在，检查 `UBIQUITOUS_LANGUAGE.md`）
- **描述行为，不描述代码**：写 “the sync service fails to apply the patch”，不要写 “applyPatch() throws on line 42”
- **复现步骤必填**：无法确定时询问用户
- **保持简洁**：开发者应能在 30 秒内读完 issue

创建后，打印所有 issue URLs（总结 blocking relationships），并问：“Next issue, or are we done?”

### 5. 继续会话

持续进行，直到用户说结束。每个 issue 独立处理，不要批量攒起来。
