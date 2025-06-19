# Socratic Shell Memory Bank

**Status**: Design phase - refined architecture based on human memory model and intelligent curation
**Last Updated**: 2025-06-19

## Current Task
Building the Socratic Shell Memory Bank - an MCP tool for content-addressable memory storage and retrieval that provides the information most likely to be relevant to the user at the moment.

## Core Goal
**Intelligent context curation**: Scale gracefully as our collaborative knowledge base grows, naturally retaining important facts while discarding extraneous detail. The system should surface the right information at the right time, handling context accumulation in a way that enhances rather than overwhelms collaboration.

## Refined Architecture

### Memory Model
- **Content-addressable storage**: Facts stored with minimal structure, retrieved by semantic similarity (RAG approach)
- **Working memory = Native context**: No separate short-term storage - facts exist in conversation until consolidated
- **Memory Banks = Consolidated storage**: Long-term storage for proven useful facts
- **Memory lifecycle**: Active use → Consolidation → Read-in → Store-back → Intelligent curation

### Dual Memory Types
1. **Project insights**: Technical discoveries, decisions, patterns that worked
2. **User observations**: Niko's preferences, working style, context patterns

### CLAUDE.md Integration
- Emoji patterns (🔍, 🎯, 🤔) signal consolidation-worthy moments
- Warning signs become negative examples to store
- Meta moments are explicit consolidation triggers
- Communication preferences inform storage and retrieval patterns

### Core Operations
- **Consolidate**: Store facts from current context based on pattern recognition
- **Read-in**: Load relevant facts into context, update access metadata
- **Store-back**: Update fact content with new insights, refresh change metadata
- **Intelligent curation**: Surface most relevant facts while filtering noise

## Context
- Evolved from manual `.ongoing` files → automatic memory management
- Inspired by human memory phases and content-addressable storage
- RAG-based semantic search leverages existing solutions
- CLAUDE.md patterns become the "operating system" for memory consolidation
- Self-improving system where collaboration patterns get better through accumulated memory

## Next Steps
1. ✅ Update CLAUDE.md with `.ongoing` process documentation (COMPLETE)
2. ✅ Add Pre-Work Hooks and Implementation Rush warning patterns (COMPLETE)
3. ✅ Refine Memory Banks architecture based on human memory model (COMPLETE)
4. ✅ Research intelligent curation approaches for relevance scoring (IN PROGRESS)
5. Design specific MCP tool interface based on research findings
6. Implement Socratic Shell Memory Bank MCP server
7. Test with writing guidelines and collaboration patterns
8. Expand to replace manual `.ongoing` files

## Key Decisions Made
- Content-addressable memory approach over structured storage
- Human memory phases model (working memory = context, consolidated storage only)
- RAG-based semantic search implementation
- CLAUDE.md patterns as consolidation triggers
- Dual focus: project insights + user observations
- Intelligent curation over simple staleness detection
- Goal: Surface relevant information, filter extraneous detail
- Name: "Socratic Shell Memory Bank"

## Research Focus
Currently investigating approaches for intelligent information curation:
- Core principles for determining information relevance over time
- Signals that indicate lasting importance vs temporary detail
- Design decisions for relevance scoring in collaborative AI memory
- Metadata/tracking requirements for effective curation

## Open Questions
- Specific relevance scoring algorithms based on research findings
- Optimal metadata tracking for curation decisions
- Integration patterns with existing Q chat workflow
- Implementation approach for RAG-based semantic search

## Resources
- MCP documentation for server implementation
- Human memory research for lifecycle modeling
- RAG/semantic search frameworks and tools
- Existing CLAUDE.md patterns for consolidation logic
