# When to Mock

只在**系统边界** mock：

- 外部 APIs（payment、email 等）
- 数据库（有时；优先 test DB）
- 时间 / 随机性
- 文件系统（有时）

不要 mock：

- 你自己的 classes/modules
- 内部协作者
- 任何你控制的东西

## Designing for Mockability

在系统边界处，设计容易 mock 的接口：

**1. 使用 dependency injection**

把外部依赖传进来，而不是在内部创建：

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 优先 SDK-style interfaces，而不是 generic fetchers**

为每个外部操作创建具体函数，不要用一个带条件逻辑的通用函数：

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK approach 的好处：

- 每个 mock 返回一个具体 shape
- test setup 中不需要条件逻辑
- 更容易看出测试覆盖了哪些 endpoints
- 每个 endpoint 都有类型安全
