---
name: diagnose
description: 当用户说 "diagnose this" / "debug this"、报告 bug、说某处 broken/throwing/failing，或描述性能回归时，用严格诊断循环处理困难 bug 和性能回归。
---

# Diagnose

这是用于困难 bug 的纪律。只有明确说明理由时，才跳过阶段。

探索代码库时，使用项目领域 glossary 建立相关模块的清晰 mental model，并检查即将触碰区域的 ADR。

## Phase 1 - 建立反馈闭环

**这就是这个 skill 的核心。** 其它部分都是机械动作。如果你有一个快速、确定、agent 可运行、能对 bug 给出 pass/fail 信号的闭环，就能找到原因：bisect、hypothesis-testing 和 instrumentation 都只是消费这个信号。如果没有闭环，盯着代码看多久都救不了你。

在这里投入不成比例的精力。**要激进，要有创造力，不要轻易放弃。**

### 构造闭环的方式，按大致顺序尝试

1. **Failing test**，放在能触达 bug 的接缝上：unit、integration、e2e 都可以。
2. **Curl / HTTP script**，打正在运行的 dev server。
3. **CLI invocation**，使用 fixture input，把 stdout 和 known-good snapshot diff。
4. **Headless browser script**（Playwright / Puppeteer）：驱动 UI，并断言 DOM / console / network。
5. **Replay a captured trace.** 把真实 network request / payload / event log 保存到磁盘，在隔离环境中 replay 这条 code path。
6. **Throwaway harness.** 启动系统最小子集（一个 service、mocked deps），用一次函数调用触发 bug code path。
7. **Property / fuzz loop.** 如果 bug 是“有时输出错误”，跑 1000 个随机输入并寻找 failure mode。
8. **Bisection harness.** 如果 bug 出现在两个已知状态之间（commit、dataset、version），自动化“在状态 X 启动、检查、重复”，这样可以 `git bisect run`。
9. **Differential loop.** 同一个输入分别跑 old-version vs new-version（或两个 configs），diff 输出。
10. **HITL bash script.** 最后手段。如果必须有人点击，就用 `scripts/hitl-loop.template.sh` 驱动**人**，让闭环仍然结构化。捕获的输出再反馈给你。

闭环搭对了，bug 就已经修好 90%。

### 迭代闭环本身

把闭环当作产品。一旦有了一个闭环，问：

- 能不能更快？（缓存 setup、跳过无关 init、缩小测试范围。）
- 信号能不能更锋利？（断言具体症状，而不是 “didn't crash”。）
- 能不能更确定？（固定时间、seed RNG、隔离 filesystem、冻结 network。）

一个 30 秒且 flaky 的闭环，只比没有闭环好一点点。一个 2 秒且确定的闭环，是调试超能力。

### 非确定性 bug

目标不是干净复现，而是**提高复现率**。把触发器循环 100 次，并行化，加 stress，缩小 timing windows，注入 sleeps。50% 复现率的 flaky bug 可以调；1% 不行。继续提高复现率，直到它可调试。

### 真的无法建立闭环时

停下来并明确说明。列出你尝试过什么。向用户要：(a) 能复现的环境访问权限，(b) 捕获的 artifact（HAR file、log dump、core dump、带 timestamps 的 screen recording），或 (c) 添加临时生产 instrumentation 的许可。**不要**在没有闭环时继续假设。

没有你信任的闭环前，不要进入 Phase 2。

## Phase 2 - 复现

运行闭环，亲眼看到 bug 出现。

确认：

- [ ] 闭环产生的是**用户**描述的 failure mode，而不是附近另一个失败。错 bug = 错修复。
- [ ] 失败能多次复现；对于非确定性 bug，复现率足够高，可以用来调试。
- [ ] 已捕获精确症状（error message、wrong output、slow timing），后续阶段能用它验证修复确实命中问题。

复现 bug 之前不要继续。

## Phase 3 - 提出假设

在测试任何假设前，先生成 **3-5 个排序后的 hypotheses**。只生成一个假设会让你锚定第一个看似合理的想法。

每个 hypothesis 都必须**可证伪**：说明它做出的预测。

> 格式："If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

如果你无法说明预测，这不是 hypothesis，只是 vibe。丢掉或收紧。

**测试前把排序列表展示给用户。** 用户往往有领域知识，可以立刻重排（“我们刚部署了 #3 相关变更”），也可能知道哪些假设已经被排除。这是低成本、高回报的 checkpoint。不要阻塞在这里；如果用户 AFK，就按你的排序继续。

## Phase 4 - 仪表化

每个 probe 都必须对应 Phase 3 中的一个具体预测。**一次只改变一个变量。**

工具偏好：

1. 如果环境支持，优先 **debugger / REPL inspection**。一个 breakpoint 胜过十条 logs。
2. 在能区分 hypotheses 的边界上打 **targeted logs**。
3. 永远不要 “log everything and grep”。

**给每条 debug log 加唯一前缀**，例如 `[DEBUG-a4f2]`。收尾时一次 grep 就能清干净。没有 tag 的 logs 容易活下来；有 tag 的 logs 要删除。

**性能分支。** 对性能回归，logs 通常是错工具。应先建立 baseline measurement（timing harness、`performance.now()`、profiler、query plan），再 bisect。先测量，再修复。

## Phase 5 - 修复 + 回归测试

在修复前写 regression test，但前提是存在**正确接缝**。

正确接缝指：测试能覆盖调用点上真实发生的 bug pattern。如果唯一可用接缝太浅（例如 bug 需要多个 callers 才会出现，但测试只有 single-caller；unit test 无法复制触发链），那里的 regression test 会给你虚假信心。

**如果不存在正确接缝，这本身就是发现。** 记录它。代码库架构正在阻止这个 bug 被锁住。把它标记给下一阶段。

如果存在正确接缝：

1. 把最小化 repro 变成该接缝上的 failing test。
2. 观察它失败。
3. 应用修复。
4. 观察它通过。
5. 用原始、未最小化场景重新运行 Phase 1 反馈闭环。

## Phase 6 - 清理 + 复盘

宣布完成前必须做：

- [ ] 原始 repro 不再复现（重新运行 Phase 1 闭环）
- [ ] Regression test 通过（或记录不存在正确接缝）
- [ ] 所有 `[DEBUG-...]` instrumentation 已删除（grep 前缀）
- [ ] 一次性 prototypes 已删除，或移动到明确标记的 debug location
- [ ] 在 commit / PR message 里说明最终正确的 hypothesis，让下一个调试者能学到东西

**然后问：什么本来可以防止这个 bug？** 如果答案涉及架构变化（没有好的 test seam、callers 缠绕、hidden coupling），把具体信息交给 `/improve-codebase-architecture` skill。建议要在修复之后提出，不要在修复之前；现在你掌握的信息更多。
