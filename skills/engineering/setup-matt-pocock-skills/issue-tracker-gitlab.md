# Issue tracker: GitLab

这个仓库的 issues 和 PRD 存放在 GitLab Issues。所有操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 约定

- **创建 issue**：`glab issue create --title "..." --description "..."`。多行 description 使用 heredoc。传 `--description -` 会打开编辑器。
- **读取 issue**：`glab issue view <number> --comments`。用 `-F json` 获取机器可读输出。
- **列出 issues**：`glab issue list -F json`，按需要加 `--label` 过滤。
- **评论 issue**：`glab issue note <number> --message "..."`。GitLab 把 comments 称为 “notes”。
- **添加 / 移除 labels**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个 label 可用逗号分隔，也可以重复 flag。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受 closing comment，所以先用 `glab issue note <number> --message "..."` 发布解释，再关闭。
- **Merge requests**：GitLab 把 PR 叫做 merge request。使用 `glab mr create`、`glab mr view`、`glab mr note` 等；形状和 `gh pr ...` 类似，只是用 `mr` 替代 `pr`，用 `note` / `--message` 替代 `comment` / `--body`。

从 `git remote -v` 推断 repo。`glab` 在 clone 内运行时会自动处理。

## 当 skill 说 “publish to the issue tracker”

创建一个 GitLab issue。

## 当 skill 说 “fetch the relevant ticket”

运行 `glab issue view <number> --comments`。
