# Repository Configuration Restructure Plan

**Status**: Planning  
**Started**: 2025-06-29  
**Goal**: Organize the socratic-shell repository to better separate its three current functions

## Current State

This repository currently serves three purposes:
1. **Global CLAUDE configuration**: Home for shared CLAUDE.md that gets symlinked to `~/.claude/CLAUDE.md`
2. **Collaboration playground**: Experimental ideas and patterns for human-AI collaboration  
3. **Socratic shell memory bank**: Specific implementation of memory/collaboration tools

The playground (#2) and memory bank project (#3) are essentially the same category - experimental collaboration work.

## Proposed Structure

### New Directory Layout
```
prompts/
├── user/          # Personal patterns for individual ~/.claude/CLAUDE.md inclusion
└── project/       # Team patterns for project-specific .socratic-shell/ directories
```

### Distribution Mechanism

**For Personal Use** (`prompts/user/`):
- Users manually reference files in their personal `~/.claude/CLAUDE.md` 
- Import syntax: `@prompts/user/collaboration-patterns.md`
- Users control which patterns they adopt

**For Project Use** (`prompts/project/`):
- Zero-install sync via `curl | bash` script
- Script downloads patterns to project's `.socratic-shell/` directory
- Team imports via `@.socratic-shell/patterns.md` in project CLAUDE.md
- Committed to git so whole team shares same patterns

### Sync Script Behavior

**File Discovery**:
- Use GitHub API to get directory listing of `prompts/project/`
- Auto-discover .md files (no hardcoded list)

**Conflict Handling**:
1. Check for uncommitted changes in `.socratic-shell/` (warn and exit if found)
2. Store commit hash in `.socratic-shell/.commit-stamp` 
3. Compare current files with old upstream versions to detect local modifications
4. Always overwrite files with new upstream versions
5. Create `conflict-{filename}-original.md` and `conflict-{filename}-modified.md` for review
6. Handle deletions: `git rm` files that no longer exist upstream

**Script URL**: `curl https://raw.githubusercontent.com/nikomatsakis/socratic-shell/main/install.sh | bash`

## Benefits

- **Clear separation**: Global vs project-specific patterns
- **Independent adoption**: Projects can use socratic-shell patterns without requiring users to change personal setup
- **Resilient**: Projects retain working copy even if socratic-shell disappears
- **Version controlled**: Teams can see when patterns change
- **Simple**: "Poor man's git submodule" without complexity

## Implementation Steps

1. Create `prompts/user/` and `prompts/project/` directories
2. Move current CLAUDE.md content appropriately
3. Create install script with conflict detection
4. Update repository README to explain new structure
5. Test script with a sample project

## Questions/Decisions

- Which current patterns belong in `user/` vs `project/`?
- What should be the initial set of files in each directory?
- Should script prompt before overwriting existing backup directories?