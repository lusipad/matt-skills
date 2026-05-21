# Hard limits on the number of questions during grilling

`/grill-me` skill（以及其它 skills 内部的 grilling sessions）不会强制最大问题数。增加可配置上限或硬性 ceiling 不在范围内。

## 为什么不在范围内

Grilling 有意保持开放式。它的目标是持续挖掘，直到决策树的每个分支都被解决：有些计划只需要三个问题，有些需要五十个。固定上限要么会在困难问题上过早截断有价值的探索，要么会在简单问题上显得武断。

如果 session 感觉太长，已有合适的 escape hatches：

- 用户可以随时停止 session，并接受当前计划状态。
- 用户可以用自然语言要求模型收尾、总结并继续。自然语言 steering 才是预期控制面，不是数字限制。

硬上限还会混淆两种不同失败模式：模型因为计划确实未充分说明而问很多问题（按预期工作），与模型提出重复或低价值问题（prompt 质量问题，不是数量问题）。后者应该在 skill prompt 里修，而不是加 counter。

## Prior requests

- #44 — "Codex just asked me 200 questions"
