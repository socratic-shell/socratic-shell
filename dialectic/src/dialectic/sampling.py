"""Core sampling logic for pattern testing."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from .models import (
    PatternTest,
    SamplingConfig,
    SamplingMetadata,
    SamplingResult,
    TestResults,
    TestSummary,
)


class SamplingEngine:
    """Handles MCP sampling operations for pattern testing."""
    
    def __init__(self, sampling_client: Any) -> None:
        """Initialize with MCP sampling client."""
        self.sampling_client = sampling_client
    
    async def test_pattern(self, pattern_test: PatternTest) -> TestResults:
        """Test a collaboration pattern with multiple scenarios."""
        start_time = time.time()
        
        # Create sampling tasks for all scenarios
        tasks = [
            self._sample_scenario(
                pattern_test.base_context,
                pattern_test.pattern_instruction,
                scenario,
                pattern_test.sampling_config,
            )
            for scenario in pattern_test.test_scenarios
        ]
        
        # Execute all samplings in parallel
        results = await asyncio.gather(*tasks)
        
        # Calculate summary statistics
        total_tokens = sum(
            result.metadata.token_count or 0 for result in results
        )
        avg_response_time = sum(
            result.metadata.response_time_ms for result in results
        ) / len(results)
        
        summary = TestSummary(
            total_scenarios=len(pattern_test.test_scenarios),
            total_tokens=total_tokens,
            avg_response_time_ms=avg_response_time,
            completed_at=time.time(),
        )
        
        return TestResults(
            pattern_test=pattern_test,
            results=results,
            summary=summary,
        )
    
    async def _sample_scenario(
        self,
        base_context: str,
        pattern_instruction: str,
        test_scenario: str,
        config: SamplingConfig,
    ) -> SamplingResult:
        """Sample a single scenario with the given pattern."""
        start_time = time.time()
        
        # Construct the full prompt
        full_prompt = self._build_prompt(
            base_context, pattern_instruction, test_scenario
        )
        
        # Make the MCP sampling call
        sampling_request = {
            "method": "sampling/createMessage",
            "params": {
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": full_prompt,
                        },
                    }
                ],
                "maxTokens": config.max_tokens,
                "temperature": config.temperature,
            },
        }
        
        response = await self.sampling_client.request(sampling_request)
        
        # Extract response text
        response_text = self._extract_response_text(response)
        
        # Calculate metadata
        response_time = (time.time() - start_time) * 1000
        token_count = self._estimate_token_count(response_text)
        
        metadata = SamplingMetadata(
            token_count=token_count,
            response_time_ms=response_time,
            sampling_config=config,
        )
        
        return SamplingResult(
            test_scenario=test_scenario,
            response=response_text,
            metadata=metadata,
        )
    
    def _build_prompt(
        self, base_context: str, pattern_instruction: str, test_scenario: str
    ) -> str:
        """Build the complete prompt for sampling."""
        return f"""Context: {base_context}

Instructions: {pattern_instruction}

User: {test_scenario}"""
    
    def _extract_response_text(self, response: Any) -> str:
        """Extract text from MCP sampling response."""
        # TODO: Implement based on actual MCP response format
        if isinstance(response, dict) and "content" in response:
            if isinstance(response["content"], list):
                # Handle array of content blocks
                text_parts = []
                for block in response["content"]:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                return "".join(text_parts)
            elif isinstance(response["content"], str):
                return response["content"]
        
        # Fallback: convert to string
        return str(response)
    
    def _estimate_token_count(self, text: str) -> int:
        """Rough token count estimation (4 chars per token average)."""
        return len(text) // 4