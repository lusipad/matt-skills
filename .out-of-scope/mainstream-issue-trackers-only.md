# Issue tracker integrations are limited to mainstream tools

`setup-matt-pocock-skills` 只为**主流** issue trackers 提供 first-class support。为小众、新出现或单一供应商实验性 trackers 增加支持，不在范围内。

## 为什么不在范围内

每个 issue-tracker backend 都会把一套 CLI 形状硬编码进 skills：commands、flags、output parsing。每新增一个 backend，都会永久增加维护面：它必须随着工具 CLI 演进而保持可用，也必须持续用 `/to-prd`、`/to-issues`、`/triage` 等 skills 验证。只有当相当一部分用户实际拥有这个 tracker 时，这个成本才值得付。

“Mainstream” 是判断，不是数字门槛：

- GitHub、GitLab 和 Backlog.md 属于我们会考虑的 mainstream 工具：广为人知、广泛使用，并且已经过了实验阶段。
- 一个刚出现、面向 agent、只有几百 GitHub stars 的工具，不管设计多有意思，都不算。

Stars、年龄和下载量都是做判断时的有用信号，但都不是规则。规则是：普通工程师会认得这个工具，并且有可能为自己的团队选择它吗？

非主流 trackers 已经有 escape hatches：

- `local markdown`：轻量 repo 内跟踪。
- `other/custom`：给想自己接入的人使用。

这两种都不要求核心 skills 知道具体工具。

## Prior requests

- #99 — "Add dex as an issue tracker backend"（请求时 dex 约 3 个月大，约 300 stars）
