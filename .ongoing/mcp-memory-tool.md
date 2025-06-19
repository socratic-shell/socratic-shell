# MCP Memory Banks Tool

**Status**: Planning phase - defining requirements and architecture
**Last Updated**: 2025-06-19

## Current Task
Building an MCP tool to store and retrieve memories about our collaboration, starting with writing style guidelines and expanding to project tracking.

## Context
- Evolved from idea of `/dev/nikos-brain/` → `/dev/claudes-brain/` → MCP Memory Banks
- Goal: Automatic, self-improving system where I learn and remember preferences over time
- Initial use case: Auto-detect writing requests and apply appropriate style guidelines

## Next Steps
1. ✅ Update CLAUDE.md with `.ongoing` process documentation (COMPLETE)
2. ✅ Add Pre-Work Hooks pattern to CLAUDE.md (COMPLETE)
3. Design minimal, flexible MCP tool interface (`store_memory`, `retrieve_memory`, `search_memories`)
4. Implement basic MCP server in socratic-shell repo
5. Test with writing guidelines use case
6. Expand to track ongoing tasks (eventually replacing manual `.ongoing` files)

## Key Decisions Made
- MCP tool approach chosen over file permissions/git access
- Building together (Niko handles MCP architecture, Claude handles memory patterns)
- Starting flexible and minimal rather than writing-specific
- Living in socratic-shell repo
- "Memory Banks" preferred over "Claude's Brain"

## Open Questions
- Exact MCP tool interface design
- Storage format (files vs structured data)
- Auto-update triggers and mechanisms
- Integration with existing Q chat workflow

## Resources
- MCP documentation for server implementation
- Existing CLAUDE.md patterns for collaboration
- Writing style guidelines as first test case
