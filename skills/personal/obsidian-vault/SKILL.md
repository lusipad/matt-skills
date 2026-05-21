---
name: obsidian-vault
description: 当用户想在 Obsidian 中查找、创建或组织笔记时，使用 wikilinks 和 index notes 搜索、创建和管理 vault 笔记。
---

# Obsidian Vault

## Vault location

`/mnt/d/Obsidian Vault/AI Research/`

根目录基本保持扁平。

## 命名约定

- **Index notes**：聚合相关主题，例如 `Ralph Wiggum Index.md`、`Skills Index.md`、`RAG Index.md`
- 所有 note names 使用 **Title Case**
- 不用 folders 组织；用 links 和 index notes 组织

## Linking

- 使用 Obsidian `[[wikilinks]]` 语法：`[[Note Title]]`
- Notes 在底部链接 dependencies / related notes
- Index notes 只是 `[[wikilinks]]` 列表

## 工作流

### 搜索 notes

```bash
# Search by filename
find "/mnt/d/Obsidian Vault/AI Research/" -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" "/mnt/d/Obsidian Vault/AI Research/" --include="*.md"
```

也可以直接在 vault path 上使用 Grep/Glob tools。

### 创建新 note

1. 文件名使用 **Title Case**
2. 按 vault rules，把内容写成一个 learning unit
3. 在底部添加指向 related notes 的 `[[wikilinks]]`
4. 如果属于编号序列，使用层级编号方案

### 查找 related notes

在 vault 中搜索 `[[Note Title]]`，找到 backlinks：

```bash
grep -rl "\\[\\[Note Title\\]\\]" "/mnt/d/Obsidian Vault/AI Research/"
```

### 查找 index notes

```bash
find "/mnt/d/Obsidian Vault/AI Research/" -name "*Index*"
```
