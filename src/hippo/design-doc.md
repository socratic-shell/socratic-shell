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
      "context": [
        "design discussion about hippo",
        "defining collaboration patterns",
        "comparing instruction vs dialogue formats"
      ],
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
- **context**: Array of independent situational aspects describing when/where the insight occurred
- **importance**: AI-generated 0-1 rating of insight significance (set at creation)
- **score_at_last_change**: The score when it was last modified (starts at 1.0)
- **score_last_modified_at**: When the score was last explicitly changed (upvote/downvote)

### Score Computation

Current score computed on-demand using research-backed weighting:

```
current_score = base_score * importance * recency_factor

where:
base_score = score_at_last_change  
recency_factor = 0.9 ^ days_since_score_last_modified
importance = AI-generated 0-1 rating (acts as importance weight from research)
```

For search ranking, we'll eventually incorporate the full research formula:
```
Relevance = 0.3×Recency + 0.2×Frequency + 0.35×Importance + 0.15×Context_Similarity
```

MVP implementation focuses on Recency (decay) and Importance (AI rating), with Frequency and Context_Similarity planned for future iterations.

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

## MCP Tool Interface

### Server Configuration
The Hippo MCP server takes a `--hippo-file` argument specifying the path to the JSON storage file:
```bash
hippo-server --hippo-file /path/to/hippo.json
```

### Tool Definitions

#### `hippo_record_insight`
```json
{
  "name": "hippo_record_insight",
  "description": "Record a new insight during consolidation moments",
  "inputSchema": {
    "type": "object",
    "properties": {
      "content": {
        "type": "string",
        "description": "The insight content - should be atomic and actionable"
      },
      "context": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Array of independent situational aspects describing when/where this insight occurred. Include: 1) General activity (e.g. 'debugging authentication flow', 'design discussion about hippo'), 2) Specific problem/goal (e.g. 'users getting logged out randomly', 'defining MCP tool interface'), 3) Additional relevant details (e.g. 'race condition suspected', 'comparing dialogue vs instruction formats'). Each element should be independently meaningful for search matching."
      },
      "importance": {
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "description": "AI-assessed importance rating: 0.8+ breakthrough insights, 0.6-0.7 useful decisions, 0.4-0.5 incremental observations, 0.1-0.3 routine details"
      }
    },
    "required": ["content", "context", "importance"]
  }
}
```

#### `hippo_search_insights`
```json
{
  "name": "hippo_search_insights",
  "description": "Search for relevant insights based on content and context",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query for insight content"
      },
      "context_filter": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Filter results by matching any context elements using partial matching. Examples: ['debugging authentication'] matches insights with 'debugging authentication flow', ['users getting logged out'] matches specific problem contexts. Can provide multiple filters - results match if ANY context element partially matches ANY filter."
      },
      "limit": {
        "type": "object",
        "properties": {
          "offset": {"type": "integer", "default": 0},
          "count": {"type": "integer", "default": 10}
        },
        "description": "Result pagination. Default: {offset: 0, count: 10} returns first 10 results. Examples: {offset: 10, count: 5} for next 5 results",
        "default": {"offset": 0, "count": 10}
      },
      "score_range": {
        "type": "object",
        "properties": {
          "min": {"type": "number", "default": 0.1},
          "max": {"type": "number", "default": null}
        },
        "description": "Score range filter. Examples: {min: 0.6, max: 1.0} for decent insights, {min: 1.0} for highly reinforced insights, {max: 0.4} for low-quality insights"
      }
    },
    "required": ["query"]
  }
}
```

**Returns:**
```json
{
  "insights": [
    {
      "uuid": "abc123-def456-789",
      "content": "User prefers dialogue format over instruction lists",
      "context": [
        "design discussion about hippo",
        "defining collaboration patterns", 
        "comparing instruction vs dialogue formats"
      ],
      "importance": 0.7,
      "current_score": 1.2,
      "created_at": "2025-07-23T17:00:00Z",
      "days_since_created": 3,
      "days_since_score_modified": 1
    }
  ],
  "total_matching": 15,
  "returned_count": 10,
  "score_distribution": {
    "below_0.2": 2,
    "0.2_to_0.4": 1, 
    "0.4_to_0.6": 2,
    "0.6_to_0.8": 3,
    "0.8_to_1.0": 4,
    "above_1.0": 3
  }
}
```

#### `hippo_modify_insight`
```json
{
  "name": "hippo_modify_insight",
  "description": "Modify an existing insight's content, context, or importance",
  "inputSchema": {
    "type": "object", 
    "properties": {
      "uuid": {
        "type": "string",
        "description": "UUID of the insight to modify"
      },
      "content": {
        "type": "string",
        "description": "New insight content (optional - only provide if changing)"
      },
      "context": {
        "type": "array",
        "items": {"type": "string"},
        "description": "New situational context array (optional - only provide if changing)"
      },
      "importance": {
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "description": "New importance rating (optional - only provide if changing)"
      },
      "reinforce": {
        "type": "string",
        "enum": ["upvote", "downvote", "none"],
        "description": "Reinforcement to apply with modification. Default: 'upvote' (since modification usually signals value)",
        "default": "upvote"
      }
    },
    "required": ["uuid"]
  }
}
```

#### `hippo_reinforce_insight`
```json
{
  "name": "hippo_reinforce_insight", 
  "description": "Apply reinforcement feedback to multiple insights",
  "inputSchema": {
    "type": "object",
    "properties": {
      "upvotes": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Array of UUIDs to upvote (2.0x score multiplier)",
        "default": []
      },
      "downvotes": {
        "type": "array", 
        "items": {"type": "string"},
        "description": "Array of UUIDs to downvote (0.1x score multiplier)",
        "default": []
      }
    },
    "required": []
  }
}
```

### LLM Usage Prompts

See [prompts.md](./prompts.md) for detailed guidance on how LLMs should use the Hippo MCP tools during insight generation, consolidation, and search.

### Core Operations
```
record_insight(content, context, importance) → uuid
search_insights(query, context_filter?, score_range?, limit?) → InsightResults
reinforce_insight(upvotes[], downvotes[]) → success
modify_insight(uuid, content?, context?, importance?, reinforce?) → success
```

## Technical Architecture
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

## Example Usage

See [example-dialog.md](./example-dialog.md) for a detailed walkthrough showing all four MCP operations in realistic collaborative sessions.

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

## Implementation Plan

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
