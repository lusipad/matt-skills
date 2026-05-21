# Interface Design for Testability

好接口会让测试自然出现：

1. **接收依赖，不要内部创建依赖**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **返回结果，不要只制造副作用**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **小表面积**
   - methods 越少，需要的测试越少
   - params 越少，测试 setup 越简单
