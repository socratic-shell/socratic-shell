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

## Entity Design Guidelines

The official memory server uses keyword-based searching. By default, Claude was simply glomming all the memories onto a single entity that represented the user. The prompt therefore includes guidance meant to improve memory retrieval by focusing memories on a small set of entities, and recognizing that all the memories in the file are always "relative" to the current user anyhow.