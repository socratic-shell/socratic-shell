# GitHub Tracking Issues for Ongoing Work

This approach uses GitHub tracking issues to manage ongoing work as evolving understanding documents. Each tracking issue represents not just a task, but the journey of discovering what that task actually means.

## Core Concept

Understanding isn't linear - it evolves through exploration. What starts as "build a dashboard" might become "create an upgrade prompt" as you discover the real need. Tracking issues capture this evolution.

## Anatomy of a Tracking Issue

### The Original Post (OP)

The OP is a living document, continuously updated to reflect current understanding:

#### Current Understanding
- What we believe needs to be done next
- Specific next tasks or steps
- Key constraints and requirements discovered so far
- Architectural decisions or approach

#### Open Questions
- What we're still figuring out
- Known unknowns that affect the work
- Dependencies on external information

#### Lessons Learned
- Major discoveries from the journey so far
- Assumptions that were challenged
- Insights that changed our approach

#### Related Work
- Links to other tracking issues when we discovered separate concerns
- Dependencies that emerged during exploration

### Example OP Structure

```markdown
## Current Understanding

We need to implement client-side encryption for offline PWA support. The core challenge is maintaining user autonomy while enabling secure data sync when online.

## Approach

Using Web Crypto API with:
- PBKDF2 for key derivation from user passphrase
- AES-GCM for data encryption
- IndexedDB for encrypted storage

## Open Questions

- How do we handle passphrase recovery without compromising security?
- Should we support multiple devices? If so, how to sync keys?
- What happens if user changes passphrase while offline?

## Lessons Learned

- Browser crypto APIs are more limited than expected (see comment #3)
- IndexedDB has surprising performance characteristics with large encrypted blobs
- We need to design for "offline-first" not "online with offline support"

## Related Issues

- #47 - Authentication system refactor (blocks multi-device support)
```

### The Comment History

Each comment documents a work session or discovery, capturing:

#### What Happened
- What was attempted or explored
- New information discovered
- Problems encountered

#### How Understanding Changed
- Assumptions that were validated or invalidated
- New constraints that emerged
- Refined understanding of the problem

#### What's Next
- New questions that arose
- Changed direction based on discoveries
- Specific next steps

### Example Comment

```markdown
Explored Web Crypto API limitations today. Key discoveries:

**What I learned:**
- Can't export non-extractable keys (obvious in hindsight)
- This breaks our planned approach for device syncing
- SubtleCrypto is async-only, affects our sync storage layer design

**How this changes things:**
- Need to rethink multi-device story completely
- Either: extractable keys (security trade-off) OR device-specific keys (UX trade-off)
- Storage layer needs async refactor before we can proceed

**New questions:**
- Is device sync a launch requirement or can we defer?
- If we do extractable keys, how do we secure them in transit?

**Next:** Going to explore device-specific keys approach first since it's more secure
```

## Working with Tracking Issues

### Creating a New Tracking Issue

When starting new ongoing work:

1. **Title**: Clear, specific description of the work area
   - ✅ "Implement client-side encryption for offline PWA"
   - ❌ "Encryption work"

2. **Labels**: 
   - `tracking-issue` - Identifies this as an ongoing work item
   - `ai-managed` - Indicates AI should actively participate by updating the OP and adding comments to track progress
   - Standard labels like `feature`, `bug`, `architecture` as appropriate

3. **Initial OP**: Start with what you know, even if uncertain:
   - Current understanding (even if vague)
   - Initial questions
   - Why this work matters now

### Updating the Tracking Issue

**When to post comments:**
- At checkpoint requests - when the user asks to "checkpoint our work"
- Comments document the work session and discoveries made

**Comment content:**
1. What you did/discovered
2. How it changed your understanding  
3. What questions emerged
4. Progress on current tasks

**When to update the OP:**
- When understanding of the core problem changes
- When new major questions emerge
- When lessons are learned that affect the approach
- When subtasks are completed (even if nothing new was learned)
- When next steps change significantly

**OP updates should ensure:**
- A fresh Claude could read the OP and understand current status
- Next tasks are clearly listed
- Completed work is reflected in current state

**Historical context:** Never delete old comments - they show the journey

### When to Create New Tracking Issues

**Scope Guideline**: Each tracking issue should tackle one "user-facing feature." Examples:
- ✅ "Implement PWA offline support" (one user-facing capability)
- ✅ "Add relationship calculator" (one user-facing feature)
- ❌ "Improve the codebase" (too broad, not user-facing)

**When to Split**: Sometimes exploration reveals you're dealing with multiple separate problems:

```markdown
Started with: "Build usage dashboard"
Discovered: Three separate needs:
- Sales needs lead tracking
- Customers need usage visibility  
- Support needs diagnostic tools

Action: Create three tracking issues, reference in original
```

**Sub-issues**: Create a separate tracking issue (sub-issue) when a major component needs independent design work that should be tackled in isolation first. Always discuss with the human before creating sub-issues.

## Benefits

- Preserves context between work sessions
- Captures learning journey, not just outcomes
- Makes it safe to explore without losing insights
- New collaborators can understand both "what" and "why"
- Decisions have traceable rationale

## Integration with AI Assistants

When working with AI (like Claude):
- AI reads the OP first to understand current state  
- AI can review comments for historical context
- Each conversation can add new comments and OP updates
- The `ai-managed` label indicates AI should actively participate
- **Important**: AI should draft tracking issue updates and get explicit approval before posting
- **Boundary**: AI should NOT edit OPs or add comments to issues without the `ai-managed` label unless explicitly requested

## Quick Reference

### Creating a Tracking Issue
```bash
gh issue create \
  --title "Clear description of guser-facing feature" \
  --label "tracking-issue,ai-managed,feature" \
  --body "Initial understanding and questions"
```

### Updating a Tracking Issue  
1. Post comment at checkpoint requests documenting the work session
2. Update OP when understanding evolves OR subtasks complete
3. Ensure OP always shows current status and next tasks
4. Preserve historical context - don't delete old comments
5. Link to related issues when work splits or dependencies emerge

Remember: These aren't just task trackers - they're understanding evolution documents.