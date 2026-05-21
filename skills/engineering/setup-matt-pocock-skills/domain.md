# 领域文档

工程类 skills 在探索代码库时，应按这里的规则读取仓库里的领域文档。

## 探索前先读

- 仓库根目录的 **`CONTEXT.md`**，或
- 根目录存在 **`CONTEXT-MAP.md`** 时读取它；它会指向每个 context 对应的 `CONTEXT.md`。只读取与当前主题相关的 context。
- **`docs/adr/`**：读取和即将处理区域相关的 ADR。多 context 仓库还要检查 `src/<context>/docs/adr/` 中的 context-scoped decisions。

如果这些文件不存在，**安静地继续**。不要专门指出缺失，也不要提前建议创建。生产这些文档的 skill（`/grill-with-docs`）会在术语或决策真正被确认时按需创建它们。

## 文件结构

单 context 仓库（大多数仓库）：

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多 context 仓库（根目录存在 `CONTEXT-MAP.md`）：

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## 使用 glossary 里的词

当输出要命名领域概念时（issue title、refactor proposal、hypothesis、test name），使用 `CONTEXT.md` 中定义的术语。不要漂移到 glossary 明确避免的同义词。

如果你需要的概念还不在 glossary 里，这是一个信号：要么你正在发明项目并未使用的语言（重新考虑），要么确实存在缺口（记录给 `/grill-with-docs`）。

## 标出 ADR 冲突

如果你的输出和现有 ADR 冲突，要明确指出，而不是默默覆盖：

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because..._
