Skills 按 bucket 组织在 `skills/` 下：

- `engineering/`：日常代码工作
- `productivity/`：非代码专用的日常工作流工具
- `misc/`：保留但低频使用
- `personal/`：绑定个人环境，不公开推广
- `in-progress/`：尚未准备发布的草稿
- `deprecated/`：不再使用

`engineering/`、`productivity/` 或 `misc/` 中的每个 skill 都必须同时出现在顶层 `README.md`、`.claude-plugin/plugin.json` 和 `.agents/skills/` 下的 Codex adapter 中。`personal/`、`in-progress/` 和 `deprecated/` 中的 skills 不得出现在任何公开插件入口。

`.codex-plugin/plugin.json` 必须指向 Codex adapter 目录，而不是直接指向 bucketed `skills/` 树，避免 draft / personal / deprecated skills 被意外暴露。

顶层 `README.md` 中的每个 skill 条目都必须把 skill name 链接到对应 `SKILL.md`。

每个 bucket folder 都有自己的 `README.md`，列出该 bucket 中每个 skill，并用一行描述说明用途；skill name 必须链接到对应 `SKILL.md`。
