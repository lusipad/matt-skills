#!/usr/bin/env bash
# Human-in-the-loop 复现闭环。
# 复制这个文件，编辑下面的步骤，然后运行。
# agent 运行脚本；用户按终端中的提示操作。
#
# Usage:
#   bash hitl-loop.template.sh
#
# 两个 helper：
#   step "<instruction>"          → 显示指令，等待 Enter
#   capture VAR "<question>"      → 显示问题，把回答读取到 VAR
#
# 结束时，捕获值会以 KEY=VALUE 打印，方便 agent 解析。

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- edit below ---------------------------------------------------------

step "打开 http://localhost:3000 并登录。"

capture ERRORED "点击 'Export' 按钮。是否报错？(y/n)"

capture ERROR_MSG "粘贴错误信息（如果没有，写 'none'）："

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
