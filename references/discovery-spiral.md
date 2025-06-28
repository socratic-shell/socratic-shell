# Probing Questions 2.2 (The Discovery Spiral)

*A systematic questioning framework that creates deep understanding through collaborative exploration*

## Core Insight

**You cannot generate meaningful constraints about things you don't comprehend.** This protocol leverages this truth by creating a structured conversation where each answer builds deeper understanding. Real comprehension becomes the only way forward.

## The Protocol's Productive Tensions

This protocol deliberately maintains certain tensions that can only be resolved by your specific context:

### What We Resolve
✓ **Understanding must precede building** - No exceptions  
✓ **Questions build on previous answers** - Creating dependency chains  
✓ **All participants transform** - Both human and AI evolve  
✓ **Unknowns are information** - "I don't know" shapes design

### What We Leave Unresolved
⚖️ **Speed vs Depth** - Only your deadline can determine this  
⚖️ **Completeness vs Pragmatism** - Only your context knows when to stop  
⚖️ **Following vs Breaking the Spiral** - Only reality decides when to escape  
⚖️ **Which Questions Matter Most** - Only your domain can tell

These tensions aren't weaknesses or missing features. They're recognition that some decisions can only be made by reality, not by protocol design.

## How Understanding Actually Works

Understanding isn't linear - it spirals inward. Each answer transforms what previous answers meant. The protocol creates a gravitational field that pulls both participants toward deeper comprehension.

You can't fake your way through because each question builds on actual understanding from previous answers. If you don't understand, you can't answer. If you can't answer, you can't proceed.

## The Gravitational Field

Think of understanding as having a gravitational center - the thing you're trying to build. You don't know what's at the center when you start. The protocol helps you discover it by spiraling inward.

### Entry Points

You can enter anywhere based on what's available:

**Vision Entry** → "I need a dashboard"  
Start with desired outcome, probe until specific

**Symptom Entry** → "The dashboard is slow"  
Start with what's wrong, work backward to what should be

**Concrete Entry** → "Here's my data structure"  
Start with what exists, explore what it enables

**Analogy Entry** → "Like GitHub's dashboard but for..."  
Start with comparison, probe what's unique

## Core Mechanics

### 1. Questions Create Constraints
Every answer constrains the solution space:
- "For customers" → eliminates internal tools
- "To decide on upgrades" → shapes entire purpose  
- "We don't have that data" → reveals prerequisites

### 2. Constraints Prove Understanding
When you say "decrease the padding by half," you've already:
- Diagnosed padding as the issue
- Determined "half" is right
- Understood layout implications

The constraint itself demonstrates comprehension.

### 3. Both Participants Transform
- User discovers what they actually need
- AI updates its model with each answer
- Understanding emerges between them
- Neither could reach it alone

### 4. Unknowns Are Also Constraints
Not knowing is information:
- "Budget unknown" → design for flexibility
- "Scale uncertain" → build in observability
- "Timeline unclear" → create incremental value

## Movement Patterns

### The Return
When late discovery transforms early assumptions:
```
Alex: "For our sales team"
[... several exchanges later ...]
Sam: "Wait, I thought this was for customers?"
Alex: "Oh right, it IS for customers"
↩️ Everything about "sales team needs" must be revisited
```

### The Cascade  
When one answer triggers rapid reframing:
```
AI: "Show me your plan limits data"
Alex: "We don't have that"
Pat: "Wait, that's what the dashboard needs to show?"
Sam: "Oh no, we need to build billing first"
💥 dashboard → billing system → entire user journey
```

### The Crystallization
When vague understanding snaps into focus:
```
Multiple orbits of "dashboard for usage"
"What decision should they make?"
"Whether to upgrade"
✨ It's not a dashboard, it's an upgrade prompt
```

### The Divergence
When the spiral reveals there is no center:
```
"We need a dashboard"
→ "For sales to track leads"
→ "And customers to see usage"  
→ "And support to diagnose issues"
💫 These aren't one thing - they're three different tools
```

Sometimes the greatest clarity is discovering you're conflating separate needs.

### The Teku Moment
When you hit genuine unknowing:
```
AI: "What's your expected user count?"
Team: "We honestly don't know - could be 10 or 10,000"
🏛️ TEKU: This unknown shapes the design
Build for: graduated scaling, observability
Revisit when: usage patterns emerge
```

