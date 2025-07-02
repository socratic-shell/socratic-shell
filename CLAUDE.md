# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@prompts/project/ongoing-work-tracking.md
@prompts/project/ai-insights.md

## Project Overview

Socratic Shell is a research experiment in deliberate AI-human collaboration design. It consists of two main MCP (Model Context Protocol) servers that enable structured collaboration patterns and pattern testing.

### Core Components

1. **socratic-shell** - Memory consolidation MCP server for intelligent information storage and retrieval
2. **dialectic** - Pattern testing MCP server for evaluating collaboration approaches through structured conversation scenarios

## Architecture

```
socratic-shell/
├── socratic-shell/          # Main MCP server for memory operations
│   └── src/socratic_shell/
│       ├── server.py        # MCP server with consolidate/read_in/store_back tools
│       └── models.py        # Pydantic models for memory operations
├── dialectic/               # Pattern testing MCP server
│   └── src/dialectic/
│       ├── server.py        # MCP server with test_pattern tool
│       ├── models.py        # Data models for pattern testing
│       └── sampling.py      # Core sampling logic (placeholder)
├── prompts/                 # User and project patterns
├── insights/                # Research findings on collaboration
├── work-tracking/           # Documentation on tracking approaches
└── references/              # Research materials and background
```

## Common Development Commands

### Running the Servers

**Socratic Shell server:**
```bash
cd socratic-shell
uv sync --quiet
uv run python -m socratic_shell
```

**Dialectic server:**
```bash
./run-dialectic.sh
# OR
cd dialectic
uv sync --quiet
uv run python -m dialectic
```

### Testing and Code Quality

**Run tests:**
```bash
cd dialectic  # or socratic-shell
uv run pytest
```

**Linting and type checking:**
```bash
cd dialectic  # or socratic-shell
uv run ruff check .
uv run mypy src/
```

**Install development dependencies:**
```bash
cd dialectic  # or socratic-shell  
uv sync  # Installs dev dependencies from pyproject.toml
```

## MCP Server Tools

### Socratic Shell Tools
- `consolidate` - Store insights/patterns with category and importance
- `read_in` - Retrieve relevant memories based on query/context
- `store_back` - Update existing memories with new insights

### Dialectic Tools
- `test_pattern` - Test collaboration patterns with multiple scenarios (currently returns placeholder results)

## Work Tracking

This repository uses the **ongoing files** approach for work tracking:

- Create `.ongoing/task-name.md` files for active development work
- Update status, next steps, and context as work progresses  
- Delete files when work is complete
- See `work-tracking/ongoing-files.md` for detailed conventions

**Check current work:**
```bash
ls -la .ongoing/ 2>/dev/null || echo "No ongoing work tracked"
grep -h "^## Status:" .ongoing/*.md 2>/dev/null || echo "No status found"
```

## Key Development Patterns

### Python Environment
- Both servers use **uv** for dependency management
- Python 3.11+ required
- Pydantic for data models
- MCP framework for server implementations

### Code Organization
- Each server is self-contained in its own directory
- Shared patterns documented in `prompts/` and `insights/`
- Clear separation between MCP protocol handling and business logic

### Testing Strategy
- `dialectic/` has placeholder MCP sampling capabilities (future: actual Claude API integration)
- Test fixtures in `test/fixtures/` for system prompts and reminders
- Pattern testing designed around real conversation scenarios

## Important Files

- `run-dialectic.sh` - Quick start script for dialectic server
- `prompts/user/main.md` - Core collaboration patterns (referenced by global CLAUDE.md)
- `insights/*.md` - Research findings on effective AI-human collaboration
- `work-tracking/*.md` - Documentation on different tracking approaches

## Notes

- The `socratic-shell` server currently has dummy memory implementation
- The `dialectic` server returns placeholder results until MCP sampling is fully implemented  
- Both servers log operations to stderr for debugging
- This is research code - focus on collaboration patterns over production polish