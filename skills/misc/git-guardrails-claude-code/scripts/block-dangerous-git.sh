#!/bin/bash

INPUT=$(cat)

if command -v jq >/dev/null 2>&1; then
  COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // .toolInput.command // .command // ""')
elif command -v python3 >/dev/null 2>&1; then
  COMMAND=$(echo "$INPUT" | python3 -c 'import json,sys
data=json.load(sys.stdin)
print((data.get("tool_input") or data.get("toolInput") or data).get("command", ""))')
elif command -v python >/dev/null 2>&1; then
  COMMAND=$(echo "$INPUT" | python -c 'import json,sys
data=json.load(sys.stdin)
print((data.get("tool_input") or data.get("toolInput") or data).get("command", ""))')
else
  echo "BLOCKED: cannot inspect command because jq/python is unavailable." >&2
  exit 2
fi

DANGEROUS_PATTERNS=(
  "git push"
  "git reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \."
  "git restore \."
  "push --force"
  "reset --hard"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches dangerous pattern '$pattern'. The user has prevented you from doing this." >&2
    exit 2
  fi
done

exit 0
