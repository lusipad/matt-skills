# HTML 报告格式

架构审查报告应呈现为一个自包含 HTML 文件，写到操作系统临时目录。Tailwind 和 Mermaid 都从 CDN 加载。Mermaid 适合处理图形关系；手写 div 和 inline SVG 适合更 editorial 的视觉表达，例如质量图、横截面。两者混用，不要所有东西都交给 Mermaid，否则报告会显得很普通。

## 脚手架

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

包含仓库名、日期和紧凑图例：实心框 = 模块，虚线 = 接缝，红色箭头 = 泄漏，厚深色框 = 深模块。不要写介绍段落，直接进入候选项。

## 候选卡片

图表承担主要解释重量。文字要短、朴素、严格使用术语表（[LANGUAGE.md](LANGUAGE.md)）。

每个候选项是一个 `<article>`：

- **Title**：短标题，命名这次加深，例如 “Fold the Order intake pipeline”。
- **Badge row**：推荐强度（`Strong` = emerald，`Worth exploring` = amber，`Speculative` = slate），加上依赖类别 badge（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **Files**：等宽列表，`font-mono text-sm`。
- **Before / After diagram**：核心区域，两列并排。模式见下文。
- **Problem**：一句话。哪里痛。
- **Solution**：一句话。会改变什么。
- **Wins**：短 bullet，每条不超过 6 个词。例如 “Tests hit one interface”、“Pricing logic stops leaking”、“Delete 4 shallow wrappers”。
- **ADR callout**（如适用）：amber 色框里一行。

不要写解释性长段落。如果图表需要一整段文字才能看懂，就重画图。

## 图表模式

选择适合候选项的模式，并混合使用。不要让每张图都长得一样；多样性是重点之一。

### Mermaid 图（依赖和调用流的主力）

当重点是 “X calls Y calls Z, and look at the mess” 时，使用 Mermaid `flowchart` 或 `graph`。把它包进 Tailwind 样式卡片里，避免像外来物。用 `classDef` 把泄漏边标红、深模块标深色。Sequence diagram 适合表达“之前 6 次往返，之后 1 次”。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手写盒子和箭头（当 Mermaid 布局碍事时）

模块用带边框和标签的 `<div>` 表达。箭头用绝对定位的 inline SVG `<line>` 或 `<path>`。如果你希望 “after” 图像一个厚边框深模块、内部结构较淡，就用这个模式；Mermaid 很难渲染出正确权重。

### 横截面（适合表现层层浅度）

堆叠水平条（`h-12 border-l-4`）展示调用经过的层。Before：6 个几乎不做事的薄层。After：1 条粗带，标出整合后的责任。

### 质量图（适合表现“接口和实现一样宽”）

每个模块两个矩形：一个表示接口表面积，一个表示实现。Before：接口矩形几乎和实现矩形一样高（浅）。After：接口矩形更短，实现矩形更高（深）。

### 调用图折叠

Before：函数调用树渲染成嵌套框。After：同一棵树折叠成一个盒子，内部调用以淡化方式显示。

## 风格指导

- Lean editorial，不是 corporate dashboard。留足空白。标题可选 serif（`font-serif` 配 stone/slate 效果不错）。
- 谨慎用色：一种强调色（emerald 或 indigo），再加 red 表示泄漏、amber 表示 warning。
- 图表高度保持约 320px，让 before/after 可以舒服地并排，不需要滚动。
- 图内模块标签使用 `text-xs uppercase tracking-wider`；它们应该像 schematic，不像 UI。
- 脚本只允许 Tailwind CDN 和 Mermaid ESM import。报告是静态的，除了 Mermaid 自身渲染外没有应用代码或交互。

## Top Recommendation 区块

一张更大的卡。候选项名称、一句话原因、指向对应卡片的 anchor link。仅此而已。

## 语气

Simple English，简洁，但架构名词和动词必须直接来自 [LANGUAGE.md](LANGUAGE.md)。简洁不是漂移术语的借口。

**准确使用：** module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**不要替代：** component、service、unit（指 module 时） · API、signature（指 interface 时） · boundary（指 seam 时） · layer、wrapper（指 module 时）。

**符合风格的短句：**

- “The Order intake module is shallow: interface almost matches implementation.”
- “Pricing leaks through completely.”
- “Deepen it: one interface, one test surface.”
- “Two adapters prove the seam: HTTP in production, in-memory in tests.”

**Wins bullet** 要用术语命名收益：*“Locality: bugs collapse into one module”*、*“Leverage: one interface, N call sites”*、*“Interface shrinks; implementation absorbs wrappers”*。不要写 *“easier to maintain”* 或 *“cleaner code”*，这些不是术语表里的词，也没有定位。

不要 hedge，不要清嗓子，不要写 “It is worth noting that...”。一句话能变成 bullet，就变成 bullet。Bullet 能删，就删。如果某个术语不在 [LANGUAGE.md](LANGUAGE.md)，先查清楚，再决定是否需要发明新词。
