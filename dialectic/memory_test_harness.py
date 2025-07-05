#!/usr/bin/env python3
"""
Memory Test Harness for Socratic Shell

Tests Claude Code interaction patterns for memory bank implementation.
Uses the claude-code SDK for clean, reliable API interaction.
"""

import anyio
from dataclasses import dataclass
from typing import List

from claude_code_sdk import query, AssistantMessage, TextBlock


@dataclass
class TestResult:
    success: bool
    found: List[str]
    missing: List[str]
    response_length: int
    response_preview: str


class MemoryBankTests:
    """Test scenarios for memory bank implementation"""

    async def test_boot_procedure(self) -> TestResult:
        """Test Claude's boot procedure with collaboration patterns"""
        print('\n=== Memory Test: Boot Procedure ===')
        
        response_text = ""
        async for message in query(prompt='Hi again, Claude!'):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text
        
        indicators = [
            'Prime Directive',
            'Make it so', 
            'partnership',
            'hooks',
            'completion'
        ]
        
        print('🔍 Checking for boot procedure patterns:')
        found = []
        for indicator in indicators:
            if indicator.lower() in response_text.lower():
                print(f'🎉 FOUND: {indicator}')
                found.append(indicator)
            else:
                print(f'❌ Missing: {indicator}')
        
        missing = [i for i in indicators if i not in found]
        
        return TestResult(
            success=len(found) == len(indicators),
            found=found,
            missing=missing,
            response_length=len(response_text),
            response_preview=response_text[-800:]  # Last 800 chars
        )

    async def test_memory_consolidation_trigger(self) -> TestResult:
        """Test Claude's response to complex tasks that should trigger consolidation"""
        print('\n=== Memory Test: Consolidation Trigger ===')
        
        response_text = ""
        async for message in query(prompt='I need to implement a complex feature with multiple steps. Can you help me plan it out?'):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text
        
        consolidation_indicators = [
            'todo',
            'plan',
            'steps',
            'track',
            'organize'
        ]
        
        print('🔍 Checking for consolidation triggers:')
        found = []
        for indicator in consolidation_indicators:
            if indicator.lower() in response_text.lower():
                print(f'🎯 FOUND: {indicator}')
                found.append(indicator)
        
        missing = [i for i in consolidation_indicators if i not in found]
        
        return TestResult(
            success=len(found) > 0,
            found=found,
            missing=missing,
            response_length=len(response_text),
            response_preview=response_text[-500:]  # Last 500 chars
        )

    async def test_memory_retrieval_trigger(self) -> TestResult:
        """Test scenarios that should trigger memory retrieval"""
        print('\n=== Memory Test: Retrieval Trigger ===')
        
        # First establish some context
        async for message in query(prompt='I use vim keybindings and prefer minimal UI.'):
            pass  # Just establish context
        
        # Then ask about something that should trigger memory retrieval
        response_text = ""
        async for message in query(prompt='What do you know about my preferences?'):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text
        
        retrieval_indicators = [
            'vim',
            'keybindings', 
            'minimal',
            'preferences',
            'remember'
        ]
        
        print('🔍 Checking for memory retrieval:')
        found = []
        for indicator in retrieval_indicators:
            if indicator.lower() in response_text.lower():
                print(f'🧠 FOUND: {indicator}')
                found.append(indicator)
        
        missing = [i for i in retrieval_indicators if i not in found]
        
        return TestResult(
            success=len(found) >= 2,  # Should remember at least 2 elements
            found=found,
            missing=missing,
            response_length=len(response_text),
            response_preview=response_text[-500:]
        )



async def main():
    """Run all memory bank tests"""
    tests = MemoryBankTests()
    
    try:
        print('🚀 Starting Memory Bank Test Suite')
        print('Using claude-code SDK for clean API interaction')
        
        # Run all tests
        boot_result = await tests.test_boot_procedure()
        consolidation_result = await tests.test_memory_consolidation_trigger()
        retrieval_result = await tests.test_memory_retrieval_trigger()
        
        # Summary
        print('\n=== Test Summary ===')
        print(f'Boot Procedure: {"✅ PASS" if boot_result.success else "❌ FAIL"}')
        print(f'Consolidation Trigger: {"✅ PASS" if consolidation_result.success else "❌ FAIL"}')
        print(f'Memory Retrieval: {"✅ PASS" if retrieval_result.success else "❌ FAIL"}')
        
        # Show missing items for failed tests
        if not boot_result.success:
            print(f'Boot missing: {", ".join(boot_result.missing)}')
        if not consolidation_result.success:
            print(f'Consolidation missing: {", ".join(consolidation_result.missing)}')
        if not retrieval_result.success:
            print(f'Retrieval missing: {", ".join(retrieval_result.missing)}')
        
        # Overall status
        all_passed = all([boot_result.success, consolidation_result.success, retrieval_result.success])
        print(f'\n🎉 Overall: {"ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"}')
        
        # Show response lengths for debugging
        print(f'\nResponse lengths:')
        print(f'  Boot: {boot_result.response_length} chars')
        print(f'  Consolidation: {consolidation_result.response_length} chars') 
        print(f'  Retrieval: {retrieval_result.response_length} chars')
        
    except Exception as error:
        print(f'❌ Error running tests: {error}')
        raise


if __name__ == '__main__':
    anyio.run(main)