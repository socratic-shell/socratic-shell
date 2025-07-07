# Dialectic Testing Tool

Dialectic is a YAML-based test runner for validating collaboration patterns and prompt engineering approaches.

## Purpose

Test whether prompts produce expected behaviors by running conversation scenarios and validating:
- Response content (what Claude says)
- Tool usage (what Claude does)
- Behavioral patterns (how Claude responds)

## Usage

```bash
cd dialectic
uv run python dialectic.py test-scripts/my-test.yaml
```

## Test Format

```yaml
name: "Test Name"
description: "What this test validates"

conversation:
  - user: "User message"
    expected_response:
      should_contain: ["expected", "phrases"]
      should_not_contain: ["forbidden", "phrases"]
    expected_tools: []  # Empty = no tools should be called
```

## Key Features

- **Fail-fast execution** - stops on first failure to avoid testing invalid conversation states
- **Streaming output** - shows responses in real-time for debugging
- **Tool parameter validation** - verifies correct parameters passed to tools
- **Human-readable format** - easy to write and understand test cases

## Current Status

Working prototype using Claude Code SDK. Useful for testing prompt patterns before deploying them.

## Development

- Uses `uv` for dependency management
- Fully typed with mypy type annotations
- Run type checking: `uv run mypy src/`