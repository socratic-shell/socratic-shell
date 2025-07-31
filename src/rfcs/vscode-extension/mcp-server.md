# RFC: Socratic Shell MCP Server Implementation

## Problem Statement

How should the unified Socratic Shell MCP server be implemented to provide a clean interface to AI tools while orchestrating multiple backend services?

## Architecture Overview

The Socratic Shell MCP server acts as a router/orchestrator that:
1. Presents a unified MCP interface to AI tools
2. Routes requests to appropriate backend MCP servers
3. Manages lifecycle of backend processes
4. Aggregates and transforms responses as needed

## Technical Design

### Core Components

**MCP Protocol Handler**
- Implements MCP server protocol for AI tool communication
- Handles tool discovery, invocation, and response formatting
- Manages connection lifecycle and error handling

**Backend Server Manager**
- Spawns and manages backend MCP server processes
- Handles process lifecycle (start, restart, cleanup)
- Monitors health and handles failures
- Routes requests via stdin/stdout MCP communication

**Request Router**
- Maps incoming tool requests to appropriate backend servers
- Handles request transformation if needed
- Aggregates responses from multiple backends
- Implements request/response caching if beneficial

### Backend Server Integration

**Communication Protocol**
```
AI Tool ←→ Socratic Shell MCP Server ←→ Backend MCP Servers
         (MCP over stdio)              (MCP over stdin/stdout)
```

**Backend Server Lifecycle**
- **Lazy Start**: Backend servers started on first request to their tools
- **Keep Alive**: Servers remain running for session duration
- **Health Monitoring**: Periodic health checks, restart on failure
- **Graceful Shutdown**: Clean termination on main server exit

**Tool Namespace Design**
```
socratic_shell_memory_search     → hippo-standalone
socratic_shell_memory_record     → hippo-standalone
socratic_shell_review_create     → dialectic-server
socratic_shell_project_setup     → built-in Rust implementation
```

### Configuration Management

**Server Configuration**
```toml
[backends]
hippo = { binary = "hippo-standalone", args = ["--mcp-mode"] }
dialectic = { binary = "dialectic-server", args = [] }

[tools]
memory_search = "hippo"
memory_record = "hippo"
review_create = "dialectic"
project_setup = "builtin"
```

**Runtime Discovery**
- Scan available backend binaries on startup
- Register tools based on backend capabilities
- Handle missing backends gracefully (disable related tools)

### Hook System Integration

The same Rust binary serves dual purposes:

**MCP Server Mode**: `socratic-shell serve --config path/to/config.toml`
**Hook Mode**: `socratic-shell hook conversation-start --context path/to/context.json`

**Hook Implementation**
- Lightweight execution (no backend server startup)
- Direct implementation of common hook operations
- Can invoke backend servers synchronously if needed
- Fast execution to avoid blocking AI tool interaction

### Error Handling Strategy

**Backend Server Failures**
- Automatic restart with exponential backoff
- Fallback to "service unavailable" responses
- Logging and diagnostics for troubleshooting
- Graceful degradation (disable failed backend tools)

**Request Failures**
- Timeout handling for backend requests
- Proper MCP error response formatting
- Request retry logic for transient failures
- Circuit breaker pattern for persistent failures

### Performance Considerations

**Resource Management**
- Limit concurrent backend processes
- Memory usage monitoring and limits
- Request queuing and rate limiting
- Efficient process communication (avoid JSON parsing overhead where possible)

**Caching Strategy**
- Cache backend server capabilities on startup
- Optional response caching for expensive operations
- Configuration caching to avoid repeated file reads

## Implementation Details

### Rust Dependencies
```toml
[dependencies]
tokio = { version = "1.0", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
clap = { version = "4.0", features = ["derive"] }
tracing = "0.1"
tracing-subscriber = "0.3"
```

### Key Modules
- `mcp/` - MCP protocol implementation
- `backends/` - Backend server management
- `routing/` - Request routing and aggregation
- `hooks/` - Hook system implementation
- `config/` - Configuration management

### Build and Distribution
- Cross-compilation targets: `windows-x64`, `darwin-x64`, `darwin-arm64`, `linux-x64`
- Static linking where possible to minimize dependencies
- Embedded default configuration
- Version information for compatibility checking

## Open Questions

1. **Backend Server Discovery**: Should we auto-discover backend capabilities or use static configuration?
2. **Request Transformation**: Do we need to transform requests/responses between main server and backends?
3. **Concurrent Requests**: How do we handle multiple simultaneous requests to the same backend?
4. **State Management**: Do we need to maintain any persistent state across requests?
5. **Debugging Support**: What debugging/introspection tools should we provide?

## Success Criteria

- Single MCP connection provides access to all Socratic Shell tools
- Backend server failures don't crash the main server
- Hook execution completes in <100ms for responsive AI tool interaction
- Memory usage remains reasonable with multiple backend servers
- Easy to add new backend servers without changing core routing logic

## Future Enhancements

- **Plugin System**: Dynamic loading of backend servers
- **Remote Backends**: Support for network-based backend servers
- **Request Analytics**: Metrics and monitoring for tool usage
- **Configuration UI**: VSCode extension interface for server configuration
