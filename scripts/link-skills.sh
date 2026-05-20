#!/usr/bin/env bash
set -euo pipefail

# Links shipped skills in the repository to local agent skill directories:
# - ~/.claude/skills for Claude Code
# - ~/.agents/skills for Codex

REPO="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-all}"

usage() {
  echo "usage: $0 [all|claude|codex]" >&2
}

destinations() {
  case "$TARGET" in
    all)
      printf '%s\n' "$HOME/.claude/skills" "$HOME/.agents/skills"
      ;;
    claude)
      printf '%s\n' "$HOME/.claude/skills"
      ;;
    codex)
      printf '%s\n' "$HOME/.agents/skills"
      ;;
    *)
      usage
      exit 2
      ;;
  esac
}

link_into() {
  dest="$1"

  # If the destination is a symlink that resolves into this repo, we'd end up
  # writing the per-skill symlinks back into the repo's own skills/ tree.
  if [ -L "$dest" ]; then
    resolved="$(readlink -f "$dest")"
    case "$resolved" in
      "$REPO"|"$REPO"/*)
        echo "error: $dest is a symlink into this repo ($resolved)." >&2
        echo "Remove it and re-run; the script will recreate it as a real dir." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -p "$dest"

  find "$REPO/skills/engineering" "$REPO/skills/productivity" "$REPO/skills/misc" \
    -mindepth 2 -maxdepth 2 -name SKILL.md -print0 |
  while IFS= read -r -d '' skill_md; do
    src="$(dirname "$skill_md")"
    name="$(basename "$src")"
    target="$dest/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "error: $target already exists and is not a symlink." >&2
      exit 1
    fi

    ln -sfn "$src" "$target"
    echo "linked $name -> $src"
  done
}

destinations |
while IFS= read -r dest; do
  link_into "$dest"
done
