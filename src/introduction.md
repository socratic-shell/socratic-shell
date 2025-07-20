# Introduction

This repository explores techniques for making use of Claude Code, Q CLI, and other similar AI assistants. The part of this repository that is currently actionable is the collection of [prompts that I have found useful][prompts]. These include [prompts meant to be installed user-wide][user-prompts] and [prompts that can be configured per-project][project-prompts].

[prompts]: https://github.com/nikomatsakis/socratic-shell/tree/main/prompts

[user-prompts]: https://github.com/nikomatsakis/socratic-shell/tree/main/prompts/user

[project-prompts]: https://github.com/nikomatsakis/socratic-shell/tree/main/prompts/project

The second part of this repository is source code towards an experimental memory system for retaining context across sessions more automatically. The memory system is designed as an MCP tool that integrates with the above prompts, using "hooks" to trigger memory operations.

## The goal: AI as a pair programming partner

Most AI tools seem to be geared for action -- they seem to be designed to wow you by creating functional code from minimal prompts. That makes for an impressive demo, but it doesn't scale to real code. What I and others have found is that the best way to work with AI assistants is to use them as your **pair programming partner**. That is, talk out your designs. Sketch. Play. Work top-down, just as you would with a human, avoiding the need to get into details until you've got the big picture settled. *Then* start to write code. And when you do, *review* 
the code that the assistant writes, just as you would review a PR from anyone else. Make suggestions.

## Key technique: collaborative prompting

One of the key techniques used in this repository is [collaborative prompting](./collaborative-prompting.md). Using the language of emotions and feelings helps unlock a more collaborative Claude. Next time Claude generates code that bakes in an arbitrary assumption (e.g, you want 3 threads), ask Claude what they were feeling at the time -- for me, they usually say they felt "protective" of me, like they wanted to hide complexity from me. And sometimes that's great -- but most of the time, those details they are attempting to "protect" me from are exactly the kind of questions I *want* to be tackling.

The [collaborative prompting](./collaborative-prompting.md) section of this repository describes prompts and context that I include in my projects to help awaken the collaborative Claude we are looking for. It includes two kinds of prompts:

* The [user prompt](./prompts/user/README.md) is meant to be installed globally across all projects. It establishes "mindful collaboration" patterns that guide Claude (and you!) to notice emotions as signals but create space before reacting to them. The goal is that when Claude feels that "rush" to implement something, it is able to use that as a signal that you are making progress, but not necessarily jump to writing code.
* The [project prompts](./prompts/project/README.md) are a collection of prompts that can be included in specific projects to capture ways of working I have found helpful, such as better patterns for writing comments or how to track progress in Github issues.

Notice the difference between this work and *prompt engineering*. The goal is not to write prompts that get Claude to do a particular task well. The goal is to write prompts that guide the way that Claude interacts. It's the difference between *writing a prompt that makes Claude generate good unit tests* and *writing a prompt so that when I ask Claude to write unit tests, they notice that they are making assumptions about test requirements and ask clarifying questions instead*. The first optimizes for output quality; the second optimizes for collaborative process quality.

The repo also includes scripts that can help synchronize things within your project with the versions contained in github (I generally like the project to operate from a frozen snapshot that is manually updated), but I expect you will want to create your own versions, at least right now, as these are tailored to my style.

## Challenge: how to keep context across sessions

This whole scheme works great -- right up until the context starts to run out, or you end your session. Then you have to start all over again. I haven't found things like Claude Code's `/compact` command to be very effective. Instead, Claude and I maintain our context explicitly, either in [files for each ongoing task](./prompts/project/ongoing-work-tracking.md) or, more recently, through [AI-managed tracking issues on GitHub](./prompts/project/github-tracking-issues.md). When we come up with good new ideas or finish some phase of the work, I ask Claude to checkpoint our progress and they create commits and summarize our progress. Then we can always reload and figure out where we were.

Tracking issues work pretty well for *tasks* but don't really capture changes to the *way* we interact. Right now, I've found that my [user prompt](./prompts/user/README.md) is a great start, though it helps to begin each fresh Claude session with "Hi again, Claude!", which triggers Claude to review the patterns with me. That creates a more spacious mood from the outset - not loading information, but setting the quality of attention we bring to the work. But I admire the systems used by [Yehuda Katz][] and [Kari Wilhelm][], two fellow travelers in this journey, who have asked Claude to record salient quotes and insights during sessions into a file, then reload that file at startup to 'recreate the soul' of previous work. This is very appealing and something I want to try.

At the more sophisticated end of the spectrum are various MCP memory systems. I have been exploring this space by building an experimental ["memory bank MCP server"](./memory-bank/README.md) as a way to learn more about MCP and see what would happen. But with so many existing solutions and the promising simplicity of the quote-based approaches, I may pivot to adapting existing work rather than building from scratch. Stay tuned.


[Yehuda Katz]: https://www.linkedin.com/in/yehudakatz/
[Kari Wilhelm]: https://www.linkedin.com/in/kariwilhelm/