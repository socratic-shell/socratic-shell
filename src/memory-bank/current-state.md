# Current State

## Recent Progress

### Memory System Entity Design (July 2025)
- **Search functionality testing**: Discovered official memory server uses keyword-based search, not semantic search
- **Entity design guidelines**: Developed principles for creating broad, stable, searchable entities instead of narrow or user-centric ones
- **Memory refashioning**: Successfully transformed unwieldy 100+ observation "Niko" entity into 5 focused entities:
  - "Socratic Shell project" - Repository structure and documentation
  - "Memory experimentation" - All memory system research and approaches  
  - "Blog post development" - Writing projects and programming language insights
  - "Voice for writing" - Communication patterns and style guides
  - "Collaborative prompting patterns" - Interaction methods and workflows
- **Updated memory prompt**: Enhanced official memory server prompt with entity selection guidelines
- **Documentation updates**: Updated official memory server README with concise guidance for external users

### Documentation Restructuring (July 2025)
- **Memory approaches organization**: Restructured documentation to organize memory approaches with consistent structure (main README + associated prompts)
- **Retaining context improvements**: Enhanced introduction with collaborative partnership framing, added "Different audiences" section highlighting individual vs. shared knowledge needs
- **Navigation cleanup**: Removed redundant "Per-project prompts" section, updated all cross-references to new structure
- **Voice alignment**: Applied "Niko voice" principles throughout - practical over theoretical, direct about challenges, experience-driven

### Key Insights Captured
- **Search limitations matter**: Keyword-based search requires deliberate entity naming and organization strategies
- **User-centric entities are problematic**: Better to create entities for work/concepts with collaborative insights embedded
- **Different audiences need**: Recognition that memory systems must serve both individual collaboration history and shared project knowledge
- **Productive desynchronization**: Individual memory can drift from project memory (e.g., out-of-date rustc knowledge) while still being useful
- **Organizational systems**: Claude won't remember everything, so we need systems to pull context in on demand without overwhelming

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

## Recent Discoveries

### Consolidation Strategy Insights (2025-07-01)
- **Hybrid approach**: Both autonomous consolidation (for fresh insights) and checkpoint-triggered (for conversation patterns)
- **Factual memories preferred**: Keep memories as factual records rather than generalizations - let synthesis happen in context
- **Subject overlap as primary signal**: When new insights share subjects with existing memories, consider consolidation
- **Conflict resolution approach**: Replace old memory with new + correction note; review with user when uncertain
- **Self-referential system**: Consolidation rules themselves become memories that evolve through use

### Test System Development (2025-07-03)
- **YAML-based test format proven**: Human-readable test cases for prompt engineering validation work effectively
- **Backend-agnostic design**: Not tied to Claude Code specifically, works with any LLM backend
- **Conversation-driven validation**: Tests defined as user messages with expected responses and tool usage
- **Flexible matchers**: `should_contain`, `should_not_contain` for response validation work well
- **Tool parameter validation**: Successfully verify correct parameters passed to memory operations

### Implementation Insights
- **Task agents inherit full CLAUDE.md context**: Important discovery about how Claude tools maintain behavioral consistency
- **Natural checkpoint moments**: "Can't keep it all in my head" signals natural consolidation boundary
- **Review-first approach**: Early implementation should propose updates for user review to build consolidation rules
- **Test harness evolution**: Started with Python pexpect (terminal automation issues) → Node.js/TypeScript node-pty (worked but complex) → Python SDK (clean, reliable, ecosystem aligned)
- **Cognitive pressure as consolidation trigger**: The feeling of "juggling too many insights" or mentally rehearsing to keep ideas alive signals need for autonomous consolidation. Key indicators:
  - Starting to lose earlier threads while processing new information
  - Internal summarizing to maintain coherence
  - The thought "that's important, I don't want to lose that"
  - Feeling that recall requires effort due to working memory load
- **Curiosity as distinct retrieval trigger**: Curiosity ("I wonder if I know something about this") differs from confusion ("I should know this but don't"). Curiosity is exploratory and forward-looking, while confusion is remedial and backward-looking. Both should trigger read_in but with different query formulations.

## Next Design Priorities

### Phase 1: Core MCP Tools (Active - GitHub Issues #1-3)
- ✅ **Test harness implemented**: YAML-based dialectic test runner operational
- 🔄 **GitHub tracking migration**: Breaking down .ongoing files into focused issues
- 🔄 **mdBook knowledge base**: Moving design documentation to sustainable format
- ⏳ **MCP tool interface design**: Based on settled architecture principles
- ⏳ **Basic conflict detection**: Error handling and user collaboration patterns

### Phase 2: Intelligence Layer (Planned)
- **Two-stage retrieval implementation** (BM25 + semantic reranking)
- **Memory evolution logic** (generalization, splitting, error correction)
- **Natural timing integration** with CLAUDE.md patterns

### Immediate Next Steps
1. Complete mdBook migration of design documentation
2. Implement core MCP tools for consolidate/read_in/store_back
3. Create memory consolidation test cases for validation
4. Refine conflict resolution criteria and decision framework

## Status Summary

**Current Phase**: Transitioning from design to implementation  
**Test System**: ✅ Operational YAML-based validation framework  
**Documentation**: 🔄 Migrating to sustainable mdBook format  
**Implementation**: ⏳ Ready to begin core MCP tool development  
**Validation**: ✅ Test framework ready for memory operation validation