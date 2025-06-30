# Socratic Shell Patterns - Quick Setup Guide

## For Personal Use

**Install from checkout**:
```bash
cd /path/to/socratic-shell
./prompts/user/install.sh
```

This adds to your `~/.claude/CLAUDE.md`:
```markdown
# Socratic Shell Collaboration Patterns
@/path/to/socratic-shell/prompts/user/main.md
```

## For Project Teams

**Install patterns to project**:
```bash
curl https://raw.githubusercontent.com/nikomatsakis/socratic-shell/main/prompts/project/install.sh | bash
```

**Add to project's CLAUDE.md**:
```markdown
# Team Collaboration Patterns
@.socratic-shell/ongoing-work-tracking.md
@.socratic-shell/github-tracking-issues.md
```

## What You Get

**User patterns** (personal choice):
- Core collaboration patterns (Prime Directive, warning signs, hooks)
- Boot procedure and meta moments
- Partnership dynamics

**Project patterns** (team shared):
- `.ongoing/` file conventions for tracking work
- GitHub tracking issues workflow
- Checkpoint and work preservation patterns

## Ongoing Work Tracking Options

Choose what fits your project:

**Option 1: .ongoing/ files**
- Local markdown files in repo
- Good for: solo work, private repos, file-based workflows

**Option 2: GitHub tracking issues**  
- GitHub issues with `tracking-issue` label
- Good for: team collaboration, public repos, existing GitHub workflows

**Option 3: Both**
- Use `.ongoing/` for active work, GitHub issues for larger features
- Reference between them as needed