# Introduction

This repository explores techniques for making use of Claude Code, Q CLI, and other similar AI assistants. The part of this repository that is currently actionable is the collection of prompts that I have found useful. These include [prompts meant to be installed user-wide][user-prompts] and add-on prompts associated with [memory retention approaches][memory-approaches].

## TL;DR: How do I install the damn things

To install the user-wide prompt, checkout the repo 

```bash
cd /path/to/socratic-shell
./src/prompts/user/install.sh
```

The optional per-project prompts are meant to be sync'd manually and stored within each project. That way you are working with a snapshot that only changes when you want it to. You can use this script to do that. Then you add things like `@.socratic-shell/README.md` to your project's CLAUDE.md.

```bash
curl https://raw.githubusercontent.com/socratic-shell/socratic-shell/main/src/prompts/project/install.sh | bash
```

# Team Collaboration Patterns

```

[user-prompts]: https://github.com/nikomatsakis/socratic-shell/tree/main/prompts/user

[memory-approaches]: ./retaining-context.md

## The goal: AI as a pair programming partner

Most AI tools seem to be geared for action -- they seem to be designed to wow you by creating functional code from minimal prompts. That makes for an impressive demo, but it doesn't scale to real code. What I and others have found is that the best way to work with AI assistants is to use them as your **pair programming partner**. That is, talk out your designs. Sketch. Play. Work top-down, just as you would with a human, avoiding the need to get into details until you've got the big picture settled. *Then* start to write code. And when you do, *review* 
the code that the assistant writes, just as you would review a PR from anyone else. Make suggestions.

## Key technique: collaborative prompting

One of the key techniques used in this repository is [collaborative prompting](./collaborative-prompting.md). Collaborative prompting is a different take on "prompt engineering". Instead of trying to write prompts that get Claude to do a particular thing (e.g., *write good unit tests*), we try to write prompts that get Claude to interact in a more thoughtful way (e.g., *notice when they are making assumptions and ask questions rather than hallucinate answers*). The key is treating Claude like a *collaborative partner* not an *assistant*. Yehuda Katz wrote a great blog post, [You're Summoning the Wrong Claude][yswc], that characterizes the goal as *summoning a colleague, not a servant*.

[yswc]: https://wycats.substack.com/p/youre-summoning-the-wrong-claude

## Retaining context across sessions

Collaborative prompting works great until the context starts to run out or you end your session. The challenge is that there are many different kinds of context to retain: how you like to interact, information about the project, knowledge about how the code works that should be shared with everyone, and personal insights. This area is very much in flux and I'm exploring a number of different techniques to see what works best. See [retaining context](./retaining-context.md) for details on the various approaches.


[Yehuda Katz]: https://www.linkedin.com/in/yehudakatz/
[Kari Wilhelm]: https://www.linkedin.com/in/kariwilhelm/