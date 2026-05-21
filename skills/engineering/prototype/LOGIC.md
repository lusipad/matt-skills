# Logic Prototype

一个很小的交互式终端应用，让用户手动驱动状态模型。问题涉及**业务逻辑、状态转移或数据形状**时使用它：这类东西纸面上看起来合理，只有推过真实案例才会暴露不对劲。

## 什么时候适合这个形状

- “我不确定这个状态机能不能处理 X 之后发生 Y 的边界情况。”
- “这个数据模型真的能表达某种场景吗？”
- “我想在正式实现前感受一下 API 应该长什么样。”
- 任何用户想要**按按钮并观察状态变化**的场景。

如果问题是“这应该长什么样”，就走错分支了。使用 [UI.md](UI.md)。

## 流程

### 1. 写下问题

写代码前，先写明你正在原型化哪个状态模型、要回答什么问题。用一段话写在原型 README 或文件顶部注释里。回答错问题的 logic prototype 纯属浪费；问题必须明确，方便用户当前检查，也方便之后 AFK 回来检查。

### 2. 选择语言

使用宿主项目已经使用的语言。如果项目没有明显 runtime（例如文档仓库），询问用户。

匹配项目现有工具约定，不要为了原型新增 package manager 或 runtime。

### 3. 把逻辑隔离到可移植模块里

把真正回答问题的逻辑放在一个小而纯的接口后面，使它之后可以被拎出来放进真实代码库。TUI 外壳是一次性的；逻辑模块不应该是。

正确形状取决于问题：

- **纯 reducer**：`(state, action) => state`。适合 action 是离散事件、state 是单一值的情况。
- **状态机**：显式 states 和 transitions。适合“当前哪些 action 合法”本身就是问题的一部分。
- **一小组作用在 plain data type 上的纯函数**。适合没有隐式当前状态、只有转换的情况。
- **带清晰 method surface 的 class 或 module**。适合逻辑确实拥有持续内部状态的情况。

选择最适合问题的形状，而不是最容易接 TUI 的形状。保持纯粹：无 I/O、无 terminal code、不要用 `console.log` 控制流程。TUI 导入它并调用它；依赖不要反向流动。

这就是原型能在自身生命周期之后仍然有价值的原因。问题回答完后，验证过的 reducer / machine / function set 可以放进真实模块；TUI shell 删除。

### 4. 构建最小 TUI 来展示状态

做成**轻量 TUI**：每个 tick 清屏（`console.clear()` / `print("\033[2J\033[H")` / equivalent），然后重绘整个 frame。用户应该看到一个稳定视图，而不是不断增长的 scrollback。

每个 frame 按顺序包含两部分：

1. **Current state**：pretty-print，并且 diff-friendly（一行一个字段，或格式化 JSON）。字段名或 section header 用 **bold**，次要上下文（timestamps、IDs、derived values）用 **dim**。原生 ANSI escape codes 足够：`\x1b[1m` bold，`\x1b[2m` dim，`\x1b[0m` reset。除非项目已经有样式库，否则不要新增。
2. **Keyboard shortcuts**：放在底部，例如 `[a] add user  [d] delete user  [t] tick clock  [q] quit`。可以加粗 key、淡化描述，或反过来，只要清楚。

行为：

1. **初始化状态**：一个内存对象或 struct。启动时渲染第一帧。
2. **一次读取一个 keystroke（或一行）**，分发到 handler 修改状态。
3. **每次 action 后重绘完整 frame**，不要 append，要 replace。
4. **循环直到 quit。**

整个 frame 应该能放进一个屏幕。

### 5. 一个命令运行

把脚本加到项目已有 task runner（`package.json` scripts、`Makefile`、`justfile`、`pyproject.toml`）。用户应该能运行 `pnpm run <prototype-name>` 或等价命令，不需要记路径。

如果宿主项目没有 task runner，就把命令写在原型 README 顶部。

### 6. 交给用户

告诉用户运行命令。让他们自己驱动；有价值的时刻通常是“等等，这不应该能发生”或“我以为 X 会不一样”。这些就是想法里的 bug。如果他们想加新 action，就加。原型会演进。

### 7. 捕获答案

原型完成任务后，唯一值得保留的是问题答案。如果用户在场，问它教会了他们什么。如果用户不在，在原型旁边留下 `NOTES.md`，方便在删除原型前补上答案（也可以由你在观察会话后填写）。

## 反模式

- **不要加测试。** 需要测试的原型已经不再是原型。
- **不要接真实数据库。** 除非问题专门关于持久化，否则使用 in-memory store。
- **不要泛化。** 不讨论“以后如果要支持 X”。原型只回答一个问题。
- **不要把逻辑和 TUI 糊在一起。** 如果 reducer / state machine 引用了 `console.log`、prompt 或 terminal escape codes，它就不再可移植。TUI 应该只是纯模块上的薄壳。
- **不要把 TUI shell 发到生产。** Shell 为终端手动驱动优化；背后的逻辑模块才是值得保留的部分。
