# Good and Bad Tests

## 好测试

**Integration-style**：通过真实接口测试，不 mock 内部部分。

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特征：

- 测试用户或调用者关心的行为
- 只使用 public API
- 能承受内部重构
- 描述 WHAT，不描述 HOW
- 每个测试一个逻辑断言

## 坏测试

**Implementation-detail tests**：和内部结构耦合。

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

红旗：

- mock 内部协作者
- 测试 private methods
- 断言调用次数或调用顺序
- 行为没变，重构后测试坏了
- 测试名描述 HOW 而不是 WHAT
- 绕过接口，用外部手段验证

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```
