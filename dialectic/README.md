# Dialectic: MCP Pattern Testing Server

An MCP server for testing collaboration patterns through structured conversation scenarios and sampling.

## Project Architecture

### Core Purpose
Test collaboration patterns (like the Insight Completion Hook) by:
1. Providing base conversation context
2. Testing multiple transition scenarios
3. Sampling Claude responses in parallel
4. Returning structured results for human evaluation

### Design Decisions

**Language & Tooling:**
- Python 3.11+ with full type annotations
- `uv` for dependency management (not pip/conda)
- `mypy` in strict mode for maximum type safety
- `ruff` for linting and code formatting
- Pydantic for data validation and serialization

**MCP Integration:**
- Uses MCP sampling API for generating responses
- Server provides `test_pattern` tool for pattern testing
- Handles untyped MCP decorators with auxiliary type comments
- Async architecture with parallel sampling for performance

**Type Safety Approach:**
```python
# MCP decorator typing: Decorator[[], Callable[[], Awaitable[list[Tool]]]]
@self.server.list_tools()  # type: ignore[misc, no-untyped-call]
async def handle_list_tools() -> list[Tool]:
```
- Document expected types in comments
- Use targeted type ignores for external library limitations
- Maintain full type annotations on our code

## Key Components

### Data Models (`models.py`)
- **`PatternTest`**: Input structure with context, instruction, and test scenarios
- **`SamplingResult`**: Individual test result with metadata
- **`TestResults`**: Complete test results with summary statistics
- **`SamplingConfig`**: Configurable sampling parameters

### Sampling Engine (`sampling.py`)
- Handles MCP sampling operations
- Parallel execution of multiple test scenarios
- Token counting and response time tracking
- Prompt construction and response parsing

### MCP Server (`server.py`)
- Registers `test_pattern` tool with JSON schema validation
- Handles stdio transport for MCP communication
- Proper server capabilities configuration

## Usage Pattern

```python
# Test the Insight Completion Hook pattern
test_input = {
    "base_context": "We've been discussing Memory Banks architecture...",
    "pattern_instruction": "Consolidate when you see explicit closure + transition signals...",
    "test_scenarios": [
        "Good point, we can figure that out as we go. Let's talk about implementation.",
        "That's very interesting. Let's talk about implementation."
    ]
}

# Returns structured results for human evaluation
results = await dialectic.test_pattern(**test_input)
```

## Development Workflow

**Setup:**
```bash
cd dialectic
uv sync  # Install all dependencies
```

**Type Checking:**
```bash
uv run mypy src/dialectic/  # Must pass without errors
```

**Testing:**
```bash
uv run pytest  # When tests are added
```

## Future Enhancements

1. **Pattern Library**: Build reusable test scenarios for common patterns
2. **Automated Evaluation**: Add second-stage sampling for automated response scoring
3. **Performance Optimization**: Implement connection pooling for high-volume testing
4. **Integration**: Connect with Memory Banks system for pattern refinement cycles

## Context for Future Claude

This server emerged from discovering that collaboration patterns (like when to consolidate insights) needed systematic testing. The "dialectic" name reflects the process of testing opposing approaches to find synthesis.

The key insight: Instead of guessing whether patterns work, we can test them empirically using fresh Claude contexts via MCP sampling, then evaluate the results systematically.

This tool enables rapid iteration on collaboration patterns without contaminating our main conversation context.