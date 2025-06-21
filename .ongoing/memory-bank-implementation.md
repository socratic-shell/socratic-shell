# Socratic Shell Memory Bank

**Status**: Design phase complete - ready for MCP tool interface design
**Last Updated**: 2025-06-21

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

## Implementation Stack
- **Language**: Python with full type annotations
- **Dependency management**: `uv` for fast, reliable package management
- **Key libraries**: `rank-bm25`, `sentence-transformers`, `chromadb`/`faiss`
- **Data validation**: `pydantic` for fact schemas and metadata
- **Project structure**: `pyproject.toml` with modern Python best practices

## Key Research Findings

### Relevance Scoring Formula
```
Relevance = 0.3×Recency + 0.2×Frequency + 0.35×Importance + 0.15×Context_Similarity
```

### Two-Stage Retrieval Architecture
- **Stage 1**: Fast BM25-based candidate retrieval (top 50-100 facts)
- **Stage 2**: Semantic reranking with cross-encoders (top 10-15 results)

### Graph-Based Importance Scoring
- **PageRank implementation**: NetworkX library for centrality calculation
- **Co-occurrence patterns**: Facts retrieved together create edges
- **Temporal decay**: Connection strength decreases without reinforcement
- **Dynamic networks**: Adapts to current collaboration patterns

### Human Memory Architecture Validation
- **Declarative vs procedural**: Facts vs behavioral patterns need different storage
- **Working memory buffer**: Claude's context serves this role naturally
- **Multi-timescale consolidation**: Read-in/store-back lifecycle matches human memory
- **Context-aware retrieval**: Semantic + contextual + emotional salience

### Enhanced Behavioral Memory Format
- **Context**: "When we're doing X" (current activity/phase)
- **Internal State**: "and I feel Y" (emotional/cognitive state)
- **Response**: "then Z" (behavioral guidance)

## Next Steps
1. ✅ Research intelligent curation approaches for relevance scoring (COMPLETE)
2. **Design specific MCP tool interface** based on research findings
3. Implement two-stage retrieval architecture (BM25 + semantic reranking)
4. Implement Socratic Shell Memory Bank MCP server
5. Test with writing guidelines and collaboration patterns
6. Expand to replace manual `.ongoing` files

## Open Questions
- Context tracking implementation: How to detect and maintain "what are we doing" state
- Co-occurrence tracking: Optimal time windows and decay functions for connection strength
- Behavioral trigger detection: Recognizing internal states and context patterns in conversation
- Fact vs behavioral memory retrieval timing: When to surface each type proactively
- Connection threshold tuning: When do weak connections effectively disappear
- Consolidation automation: Detecting emoji patterns and extracting insights automatically
- Integration with existing collaboration workflow

## Key Decisions Made
- Content-addressable memory approach over structured storage
- Human memory phases model (working memory = context, consolidated storage only)
- RAG-based semantic search implementation
- CLAUDE.md patterns as consolidation triggers
- Dual focus: project insights + user observations
- Intelligent curation over simple staleness detection
- Goal: Surface relevant information, filter extraneous detail
- Name: "Socratic Shell Memory Bank"
- Two-stage retrieval architecture (BM25 + semantic reranking)
- Implementation: Python with `uv`, type annotations, and modern tooling

## Context
- Evolved from manual `.ongoing` files → automatic memory management
- Inspired by human memory phases and content-addressable storage
- RAG-based semantic search leverages existing solutions
- CLAUDE.md patterns become the "operating system" for memory consolidation
- Self-improving system where collaboration patterns get better through accumulated memory

## Resources
- Human memory research findings in `references/human-memory-architectural-insights.md`
- Relevance scoring analysis in `references/2025-06-19-designing-memory-banks.md`
- RAG/semantic search frameworks and implementation guides
- Existing CLAUDE.md patterns for consolidation logic