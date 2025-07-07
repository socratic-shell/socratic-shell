# Design Foundation

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

## Key Design Decisions

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