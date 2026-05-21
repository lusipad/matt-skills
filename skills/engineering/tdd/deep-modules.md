# Deep Modules

来自《A Philosophy of Software Design》：

**Deep module** = 小接口 + 大量实现

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
│                     │
└─────────────────────┘
```

**Shallow module** = 大接口 + 少量实现（避免）

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

设计接口时问：

- 能不能减少 methods 数量？
- 能不能简化参数？
- 能不能把更多复杂性藏到内部？
