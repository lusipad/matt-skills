<p>
  <a href="https://www.aihero.dev/s/skills-newsletter">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skills-repo-dark_2x.png">
      <source media="(prefers-color-scheme: light)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png">
      <img alt="Skills" src="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png" width="369">
    </picture>
  </a>
</p>

# 面向真实工程的 Skills

[![skills.sh](https://skills.sh/b/mattpocock/skills)](https://skills.sh/mattpocock/skills)

这是一组我日常用于真实工程工作的 agent skills。它们不是为了“氛围式编程”，而是为了把需求澄清、工程判断、反馈闭环和交付节奏变成可重复执行的工作流。

同一份 `skills/` 源内容同时打包给 Codex 和 Claude Code 使用。

真实应用很难开发。GSD、BMAD、Spec-Kit 这类方法会试图接管流程来帮助你，但一旦流程本身出错，你反而更难看清问题在哪里，也更难保留自己的工程判断。

这个仓库的思路相反：每个 skill 都尽量小、容易改、能组合。它们不绑定某个模型，也不假设你只能使用某一个 agent。你可以直接使用，也可以按自己的团队习惯改造。

## 快速开始

1. 运行 `skills.sh` 安装器：

```bash
npx skills@latest add mattpocock/skills
```

2. 选择你想安装的 skills，以及要安装到哪些编码代理上。请确保选择 `/setup-matt-pocock-skills`。

3. 在 agent 中运行 `/setup-matt-pocock-skills`。它会询问：
   - 这个仓库使用哪个议题跟踪系统，例如 GitHub、Linear 或本地文件
   - 分诊议题时使用哪些标签，`/triage` 会读取这些标签
   - 后续生成的文档应该保存到哪里

4. 设置完成后，其它工程类 skills 就能读取这些项目约定。

## Codex 与 Claude 兼容

这个仓库只维护一份规范 skill 正文：`skills/`。

Claude Code 通过 `.claude-plugin/plugin.json` 读取公开 skill 文件夹。Codex 通过 `.codex-plugin/plugin.json` 读取 `.agents/skills/` 下的轻量适配器；这些适配器只负责把 Codex 指向同一份规范正文，不复制业务逻辑。

对外发布的 skills 只来自：

- `skills/engineering/`
- `skills/productivity/`
- `skills/misc/`

以下目录不会进入公开插件清单：

- `skills/in-progress/`
- `skills/personal/`
- `skills/deprecated/`

如果不通过 marketplace 安装，而是在本机开发调试，可以运行：

```bash
./scripts/link-skills.sh all
```

这会把公开 skills 链接到 `~/.claude/skills` 和 `~/.agents/skills`。

修改 skill 目录、插件清单或 README 索引后，请运行：

```bash
python scripts/validate-skill-indexes.py
```

中文化规则见 [docs/localization-zh.md](./docs/localization-zh.md)。翻译或改写 `SKILL.md` 时，保留 skill name、路径、命令、代码块和 frontmatter key，不要做会破坏触发和工具执行的直译。

## 为什么需要这些 Skills

我创建这些 skills，是为了解决 Claude Code、Codex 和其它编码代理在真实项目里常见的几类失败模式。

### 1. Agent 没有理解我要什么

> "No-one knows exactly what they want"
>
> David Thomas & Andrew Hunt, [The Pragmatic Programmer](https://www.amazon.co.uk/Pragmatic-Programmer-Anniversary-Journey-Mastery/dp/B0833F1T3V)

软件开发中最常见的问题不是“不会写代码”，而是对齐失败。你以为开发者理解了需求，直到看到交付物才发现双方想的根本不是一回事。

AI 时代也是一样。用户和 agent 之间天然存在沟通落差。解决办法不是让 agent 更自信，而是先进行一轮高质量追问，把需求、约束和分支判断讲清楚。

可以使用：

- [`/grill-me`](./skills/productivity/grill-me/SKILL.md) - 用于非代码场景的需求追问
- [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md) - 面向工程项目的需求追问，会同步项目语言和 ADR

这两个 skills 的目标，是在动手前帮助你和 agent 对齐，并把模糊想法压成可以执行的决策。

### 2. Agent 太啰嗦，也不懂项目语言

> With a ubiquitous language, conversations among developers and expressions of the code are all derived from the same domain model.
>
> Eric Evans, [Domain-Driven Design](https://www.amazon.co.uk/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)

一个项目刚开始时，开发者和领域专家经常使用不同语言。Agent 进入项目时也一样：如果它不知道项目里的核心术语，就会用很多泛泛而谈的话绕来绕去。

解决办法是维护一份共享语言文档，让 agent 能读懂项目术语、业务概念和架构决策。

<details>
<summary>示例</summary>

这里有一个来自 `course-video-manager` 仓库的 [`CONTEXT.md`](https://github.com/mattpocock/course-video-manager/blob/076a5a7a182db0fe1e62971dd7a68bcadf010f1c/CONTEXT.md)。比较下面两种说法：

- 变更前："There's a problem when a lesson inside a section of a course is made 'real' (i.e. given a spot in the file system)"
- 变更后："There's a problem with the materialization cascade"

第二种表达更短，因为它使用了项目内部已经定义过的共享语言。

</details>

[`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md) 会把这种共享语言机制带进需求追问过程：当术语、约束或决策变清楚时，就更新 `CONTEXT.md` 和 ADR。

共享语言不仅减少废话，还会带来几个直接收益：

- 变量、函数和文件更容易按同一套概念命名
- Agent 更容易在代码库里导航
- Agent 不需要每轮重新解释同一批背景，思考成本更低

### 3. 代码写出来但不能工作

> "Always take small, deliberate steps. The rate of feedback is your speed limit. Never take on a task that’s too big."
>
> David Thomas & Andrew Hunt, [The Pragmatic Programmer](https://www.amazon.co.uk/Pragmatic-Programmer-Anniversary-Journey-Mastery/dp/B0833F1T3V)

即使需求已经对齐，agent 仍然可能写出不能工作的代码。此时问题通常不在“提示词不够好”，而在反馈闭环太弱。

真实工程需要常规反馈：静态类型、浏览器验证、自动化测试、可复现的失败信号。

[`/tdd`](./skills/engineering/tdd/SKILL.md) 用红绿重构循环约束开发：先写失败测试，再让实现通过测试，最后重构。这样 agent 的每一步都有清晰反馈。

[`/diagnose`](./skills/engineering/diagnose/SKILL.md) 则把调试过程压成一个纪律化循环：复现、最小化、提出假设、加仪表、修复、补回归测试。

### 4. 项目变成一团泥

> "Invest in the design of the system _every day_."
>
> Kent Beck, [Extreme Programming Explained](https://www.amazon.co.uk/Extreme-Programming-Explained-Embrace-Change/dp/0321278658)

> "The best modules are deep. They allow a lot of functionality to be accessed through a simple interface."
>
> John Ousterhout, [A Philosophy Of Software Design](https://www.amazon.co.uk/Philosophy-Software-Design-2nd/dp/173210221X)

Agent 能显著加快写代码的速度，也会加快软件熵增。如果没有设计纪律，代码库会更快变复杂、更难改、更难测试。

这些 skills 把设计意识放进日常工作流：

- [`/to-prd`](./skills/engineering/to-prd/SKILL.md) 在生成 PRD 前要求你明确会触碰哪些模块
- [`/zoom-out`](./skills/engineering/zoom-out/SKILL.md) 要求 agent 跳出局部代码，解释它在整个系统中的位置
- [`/improve-codebase-architecture`](./skills/engineering/improve-codebase-architecture/SKILL.md) 帮你识别浅模块、坏接缝和可以加深的模块

## 总结

软件工程基本功在 agent 时代更重要，而不是更不重要。这个仓库试图把这些基本功压缩成一组可重复执行的 skills，帮助你更稳定地交付真实软件。

## 索引

### Engineering

日常代码工作相关 skills。

- **[diagnose](./skills/engineering/diagnose/SKILL.md)** — 严格的诊断循环，用于困难 bug 和性能回归：复现 → 最小化 → 假设 → 仪表化 → 修复 → 回归测试。
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)** — 结合现有领域模型追问计划，收紧术语，并在过程中更新 `CONTEXT.md` 和 ADR。
- **[triage](./skills/engineering/triage/SKILL.md)** — 用分诊角色的状态机处理议题。
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)** — 结合 `CONTEXT.md` 的领域语言和 `docs/adr/` 的历史决策，寻找可以加深模块、改善架构的位置。
- **[setup-matt-pocock-skills](./skills/engineering/setup-matt-pocock-skills/SKILL.md)** — 为仓库生成其它工程 skills 所需的配置：议题跟踪系统、分诊标签词汇、领域文档布局。每个仓库先运行一次。
- **[tdd](./skills/engineering/tdd/SKILL.md)** — 使用红绿重构循环进行测试驱动开发，一次推进一个垂直切片。
- **[to-issues](./skills/engineering/to-issues/SKILL.md)** — 把计划、规范或 PRD 拆成可以独立领取的 GitHub issues。
- **[to-prd](./skills/engineering/to-prd/SKILL.md)** — 把当前对话上下文整理成 PRD，并作为 GitHub issue 提交。
- **[zoom-out](./skills/engineering/zoom-out/SKILL.md)** — 要求 agent 抽高一层，解释陌生代码区域的上下文和系统位置。
- **[prototype](./skills/engineering/prototype/SKILL.md)** — 构建一次性原型，用于验证状态、业务逻辑、数据模型或 UI 设计。

### Productivity

非代码专用的通用工作流 skills。

- **[caveman](./skills/productivity/caveman/SKILL.md)** — 超压缩沟通模式，去掉填充语，同时保留技术准确性。
- **[grill-me](./skills/productivity/grill-me/SKILL.md)** — 围绕计划或设计进行高强度追问，直到决策树的关键分支被澄清。
- **[handoff](./skills/productivity/handoff/SKILL.md)** — 把当前对话压缩成交接文档，让另一个 agent 可以继续。
- **[write-a-skill](./skills/productivity/write-a-skill/SKILL.md)** — 创建结构正确、渐进披露、可附带资源的新 skill。

### Misc

低频但仍然保留的工具类 skills。

- **[git-guardrails-claude-code](./skills/misc/git-guardrails-claude-code/SKILL.md)** — 为 Claude Code 或 Codex 设置 hook，在危险 git 命令执行前阻止它们，例如 `push`、`reset --hard`、`clean`。
- **[migrate-to-shoehorn](./skills/misc/migrate-to-shoehorn/SKILL.md)** — 把测试文件里的 `as` 类型断言迁移到 `@total-typescript/shoehorn`。
- **[scaffold-exercises](./skills/misc/scaffold-exercises/SKILL.md)** — 创建包含章节、题目、答案和讲解的练习目录结构。
- **[setup-pre-commit](./skills/misc/setup-pre-commit/SKILL.md)** — 使用 Husky、lint-staged、Prettier、类型检查和测试设置预提交 hook。
