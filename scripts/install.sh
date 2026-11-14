#!/usr/bin/env bash
# Selectively install xc-skill skills into an agent skills directory.
# Default target: ~/.qoder-cn/skills (Qoder). Override with --target or XC_SKILLS_TARGET.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$REPO_DIR/skills"
TARGET="${XC_SKILLS_TARGET:-$HOME/.qoder-cn/skills}"
MODE="link"
ALL=0
LIST=0
NAMES=()

usage() {
  cat <<'EOF'
Usage: install.sh [options] [skill-name ...]

Options:
  --list           List available skills
  --all            Install all skills
  --copy           Copy directories instead of symlinking
  --target DIR     Install target (default: ~/.qoder-cn/skills, env XC_SKILLS_TARGET)
  -h, --help       Show this help

Examples:
  install.sh --list
  install.sh xc-article-illustrator
  install.sh --target ~/.claude/skills --all
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list) LIST=1; shift ;;
    --all) ALL=1; shift ;;
    --copy) MODE="copy"; shift ;;
    --target) TARGET="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; usage; exit 1 ;;
    *) NAMES+=("$1"); shift ;;
  esac
done

available() {
  local d
  for d in "$SRC_DIR"/*/; do
    [[ -f "$d/SKILL.md" ]] && basename "$d"
  done
}

if [[ $LIST -eq 1 ]]; then
  echo "Available skills (source: $SRC_DIR):"
  while IFS= read -r name; do
    desc="$(sed -n 's/^description: *//p' "$SRC_DIR/$name/SKILL.md" | head -1 | cut -c1-100)"
    printf '  %-28s %s\n' "$name" "$desc"
  done < <(available)
  exit 0
fi

if [[ $ALL -eq 1 ]]; then
  while IFS= read -r name; do NAMES+=("$name"); done < <(available)
fi

if [[ ${#NAMES[@]} -eq 0 ]]; then
  usage
  exit 1
fi

mkdir -p "$TARGET"
installed=0 skipped=0 failed=0

for name in "${NAMES[@]}"; do
  src="$SRC_DIR/$name"
  dst="$TARGET/$name"
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "FAIL  $name: no SKILL.md in $src" >&2
    failed=$((failed+1)); continue
  fi
  if [[ -L "$dst" ]]; then
    current="$(readlink "$dst")"
    if [[ "$current" == "$src" && "$MODE" == "link" ]]; then
      echo "OK    $name: already linked"
      installed=$((installed+1)); continue
    fi
    rm "$dst"
  elif [[ -e "$dst" ]]; then
    echo "SKIP  $name: $dst exists and is not a symlink (remove it manually to reinstall)" >&2
    skipped=$((skipped+1)); continue
  fi
  if [[ "$MODE" == "link" ]]; then
    ln -s "$src" "$dst"
    echo "OK    $name: linked -> $dst"
  else
    cp -R "$src" "$dst"
    echo "OK    $name: copied -> $dst"
  fi
  installed=$((installed+1))
done

echo "Done: $installed installed, $skipped skipped, $failed failed (target: $TARGET)"
[[ $failed -eq 0 ]]