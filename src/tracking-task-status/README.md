# Tracking Task Status Explicitly

Using structured files and GitHub issues to maintain context across work sessions.

## What It Provides
- Persistent task state that survives session boundaries
- Clear scope definition for multi-session work
- Progress tracking and session continuity
- Natural integration with existing development workflows

## Two Approaches

### GitHub Issues (Current)
Using GitHub issues as living documents with specific conventions. Each substantial feature gets a tracking issue where the Original Post maintains current status and comments capture session details.

### .ongoing Files (Legacy)
File-based approach where each ongoing task gets a dedicated `.ongoing` file in the project directory to track progress and context.

## Key Benefits
This explicit context management works well because both human and AI can reference and update the same structured information, providing reliable continuity across sessions without requiring specialized infrastructure.

## Custom Prompt Integration
- [GitHub Issues prompt](../prompts/project/github-tracking-issues.md) - Current approach with detailed conventions
- [.ongoing Files prompt](../prompts/project/ongoing-work-tracking.md) - Legacy file-based approach

## Status
**Working approach** - Explicit task tracking has proven effective for maintaining context. The GitHub issues approach is currently preferred over the older file-based system.
