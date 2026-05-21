---
name: design-an-interface
description: 当用户想设计 API、探索接口选项、比较模块形状，或提到 "design it twice" 时，使用并行子代理为模块生成多个明显不同的接口设计。
---

# Design an Interface

基于《A Philosophy of Software Design》里的 “design it twice”：第一个想法很可能不是最好的。生成多个完全不同的设计，然后比较。

## 工作流

### 1. 收集需求

设计前先理解：

- [ ] 这个模块解决什么问题？
- [ ] 调用者是谁？（其它模块、外部用户、测试）
- [ ] 关键操作有哪些？
- [ ] 有哪些约束？（性能、兼容性、现有模式）
- [ ] 什么应该藏在内部，什么应该暴露？

询问：“这个模块需要做什么？谁会使用它？”

### 2. 生成设计（并行子代理）

使用 Task tool 同时生成 3 个以上子代理。每个子代理都必须提出一种**完全不同**的方法。

```
Prompt template for each sub-agent:

Design an interface for: [module description]

Requirements: [gathered requirements]

Constraints for this design: [assign a different constraint to each agent]
- Agent 1: "Minimize method count - aim for 1-3 methods max"
- Agent 2: "Maximize flexibility - support many use cases"
- Agent 3: "Optimize for the most common case"
- Agent 4: "Take inspiration from [specific paradigm/library]"

Output format:
1. Interface signature (types/methods)
2. Usage example (how caller uses it)
3. What this design hides internally
4. Trade-offs of this approach
```

### 3. 展示设计

展示每个设计：

1. **Interface signature**：类型、方法、参数
2. **Usage example**：调用者实际如何使用
3. **What it hides**：哪些复杂性留在内部

按顺序展示，让用户先吸收每种方法，再进行比较。

### 4. 比较设计

展示所有设计后，比较它们：

- **Interface simplicity**：方法更少、参数更简单
- **General vs specific**：灵活性和专注度之间的取舍
- **Implementation efficiency**：这个形状是否允许高效内部实现？
- **Depth**：隐藏大量复杂性的小接口（好）vs 大接口薄实现（坏）
- **Ease of correct use** vs **ease of misuse**

用 prose 讨论权衡，不要用表格。突出设计之间差异最大的地方。

### 5. 综合

最好的设计通常会结合多个方案的洞见。询问：

- “哪种设计最适合你的主要用例？”
- “其它设计中有哪些元素值得吸收？”

## 评价标准

摘自《A Philosophy of Software Design》：

**Interface simplicity**：更少的方法、更简单的参数 = 更容易学习并正确使用。

**Generality**：无需修改就能处理未来用例。但要小心过度泛化。

**Implementation efficiency**：接口形状是否允许高效实现？还是会迫使内部变得尴尬？

**Depth**：小接口隐藏大量复杂性 = deep module（好）。大接口加薄实现 = shallow module（避免）。

## 反模式

- 不要让子代理产出相似设计；强制根本差异
- 不要跳过比较，价值就在对比
- 不要实现；这个 skill 只讨论接口形状
- 不要根据实现工作量评价设计
