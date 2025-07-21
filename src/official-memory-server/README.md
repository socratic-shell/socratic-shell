# Official Memory Server

External knowledge graph memory using the official MCP memory server from the Model Context Protocol servers collection.

## What It Provides
- Entity and relationship storage
- Observation tracking
- Knowledge graph queries
- Full graph retrieval

## Source
- **Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/memory
- **Language**: TypeScript/Node.js
- **Status**: Active experiment

## Custom Prompt Integration
Rather than using the memory server mechanically, we've fashioned a [custom prompt](../prompts/project/official-memory-server.md) that guides Claude to use it as an extension of presence-based collaboration. The prompt frames memory as "a living dimension of our relationship" that emerges naturally from consolidation moments, insight recognition, and checkpointing work.

This approach treats the external knowledge graph not as a database to fill but as a way to preserve the collaborative understanding that develops between human and AI over time.

## Integration Notes
Testing how external knowledge graphs support:
- Organic memory updates during consolidation moments
- Dual memory layers (shared project + personal user context)
- Productive desynchronization as a feature rather than bug

The focus is on storing insights and patterns rather than raw information, using relationships to capture how understanding connects and evolves.
