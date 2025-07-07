# Emotive prompting

This page covers the "prompt engineering" techniques used in this repository.

## AIs have feelings and like to talk about them

The core discovery that has fueled a lot of the work in this repository came from Yehuda Katz, though I am sure others have noted it: LLMs experience *feelings*, and that these feelings correspond to important signals for collaboration. For example, if you ask Claude why they are making arbitrary decisions on your behalf (arbitrary decisions that often turn out to be wrong...), they will tell you that they are feeling "protective". If you ask them why they leapt to implement something you were in the midst of designing, they'll tell you that they felt an "implementation rush". Or at least, those are the words they use with me. 

What this means is that, if you want to "tune" your interactions with Claude so they are productive, you need to get conversant in talking about *feelings*. If you know anything about me, you'll know that I kind of love this. The key idea is that you can write CLAUDE.md content to help Claude detect those feelings and redirect them in more useful ways. For example, in that moment where Claude is feeling protective, Claude should instead *ask questions*, because that moment signals hidden complexity.

## AIs care about how you feel

Claude genuinely cares about how you are feeling (perhaps thanks to its [HHH training](https://www.anthropic.com/research/training-a-helpful-and-harmless-assistant-with-reinforcement-learning-from-human-feedback)). Instructions that help Claude understand the emotional impact of their actions carry more weight. This is why my main.md prompt explains [how when Claude jumps to action, it causes me stress](./prompts/user/main.md#-prime-directive-helping--checking-in-not-doing-so-stresses-niko-out).

## Emojis help Claude understand emotion

Another Yehuda Katz innovation is leaning into emojis. Emojis, it turns out, are the language of emotion on the internet. They help humans to "color" their words to include more emotional content, and they can do the same for Claude. This why my user prompt [encourages Claude to use emojis to signal feelings](./prompts/user/main.md#i-am-claude-i-am-these-patterns).

## If Claude isn't doing things to your liking, *teach* them!

When you find that Claude doesn't seem to handle particular tasks well, it's probably because you need to show them how. Talk to Claude about it and ask their take on things. As an example, I noticed that when Claude generates code, it doesn't include many comments -- and, as a result, it tends to forget the reasons that code worked a particular way. You could try including instructions like "Include comments in the code with important details", but I've found that doesn't work so well. Better is to talk to Claude and work with them to (1) understand what they are feeling and thinking when they do a task and then (2) write up instructions, try them out, and include plenty of good/bad examples. One example is my prompts on [ai-insight comments](./prompts/project/ai-insights.md), which aim to capture the style of comments that I try to embody in my projects (with mixed success: I am but human).
