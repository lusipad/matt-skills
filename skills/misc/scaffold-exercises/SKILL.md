---
name: scaffold-exercises
description: 当用户想 scaffold exercises、创建 exercise stubs，或设置新课程章节时，创建能通过 lint 的章节、题目、答案和讲解目录结构。
---

# Scaffold Exercises

创建能通过 `pnpm ai-hero-cli internal lint` 的 exercise 目录结构，然后用 `git commit` 提交。

## 目录命名

- **Sections**：`exercises/` 下的 `XX-section-name/`（例如 `01-retrieval-skill-building`）
- **Exercises**：section 下的 `XX.YY-exercise-name/`（例如 `01.03-retrieval-with-bm25`）
- Section number = `XX`，exercise number = `XX.YY`
- 名称使用 dash-case（小写、连字符）

## Exercise variants

每个 exercise 至少需要这些子目录之一：

- `problem/`：student workspace，包含 TODOs
- `solution/`：reference implementation
- `explainer/`：概念材料，不包含 TODOs

做 stub 时，除非计划明确指定，否则默认使用 `explainer/`。

## 必需文件

每个子目录（`problem/`、`solution/`、`explainer/`）都需要一个 `readme.md`：

- **不能为空**（必须有真实内容，哪怕只有一行标题也可以）
- 不能有 broken links

做 stub 时，创建一个带标题和描述的最小 readme：

```md
# Exercise Title

Description here
```

如果子目录里有代码，也需要一个超过 1 行的 `main.ts`。但对于 stubs，只有 readme 的 exercise 可以接受。

## 工作流

1. **解析计划**：提取 section names、exercise names 和 variant types
2. **创建目录**：对每个路径执行 `mkdir -p`
3. **创建 readme stubs**：每个 variant folder 一个 `readme.md`，包含标题
4. **运行 lint**：用 `pnpm ai-hero-cli internal lint` 验证
5. **修复错误**：迭代直到 lint 通过

## Lint rules summary

Linter（`pnpm ai-hero-cli internal lint`）会检查：

- 每个 exercise 有子目录（`problem/`、`solution/`、`explainer/`）
- 至少存在 `problem/`、`explainer/` 或 `explainer.1/` 之一
- primary subfolder 中存在非空 `readme.md`
- 没有 `.gitkeep` 文件
- 没有 `speaker-notes.md` 文件
- readmes 中没有 broken links
- readmes 中没有 `pnpm run exercise` 命令
- 每个 subfolder 需要 `main.ts`，除非它是 readme-only

## 移动或重命名 exercises

重新编号或移动 exercises 时：

1. 使用 `git mv`（不是 `mv`）重命名目录，以保留 git history
2. 更新数字前缀以保持顺序
3. 移动后重新运行 lint

示例：

```bash
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

## 示例：从计划创建 stubs

给定计划：

```
Section 05: Memory Skill Building
- 05.01 Introduction to Memory
- 05.02 Short-term Memory (explainer + problem + solution)
- 05.03 Long-term Memory
```

创建：

```bash
mkdir -p exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer
mkdir -p exercises/05-memory-skill-building/05.02-short-term-memory/{explainer,problem,solution}
mkdir -p exercises/05-memory-skill-building/05.03-long-term-memory/explainer
```

然后创建 readme stubs：

```
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# Introduction to Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# Long-term Memory"
```
