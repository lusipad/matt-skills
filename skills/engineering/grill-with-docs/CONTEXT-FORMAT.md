# CONTEXT.md 格式

## 结构

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## 规则

- **要有判断。** 同一个概念有多个说法时，选一个最佳术语，其它说法放进 `_Avoid_`，避免继续混用。
- **明确标出冲突。** 如果某个词已经被模糊使用，在 “Flagged ambiguities” 里写清楚冲突和最终约定。
- **定义要紧。** 最多一两句话。说明它是什么，不要写成它会做什么。
- **写出关系。** 用粗体标出术语名；关系很明确时，把一对多、一对一这类数量关系也写出来。
- **只记录项目语境里的专有概念。** timeout、error type、utility pattern 这类通用编程概念，即使项目大量使用，也不属于 `CONTEXT.md`。加术语前先问：这是这个项目语境独有的概念，还是通用编程概念？只有前者应该进入文档。
- **自然成组时加小标题。** 如果术语都属于同一个紧密区域，平铺列表就可以。
- **写一段示例对话。** 用开发者和领域专家的对话展示术语如何自然配合，并澄清相近概念的边界。

## 单上下文仓库与多上下文仓库

**单一上下文（大多数仓库）：** 仓库根目录有一个 `CONTEXT.md`。

**多个上下文：** 仓库根目录的 `CONTEXT-MAP.md` 列出各个上下文、它们所在的位置，以及彼此之间的关系：

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

这个 skill 会按以下规则判断应该使用哪种结构：

- 如果存在 `CONTEXT-MAP.md`，读取它来找到相关上下文
- 如果只有根目录的 `CONTEXT.md`，按单一上下文处理
- 如果两者都不存在，在第一个术语被确认时再创建根目录的 `CONTEXT.md`

当存在多个上下文时，推断当前主题与哪一个相关。如果不清楚，请询问。
