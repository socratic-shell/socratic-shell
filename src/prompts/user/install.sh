#!/bin/bash
set -euo pipefail

# Socratic Shell User Patterns Installer
# Run this script from a checked-out socratic-shell repository
# It will add imports to ~/.claude/CLAUDE.md that reference this repo's patterns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_FILE="$CLAUDE_DIR/CLAUDE.md"

echo "Installing socratic-shell user patterns..."
echo "Repository: $REPO_ROOT"
echo "Claude config: $CLAUDE_FILE"

# Create ~/.claude directory if it doesn't exist
mkdir -p "$CLAUDE_DIR"

# Create CLAUDE.md if it doesn't exist
if [[ ! -f "$CLAUDE_FILE" ]]; then
    echo "Creating new $CLAUDE_FILE"
    touch "$CLAUDE_FILE"
fi

# Check if socratic-shell patterns are already referenced
if grep -q "socratic-shell" "$CLAUDE_FILE" && grep -q "prompts/user/main.md" "$CLAUDE_FILE"; then
    echo "⚠️  Socratic-shell patterns already appear to be installed in $CLAUDE_FILE"
    echo "Please review manually to avoid duplicates."
    exit 1
fi

# Add import line
echo "" >> "$CLAUDE_FILE"
echo "# Socratic Shell Collaboration Patterns" >> "$CLAUDE_FILE"
echo "@$REPO_ROOT/src/prompts/user/main.md" >> "$CLAUDE_FILE"

echo "✅ Successfully added socratic-shell patterns to $CLAUDE_FILE"
echo ""
echo "The following import was added:"
echo "  @$REPO_ROOT/src/prompts/user/main.md"
echo ""
echo "To uninstall, remove the socratic-shell lines from $CLAUDE_FILE"