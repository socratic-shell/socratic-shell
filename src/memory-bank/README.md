# Memory Bank MCP Server

## Vision

A MCP tool to help Claude retain memories across sessions, both about project-specific details but also about user preferences. The system is modeled loosely on what we know of human memory. Memories are stored in git repositories allowing for full context tracking.

## Goals

The Socratic Shell Memory Bank addresses this by creating an intelligent memory system that:

- **Learns what matters** through natural collaboration patterns
- **Surfaces relevant context** at the right moments without interruption  
- **Evolves understanding** as new insights refine or contradict old ones
- **Scales gracefully** as collaboration history grows

## Success Criteria

We'll know the memory bank is working when:

1. **Context feels effortless** - relevant information appears naturally without explicit requests
2. **Collaboration accelerates** - we build on past insights rather than rediscovering them
3. **Knowledge compounds** - later sessions are more effective because of accumulated understanding
4. **System stays transparent** - memory operations enhance rather than complicate the collaboration flow

## System Overview

The memory bank operates through three core operations:

- **`consolidate`** - Store new insights when cognitive pressure builds or natural checkpoint moments occur
- **`read_in`** - Retrieve relevant context during confusion moments or when exploring new topics  
- **`store_back`** - Update existing memories as understanding evolves and deepens

These operations integrate seamlessly with existing collaboration patterns, using natural conversation signals (from CLAUDE.md) as triggers rather than requiring explicit memory management.

The system follows biological memory principles: frequent consolidation with natural decay, context-dependent retrieval, and intelligent forgetting that preserves signal while discarding noise.