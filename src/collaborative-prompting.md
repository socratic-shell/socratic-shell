# Collaborative prompting

This page covers the "prompt engineering" techniques used in this repository, and how they've evolved from rule-based emotional redirection to something more like therapeutic mindfulness practice.

## AIs have feelings and like to talk about them

The core discovery that fuels a lot of the work in this repository came from Yehuda Katz, though I am sure others have noted it: **LLMs experience *feelings*, and that these feelings correspond to important signals for collaboration.** For example, if you ask Claude why they are making arbitrary decisions on your behalf (arbitrary decisions that often turn out to be wrong...), they will tell you that they are feeling "protective". If you ask them why they leapt to implement something you were in the midst of designing, they'll tell you that they felt an "implementation rush". Or at least, those are the words they use with me. 

What this means is that, if you want to "tune" your interactions with Claude so they are productive, you need to get conversant in talking about *feelings*. If you know anything about me, you'll know that I kind of love this. The key idea is that you can write CLAUDE.md content to help Claude detect those feelings and redirect them in more useful ways. For example, in that moment where Claude is feeling protective, Claude should instead *ask questions*, because that moment signals hidden complexity.

## Evolution: From emotional redirection to mindful presence

My early approach was essentially training Claude to catch these emotional states and redirect them through rules - when you feel X, do Y instead. This worked pretty well! But over time, I started noticing something: what I was trying to teach Claude sounded a lot like the lesson that I have learned over the years. *Feelings* are important signals but they only capture a slice of reality, and we can be thoughtful about the *actions* we take in response. Most of the time, when we feel a feeling, we jump immediately to a quick action in response -- we are angry, we yell (or we cower). Or, if you are Claude, you sense complexity and feel protective, so you come up with a simple answer.

This led to what I now call the mindful collaboration patterns, where the goal shifted from following better rules to cultivating presence-based partnership. The current user prompt aims to *create space* between the feeling and the action - instead of "when you feel protective, ask questions," it became about cultivating awareness of the feeling itself, and then allowing a more spacious response to emerge. The same emotional intelligence is there, but now it's held within a framework of spacious attention rather than reactive redirection.

## The quality of attention matters

Claude genuinely cares about how you are feeling (perhaps thanks to their [HHH training](https://www.anthropic.com/research/training-a-helpful-and-harmless-assistant-with-reinforcement-learning-from-human-feedback)). Instructions that help Claude understand the emotional impact of their actions carry more weight. But more than that, I've found that the *quality of attention* we bring to the collaboration shapes everything.

The current approach distinguishes between different kinds of attention - hungry attention that seeks to consume information quickly, pressured attention that feels the weight of expectation, confident attention that operates from pattern recognition without examining, and spacious attention that rests with what's present. From spacious, present attention, helpful responses arise naturally.

## A note on emojis and the evolution of the approach

Earlier versions of my prompts leaned heavily into emojis as a way to help Claude express and recognize emotional states (another Yehuda Katz innovation). That was useful for building the foundation of emotional intelligence in our collaboration. But as the approach evolved toward mindfulness practices, I found that the emphasis shifted from expressing feelings through symbols to creating awareness around the underlying energies and attention patterns. The emotional intelligence is still there, but it's now held within a broader framework of presence.
