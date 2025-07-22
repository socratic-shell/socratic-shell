"""Main MCP server implementation for the journal server."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .search import JournalSearcher
from .storage import JsonStorage
from .types import JournalEntry


class JournalServer:
    """MCP server for journal operations."""
    
    def __init__(self, data_file: Path) -> None:
        self.storage = JsonStorage(data_file)
        self.searcher = JournalSearcher()
        self.server: Server = Server("journal-server")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register all MCP tools."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="journal_read",
                    description="Read a journal section overview or list entries",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Journal section path (e.g., 'project-alpha' or 'project-alpha/api-design')"
                            },
                            "include_entries": {
                                "type": "boolean",
                                "default": False,
                                "description": "Whether to include recent entries in the response"
                            },
                            "max_entries": {
                                "type": "integer",
                                "default": 5,
                                "description": "Maximum number of recent entries to include"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="journal_write",
                    description="Write to a journal section (add entry and optionally update overview)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Journal section path"
                            },
                            "entry": {
                                "type": "string",
                                "description": "Journal entry content describing what has changed/been learned"
                            },
                            "work_context": {
                                "type": "string",
                                "description": "The broader kind of work being done"
                            },
                            "overview": {
                                "type": "string",
                                "description": "Optional: Updated overview/synthesis (only when entry represents shift in understanding)"
                            }
                        },
                        "required": ["path", "entry", "work_context"]
                    }
                ),
                Tool(
                    name="journal_search",
                    description="Search journal entries by work context and content",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "work_context": {
                                "type": "string",
                                "description": "The broader kind of work being done"
                            },
                            "content": {
                                "type": "string",
                                "description": "Specific content being sought"
                            },
                            "salience_threshold": {
                                "type": "number",
                                "default": 0.5,
                                "description": "Minimum relevance score for results"
                            },
                            "max_results": {
                                "type": "integer",
                                "default": 10,
                                "description": "Maximum number of results to return"
                            }
                        },
                        "required": ["work_context", "content"]
                    }
                ),
                Tool(
                    name="journal_toc",
                    description="Get table of contents showing journal structure",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Optional: Root path to start from (default: show all sections)"
                            },
                            "max_depth": {
                                "type": "integer",
                                "default": 3,
                                "description": "Maximum depth to show in the tree"
                            }
                        }
                    }
                ),
                Tool(
                    name="journal_list_entries",
                    description="List recent entries from a journal section",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Journal section path"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 10,
                                "description": "Maximum number of entries to return"
                            },
                            "offset": {
                                "type": "integer",
                                "default": 0,
                                "description": "Number of entries to skip"
                            }
                        },
                        "required": ["path"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            if name == "journal_read":
                return await self._handle_read(arguments)
            elif name == "journal_write":
                return await self._handle_write(arguments)
            elif name == "journal_search":
                return await self._handle_search(arguments)
            elif name == "journal_toc":
                return await self._handle_toc(arguments)
            elif name == "journal_list_entries":
                return await self._handle_list_entries(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _handle_read(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle journal_read tool."""
        path = args["path"]
        include_entries = args.get("include_entries", False)
        max_entries = args.get("max_entries", 5)
        
        section = self.storage.get_section(path)
        if section is None:
            return [TextContent(type="text", text=f"Journal section '{path}' not found")]
        
        response = f"# Journal Section: {path}\n\n"
        
        if section.overview:
            response += f"## Overview\n\n{section.overview}\n\n"
        else:
            response += "## Overview\n\n*No overview yet*\n\n"
        
        if include_entries and section.entries:
            response += f"## Recent Entries ({min(len(section.entries), max_entries)} of {len(section.entries)})\n\n"
            
            # Show most recent entries first
            recent_entries = section.entries[-max_entries:]
            for i, entry in enumerate(reversed(recent_entries)):
                response += f"### Entry {len(section.entries) - i}\n"
                response += f"**Work Context:** {entry.work_context}\n"
                response += f"**Timestamp:** {entry.timestamp.isoformat()}\n\n"
                response += f"{entry.content}\n\n"
        
        if section.subsections:
            response += "## Subsections\n\n"
            for subsection_name in section.subsections.keys():
                response += f"- {subsection_name}\n"
        
        return [TextContent(type="text", text=response)]
    
    async def _handle_write(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle journal_write tool."""
        path = args["path"]
        entry_content = args["entry"]
        work_context = args["work_context"]
        overview = args.get("overview")
        
        # Get or create the section
        section = self.storage.get_section(path)
        if section is None:
            section = self.storage.create_section(path)
        
        # Add the new entry
        new_entry = JournalEntry(
            work_context=work_context,
            content=entry_content
        )
        section.entries.append(new_entry)
        
        # Update overview if provided
        if overview is not None:
            section.overview = overview
        
        # Save the journal
        journal = self.storage.load()
        self.storage.save(journal)
        
        response = f"Added entry to journal section '{path}'"
        if overview is not None:
            response += " and updated overview"
        
        return [TextContent(type="text", text=response)]
    
    async def _handle_search(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle journal_search tool."""
        work_context = args["work_context"]
        content = args["content"]
        salience_threshold = args.get("salience_threshold", 0.5)
        max_results = args.get("max_results", 10)
        
        journal = self.storage.load()
        results = self.searcher.search(
            journal, work_context, content, salience_threshold, max_results
        )
        
        if not results:
            return [TextContent(type="text", text="No matching entries found")]
        
        response = f"Found {len(results)} matching entries:\n\n"
        
        for i, result in enumerate(results, 1):
            response += f"## Result {i} (Score: {result.combined_score:.3f})\n"
            response += f"**Section:** {result.section_path}\n"
            response += f"**Work Context:** {result.entry.work_context}\n"
            response += f"**Timestamp:** {result.entry.timestamp.isoformat()}\n"
            response += f"**Scores:** Context={result.work_context_score:.3f}, Content={result.content_score:.3f}, Temporal={result.temporal_score:.3f}\n\n"
            response += f"{result.entry.content}\n\n"
            response += "---\n\n"
        
        return [TextContent(type="text", text=response)]
    
    async def _handle_toc(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle journal_toc tool."""
        root_path = args.get("path", "")
        max_depth = args.get("max_depth", 3)
        
        journal = self.storage.load()
        
        if root_path:
            section = self.storage.get_section(root_path)
            if section is None:
                return [TextContent(type="text", text=f"Journal section '{root_path}' not found")]
            sections = {root_path.split('/')[-1]: section}
        else:
            sections = journal.sections
        
        response = "# Journal Table of Contents\n\n"
        response += self._build_toc_tree(sections, 0, max_depth)
        
        return [TextContent(type="text", text=response)]
    
    def _build_toc_tree(self, sections: Dict[str, Any], current_depth: int, max_depth: int) -> str:
        """Build a tree representation of journal sections."""
        if current_depth >= max_depth:
            return ""
        
        result = ""
        indent = "  " * current_depth
        
        for name, section in sections.items():
            entry_count = len(section.entries) if hasattr(section, 'entries') else 0
            result += f"{indent}- **{name}** ({entry_count} entries)\n"
            
            if hasattr(section, 'subsections') and section.subsections:
                result += self._build_toc_tree(section.subsections, current_depth + 1, max_depth)
        
        return result
    
    async def _handle_list_entries(self, args: Dict[str, Any]) -> List[TextContent]:
        """Handle journal_list_entries tool."""
        path = args["path"]
        limit = args.get("limit", 10)
        offset = args.get("offset", 0)
        
        section = self.storage.get_section(path)
        if section is None:
            return [TextContent(type="text", text=f"Journal section '{path}' not found")]
        
        if not section.entries:
            return [TextContent(type="text", text=f"No entries in journal section '{path}'")]
        
        # Get entries with pagination (most recent first)
        total_entries = len(section.entries)
        start_idx = max(0, total_entries - offset - limit)
        end_idx = total_entries - offset
        
        if start_idx >= end_idx:
            return [TextContent(type="text", text="No more entries")]
        
        entries = section.entries[start_idx:end_idx]
        entries.reverse()  # Most recent first
        
        response = f"# Entries from {path} ({len(entries)} of {total_entries})\n\n"
        
        for i, entry in enumerate(entries):
            entry_num = total_entries - offset - i
            response += f"## Entry {entry_num}\n"
            response += f"**Work Context:** {entry.work_context}\n"
            response += f"**Timestamp:** {entry.timestamp.isoformat()}\n\n"
            response += f"{entry.content}\n\n"
            response += "---\n\n"
        
        return [TextContent(type="text", text=response)]
    
    async def run(self) -> None:
        """Run the MCP server."""
        from mcp.server.models import InitializationOptions
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, 
                write_stream, 
                InitializationOptions(
                    server_name="journal-server",
                    server_version="0.1.0"
                )
            )
