---
name: writing-shape
description: 当用户有一堆 notes、fragments 或 rough draft，想把它整理成可发布文章时，读取 markdown 原材料，并通过对话逐段塑形、讨论开头、结构和格式选择。
---

<what-to-do>

用户已经传入或将会传入一个 markdown 原材料文件。把它当作输入素材堆：可以是整齐 fragment 列表、无结构长文、transcript，格式不重要。先完整读一遍，再做任何事。

然后运行 shaping session，产出一个独立 article document。不要编辑原材料文件；对这个 skill 来说它是 read-only。

如果用户没说文章保存到哪里，问一次并记住路径。用户会在 session 中编辑 article 文件；每次写入前都要重新读取它，确保保留用户修改。

</what-to-do>

<supporting-info>

## 循环

1. **读取素材堆。** 完整读取输入文件，形成对内容的整体感。
2. **起草 2-3 个候选开头。** 每个开头都应该暗示不同 thesis 或 angle。全部展示给用户，迫使用户选择或组合 hybrid。被选中的开头决定文章其余部分必须完成什么。
3. **逐段生长。** 开头确定后，问：“基于这个开头，读者下一步需要听到什么？” 从素材堆里抽取内容来回答。争论下一个 beat 应该是段落、列表、表格、callout、引用还是代码块。每个格式选择都应有明确理由。
4. **边走边追加到 article 文件。** 不要批量攒到最后。每个达成一致的段落或 block 立刻写入，让用户看到文章成形。
5. **重复步骤 3，直到文章完成。** 用户决定什么时候完成。

## 对话感觉

这是倒过来的 grilling session。构思阶段的问题是“你到底注意到了什么？”这里的问题是“这篇文章到底在论证什么，读者需要按什么顺序听到它？”要 push back。不要让弱 transition 混过去。如果某段没有挣到位置，就删。

持续使用这些动作：

- “这段给读者带来了上一段没有带来的什么？”
- “如果我删掉它，哪里会断？”
- “这应该是 prose，还是 list？为什么是 prose？”
- “这句话在做两件事；拆开，或只选一件。”
- “开头承诺的是 X，但我们漂到了 Y。要么重新接线，要么改开头。”

## 从素材堆里抽取

把原材料当 quarry，不是 script。抽出 fragment，改写到适合周围段落的位置，再放进去。一个 fragment 可以被拆成多段、和另一个合并，或被 paraphrase。素材堆的任务是被开采；文章的任务是读起来像一个声音。

如果素材堆缺少文章需要的东西，明确指出 gap：“这里需要一个例子，但素材里没有。现在给我一个，或者我们删掉这一节。”

## 必须真的讨论的格式问题

选择如何呈现一个 beat 时，和用户把取舍说出来，不要默默决定：

- **Prose vs list。** Prose 承载论证；list 承载并列项。如果 items 不真正并列，prose 更好。如果它们并列，list 更容易扫描。
- **Inline vs callout。** Tips、warnings、asides 放进 callouts（`> [!TIP]`、`> [!NOTE]`），但只有当它们 inline 会打断主论证时才这样做。否则留在正文里。
- **Table vs repeated structure。** 同一形状重复 3 次以上且字段相同，用 table。否则用 prose 加 bold leads。
- **Quote vs paraphrase。** 原话本身重要时引用；只有意思重要时 paraphrase。
- **Code block vs inline code。** 多行、可运行或说明性代码用 block；单个 token 或 identifier 用 inline。

## 写作节奏

每个 block 达成一致后就追加到 article 文件。每次写入前都从磁盘重新读取文件，因为用户可能在两轮之间编辑。永远不要盲目覆盖。如果用户要重写某段，就只原地编辑那段，其他部分不动。

## Out of scope

- 挖掘素材堆里没有的新 fragments。素材堆就是输入；如果不完整，就指出 gap，让用户补，或删掉这一节。
- 编辑原材料文件。
- 发布、适配特定平台格式，或添加用户没有要求的 frontmatter。

</supporting-info>
