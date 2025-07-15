"""Socratic Shell MCP Server implementation."""

import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence, Dict
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities
from mcp.server import NotificationOptions, Server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

import nltk
from nltk.stem import PorterStemmer

from .models import WriteMemoryRequest, ReadInRequest, Memory

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("socratic-shell")

# Debug logging to file if environment variable is set
debug_log_path = os.environ.get('SOCRATIC_SHELL_LOG')
debug_logger = None
if debug_log_path:
    debug_logger = logging.getLogger("socratic-shell-debug")
    debug_handler = logging.FileHandler(debug_log_path)
    debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    debug_logger.addHandler(debug_handler)
    debug_logger.setLevel(logging.INFO)
    debug_logger.info("=== Socratic Shell Debug Log Started ===")

# Initialize NLTK (download required data)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
stemmer = PorterStemmer()

server = Server("socratic-shell")

# Global configuration - set during server startup via command line arguments
# MEMORIES_DIR_OVERRIDE: When set via --memories-dir, overrides the directory search
# for .memories folders. Normally searches from CWD upward to root.
MEMORIES_DIR_OVERRIDE = None

# SIMULATED_MODE: When set via --simulated flag, prevents actual file writes.
# All write operations go to in-memory store instead of disk.
SIMULATED_MODE = False

# 💡: Memory cache for session persistence - tracks memories that have been
# read or written during this session. Used for:
# 1. Optimistic concurrency control (must read before update)
# 2. Simulated mode storage (writes go here instead of disk)
# 3. Making simulated writes visible to subsequent read_in calls
# Maps memory ID -> memory data dict (same format as JSON files)
read_cache: Dict[str, Dict[str, Any]] = {}


def find_all_memories_dirs(override_dir=None):
    """Walk up from CWD to collect all .memories directories.
    
    Args:
        override_dir: Optional directory to search from instead of CWD
    """
    memories_dirs = []
    current = Path(override_dir) if override_dir else Path.cwd()
    if debug_logger:
        debug_logger.info(f"Starting search from: {current}")
    while current != current.parent:
        memories_dir = current / ".memories"
        if debug_logger:
            debug_logger.info(f"Checking for .memories at: {memories_dir}")
        if memories_dir.exists() and memories_dir.is_dir():
            if debug_logger:
                debug_logger.info(f"Found .memories directory: {memories_dir}")
            memories_dirs.append(memories_dir)
        current = current.parent
    if debug_logger:
        debug_logger.info(f"Total .memories directories found: {len(memories_dirs)}")
    return memories_dirs


def load_memories(memories_dir):
    """Load all JSON files from a memories directory."""
    memories = []
    for file_path in memories_dir.glob("*.json"):
        try:
            with open(file_path) as f:
                memory_data = json.load(f)
                # Add file path as id if not present
                if "id" not in memory_data:
                    memory_data["id"] = file_path.stem
                memories.append(memory_data)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Failed to load memory from {file_path}: {e}")
    return memories


def load_all_memories():
    """Load memories from all .memories directories."""
    all_memories = []
    for memories_dir in find_all_memories_dirs(MEMORIES_DIR_OVERRIDE):
        logger.info(f"Loading memories from {memories_dir}")
        all_memories.extend(load_memories(memories_dir))
    
    # 💡: Include cached memories in search results (includes simulated writes)
    all_memories.extend(read_cache.values())
    
    return all_memories


def get_memory_write_dir():
    """Get the .memories directory in current working directory for new memories.
    
    Always writes new memories to CWD/.memories, creating it if needed.
    """
    current_dir = Path(MEMORIES_DIR_OVERRIDE) if MEMORIES_DIR_OVERRIDE else Path.cwd()
    memories_dir = current_dir / ".memories"
    memories_dir.mkdir(exist_ok=True)
    return memories_dir


