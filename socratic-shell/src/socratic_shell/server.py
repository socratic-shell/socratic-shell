"""Socratic Shell MCP Server implementation."""

import logging
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

from .models import ConsolidateRequest, ReadInRequest, StoreBackRequest, Memory

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("socratic-shell")

server = Server("socratic-shell")


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
                    "category": {
                        "type": "string",
                        "description": "Category of memory (e.g., 'collaboration-pattern', 'user-preference', 'technical-insight')"
                    },
                    "importance": {
                        "type": "string",
                        "description": "Importance level: low, medium, high",
                        "enum": ["low", "medium", "high"],
                        "default": "medium"
                    }
                },
                "required": ["content", "category"]
            }
        ),
        Tool(
            name="read_in",
            description="Retrieve relevant memories based on current context or query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What kind of information to retrieve"
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
        logger.info(f"🧠 CONSOLIDATE [{request.category}] (importance: {request.importance})")
        logger.info(f"   Content: {request.content}")
        
        return [
            TextContent(
                type="text",
                text=f"✅ Consolidated memory in category '{request.category}' with importance '{request.importance}'"
            )
        ]

    elif name == "read_in":
        request = ReadInRequest(**arguments)
        logger.info(f"🔍 READ_IN Query: {request.query}")
        if request.context:
            logger.info(f"   Context: {request.context}")
        
        # Return some dummy memories for now
        dummy_memories = [
            Memory(
                id="mem_001",
                content="Niko prefers being asked questions when I'm uncertain rather than me making assumptions",
                category="collaboration-pattern",
                relevance_score=0.9
            ),
            Memory(
                id="mem_002", 
                content="When I feel 'protective mode' anxiety, that's a signal to present options instead of making safe choices",
                category="collaboration-pattern",
                relevance_score=0.8
            )
        ]
        
        memory_text = "\n".join([
            f"• [{mem.category}] {mem.content} (relevance: {mem.relevance_score})"
            for mem in dummy_memories
        ])
        
        return [
            TextContent(
                type="text",
                text=f"📚 Retrieved memories for '{request.query}':\n\n{memory_text}"
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