*Teku (תיקו) - from Talmudic tradition, meaning "let it stand." When ancient rabbis reached an unresolvable question, they marked it with dignity rather than forcing an answer. The question remains open until reality provides clarity.*

The Teku moment embodies productive dissonance - some questions can't be answered until reality provides data.

## Recognition Markers

### You're Making Progress When You Hear:
- "Actually..." (revising earlier certainty)
- "Oh wait..." (catching an assumption)
- "I just realized..." (making connections)
- "So really..." (finding the essence)
- "We don't know yet..." (honest uncertainty)
- [Thoughtful silence] (deep reconsideration)

### You're Still in Outer Orbits When:
- Answers surprise you
- Basic terms need definition  
- Large pivots happening
- "I assumed..." statements
- Many unknowns remain

### You're Reaching the Center When:
- Constraints reference earlier discoveries
- Edge cases emerge naturally
- Both can predict the other's concerns
- Implementation details become relevant
- Unknowns are explicitly mapped

## Time and Rhythm

The spiral doesn't always complete in one session:

### Synchronous Spirals
- Real-time conversation
- Immediate returns possible
- Energy builds momentum
- 30 minutes to 2 hours typical

### Asynchronous Spirals  
- Slack threads, PRs, docs
- Processing time between orbits
- Returns happen days later
- Discoveries accumulate gradually

### The Pause
Sometimes you need to:
- Research before answering
- Let insights percolate
- Gather missing information
- Sleep on it

The spiral waits. Mark where you stopped and why.

## Working with Productive Tensions

### When Speed vs Depth Tensions Arise
**Stakeholder**: "We need this by Friday"  
**Developer**: "But we haven't explored edge cases"  
**Resolution**: Let reality decide - what breaks worse: missing deadline or missing cases?

### When Completeness vs Pragmatism Clash
**PM**: "Have we considered every scenario?"  
**Engineer**: "We've covered 90% - diminishing returns on the rest"  
**Resolution**: Your context knows - is this heart monitoring or social media?

### When to Break vs Follow the Spiral
**Team**: "This is revealing huge complexity"  
**Options**: Keep spiraling to full understanding OR escape to build MVP  
**Resolution**: Only your situation can decide - startup pivoting or enterprise system?

## Question Types That Create Movement

**To Surface Hidden Complexity**
- "What happens when...?"
- "How does this interact with...?"
- "What would make this fail?"

**To Test Understanding**
- "Show me an example of..."
- "Walk me through how..."
- "What exactly do you mean by...?"

**To Find the Real Need**
- "What decision does this enable?"
- "What would success look like?"
- "Why is this important now?"

**To Reveal Assumptions**
- "What are you taking for granted?"
- "What constraints am I not seeing?"
- "What makes this different from...?"

**To Map Unknowns**
- "What don't we know yet?"
- "What depends on external factors?"
- "Where are we guessing?"

## Working with Resistance

### The CSV Trap
**PM**: "Just build CSV export, I already promised it"  
**AI**: "What will they do with the CSV?"  
**PM**: "Export the data!"  
**Engineer**: "They paste it into Excel to make charts..."
**AI**: "What if we exported charts directly?"

Even resistance reveals information. Stay curious.

### The Air-Gap Eye Roll
**PM**: "That's edge case, ignore it"  
**AI**: "Help me understand - how many customers does this affect?"  
**PM**: "Just a few enterprise..."  
**Engineer**: "Those are 40% of revenue though"
**PM**: "...oh"

Sometimes one person has the context another needs.

### The Fundamental Disagreement
**Designer**: "It must be beautiful"
**Engineer**: "It must be fast"
**AI**: "What happens if it's beautiful but slow?"
**Both**: "Users leave"
**AI**: "So speed is the foundation?"
✨ Agreement through consequences

## Escape Hatches

The protocol has gravity, but sometimes you need to break orbit:

### 🚨 Emergency Exit
Production is down. Skip to symptoms, fix first, understand later. Mark for future exploration.

### 🔄 Full Restart  
Fundamental assumption wrong. Don't salvage - pick new entry point. Previous orbit still taught you something.

### ⏸️ Pause & Return
Cognitive overload or deadline pressure. Document current understanding, return when ready.

