---
name: improve-codebase-architecture
description: 当用户想改进架构、寻找重构机会、合并强耦合模块，或让代码库更易测试、更利于 AI 导航时，用 CONTEXT.md 的领域语言和 docs/adr/ 的历史决策寻找模块加深机会。
---

# 改进代码库架构

暴露架构摩擦，并提出**加深机会**：把浅模块重构成深模块。目标是提升可测试性和 AI 导航性。

## 术语表

每条建议都必须准确使用这些术语。一致语言是重点，不要滑到“component”“service”“API”或“boundary”。完整定义见 [LANGUAGE.md](LANGUAGE.md)。

- **模块**：任何有接口和实现的东西，例如函数、类、包、切片。
- **接口**：调用者为了使用模块必须知道的一切，包括类型、不变量、错误模式、顺序、配置，而不只是类型签名。
- **实现**：模块内部的代码。
- **深度**：接口上的杠杆。小接口背后有大量行为。**深** = 高杠杆；**浅** = 接口几乎和实现一样复杂。
- **接缝**：接口所在的位置；可以不原地编辑代码而改变行为的地方。用这个词，不要用“boundary”。
- **适配器**：在接缝处满足接口的具体东西。
- **杠杆**：调用者从深度中获得的收益。
- **局部性**：维护者从深度中获得的收益：变更、错误和知识集中在一处。

关键原则（完整列表见 [LANGUAGE.md](LANGUAGE.md)）：

- **删除测试**：想象删除这个模块。如果复杂性消失，它只是 pass-through。如果复杂性会在 N 个调用者里重新出现，它就在创造价值。
- **接口就是测试表面。**
- **一个适配器 = 假设接缝；两个适配器 = 真实接缝。**

这个 skill 受项目领域模型约束。领域语言给好的接缝命名；ADR 记录不应被反复重审的历史决策。

## 流程

### 1. 探索

先阅读项目的领域 glossary，以及即将触碰区域相关的 ADR。

然后使用宿主 agent 的轻量代码库探索能力遍历代码库：Codex 可以使用 `explore` 子代理，Claude Code 可以使用 Task/Agent 工具，没有子代理能力的 agent 就直接探索。不要套死板启发式；自然探索，并记录你在哪里遇到理解摩擦：

- 理解一个概念是否需要在许多小模块之间来回跳？
- 哪些模块很**浅**，接口几乎和实现一样复杂？
- 哪里为了可测试性抽出了纯函数，但真正 bug 藏在调用方式里，缺少**局部性**？
- 哪些强耦合模块跨接缝泄漏？
- 哪些代码区域没测试，或很难通过当前接口测试？

对任何疑似浅模块应用**删除测试**：删除它会集中复杂性，还是只是把复杂性挪到别处？“会集中”就是你要找的信号。

### 2. 用 HTML 报告展示候选项

把一个自包含 HTML 文件写到操作系统临时目录，避免在仓库里留下文件。从 `$TMPDIR` 解析临时目录，回退到 `/tmp`（Windows 上回退到 `%TEMP%`），写入 `<tmpdir>/architecture-review-<timestamp>.html`，确保每次运行都有新文件。为用户打开它：Linux 用 `xdg-open <path>`，macOS 用 `open <path>`，Windows 用 `start <path>`，并告诉用户绝对路径。

报告使用 **Tailwind via CDN** 做布局和样式，使用 **Mermaid via CDN** 表达适合 graph/flow/sequence 的结构。把 Mermaid 和手写 CSS/SVG 视觉混合使用：调用图、依赖图、序列用 Mermaid；质量图、横截面、折叠效果这类更 editorial 的表达用手写 div/SVG。每个候选项都要有 **before/after visualization**。要视觉化。

每个候选项用卡片呈现：

- **Files**：涉及的 files/modules
- **Problem**：当前架构为什么造成摩擦
- **Solution**：用 plain English 描述会改变什么
- **Benefits**：用局部性、杠杆、测试如何改善来解释
- **Before / After diagram**：并排、自定义绘制，说明浅在哪里、如何加深
- **Recommendation strength**：`Strong`、`Worth exploring`、`Speculative` 之一，用 badge 呈现

报告最后放 **Top recommendation**：你建议先处理哪个候选项，以及为什么。

**领域部分使用 CONTEXT.md 词汇，架构部分使用 [LANGUAGE.md](LANGUAGE.md) 词汇。** 如果 `CONTEXT.md` 定义了 “Order”，就说 “Order intake module”，不要说 “FooBarHandler”，也不要说 “Order service”。

**ADR 冲突**：如果候选项和现有 ADR 冲突，只有当摩擦真实到值得重开 ADR 时才提出。要在卡片中明确标注，例如 warning callout：_“contradicts ADR-0007, but worth reopening because...”_。不要列出每个被 ADR 理论上禁止的重构。

完整 HTML 脚手架、图表模式和样式指南见 [HTML-REPORT.md](HTML-REPORT.md)。

先不要提出接口。文件写好后问用户：“你想探索其中哪一个？”

### 3. 追问循环

用户选择候选项后，进入追问对话。和用户一起走完整棵设计树：约束、依赖、加深后模块的形状、接缝背后是什么、哪些测试能保留下来。

随着决策变清楚，立即产生这些副作用：

- **用 `CONTEXT.md` 中不存在的概念给加深模块命名？** 把术语加入 `CONTEXT.md`，规则同 `/grill-with-docs`（见 [CONTEXT-FORMAT.md](../grill-with-docs/CONTEXT-FORMAT.md)）。如果文件不存在，就按需创建。
- **对话中收紧了模糊术语？** 立刻更新 `CONTEXT.md`。
- **用户用承重理由拒绝候选项？** 建议写 ADR，表达为：_“要不要把这个记录成 ADR，避免未来架构审查再次建议它？”_ 只有当这个理由确实能帮助未来探索者避免重复建议时才提出；临时理由（“现在不值得”）和显而易见的理由跳过。见 [ADR-FORMAT.md](../grill-with-docs/ADR-FORMAT.md)。
- **想探索加深模块的备选接口？** 见 [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md)。
