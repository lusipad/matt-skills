---
name: ubiquitous-language
description: 当用户想定义领域术语、构建 glossary、收紧命名、创建 ubiquitous language，或提到 domain model / DDD 时，从当前对话中提取 DDD 风格术语表。
disable-model-invocation: true
---

# Ubiquitous Language

从当前对话中提取领域术语，整理成一致的 glossary，并保存到本地文件。

## 流程

1. **扫描对话**，找出领域相关名词、动词和概念
2. **识别问题**：
   - 同一个词被用于不同概念（歧义）
   - 同一个概念被多个词表达（同义词）
   - 模糊或 overloaded 的术语
3. **提出 canonical glossary**，并做有判断的术语选择
4. **按下面格式写入工作目录中的 `UBIQUITOUS_LANGUAGE.md`**
5. **在对话中给出 inline summary**

## 输出格式

写一个结构如下的 `UBIQUITOUS_LANGUAGE.md`：

```md
# Ubiquitous Language

## Order lifecycle

| Term        | Definition                                              | Aliases to avoid      |
| ----------- | ------------------------------------------------------- | --------------------- |
| **Order**   | A customer's request to purchase one or more items      | Purchase, transaction |
| **Invoice** | A request for payment sent to a customer after delivery | Bill, payment request |

## People

| Term         | Definition                                  | Aliases to avoid       |
| ------------ | ------------------------------------------- | ---------------------- |
| **Customer** | A person or organization that places orders | Client, buyer, account |
| **User**     | An authentication identity in the system    | Login, account         |

## Relationships

- An **Invoice** belongs to exactly one **Customer**
- An **Order** produces one or more **Invoices**

## Example dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No — an **Invoice** is only generated once a **Fulfillment** is confirmed. A single **Order** can produce multiple **Invoices** if items ship in separate **Shipments**."
> **Dev:** "So if a **Shipment** is cancelled before dispatch, no **Invoice** exists for it?"
> **Domain expert:** "Exactly. The **Invoice** lifecycle is tied to the **Fulfillment**, not the **Order**."

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — these are distinct concepts: a **Customer** places orders, while a **User** is an authentication identity that may or may not represent a **Customer**.
```

## 规则

- **要有判断。** 同一概念有多个说法时，选一个最佳术语，其它说法放进 aliases to avoid。
- **明确标出冲突。** 如果对话里的术语有歧义，在 “Flagged ambiguities” 中写出来，并给出明确建议。
- **只包含领域专家会关心的术语。** 模块或类名只有在领域语言中有含义时才加入。
- **定义要紧。** 最多一句话。说明它是什么，而不是它做什么。
- **写出关系。** 用粗体术语名，并在明显时表达数量关系。
- **只包含领域术语。** 跳过数组、函数、endpoint 这类通用编程概念，除非它在该领域里有特殊含义。
- **自然成组时分表。** 可以按 subdomain、lifecycle 或 actor 分组。每组有自己的标题和表格。如果所有术语都属于单一内聚领域，一张表就够了，不要强行分组。
- **写示例对话。** 用开发者和领域专家之间 3-5 轮短对话展示术语如何自然互动。对话应澄清相近概念边界，并准确使用术语。

<example>

## Example dialogue

> **Dev:** "How do we test the **Sync Service** without Docker?"

> **Domain expert:** "Provide a **Filesystem Layer** instead of a **Docker Layer**. It implements the same **Sandbox Service** interface but uses local directories as the **Sandbox**."

> **Dev:** "So **Sync** still creates a **Bundle** and extracts it?"

> **Domain expert:** "Exactly. The **Sync Service** doesn't know which layer it's talking to. It calls `exec` and `copyIn`; the **Filesystem Layer** just runs those as local shell commands."

</example>

## 重新运行

在同一对话中再次调用时：

1. 读取已有 `UBIQUITOUS_LANGUAGE.md`
2. 纳入后续讨论中的新术语
3. 如果理解发生变化，更新定义
4. 重新标记新的歧义
5. 重写示例对话以纳入新术语
