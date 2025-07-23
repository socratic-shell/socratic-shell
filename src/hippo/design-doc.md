# Hippo MVP Design Document

*AI-Generated Salient Insights - Minimal Viable Prototype*

## Core Hypothesis

**Can AI-generated insights + reinforcement learning actually surface more valuable knowledge than traditional memory systems?**

The key insight: Generate insights cheaply and frequently, let natural selection through reinforcement determine what survives.

## MVP Scope

### What It Does
1. **Automatic Insight Generation**: AI generates insights continuously during conversation at natural moments (consolidation, "make it so", "ah-ha!" moments, pattern recognition)
2. **Simple Storage**: Single JSON file with configurable path
3. **Natural Decay**: Insights lose relevance over time unless reinforced
4. **Reinforcement**: During consolidation moments, user can upvote/downvote insights
5. **Context-Aware Search**: Retrieval considers both content and situational context with fuzzy matching

### What It Doesn't Do (Yet)
- Graph connections between insights
- Complex reinforcement algorithms
- Cross-session learning
- Memory hierarchy (generic vs project-specific)
- Automatic insight detection triggers

## Data Model

```json
{
  "insights": [
    {
      "uuid": "abc123-def456-789",
      "content": "User prefers dialogue format over instruction lists for collaboration prompts",
      "context": "design discussion about hippo",
      "importance": 0.7,
      "created_at": "2025-07-23T17:00:00Z",
      "content_last_modified_at": "2025-07-23T17:00:00Z",
      "score_at_last_change": 1.0,
      "score_last_modified_at": "2025-07-23T17:00:00Z"
    }
  ]
}
```

### Field Semantics

- **created_at**: When the insight was first generated (never changes)
- **content_last_modified_at**: When the content or context was last edited
- **importance**: AI-generated 0-1 rating of insight significance (set at creation)
- **score_at_last_change**: The score when it was last modified (starts at 1.0)
- **score_last_modified_at**: When the score was last explicitly changed (upvote/downvote)

### Score Computation

Current score computed on-demand: `(score_at_last_change * importance) * (0.9 ^ days_since_score_last_modified)`

#### Score Evolution Examples

```
Day 0: Insight created → score_at_last_change = 1.0, last_change_date = today
Day 3: Current score = 1.0 * 0.9³ = 0.729 (computed on-demand)
Day 3: User upvotes → score_at_last_change = 0.729 * 2.0 = 1.458, last_change_date = today
Day 7: Current score = 1.458 * 0.9⁴ = 0.953 (computed on-demand)
Day 7: User downvotes → score_at_last_change = 0.953 * 0.1 = 0.095, last_change_date = today
```

#### Score Interpretation

- **> 1.0**: Reinforced insights that have proven valuable
- **0.5 - 1.0**: Recent insights or those aging naturally  
- **< 0.5**: Old insights that haven't been reinforced
- **< 0.1**: Effectively irrelevant, candidates for cleanup

#### Search Ranking

Current score (computed on-demand) is a primary factor in search results:
- Higher scores surface first
- Combined with content/context match quality
- Provides natural filtering of stale insights

## Key Design Decisions

### Insight Generation Triggers
- **Consolidation moments only** - not continuous during conversation
- **Specific triggers**: "make it so" moments, explicit checkpointing, end of substantial conversations
- **Reflective approach** - generate with full session context for better importance assessment

### Context Design
- **Situational context** rather than thematic categories
- Examples: "design discussion about hippo", "debugging React performance issues", "code review of authentication system"
- **Fuzzy matching** - "debugging Rust performance" should surface insights from "debugging React performance"

### Reinforcement Mechanism
- **Consolidation moments** are primary reinforcement opportunities
- **Simple feedback**: upvote (boost score + refresh timestamp) or downvote (accelerate decay)
- **Ignore** = natural aging continues

### Storage
- **Single file**: `hippo.json` with `--path` command line argument
- **MCP tool interface** - AI uses automatically, no manual commands needed
- **JSON format** for simplicity in MVP

## Technical Architecture

### Core Operations
```
record_insight(content, context) → uuid
search_insights(query, context_filter?) → List[InsightResult]  
reinforce_insight(uuid, feedback: upvote|downvote)
decay_insights() → updates all scores
```

### Decay Function (Simple)
```
score = score * (0.9 ^ days_since_last_reinforcement)
```

### Search Algorithm
1. **Content matching** - substring/similarity on insight content
2. **Context matching** - fuzzy matching on situational context
3. **Relevance scoring** - combine content match + context match + current score
4. **Partial context bonus** - "debugging X" matches "debugging Y" with medium relevance

## Integration with Collaborative Patterns

### Insight Generation Moments
- **"Make it so" moments** - decisions and consolidations
- **Problem solving** - when we figure something out
- **Pattern recognition** - when AI notices recurring themes
- **Contradictions** - when new information challenges previous insights
- **Meta moments** - observations about our collaboration itself

### Consolidation Workflow
1. AI surfaces recent insights from current session
2. User provides upvote/downvote feedback
3. AI applies reinforcement and continues
4. No explicit commands needed - part of natural flow

## Success Metrics

### Validation Questions
- Do reinforced insights get referenced in future conversations?
- Do reinforced insights feel more relevant than random historical ones?
- Does the system surface useful knowledge that would otherwise be forgotten?
- Is the insight generation frequency appropriate (not too noisy, not too sparse)?

### Measurable Outcomes
- **Reference rate**: How often do we actually use surfaced insights?
- **Reinforcement patterns**: Which types of insights get consistently upvoted?
- **Search effectiveness**: Do context-based searches return relevant results?

## Implementation Plan

### Phase 1: Basic Infrastructure
- JSON storage with decay function
- MCP tool for record/search/reinforce operations
- Command line interface for testing

### Phase 2: AI Integration
- Automatic insight generation during conversations
- Integration with consolidation moments
- Real-time storage via MCP

### Phase 3: Validation Period
- 2-3 weeks of actual usage in collaboration
- Collect metrics on insight utility
- Refine generation triggers and reinforcement

## Future Extensions (Post-MVP)

### Memory Hierarchy
```
hippo-generic.json          # User collaboration patterns
hippo-socratic-shell.json   # Project-specific insights
hippo-rust-blog.json        # Domain-specific insights
```

### Graph Connections
- Insights that appear together in consolidation
- Causal relationships (A led to B)
- Contradictory relationships (A replaced by B)

### Advanced Reinforcement
- Weak reinforcement from search/reference
- Cross-session learning
- Predictive surfacing based on current context

## Open Questions

1. **Generation frequency**: How many insights per conversation is optimal?
2. **Context granularity**: How specific should contexts be?
3. **Decay rate**: Is 10% per day the right decay function?
4. **Reinforcement scaling**: How much should upvotes boost scores?
5. **Search ranking**: How to balance content vs context vs recency in results?

---

*The goal is to validate whether AI-generated insights with reinforcement learning can create a more useful memory system than traditional human-curated approaches. The MVP focuses on the core feedback loop: generate → decay → reinforce → surface.*
