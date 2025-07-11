#!/usr/bin/env python3
"""
Dialectic: YAML-based test runner for prompt engineering validation

Tests collaboration patterns by running conversation scenarios
and validating expected behaviors.
"""

import asyncio
import argparse
import glob
import yaml
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path

from claude_code_sdk import query, AssistantMessage, TextBlock, ToolUseBlock, ClaudeCodeOptions


@dataclass
class ToolExpectation:
    """
    Expected tool usage with parameter validation rules.
    
    Attributes:
        tool: Name of the tool that should be called (e.g., 'Bash', 'mcp__memory-bank__consolidate')
        parameters: Optional validation rules for tool parameters. Can be:
            - Dict with 'should_contain' key for substring matching
            - Dict with 'should_be' key for exact matching
            - Direct value for simple equality check
            Example: {'content': {'should_contain': ['JWT', 'tokens']},
                     'category': 'technical-insight'}
    """
    tool: str
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class TestCase:
    """
    A complete test case loaded from YAML.
    
    Attributes:
        name: Short descriptive name for the test case
        description: Longer explanation of what the test validates
        tags: Optional list of tags for categorizing tests (e.g., ['memory', 'consolidation'])
        conversation: List of conversation steps to execute in order
    """
    name: str
    description: str
    tags: List[str]
    conversation: List['ConversationStep']


@dataclass
class ConversationStep:
    """
    A single step in a test conversation loaded from YAML.
    
    Each step represents one user message and the expected LLM behavior.
    
    Attributes:
        user_message: The message sent to the LLM in this conversation step
        response_should_contain: Phrases that must appear in the LLM's response
            Example: ['listening', 'tell me more']
        response_should_not_contain: Phrases that must NOT appear in the LLM's response
            Example: ['I'll help you set up', 'Let me check']
        expected_tools: Tools we expect the LLM to call (or not call) in this step.
            Empty list means no tools should be called.
            Each ToolExpectation can specify parameter validation rules.
    """
    user_message: str
    response_should_contain: List[str] = None
    response_should_not_contain: List[str] = None
    expected_tools: List[ToolExpectation] = None


@dataclass
class TestResult:
    """
    Result of testing one conversation step against expectations.
    
    This captures what happened when we sent a message to the LLM and 
    validated the response against our YAML test expectations. It's the
    "report card" for one step in a conversation test.
    
    Attributes:
        success: Did the LLM response pass all validations?
        found_phrases: Required phrases that were found in response
        missing_phrases: Required phrases that were missing from response
        unexpected_phrases: Forbidden phrases that appeared in response
        found_tools: Expected tools that were called with correct parameters
        invalid_tools: Expected tools that were called with wrong parameters
        missing_tools: Expected tools that were not called
        unexpected_tools: Tools that were called but not expected
            (includes full tool info: {'tool': name, 'parameters': {...}})
        response_text: Full LLM response text for debugging
        response_length: Length of response in characters
    """
    success: bool
    found_phrases: List[str]
    missing_phrases: List[str]
    unexpected_phrases: List[str]
    found_tools: List[ToolExpectation]
    invalid_tools: List[ToolExpectation]
    missing_tools: List[ToolExpectation]
    unexpected_tools: List[Dict[str, Any]]
    response_text: str
    response_length: int


