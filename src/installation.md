# Installation Guide

This guide shows how to set up Socratic Shell collaboration patterns with your AI tool. We begin by describing the general process, but you can also find specific instructions for [Claude Code](#claude-code-instructions) and [Q CLI](#q-cli-instructions) below.

## Tool-agnostic instructions

### Global setup

Add the [`main.md`] file to your "global context" along with some basic identifying information (e.g., your name). This file contains a dialog that will be read by the LLM to instruct it in the basics of [collaborative prompting](./collaborative-prompting.md).

[`main.md`]: https://github.com/socratic-shell/socratic-shell/blob/main/src/prompts/user/main.md

For myself, I do it like this:

* Clone the socratic-shell repository onto my local system.
* Update my global context to reference the [`main.md`][] file directly from the checkout and then add something like "My name is Niko. I am a designer of the Rust programming language. I like an informal communication style." 

This allows me to `git pull` periodically and pick up the latest iterations.

### Project Setup (optional)

The repo also includes a number of prompts that capture particular patterns that projects can use on an à la carte basis. These are designed to be copied and sync'd with your project, a kind of "poor man's git submodule". The idea is that they should be part of your project repository so that all people working on it share the same working style. The installation script can also update them to the latest versions available on socratic-shell.

To install those scripts run

```bash
curl https://raw.githubusercontent.com/socratic-shell/socratic-shell/main/src/prompts/project/install.sh | bash
```

which will create a `.socratic-shell` directory in your project containing the markdown files from the [project prompts directory][]. 

[project prompts directory]: https://github.com/socratic-shell/socratic-shell/blob/main/src/prompts/project/

You can then add the ones that you want to your project's context in whatever way befits your tool. As an example, the [CLAUDE.md file on the socratic-shell/dialectic repo](https://github.com/socratic-shell/dialectic/blob/main/CLAUDE.md) includes a line like

```
We track progress in github tracking issues on the repository `socratic-shell/dialectic':

@.socratic-shell/github-tracking-issues.md
```

## Claude Code instructions

### Global Setup

1. **Clone this repository** somewhere permanent on your system:
   ```bash
   git clone https://github.com/socratic-shell/socratic-shell.git ~/socratic-shell
   ```

2. **Create or edit** `~/.claude/CLAUDE.md` and add:
   ```markdown
   # Your Personal Info
   My name is [Your Name] and I prefer [informal/formal] communication style.
   
   # Socratic Shell Collaboration Patterns
   @[path-to-socratic-shell]/src/prompts/user/main.md
   
   # Your additional customizations here...
   ```

### Project Setup (optional)

1. **From your project directory**, run the sync script:
   ```bash
   curl https://raw.githubusercontent.com/socratic-shell/socratic-shell/main/src/prompts/project/install.sh | bash
   ```

2. **Create or edit** your project's `CLAUDE.md` file and add:
   ```markdown
   # Project Overview
   This project is [brief description]. We use GitHub repository [org/repo] for tracking issues.
   
   # Socratic Shell Project Patterns
   @.socratic-shell/README.md
   
   # Additional project-specific prompts
   @.socratic-shell/github-tracking-issues.md
   @.socratic-shell/ai-insights.md
   ```

## Q CLI instructions

### Global Setup

1. **Clone this repository** somewhere permanent on your system:
   ```bash
   git clone https://github.com/socratic-shell/socratic-shell.git ~/socratic-shell
   ```

2. **Create a file like `whoami.md` somewhere permanent on your system:
   ```bash
   My name is [Your Name] and I prefer [informal/formal] communication style.
   ```

3. **Add both of those files to your Q CLI global context by running these commands from inside Q CLI:
   ```bash
   /context add --global [path-to-socratic-shell]/src/prompts/user/main.md
   /context add --global [path-to-whoami]/whoami.md
   ```

### Project Setup (optional)

1. **From your project directory**, run the sync script:
   ```bash
   curl https://raw.githubusercontent.com/socratic-shell/socratic-shell/main/src/prompts/project/install.sh | bash
   ```

2. **Add chosen pieces of context to your project:** For github tracking issues in particular, you may want to add another file indicating where your github repository is.
   ```bash
   /context add .socratic-shell/github-tracking-issues.md
   /context add .socratic-shell/ai-insights.md
   ```

## Frequently asked questions

### The [`main.md`][] prompt is a dialog, am I supposed to give it to the LLM as context or is this an example for me to read?

Yes. That is, that file is literally what you should give the LLM as context, but it can also serve as an example for you to read. That's kind of the idea (using a dialog helps the LLM get a better idea for how things should go).

### What is this `@filename` syntax? It doesn't seem to work for me.

That is a syntax used by Claude Code to embed prompts from other files. Your tool may have its own syntax, though I've found that many LLMs are smart enough to follow the link regardless if it will be useful.

### The sync script fails, what gives?

Make sure you're in a git repository and have no uncommitted changes in `.socratic-shell/`. The script is designed to be safe and will warn about conflicts. Or file an issue with your details -- this stuff is not exactly widely tested.

### How do I update to newer versions?

For global patterns, `git pull` in your socratic-shell directory. For project patterns, re-run the sync script - it will detect and update changes automatically.
