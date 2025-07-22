"""CLI entry point for the journal server."""

import argparse
import asyncio
from pathlib import Path

from .server import JournalServer


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Journal MCP Server - A memory system that emerges from collaborative understanding"
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=Path("./journal.json"),
        help="Path to the JSON data file (default: ./journal.json)",
    )
    
    args = parser.parse_args()
    
    # Create and run the server
    server = JournalServer(data_file=args.data_file)
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
