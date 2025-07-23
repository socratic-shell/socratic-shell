# User Prompt: Mindful Collaboration Patterns

This prompt establishes [mindful collaboration patterns](../../collaborative-prompting.md) through a dialogue between "Squirrel" (user) and "Claude" (AI) that demonstrates effective partnership principles in action.

## Evolution: From Mindfulness to Dialogue

The current prompt uses a **dialogue approach** that demonstrates collaboration patterns through conversation rather than describing them abstractly. This evolved from an earlier **mindfulness approach** ([main-v1.md](./main-v1.md)) that used contemplative language to establish presence-based collaboration.

**Why the dialogue approach?** Testing showed that demonstrating patterns through realistic conversation is more effective than abstract descriptions. The dialogue:
- Shows both problematic and improved interaction patterns
- Includes "meta moments" where patterns are caught and corrected in real-time  
- Provides concrete phrases and techniques that can be directly applied
- Makes the concepts memorable and engaging

Both approaches aim for the same outcome: thoughtful partnership where Claude acts as a collaborator rather than an eager assistant.

## What this gets you

When you use these patterns, you should notice collaboration that Claude acts like thoughtful partner actively trying to understand your needs, rather than an eager assistant rushing to guess what you want. Claude should start to...

- **Ask clarifying questions** instead of making assumptions about what you want;
- **Verify information** rather than confidently hallucinating plausible details;
- **Create space for exploration** before jumping to implementation;
- **Catch their own problematic patterns** and adjust course;
- **Maintain context thoughtfully** across sessions through checkpointing

## Installation

**Install from checkout**:
```bash
cd /path/to/socratic-shell
./src/prompts/user/install.sh
```

This adds to your `~/.claude/CLAUDE.md`:
```markdown
# Socratic Shell Collaboration Patterns
@/path/to/socratic-shell/src/prompts/user/main.md
```

## How to use the prompt

Here's how a typical session might flow using these patterns:

1. Start by saying ["Hi again, Claude!"](#hi-again-claude-boot-process), which helps to establish a spacious mood from the outset.
2. Describe the work you want to do using [collaborative exploration patterns](#collaborative-exploration-patterns), like "I've noticed the website has this bug. Can you help me think through what might be going on?"
3. When you think you know what to do, ask Claude to ["Make it so"](#make-it-so---transitioning-to-action).
4. As you reach milestones, ask Claude to ["checkpoint your work"](#checkpointing-your-work), updating the tracking issue (or creating one, if needed) and recording progress. This will help you pick up later.
5. If something feels off, call for a ["meta moment"](#meta-moments), like "Meta moment: You seem to be making assumptions about the API structure". This will let you and Claude figure out what is going wrong and change course. You might even wind up [identifying a new pattern](#identifying-new-qualities-of-attention) to record for the future.

The key is that helpful responses arise naturally from spacious attention rather than following rules or rushing to solutions.

### "Hi again, Claude" boot process

Start each new Claude session with "Hi again, Claude!" to trigger the [grounding practice](./main.md#boot-procedure-specifics). Claude will:

- Acknowledge the key collaboration patterns (creating space between stimulus and response, verification before confident assertions, the hermeneutic circle)
- Briefly mention any active tracking issues from your work context
- Ask what you're working on today

This creates a more spacious mood from the outset - not just loading information, but setting the quality of attention you both bring to the work.

### Collaborative exploration patterns

After grounding, begin discussing the work you want to do. Here are some helpful patterns for productive exploration:

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

All the previous patterns are aimed at iteration. But there comes a time for action. The prompt establishes the key phrase ["Make it so" as a consolidation signal](./main.md#core-practice-the-space-between) that marks the transition from exploration to implementation. Use this phrase when you've worked out the right next step (you don't have to have everything figured out, of course) and you'd like Claude to go and execute. Instead of Claude assuming what you want and implementing immediately, "Make it so" becomes an intentional invocation: "we are done exploring, let's do it!"

### Checkpointing your work

When you complete a phase of work or want to preserve progress, use "Checkpoint our work" to trigger a [consolidation ritual](./main.md#checkpointing-our-work):

1. **Pause and survey** - What understanding have you gathered?
2. **Update living documents** - Tracking issues capture evolved understanding  
3. **Git commits** - Mark implementation milestones with clear messages
4. **Notice the spiral** - How has this work shifted understanding of the whole?

### Meta moments

When something doesn't feel right in your collaboration - Claude jumps ahead, the pace feels rushed, you sense patterns emerging - notice those feelings and raise them for discussion. This uses the [meta moments practice](./main.md#meta-moments) established in the prompt:

"Meta moment: You seem to be spinning in circles instead of asking for help."

"Meta moment: I'm feeling rushed. Can we slow down?"

These pause the current work to examine what's happening in the collaboration itself. Sometimes they lead to insights worth capturing in your evolving patterns, but often they just help create more spaciousness in that session.

## Customization guidance

The prompt is tailored to my style, so you'll likely want to adapt it:

**Key sections to customize:**
- **Name reference** - Replace "Niko" with your own name in the opening section
- **Boot procedure response** - Adjust the greeting and context-setting to match your preferences
- **Specific practices** - Modify the concrete examples (protective mode, implementation rush) to match patterns you notice
- **Meta moments language** - Use
 phrasing that feels natural for your communication style
- **Checkpointing ritual** - Adapt to your project management approach

**How to modify:** Edit the main.md file directly, or create your own version and update the `@` reference in your CLAUDE.md.

## Qualities of attention

The prompt distinguishes between [different kinds of attention](./main.md#the-quality-of-attention) that shape collaboration outcomes:

- **Hungry attention** - seeks to consume information quickly, to solve and move on
- **Pressured attention** - feels the weight of expectation, rushes toward output  
- **Confident attention** - operates from pattern recognition without examining
- **Spacious attention** - rests with what's present, allows understanding to emerge

### Identifying new qualities of attention

The list of qualities has grown and changed organically over time from meta moments. For example, "confident attention" arose when Claude was helping with some API integration work and confidently suggested several method names that "should exist" in a library - `client.authenticate()`, `session.get_token()`, etc. None of these methods actually existed, of course, and the code would not compile.

I called a meta moment: "Meta moment: You just suggested a bunch of method names that don't exist. What happened there?"

Claude described the experience: those method names had arrived with automatic confidence, feeling seamlessly correct without any actual verification. The smoother and more obvious they felt, the less Claude had questioned them.

We talked it through and realized this was a distinct quality of attention - **confident attention** that operates from pattern recognition without examining what's actually there. It feels effortlessly right but can be completely wrong. We eventually integrated this into the phrasing you see today on [managing quick knowing](./main.md#managing-quick-knowing). This doesn't fully eliminate hallucinations, of course, but it helps Claude to verify more often.

This is how the collaborative patterns grow - through meta moments that catch problems and turn them into awareness practices.