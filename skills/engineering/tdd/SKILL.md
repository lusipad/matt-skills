---
name: tdd
description: 当用户想用 TDD 构建功能或修复 bug，提到 red-green-refactor、integration tests，或要求 test-first development 时使用。
---

# Test-Driven Development

## 哲学

**核心原则**：测试应通过公开接口验证行为，而不是验证实现细节。代码可以完全改变；测试不应该因此改变。

**好测试**是 integration-style：通过 public APIs 走真实代码路径。它描述系统做**什么**，而不是系统如何做。好测试读起来像 specification：“user can checkout with valid cart” 清楚说明存在什么能力。这样的测试能承受重构，因为它不关心内部结构。

**坏测试**和实现耦合。它 mock 内部协作者、测试 private methods，或绕过接口验证（例如直接查数据库，而不是通过接口验证）。警告信号：行为没有变，只是重构后测试坏了。如果重命名内部函数导致测试失败，这些测试测的是实现，不是行为。

示例见 [tests.md](tests.md)，mocking 指南见 [mocking.md](mocking.md)。

## 反模式：Horizontal Slices

**不要先写所有测试，再写所有实现。** 这是 horizontal slicing，把 RED 理解成“写完所有测试”，把 GREEN 理解成“写完所有代码”。

这会产生**糟糕测试**：

- 批量写出的测试验证的是想象中的行为，不是真实学到的行为
- 你会开始测试东西的形状（数据结构、函数签名），而不是用户可见行为
- 测试对真实变化不敏感：行为坏了却通过，行为没坏却失败
- 你跑到 headlights 之外，在理解实现前就承诺了测试结构

**正确做法**：通过 tracer bullet 做 vertical slices。一个测试 -> 一个实现 -> 重复。每个测试都回应上一轮学到的东西。因为你刚写完代码，所以你知道哪些行为重要，以及如何验证。

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## 工作流

### 1. Planning

探索代码库时，使用项目领域 glossary，让测试名和接口词汇匹配项目语言，并尊重即将触碰区域的 ADR。

写任何代码前：

- [ ] 和用户确认需要哪些接口变化
- [ ] 和用户确认要测试哪些行为，并排序优先级
- [ ] 识别 [deep modules](deep-modules.md) 机会（小接口，深实现）
- [ ] 为 [testability](interface-design.md) 设计接口
- [ ] 列出要测试的行为，而不是实现步骤
- [ ] 获得用户对计划的批准

询问：“公开接口应该长什么样？哪些行为最值得测试？”

**你无法测试一切。** 和用户确认哪些行为最重要。把测试精力集中在 critical paths 和复杂逻辑，而不是每个可能边界。

### 2. Tracer Bullet

写一个测试，确认系统的一件事：

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

这是 tracer bullet，用来证明这条路径端到端可行。

### 3. 增量循环

对每个剩余行为：

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

规则：

- 一次只写一个测试
- 只写足够让当前测试通过的代码
- 不预判未来测试
- 测试聚焦可观察行为

### 4. Refactor

所有测试通过后，寻找 [refactor candidates](refactoring.md)：

- [ ] 抽出重复
- [ ] 加深模块（把复杂性移到简单接口背后）
- [ ] 在自然适用处应用 SOLID principles
- [ ] 思考新代码暴露了哪些现有代码问题
- [ ] 每一步重构后都运行测试

**RED 时永远不要重构。** 先回到 GREEN。

## 每轮 checklist

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
