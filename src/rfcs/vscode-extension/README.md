# RFC: Socratic Shell VSCode Extension for Centralized Installation and Configuration

> **Tracking Issue**: [#16 - Implement unified Socratic Shell installation and MCP server](https://github.com/socratic-shell/socratic-shell/issues/16)

## Problem Statement

Socratic Shell currently exists as a collection of separate tools and documentation patterns that require manual setup and configuration. Users must:
- Manually install and configure multiple MCP servers (hippo, dialectic)
- Set up context injection for their AI tools
- Configure hooks and integrations
- Understand complex multi-tool interactions

This creates a high barrier to entry and limits adoption.

## Goals

Transform Socratic Shell from a collection of tools into a cohesive collaborative AI environment that "just works out of the box" through:

1. **Single Installation Point**: VSCode extension as the primary distribution mechanism
2. **Unified MCP Interface**: One MCP server that orchestrates all Socratic Shell capabilities
3. **Guided Setup**: UI-driven configuration that adapts to user's AI tool (Claude Code, Q CLI)
4. **Complete Integration**: Automatic context injection, hook setup, and lifecycle management

## High-Level Architecture

### Components

**VSCode Extension (Control Plane)**
- Installation orchestration and UI guidance
- Lifecycle management of background services
- Platform detection and binary selection
- Configuration management

**Socratic Shell MCP Server (Rust Binary)**
- Unified MCP interface for AI tools
- Request routing to backend services
- Process management for backend MCP servers
- Hook execution (conversation-start, per-prompt)

**Backend MCP Servers**
- `hippo-standalone` (Python executable) - memory operations
- `dialectic-server` (TypeScript bundle) - code review and file operations
- Future components as separate MCP servers

### Distribution Strategy

**Multi-Binary Bundling**
```
socratic-shell-extension/
├── binaries/
│   ├── windows-x64/
│   ├── darwin-x64/
│   ├── darwin-arm64/
│   └── linux-x64/
├── dialectic/ (TypeScript bundle)
└── extension.js
```

**Installation Flow**
1. User installs VSCode extension from marketplace
2. Extension detects platform and AI tool configuration
3. UI guides user through setup choices
4. Extension configures MCP connections and hooks
5. Background services start automatically

## Key Design Decisions

### Why VSCode Extension as Primary Distribution?
- Single install point with cross-platform support
- Built-in UI capabilities for guided setup
- Natural integration with dialectic (already VSCode-focused)
- Handles binary distribution and lifecycle management

### Why Rust for Main MCP Server?
- Single static binary (easy bundling)
- Minimal resource overhead for orchestration
- Excellent process management and IPC capabilities
- Good cross-platform support

### Why Multi-Binary vs Universal Binary?
- Proven Rust cross-compilation toolchain
- Avoids experimental dependencies (cosmopolitan)
- Predictable behavior across platforms
- Standard CI/CD pipeline support

### Why Bundle All Binaries Initially?
- Simplest installation experience ("just works offline")
- Eliminates network dependency failures
- Can optimize with lazy download later if size becomes issue

## Implementation Phases

### Phase 1: Core Infrastructure
- Rust MCP server with basic routing
- VSCode extension with platform detection
- Multi-platform build pipeline
- Basic backend server integration (hippo, dialectic)

### Phase 2: Installation Experience
- Guided setup UI in VSCode extension
- AI tool detection and configuration
- Context injection mechanisms
- Hook system integration

### Phase 3: Enhanced Features
- Canned prompts/tools for common operations
- Project-specific setup automation
- Advanced lifecycle management
- Performance optimizations

## Open Questions

1. **Hook Integration Points**: Where exactly do we plug into Claude Code vs Q CLI lifecycle events?
2. **Context Injection Mechanics**: How do we reliably inject prompts into different AI tool contexts?
3. **Backend Server Lifecycle**: Start/stop on demand vs keep-alive strategies?
4. **Configuration Management**: How do we handle updates and version compatibility?
5. **Error Handling**: How do we provide good diagnostics when components fail?

## Success Criteria

- New user can install and use Socratic Shell in under 5 minutes
- Single VSCode extension provides complete Socratic Shell experience
- Works reliably across Windows, macOS, and Linux
- Extensible architecture supports future Socratic Shell components
- Maintains performance characteristics of individual tools

## Related RFCs

- [MCP Server Implementation Details](./mcp-server.md)
- [Hook System Design](./hooks.md)
- [Repository Coordination and Multi-Language Bundling](./repo-coordination.md)
