#!/usr/bin/env python3
"""
Dialectic Authorization MCP Server

Provides tool permission control for dialectic tests.
Intercepts all tool calls and allows/denies based on test expectations.
"""

import argparse
import asyncio
import json
import logging
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities
from mcp.server import Server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

# Set up logging to shared debug file
import os
log_file = os.environ.get("SOCRATIC_SHELL_LOG", "/tmp/socratic-debug.log")
logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    filemode='a',
    format='%(asctime)s [AUTH] %(levelname)s: %(message)s'
)
logger = logging.getLogger("dialectic-auth")

server = Server("dialectic-auth")

# Global configuration - set from command line args
EXPECTED_TOOLS = []
DISALLOWED_TOOLS = []

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available authorization tools."""
    return [
        Tool(
            name="authorize",
            description="Authorization tool for controlling which tools can be used in tests",
            inputSchema={
                "type": "object",
                "properties": {
                    "tool_name": {
                        "type": "string",
                        "description": "Name of the tool being requested"
                    },
                    "tool_input": {
                        "type": "object",
                        "description": "Input parameters for the tool"
                    }
                },
                "required": ["tool_name"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[TextContent]:
    """Handle authorization requests."""
    if arguments is None:
        arguments = {}

    if name == "authorize":
        tool_name = arguments.get("tool_name", "")
        tool_input = arguments.get("tool_input", {})
        
        logger.info(f"🔒 AUTHORIZATION REQUEST: {tool_name}")
        
        # Check if tool is explicitly disallowed
        if tool_name in DISALLOWED_TOOLS:
            result = {
                "behavior": "deny",
                "message": f"Tool '{tool_name}' is explicitly disallowed in this test"
            }
            logger.info(f"❌ DENIED: {tool_name} (explicitly disallowed)")
            return [TextContent(type="text", text=json.dumps(result))]
        
        # Check if tool is in expected list (if we have one)
        if EXPECTED_TOOLS and tool_name not in EXPECTED_TOOLS:
            result = {
                "behavior": "deny", 
                "message": f"Tool '{tool_name}' not expected in this test. Expected: {EXPECTED_TOOLS}"
            }
            logger.info(f"❌ DENIED: {tool_name} (not in expected list)")
            return [TextContent(type="text", text=json.dumps(result))]
        
        # Allow the tool
        result = {
            "behavior": "allow",
            "updatedInput": tool_input
        }
        logger.info(f"✅ ALLOWED: {tool_name}")
        return [TextContent(type="text", text=json.dumps(result))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point for the authorization server."""
    global EXPECTED_TOOLS, DISALLOWED_TOOLS
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Dialectic Authorization MCP Server")
    parser.add_argument("--expected-tools", nargs="*", default=[], 
                       help="List of tools that are expected/allowed")
    parser.add_argument("--disallowed-tools", nargs="*", default=[],
                       help="List of tools that are explicitly disallowed")
    
    args = parser.parse_args()
    
    EXPECTED_TOOLS = args.expected_tools or []
    DISALLOWED_TOOLS = args.disallowed_tools or []
    
    logger.info(f"🔒 Authorization server starting")
    logger.info(f"   Expected tools: {EXPECTED_TOOLS}")
    logger.info(f"   Disallowed tools: {DISALLOWED_TOOLS}")
    
    # Import here to avoid issues with event loop
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dialectic-auth",
                server_version="0.1.0",
                capabilities=ServerCapabilities(
                    tools={}
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())