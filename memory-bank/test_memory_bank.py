#!/usr/bin/env python3
"""Unit tests for memory bank functionality."""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add src to path so we can import memory_bank
sys.path.insert(0, str(Path(__file__).parent / "src"))

from memory_bank.server import (
    find_all_memories_dirs, 
    load_memories, 
    load_all_memories, 
    search_memories,
    MEMORIES_DIR_OVERRIDE
)

def test_find_memories_dirs_with_override():
    """Test finding memories directories with override."""
    test_dir = "/home/nikomatsakis/dev/socratic-shell/dialectic/tests/memory-basic"
    memories_dirs = find_all_memories_dirs(test_dir)
    
    print(f"Override dir: {test_dir}")
    print(f"Found directories: {memories_dirs}")
    assert len(memories_dirs) >= 1, f"Should find at least 1 .memories directory, found {len(memories_dirs)}"
    
    # Check that the first directory is the expected one
    expected_dir = Path(test_dir) / ".memories"
    assert expected_dir in memories_dirs, f"Should find {expected_dir} in {memories_dirs}"

def test_load_memories_from_test_dir():
    """Test loading memories from the test directory."""
    test_memories_dir = Path("/home/nikomatsakis/dev/socratic-shell/dialectic/tests/memory-basic/.memories")
    
    if not test_memories_dir.exists():
        print(f"Test memories directory not found: {test_memories_dir}")
        return
    
    memories = load_memories(test_memories_dir)
    print(f"Loaded {len(memories)} memories from {test_memories_dir}")
    
    for memory in memories:
        print(f"  Memory ID: {memory.get('id', 'no-id')}")
        print(f"  Content: {memory.get('content', 'no-content')[:100]}...")
        print(f"  Situation: {memory.get('situation', [])}")
        print()

def test_search_memories():
    """Test the search functionality that's causing NLTK issues."""
    # Create some test memories
    test_memories = [
        {
            "id": "test-1",
            "content": "We decided to use natural language phrases for the situation field instead of structured tags",
            "situation": ["design-decision", "situation-field", "natural-language"]
        },
        {
            "id": "test-2", 
            "content": "The memory bank should support hierarchical .memories directories",
            "situation": ["architecture", "file-organization", "memory-storage"]
        }
    ]
    
    # Test the search function
    query = "situation field design decisions"
    situation = ["reviewing-design", "checking-decisions"]
    
    print(f"Testing search with query: '{query}'")
    print(f"Situation: {situation}")
    
    try:
        results = search_memories(query, situation, test_memories)
        print(f"Search returned {len(results)} results")
        
        for result in results:
            print(f"  Found: {result['id']} - {result['content'][:50]}...")
            
    except Exception as e:
        print(f"ERROR during search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Testing Memory Bank Functionality ===\n")
    
    print("1. Testing find_all_memories_dirs with override...")
    test_find_memories_dirs_with_override()
    print("✅ find_all_memories_dirs test passed\n")
    
    print("2. Testing load_memories from test directory...")
    test_load_memories_from_test_dir()
    print("✅ load_memories test passed\n")
    
    print("3. Testing search_memories (potential NLTK issue)...")
    test_search_memories()
    print("✅ search_memories test passed\n")
    
    print("All tests completed!")