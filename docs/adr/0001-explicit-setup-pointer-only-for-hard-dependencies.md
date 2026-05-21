# 只有硬依赖才显式提示 `/setup-matt-pocock-skills`

工程类 skills 会使用 `/setup-matt-pocock-skills` 生成的仓库级配置：issue tracker、triage label vocabulary、domain doc layout。缺少这些配置时，有些 skills 无法正确工作，因为它们必须发布到具体 issue tracker，或应用具体 label 字符串。另一些 skills 只是用这些配置来提升输出质量，例如使用领域词汇、感知 ADR；缺少配置时仍然可以优雅降级。

因此我们把 skills 分成**硬依赖**和**软依赖**：

- **硬依赖**（`to-issues`、`to-prd`、`triage`）：包含明确单行提示：_“... should have been provided to you; run `/setup-matt-pocock-skills` if not.”_ 没有映射时，输出会是错误的，而不只是模糊。
- **软依赖**（`diagnose`、`tdd`、`improve-codebase-architecture`、`zoom-out`）：只在正文里自然提到“项目的领域 glossary”和“即将触碰区域的 ADR”。即使没有这些文档，skill 仍然有效，只是输出没那么锋利。

这个划分让软依赖 skills 保持轻量，避免在不承重的地方堆满 setup 指针。
