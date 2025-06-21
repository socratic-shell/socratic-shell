# Dialectic: Collaboration Pattern Testing Tool

**Status**: STALLED - waiting for MCP sampling support in Claude Code
**Last Updated**: 2025-06-21

## Current Task
Building the Dialectic MCP server for systematic testing of collaboration patterns through structured conversation scenarios.

## Core Goal
**Pattern validation through controlled testing**: Enable rapid iteration on collaboration patterns by spawning fresh Claude instances with custom system prompts and testing scenarios. Provides structured feedback on pattern recognition and effectiveness without contaminating the main conversation thread.

## Architecture

### MCP Server Implementation
- **Language**: Python with full type annotations
- **Dependency management**: `uv` for fast, reliable package management  
- **Async architecture**: Parallel sampling of multiple scenarios
- **Type safety**: Pydantic models with strict validation
- **MCP integration**: Proper server registration with auxiliary type comments

### Core Operations
- **test_pattern**: Takes base context + pattern description + test scenarios
- **Parallel sampling**: Execute multiple conversation scenarios simultaneously
- **Structured results**: Return responses with metadata for systematic analysis
- **Pattern iteration**: Enable rapid refinement based on fresh Claude responses

## Implementation Status

### ✅ Complete
- Full MCP server implementation with proper typing
- Pydantic models for request/response validation
- Async parallel sampling architecture
- Server registration and command-line entry point
- Integration with Claude Code MCP system

### ❌ Blocked: MCP Sampling Not Available
- Claude Code doesn't yet support server-initiated sampling requests
- Server returns placeholder responses instead of actual Claude generations
- Core functionality requires MCP sampling capabilities to work

## Workaround Discovered

### claude --print Method
- **Approach**: Create custom CLAUDE.md files in temporary directories
- **Process**: Write test conversations, use `claude --print < conversation.txt`
- **Benefits**: Immediate feedback, systematic pattern testing
- **Limitations**: Less control over system prompts, no batch processing

### Validation Results
Tested Completion Hook pattern with three scenarios:
1. **Clear completion signal**: "we can figure that out as we go" → Triggered checkpoint suggestion
2. **Ambiguous signal**: "That's very interesting" → Less certain checkpoint offer  
3. **No transition signal**: Direct topic question → No checkpoint suggestion

## Next Steps

### When MCP Sampling Becomes Available
1. Test full dialectic functionality with real Claude responses
2. Implement batch pattern testing workflows
3. Add system prompt variation testing
4. Create pattern effectiveness scoring metrics

### Current Alternative Approach
1. Continue using `claude --print` for immediate pattern validation
2. Build library of test scenarios for key collaboration patterns
3. Document pattern recognition accuracy across different phrasings
4. Prepare for easy migration when sampling support arrives

## Key Insights

**Pattern testing is valuable**: Even with the workaround, systematic testing reveals pattern recognition accuracy and helps refine trigger phrases.

**Fresh context matters**: Testing with clean Claude instances (no conversation history) shows how patterns work for new collaborations.

**Signal clarity varies**: Explicit transition phrases work better than implicit ones for pattern recognition.

## Resources
- MCP sampling specification and documentation
- Claude Code MCP integration guides
- Pattern testing methodologies and best practices