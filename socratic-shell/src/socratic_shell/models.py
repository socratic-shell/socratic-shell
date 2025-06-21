"""Pydantic models for socratic-shell MCP server."""

from typing import Optional
from pydantic import BaseModel


class ConsolidateRequest(BaseModel):
    """Request to consolidate information into memory."""
    content: str
    category: str
    importance: Optional[str] = "medium"


class ReadInRequest(BaseModel):
    """Request to read in relevant memories."""
    query: str
    context: Optional[str] = None


class StoreBackRequest(BaseModel):
    """Request to update existing memory with new insights."""
    memory_id: str
    updated_content: str
    reason: Optional[str] = None


class Memory(BaseModel):
    """A memory object returned from the system."""
    id: str
    content: str
    category: str
    relevance_score: Optional[float] = None
    last_accessed: Optional[str] = None