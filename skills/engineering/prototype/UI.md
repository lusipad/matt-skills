# UI Prototype

在同一个 route 上生成**几个完全不同的 UI 变体**，通过底部浮动栏切换。用户在浏览器里来回比较，选择一个，或从多个变体里拼出想要的方向，然后丢掉其余部分。

如果问题是逻辑或状态，而不是“它应该长什么样”，就走错分支了。使用 [LOGIC.md](LOGIC.md)。

## 什么时候适合这个形状

- “这个页面应该长什么样？”
- “我想在确定前看几个 dashboard 方案。”
- “给 settings screen 试一个不同布局。”
- 任何用户本来会花一天在脑子里比较三种模糊 mockup 的情况。

## 两个子形状，强烈优先 A

UI prototype 贴着应用其它部分时最容易判断：真实 header、真实 sidebar、真实数据、真实密度。单独的一次性 route 是真空环境，每个变体孤立看都还行。只要有合理的现有页面可以承载变体，就默认使用子形状 A。只有原型确实没有附近归宿时，才使用子形状 B。

### 子形状 A：调整现有页面（优先）

route 已经存在。变体渲染在**同一个 route**，通过 `?variant=` URL search param 控制。现有 data fetching、params、auth 都保留，只替换渲染。默认选择这个，除非有具体理由不用。

如果原型化的东西还没有页面，但自然会放进某个已有页面（dashboard 新 section、settings 新 card、现有 flow 的新 step），也仍然属于子形状 A。把变体挂进宿主页面里。

### 子形状 B：新页面（最后手段）

只有当被原型化的东西真的没有现有页面可放时才使用，例如全新的顶层 surface，或无法合理嵌入任何地方的 flow。

按项目已有路由约定创建**一次性 route**，不要发明新的顶层结构。命名要明显是 prototype，例如 path 或 filename 里包含 `prototype`。同样使用 `?variant=` 模式。

在决定使用子形状 B 前做一次 sanity-check：真的没有现有页面可以嵌进去吗？空 route 会隐藏真实页面数据和密度暴露出来的设计问题。

两个子形状使用同一个底部浮动栏。

## 流程

### 1. 写下问题并选择 N

默认 **3 个变体**。超过 5 个就不再是 radically different，而会变成噪音；上限 5。

在原型位置或文件顶部注释里写一行计划：

> "Three variants of the settings page, switchable via `?variant=`, on the existing `/settings` route."

无论用户是否在场，这都能让方向可检查。

### 2. 生成结构明显不同的变体

草拟每个变体，并让它们遵守：

- 页面目标和可访问数据
- 项目的 component library / styling system（TailwindCSS、shadcn、MUI、plain CSS 等）
- 清晰的 exported component name，例如 `VariantA`、`VariantB`、`VariantC`

变体必须**结构不同**：不同布局、不同信息层级、不同 primary affordance，而不只是颜色不同。三个稍微调过的 card grid 不是 UI prototype，而是 wallpaper。如果两个草稿太像，就带着明确约束重做一个，例如 “do not use a card grid”。

### 3. 串起来

在 route 上创建一个 switcher component：

```tsx
// pseudo-code — adapt to the project's framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

子形状 A（现有页面）：保留 switcher 之上的所有现有 data fetching；只有每个 variant 的 rendered subtree 改变。

子形状 B（新页面）：`/prototype/<name>` 下的一次性 route 挂载同一个 switcher。

### 4. 构建底部浮动切换器

屏幕底部居中的小型 fixed bar，包含三部分：

- **Left arrow**：切到上一个变体（循环）。
- **Variant label**：显示当前 variant key；如果 variant 导出名称，也显示名称。例如 `B - Sidebar layout`。
- **Right arrow**：切到下一个变体（循环）。

行为：

- 点击箭头更新 URL search param（使用框架 router，例如 Next 的 `router.replace`、React Router 的 `navigate`），让 variant 可分享、刷新后稳定。
- 键盘：`←` 和 `→` 也切换。焦点在 `<input>`、`<textarea>` 或 `[contenteditable]` 时不要拦截方向键。
- 视觉上要和页面区分开，例如高对比 pill、轻微 shadow，让它显然不是正在评估的设计的一部分。
- 生产构建中隐藏：用 `process.env.NODE_ENV !== 'production'` 或等价检查 gate，避免误合并时把切换栏发给用户。

把 switcher 放到一个共享组件里，方便两个子形状复用。位置跟随项目共享 UI 的习惯。

### 5. 交给用户

给出 URL 和 `?variant=` keys。用户会自己翻看。最有价值的反馈通常是 **“我想要 B 的 header 加 C 的 sidebar”**，那才是真正想要的设计。

### 6. 捕获答案并清理

当某个变体胜出，写下它是哪一个以及为什么（commit message、ADR、issue，或用户不在场时原型旁边的 `NOTES.md`）。然后：

- **子形状 A**：删除失败变体和 switcher；把胜出设计折进现有页面。
- **子形状 B**：把胜出变体提升为真实 route，删除一次性 route 和 switcher。

不要把 variant components 或 switcher 留在那里。它们会很快腐烂，并让下一个读者困惑。

## 反模式

- **只有颜色或文案不同的变体。** 那是 tweak，不是 prototype。真正的变体在结构上有分歧。
- **变体共享太多代码。** 共享 `<Header>` 可以；共享 `<Layout>` 会破坏原型目的。每个变体都应该能扔掉整个 layout。
- **把变体接到真实 mutation。** Read-only prototype 没问题。如果变体需要 mutate，就指向 stub；问题是“它应该长什么样”，不是“后端能不能工作”。
- **把 prototype 直接提升为 production。** 变体代码是在原型约束下写的（无测试、最小错误处理）。折进真实产品时要按正常标准重写。
