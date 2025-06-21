"""Main entry point for socratic-shell MCP server."""

import asyncio
from .server import main


def main_sync():
    """Synchronous entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    main_sync()