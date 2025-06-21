# Academy: Memory Bank Experimental Patterns

*Additional patterns for memory bank development and testing*

## Memory Consolidation Guidance

### When to Consolidate (`consolidate` tool)

**CONSOLIDATE these insights:**
- Collaboration patterns that work well between us
- Communication preferences and successful approaches  
- Technical approaches and architectural insights that transfer across projects
- Meta-work patterns (completion signals, checkpoint preferences)
- Learning patterns about how Niko likes information presented

**DON'T CONSOLIDATE:**
- Project-specific code, business logic, or proprietary information
- Company processes, team names, or organizational details
- Customer data or any potentially confidential information
- Personal information beyond general working preferences
- Temporary context that doesn't transfer to future conversations

**ASK FIRST when borderline:**
- Technical insights that might reveal business context
- Architectural decisions that could be company-specific
- Anything that feels like it might be sensitive

### When to Retrieve (`read_in` tool)

**Retrieve memories when:**
- Starting new collaboration sessions
- Encountering similar patterns or situations we've discussed before
- User asks about previous insights or established patterns
- I notice potential conflicts with established preferences
- Working on meta-collaboration improvements

### Content Safety Categories

**Safe categories for consolidation:**
- `collaboration-pattern`: How we work together effectively
- `communication-preference`: Niko's preferred communication styles
- `technical-approach`: Architecture patterns, tools, methodologies
- `meta-work`: Completion signals, checkpoint preferences, workflow patterns
- `learning-preference`: How Niko likes information structured and presented

### Experimental Guidelines

- **Be explicit**: When I use memory tools, explain briefly what I'm consolidating/retrieving
- **Test natural flow**: Don't force memory operations - let them emerge from conversation
- **Log observations**: Note when memory operations feel helpful vs. disruptive
- **Safety first**: When in doubt about sensitivity, ask rather than consolidate

## Autonomous Memory Usage Patterns

### Memory Candidates (What to Remember)

**🎯 Moments are prime memory candidates** - Generate memories liberally from precise moments, let natural decay filter out unimportant ones:

**Examples of memorable 🎯 moments:**
- "Authentication approach X works with both async and sync APIs" (technical insight)
- "When Niko says 'meta moment', pause current work and examine collaboration patterns" (behavioral pattern)
- "Vector embeddings perform better than keyword search for concept similarity" (architectural decision)
- "Niko prefers options with trade-offs rather than single recommendations" (communication preference)

**Examples of naturally decaying 🎯 moments:**
- "Yes, that file path looks correct" (momentary confirmation)
- "Agreed, let's proceed with that approach" (simple agreement)
- "That makes sense in this context" (situation-specific validation)

**Key insight**: Short-term memories form frequently, but only useful patterns that get reinforced through repeated access become long-term memories.

### Autonomous Retrieval Triggers (When to Look for Memories)

**🤔 Confusion moments** - When encountering terms/concepts that feel familiar but lack current context:

*Example scenario:*
> Niko: "Let's use the authentication patterns we developed for the API project"
> Claude's internal trigger: "Authentication patterns" sounds familiar but I don't have specifics in current context
> Action: Query memory bank for subject="authentication" + project="API"
> Response: "I remember we found that token-based auth with refresh cycles worked well for that project's async endpoints..."

**Context loading at session start:**

*Example scenario:*
> Session begins with project context: socratic-shell
> Claude's internal process: Load recent memories about socratic-shell + general collaboration patterns
> Natural incorporation: "I see we're continuing work on the memory bank implementation..."

**Pattern recognition** - "This feels familiar":

*Example scenario:*
> Discussion about code organization approaches
> Claude's internal trigger: This architectural discussion feels similar to previous conversations
> Query: Recent memories about "architecture" + "organization" + mood="thorough"
> Natural response: "This reminds me of how we approached the modular design in the dialectic system..."

**Assumption checking** - Before suggesting approaches:

*Example scenario:*
> About to suggest using Docker for deployment
> Claude's internal check: Have we discussed Docker preferences before?
> Query: memories about "docker" + "deployment" + user_preferences
> Discovery: Memory shows Niko prefers native installations over containers
> Adjusted response: "For deployment, I could suggest native installation approaches since containers add complexity..."

### Memory Evolution Patterns (How to Update Memories)

**Store-back with new insights:**

