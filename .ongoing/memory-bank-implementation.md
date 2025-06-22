# Socratic Shell Memory Bank - Living Design Document

**Status**: Design Complete - Ready for Implementation  
**Last Updated**: 2025-06-22

## Core Goal
**Intelligent context curation**: Scale gracefully as our collaborative knowledge base grows, naturally retaining important facts while discarding extraneous detail. The system should surface the right information at the right time, handling context accumulation in a way that enhances rather than overwhelms collaboration.

## Design Axioms

### Intelligence at the Right Layer
- **Keep tools simple and deterministic** - MCP tools handle storage, detection, basic operations
- **Put semantic understanding in the Claude layer** - Complex decisions happen with full context
- **Let the intelligent layer handle ambiguity** - Claude collaborates with user on uncertain cases

### User Partnership Over Automation  
- **When uncertain, involve the user rather than guessing** - Ask for guidance in ambiguous scenarios
- **Make collaborative decisions transparent, not hidden** - Show reasoning, present options
- **Build trust through predictable behavior + intelligent guidance** - Consistent tool layer, smart human layer

### Follow Natural Conversation Topology
- **Operations align with natural boundaries** - Checkpoints, topic shifts, completion signals
- **Memory serves conversation flow rather than interrupting it** - Background operations, invisible integration
- **Context expands/contracts based on actual needs** - Load what's relevant when it's relevant

### Context is King
- **Full conversation context beats isolated processing** - Current work informs memory decisions
- **Rich context enables better decision-making** - Memory conflicts resolved with full understanding
- **Current insights inform past memory evolution** - Store-back updates use fresh context

### Learn from Biology
- **Mirror human memory architecture** - Short-term (LLM context) to long-term (consolidated storage) pipeline
- **Episodic vs semantic memory distinction** - Store both specific experiences and generalized patterns
- **Intelligent forgetting as feature** - Natural decay filters signal from noise, like human forgetting curve
- **Context-dependent retrieval** - Memory surfaced based on current situation, not just keyword matching
- **Consolidation during rest periods** - Memory operations align with natural conversation boundaries

## Settled Design Decisions

### Memory Architecture
- **Content-addressable storage**: Facts stored with minimal structure, retrieved by semantic similarity (RAG approach)
- **Working memory = Native context**: No separate short-term storage - facts exist in conversation until consolidated
- **Memory Banks = Consolidated storage**: Long-term storage for proven useful facts
- **Memory lifecycle**: Active use → Consolidation → Read-in → Store-back → Intelligent curation

### Memory Structure
```json
{
  "content": "Rich natural language memory with full context",
  "subject": ["explicit", "searchable", "topics"],
  "project": "socratic-shell" | "global", 
  "mood": "curious" | "precise" | "understanding-check",
  "content_type": "insight" | "pattern" | "decision" | "ongoing_task"
}
```

**Why explicit subjects over pure embedding search:**
- **Relevance scoring enhancement**: Explicit subject matching provides strong signal for Context_Similarity component of relevance formula
- **Fast lookup on confusion**: When Claude encounters unfamiliar terms, direct subject search enables immediate context retrieval
- **Multi-subject memories**: Tags allow memories to surface for related but differently-worded concepts
- **Precision + semantic flexibility**: Combines exact topic matching with embedding search for comprehensive retrieval

### Memory Types
1. **Project insights**: Technical discoveries, decisions, patterns that worked
2. **User observations**: Niko's preferences, working style, context patterns  
3. **Cross-project patterns**: Collaboration approaches, meta-work insights

### Memory Interaction Patterns

**Memory Candidates** (What to Remember):
- **🎯 Precise moments** generate memories liberally with natural decay filtering
- Technical insights, behavioral patterns, architectural decisions, communication preferences
- Short-term memories form frequently, only reinforced patterns become long-term

**Autonomous Retrieval Triggers** (When to Look for Memories):
- **🤔 Confusion moments**: Unfamiliar terms/concepts that feel familiar
- **Context loading**: Session start, new topic emergence, explicit connections
- **Pattern recognition**: "This feels familiar" situations
- **Assumption checking**: Before suggesting approaches

**Memory Evolution Patterns** (How to Update):
- **Store-back**: Add new insights to existing memories about same topics
- **Generalization**: Broaden context when new situations prove wider applicability
- **Error correction**: Update incorrect memories + create mistake pattern memories
- **Memory splitting**: Separate distinct contexts that have grown together
- **Ask for guidance**: Present options when evolution path is unclear

### Operation Timing (Natural Conversation Flow)
- **Session start**: Load project + recent collaboration context  
- **During session**: Background retrieval on confusion/new topics, load context on connections
- **Topic boundaries/checkpoints**: Consolidate + store-back (same as "checkpoint our work")
- **Session end**: Final consolidation sweep

### Conflict Resolution Architecture
- **MCP tool**: Detects concurrent updates, returns conflict error with both versions
- **Claude layer**: Attempts intelligent merge using full conversation context
- **User collaboration**: Present merged result for approval/editing
- **Evolution opportunity**: Apply memory splitting/generalization rules during resolution

