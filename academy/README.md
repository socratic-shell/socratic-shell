# Academy: Memory Bank Experimentation Workspace

**The Academy is where we develop and refine the socratic-shell memory bank.**

## Purpose

This directory serves as an isolated experimental workspace for developing intelligent memory consolidation and retrieval patterns. It allows us to iterate on memory bank functionality without disrupting established collaboration workflows.

## What's Different Here

- **Extended CLAUDE.md**: Includes experimental memory consolidation patterns and prompting guidance
- **Local MCP Configuration**: Socratic-shell memory bank server configured to work only in this directory
- **Experimental Safety**: Changes stay contained until we're ready to merge them back

## Memory Bank Development Focus

We're experimenting with:
- **Consolidation triggers**: When Claude should store important insights
- **Content classification**: What's safe to remember vs. what should stay ephemeral  
- **Retrieval patterns**: When and how Claude should surface relevant memories
- **Conversation flow**: Natural integration of memory operations into dialogue

## Working Method

1. **Develop in Academy**: All memory bank experimentation happens here
2. **Test patterns**: Real conversations using the memory bank tools
3. **Refine prompting**: Iterate on when/how memory operations get triggered
4. **Document learnings**: Capture what works and what doesn't
5. **Graduate to main**: Once stable, merge successful patterns back to the main CLAUDE.md

## Technical Setup

- **MCP Server**: `../socratic-shell/` - minimal logging-only implementation for testing
- **Configuration**: Local MCP config in `.claude_code_mcp_config.json`
- **Isolation**: Working here doesn't affect other directories or projects

---

*The Academy: Where collaboration patterns are born and refined.*