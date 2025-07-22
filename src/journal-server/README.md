# Journal Server Design

*A memory system that emerges from collaborative understanding*

## Vision

The journal server reimagines AI memory as an organic, reflective practice rather than mechanical storage. Instead of a database of facts, it maintains a living journal that captures both our current understanding and the collaborative journey that led there.

## Core Insight

Our experiments with the official MCP memory server revealed that traditional memory systems miss something essential: the hermeneutic circle of understanding. We don't just need to store facts - we need to capture how understanding deepens through the back-and-forth between parts and whole, between specific discoveries and evolving context.

The journal server aligns with our existing collaboration patterns:
- `.ongoing` files that track evolving work
- GitHub tracking issues that document understanding as it shifts
- Consolidation moments ("Make it so") when insights crystallize
- The natural rhythm of exploration → synthesis → new exploration

## Architecture

### Tree Structure

The journal organizes around a hierarchical structure that mirrors how understanding naturally develops:

```
journal/
├── project-alpha/
│   ├── overview.md          # Current synthesis/pre-understanding
│   ├── entries/             # Chronological journey log
│   │   ├── 2024-07-21-initial-exploration.md
│   │   ├── 2024-07-22-breakthrough-insight.md
│   │   └── ...
│   └── subsections/
│       ├── api-design/
│       │   ├── overview.md
│       │   └── entries/
│       └── error-handling/
│           ├── overview.md
│           └── entries/
└── project-beta/
    └── ...
```

### Three Types of Content

**Overviews**: Living synthesis documents that capture our current understanding of each section. These represent our "pre-understanding" - what we bring to new work in this area.

**Entries**: Chronological log of collaborative moments, insights, and discoveries. These document the hermeneutic journey - how our understanding evolved through actual work.

**Subsections**: Natural divisions that emerge from the work itself - major features, distinct problem domains, or significant architectural boundaries.

## Temporal Salience

Memory naturally decays and requires increasing relevance to surface:

- **Recent entries** (days/weeks): Easily accessible, loaded by default
- **Older entries** (months): Require higher relevance matching
- **Ancient entries** (longer): Only surface when specifically salient

This creates natural rhythms where current work builds on recent understanding while allowing deeper patterns to emerge when truly relevant.

## Session Flow

### Starting Work
When beginning a session, the journal server loads:
- **Current overviews** for relevant sections
- **Recent entries** that provide collaborative context
- **Salient older entries** that meet relevance thresholds

### During Work
The journal remains available for:
- Searching for related patterns and insights
- Referencing previous collaborative moments
- Understanding how current work connects to broader context

### Consolidation Moments
During checkpointing and "Make it so" moments:
- **Update overviews** with refined understanding
- **Add new entries** documenting the journey and insights
- **Create new sections** when work reveals natural boundaries

## Search Design

Search operates on two dimensions to provide contextually relevant results:

**Context**: The broader kind of work being done
- "debugging memory retrieval issues"
- "designing API interfaces" 
- "refactoring error handling"

**Content**: The specific thing being sought
- "async/await patterns"
- "configuration approaches"
- "testing strategies"

Journal entries are matched against both dimensions, preventing false positives where content matches but context doesn't (or vice versa).

## Integration with Existing Patterns

### Relationship to GitHub Issues
- **GitHub issues**: External view, public artifacts, status communication
- **Journal entries**: Internal view, intimate collaborative space, thinking process

### Relationship to `.ongoing` Files
- `.ongoing` files capture immediate work state
- Journal entries distill insights from `.ongoing` work during consolidation
- Overviews synthesize patterns across multiple `.ongoing` cycles

### Relationship to Tracking Issues
- Tracking issues document decisions and status for project management
- Journal entries capture the collaborative journey that led to those decisions
- Both evolve together but serve different purposes

## Why Journal vs. Database

Traditional memory systems treat information as discrete facts to be stored and retrieved. The journal approach recognizes that understanding is:

- **Contextual**: The same insight means different things in different situations
- **Temporal**: Recent understanding builds on older insights in complex ways
- **Collaborative**: Meaning emerges between minds, not within individual storage
- **Organic**: Consolidation happens naturally, not on rigid schedules

The journal serves the deeper practice of collaborative understanding rather than just information management.

## Next Steps

This design document captures our current understanding of the journal server concept. The next phase involves:

1. **Detailed specifications** for the tree structure and entry formats
2. **Search implementation** design for context/content matching
3. **Integration patterns** with existing MCP tooling
4. **Prototype development** to test the core concepts

---

*This design emerges from our collaborative exploration of memory systems that honor the hermeneutic circle of understanding.*
