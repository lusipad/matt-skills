---
name: handoff
description: 当需要把当前对话压缩成可交接文档，让另一个 agent 接手继续工作时使用。
---

写一份交接文档，总结当前对话，让一个全新的 agent 可以继续工作。保存到用户操作系统的临时目录，不要保存到当前 workspace。

文档里包含 “suggested skills” 小节，列出下一个 agent 应该调用的 skills。

不要重复已经写进其它 artifact 的内容，例如 PRD、计划、ADR、issues、commits、diffs。用路径或 URL 引用它们。

删去敏感信息，例如 API key、密码或个人身份信息。

如果用户传入参数，把它当作下一轮会话的重点，并据此调整交接文档。

如果宿主 agent 支持命令参数或 invocation hint，把用户参数理解为：“下一轮会话要用来做什么？”
