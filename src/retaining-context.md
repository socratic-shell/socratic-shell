# Retaining Context

Collaborative prompting works great until the context starts to run out or you end your session. Then you have to start all over again. I haven't found things like Claude Code's `/compact` command to be very effective, so I've been exploring alternatives.

## The Challenge: Multiple Types of Context

There are many different kinds of context to retain:
- **Interaction preferences** - How you like to work with AI
- **Project information** - Current state, goals, architecture decisions  
- **Shared code knowledge** - How things work that should benefit everyone
- **Personal insights** - Your individual journey and understanding

## Current Approaches

### Explicit Context Management
Claude and I maintain our context explicitly, either in [files for each ongoing task](./prompts/project/ongoing-work-tracking.md) or, more recently, through [AI-managed tracking issues on GitHub](./prompts/project/github-tracking-issues.md). When we come up with good new ideas or finish some phase of the work, I ask Claude to checkpoint our progress and they create commits and summarize our progress. Then we can always reload and figure out where we were.

### Interaction Pattern Memory
Tracking issues work pretty well for *tasks* but don't really capture changes to the *way* we interact. Right now, I've found that my [user prompt](./prompts/user/README.md) is a great start, though it helps to begin each fresh Claude session with "Hi again, Claude!", which triggers Claude to review the patterns with me. That creates a more spacious mood from the outset - not loading information, but setting the quality of attention we bring to the work.

### Quote-Based Systems
I admire the systems used by [Yehuda Katz][] and [Kari Wilhelm][], two fellow travelers in this journey, who have asked Claude to record salient quotes and insights during sessions into a file, then reload that file at startup to 'recreate the soul' of previous work. This is very appealing and something I want to try.

### MCP Memory Systems
At the more sophisticated end of the spectrum are various MCP memory systems. I have been exploring this space - see [Memory Experimentation](./memory-experimentation.md) for details on the different approaches I'm testing, including an experimental custom memory bank and the official MCP memory server.

## Status

This area is very much in flux. With so many existing solutions and the promising simplicity of the quote-based approaches, I may pivot to adapting existing work rather than building from scratch. The key insight is that different types of context may need different retention strategies.

[Yehuda Katz]: https://www.linkedin.com/in/yehudakatz/
[Kari Wilhelm]: https://www.linkedin.com/in/kariwilhelm/
