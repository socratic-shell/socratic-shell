# Ongoing Files for Work Tracking

This approach uses a `.ongoing/` directory with markdown files to track active development work and maintain context between sessions.

## Core Concept

Each major feature or investigation gets its own markdown file in `.ongoing/` that serves as a living document for tracking progress, decisions, and next steps.

## Directory Structure

```
.ongoing/
├── feature-name.md
├── bug-investigation.md
└── architecture-decision.md
```

## File Structure

Each ongoing file should include:

### Status Line
- Current phase of work (e.g., "Design Approved", "Implementation Started", "Blocked")
- Created/Updated dates
- Priority level if relevant

### Overview
- Brief description of what this work is about
- Why it matters
- Success criteria

### Current State
- What's been completed
- What's in progress
- Known blockers or dependencies

### Next Steps
- Specific, actionable tasks
- Include file/line references where relevant
- Priority order

### Technical Details
- Key design decisions
- Architecture choices
- Integration points

### Open Questions
- Unresolved issues
- Decisions that need input
- Dependencies on external factors

## Example Ongoing File

```markdown
# Client-Side Encryption

## Status: Architecture Finalized, Starting Implementation
**Created**: June 24, 2025
**Updated**: June 24, 2025
**Priority**: HIGH - Enables removing server-side auth for PWA support

## Overview
Replace server-side password protection with client-side encryption to enable PWA functionality while maintaining privacy. Users enter a password once, which is stored locally and used to decrypt the family data.

## Problem
- Server-side auth blocks PWA features (manifest.json returns 401)
- PWA can't install or work offline with server auth
- Need privacy protection for sensitive data

## Current State
- [x] Architecture design complete
- [x] Encryption approach selected (AES-GCM)
- [ ] Build-time encryption script
- [ ] Client-side decryption
- [ ] Password UI implementation

## Next Steps
1. Create Node.js script to encrypt JSON files at build time
2. Implement password prompt component
3. Add client-side decryption to data service
4. Test offline functionality

## Technical Details
- Use Web Crypto API for client-side decryption
- PBKDF2 for key derivation
- Store password in localStorage
- Encrypted files use .enc extension

## Open Questions
- How to handle password changes?
- Should we support "remember me" functionality?
- What's the UX for wrong password attempts?
```

## Content Guidelines

### INCLUDE (essential for resuming work):
- High-level status and completion percentage
- Priority-ordered next steps with specific file/line references
- Key design decisions with pointers to detailed explanations in code
- Integration points (which files/services connect to this work)
- Known blockers or dependencies

### EXCLUDE (belongs elsewhere):
- Detailed algorithms or mathematical foundations (put in code comments or architecture docs)
- Complete implementation history or session-by-session changes (git handles this)
- Code examples or debugging snippets (put in actual code files)
- ASCII diagrams or visual mockups (put in architecture documentation)
- Detailed bug-fixing narratives (git commit messages capture this)

The goal is concise context for continuation, not comprehensive documentation.

## Working with Ongoing Files

### Creating a New File
When starting new work:
1. Create descriptive filename: `feature-name.md`
2. Start with status, overview, and initial understanding
3. List known tasks and questions
4. Update as work progresses

### Updating Files
- Update status line when phase changes
- Check off completed items
- Add new discoveries to relevant sections
- Keep next steps current and actionable

### Completing Work
When work is done:
- Mark status as "COMPLETED"
- Archive to `.ongoing/completed/` or remove file
- Ensure learnings are captured in code comments or docs

## Benefits

- Simple file-based system, no external dependencies
- Easy to grep/search for current work
- Works offline
- Version controlled with the code
- Quick context switching between tasks

## Integration with AI Assistants

When working with AI:
- AI should check `.ongoing/` at start of session
- Update relevant files as work progresses
- Create new files for new work streams
- Use files to maintain context between conversations

## When to Use This Approach

Best for:
- Smaller teams or solo developers
- Projects without issue tracking systems
- Work that needs detailed technical notes
- Situations where you want work tracking in the repo itself

Not ideal for:
- Large teams needing visibility
- Work requiring external collaboration
- Projects with existing issue tracking workflows

## Quick Reference

### Create new ongoing work:
```bash
echo "# Feature Name\n\n## Status: Started\n**Created**: $(date +%Y-%m-%d)\n\n## Overview\n\n## Next Steps\n" > .ongoing/feature-name.md
```

### Check current work:
```bash
ls -la .ongoing/
grep -h "^## Status:" .ongoing/*.md
```

### Clean up completed work:
```bash
mkdir -p .ongoing/completed
mv .ongoing/completed-feature.md .ongoing/completed/
```

Remember: The goal is maintaining just enough context to resume work effectively, not creating comprehensive documentation.