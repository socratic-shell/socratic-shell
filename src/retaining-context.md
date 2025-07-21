# Retaining Context

With collaborative prompting, you can build up good rapport with Claude - shared understanding, working patterns, and preferences for how to approach problems. But when you quit and return later, Claude has forgotten the specifics of what you were doing and details of what you like and don't like.

## The Goal: Collaborative Partnership, Not Rigid Structure

The aim isn't to create a complex memory system that forces AI into rigid patterns. Instead, we want to preserve the collaborative relationship while leveraging AI's natural strengths - the ability to collect, digest, and synthesize information organically. 

Rather than cognitive overhead from complex structures, we want memory that supports the natural flow of collaborative work: consolidation moments, insight recognition, and the gradual deepening of shared understanding.

## Different Types of Context Need Different Approaches

Context retention isn't one problem but several:
- **Interaction preferences** - How you like to work with AI. Sometimes a pattern is so broad that we extend the user prompt, but memory systems can be helpful for finer-grained details.
- **Project information** - Current state, goals, architecture decisions.
- **Shared code knowledge** - How things work that should benefit everyone
- **Personal insights** - Your individual journey and understanding

## Different audiences

One of my key goals is to figure out how to fit Claude into existing project workflows, particularly open source workflows. I want to be able to retain *both* individual memory that is tailored to what *you* have done and to separate out general knowledge that can be useful to everyone. I believe that, just like humans, Claude won't be able to remember everything all of the time, so we need organizational systems that let us pull things in on demand and avoid overwhelming Claude (or the human!). 

It's also useful sometimes for the memory of an individual to drift from the memory of the project -- for example, much of my memory about rustc is out-of-date when it comes to the particular project structure, but it'd still be useful for Claude to remember what we last saw and be updated with the latest version. Then it can advise me that something has changed since I last looked at it.

## Current Approaches

### [Explicit Context Management](./tracking-task-status/README.md)
To track the state of tasks, explicit context management seems to work pretty well. Claude and I maintain our context explicitly, either through [AI-managed tracking issues on GitHub](./tracking-task-status/README.md) or the older approach of [files for each ongoing task](./tracking-task-status/README.md). When we come up with good new ideas or finish some phase of the work, I ask Claude to checkpoint our progress and they create commits and summarize our progress. Then we can always reload and figure out where we were.

### [AI Insights Comments](./ai-insights-comments/README.md)
[AI insights comments](./ai-insights-comments/README.md) retain knowledge directly in code that will be needed when later editing the code. Using `💡` comment annotations, we capture non-obvious constraints, reasoning, and implementation tradeoffs right where they're most relevant. This is an example of encoding memory for others to find in a natural way - the context travels with the code itself.

### MCP Memory Systems
At the more sophisticated end of the spectrum are various MCP memory systems. I have two ongoing experiments: 

1. [Adapting the official MCP memory server](./official-memory-server/README.md) for use with collaborative prompting.
2. Experimenting with building a [custom memory bank](./memory-bank/README.md) server.

## Status

This area is very much in flux. The key insight is that different types of context may need different retention strategies.

[Yehuda Katz]: https://www.linkedin.com/in/yehudakatz/
[Kari Wilhelm]: https://www.linkedin.com/in/kariwilhelm/
