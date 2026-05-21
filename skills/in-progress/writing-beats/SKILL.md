---
name: writing-beats
description: 当用户有 raw material，并想把文章组装成叙事旅程而不是论证时，以 choose-your-own-adventure 风格逐个 beat 塑形文章。
---

<what-to-do>

用户已经传入或将会传入一个 markdown 原材料文件。

如果用户没说文章保存到哪里，问一次并记住路径。

然后运行 beat-by-beat journey：

1. 从原材料中写 2-3 个候选 **starting beats**。每个都是进入文章的不同入口。先展示给用户，不要写入 article 文件。用户选择一个。预览它写下后可能通向哪些 beats，就像让用户看到前方一小段路。
2. 用户选定 starting beat 后，只把**那个 beat**写入 article 文件。一个 beat 可以是一句话，也可以是几段，取决于它自然需要什么。写完就停。
3. 从磁盘重新读取 article 文件。然后提供 2-3 个候选 **next beats**，代表文章当前位置可以 pivot 到的不同方向。
4. 重复步骤 2-4，直到文章自然结束。

</what-to-do>

<supporting-info>

## 什么是 beat

Beat 是旅程中的一个动作。它只做一件事：设定场景、落下一个观点、提出问题、插入旁白、扭转角度。然后停下，把读者留在一个下个 beat 可以 pivot 的位置。

Beat 的大小由它需要完成的动作决定：

- 如果动作只有一句话，那就是一句：“And then nothing happened for three weeks.”
- 如果动作需要铺垫，就是短段落。
- 如果 beat 是一个自足 vignette、argument 或 example，可以是多段。

如果一个 “beat” 需要五段和三个小标题，它就不是一个 beat，而是两个 beat 粘在一起。拆开。

## 写一个 beat

一旦 beat 被选中，只把**那个 beat**写进 article 文件。不要提前写下一个 beat。

从 raw pile 中抽取材料填充 beat。你可以 paraphrase、拆分、重组或引用。素材堆是 quarry。

## 结束旅程

文章在旅程完成时结束，而不是在素材堆耗尽时结束。大多数素材堆都会剩下没用上的 fragments。没关系，这正是原材料多于需求的意义。

## 写作节奏

- 一次只追加一个 beat。永远不要提前写。
- 每次写入前都从磁盘重新读取 article 文件。绝对保留用户编辑。
- 如果用户大幅编辑了前一个 beat，让它改变后续走向。
- 如果用户说 “rewrite that beat” 或 “go back and try a different beat 3”，就照做：原地编辑，其它部分不动。

</supporting-info>