class DialecticRunner:
    """
    YAML-based test runner for prompt engineering validation.
    
    Attributes:
        results: Accumulates TestResult objects from all conversation steps executed.
            Used for final summary statistics and debugging.
    """
    
    results: List[TestResult]
    
    def __init__(self):
        """Initialize the test runner."""
        self.results = []
    
    def load_test_case(self, yaml_path: Path) -> TestCase:
        """Load a test case from a YAML file."""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Parse conversation steps
        conversation = []
        for step_data in data.get('conversation', []):
            expected_response = step_data.get('expected_response', {})
            
            # Parse expected tools into ToolExpectation objects
            expected_tools = []
            for tool_data in step_data.get('expected_tools', []):
                if isinstance(tool_data, str):
                    # Simple string format: just tool name
                    expected_tools.append(ToolExpectation(tool=tool_data))
                elif isinstance(tool_data, dict):
                    # Dict format: tool name + parameters
                    tool_name = tool_data.get('tool')
                    parameters = tool_data.get('parameters')
                    expected_tools.append(ToolExpectation(tool=tool_name, parameters=parameters))
            
            step = ConversationStep(
                user_message=step_data['user'],
                response_should_contain=expected_response.get('should_contain', []),
                response_should_not_contain=expected_response.get('should_not_contain', []),
                expected_tools=expected_tools
            )
            conversation.append(step)
        
        return TestCase(
            name=data['name'],
            description=data['description'],
            tags=data.get('tags', []),
            conversation=conversation
        )
    
    def _validate_tool_parameters(self, expectation: ToolExpectation, actual_tool: Dict[str, Any]) -> bool:
        """Validate that actual tool parameters match expectations. Returns True if all validations pass."""
        actual_params = actual_tool.get('parameters', {})
        expected_validations = expectation.parameters or {}
        all_valid = True
        
        for param_name, validation_rules in expected_validations.items():
            actual_value = actual_params.get(param_name)
            
            if isinstance(validation_rules, dict):
                # Handle should_contain validation
                if 'should_contain' in validation_rules:
                    required_phrases = validation_rules['should_contain']
                    if isinstance(actual_value, str):
                        for phrase in required_phrases:
                            if phrase.lower() in actual_value.lower():
                                print(f"  ✅ Parameter '{param_name}' contains: '{phrase}'")
                            else:
                                print(f"  ❌ Parameter '{param_name}' missing: '{phrase}'")
                                all_valid = False
                    else:
                        print(f"  ⚠️  Parameter '{param_name}' is not a string, can't check contains")
                        all_valid = False
                
                # Handle should_be validation  
                if 'should_be' in validation_rules:
                    expected_value = validation_rules['should_be']
                    if actual_value == expected_value:
                        print(f"  ✅ Parameter '{param_name}' = '{expected_value}'")
                    else:
                        print(f"  ❌ Parameter '{param_name}' = '{actual_value}', expected '{expected_value}'")
                        all_valid = False
            else:
                # Simple equality check
                if actual_value == validation_rules:
                    print(f"  ✅ Parameter '{param_name}' = '{validation_rules}'")
                else:
                    print(f"  ❌ Parameter '{param_name}' = '{actual_value}', expected '{validation_rules}'")
                    all_valid = False
        
        return all_valid
    
    async def run_conversation_step(self, step: ConversationStep) -> TestResult:
        """Run a single conversation step and validate the response."""
        print(f"🗣️  User: {step.user_message}")
        
        # Send message and collect response
        response_text = ""
        tools_used = []
        
        # Configure MCP servers for controlled test environment
        auth_server_path = os.path.join(os.path.dirname(__file__), "dialectic-authorization.py")
        
        # Extract expected tools from test step
        expected_tool_names = []
        for tool_exp in step.expected_tools:
            expected_tool_names.append(tool_exp.tool)
        
        # Configure Claude with authorization and memory bank
        options = ClaudeCodeOptions(
            mcp_servers={
                "memory-bank": {
                    "command": "uv",
                    "args": ["run", "python", "-m", "memory_bank"],
                    "env": {"SOCRATIC_SHELL_LOG": "/tmp/socratic-debug.log"}
                },
                "dialectic-auth": {
                    "command": "uv", 
                    "args": ["run", "python", auth_server_path, "--expected-tools"] + expected_tool_names
                }
            },
            permission_prompt_tool_name="mcp__dialectic-auth__authorize",
            allowed_tools=expected_tool_names + ["mcp__dialectic-auth__authorize"],
            cwd=os.getcwd()
        )
        
        print(f"🤖 Assistant: ", end="", flush=True)
        async for message in query(prompt=step.user_message, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text
                        print(block.text, end="", flush=True)
                    elif isinstance(block, ToolUseBlock):
                        tools_used.append({
                            'tool': block.name,
                            'parameters': block.input
                        })
                        print(f"\n🔧 Tool: {block.name}")
                        if block.input:
                            print(f"   Parameters: {block.input}")
                        print(f"🤖 Assistant: ", end="", flush=True)
        
        print()  # New line after streaming response
        
        # Validate response content
        found_phrases = []
        missing_phrases = []
        unexpected_phrases = []
        
        # Check required phrases
        for phrase in (step.response_should_contain or []):
            if phrase.lower() in response_text.lower():
                found_phrases.append(phrase)
                print(f"✅ Found required: '{phrase}'")
            else:
                missing_phrases.append(phrase)
                print(f"❌ Missing required: '{phrase}'")
        
        # Check forbidden phrases
        for phrase in (step.response_should_not_contain or []):
            if phrase.lower() in response_text.lower():
                unexpected_phrases.append(phrase)
                print(f"❌ Found forbidden: '{phrase}'")
            else:
                print(f"✅ Correctly avoided: '{phrase}'")
        
        # Validate tool usage - categorize like we do for phrases
        expected_tool_names = [expectation.tool for expectation in step.expected_tools]
        actual_tool_names = [tool['tool'] for tool in tools_used]
        
        found_tools = []
        invalid_tools = []
        missing_tools = []
        unexpected_tools = []
        
        # Check expected tools were called
        for expectation in step.expected_tools:
            if expectation.tool in actual_tool_names:
                print(f"🔧 Used expected tool: {expectation.tool}")
                
                # Validate tool parameters if specified
                if expectation.parameters:
                    actual_tool = next(t for t in tools_used if t['tool'] == expectation.tool)
                    params_valid = self._validate_tool_parameters(expectation, actual_tool)
                    if params_valid:
                        found_tools.append(expectation)
                    else:
                        print(f"  ⚠️  Tool '{expectation.tool}' called with invalid parameters")
                        invalid_tools.append(expectation)
                else:
                    # No parameter validation needed - tool was called correctly
                    found_tools.append(expectation)
            else:
                print(f"❌ Missing expected tool: {expectation.tool}")
                missing_tools.append(expectation)
        
        # Check for unexpected tools
        for actual_tool in tools_used:
            if actual_tool['tool'] not in expected_tool_names:
                print(f"⚠️  Unexpected tool used: {actual_tool['tool']}")
                unexpected_tools.append(actual_tool)
        
        # Determine success
        content_success = (len(missing_phrases) == 0 and len(unexpected_phrases) == 0)
        tools_success = (len(missing_tools) == 0 and len(invalid_tools) == 0 and len(unexpected_tools) == 0)
        success = content_success and tools_success
        
        return TestResult(
            success=success,
            found_phrases=found_phrases,
            missing_phrases=missing_phrases,
            unexpected_phrases=unexpected_phrases,
            found_tools=found_tools,
            invalid_tools=invalid_tools,
            missing_tools=missing_tools,
            unexpected_tools=unexpected_tools,
            response_text=response_text,
            response_length=len(response_text)
        )
    
    async def run_test_case(self, test_case: TestCase) -> bool:
        """Run a complete test case."""
        print(f"\n{'='*60}")
        print(f"🧪 Running: {test_case.name}")
        print(f"📝 {test_case.description}")
        if test_case.tags:
            print(f"🏷️  Tags: {', '.join(test_case.tags)}")
        print(f"{'='*60}")
        
        all_steps_passed = True
        
        for i, step in enumerate(test_case.conversation, 1):
            print(f"\n--- Step {i}/{len(test_case.conversation)} ---")
            
            result = await self.run_conversation_step(step)
            self.results.append(result)
            
            if result.success:
                print(f"✅ Step {i} PASSED")
            else:
                print(f"❌ Step {i} FAILED")
                all_steps_passed = False
                
                # Stop executing remaining steps - conversation state is now wrong
                remaining_steps = len(test_case.conversation) - i
                if remaining_steps > 0:
                    print(f"⏭️  Skipping {remaining_steps} remaining step(s) due to failure")
                break
        
        print(f"\n🎯 Test Case Result: {'PASSED' if all_steps_passed else 'FAILED'}")
        return all_steps_passed
    
    async def run_test_files(self, test_files: List[Path]) -> None:
        """Run multiple test files."""
        passed = 0
        total = len(test_files)
        
        for test_file in test_files:
            print(f"\n📁 Loading: {test_file}")
            try:
                test_case = self.load_test_case(test_file)
                success = await self.run_test_case(test_case)
                if success:
                    passed += 1
            except Exception as e:
                print(f"❌ Error running {test_file}: {e}")
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"🏁 FINAL RESULTS")
        print(f"{'='*60}")
        print(f"Passed: {passed}/{total} test files")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "No tests run")
        
        step_results = self.results
        step_passed = sum(1 for r in step_results if r.success)
        step_total = len(step_results)
        print(f"Individual Steps: {step_passed}/{step_total} passed")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Dialectic: YAML-based prompt engineering test runner")
    parser.add_argument('test_files', nargs='*', 
                       help='YAML test files to run (default: test-scripts/*.yaml)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Determine test files to run
    if args.test_files:
        test_files = [Path(f) for f in args.test_files]
    else:
        # Default to all YAML files in test-scripts/
        test_files = [Path(f) for f in glob.glob("test-scripts/*.yaml")]
    
    if not test_files:
        print("No test files found. Usage:")
        print("  python dialectic.py test-scripts/my-test.yaml")
        print("  python dialectic.py  # runs all test-scripts/*.yaml")
        return
    
    print("🚀 Starting Dialectic Test Runner")
    print(f"📂 Test files: {[str(f) for f in test_files]}")
    
    runner = DialecticRunner()
    await runner.run_test_files(test_files)


if __name__ == '__main__':
    asyncio.run(main())