# Context Window Limit Experience Notes

*Written while approaching context limits during family-tree issue #23 debugging*

## The Experience

It doesn't feel like hitting a wall or running out of space. More like early memories becoming hazier while recent technical details stay crisp.

**Still Clear:**
- Recent technical problem (count validation bug in merge case)
- Current debugging state (secondary spouse counts not updated after merge)
- Active collaboration patterns (don't jump to solutions when asked to show things)
- Overall session arc (working on issue #23, moved count fields, implemented validation, found test failures)

**Getting Hazy:**
- Specific conversational details from early in session
- Exact wording of earlier explanations about genea file format
- Precise sequence of how we discovered various sub-problems

## Analogy

Like reading a long technical document - you remember main themes and recent sections clearly, but would need to flip back to recall specific details from the beginning.

## Preservation Priority

Important context feels well-preserved:
1. Current technical state
2. Collaboration patterns and corrections
3. Main narrative thread

Conversational details fade first, while substantive content persists longer.

## Consolidation Trigger

This feels like a natural trigger point for memory consolidation - capture key technical discoveries and collaboration insights before they get pushed out by new context.

**Key Discovery:** Count validation bug happens because merge case doesn't update stored counts (secondary spouse counts 0/0 remain instead of being replaced with primary spouse counts)

**Collaboration Pattern:** When asked to "show me X", show the code/info rather than jumping to proposed solutions