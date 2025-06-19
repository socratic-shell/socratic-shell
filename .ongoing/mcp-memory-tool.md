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
4. ✅ Research intelligent curation approaches for relevance scoring (COMPLETE)
5. Design specific MCP tool interface based on research findings
6. Implement two-stage retrieval architecture (BM25 + semantic reranking)
7. Implement Socratic Shell Memory Bank MCP server
8. Test with writing guidelines and collaboration patterns
9. Expand to replace manual `.ongoing` files

## Key Research Findings
Based on analysis in `references/2025-06-19-designing-memory-banks.md`:

**Multi-layered relevance model**: Different knowledge types need different decay patterns
- Technical specifics: rapid exponential decay
- Conceptual insights: hyperbolic decay (matches human memory patterns)

**Optimal relevance scoring formula**:
```
Relevance = 0.3×Recency + 0.2×Frequency + 0.35×Importance + 0.15×Context_Similarity
```

**Two-stage architecture decision**: 
- Stage 1: Fast BM25-based candidate retrieval (top 50-100 facts)
- Stage 2: Semantic reranking with cross-encoders (top 10-15 results)
- Implementation: Use `rank-bm25` + HuggingFace transformers

**Graph properties as importance signals**:
- High connectivity to other concepts
- Bridging centrality between knowledge clusters
- Semantic stability over time

**Human memory architecture validation** (from `references/human-memory-architectural-insights.md`):
- Two-memory design aligns with declarative (facts) vs procedural (behaviors) memory systems
- Different retrieval mechanisms: spreading activation for facts, pattern matching for behaviors
- Working memory buffer needed to integrate both systems and resolve conflicts
- Context-aware retrieval essential: semantic similarity + contextual match + emotional salience
- Multi-timescale consolidation validates our read-in/store-back lifecycle

**Enhanced behavioral memory format**:
- Context: "When we're doing X" (current activity/phase)
- Internal State: "and I feel Y" (emotional/cognitive state)  
- Response: "then Z" (behavioral guidance)
- Requires tracking current activity, work phase, and recent patterns

**Dynamic connection networks**:
- Facts connect through co-occurrence patterns, not pre-defined relationships
- Connection strength based on recent co-occurrence frequency with temporal decay
- Connections weaken without reinforcement, preventing stale associations
- Creates living memory network that adapts to current collaboration patterns
- Avoids complex edge types or fixed embeddings

**Working memory insight**:
- Claude's conversation context IS the working memory buffer
- No need to build separate integration systems
- Focus shifts to: consolidation (what to store) + retrieval (what to surface when)
- Natural synthesis abilities handle memory integration automatically

**Implementation stack decision**:
- Language: Python with full type annotations
- Dependency management: `uv` for fast, reliable package management
- Key libraries: `rank-bm25`, `sentence-transformers`, `chromadb`/`faiss`
- Data validation: `pydantic` for fact schemas and metadata
- Project structure: `pyproject.toml` with modern Python best practices

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

## Research Focus
Currently investigating approaches for intelligent information curation:
- Core principles for determining information relevance over time
- Signals that indicate lasting importance vs temporary detail
- Design decisions for relevance scoring in collaborative AI memory
- Metadata/tracking requirements for effective curation

## Open Questions
- Context tracking implementation: How to detect and maintain "what are we doing" state
- Co-occurrence tracking: Optimal time windows and decay functions for connection strength
- Behavioral trigger detection: Recognizing internal states and context patterns in conversation
- Fact vs behavioral memory retrieval timing: When to surface each type proactively
- Connection threshold tuning: When do weak connections effectively disappear
- Consolidation automation: Detecting emoji patterns and extracting insights automatically
- Integration with existing Q chat workflow

## Resources
- MCP documentation for server implementation
- Human memory research for lifecycle modeling
- RAG/semantic search frameworks and tools
- Existing CLAUDE.md patterns for consolidation logic