**Conflict Resolution Strategies:**
- **Additive merge**: Combine complementary insights about same topic ("auth works with REST" + "auth works with GraphQL" → "auth works with both REST and GraphQL")
- **Generalization**: Broaden context when updates suggest wider applicability ("web sessions" + "mobile sessions" → "session management for stateful applications")
- **Memory splitting**: Separate into distinct context-specific memories when scope has diverged
- **Error correction**: Update incorrect information + create mistake pattern memory for learning
- **Ask for guidance**: Present options when resolution path is unclear ("Should I generalize or split this memory?")

### Technical Stack
- **Language**: Python with full type annotations
- **Dependency management**: `uv` for fast, reliable package management  
- **Storage**: Git repository with individual JSON files (UUID + semantic prefix naming)
- **Indexing**: ChromaDB for in-memory two-stage retrieval (BM25 + semantic reranking)
- **Data validation**: Pydantic schemas for memory structure
- **Relevance scoring**: `0.3×Recency + 0.2×Frequency + 0.35×Importance + 0.15×Context_Similarity`

### Content Safety Strategy
- **Claude as gatekeeper**: Uses CLAUDE.md guidance for consolidation decisions
- **Safe categories**: Collaboration patterns, communication preferences, technical approaches, meta-work insights
- **Excluded**: Project code, company processes, proprietary information, personal details
- **Borderline cases**: Ask user explicitly rather than assume

### Integration with CLAUDE.md
- **Emoji patterns signal memory operations**: 🔍 curious exploration, 🎯 precise insights, 🤔 understanding checks
- **Warning signs become negative examples**: Store assumption traps and communication failures
- **Meta moments trigger explicit consolidation**: "Meta moment" = memory boundary
- **Completion hooks align with memory operations**: Same natural rhythm for all preservation

## Implementation Roadmap

### Phase 1: Core MCP Tools (Next)
- [ ] **Design MCP tool interface** based on settled architecture
- [ ] **Implement consolidate/read_in/store_back operations**
- [ ] **Basic conflict detection and error handling**
- [ ] **Refine conflict resolution criteria** - decision framework for when to apply additive merge vs. generalization vs. splitting vs. error correction

### Phase 2: Intelligence Layer
- [ ] **Two-stage retrieval implementation** (BM25 + semantic reranking)
- [ ] **Memory evolution logic** (generalization, splitting, error correction)
- [ ] **Natural timing integration** with CLAUDE.md patterns

### Phase 3: Testing & Refinement  
- [ ] **Academy integration** with experimental usage patterns
- [ ] **Real collaboration testing** with memory bank MCP server
- [ ] **Pattern refinement** based on actual usage

### Phase 4: Expansion
- [ ] **Replace manual .ongoing files** with memory bank storage
- [ ] **Cross-project memory sync** and inheritance patterns

## Open Questions

### Technical Implementation
- **Context detection**: How to automatically identify "what we're doing" for memory tagging
- **Co-occurrence tracking**: Optimal time windows and decay functions for connection strength
- **Connection thresholds**: When do weak memory connections effectively disappear
- **Performance optimization**: Memory loading strategies for large collaboration histories

### User Experience  
- **Memory operation visibility**: How much to show vs. keep invisible during natural usage
- **Conflict resolution UX**: Best ways to present merge options and gather user input
- **Cross-session continuity**: Maintaining memory context across different Claude instances

### Evolution & Learning
- **Pattern extraction**: Automatically detecting successful collaboration patterns from memory usage
- **Memory curation**: Balancing selective retention with comprehensive capture
- **System evolution**: How the memory bank itself learns and improves over time

## Frequently Asked Questions

### Why did memory bank scope evolve from "no project-specific data" to configurable storage?
Initially designed for pure cross-project patterns, but `.ongoing` files revealed that project-specific memories (like ongoing tasks) benefit from memory bank features. Solution: configurable storage destinations per project, allowing inheritance from global patterns while maintaining project-specific context.

### Why does conflict resolution happen in Claude layer rather than automated in MCP tool?
**Context advantage**: Claude has full conversation context when conflicts occur, enabling intelligent decisions about whether to merge, generalize, or split memories. Current work often reveals the right resolution path (e.g., "we're building mobile API now, so this conflict should favor mobile considerations"). Automated resolution would lack this contextual intelligence.

### How does natural decay work as signal filtering?
Like human forgetting curve, most memories form but only useful patterns survive through repeated access. 🎯 moments generate memories liberally, but memories that don't get "read-in" or "store-back" during future relevant conversations naturally fade. This filters signal from noise without requiring perfect upfront curation.

### Why align memory operations with checkpoint moments instead of immediate processing?
**Conversation flow preservation**: Memory operations at topic boundaries feel natural rather than disruptive. **Complete context**: Consolidation happens when understanding of a topic is complete, not mid-development. **Unified rhythm**: Single preservation moment handles both memory and git operations, reducing cognitive overhead.

### How do emoji patterns relate to memory moods?
Emoji patterns in CLAUDE.md serve as natural mode indicators that suggest memory consolidation opportunities. 🔍 curious exploration, 🎯 precise insights, 🤔 understanding checks each create different types of valuable memories. Not all emoji usage triggers consolidation - only when insights prove significant enough for future reference.

---

## Resources
- Human memory research: `references/human-memory-architectural-insights.md`
- Relevance scoring analysis: `references/2025-06-19-designing-memory-banks.md`  
- Behavioral patterns: `academy/CLAUDE.md`
- Technical foundation: `socratic-shell/` MCP server implementation