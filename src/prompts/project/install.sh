#!/bin/bash
set -euo pipefail

# Socratic Shell Project Patterns Installer
# Syncs team collaboration patterns from GitHub to .socratic-shell/
# Usage: curl https://raw.githubusercontent.com/nikomatsakis/socratic-shell/main/src/prompts/project/install.sh | bash

REPO_OWNER="nikomatsakis"
REPO_NAME="socratic-shell"
TARGET_DIR=".socratic-shell"
STAMP_FILE="$TARGET_DIR/.commit-stamp"

echo "🔄 Syncing socratic-shell project patterns..."

# Check if we're in a git repository
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "❌ Not in a git repository. Please run from your project root."
    exit 1
fi

# Check for uncommitted changes in .socratic-shell/
if [[ -d "$TARGET_DIR" ]] && ! git diff --quiet "$TARGET_DIR/" 2>/dev/null; then
    echo "⚠️  Uncommitted changes detected in $TARGET_DIR/"
    echo "Please commit your changes first:"
    echo "  git add $TARGET_DIR/"
    echo "  git commit -m 'Update socratic-shell patterns'"
    exit 1
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Get current and new commit hashes
old_hash=""
if [[ -f "$STAMP_FILE" ]]; then
    old_hash=$(cat "$STAMP_FILE")
fi

new_hash=$(curl -s "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/commits/main" | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['sha'])")

if [[ -z "$new_hash" ]]; then
    echo "❌ Failed to fetch latest commit hash from GitHub"
    exit 1
fi

echo "📋 Old version: ${old_hash:-'(none)'}"
echo "📋 New version: $new_hash"

if [[ "$old_hash" == "$new_hash" ]]; then
    echo "✅ Already up to date!"
    exit 0
fi

# Get list of .md files in src/prompts/project/
echo "🔍 Fetching file list from GitHub..."
file_list=$(curl -s "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/contents/src/prompts/project?ref=$new_hash" | \
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    files = [item['name'] for item in data if item['type'] == 'file' and item['name'].endswith('.md')]
    print('\n'.join(files))
except:
    exit(1)
")

if [[ -z "$file_list" ]]; then
    echo "❌ Failed to fetch file list from GitHub"
    exit 1
fi

echo "📁 Files to sync:"
echo "$file_list" | sed 's/^/  - /'

# Detect conflicts (compare current files with old upstream versions)
conflicts=()
if [[ -n "$old_hash" ]]; then
    echo "🔍 Checking for local modifications..."
    for file in $file_list; do
        local_file="$TARGET_DIR/$file"
        if [[ -f "$local_file" ]]; then
            # Get old upstream version and compare
            old_content=$(curl -s "https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$old_hash/src/prompts/project/$file" 2>/dev/null || echo "")
            if [[ -n "$old_content" ]] && ! echo "$old_content" | diff -q - "$local_file" >/dev/null 2>&1; then
                conflicts+=("$file")
            fi
        fi
    done
fi

# Download new versions
echo "⬇️  Downloading files..."
for file in $file_list; do
    echo "  - $file"
    curl -s "https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$new_hash/src/prompts/project/$file" > "$TARGET_DIR/$file"
done

# Handle deletions (remove files that no longer exist upstream)
echo "🗑️  Checking for deleted files..."
deleted_files=()
if [[ -d "$TARGET_DIR" ]]; then
    for local_file in "$TARGET_DIR"/*.md; do
        [[ -f "$local_file" ]] || continue  # Skip if no .md files exist
        filename=$(basename "$local_file")
        if [[ "$filename" != ".commit-stamp" ]] && ! echo "$file_list" | grep -q "^$filename$"; then
            echo "  - Removing deleted file: $filename"
            git rm "$local_file" 2>/dev/null || rm "$local_file"
            deleted_files+=("$filename")
        fi
    done
fi

# Create conflict files for review
if [[ ${#conflicts[@]} -gt 0 ]]; then
    echo "⚠️  Local modifications detected in ${#conflicts[@]} file(s):"
    for file in "${conflicts[@]}"; do
        echo "  - $file"
        # Create conflict files
        original_file="conflict-$file-original.md"
        modified_file="conflict-$file-modified.md"
        
        # Get original version (from old commit)
        curl -s "https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$old_hash/src/prompts/project/$file" > "$original_file"
        
        # Get the version that was modified (from git history or backup)
        if git show "HEAD:$TARGET_DIR/$file" >/dev/null 2>&1; then
            git show "HEAD:$TARGET_DIR/$file" > "$modified_file"
        else
            echo "# Could not retrieve modified version - file may be new" > "$modified_file"
        fi
    done
    echo ""
    echo "Conflict files created for review:"
    echo "  - conflict-*-original.md (old upstream version)"
    echo "  - conflict-*-modified.md (your modified version)"
    echo ""
    echo "Review the changes and 'rm conflict-*.md' when done."
fi

# Update commit stamp
echo "$new_hash" > "$STAMP_FILE"

# Summary
echo ""
echo "✅ Sync completed!"
echo "   Downloaded: $(echo "$file_list" | wc -l) files"
if [[ ${#deleted_files[@]} -gt 0 ]]; then
    echo "   Deleted: ${#deleted_files[@]} files"
fi
if [[ ${#conflicts[@]} -gt 0 ]]; then
    echo "   Conflicts: ${#conflicts[@]} files (see conflict-*.md)"
fi
echo ""
echo "Add to your project's CLAUDE.md:"
echo "  @.socratic-shell/README.md"