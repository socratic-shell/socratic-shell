#!/bin/bash

# Run the dialectic MCP server
# Usage: ./run-dialectic.sh

set -e
cd dialectic

# Ensure dependencies are installed
uv sync --quiet

# Run the dialectic server (exec ensures proper stdin/stdout for MCP)
exec uv run python -m dialectic