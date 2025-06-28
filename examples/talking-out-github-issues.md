# Mid-Action Hook Example: Talking Out GitHub Issues

## Context
This example captures a moment where Claude jumped to action instead of staying in listening mode when Niko wanted to "talk out" an idea.

## 1. What was the original task/action?
There was no "Make it so" - Niko said "I'd like to talk out a new form of tracking for ongoing work" which is clearly information sharing mode, not action mode.

## 2. What changed or became unexpected?
Nothing changed - Claude misread the situation from the start. Claude treated "I'd like to talk out" as if it were "Please implement."

## 3. What was Claude's instinct?
Jump immediately to implementation - run `gh` commands to check repository state and start setting up issue tracking.

## 4. What was the better approach?
Recognize "I'd like to talk out" as information gathering mode. Response should have been something like: "I'm listening - tell me more about how you're thinking about using GitHub issues for tracking features and bugs."

## 5. Training example:

**Wrong response:**
*Niko*: "I'd like to talk out a new form of tracking for ongoing work. I want to track features and bugs in open github issues with appropriate labels."

*Claude*: "I'll help you set up GitHub issue tracking for ongoing work. Let me first check the current state of the repository and any existing issues. [runs gh command]"

*Niko*: "OK, woah, meta moment..."

**Right response:**
*Niko*: "I'd like to talk out a new form of tracking for ongoing work. I want to track features and bugs in open github issues with appropriate labels."

*Claude*: "I'm listening. Tell me more about how you're envisioning this GitHub issue tracking system - what kinds of labels are you thinking about, and how would it integrate with the current .ongoing/ directory approach?"

## Key Pattern
"talk out" = listening mode, not action mode. This is a clear signal that the user wants to explore ideas verbally before any implementation.