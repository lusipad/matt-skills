---
name: grill-with-docs
description: 当用户想用项目语言和已有决策来压力测试计划、澄清领域术语，并在过程中更新 CONTEXT.md 或 ADR 时使用。
---

<what-to-do>

围绕这个计划持续追问我，直到我们形成共享理解。沿着设计树逐个分支推进，一次解决一个决策依赖。每次提问时，都给出你推荐的答案。

一次只问一个问题，等我反馈后再继续。

如果某个问题可以通过探索代码库回答，就先探索代码库，不要把问题抛给我。

</what-to-do>

<supporting-info>

## 领域意识

探索代码库时，同时查找已有文档：

### 文件结构

大多数仓库只有一个上下文：

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

如果根目录存在 `CONTEXT-MAP.md`，说明仓库有多个上下文。这个 map 会指出每个上下文的位置：

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

按需创建文件：只有真的有内容可写时才创建。如果没有 `CONTEXT.md`，在第一个术语被确认时创建。如果没有 `docs/adr/`，在第一份 ADR 被确认需要时创建。

## 追问过程中

### 对照词汇表

当用户使用的术语和 `CONTEXT.md` 里的现有语言冲突时，立即指出：“你的 glossary 把 'cancellation' 定义为 X，但你现在似乎在表达 Y。这里到底是哪一个？”

### 收紧模糊语言

当用户使用模糊或 overloaded 的词时，提出更精确的 canonical term：“你说的 'account'，指的是 Customer 还是 User？它们不是同一个概念。”

### 讨论具体场景

讨论领域关系时，用具体场景压力测试它们。主动构造能触碰边界条件的场景，迫使概念边界变清楚。

### 与代码交叉验证

当用户描述某件事如何工作时，检查代码是否同意。如果发现矛盾，直接指出：“代码里取消的是整个 Order，但你刚刚说可以部分取消。哪个才是对的？”

### 即时更新 CONTEXT.md

当一个术语被确认后，立刻更新 `CONTEXT.md`。不要攒到最后再批量处理；趁上下文还新鲜时记录下来。格式参考 [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)。

`CONTEXT.md` 不应包含实现细节。不要把它当 spec、草稿纸或实现决策仓库。它只是 glossary。

### 谨慎提供 ADR

只有同时满足三点时，才建议创建 ADR：

1. **难以逆转**：以后改主意会付出明显成本。
2. **缺少上下文会显得反常**：未来读者会问“为什么这样做？”。
3. **来自真实权衡**：确实存在可行备选方案，而团队基于具体原因选择了其中一个。

如果缺少任何一点，就跳过 ADR。格式参考 [ADR-FORMAT.md](./ADR-FORMAT.md)。

</supporting-info>
