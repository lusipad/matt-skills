# Issue tracker: Local Markdown

这个仓库的 issues 和 PRD 存放为 `.scratch/` 下的 markdown 文件。

## 约定

- 每个 feature 一个目录：`.scratch/<feature-slug>/`
- PRD 是 `.scratch/<feature-slug>/PRD.md`
- 实现议题是 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，编号从 `01` 开始
- 分诊状态记录为 issue 文件顶部附近的 `Status:` 行（role 字符串见 `triage-labels.md`）
- Comments 和对话历史追加到文件底部的 `## Comments` 小节

## 当 skill 说 “publish to the issue tracker”

在 `.scratch/<feature-slug>/` 下创建新文件，必要时创建目录。

## 当 skill 说 “fetch the relevant ticket”

读取引用路径对应的文件。用户通常会直接传路径或 issue number。
