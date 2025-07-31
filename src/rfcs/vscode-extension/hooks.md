# RFC: Socratic Shell Hook System Design

## Problem Statement

How should Socratic Shell integrate with AI tool lifecycle events to provide seamless collaborative experiences without disrupting user interaction flow?

## Hook Types and Integration Points

### Conversation Start Hook
**Trigger**: Beginning of new AI conversation session
**Purpose**: Set collaborative context and inject relevant project information

**Claude Code Integration**
- Configured via `.claude/claude_desktop_config.json`
- Executed before first user message processed
- Can inject system context or initial assistant message

**Q CLI Integration** 
- Configured via MCP server settings or CLI flags
- Executed on `q chat` session initialization
- Context injection via initial system prompt

**Implementation**
```bash
socratic-shell hook conversation-start \
  --project-path /path/to/current/project \
  --ai-tool claude-code \
  --output-format context-injection
```

### Per-Prompt Hook
**Trigger**: Before/after each user prompt processing
**Purpose**: Contextual memory updates and session state management

**Use Cases**
- Record insights during natural consolidation moments
- Update project state based on conversation content
- Inject relevant historical context for current topic

**Implementation**
```bash
socratic-shell hook per-prompt \
  --phase before|after \
  --prompt-content "user message content" \
  --conversation-id session-123 \
  --project-path /path/to/project
```

## Hook Implementation Strategy

### Execution Model
**Synchronous Execution**: Hooks run in AI tool's critical path
- Must complete quickly (<100ms target)
- Failure should not block user interaction
- Minimal resource usage

**Lightweight Operations**
- File system checks and simple context injection
- Quick database lookups for relevant insights
- Avoid expensive operations (network calls, heavy computation)

### Context Injection Mechanisms

**Claude Code Context Injection**
```json
{
  "context_files": [
    "/path/to/project/CLAUDE.md",
    "/tmp/socratic-shell-session-context.md"
  ],
  "system_prompt_additions": [
    "You are working in project: MyProject",
    "Recent insights: [generated from memory]"
  ]
}
```

**Q CLI Context Injection**
```bash
# Via MCP server context
socratic-shell serve --inject-context /tmp/session-context.md

# Via CLI arguments
q chat --context-file /tmp/socratic-shell-context.md
```

### Hook Configuration

**Per-Project Configuration**
```toml
# .socratic-shell/config.toml
[hooks]
conversation_start = true
per_prompt = false

[context]
include_recent_insights = true
include_project_status = true
max_context_age_days = 7

[ai_tools]
claude_code = { enabled = true, config_path = ".claude/claude_desktop_config.json" }
q_cli = { enabled = true, mcp_config = true }
```

**Global Configuration**
```toml
# ~/.socratic-shell/global-config.toml
[defaults]
conversation_start_timeout_ms = 100
per_prompt_timeout_ms = 50
max_context_size_kb = 10

[logging]
hook_execution = true
performance_metrics = true
```

## Specific Hook Implementations

### Conversation Start Hook Logic

```rust
pub async fn conversation_start_hook(args: ConversationStartArgs) -> Result<HookOutput> {
    let project_context = detect_project_context(&args.project_path)?;
    let recent_insights = query_recent_insights(&project_context, Duration::days(7))?;
    let collaboration_patterns = load_collaboration_patterns()?;
    
    let context = ContextInjection {
        project_info: project_context,
        recent_insights: recent_insights.into_iter().take(5).collect(),
        collaboration_prompt: collaboration_patterns,
        session_id: generate_session_id(),
    };
    
    Ok(HookOutput::ContextInjection(context))
}
```

### Per-Prompt Hook Logic

```rust
pub async fn per_prompt_hook(args: PerPromptArgs) -> Result<HookOutput> {
    match args.phase {
        Phase::Before => {
            // Inject relevant context for current prompt
            let relevant_insights = search_relevant_insights(&args.prompt_content)?;
            Ok(HookOutput::ContextAddition(relevant_insights))
        }
        Phase::After => {
            // Record insights if this looks like a consolidation moment
            if is_consolidation_moment(&args.prompt_content) {
                record_session_insights(&args.conversation_id, &args.project_path)?;
            }
            Ok(HookOutput::None)
        }
    }
}
```

## AI Tool Integration Details

### Claude Code Integration
**Configuration Location**: `.claude/claude_desktop_config.json`
```json
{
  "mcpServers": {
    "socratic-shell": {
      "command": "/path/to/socratic-shell",
      "args": ["serve", "--config", ".socratic-shell/config.toml"],
      "hooks": {
        "conversation_start": {
          "command": "/path/to/socratic-shell",
          "args": ["hook", "conversation-start", "--project-path", "${PWD}"]
        }
      }
    }
  }
}
```

### Q CLI Integration
**MCP Server Configuration**: Automatic via MCP server registration
**Hook Configuration**: Via Q CLI configuration or MCP server settings

```bash
# Q CLI with MCP server that handles hooks internally
q chat --mcp-server socratic-shell
```

## Error Handling and Fallbacks

### Hook Failure Scenarios
1. **Timeout**: Hook execution exceeds time limit
2. **Process Failure**: Hook process crashes or returns error
3. **Resource Unavailable**: Required files or services not accessible

### Fallback Strategy
```rust
pub async fn execute_hook_with_fallback(hook: Hook, timeout: Duration) -> HookResult {
    match tokio::time::timeout(timeout, hook.execute()).await {
        Ok(Ok(result)) => HookResult::Success(result),
        Ok(Err(error)) => {
            log::warn!("Hook failed: {}", error);
            HookResult::Failed(error)
        }
        Err(_timeout) => {
            log::warn!("Hook timed out after {:?}", timeout);
            HookResult::TimedOut
        }
    }
}
```

### Graceful Degradation
- Hook failures should not prevent AI tool operation
- Log failures for debugging but continue normal operation
- Provide user notification for persistent hook failures
- Allow disabling problematic hooks via configuration

## Performance Considerations

### Optimization Strategies
- **Caching**: Cache expensive lookups (project detection, insight queries)
- **Lazy Loading**: Only load resources when actually needed
- **Parallel Execution**: Run independent hook operations concurrently
- **Resource Limits**: Prevent hooks from consuming excessive resources

### Monitoring and Metrics
```rust
struct HookMetrics {
    execution_time: Duration,
    memory_usage: usize,
    success_rate: f64,
    timeout_rate: f64,
}
```

## Open Questions

1. **Hook Discovery**: How do we detect which AI tool is being used?
2. **Context Size Limits**: What are reasonable limits for injected context?
3. **Hook Ordering**: If multiple hooks are configured, what's the execution order?
4. **State Persistence**: Should hooks maintain state between executions?
5. **User Control**: How much control should users have over hook behavior?

## Success Criteria

- Hooks execute reliably without blocking user interaction
- Context injection improves collaboration quality
- Hook failures don't disrupt AI tool operation
- Easy to configure and customize per project
- Performance impact is negligible (<5% overhead)

## Future Enhancements

- **Custom Hooks**: User-defined hook scripts
- **Hook Marketplace**: Shared hook configurations
- **Advanced Context**: Semantic context injection based on conversation analysis
- **Multi-Tool Sync**: Coordinate context across multiple AI tools
