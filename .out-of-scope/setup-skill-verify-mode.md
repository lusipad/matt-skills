# Verify/Check Mode for `setup-matt-pocock-skills`

本项目不会为 `setup-matt-pocock-skills` 增加专门的 verify/check mode，也不会新增独立 verify skill。

## 为什么不在范围内

再加一个 skill，或给它加 `--verify` flag，用来检查 `docs/agents/*.md` artifacts 是否仍匹配 seed-template schema，会重复现有 setup skill 已经能通过对话完成的工作。

预期工作流是：**运行 `/setup-matt-pocock-skills`，并告诉它验证当前 setup。** 这个 skill 是 prompt-driven 的，所以 maintainer 可以把它限定为 verification pass，例如：“不要重写任何东西，只检查我现有文件和当前 seed templates 是否有 drift，并报告结果。” 不需要单独代码路径。新增 flag 或 sibling skill 会把一个已经能通过自然语言入口表达的功能拆成更多 surface area。

把配置管理保留在一个 skill 里，也能避免 seed templates 演进时两个 skills 互相漂移。

## Prior requests

- #106 — Feature request: verify/check mode for setup-matt-pocock-skills
