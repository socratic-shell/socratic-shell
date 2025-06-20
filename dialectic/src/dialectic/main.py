"""Entry point for dialectic MCP server."""

from __future__ import annotations

import asyncio
import sys

from .server import DialecticServer


async def main() -> None:
    """Main entry point for the dialectic server."""
    server = DialecticServer()
    
    try:
        await server.run()
    except KeyboardInterrupt:
        print("Server shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)


def cli() -> None:
    """Sync entry point for command line usage."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()