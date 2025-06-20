"""Core sampling logic for pattern testing."""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
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
        
        # Read system prompt and reminders from files
        system_prompt = await self._read_file_if_exists(pattern_test.system_prompt_path)
        system_reminders = await self._read_system_reminders(pattern_test.system_reminders_paths)
        
        # Create sampling tasks for all scenarios
        tasks = [
            self._sample_scenario(
                pattern_test.base_context,
                scenario,
                pattern_test.sampling_config,
                system_prompt,
                system_reminders,
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
        test_scenario: str,
        config: SamplingConfig,
        system_prompt: str | None,
        system_reminders: list[str],
    ) -> SamplingResult:
        """Sample a single scenario with the given pattern."""
        start_time = time.time()
        
        # Build messages with system reminders and user message
        messages = self._build_messages(
            base_context, test_scenario, system_reminders
        )
        
        # Make the MCP sampling call
        sampling_params = {
            "messages": messages,
            "maxTokens": config.max_tokens,
            "temperature": config.temperature,
        }
        
        # Add system prompt if provided
        if system_prompt:
            sampling_params["systemPrompt"] = system_prompt
            
        sampling_request = {
            "method": "sampling/createMessage",
            "params": sampling_params,
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
    
    def _build_messages(
        self, base_context: str, test_scenario: str, system_reminders: list[str]
    ) -> list[dict[str, Any]]:
        """Build message array with system reminders and user message."""
        messages = []
        
        # Add system reminders as user messages (mimicking Claude's actual format)
        if system_reminders:
            reminder_content = "\n\n".join(system_reminders)
            messages.append({
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"<system-reminder>\n{reminder_content}\n</system-reminder>"
                }
            })
        
        # Add base context and test scenario
        user_message = f"{base_context}\n\nUser: {test_scenario}"
        messages.append({
            "role": "user", 
            "content": {
                "type": "text",
                "text": user_message
            }
        })
        
        return messages
    
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
    
    async def _read_file_if_exists(self, file_path: str | None) -> str | None:
        """Read file content if path is provided and file exists."""
        if not file_path:
            return None
            
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        return path.read_text(encoding="utf-8")
    
    async def _read_system_reminders(self, file_paths: list[str]) -> list[str]:
        """Read multiple system reminder files."""
        reminders = []
        for file_path in file_paths:
            content = await self._read_file_if_exists(file_path)
            if content:
                reminders.append(content)
        return reminders