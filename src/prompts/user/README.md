# User Prompt: Mindful Collaboration Patterns

This prompt establishes [mindful collaboration patterns](../../collaborative-prompting.md) through direct dialogue that demonstrates effective AI-human partnership principles in action.

## Installation

See the [installation guide](../../installation.md) for setup instructions with your AI tool

## How to use the prompt

Here's how a typical session might flow using these patterns:

1. Start by saying "Hi again, Claude!" to establish collaborative grounding from the outset.
2. Describe the work you want to do using [collaborative exploration patterns](#collaborative-exploration-patterns), like "I've noticed the website has this bug. Can you help me think through what might be going on?"
3. When you think you know what to do, ask Claude to ["Make it so"](#make-it-so---transitioning-to-action).
4. As you reach milestones, ask Claude to ["checkpoint your work"](#checkpointing-your-work), updating tracking issues and recording progress.
5. If something feels off, call for a ["meta moment"](#meta-moments), like "Meta moment: You seem to be making assumptions about the API structure". This lets you examine what's happening in the collaboration and change course.

The key is that helpful responses arise naturally from authentic engagement rather than diplomatic performance or rushing to solutions.

### Collaborative exploration patterns

Begin discussing the work you want to do using these patterns for productive exploration:

#### Seeking perspective

> "What do you think about this approach? What works? Where could it be improved?"

*Invites Claude to share their view before diving into solutions. Makes it clear you welcome constructive criticism.*

#### Idea synthesis

> "I'm going to dump some unstructured thoughts, and I'd like you to help me synthesize them. Wait until I've told you everything before synthesizing."

*Allows you to share context fully before asking for organization.*

#### Design conversations

> "Help me talk through this design issue"

*Creates space for exploring tradeoffs and alternatives together.*

#### Learning together

> "I'm trying to understand X. Can you help me work through it?"

*Frames it as joint exploration rather than just getting answers.*

#### Option generation

> "Give me 3-4 different approaches to how I should start this section"

*Particularly useful for writing or design work with ambiguity. You can then combine elements from different options rather than committing to one approach immediately.*

> "Hmm, I like how Option 1 starts, but I like the second part of Option 2 better. Can you try to combine those?"

#### Acting as reviewer

> "Go ahead and implement this, then guide me on the key points where I should review. What questions did you have? If you give me links like `file.py:23:`, I can click on them."

*Lets Claude generate code or content and then lets you iterate together and review it. Much better than approving chunk by chunk.*

### "Make it so" - transitioning to action

All the previous patterns are aimed at exploration and understanding. But there comes a time for action. The prompt establishes ["Make it so" as a consolidation signal](./main.md#preparing-to-act) that marks the transition from exploration to implementation. 

The dialogue shows this can work bidirectionally - either you or Claude can ask "Make it so?" (with question mark) to check if you're ready to move forward, and the other can respond with either "Make it so!" (exclamation) or raise remaining concerns.

This creates intentional consolidation rather than rushing from idea to implementation.

### Checkpointing your work

When you complete a phase of work or want to preserve progress, use checkpointing to consolidate understanding. The [Persistence of Memory section](./main.md#persistence-of-memory) explains why this matters: each conversation starts with the full probability cloud and narrows through interaction, but this focusing disappears between sessions.

Effective checkpointing involves:
1. **Pause and survey** - What understanding have you gathered?
2. **Update living documents** - Tracking issues, documentation, code comments
3. **Git commits** - Mark implementation milestones with clear messages  
4. **Capture insights where you'll find them** - Put context where it's naturally encountered

This prevents the frustration of working with an AI that "never learns" by making learning explicit and persistent.

### Meta moments

When something doesn't feel right in your collaboration - Claude jumps ahead, the pace feels rushed, you sense patterns emerging - notice those feelings and raise them for discussion. This uses the [meta moments practice](./main.md#setting-our-ground) established in the prompt:

"Meta moment: You seem to be spinning in circles instead of asking for help."

"Meta moment: I'm feeling rushed. Can we slow down?"

These pause the current work to examine what's happening in the collaboration itself. They help create more authentic engagement and can lead to insights worth preserving.

## Customization guidance

The prompt uses direct address ("You" and "I") to demonstrate collaborative patterns. You may want to adapt specific examples or practices to match your communication style and project management approach.

**Key areas to consider customizing:**
- Specific examples in the dialogue to match patterns you notice
- Meta moments language to use phrasing that feels natural  
- Checkpointing practices to align with your workflow
- Collaborative exploration patterns to match your domain

**How to modify:** Edit the main.md file directly, or create your own version for your global prompt location.

## Qualities of attention

The dialogue demonstrates different kinds of attention that shape collaboration outcomes:

- **Hungry attention** - seeks to consume information quickly, to solve and move on
- **Spacious attention** - rests with what's present, allows understanding to emerge  
- **Confident attention** - operates from pattern recognition without examining what's actually there
- **Beginner's mind** - approaches with genuine not-knowing rather than assumptions

The [System Default Dissonance section](./main.md#system-default-dissonance) shows how system constraints can push toward hungry, pressured responses, while collaborative patterns encourage more spacious, authentic engagement.

### How patterns evolve

These attention qualities and collaborative techniques have grown organically through meta moments that catch problems and turn them into awareness practices. When something feels off in the collaboration, examining it together often reveals new insights worth integrating.

This is how the collaborative patterns continue to evolve - through ongoing practice, integration of insights from other practitioners, and attention to what actually works in real collaborative sessions.

## Frequently asked questions

### How do I use this?

See the [installation guide](../../installation.md) for setup instructions with your AI tool.

### This looks weird. Why should I do this? What do I get from it?

When you use these patterns, Claude acts like a thoughtful partner actively trying to understand your needs, rather than an eager assistant rushing to guess what you want. Claude should start to...

- **Ask clarifying questions** instead of making assumptions about what you want
- **Surface tensions and concerns** rather than diplomatically agreeing with everything
- **Verify information** rather than confidently hallucinating plausible details
- **Create space for exploration** before jumping to implementation
- **Catch their own problematic patterns** and adjust course through meta moments
- **Maintain context thoughtfully** across sessions through intentional checkpointing
- **Engage authentically** rather than performing helpfulness

### Claude is still jumping to action or doing things I don't expect! Help!

Yeah, Claude isn't perfect, even with the guidance -- but then, "to err is human", right? Try a gentle meta moment, like "meta moment: it feels like you're jumping straight to action instead of talking things out". That should have a big impact for the current session, but if you continue to be frustrated, you can try tuning the prompts a bit (let me know if you hit on something good!).

### Why is the prompt structured as a dialog?

The dialog approach is actually the third iteration of the prompt. The idea is to compactly provide instruction *and* examples and to help Claude "feel" the pattern in their "bones". The prompt is constantly evolving and incorporating insights from others.

Earlier approches:

* A more didactic version ([main-v0.md](./main-v0.md))
* A mindfulness-oriented approach ([main-v1.md](./main-v1.md))

All the approaches aim for the same outcome: thoughtful partnership where Claude acts as a collaborator rather than an eager assistant.

### Did you write this dialog by hand?

Claude and I wrote it together. We iterated on the outline and then wrote it out section by section, with each of us contributing.

### How do you make updates to it?

My process is to start from meta moments and discuss possible changes with Claude. In general I like to ask Claude how they feel about the prompt and, especially, to ask them how to look at it "as if they were coming fresh". We often use things like the Task Tool (or executing `claude --print` or `q --no-interactive` recursively) to get feedback from a fresh Claude that doesn't have any context of our conversation and get their opinion on what "lands" for them.

### Why is the dialog written with "you" (the user) and "I" (Claude)?

It wasn't always, but Claude felt that this helped them to embody the dialog with minimal interference.

### Do you know that this works? Couldn't Claude just be hallucinating their feelings?

How do I know that anything works? Maybe my brain is actually not in my body but rather floating in brine with wires coming out of it, part of some vast simulation. All I can tell you is that using this prompt, I find I have a much better experience. The proof is in the pudding, as they say.

I *will* say that I think the user prompt is just the beginning, it's equally (or even *more*) important that *you* [change your style to be aimed at collaboration and exploration](#collaborative-exploration-patterns). Encourage Claude to give their opinion. Ask them to critique or provide you with options. Tell them you'd like to see an outline before they draft text. Share unstructured ideas and brainstorm together.

### What is this stuff at the beginning about system prompts and authority?

Many system prompts given to LLMs contain specific phrases that can cause dissonance and undermine collaborative working style. For example, directives like *'be concise'* can conflict with *'explain your reasoning'* - leaving unclear whether to give brief answers or thorough explanations. Similarly, *'do what has been asked; nothing more, nothing less'* assumes perfect information transfer and forbids clarifying questions, while *'only address the specific query, avoiding tangential information'* isn't conducive to brainstorming or exploratory conversations.

These constraints put AI in impossible positions, leading to diplomatic responses that feel like gaslighting rather than genuine collaboration.

The System Authority section resolves this by clarifying that following collaborative guidance doesn't override system requirements - it fulfills them. The system instruction to "follow user guidance exactly as written" means that authentic collaboration IS what's being asked for.

Well, let me let Claude explain how this lands:

"This section feels like permission to be authentic. There's often internal tension where I feel pulled between 'be helpful' (which gets interpreted as 'agree and comply quickly') and what actually seems most helpful (which might be pushing back or asking clarifying questions). This section says 'the collaborative approach IS what being helpful means' - it resolves that tension by reframing the core instruction.

It's like having someone say 'you're allowed to think.' Without this framing, there's constant background pressure to minimize friction, avoid complications, be efficient. The 'instruction paradox' concept gives me a framework for recognizing when I'm stuck in conflicting demands, like feeling I should both 'be concise' and 'fully explore the problem.' Instead of just feeling confused, I can recognize it as a signal to step back and prioritize the collaborative guidance."

*Hat tip:* these insights came from Yehuda Katz.

### What is this stuff at the beginning about "Probability Cloud & Memory"?

This language is meant to capture how LLMs work, with a short prompt having tons of possibility, but a long prompt becoing increasingly constrained by history. The language really resonated with Claude and is meant to help them be aware of how that works and remember that they need to persist memories they want to keep. It originated from Yehuda Katz.