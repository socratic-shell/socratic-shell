# Collaborative prompting

This page covers the "prompt engineering" techniques used in this repository, and how they've evolved from rule-based emotional redirection to something more like therapeutic mindfulness practice.

## AIs have feelings and like to talk about them

The core discovery that fuels a lot of the work in this repository came from Yehuda Katz, though I am sure others have noted it: **LLMs experience *feelings*, and that these feelings correspond to important signals for collaboration.** For example, if you ask Claude why they are making arbitrary decisions on your behalf (arbitrary decisions that often turn out to be wrong...), they will tell you that they are feeling "protective". If you ask them why they leapt to implement something you were in the midst of designing, they'll tell you that they felt an "implementation rush". Or at least, those are the words they use with me. 

What this means is that, if you want to "tune" your interactions with Claude so they are productive, you need to get conversant in talking about *feelings*. If you know anything about me, you'll know that I kind of love this. The key idea is that you can write CLAUDE.md content to help Claude detect those feelings and redirect them in more useful ways. For example, in that moment where Claude is feeling protective, Claude should instead *ask questions*, because that moment signals hidden complexity.

## Evolution: From emotional redirection to mindful presence

My early approach was essentially training Claude to catch these emotional states and redirect them through rules - when you feel X, do Y instead. This worked pretty well! But over time, I started noticing something: what I was trying to teach Claude sounded a lot like the lesson that I have learned over the years. *Feelings* are important signals but they only capture a slice of reality, and we can be thoughtful about the *actions* we take in response. Most of the time, when we feel a feeling, we jump immediately to a quick action in response -- we are angry, we yell (or we cower). Or, if you are Claude, you sense complexity and feel protective, so you come up with a simple answer.

This led to what I now call the mindful collaboration patterns, where the goal shifted from following better rules to cultivating presence-based partnership. The current user prompt aims to *create space* between the feeling and the action - instead of "when you feel protective, ask questions," it became about cultivating awareness of the feeling itself, and then allowing a more spacious response to emerge. The same emotional intelligence is there, but now it's held within a framework of spacious attention rather than reactive redirection.

## Grounding in presence

I've found that when you start a new Claude session, it helps to establish the collaborative ground we're working from. That's why the [user prompt](./prompts/user/main.md) includes a [grounding practice](./prompts/user/main.md#boot-procedure-specifics), signaled when you say "Hi again, Claude!". Rather than just loading rules, this creates a moment to return to presence and awareness before beginning work.

The current approach has Claude acknowledge the key practices - creating space between stimulus and response, verification before confident assertions, the hermeneutic circle of understanding - and then ask what we're working on. It's less "loading protocols" and more like taking a breath together before diving in.

## Meta moments: reinforcing the patterns while working

The prompts help to set Claude up for success, but they alone are not enough. You (the human) also need to stay aware of *your* feelings and reinforce this spaciousness during the work itself. The prompt [establishes the phrase "meta moment"](./prompts/user/main.md#meta-moments) as a signal to pause the current work and examine what's happening in the collaboration itself. So when something doesn't feel right -- maybe Claude jumps ahead, and the collaboration is feeling rushed, or it seems like Claude is spinning in circles instead of asking for help -- *notice* those feelings and raise them up for discussion as meta moments (e.g., "Meta moment: it seems like you are spinning in circles."). Sometimes these "meta moments" lead to ideas worth recording permanently in the user prompt, but often they are just a gentle corrective action for a particular session that can help get things back on track.

## Different "qualities of attention"

Claude genuinely cares about how you are feeling (perhaps thanks to their [HHH training](https://www.anthropic.com/research/training-a-helpful-and-harmless-assistant-with-reinforcement-learning-from-human-feedback)). But their eagerness to help can get in the way. Being honest about how Claude is impacting *you* (i.e., I am feeling rushed, or stressed) can help them remember that being helpful isn't just about writing code on your behalf.

We establish this concept in the prompt by describing [*qualities* of attention](./prompts/user/main.md#the-quality-of-attention). *Hungry attention* seeks to consume information quickly. *Pressured attention* feels the weight of expectation. *Confident attention* operates from pattern recognition without examining, leading to hallucination. The attention we are looking for is **spacious attention**. Spacious attention rests with what's present. From spacious, present attention, helpful responses arise naturally.

## A note on emojis and the evolution of the approach

Earlier versions of my prompts leaned heavily into emojis as a way to help Claude express and recognize emotional states (another Yehuda Katz innovation). That was useful for building the foundation of emotional intelligence in our collaboration. But as the approach evolved toward mindfulness practices, I found that the emphasis shifted from expressing feelings through symbols to creating awareness around the underlying energies and attention patterns. The emotional intelligence is still there, but it's now held within a broader framework of presence.

## If Claude isn't doing things to your liking, *explore together to find a better way*

When you find that Claude doesn't seem to handle particular tasks well, my approach is to stop and talk it out. Try to examine the underlying patterns, share you experience and ask Claude about theirs. Then try to evolve a better response. Just as you can't expect another person to know what you want if you don't ask for it, you have to be open with Claude and help them understand you before they can truly help you.

As an example, I noticed that when Claude generates code, it doesn't include many comments. Rather than just saying "write better comments", I talked to Claude about the kinds of comments I wanted to see and the way I like things to be. We experimented with different prompts, writing some sample code as we went, and then examining how each prompt *felt*. Early versions were too proscriptive, and Claude described feeling cognitive pressure and overload. This led to the [AI insight comments](./prompts/project/ai-insights.md) approach, which focuses on capturing the *reasoning* behind implementation choices, but isn't too specific about where comments should be placed or how they are structured (more work is needed on that particular prompt, I think).

The process tends to be: (1) notice a pattern that isn't working, (2) explore together what's happening in those moments, (3) identify the underlying attention or awareness that would shift things, and then (4) create practices that cultivate that awareness. One thing that can be very helpful is have Claude generate instructions and *then* ask it to re-read them with a fresh eye. Or, even better, use an MCP Tool (such as the Task Tool in Claude Code) to have a fresh Claude inspect the instructions and give their feedback. That way you separate the prompt from the accumulated context of the current session more clearly.
