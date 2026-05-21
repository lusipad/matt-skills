---
name: setup-pre-commit
description: 当用户想添加 pre-commit hooks、设置 Husky、配置 lint-staged，或在 commit 时运行格式化、类型检查和测试时使用。
---

# Setup Pre-Commit Hooks

## 会设置什么

- **Husky** pre-commit hook
- **lint-staged**，对所有 staged files 运行 Prettier
- **Prettier** config（如果缺失）
- pre-commit hook 中的 **typecheck** 和 **test** scripts

## 步骤

### 1. 检测 package manager

检查 `package-lock.json`（npm）、`pnpm-lock.yaml`（pnpm）、`yarn.lock`（yarn）、`bun.lockb`（bun）。使用已存在的那个。不清楚时默认 npm。

### 2. 安装依赖

安装为 devDependencies：

```
husky lint-staged prettier
```

### 3. 初始化 Husky

```bash
npx husky init
```

这会创建 `.husky/` 目录，并向 package.json 添加 `prepare: "husky"`。

### 4. 创建 `.husky/pre-commit`

写入这个文件（Husky v9+ 不需要 shebang）：

```
npx lint-staged
npm run typecheck
npm run test
```

**适配**：把 `npm` 替换成检测到的 package manager。如果 repo 的 package.json 没有 `typecheck` 或 `test` script，就省略对应行并告诉用户。

### 5. 创建 `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. 创建 `.prettierrc`（如果缺失）

只有没有 Prettier config 时才创建。使用默认值：

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. 验证

- [ ] `.husky/pre-commit` 存在且可执行
- [ ] `.lintstagedrc` 存在
- [ ] package.json 中的 `prepare` script 是 `"husky"`
- [ ] prettier config 存在
- [ ] 运行 `npx lint-staged` 验证可用

### 8. Commit

Stage 所有变更或新建文件，并提交信息：`Add pre-commit hooks (husky + lint-staged + prettier)`

这会跑过新的 pre-commit hooks，是一次很好的 smoke test。

## Notes

- Husky v9+ 的 hook files 不需要 shebang
- `prettier --ignore-unknown` 会跳过 Prettier 不能解析的文件（图片等）
- pre-commit 先运行 lint-staged（快，只处理 staged files），再运行完整 typecheck 和 tests
