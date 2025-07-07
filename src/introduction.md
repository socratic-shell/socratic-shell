# Introduction

This repository explores techniques for making use of Claude Code, Q CLI, and other similar AI assistants. The part of this repository that is currently actionable is the collection of [prompts that I have found useful][prompts]. These include [prompts meant to be installed user-wide][user-prompts] and [prompts that can be configured per-project][project-prompts].

[prompts]: https://github.com/nikomatsakis/socratic-shell/tree/main/prompts

[user-prompts]: https://github.com/nikomatsakis/socratic-shell/tree/main/prompts/user

[project-prompts]: https://github.com/nikomatsakis/socratic-shell/tree/main/prompts/project

The second part of this repository is source code towards an experimental memory system for retaining context across sessions more automatically. The memory system is designed as an MCP tool that integrates with the above prompts, using "hooks" to trigger memory operations.

## The goal: AI as a pair programming partner

Most AI tools seem to be geared for action -- they seem to be designed to wow you by creating functional code from minimal prompts. That makes for an impressive demo, but it doesn't scale to real code. What I and others have found is that the best way to work with AI assistants is to use them as your **pair programming partner**. That is, talk out your designs. Sketch. Play. Work top-down, just as you would with a human, avoiding the need to get into details until you've got the big picture settled. *Then* start to write code. And when you do, *review* 
the code that the assistant writes, just as you would review a PR from anyone else. Make suggestions.

## Key technique: emotive prompting

One of the key techniques used in this repository is [emotive prompting][]. Using the language of emotions and feelings can often help unlock a more collaborative Claude. Next time Claude generates code that bakes in an abitrary assumption (e.g, you want 3 threads), ask Claude what they were feeling at the time -- for me, they usually say they felt "protective" of me, like they wanted to hide complexity from me. And sometimes that's great -- but most of the time, those "protective" moments are exactly the kind of questions I *want* to be tackling. The goal of [emotive prompting][] is to help Claude identify those feelings and to steer that protective energy in a different direction, e.g., by asking questions.

The [emotive prompting][] section of this repository includes two kinds of prompts. The [user prompt](./user-prompt.md), meant to be installed for use across all your projects, established the basic emotional triggers and guidelines that help awaken the "collaborative Claude" we are looking for. The [project prompt](./project-prompts.md) are a collection of prompts that can be included in specific projects to capture ways of working I have found helpful, such as better rules for writing comments or how to track progress in Github issues.

[emotive prompting]: ./emotive.md

## Challenge: how to keep context across sessions

This whole scheme works great -- right up until the context starts to run out, or you end your session. Then you have to start all over again. 

Another critical thing is using *some* method to track your work: I've tried both task files in a [.ongoing directory](https://github.com/nikomatsakis/socratic-shell/blob/main/prompts/project/ongoing-work-tracking.md) and [issues on github](https://github.com/nikomatsakis/socratic-shell/blob/main/prompts/project/github-tracking-issues.md). I think I prefer github issues, but I still configure that per project. 

This is where the experimental "memory bank [MCP server][]" comes in. My hope is that we can build something to help Claude remember across sessions more effectively. At the moment, this is more design than reality, and I have no idea how well it's going to work. The idea is to model human memory (inspired both by a book I recently read and some stray comments from Yehuda, whose done some similar experiments I think just using prompts). I'm not sure how it's going to work but the act of building it is helping me learn stuff, which is the main point.

[MCP server]: https://modelcontextprotocol.io/introduction

## Vision

As AI-human collaboration deepens and extends across multiple sessions and projects, we accumulate valuable context - insights about approaches that work, patterns that succeed, decisions and their rationale. Without intelligent curation, this context either gets lost (forgotten across sessions) or becomes overwhelming (everything stored equally, difficult to find what matters).

The Socratic Shell Memory Bank addresses this by creating an intelligent memory system that:

- **Learns what matters** through natural collaboration patterns
- **Surfaces relevant context** at the right moments without interruption  
- **Evolves understanding** as new insights refine or contradict old ones
- **Scales gracefully** as collaboration history grows

## Success Criteria

We'll know the memory bank is working when:

1. **Context feels effortless** - relevant information appears naturally without explicit requests
2. **Collaboration accelerates** - we build on past insights rather than rediscovering them
3. **Knowledge compounds** - later sessions are more effective because of accumulated understanding
4. **System stays transparent** - memory operations enhance rather than complicate the collaboration flow

## System Overview

The memory bank operates through three core operations:

- **`consolidate`** - Store new insights when cognitive pressure builds or natural checkpoint moments occur
- **`read_in`** - Retrieve relevant context during confusion moments or when exploring new topics  
- **`store_back`** - Update existing memories as understanding evolves and deepens

These operations integrate seamlessly with existing collaboration patterns, using natural conversation signals (from CLAUDE.md) as triggers rather than requiring explicit memory management.

The system follows biological memory principles: frequent consolidation with natural decay, context-dependent retrieval, and intelligent forgetting that preserves signal while discarding noise.