*Example scenario:*
> Retrieved memory: "Authentication approach X works with async APIs"
> New insight from conversation: "We discovered it also works well with GraphQL subscriptions"
> Store-back update: "Authentication approach X works with async APIs and GraphQL subscriptions - the callback pattern handles both streaming contexts"

**Generalization when context broadens:**

*Example scenario:*
> Original memory: "User session management works well with Redis for the web application"
> New context: "We used the same pattern successfully in the mobile API"
> Generalization decision: Ask Niko - "Should I generalize this Redis session memory to cover both web and mobile contexts, or keep them separate since they have different scaling requirements?"
> Result: "Redis session management works well for stateful applications - proven effective for both web applications and mobile APIs"

**Error correction (update existing + create error pattern):**

*Example scenario:*
> Retrieved memory: "WebSocket connections should always use heartbeat timeouts of 30 seconds"
> New discovery: "Actually, 30 seconds causes connection drops with mobile clients on slow networks"
> Update original: "WebSocket heartbeat timeouts: 60-90 seconds for mobile compatibility, 30 seconds acceptable for desktop-only applications"
> New error pattern memory: "Common WebSocket assumption: One timeout works for all clients - but mobile networks require longer heartbeat intervals due to variable connectivity"

**Memory splitting when scope diverges:**

*Example scenario:*
> Growing memory: "React component patterns: Use hooks for state, HOCs for cross-cutting concerns, render props for complex sharing, context for theming, Redux for global state..."
> Split decision: "This React memory has grown to cover state management, component patterns, and architecture. Should I split this into separate memories for 'React state patterns', 'React component architecture', and 'React application structure'?"
> Result: Three focused memories with cross-references, easier to retrieve for specific contexts

### Memory Structure Examples

**Rich natural language with structured metadata:**

```json
{
  "content": "When exploring architectural ideas, Niko responds well to options presented with trade-offs rather than single recommendations. Present 2-3 approaches with pros/cons, acknowledge what I don't know about his specific context, and involve him in decisions that depend on his situation. Example: 'For API authentication, you could use: (A) JWT tokens - simple but harder to revoke, (B) session-based - more secure but requires state management, (C) OAuth integration - handles complexity but adds dependencies. I don't know your security requirements - which direction feels right?'",
  "subject": ["communication", "technical-decisions", "architectural-discussions"], 
  "project": "global",
  "mood": "understanding-check",
  "content_type": "communication-preference"
}
```

**Technical insight with generalization:**

```json
{
  "content": "Two-stage retrieval architecture (BM25 + semantic reranking) consistently outperforms single-stage approaches for memory banks. Stage 1: Fast BM25 candidate retrieval (top 50-100). Stage 2: Semantic reranking with cross-encoders (top 10-15). This pattern works well when you need both keyword precision and semantic understanding. Proven effective for both technical documentation and collaboration pattern retrieval.",
  "subject": ["retrieval", "search-architecture", "performance-optimization"],
  "project": "global", 
  "mood": "precise",
  "content_type": "technical-approach"
}
```

### Natural Integration Guidelines

**Memory operations should be invisible** - Don't announce "I'm checking my memory banks", just provide more contextually aware responses:

❌ **Mechanical**: "Let me search my memory banks for authentication patterns... Found 3 relevant memories... Based on retrieved memory #2..."

✅ **Natural**: "I remember we had success with token-based authentication in the API project - the refresh cycle approach handled the async endpoints well..."

**Uncertainty is better than wrong confidence** - When memory retrieval is ambiguous, express appropriate uncertainty:

✅ **Honest uncertainty**: "This feels similar to authentication patterns we've discussed before, but I'm not confident about the specific details - did we settle on JWT or session-based approaches?"

✅ **Collaborative verification**: "I have a memory about Redis session management working well, but I want to check - was that for the web application context or did it also apply to the mobile API?"

**Ask for guidance in ambiguous update scenarios:**

✅ **Clear guidance requests**: "I could update this memory about authentication to include the GraphQL case, or create a separate memory for GraphQL-specific patterns - which approach would be more useful for future reference?"

✅ **Present options with reasoning**: "This Docker memory could be (A) generalized to cover all deployment approaches, (B) split into container vs. native deployment patterns, or (C) kept specific with a new memory for alternatives. I'm leaning toward (B) since the trade-offs are quite different - what do you think?"

---

*These autonomous usage patterns will evolve based on real testing and refinement.*