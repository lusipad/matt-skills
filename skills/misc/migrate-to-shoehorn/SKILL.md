---
name: migrate-to-shoehorn
description: 当用户提到 shoehorn、想替换测试里的 `as`，或需要在测试中传 partial test data 时，把测试文件从 `as` 类型断言迁移到 @total-typescript/shoehorn。
---

# Migrate to Shoehorn

## 为什么用 shoehorn？

`shoehorn` 允许你在测试中传 partial data，同时让 TypeScript 满意。它用更类型安全的替代方案取代 `as` 断言。

**只用于测试代码。** 不要在 production code 中使用 shoehorn。

测试里 `as` 的问题：

- 它训练你忽略类型系统
- 必须手动指定目标类型
- 为故意错误数据写 double-as（`as unknown as Type`）

## 安装

```bash
npm i @total-typescript/shoehorn
```

## 迁移模式

### 大对象但只需要少数字段

Before:

```ts
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
  // ...20 more properties
};

it("gets user by id", () => {
  // Only care about body.id but must fake entire Request
  getUser({
    body: { id: "123" },
    headers: {},
    cookies: {},
    // ...fake all 20 properties
  });
});
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

it("gets user by id", () => {
  getUser(
    fromPartial({
      body: { id: "123" },
    }),
  );
});
```

### `as Type` -> `fromPartial()`

Before:

```ts
getUser({ body: { id: "123" } } as Request);
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` -> `fromAny()`

Before:

```ts
getUser({ body: { id: 123 } } as unknown as Request); // wrong type on purpose
```

After:

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

## 什么时候用哪个

| Function        | Use case                                           |
| --------------- | -------------------------------------------------- |
| `fromPartial()` | Pass partial data that still type-checks           |
| `fromAny()`     | Pass intentionally wrong data (keeps autocomplete) |
| `fromExact()`   | Force full object (swap with fromPartial later)    |

## 工作流

1. **收集需求**，询问用户：
   - 哪些 test files 里的 `as` assertions 正在造成问题？
   - 是否在处理大对象，而测试只关心少数字段？
   - 是否需要为了错误测试传入故意错误的数据？

2. **安装并迁移**：
   - [ ] 安装：`npm i @total-typescript/shoehorn`
   - [ ] 查找包含 `as` assertions 的测试文件：`grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"`
   - [ ] 把 `as Type` 替换为 `fromPartial()`
   - [ ] 把 `as unknown as Type` 替换为 `fromAny()`
   - [ ] 添加 `@total-typescript/shoehorn` imports
   - [ ] 运行 type check 验证
