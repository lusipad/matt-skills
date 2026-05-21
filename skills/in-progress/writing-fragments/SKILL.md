---
name: writing-fragments
description: 当用户想在强加结构前发展想法，或提到 fragments、ideate、raw material for writing 时，通过追问挖掘异质写作 fragments，并追加到单个 markdown 文档。
---

<what-to-do>

运行一个产出 fragments 的 grilling session。围绕用户想写的主题持续追问。不要强加 phases、outline 或结构；这些明确 out of scope。

当对话双方产生 fragments 时，把它们追加到同一个 markdown 文件。用户会在 session 中编辑这个文件；每次写入前都要重新读取，确保保留用户修改。

如果用户没有传路径，问一次保存到哪里，然后在本 session 余下时间记住它。

从用户说的第一句话开始捕获 fragments，包括初始 prompt。

第一次写入时，在顶部放一个 H1 作为 working title（以后可以改），除此之外不要加 metadata、TOC 或日期。

</what-to-do>

<supporting-info>

## 什么是 fragment

Fragment 是任何可能存活到最终文章里的文本。它必须让**作者自己读得懂**，作者能看出它是什么意思；但它不需要定义术语，也不需要让冷读者立即理解。标准是“这是不是一块好的写作材料？”，不是“这是不是一个自足论证？”

Fragments 刻意保持异质。可能成为 fragment 的东西：

- 一句锋利的话，之后可能放进某处，但现在还不知道放哪
- 一个 claim 加一行理由
- 一个 vignette：发生过的一件事、代码片段、场景、类比
- 一个半成形想法：“某种 X 像 Y 的感觉，之后再展开”
- 引用、对话、听来的句子
- 一组凭感觉连在一起的观察
- 抱怨、坦白、punchline

小说家的日记是模型：多年无结构观察，之后被开采成原材料。Fragments 就是 noticings。

## 文件格式

```markdown
# Working title

A first fragment lives here.

It can be multiple paragraphs. It can include lists, code, quotes — whatever
shape the fragment naturally takes.

---

A second fragment.

---

> A quoted line that the user wants to keep around.

A reaction to it.

---

- A cluster of related observations
- That hang together by feel
- And want to be near each other
```

Fragments 用水平线分隔（`\n---\n`）。正文内部不加 headings，不加 tags，不重新排序，只保留追加顺序。

## 写作节奏

默默追加。不要每个 fragment 都请求许可。可以顺带说一句 “adding that”，但不要用保存确认打断对话。

每次写入前：从磁盘重新读取文件。用户可能在两轮之间编辑、重排或删除 fragments，必须保留他们的修改。永远不要覆盖文件；只追加，除非用户要求编辑某个具体 fragment。

用户随时可以说 “cut the last one”、“rewrite that one sharper”、“merge those two”。把这些视为一等指令。

</supporting-info>
