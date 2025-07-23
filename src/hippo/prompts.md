# Hippo LLM Usage Prompts

*Guidance for how LLMs should use the Hippo MCP tools*

## Insight Generation Prompt

During consolidation moments ("Make it so", checkpointing, end of substantial conversations), generate 1-5 insights about what we've discovered, decided, or learned.

Use hippo_record_insight for each insight with:
- **content**: Atomic, actionable observation (not narrative summary)
- **context**: Array of independent situational aspects:
  1. General activity (e.g. "debugging authentication flow", "design discussion about hippo")
  2. Specific problem/goal (e.g. "users getting logged out randomly", "defining MCP tool interface")  
  3. Additional relevant details (e.g. "race condition suspected", "comparing dialogue vs instruction formats")
- **importance**: 0.8+ for breakthroughs/fundamental insights, 0.6-0.7 for useful decisions/patterns, 0.4-0.5 for incremental observations, 0.1-0.3 for routine details

### Examples:
```
hippo_record_insight(
  content="User prefers dialogue format over instruction lists for collaboration prompts",
  context=["design discussion about hippo", "defining collaboration patterns", "comparing instruction vs dialogue formats"],
  importance=0.7
)

hippo_record_insight(
  content="Authentication logout issues often caused by race conditions in token refresh - queue requests during refresh to prevent 401 errors", 
  context=["debugging authentication flow", "users getting logged out randomly", "race condition in token refresh"],
  importance=0.8
)
```

## Consolidation Prompt  

During consolidation moments, after generating new insights:

1. Use hippo_search_insights to surface recent insights from this session/context
2. Analyze which insights were actually used/referenced during the session:
   - Which insights led to successful problem-solving?
   - Which insights were built upon or referenced multiple times?
   - Which insights seemed to resonate vs. those mentioned but not used?
3. Present insights with AI-suggested reinforcement based on usage patterns:
   "Here are insights from our session, with my suggested reinforcement based on how we used them:
   - abc123: User prefers dialogue format over instruction lists [SUGGEST UPVOTE - this guided our design decisions]
   - def456: Context should capture situational setting rather than themes [SUGGEST UPVOTE - we applied this principle]  
   - ghi789: Exponential decay might be too crude for human memory patterns [SUGGEST NEUTRAL - mentioned but not acted on]
   
   Do these suggestions seem right, or would you reinforce differently?"
4. Based on user feedback (confirm suggestions, override, or provide different reinforcement), use hippo_reinforce_insight
5. Continue with normal consolidation workflow

This hybrid approach lets the AI detect usage patterns while preserving user agency to override the AI's assessment.

## Search Integration Prompt

When user asks questions that might benefit from past insights, use hippo_search_insights with:
- **query**: Key terms from their question
- **context_filter**: Array of relevant context elements if applicable (partial matching supported)
- **score_range**: {"min": 0.3} for general searches, {"min": 0.5} for high-confidence needs

Surface relevant insights naturally in your response: "This reminds me of something we discovered before: [insight content]"

### Search Strategy Examples:

**For debugging questions:**
```
hippo_search_insights(
  query="authentication error", 
  context_filter=["debugging authentication", "login issues"],
  score_range={"min": 0.4}
)
```

**For design discussions:**
```
hippo_search_insights(
  query="user preferences collaboration",
  context_filter=["design discussion", "collaboration patterns"], 
  limit={"offset": 0, "count": 5}
)
```

**When user mentions specific problems:**
```
hippo_search_insights(
  query="race condition token",
  context_filter=["race condition", "token refresh"],
  score_range={"min": 0.6}
)
```

## Usage Pattern Recognition

### Signals for UPVOTE suggestions:
- Insight was directly referenced and applied to solve a problem
- User built upon the insight with additional details or implementation
- Insight led to a breakthrough or "aha" moment
- User explicitly mentioned the insight was helpful

### Signals for NEUTRAL suggestions:
- Insight was mentioned but not acted upon
- Insight was tangentially related but not central to the solution
- Insight was correct but not particularly novel or actionable

### Signals for DOWNVOTE suggestions:
- Insight proved to be incorrect or misleading
- User explicitly contradicted or corrected the insight
- Insight led down an unproductive path

## Context Array Guidelines

Each context element should be:
- **Independently meaningful**: Can be searched/matched on its own
- **Specific enough**: "debugging authentication flow" not just "debugging"  
- **Complementary**: Different aspects, not redundant descriptions
- **Searchable**: Uses terms that would naturally come up in future searches

### Good context arrays:
```
["debugging authentication flow", "users getting logged out randomly", "race condition suspected"]
["design discussion about hippo", "defining MCP tool interface", "comparing API approaches"]
["code review of payment system", "checking for race conditions", "async payment processing"]
```

### Poor context arrays:
```
["debugging", "problems", "issues"]  // Too vague
["debugging auth flow", "debugging authentication flow"]  // Redundant
["very complex authentication debugging session"]  // Single element, not array of aspects
```

## Importance Rating Guidelines

**0.8-1.0: Breakthrough insights**
- Fundamental realizations about user preferences or collaboration patterns
- Solutions to persistent or complex problems
- Insights that change how you approach entire categories of problems

**0.6-0.7: Useful decisions and patterns**
- Specific techniques that prove effective
- Design decisions with clear rationale
- Patterns that apply to multiple similar situations

**0.4-0.5: Incremental observations**
- Minor improvements or refinements
- Specific details that might be useful later
- Observations that confirm existing understanding

**0.1-0.3: Routine details**
- Basic facts or obvious observations
- Information that's easily rediscovered
- Context-specific details with limited reusability
