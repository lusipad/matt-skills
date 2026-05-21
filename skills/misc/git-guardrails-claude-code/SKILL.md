---
name: git-guardrails-claude-code
description: 当用户想为 Claude Code 或 Codex 添加 git 安全 hooks，阻止 push、reset --hard、clean、branch -D 等危险 git 命令执行前通过时使用。
---

# Setup Git Guardrails

设置一个 PreToolUse hook，在 Claude Code 或 Codex 执行危险 git 命令前拦截并阻止。

这个 skill 保留历史名称 `git-guardrails-claude-code` 以保持兼容，但工作流同时支持两个 agent。

## 会阻止什么

- `git push`（包括 `--force` 等所有变体）
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

命令被阻止时，agent 会看到一条消息，说明它没有权限访问这些命令。

## 步骤

### 1. 询问目标和范围

询问用户要安装到哪个目标：

- **Claude Code**
- **Codex**
- **Both**

然后询问范围：

- **This project only**
- **All projects**

### 2. 复制 hook 脚本

内置脚本位于：[scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

根据目标和范围复制到对应位置：

- **Claude project**：`.claude/hooks/block-dangerous-git.sh`
- **Claude global**：`~/.claude/hooks/block-dangerous-git.sh`
- **Codex project**：`.codex/hooks/block-dangerous-git.sh`
- **Codex global**：`~/.codex/hooks/block-dangerous-git.sh`

用 `chmod +x` 让它可执行。

### 3. 添加到 settings

写入对应 settings 文件。

**Claude project**（`.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Claude global**（`~/.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

如果 settings 文件已存在，把 hook merge 到现有 `hooks.PreToolUse` array，不要覆盖其它 settings。

**Codex project**（`.codex/hooks.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "\"$(git rev-parse --show-toplevel)/.codex/hooks/block-dangerous-git.sh\"",
            "statusMessage": "Checking git command"
          }
        ]
      }
    ]
  }
}
```

**Codex global**（`~/.codex/hooks.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "~/.codex/hooks/block-dangerous-git.sh",
            "statusMessage": "Checking git command"
          }
        ]
      }
    ]
  }
}
```

如果 Codex hooks 文件已存在，把 hook merge 到现有 `hooks.PreToolUse` array，不要覆盖其它 hooks。Codex 默认启用 hooks；如果用户 config 显式设置 `[features].hooks = false`，修改前先询问。

### 4. 询问是否自定义

询问用户是否要向 blocked list 添加或移除 pattern。按需编辑复制后的脚本。

### 5. 验证

运行快速测试：

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

应该以 code 2 退出，并向 stderr 打印 BLOCKED 消息。
