# Journal MCP Server

A memory system that emerges from collaborative understanding, reimagining AI memory as an organic, reflective practice rather than mechanical storage.

## Phase 1: JSON Prototype ✅

The JSON prototype is now complete with all core functionality:

- **5 MCP Tools**: `journal_read`, `journal_write`, `journal_search`, `journal_toc`, `journal_list_entries`
- **Dual-dimension search**: Work context + content matching with temporal salience
- **Configurable storage**: `--data-file` argument for custom JSON locations
- **Full type checking**: mypy compliance with comprehensive test coverage

## Quick Start

### Installation

```bash
# Install in development mode
uv pip install -e .

# Run with default data file (./journal.json)
uv run journal-server

# Run with custom data file
uv run journal-server --data-file ~/my-journal.json
```

### Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run type checking
uv run mypy src/journal_server/ --ignore-missing-imports
```

## MCP Tools

### journal_write
Add entries and optionally update section overviews:
```json
{
  "path": "project-alpha",
  "entry": "Implemented user authentication with JWT tokens",
  "work_context": "authentication development",
  "overview": "Building secure user management system"
}
```

### journal_read
Read section overviews and recent entries:
```json
{
  "path": "project-alpha",
  "include_entries": true,
  "max_entries": 5
}
```

### journal_search
Semantic search with dual-dimension matching:
```json
{
  "work_context": "authentication development",
  "content": "JWT tokens",
  "salience_threshold": 0.5
}
```

### journal_toc
Navigate journal structure:
```json
{
  "max_depth": 3
}
```

### journal_list_entries
Browse entries with pagination:
```json
{
  "path": "project-alpha",
  "limit": 10,
  "offset": 0
}
```

## Architecture

**Core concept**: Git-centric design where journal sections are markdown files with current understanding as file contents and incremental entries stored as git commit messages.

**Current implementation**: JSON prototype that validates the interface before migrating to git backend.

**Tree structure**: Hierarchical organization with overviews (current synthesis), entries (chronological journey), and subsections that emerge naturally.

## Documentation

For the full concept, design, and architecture details, see the [mdBook documentation](../src/journal-mcp-server/).

## Development Status

Track implementation progress in [GitHub issue #9](https://github.com/socratic-shell/socratic-shell/issues/9).

**Phase 1 Complete**: JSON prototype with all 5 MCP tools working  
**Next**: Phase 2 interface refinement and real-world testing
