---
name: git-guardrails-claude-code
description: Set up Claude Code or Codex hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code or Codex.
---

# Setup Git Guardrails

Sets up a PreToolUse hook that intercepts and blocks dangerous git commands before Claude Code or Codex executes them.

The skill keeps its historical `git-guardrails-claude-code` name for compatibility, but the workflow supports both agents.

## What Gets Blocked

- `git push` (all variants including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

When blocked, the agent sees a message telling it that it does not have authority to access these commands.

## Steps

### 1. Ask target and scope

Ask the user which target to install for:

- **Claude Code**
- **Codex**
- **Both**

Then ask scope:

- **This project only**
- **All projects**

### 2. Copy the hook script

The bundled script is at: [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

Copy it to the target location based on target and scope:

- **Claude project**: `.claude/hooks/block-dangerous-git.sh`
- **Claude global**: `~/.claude/hooks/block-dangerous-git.sh`
- **Codex project**: `.codex/hooks/block-dangerous-git.sh`
- **Codex global**: `~/.codex/hooks/block-dangerous-git.sh`

Make it executable with `chmod +x`.

### 3. Add hook to settings

Add to the appropriate settings file.

**Claude project** (`.claude/settings.json`):

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

**Claude global** (`~/.claude/settings.json`):

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

If the settings file already exists, merge the hook into existing `hooks.PreToolUse` array — don't overwrite other settings.

**Codex project** (`.codex/hooks.json`):

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

**Codex global** (`~/.codex/hooks.json`):

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

If the Codex hooks file already exists, merge the hook into existing `hooks.PreToolUse` array — don't overwrite other hooks. Hooks are enabled by default in Codex; if the user's config explicitly disables hooks with `[features].hooks = false`, ask before changing it.

### 4. Ask about customization

Ask if user wants to add or remove any patterns from the blocked list. Edit the copied script accordingly.

### 5. Verify

Run a quick test:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

Should exit with code 2 and print a BLOCKED message to stderr.
