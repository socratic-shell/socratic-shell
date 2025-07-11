"""Socratic Shell MCP Server implementation."""

import json
import logging
import os
from pathlib import Path
from typing import Any, Sequence
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

from .models import ConsolidateRequest, ReadInRequest, StoreBackRequest, Memory

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
stemmer = PorterStemmer()

server = Server("socratic-shell")


def find_all_memories_dirs():
    """Walk up from CWD to collect all .memories directories."""
    memories_dirs = []
    current = Path.cwd()
    while current != current.parent:
        memories_dir = current / ".memories"
        if memories_dir.exists() and memories_dir.is_dir():
            memories_dirs.append(memories_dir)
        current = current.parent
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
    for memories_dir in find_all_memories_dirs():
        logger.info(f"Loading memories from {memories_dir}")
        all_memories.extend(load_memories(memories_dir))
    return all_memories


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
            name="consolidate",
            description="Store important insights, collaboration patterns, or knowledge for future retrieval",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The information to consolidate into memory"
                    },
                    "situation": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Multiple situation aspects as separate phrases, e.g., ['debugging payment system', 'feeling frustrated', 'third concurrency issue this week', 'after team meeting']"
                    },
                    "importance": {
                        "type": "string",
                        "description": "Importance level: low, medium, high",
                        "enum": ["low", "medium", "high"],
                        "default": "medium"
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
                    },
                    "context": {
                        "type": "string",
                        "description": "Additional context about current situation"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="store_back",
            description="Update existing memory with new insights or refinements",
            inputSchema={
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "string",
                        "description": "ID of the memory to update"
                    },
                    "updated_content": {
                        "type": "string",
                        "description": "Updated or refined content"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for the update"
                    }
                },
                "required": ["memory_id", "updated_content"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[TextContent]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    if name == "consolidate":
        request = ConsolidateRequest(**arguments)
        logger.info(f"🧠 CONSOLIDATE (importance: {request.importance})")
        logger.info(f"   Content: {request.content}")
        
        return [
            TextContent(
                type="text",
                text=f"✅ Consolidated memory with importance '{request.importance}'"
            )
        ]

    elif name == "read_in":
        request = ReadInRequest(**arguments)
        logger.info(f"🔍 READ_IN Query: {request.query}")
        if request.context:
            logger.info(f"   Context: {request.context}")
        
        # Debug logging
        if debug_logger:
            debug_logger.info(f"READ_IN called with query='{request.query}', situation={request.situation}")
        
        # Load and search memories
        all_memories = load_all_memories()
        if debug_logger:
            debug_logger.info(f"Loaded {len(all_memories)} total memories")
            
        matching_memories = search_memories(request.query, request.situation, all_memories)
        
        if debug_logger:
            debug_logger.info(f"Found {len(matching_memories)} matching memories")
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

    elif name == "store_back":
        request = StoreBackRequest(**arguments)
        logger.info(f"📝 STORE_BACK Memory ID: {request.memory_id}")
        logger.info(f"   Updated content: {request.updated_content}")
        if request.reason:
            logger.info(f"   Reason: {request.reason}")
        
        return [
            TextContent(
                type="text",
                text=f"✅ Updated memory {request.memory_id}"
            )
        ]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the server."""
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