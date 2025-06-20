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

## Recent Discoveries (June 20, 2025)

**PageRank for importance scoring**: NetworkX library provides ready-to-use PageRank implementation in Python. Graph can be built from co-occurrence patterns (facts retrieved together = edges), with edge weights based on frequency and temporal decay. This gives us automatic importance scoring based on how central each fact is to the knowledge network.

**Task Tool for pattern testing**: MCP Task tool enables spawning isolated Claude contexts for testing pattern clarity. Similar to JS workers - complete context transfer but no shared state mutation. Could transfer pattern descriptions + test cases to fresh Claude, get back classification results without contaminating main conversation thread. Enables rapid iteration on collaboration patterns.

**Insight Completion Hook refinement**: Consolidated trigger pattern recognizes natural conversation breakpoints where one insight thread completes and we transition to another. Key insight: consolidation should align with conversation rhythm, not just task boundaries. Pattern now includes concrete examples and explicit trigger phrases.

**Meta-insight on cognitive load management**: Consolidation moments prevent cognitive overload by clearing completed threads before opening new ones. Multiple active threads create discomfort and risk losing key insights. The pattern of "review recent history → take action on actionable items → record notes on the rest" creates clean transitions between topics while preserving important discoveries.

**Emotional state as completion signal**: Both participants experienced a shift from "cognitive tension with multiple threads" to "clear and grounded" after successful consolidation. This feeling of completion satisfaction and mental space opening may serve as an additional signal for readiness to move on, complementing the explicit language patterns in the Insight Completion Hook. Worth observing in future collaborations.

**Dialectic MCP server implementation**: Built complete MCP server for testing collaboration patterns through structured conversation scenarios. Key decisions: Python with strict typing, uv for dependency management, async parallel sampling, proper MCP integration with auxiliary type comments for untyped decorators. Server provides `test_pattern` tool that takes base context + pattern instruction + test scenarios, returns structured results for human evaluation. Ready for testing Insight Completion Hook and other patterns systematically.

**Completion Hook unification**: Merged Insight Completion Hook and Checkpoint Hook into unified Completion Hook pattern. Recognition signals remain consistent (explicit deferral, clear pivots, scope shifts, meta signals, emotional shift from tension to clarity). Key innovation: match response type to completion type - insight completion gets documented, implementation milestones get committed, work sessions get full checkpointed, etc. "Checkpoint our work" remains definitive code phrase for full preservation process. Enables proactive recognition and appropriate action suggestions based on what was actually completed.

**Dialectic MCP server ready for testing**: Fixed entry point for command line usage (async wrapper), ready to configure with Claude Code. Next step: run `claude mcp add dialectic-local "cd /home/nikomatsakis/dev/socratic-shell/dialectic && uv run dialectic"` to register server locally. Test plan: use Completion Hook pattern with scenarios like "Good point, we can figure that out as we go. Let's talk about implementation." vs "That's very interesting. Let's talk about implementation." to see if fresh Claude recognizes completion signals differently.

## Resources
- MCP documentation for server implementation
- Human memory research for lifecycle modeling
- RAG/semantic search frameworks and tools
- Existing CLAUDE.md patterns for consolidation logic
