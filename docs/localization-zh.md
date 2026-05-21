# 中文化规则

这个仓库的中文化目标是“本地化改写”，不是机器直译。`SKILL.md` 是 agent 会执行的工作流文档，翻译时必须优先保护可执行性、触发词和工程语气。

## 保留不翻译

- skill `name`，例如 `diagnose`、`tdd`、`handoff`
- frontmatter 的 key，例如 `name`、`description`
- 文件名、目录名、路径、URL
- 命令、代码块、配置 key、JSON/TOML/YAML 字段
- 包名、库名、产品名和专有名词，例如 Codex、Claude Code、GitHub、Husky、Prettier

## 可以中文化

- README、索引、说明性段落
- `description` 的自然语言部分
- `SKILL.md` 正文里的流程说明、验收标准、注意事项
- 用户可见的解释文本和交接文本

## 推荐术语

| 英文 | 中文 |
| --- | --- |
| agent | agent / 代理 |
| coding agent | 编码代理 |
| skill | skill / 技能 |
| issue | 议题 |
| issue tracker | 议题跟踪系统 |
| triage | 分诊 |
| triage role | 分诊角色 |
| handoff | 交接 |
| grill / grilling session | 追问 / 需求追问 |
| shared language | 共享语言 |
| ubiquitous language | 统一语言 |
| domain model | 领域模型 |
| ADR | ADR / 架构决策记录 |
| PRD | PRD / 产品需求文档 |
| feedback loop | 反馈闭环 |
| red-green-refactor | 红绿重构 |
| regression test | 回归测试 |
| module | 模块 |
| deep module | 深模块 |
| shallow module | 浅模块 |
| seam | 接缝 |
| adapter | 适配器 |
| interface | 接口 |
| implementation | 实现 |
| vertical slice | 垂直切片 |

## 风格要求

- 不把 agent 翻成“特工”。
- 不把 grilling session 翻成“烧烤会议”；按语境使用“追问”或“需求追问”。
- 不把 ticket 机械翻成“票据”；本仓库统一用“议题”。
- 不追求逐句对应；优先写成自然、可执行的中文说明。
- 每次中文化后都运行 `python scripts/validate-skill-indexes.py`，确保索引、manifest 和 Codex adapter 没有漂移。
