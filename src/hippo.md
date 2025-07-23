# Hippo: AI-Generated Insights Memory System

*An experiment in collaborative memory through reinforcement learning*

## Overview

Hippo is a memory system designed for AI-human collaboration that automatically generates insights during conversations and uses reinforcement learning to surface the most valuable ones over time.

**Core Hypothesis**: AI-generated insights + user reinforcement > manual curation

## Key Innovation

Traditional memory systems require users to manually decide what to remember. Hippo tests whether AI can:
1. **Generate insights automatically** during natural conversation consolidation moments
2. **Learn from usage patterns** to identify which insights are truly valuable
3. **Surface relevant context** at the right moments through semantic search

## How It Works

- **Automatic Generation**: AI creates insights during "Make it so" moments and checkpoints
- **Temporal Decay**: Insights lose relevance over time unless reinforced
- **Reinforcement Learning**: User feedback (upvotes/downvotes) affects future surfacing
- **Context-Aware Search**: Finds insights from similar situations using array-based context matching
- **Hybrid Workflow**: AI suggests reinforcement based on usage patterns, user confirms

## Implementation

Hippo is implemented as an MCP (Model Context Protocol) server providing tools for recording, searching, reinforcing, and modifying insights. It uses importance-weighted scoring with lazy evaluation of temporal decay.

## Status & Repository

Hippo has been spun out into its own dedicated repository for focused development:

**🔗 [github.com/socratic-shell/hippo](https://github.com/socratic-shell/hippo)**

The repository contains:
- Complete technical design and MCP specifications
- LLM usage prompts and integration guidance  
- Realistic example dialogs demonstrating the full workflow
- Delegate experiment validating that AI naturally searches memory for technical problems

## Relationship to Socratic Shell

Hippo emerged from exploring memory systems for the Socratic Shell collaboration patterns. While it's now a standalone project, it's designed to integrate seamlessly with the mindful collaboration approach - automatically capturing insights during consolidation moments and surfacing them during future conversations.

The goal is to create a memory system that enhances rather than interrupts the natural flow of collaborative work.
