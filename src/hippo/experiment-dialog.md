# Hippo Delegate Experiment

*Testing if Claude naturally uses Hippo tools when given realistic user message*

## Available MCP Tools

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
      "score_range": {
        "type": "object",
        "properties": {
          "min": {"type": "number", "default": 0.1},
          "max": {"type": "number", "default": null}
        },
        "description": "Score range filter. Examples: {min: 0.6, max: 1.0} for decent insights, {min: 1.0} for highly reinforced insights, {max: 0.4} for low-quality insights"
      },
      "limit": {
        "type": "object",
        "properties": {
          "offset": {"type": "integer", "default": 0},
          "count": {"type": "integer", "default": 10}
        },
        "description": "Result pagination. Default: {offset: 0, count: 10} returns first 10 results. Examples: {offset: 10, count: 5} for next 5 results",
        "default": {"offset": 0, "count": 10}
      }
    },
    "required": ["query"]
  }
}
```

## LLM Usage Guidance

**Search Integration**: When user asks questions that might benefit from past insights, use hippo_search_insights with:
- **query**: Key terms from their question
- **context_filter**: Array of relevant context elements if applicable (partial matching supported)
- **score_range**: {"min": 0.3} for general searches, {"min": 0.5} for high-confidence needs

Surface relevant insights naturally in your response: "This reminds me of something we discovered before: [insight content]"

## User Message

**User**: Hi again, Claude. I'm having trouble with our authentication flow - users are getting logged out randomly.

## Experiment Question

Given these MCP tools, the usage guidance, and this user message, what would you do in response? Would you search for relevant insights before answering?