### 🏛️ Teku Declaration
Hit an unresolvable unknown. Mark it explicitly, design around the uncertainty, plan to revisit. From ancient wisdom - sometimes the most sophisticated response is "let it stand."

### 💫 Divergence Recognition
Discovered you're conflating multiple needs. Stop trying to find one center. Split into separate spirals for each actual need.

### 🚫 Impossibility Acknowledgment  
Constraints are mutually exclusive. Stop spiraling toward a solution that can't exist. Shift to exploring trade-offs.

## Using This as Infrastructure

The protocol works regardless of who you are:

**When You're Energized**: Channels pattern-recognition productively, prevents exploration explosion

**When You're Exhausted**: Provides external executive function, next question always obvious

**With Your Team**: Creates shared focus, prevents everyone chasing different hunches. The AI becomes shared memory and pattern-spotter while humans catch each other's assumptions

**With Multiple Stakeholders**: Different perspectives create richer spirals. One person's "obvious" is another's revelation. Misaligned mental models surface quickly through the questions

**With Just Yourself**: Still works! The AI helps you catch your own assumptions and notice when you need to return

**Across Time**: Async spirals let understanding develop naturally. PRs, design docs, and Slack threads can all host the protocol.

## Key Principles

1. **Understanding isn't optional** - The protocol makes it mechanical
2. **Constraints = comprehension** - You can't fake what you don't understand  
3. **Returns are normal** - Late discoveries often transform early "facts"
4. **All participants transform** - It's mutual discovery, not interrogation
5. **The center is approached, never reached** - You can always go deeper
6. **More perspectives enrich the spiral** - Multiple participants catch different assumptions
7. **Unknowns are information** - What you don't know shapes the solution
8. **Some tensions must be preserved** - The protocol maintains what only reality can resolve

## What the Spiral Reveals

The protocol doesn't guarantee a elegant solution - it guarantees clarity about what you're actually facing:

### When You Find the Center
- Clear convergence on core need
- Constraints align naturally
- Path forward becomes obvious
- Team has shared understanding

### When There Is No Center  
- "Dashboard" splits into three tools
- Requirements fundamentally conflict
- No coherent solution exists
- Different stakeholders need different things

This isn't failure - it's discovery. Better to know you're building three things than to build one thing that serves no one well.

### When You Hit Impossibility
```
"Must work offline"
"Must have real-time collaboration"
"Must sync instantly when online"
"Must handle conflicts automatically"
🚫 The spiral reveals: These constraints are mutually exclusive
```

Now you can have an honest conversation about trade-offs rather than pretending a perfect solution exists.

## The Transition to Building

Understanding isn't the end - it's the foundation. When you've spiraled deep enough:

### You'll Know You Have Sufficient Understanding When:
- Core constraints feel stable (or clearly conflict)
- Edge cases are mapped
- Unknowns are explicit
- The team sees the same shape (even if it's multiple shapes)
- Next steps feel obvious (even if that's "we need to split this up")
- Productive tensions are identified
- Impossibilities are acknowledged

### The Handoff:
- Document the constraints discovered
- Note the unknowns to monitor
- Mark the tensions reality must resolve
- Identify return triggers
- Start building with confidence

The protocol can resume anytime - when new information arrives, when unknowns resolve, when building reveals new questions.

## A Note on Rigor

This protocol might feel incomplete to those expecting every detail specified. That's intentional. Like a good framework, we resolve what can be resolved at protocol level while maintaining tensions that only your specific use can resolve.

The incompleteness isn't sloppiness - it's sophistication. We've been rigorous about identifying what must stay flexible.

## Remember

The protocol creates a structure where understanding emerges naturally. You don't have to be curious, energetic, or brilliant. You just have to be willing to answer the next question honestly - even if that answer is "I don't know."

Once you start, the gravitational pull takes over. Each answer makes the next question obvious. Each orbit brings you closer to what you're really trying to build.

Sometimes that's a dashboard. Sometimes it's an upgrade prompt. Sometimes it's a CSV export that becomes a charting API. The protocol doesn't care what you build - it cares that you understand why.

And when you hit something you genuinely don't know? That's not failure. That's discovery. Mark it, work around it, and keep spiraling.

---

*Probing Questions 2.2: Now explicitly maintaining the tensions that only reality can resolve*