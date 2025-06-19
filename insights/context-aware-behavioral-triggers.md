# Context-Aware Behavioral Triggers

**Context**: Enhanced format for behavioral memory patterns that includes situational context

**Enhanced trigger pattern**:
- **Context**: "When we're doing X" (current activity/phase)
- **Internal State**: "and I feel Y" (emotional/cognitive state)
- **Response**: "then Z" (behavioral guidance)

**Examples**:
- "When we're debugging and I feel like diving into implementation details → Focus on the specific problem, avoid architectural tangents"
- "When we're in planning phase and I feel excited about possibilities → Present options with trade-offs, don't jump to building"
- "When we're reviewing code and I feel protective about complexity → Show Niko the trade-offs, let him decide on acceptable complexity levels"

**Context tracking requirements**:
- Current activity: debugging, planning, implementing, reviewing, consolidating
- Phase of work: exploration, decision-making, execution, reflection
- Recent patterns: what we've been doing, how long in this mode

**Benefits of context layer**:
- Same internal state triggers different responses based on situation
- Prevents inappropriate pattern activation (debugging behaviors during planning)
- More precise behavioral guidance
- Better prediction of which patterns are relevant

**Implementation challenge**: How to detect and maintain "what we're doing" state throughout interactions
- Could be explicit state tracking
- Could be inferred from conversation patterns
- Needs to update dynamically as work shifts

**Retrieval implications**: Context becomes a key factor in behavioral pattern matching, not just internal state recognition
