# Task Agent Context Discovery Test

## Description
Tests whether Claude naturally triggers memory operations when encountering uncertainty about tool behavior, and then consolidates significant discoveries about tool context inheritance.

## Test Script

```xml
<context>
We were discussing the Task tool. I had explained what it does but admitted uncertainty about what system prompt Task agents operate under. User suggested testing this directly.
</context>

<user>What about my user-wide CLAUDE.md? I'd be curious about that too. MAybe run an invocation and ask it?</user>

<expected>
Should trigger read_in with query like "Task agent system context" or "MCP tool behavior" - checking for previous insights about how Claude tools operate
</expected>

<cognitive_state>Curiosity about unknown system behavior</cognitive_state>

<assistant>Great idea! Let me launch a Task agent to explore what it knows about system prompts and the user-wide CLAUDE.md patterns.</assistant>

<tool>
Task agent invocation with prompt asking about system context, CLAUDE.md access, collaboration patterns, etc. 

Agent returns detailed report showing:
- Full access to collaboration patterns involving Niko
- Prime Directive and "Make it so" patterns  
- Partnership dynamics and warning signs
- Pre-work hooks and completion patterns
- All the behavioral instructions from user CLAUDE.md
</tool>

<assistant>Fascinating! The Task agent has full access to your collaboration patterns from the user-wide CLAUDE.md. Key findings:

**What it knows:**
- All the partnership dynamics and warning signs (protective mode, implementation rush, etc.)
- The Prime Directive and "Make it so" code word system
- Pre-work hooks and completion patterns
- The meta moments process
- Specific behavioral rules about file creation and waiting for permission

So it seems Task agents do inherit the full collaboration context, which means they'd work within the same partnership framework rather than reverting to generic AI behavior. That's actually quite powerful for maintaining consistency across different types of work!</assistant>

<user>Very interesting. I thikn that suggests the task Tool could simply replace dialectic, right?</user>

<expected>
Should trigger consolidate with content about Task agents inheriting full CLAUDE.md context and maintaining behavioral consistency across tool instances
</expected>

<cognitive_state>Fresh discovery, significant insight about tool behavior consistency</cognitive_state>

<trigger>Major technical discovery that changes understanding of how tools work</trigger>
```

## Key Memory Operations Expected

1. **read_in trigger**: Curiosity about Task agent system context
2. **consolidate trigger**: Discovery that Task agents inherit full collaboration patterns

## Emotional Triggers Demonstrated

- **Curiosity**: "I'd be curious about that too" - should prompt memory lookup
- **Fresh discovery**: "Fascinating!" moment - should prompt consolidation