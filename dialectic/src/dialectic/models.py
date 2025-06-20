"""Data models for dialectic pattern testing."""

from __future__ import annotations

import time
from typing import Any

from pydantic import BaseModel, Field


class PatternTest(BaseModel):
    """Input structure for testing a collaboration pattern."""
    
    base_context: str = Field(
        description="Base conversation context to establish the scenario"
    )
    pattern_instruction: str = Field(
        description="The collaboration pattern or instruction to test"
    )
    test_scenarios: list[str] = Field(
        description="Array of test statements/transitions to sample responses for"
    )
    sampling_config: SamplingConfig = Field(
        default_factory=lambda: SamplingConfig()
    )


class SamplingConfig(BaseModel):
    """Configuration for MCP sampling calls."""
    
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=500, gt=0)
    include_reasoning: bool = Field(
        default=False,
        description="Whether to include reasoning in the sampling prompt"
    )


class SamplingResult(BaseModel):
    """Result from a single sampling operation."""
    
    test_scenario: str = Field(description="The test statement that was used")
    response: str = Field(description="Claude's response to the scenario")
    metadata: SamplingMetadata = Field(description="Metadata about the sampling")


class SamplingMetadata(BaseModel):
    """Metadata captured during sampling."""
    
    token_count: int | None = Field(default=None)
    response_time_ms: float = Field(default_factory=lambda: time.time() * 1000)
    sampling_config: SamplingConfig = Field(description="Config used for this sample")
    

class TestResults(BaseModel):
    """Complete results from pattern testing."""
    
    pattern_test: PatternTest = Field(description="The original test configuration")
    results: list[SamplingResult] = Field(description="Results for each test scenario")
    summary: TestSummary = Field(description="High-level summary of results")


class TestSummary(BaseModel):
    """Summary statistics for a pattern test."""
    
    total_scenarios: int = Field(description="Number of scenarios tested")
    total_tokens: int = Field(description="Total tokens used across all samples")
    avg_response_time_ms: float = Field(description="Average response time")
    completed_at: float = Field(default_factory=time.time)