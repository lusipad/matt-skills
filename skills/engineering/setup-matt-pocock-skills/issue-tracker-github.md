# Issue tracker: GitHub

这个仓库的 issues 和 PRD 存放在 GitHub Issues。所有操作使用 `gh` CLI。

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行正文使用 heredoc。
- **读取 issue**：`gh issue view <number> --comments`，同时获取 labels，comments 可用 `jq` 过滤。
- **列出 issues**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，按需要加 `--label` 和 `--state` 过滤。
- **评论 issue**：`gh issue comment <number> --body "..."`
- **添加 / 移除 labels**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

从 `git remote -v` 推断 repo。`gh` 在 clone 内运行时会自动处理。

## 当 skill 说 “publish to the issue tracker”

创建一个 GitHub issue。

## 当 skill 说 “fetch the relevant ticket”

运行 `gh issue view <number> --comments`。
