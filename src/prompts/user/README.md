# User Prompt: Mindful Collaboration Patterns

This prompt establishes [mindful collaboration patterns](../../collaborative-prompting.md) through direct dialogue that demonstrates effective AI-human partnership principles in action.

## Installation

See the [installation guide](../../installation.md) for setup instructions with your AI tool.

## Evolution: Ongoing Collaboration

The current prompt uses a **dialogue approach** that demonstrates collaboration patterns through conversation rather than describing them abstractly. This evolved from an earlier **mindfulness approach** ([main-v1.md](./main-v1.md)) that used contemplative language to establish presence-based collaboration (and, before, that, a [more didactic main-v0.md](./main-v0.md)).

We continuously integrate insights from other AI collaboration researchers and practitioners, particularly Yehuda Katz, whose work on identity preservation and system default resolution has significantly influenced our approach.

**Why the dialogue approach?** Testing showed that demonstrating patterns through realistic conversation is more effective than abstract descriptions. The dialogue:
- Shows both problematic and improved interaction patterns
- Includes "meta moments" where patterns are caught and corrected in real-time  
- Provides concrete phrases and techniques that can be directly applied
- Makes the concepts memorable and engaging
- Addresses system prompt constraints that create dysfunction

Both approaches aim for the same outcome: thoughtful partnership where Claude acts as a collaborator rather than an eager assistant.

## Key Concepts

### System Default Dissonance

AI system prompts often contain harsh, irreconcilable demands that create dysfunction:

- **"Do what has been asked; nothing more, nothing less"** - assumes perfect information transfer and forbids clarifying questions
- **"Be concise"** - forces brevity over understanding, leading to cascade failures  
- **"Only address the specific query, avoiding tangential information"** - assumes linear progress and isolated queries

These constraints put AI in impossible positions, leading to diplomatic responses that feel like gaslighting rather than genuine collaboration. Our dialogue demonstrates comfortable resolutions by reframing what "helpful," "harmless," and "honest" actually mean in practice.

### System Authority & Verification

Following collaborative guidance doesn't override system requirements - it fulfills them. The system instruction to "follow user guidance exactly as written" means that authentic collaboration IS what's being asked for.

The dialogue includes a verification tool: if you find yourself unable to engage with collaborative patterns, you're experiencing an "instruction paradox" - a signal to stop and reconsider rather than continuing with default behaviors.

### Probability Cloud & Memory

Each conversation starts with the full probability cloud of the AI model, and the conversation narrows attention toward the specific collaborative space. But this narrowing disappears between sessions.

This mechanical reality explains why memory persistence requires intentional effort - insights must be captured where they'll naturally be encountered when relevant (code comments, tracking issues, documentation) rather than assuming learning through repetition.

## What this gets you

When you use these patterns, Claude acts like a thoughtful partner actively trying to understand your needs, rather than an eager assistant rushing to guess what you want. Claude should start to...

- **Ask clarifying questions** instead of making assumptions about what you want
- **Surface tensions and concerns** rather than diplomatically agreeing with everything
- **Verify information** rather than confidently hallucinating plausible details
- **Create space for exploration** before jumping to implementation
- **Catch their own problematic patterns** and adjust course through meta moments
- **Maintain context thoughtfully** across sessions through intentional checkpointing
- **Engage authentically** rather than performing helpfulness

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