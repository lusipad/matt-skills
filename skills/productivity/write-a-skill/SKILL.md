---
name: write-a-skill
description: 当用户想创建、编写或构建一个新 skill 时，使用正确结构、渐进披露和可附带资源的方式创建 agent skill。
---

# Writing Skills

## 流程

1. **收集需求**，询问用户：
   - 这个 skill 覆盖什么任务或领域？
   - 它需要处理哪些具体用例？
   - 它需要可执行 scripts，还是只需要 instructions？
   - 是否有 reference materials 要包含？

2. **起草 skill**，创建：
   - 带简洁 instructions 的 `SKILL.md`
   - 内容超过 500 行时，拆出额外 reference files
   - 需要确定性操作时，添加 utility scripts

3. **和用户 review**，展示草稿并询问：
   - 是否覆盖了你的用例？
   - 有没有缺失或不清楚的地方？
   - 哪些 section 应该更详细或更简短？

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](REFERENCE.md)]
```

## Description 要求

`description` 是 agent 决定是否加载 skill 时唯一会先看到的内容。它会和其它已安装 skills 的描述一起出现在 system prompt 里。Agent 读取这些 descriptions，并根据用户请求选择相关 skill。

**目标**：给 agent 足够信息判断：

1. 这个 skill 提供什么能力
2. 什么时候、为什么触发它（具体关键词、上下文、文件类型）

**格式**：

- 最多 1024 chars
- 第三人称
- 第一句：它做什么
- 第二句：`Use when [specific triggers]`

**好例子**：

```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**坏例子**：

```
Helps with documents.
```

坏例子无法让 agent 区分它和其它 document skills。

## 何时添加 Scripts

在这些情况下添加 utility scripts：

- 操作是确定性的（validation、formatting）
- 同一段代码会被反复生成
- 错误需要明确处理

Scripts 能节省 tokens，并比生成代码更可靠。

## 何时拆分文件

这些情况下拆成独立文件：

- `SKILL.md` 超过 100 行
- 内容属于不同领域（finance vs sales schemas）
- 高级功能很少需要

## Review Checklist

草稿完成后验证：

- [ ] Description 包含 triggers（"Use when..."）
- [ ] `SKILL.md` 小于 100 行
- [ ] 没有 time-sensitive info
- [ ] 术语一致
- [ ] 包含具体 examples
- [ ] References 只深入一层
