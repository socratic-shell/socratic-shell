# AI Insights Comments

Contextual memory embedded directly in code using structured comment annotations.

## What It Provides
- Non-obvious constraints and reasoning preserved in code
- Context for future AI programming sessions
- Decision boundaries and implementation tradeoffs
- Algorithmic and architectural choices explained inline

## The Approach
Rather than external memory systems, this approach embeds collaborative insights directly where they're most relevant - in the code itself. Using `💡` comment annotations, we capture the reasoning behind implementation choices that aren't obvious from reading the code alone.

This creates a form of contextual memory that travels with the code and provides immediate context when AI encounters it in future sessions.

## Custom Prompt Integration
The [AI Insights prompt](../prompts/project/ai-insights.md) guides Claude to systematically add these annotations during code generation and modification, ensuring that important reasoning doesn't get lost between sessions.

## Status
**Active experiment** - Testing whether inline contextual memory can reduce the need for external memory systems by preserving collaborative insights where they're most useful.