def write_memory(content, situation=None, memory_id=None):
    """Write memory to storage with optimistic concurrency control.
    
    Args:
        content: Memory content to store
        situation: Optional context phrases for retrieval
        memory_id: Optional memory ID for updates (requires prior read)
        
    Returns:
        Memory ID of written memory
        
    Raises:
        ValueError: If memory_id provided but not in read cache or content changed
    """
    global read_cache
    
    if memory_id:
        # 💡: Update existing memory - check optimistic concurrency control
        # Check if memory was read during this session (applies to both modes)
        if memory_id not in read_cache:
            raise ValueError(f"Memory {memory_id} must be read before updating")
        
        if SIMULATED_MODE:
            # In simulated mode, update the cache directly (no file operations)
            cached_memory = read_cache[memory_id]
            memory_data = {
                "id": memory_id,
                "content": content,
                "situation": situation or cached_memory.get('situation', []),
                "created_at": cached_memory.get('created_at', datetime.now().isoformat())
            }
            read_cache[memory_id] = memory_data
            return memory_id
        
        # Find the memory file
        memory_file = None
        for memories_dir in find_all_memories_dirs(MEMORIES_DIR_OVERRIDE):
            potential_file = memories_dir / f"{memory_id}.json"
            if potential_file.exists():
                memory_file = potential_file
                break
        
        if not memory_file:
            raise ValueError(f"Memory {memory_id} does not exist")
        
        # Check if file content matches our cached version
        try:
            with open(memory_file) as f:
                current_content = json.load(f)
            
            cached_content = read_cache[memory_id]
            if current_content.get('content') != cached_content.get('content'):
                # 💡: Concurrent modification detected - update cache and return new content
                read_cache[memory_id] = current_content.copy()
                raise ValueError(f"Memory {memory_id} has been modified: {current_content['content']}")
        except (json.JSONDecodeError, OSError) as e:
            raise ValueError(f"Error reading memory {memory_id}: {e}")
        
        # Update the memory
        updated_memory = {
            "id": memory_id,
            "content": content,
            "situation": situation or current_content.get('situation', []),
            "created_at": current_content.get('created_at', datetime.now().isoformat())
        }
        
        with open(memory_file, 'w') as f:
            json.dump(updated_memory, f, indent=2)
        
        # Update read cache
        read_cache[memory_id] = updated_memory.copy()
        
        return memory_id
    
    else:
        # 💡: Create new memory with generated UUID
        new_id = str(uuid.uuid4())
        
        memory_data = {
            "id": new_id,
            "content": content,
            "situation": situation or [],
            "created_at": datetime.now().isoformat()
        }
        
        if SIMULATED_MODE:
            # In simulated mode, just add to cache
            read_cache[new_id] = memory_data
            return new_id
        
        # Write new memories to current directory
        memories_dir = get_memory_write_dir()
        memory_file = memories_dir / f"{new_id}.json"
        
        with open(memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
        
        # Add to read cache for potential future updates
        read_cache[new_id] = memory_data.copy()
        
        return new_id


def search_memories(query, situation_list, memories):
    """Search memories using keyword matching with stemming."""
    # Combine query and situation aspects into search terms
    search_text = query if query.strip() else ""
    if situation_list:
        search_text += " " + " ".join(situation_list)
    
    if not search_text.strip():
        return []
        
    # Tokenize and stem all search terms
    search_words = nltk.word_tokenize(search_text.lower())
    search_stems = [stemmer.stem(word) for word in search_words]
    
    results = []
    for memory in memories:
        # Score situation and content separately
        situation_text = ' '.join(memory.get('situation', []))
        situation_stems = [stemmer.stem(word) for word in nltk.word_tokenize(situation_text.lower())]
        situation_matches = sum(1 for stem in search_stems if stem in situation_stems)
        
        content_stems = [stemmer.stem(word) for word in nltk.word_tokenize(memory['content'].lower())]
        content_matches = sum(1 for stem in search_stems if stem in content_stems)
        
        # Weight situation higher since it captures relevant context
        total_score = (situation_matches * 2) + content_matches
        
        if total_score > 0:
            results.append((memory, total_score))
    
    # Return top 5 memories
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    return [memory for memory, _ in sorted_results[:5]]


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="write-memory",
            description="Store or update memory content. For new memories, omit the id parameter. For updates, provide the id of a memory that has been previously read via read_in.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The memory content to store"
                    },
                    "situation": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Context phrases for better retrieval, e.g., ['debugging payment system', 'feeling frustrated', 'third concurrency issue this week']"
                    },
                    "id": {
                        "type": "string",
                        "description": "Memory ID for updates (omit for new memories)"
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="read_in",
            description="Retrieve memories from similar past situations. Describe your current situation naturally, including: what you're working on, emotional state, recent events, time context, and any other relevant details. Example: 'Debugging race condition in payment system, frustrated because it's the third concurrency issue this week, late afternoon after team meeting about Q2 priorities'. The richer your situational description, the better the memory matches.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What kind of information to retrieve"
                    },
                    "situation": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Current situation as multiple aspects, e.g., ['debugging race condition', 'feeling frustrated', 'third time this week', 'after team meeting']"
                    }
                },
                "required": ["query"]
            }
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[TextContent]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    if name == "read_in":
        request = ReadInRequest(**arguments)
        logger.info(f"🔍 READ_IN Query: {request.query}")
        
        # Debug logging
        if debug_logger:
            debug_logger.info(f"READ_IN called with query='{request.query}', situation={request.situation}")
        
        # Load and search memories
        all_memories = load_all_memories()
        if debug_logger:
            debug_logger.info(f"Loaded {len(all_memories)} total memories")
            
        matching_memories = search_memories(request.query, request.situation, all_memories)
        
        # 💡: Populate read cache with returned memories to enable write-memory updates
        for memory in matching_memories:
            if 'id' in memory:
                read_cache[memory['id']] = memory.copy()
        
        if debug_logger:
            debug_logger.info(f"Found {len(matching_memories)} matching memories")
            debug_logger.info(f"Updated read cache with {len(matching_memories)} memories")
            for i, mem in enumerate(matching_memories):
                debug_logger.info(f"  Memory {i+1}: {mem.get('id', 'no-id')} - {mem['content'][:100]}...")
        
        if not matching_memories:
            result_text = f"📚 No memories found for '{request.query}'"
            if debug_logger:
                debug_logger.info(f"Response: {result_text}")
            return [
                TextContent(
                    type="text",
                    text=result_text
                )
            ]
        
        # Format results
        memory_text = "\n".join([
            f"• {mem['content']}"
            for mem in matching_memories
        ])
        
        result_text = f"📚 Retrieved {len(matching_memories)} memories for '{request.query}':\n\n{memory_text}"
        if debug_logger:
            debug_logger.info(f"Response: {result_text}")
        
        return [
            TextContent(
                type="text",
                text=result_text
            )
        ]

    elif name == "write-memory":
        request = WriteMemoryRequest(**arguments)
        logger.info(f"💾 WRITE-MEMORY")
        logger.info(f"   Content: {request.content[:100]}{'...' if len(request.content) > 100 else ''}")
        if request.id:
            logger.info(f"   Memory ID: {request.id}")
        
        try:
            memory_id = write_memory(
                content=request.content,
                situation=request.situation,
                memory_id=request.id
            )
            
            return [
                TextContent(
                    type="text",
                    text=f"✅ Memory stored with ID: {memory_id}"
                )
            ]
        except ValueError as e:
            return [
                TextContent(
                    type="text", 
                    text=f"❌ Error: {str(e)}"
                )
            ]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the server."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Memory Bank MCP Server")
    parser.add_argument("--memories-dir", help="Override directory to search for .memories directories")
    parser.add_argument("--simulated", action="store_true", help="Run in simulated mode (no file writes)")
    args = parser.parse_args()
    
    # Set global configuration
    global MEMORIES_DIR_OVERRIDE, SIMULATED_MODE
    if args.memories_dir:
        MEMORIES_DIR_OVERRIDE = args.memories_dir
        if debug_logger:
            debug_logger.info(f"Using memories directory override: {MEMORIES_DIR_OVERRIDE}")
    
    if args.simulated:
        SIMULATED_MODE = True
        logger.info("🧪 SIMULATED MODE: Memory operations will not write to disk")
        if debug_logger:
            debug_logger.info("Running in simulated mode - no file system changes")
    
    # Import here to avoid issues with event loop
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="socratic-shell",
                server_version="0.1.0",
                capabilities=ServerCapabilities(
                    tools={}
                ),
            ),
        )