# Refactor Candidates

TDD cycle 之后，寻找：

- **Duplication** -> 抽出 function/class
- **Long methods** -> 拆成 private helpers（测试仍然只测 public interface）
- **Shallow modules** -> 合并或加深
- **Feature envy** -> 把逻辑移动到数据所在处
- **Primitive obsession** -> 引入 value objects
- **Existing code**：新代码暴露出的现有问题
